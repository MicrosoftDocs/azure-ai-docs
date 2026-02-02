---
title: 'Tutorial: Build an agentic retrieval solution'
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents in AI Foundry.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 09/10/2025
ms.service: azure-ai-search
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build an agent-to-agent retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article describes an approach or pattern for building a solution that uses Azure AI Search for knowledge retrieval, and how to integrate knowledge retrieval into a custom solution that includes Azure AI Agent. This pattern uses an agent tool to invoke an agentic retrieval pipeline in Azure AI Search.

:::image type="content" source="media/agentic-retrieval/agent-to-agent-pipeline.svg" alt-text="Diagram of Azure AI Search integration with Azure AI Agent service." lightbox="media/agentic-retrieval/agent-to-agent-pipeline.png" :::

This exercise differs from the [Agentic Retrieval Quickstart](search-get-started-agentic-retrieval.md) in how it uses Azure AI Agent to retrieve data from the index, and how it uses an agent tool for orchestration. If you want to understand the retrieval pipeline in its simplest form, begin with the quickstart.

> [!TIP]
> To run the code for this tutorial, download the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python sample on GitHub.

## Prerequisites

The following resources are required for this design pattern:

+ Azure AI Search, Basic pricing tier or higher, in a [region that provides semantic ranking](search-region-support.md).

+ A search index that satisfies the [index criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md).

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
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

### Package version requirements

Use a package version that provides preview functionality. See the [`requirements.txt`](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/agentic-retrieval-pipeline-example/requirements.txt) file for more packages used in the example solution.

```
azure-ai-projects==1.1.0b3
azure-ai-agents==1.2.0b3
azure-search-documents==11.7.0b1
```

### Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, you can use [key-based authentication](search-security-api-keys.md) instead.

Configure access to each resource identified in this section.

### [**Azure AI Search**](#tab/search-perms)

Azure AI Search provides the agentic retrieval pipeline. Configure access for yourself, your app, and your search service for downstream access to models.

1. [Enable role-based access](search-security-enable-roles.md).
1. [Configure a managed identity](search-how-to-managed-identities.md).
1. [Assign roles](search-security-rbac.md):

   + For local testing, you must have **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader** role assignments to create, load, and retrieve on Azure AI Search.

   + For integrated operations, ensure that all clients using the retrieval pipeline (agent and tool) have **Search Index Data Reader** role assignments for sending retrieval requests.

### [**Azure AI Foundry**](#tab/foundry-perms)

Azure AI Foundry hosts the AI agent and tool. Permissions are needed to create and use the resource.

+ You must be an **Owner** of your Azure subscription to create the project and resource.

+ For local testing, you must be an **Azure AI User** to access chat completion models deployed to the Foundry resource. This assignment is conferred automatically for **Owners** when you create the resource. Other users need a specific role assignment. For more information, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has an **Azure AI User** role assignment on the Foundry resource.

### [**Azure OpenAI**](#tab/openai-perms)

Azure OpenAI hosts the models used by the agentic retrieval pipeline. Configure access for yourself and for the search service.

+ For local testing, ensure that you have a **Cognitive Services User** role assignment to access the chat completion model and embedding models (if using).

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has a **Cognitive Services User** role assignment for model access.

---

## Development tasks

Development tasks on the Azure AI Search side include:

+ [Create a knowledge source](agentic-knowledge-source-overview.md) that maps to a [searchable index](agentic-retrieval-how-to-create-index.md).
+ [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md) on Azure AI Search that maps to your deployed model in Azure AI Foundry Model.
+ [Call the retriever](agentic-retrieval-how-to-retrieve.md) and provide a query, conversation, and override parameters.
+ Parse the response for the parts you want to include in your chat application. For many scenarios, just the content portion of the response is sufficient. You can also try [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) for a simpler workflow.

Developments on the Azure AI Agent side include:

+ Set up the AI project client and an AI agent.
+ Add a tool to coordinate calls from the AI agent to the retriever and knowledge agent.

Query processing is initiated by user interaction in a client app, such as a chat bot, that calls an AI agent. The AI agent is configured to use a tool that orchestrates the requests and directs the responses. When the chat bot calls the agent, the tool calls the [retriever](agentic-retrieval-how-to-retrieve.md) on Azure AI Search, waits for the response, and then sends the response back to the AI agent and chat bot. In Azure AI Search, you can use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) to obtain an LLM-generated response from within the query pipeline, or you can call an LLM in your code if you want more control over answer generation.

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

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and open your project. 

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

An end-to-end pipeline needs an orchestration mechanism for coordinating calls to the retriever and knowledge agent on Azure AI Search. You can use a [tool](/azure/ai-services/agents/how-to/tools/function-calling) for this task. The tool is configured in the AI agent and it calls the Azure AI Search knowledge retrieval client and sends back responses that drive the conversation with the user.

```python
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent

agent_client = KnowledgeAgentRetrievalClient(endpoint=endpoint, agent_name=agent_name, credential=credential)

thread = project_client.agents.threads.create()
retrieval_results = {}

# AGENTIC RETRIEVAL DEFINITION "LIFTED AND SHIFTED" TO NEXT SECTION

functions = FunctionTool({ agentic_retrieval })
toolset = ToolSet()
toolset.add(functions)
project_client.agents.enable_auto_function_calls(toolset)
```

## How to structure messages

The messages sent to the agent tool include instructions for chat history and using the results obtained from [knowledge retrieval](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) on Azure AI Search. The response is passed as a large single string with no serialization or structure.

This code snippet is the agentic retrieval definition mentioned in the previous code snippet.

```python
def agentic_retrieval() -> str:
    """
        Searches a NASA e-book about images of Earth at night and other science related facts.
        The returned string is in a JSON format that contains the reference id.
        Be sure to use the same format in your agent's response
        You must refer to references by id number
    """
    # Take the last 5 messages in the conversation
    messages = project_client.agents.messages.list(thread.id, limit=5, order=ListSortOrder.DESCENDING)
    # Reverse the order so the most recent message is last
    messages = list(messages)
    messages.reverse()
    retrieval_result = agent_client.retrieve(
        retrieval_request=KnowledgeAgentRetrievalRequest(
            messages=[
                    KnowledgeAgentMessage(
                        role=m["role"],
                        content=[KnowledgeAgentMessageTextContent(text=m["content"])]
                    ) for m in messages if m["role"] != "system"
            ]
        )
    )

    # Associate the retrieval results with the last message in the conversation
    last_message = messages[-1]
    retrieval_results[last_message.id] = retrieval_result

    # Return the grounding response to the agent
    return retrieval_result.response[0].content[0].text
```

## How to start the conversation

To start the chat, use the standard Azure AI agent tool calling APIs. Send the message with questions, and the agent decides when to retrieve knowledge from your search index using agentic retrieval.

```python
from azure.ai.agents.models import AgentsNamedToolChoice, AgentsNamedToolChoiceType, FunctionName

message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="""
        Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
        Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """
)

run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
    tool_choice=AgentsNamedToolChoice(type=AgentsNamedToolChoiceType.FUNCTION, function=FunctionName(name="agentic_retrieval")),
    toolset=toolset)
if run.status == "failed":
    raise RuntimeError(f"Run failed: {run.last_error}")
output = project_client.agents.messages.get_last_message_text_by_role(thread_id=thread.id, role="assistant").text.value

print("Agent response:", output.replace(".", "\n"))
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

As the developer, the best way to control the number of subqueries is by setting the [maxSubQueries](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview#knowledgesourcereference&preserve-view=true) property in a knowledge agent. 

The semantic ranker processes up to 50 documents as an input, and the system creates subqueries to accommodate all of the inputs to semantic ranker. For example, if you only wanted two subqueries, you could set `maxSubQueries` to 100 to accommodate all documents in two batches.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the smaller input size. 

<!-- As the developer, the best way to control the number of subqueries is by setting the `defaultMaxDocsForReranker` in either the knowledge agent definition or as an override on the retrieve action. 

The semantic ranker processes up to 50 documents as an input, and the system creates subqueries to accommodate all of the inputs to semantic ranker. For example, if you only wanted two subqueries, you could set `defaultMaxDocsForReranker` to 100 to accommodate all documents in two batches.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the `defaultMaxDocsForReranker` threshold. -->

## Control the number of threads in chat history

A knowledge agent object in Azure AI Search acquires chat history through API calls to the Azure Evaluations SDK, which maintains the thread history. You can filter this list to get a subset of the messages, for example, the last five conversation turns.

## Control costs and limit operations

Look at output tokens in the [activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array) for insights into the query plan.

## Tips for improving performance

+ Summarize message threads.

+ Use `gpt mini` or a smaller model that performs faster.

+ Set `maxOutputSize` in the [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md) to govern the size of the response, or `maxRuntimeInSeconds` for time-bound processing.

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can also delete individual objects:

+ [Delete a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md#delete-an-agent)

+ [Delete a knowledge source](agentic-knowledge-source-how-to-search-index.md#delete-a-knowledge-source)

+ [Delete an index](search-how-to-manage-index.md#delete-an-index)

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
