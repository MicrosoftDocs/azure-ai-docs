---
title: Build an agentic retrieval solution
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/21/2025
---

# Build an agent-to-agent retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article describes an approach or pattern for building a solution that uses Azure AI Search for knowledge retrieval, and how to integrate knowledge retrieval into a custom solution that includes Azure AI Agent.

This article supports the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python sample on GitHub.

This exercise differs from the [Agentic Retrieval Quickstart](search-get-started-agentic-retrieval.md) in how it uses Azure AI Agent to retrieve data from the index, and how it uses an agent tool for orchestration. If you want to understand the retrieval pipeline in its simplest form, begin with the quickstart.

## Prerequisites

The following resources are required for this design pattern:

+ Azure AI Search, basic tier or higher, in a [region that provides semantic ranking](search-region-support.md).

+ A search index that satisfies the [index criteria for agentic retrieval](search-agentic-retrieval-how-to-index.md).

+ A project in Azure AI Foundry, with an Azure AI Agent in a Basic setup.

  Follow the steps in [Create a project for Azure AI Foundry](/azure/ai-foundry/how-to/create-projects). Creating the project also creates the Azure AI Foundry resource in your Azure subscription.

+ Azure OpenAI with a deployment of one of the chat completion models listed below. We recommend a minimum of 100,000 token capacity for your model. You can find capacity and the rate limit in the model deployments list in the Azure AI Foundry portal. You can also deploy text embedding models if you want [vectorization at query time](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries).

### Supported large language models

Use one of the following chat completion models with your AI agent:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`

### Package version requirements

Use a package version that provides preview functionality. See the [`requirements.txt`](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/agentic-retrieval-pipeline-example/requirements.txt) file for more packages used in the example solution.

```
azure-ai-projects==1.0.0b11
azure-ai-agents==1.0.0
azure-search-documents==11.6.0b12
```

### Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, you can use [key-based authentication](search-security-api-keys.md) instead.

Configure access to each resource identified in this section.

### [**Azure AI Search**](#tab/search-perms)

Azure AI Search provides the agentic retrieval pipeline. Configure access for yourself, your app, and your search service for downstream access to models.

1. [Enable role-based access](search-security-enable-roles.md).
1. [Configure a managed identity](search-howto-managed-identities-data-sources.md).
1. [Assign roles](search-security-rbac.md):

   + For local testing, you must have **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader** role assignments to create, load, and retrieve on Azure AI Search.

   + For integrated operations, ensure that all clients using the retrieval pipeline (agent and tool) have **Search Index Data Reader** role assignments for sending retrieval requests.

### [**Azure AI Foundry**](#tab/foundry-perms)

Azure AI Foundry hosts the AI agent and tool. Permissions are needed to create and use the resource.

+ You must be an **Owner** of your Azure subscription to create the project and resource.

+ For local testing, you must be an **Azure AI User** to access chat completion models deployed to the Foundry resource. This assignment is conferred automatically for **Owners** when you create the resource. Other users need a specific role assignment. For more information, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

+ For integrated operations, ensure your [search service identity](search-howto-managed-identities-data-sources.md) has an **Azure AI User** role assignment on the Foundry resource.

### [**Azure OpenAI**](#tab/openai-perms)

Azure OpenAI hosts the models used by the agentic retrieval pipeline. Configure access for yourself and for the search service.

+ For local testing, ensure that you have a **Cognitive Services User** role assignment to access the chat completion model and embedding models (if using).

+ For integrated operations, ensure your [search service identity](search-howto-managed-identities-data-sources.md) has a **Cognitive Services User** role assignment for model access.

---

## Development tasks

Development tasks on the Azure AI Search side include:

+ Create a knowledge agent on Azure AI Search that maps to your deployed model in Azure AI Foundry Model.
+ Call the retriever and provide a query, conversation, and override parameters.
+ Parse the response for the parts you want to include in your chat application. For many scenarios, just the content portion of the response is sufficient. 

## Components of the solution

Your custom application makes API calls to Azure AI Search and an Azure SDK.

+ External data from anywhere, although we recommend [data sources used for integrated indexing](search-data-sources-gallery.md).
+ Azure AI Search, hosting indexed data and the agentic data retrieval engine.
+ Azure AI Foundry, hosting the AI agent and tool.
+ Azure SDK with a Foundry project, providing programmatic access to Azure AI Foundry.
+ Azure OpenAI, hosting a chat completion model used by the knowledge agent and any embedding models used by vectorizers for vector search.

## Set up your environment

The canonical use case for agentic retrieval is through the Azure AI Agent service. We recommend it because it's the easiest way to create a chatbot.

An agent-to-agent solution combines Azure AI Search with Foundry projects that you use to build custom agents. An agent simplifies development by tracking conversation history and calling other tools.

You need endpoints for:

+ Azure AI Search
+ Azure OpenAI
+ Azure AI Foundry project

You can find endpoints for Azure AI Search and Azure OpenAI in the [Azure portal](https://portal.azure.com), in the **Overview** pages for each resource.

You can find the project endpoint in the Azure AI Foundry portal:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com) and open your project. 

1. In the **Overview** tile, find and copy the Azure AI Foundry project endpoint.

   A hypothetical endpoint might look like this: `https://your-foundry-resource.services.ai.azure.com/api/projects/your-foundry-project`

If you don't have an Azure OpenAI resource in your Foundry project, revisit the model deployment prerequisite. A connection to the resource is created when you deploy a model.

### Set up an AI project client and create an agent

Use [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient?view=azure-python-preview&preserve-view=true) to create your AI agent.

```python
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

list(project_client.agents.list_agents())
```

Your agent is backed by a supported language model and instructions inform the agent of its scope.

```python
instructions = """
A Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer using the format [ref_id].
If you do not have the answer, respond with "I don't know".
"""
agent = project_client.agents.create_agent(
    model=agent_model,
    name=agent_name,
    instructions=instructions
)

print(f"AI agent '{agent_name}' created or updated successfully")
```

### Add an agentic retrieval tool to AI Agent

An end-to-end pipeline needs an orchestration mechanism for coordinating calls to the retriever and knowledge agent. You can use a [tool](/azure/ai-services/agents/how-to/tools/function-calling) for this task. The tool calls the Azure AI Search knowledge retrieval client and the Azure AI agent, and it drives the conversations with the user.

```python
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent, KnowledgeAgentIndexParams

agent_client = KnowledgeAgentRetrievalClient(endpoint=endpoint, agent_name=agent_name, credential=credential)

thread = project_client.agents.threads.create()
retrieval_results = {}

# AGENTIC RETRIEVAL DEFINITION DEFERRED TO NEXT SECTION

functions = FunctionTool({ agentic_retrieval })
toolset = ToolSet()
toolset.add(functions)
project_client.agents.enable_auto_function_calls(toolset)
```

## How to structure messages

The messages sent to the agent tool include instructions for chat history and using the results obtained from [knowledge retrieval](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-05-01-preview&preserve-view=true) on Azure AI Search. The response is passed as a large single string with no serialization or structure.

```python
def agentic_retrieval() -> str:
    """
        Searches a NASA e-book about images of Earth at night and other science related facts.
        The returned string is in a JSON format that contains the reference id.
        Be sure to use the same format in your agent's response
    """
    # Take the last 5 messages in the conversation
    messages = project_client.agents.list_messages(thread.id, limit=5, order=ListSortOrder.DESCENDING)
    # Reverse the order so the most recent message is last
    messages.data.reverse()
    retrieval_result = retrieval_result = agent_client.retrieve(
        retrieval_request=KnowledgeAgentRetrievalRequest(
            messages=[KnowledgeAgentMessage(role=msg["role"], content=[KnowledgeAgentMessageTextContent(text=msg.content[0].text)]) for msg in messages.data],
            target_index_params=[KnowledgeAgentIndexParams(index_name=index_name, reranker_threshold=2.5)]
        )
    )

    # Associate the retrieval results with the last message in the conversation
    last_message = messages.data[-1]
    retrieval_results[last_message.id] = retrieval_result

    # Return the grounding response to the agent
    return retrieval_result.response[0].content[0].text
```

## How to improve data quality

Search results are consolidated into a large unified string that you can pass to a chat completion model for a grounded answer. The following indexing and relevance tuning features in Azure AI Search are available to help you generate high quality results. You can implement these features in the search index, and the improvements in search relevance are evident in the quality of the response returned during retrieval.

+ [Scoring profiles](index-add-scoring-profiles.md) (added to your search index) provide built-in boosting criteria. Your index must specify a default scoring profile, and that's the one used by the retrieval engine when queries include fields associated with that profile.

+ [Semantic configuration](semantic-how-to-configure.md) is required, but you determine which fields are prioritized and used for ranking.

+ For plain text content, you can use [analyzers](index-add-custom-analyzers.md) to control tokenization during indexing.

+ For [multimodal or image content](multimodal-search-overview.md), you can use image verbalization for LLM-generated descriptions of your images, or classic OCR and image analysis via skillsets during indexing.

## Control the number of subqueries

The LLM determines the quantity of subqueries based on these factors:

+ User query
+ Chat history
+ Semantic ranker input constraints

As the developer, the best way to control the number of subqueries is by setting the `defaultMaxDocsForReranker` in either the knowledge agent definition or as an override on the retrieve action. 

The semantic ranker processes up to 50 documents as an input, and the system creates subqueries to accommodate all of the inputs to semantic ranker. For example, if you only wanted two subqueries, you could set `defaultMaxDocsForReranker` to 100 to accommodate all documents in two batches.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the `defaultMaxDocsForReranker` threshold.

## Control the number of threads in chat history

A knowledge agent object in Azure AI Search acquires chat history through API calls to the Azure Evaluations SDK, which maintains the thread history. You can filter this list to get a subset of the messages, for example, the last five conversation turns.

## Control costs and limit operations

Look at output tokens in the [activity array](search-agentic-retrieval-how-to-retrieve.md#review-the-activity-array) for insights into the query plan.

## Tips for improving performance

+ Summarize message threads.

+ Use `gpt mini` or a smaller model that performs faster.

+ Set `maxOutputSize` in the [knowledge agent](search-agentic-retrieval-how-to-create.md) to govern the size of the response, or `maxRuntimeInSeconds` for time-bound processing.

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
