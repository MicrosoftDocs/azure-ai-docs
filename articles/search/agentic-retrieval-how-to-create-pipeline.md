---
title: 'Tutorial: Create an Agentic Retrieval Solution'
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents in Azure AI Foundry.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 11/06/2025
ms.service: azure-ai-search
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build an agentic retrieval solution using Azure AI Search and Azure AI Foundry

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this tutorial, you learn how to build a solution that integrates Azure AI Search and Azure AI Foundry Agent service for intelligent knowledge retrieval.

This solution uses the Model Context Protocol (MCP) to establish a standardized connection between your agentic retrieval pipeline in Azure AI Search, which consists of a *knowledge base* that references a *knowledge sources*, and your agent in Azure AI Foundry.

The following diagram shows the high-level architecture of this agentic retrieval solution:

:::image type="content" source="media/agentic-retrieval/agent-to-agent-pipeline.svg" alt-text="Diagram of Azure AI Search integration with Azure AI Foundry Agent service via MCP." lightbox="media/agentic-retrieval/agent-to-agent-pipeline.png" :::

> [!TIP]
> + Want to get started right away? See the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python sample on GitHub.
> + Want a simpler introduction to agentic retrieval? See [Quickstart: Use agentic retrieval](search-get-started-agentic-retrieval.md).

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md).

+ A search index that satisfies the [criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md).

+ An [Azure AI Foundry project](/azure/ai-foundry/how-to/create-projects) and Azure AI Foundry resource. When you create a project, the resource is automatically created.

+ An Azure OpenAI resource with a [supported LLM](agentic-retrieval-how-to-create-knowledge-base#supported-llms) deployment. We recommend a minimum token capacity of 100,000. You can find the capacity and rate limit on the model deployments list in the Azure AI Foundry portal. If you want [vectorization at query time](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries), you can also deploy a text embedding model.

+ Package versions that provide preview functionality. For the complete list of versions used in this solution, see the [`requirements.txt`](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/agentic-retrieval-pipeline-example/requirements.txt) file.

### Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, you can use [key-based authentication](search-security-api-keys.md) instead.

Configure access to each resource identified in this section.

### [**Azure AI Search**](#tab/search-perms)

Azure AI Search provides the agentic retrieval pipeline. Configure access for yourself, your app, and your search service for downstream access to models.

1. [Enable role-based access](search-security-enable-roles.md).
1. [Configure a managed identity](search-how-to-managed-identities.md).
1. [Assign roles](search-security-rbac.md):

   + You must have the **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader** roles to create, load, and retrieve on Azure AI Search.

   + For integrated operations, ensure that all clients using the retrieval pipeline (agent) have the **Search Index Data Reader** role for sending retrieval requests.

### [**Azure OpenAI**](#tab/openai-perms)

Azure OpenAI hosts the models used by the agentic retrieval pipeline. Configure access for yourself and for the search service.

+ You must have the **Cognitive Services User** role to access the LLM and embedding model (if using).

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has the **Cognitive Services User** role for model access.

### [**Azure AI Foundry**](#tab/foundry-perms)

Azure AI Foundry hosts the agent, and MCP tool. Permissions are needed to create and use these resources. For more information, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

+ You must be an **Owner** of your Azure subscription to create the project and resource.

+ On the resource, you must have the **Azure AI User** role to access LLM deployments and create agents. This assignment is conferred automatically for **Owners** when you create the resource. Other users need a specific role assignment.

+ On the resource, you must have the **Azure AI Project Manager** role to create a project connection for MCP authentication and either **Azure AI User** or **Azure AI Project Manager** to use the MCP tool in agents.

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has the **Cognitive Services User** role on the resource.

---

## Development tasks

Development tasks for this solution include:

### [Azure AI Search](#tab/search-development)

+ [Create a knowledge source](agentic-knowledge-source-overview.md) that maps to a [searchable index](agentic-retrieval-how-to-create-index.md).

+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that maps to your LLM deployment and uses the extractive data output mode, which we recommend for interaction with Azure AI Foundry Agent Service.

+ [Call the retrieve action](agentic-retrieval-how-to-retrieve.md) on the knowledge base to process a query, conversation, and override parameters.

+ Parse the response for the parts you want to include in your chat application. For many scenarios, the content portion of the response is sufficient.

### [Azure AI Foundry](#tab/foundry-development)

+ Create a project connection and an agent that uses the MCP tool.

+ Use the MCP tool to coordinate calls from the agent to the knowledge base.

---

A user initiates query processing by interacting with a client app, such as a chatbot, which calls an agent. The agent uses the MCP tool to orchestrate requests and direct responses. When the chatbot calls the agent, the MCP tool calls the knowledge base in Azure AI Search, waits for the response, and sends it back to the agent and chatbot.

Knowledge bases support both extractive data and [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) for response generation. We recommend extractive data for this solution, as it returns verbatim results from your indexed content that the agent can use for grounding and reasoning.

## Components of the solution

Your custom application makes API calls to Azure AI Search and an Azure SDK. The components include:

+ External data from anywhere, but we recommend [data sources used for integrated indexing](search-data-sources-gallery.md).

+ Azure AI Search hosts indexed data and the agentic data retrieval engine with a knowledge base and knowledge source.

+ Azure OpenAI hosts an LLM used by the knowledge base and any embedding models used by vectorizers in the search index.

+ Azure AI Foundry hosts the agent configured with the MCP tool.

+ Azure SDK with an Azure AI Foundry project connection, which provides secure access to Azure AI Search through MCP.

## Set up your environment

This agentic retrieval solution combines Azure AI Search with a custom agent you built in Azure AI Foundry. An agent simplifies development by tracking conversation history, determining when to call external tools, and managing the orchestration of tool calls.

For this solution, you need the following:

### [Azure AI Search](#tab/search-setup)

+ The endpoint for your search service, which you can find on the **Overview** page in the Azure portal.

+ An API key for your search service, which you can find on the **Keys and Endpoint** page in the Azure portal.

### [Azure OpenAI](#tab/aoai-setup)

+ The endpoint for your Azure OpenAI resource, which you can find on the **Overview** page in the Azure portal.

### [Azure AI Foundry](#tab/foundry-setup)

+ The endpoint for your project, which you can find on the **Endpoints** page in the Azure portal. It should look like this: `https://{your-resource-name}.services.ai.azure.com/api/projects/{your-project-name}`

+ The resource ID of your project, which you can find on the **Properties** page in the Azure portal. It should look like this: `/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}`

---

### Create a project connection

Before you can use the MCP tool in an agent, you must create a project connection in Azure AI Foundry. This connection securely stores the API credentials needed for the MCP tool to authenticate and communicate with your Azure AI Search knowledge base.

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import ConnectionPropertiesV2BasicResource, CustomKeysConnectionProperties, CustomKeys

mgmt_client = CognitiveServicesManagementClient(credential, subscription_id)
resource = mgmt_client.project_connections.create(
    resource_group_name=resource_group,
    account_name=account_name,
    project_name=project_name,
    connection_name=project_connection_name,
    connection=ConnectionPropertiesV2BasicResource(
        properties=CustomKeysConnectionProperties(
            category="RemoteTool",
            target=mcp_endpoint,
            is_shared_to_all=True,
            metadata={ "ApiType": "Azure" },
            credentials=CustomKeys(
                keys={ "api-key": search_api_key }
            )
        )
    )
)

print(f"Connection '{resource.name}' created or updated successfully.")
```

### Set up the AI project client

Use [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient?view=azure-python-preview&preserve-view=true) to access your Azure AI Foundry project.

```python
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

list(project_client.agents.list())
```

### Create an agent that uses the MCP tool

In Azure AI Foundry, an agent is a smart micro-service that can do RAG. The purpose of this specific agent is to decide when to send a query to the knowledge base using the MCP tool.

```python
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

instructions = """
A Q&A agent that can answer questions about the Earth at night.
Always provide references to the ID of the data source used to answer the question.
If you do not have the answer, respond with "I don't know".
"""
mcp_kb_tool = MCPTool(
    server_label="knowledge-base",
    server_url=mcp_endpoint,
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],
    project_connection_id=project_connection_name
)
agent = project_client.agents.create_version(
    agent_name=agent_name,
    definition=PromptAgentDefinition(
        model=agent_model,
        instructions=instructions,
        tools=[mcp_kb_tool]
    )
)


print(f"AI agent '{agent_name}' created or updated successfully")
```

### Chat with the agent

Messages sent to the agent use the OpenAI conversations and responses APIs. The agent with the MCP tool routes requests to the Azure AI Search knowledge base, which retrieves content and returns results that drive the conversation.

```python
# Get the OpenAI client for responses and conversations
openai_client = project_client.get_openai_client()

conversation = openai_client.conversations.create()

# Send initial request that will trigger the MCP tool
response = openai_client.responses.create(
    conversation=conversation.id,
    input="""
        Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
        Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """,
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response: {response.output_text}")
```

The MCP tool handles the orchestration automatically. When the agent determines that it needs to retrieve knowledge, it calls the knowledge base through the MCP connection, and the results are returned as context for the agent's response.

## How to improve data quality

By default, search results from the knowledge base are consolidated into a large unified string that you can pass to an LLM for grounding. The following indexing and relevance tuning features in Azure AI Search are available to help you generate high-quality results. You can implement these features in the search index, and the improvements in search relevance are evident in the quality of the response returned during retrieval.

+ [Scoring profiles](index-add-scoring-profiles.md) (added to your search index) provide built-in boosting criteria. Your index must specify a default scoring profile, and that's the one used by the retrieval engine when queries include fields associated with that profile.

+ [Semantic configuration](semantic-how-to-configure.md) is required, but you determine which fields are prioritized and used for ranking.

+ For plain text content, you can use [analyzers](index-add-custom-analyzers.md) to control tokenization during indexing.

+ For [multimodal or image content](multimodal-search-overview.md), you can use image verbalization for LLM-generated descriptions of your images, or classic OCR and image analysis via skillsets during indexing.

## Control the number of subqueries

The LLM determines the quantity of subqueries based on these factors:

+ User query
+ Chat history
+ Semantic ranker input constraints

As the developer, you can control the number of subqueries by [setting the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). The retrieval reasoning effort determines the level of LLM processing for query planning, ranging from minimal (no LLM processing) to medium (deeper search and follow-up iterations).

<!-- As the developer, the best way to control the number of subqueries is by setting the `defaultMaxDocsForReranker` in either the knowledge agent definition or as an override on the retrieve action. 

The semantic ranker processes up to 50 documents as an input, and the system creates subqueries to accommodate all of the inputs to semantic ranker. For example, if you only wanted two subqueries, you could set `defaultMaxDocsForReranker` to 100 to accommodate all documents in two batches.

The [semantic configuration](semantic-how-to-configure.md) in the index determines whether the input is 50 or not. If the value is less, the query plan specifies however many subqueries are necessary to meet the `defaultMaxDocsForReranker` threshold. -->

## Control the number of threads in chat history

A knowledge base object in Azure AI Search acquires chat history through API calls to the Azure Evaluations SDK, which maintains the thread history. You can filter this list to get a subset of the messages, such as the last five conversation turns.

## Control costs and limit operations

Look at output tokens in the [activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array) for insights into the query plan.

## Tips for improving performance

+ Summarize message threads.

+ Use `gpt-mini` or a smaller model that performs faster.

+ Set `maxOutputSize` on the [retrieve action](agentic-retrieval-how-to-retrieve.md) to govern the size of the response or `maxRuntimeInSeconds` for time-bound processing.

## Clean up resources

When you're working in your own subscription, at the end of a project, it's a good idea to remove the resources that you no longer need. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can also delete individual objects:

```python
# Delete the agent
project_client.agents.delete_version(agent.name, agent.version)
print(f"AI agent '{agent.name}' version '{agent.version}' deleted successfully")

# Delete the knowledge base
index_client.delete_knowledge_base(base_name)
print(f"Knowledge base '{base_name}' deleted successfully")

# Delete the knowledge source
index_client.delete_knowledge_source(knowledge_source=knowledge_source_name) # This is new feature in 2025-08-01-Preview api version
print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")

# Delete the search index
index_client.delete_index(index)
print(f"Index '{index_name}' deleted successfully")
```

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
