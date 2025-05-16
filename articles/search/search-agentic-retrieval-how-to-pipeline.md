---
title: Build an agentic retrieval solution
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/10/2025
---

# Build an agent-to-agent retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article describes an approach or pattern for building a solution that uses Azure AI Search for data retrieval and how to integrate the retrieval into a custom solution that includes Azure AI Agent.

This article supports the [agent-example](https://github.com/Azure-Samples/agentic-retrieval-pipeline-example) Python sample on GitHub.

This exercise differs from the [Agentic Retrieval Quickstart](search-get-started-agentic-retrieval.md) in how it uses Azure AI Agent to determine whether to retrieve data from the index, and how it uses an agent tool for orchestration.

## Prerequisites

The following resources are required for this design pattern:

+ Azure AI Search, basic tier or higher, in a [region that provides semantic ranker](search-region-support.md).

+ A search index that satisfies the [index criteria for agentic retrieval](search-agentic-retrieval-how-to-index.md).

+ Azure OpenAI, and you should have an **Azure AI Developer** role assignment to create a Foundry project.

+ A project in Azure AI Foundry, with a deployment of a supported large language model and an Azure AI Agent in a basic setup. To meet this requirement, follow the steps in [Quickstart: Create a new agent (Preview)](/azure/ai-services/agents/quickstart?pivots=ai-foundry-portal). We recommend 100,000 token capacity for your model. You can find capacity and the rate limit in the model deployments list in the Azure AI Foundry portal.

### Supported large language models

Use Azure OpenAI or an equivalent open source model:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`

## Development tasks

Development tasks on the Azure AI Search side include:

+ Create a search agent on Azure AI Search that maps to your deployed model in Azure AI Foundry Model.
+ Call the retriever and provide a query, conversation, and override parameters.
+ Parse the response for the parts you want to include in your chat application. For many scenarios, just the content portion of the response is sufficient. 

## Components of the solution

Your custom application makes API calls to Azure AI Search and an Azure SDK.

+ External data from anywhere
+ Azure AI Search, hosting indexed data and the agentic data retrieval engine
+ Azure AI Foundry Model, providing a chat model (an LLM) for user interaction
+ Azure SDK with a Foundry project, providing programmatic access to chat and chat history
+ Azure AI Agent, with an agent for handling the conversation, and a tool for orchestration

## How to customize grounding data

Search results are consolidating into a large unified string that you can pass to a conversational language model for a grounded answer. The following indexing and relevance tuning features in Azure AI Search are available to help you generate high quality results:

+ Scoring profiles (added to your search index) provide built-in boosting criteria. Your index must specify a default scoring profile, and that's the one used by the retrieval engine when queries include fields associated with that profile.

+ Semantic configuration is required, but you determine which fields are prioritized and used for ranking.

+ For plain text content, you can use analyzers to control tokenization during indexing.

+ For multimodal or image content, you can use image verbalization for LLM-generated descriptions of your images, or classic OCR and image analysis via skillsets during indexing.

## Create the project

The canonical use case for agentic retrieval is through the Azure AI Agent service. We recommend it because it's the easiest way to create a chatbot.

An agent-to-agent solution combines Azure AI Search with Foundry projects that you use to build custom agents. An agent simplifies development by tracking conversation history and calling other tools.

You need endpoints for:

+ Azure AI Search
+ Azure OpenAI
+ Azure AI Foundry project

You can find endpoints for Azure AI Search and Azure OpenAI in the [Azure portal](https://portal.azure.com).

You can find the project connection string in the Azure AI Foundry portal:

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com) and open your project. 

1. In the **Project details** tile, find and copy the **Project connection string**. 

   A hypothetical connection string might look like this: `eastus2.api.azureml.ms;00000000-0000-0000-0000-0000000000;rg-my-resource-group-name;my-foundry-project-name`

1. Check the authentication type for your Azure OpenAI resource and make sure it uses an API key shared to all projects. Still in **Project details**, expand the **Connected resources** tile to view the authentication type for your Azure OpenAI resource.

If you don't have an Azure OpenAI resource in your Foundry project, revisit the model deployment prerequisite. A connection to the resource is created when you deploy a model.

### Add an agentic retrieval tool to AI Agent

An end-to-end pipeline needs an orchestration mechanism for coordinating calls to the retriever and agent. You can use a [tool](/azure/ai-services/agents/how-to/tools/function-calling) for this task. The tool calls the Azure AI Search knowledge retrieval client and the Azure AI agent, and it drives the conversations with the user.

## How to design a prompt

The prompt sent to the LLM includes instructions for working with the grounding data, which is passed as a large single string with no serialization or structure.

The tool or function that you use to drive the pipeline provides the instructions to the LLM for the conversation.

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
    retrieval_result = agent_client.knowledge_retrieval.retrieve(
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

To provide instructions used for building the query plan and the subqueries used to get the grounding data, set the message in the search agent:

```python
project_client = AIProjectClient.from_connection_string(project_conn_str, credential=credential)

instructions = """
An Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer.
If you do not have the answer, respond with "I don't know".
"""
agent = project_client.agents.create_agent(
    model=agent_model,
    name=agent_name,
    instructions=instructions
)
```

## Control the number of subqueries

The LLM determines the quantity of subqueries based on these factors:

+ User query
+ Chat history
+ Semantic ranker input constraints

As the developer, the best way to control the number of subqueries is by setting the `defaultMaxDocsForReranker` in either the agent definition or as an override on the retrieve action. 

The semantic ranker processes up to 50 documents as an input, and the system creates subqueries to accommodate all of the inputs to semantic ranker. For example, if you only wanted two subqueries, you could set `defaultMaxDocsForReranker` to 100 to accommodate all documents in two batches.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the `defaultMaxDocsForReranker` threshold.

## Control the number of threads in chat history

An agent object in Azure AI Search acquires chat history through API calls to the Azure Evaluations SDK, which maintains the thread history. You can filter this list to get a subset of the messages, for example, the last five conversation turns.

## Control costs and limit operations

Look at output tokens in the [activity array](search-agentic-retrieval-how-to-retrieve.md#review-the-activity-array) for insights into the query plan.

## Tips for improving performance

+ Summarize message threads.

+ Use `gpt mini`.

+ Set `maxOutputSize` in the [search agent](search-agentic-retrieval-how-to-create.md) to govern the size of the response, or `maxRuntimeInSeconds` for time-bound processing.

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
