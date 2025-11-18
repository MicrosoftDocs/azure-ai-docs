---
title: 'Tutorial: Create an End-to-End Retrieval Solution'
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents in Microsoft Foundry.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 11/07/2025
ms.service: azure-ai-search
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build an end-to-end agentic retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In this tutorial, you learn how to build a solution that integrates Azure AI Search and Foundry Agent Service for intelligent knowledge retrieval.

This solution uses the Model Context Protocol (MCP) to establish a standardized connection between your agentic retrieval pipeline in Azure AI Search, which consists of a *knowledge base* that references a *knowledge source*, and your agent in Foundry Agent Service.

The following diagram shows the high-level architecture of this agentic retrieval solution:

:::image type="content" source="media/agentic-retrieval/end-to-end-pipeline.svg" alt-text="Diagram of Azure AI Search integration with Foundry Agent Service via MCP." lightbox="media/agentic-retrieval/end-to-end-pipeline.svg" :::

> [!TIP]
> + To run the code for this tutorial, download the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python sample on GitHub.
> + Want a simpler introduction to agentic retrieval? See [Quickstart: Use agentic retrieval](search-get-started-agentic-retrieval.md).

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md).

+ A search index that satisfies the [criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ An Azure OpenAI resource with a [supported LLM](agentic-retrieval-how-to-create-knowledge-base.md#supported-models) deployment. We recommend a minimum token capacity of 100,000. You can find the LLM's capacity and rate limit in the Foundry portal. If you want [vectorization at query time](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries), you should also deploy a text embedding model.

+ [Authorization and permissions](#configure-access) to access each resource.

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

   + For integrated operations, ensure that all clients using the retrieval pipeline have the **Search Index Data Reader** role for sending retrieval requests.

### [**Azure OpenAI**](#tab/openai-perms)

Azure OpenAI hosts the models used by the agentic retrieval pipeline. Configure access for yourself and the search service.

+ You must have the **Cognitive Services User** role to access the LLM and embedding model (if using).

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has the **Cognitive Services User** role for model access.

### [**Microsoft Foundry**](#tab/foundry-perms)

Foundry hosts the agent and MCP tool. Permissions are needed to create and use these resources. For more information, see [Role-based access control in Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

+ You must be an **Owner** of your Azure subscription to create the project and resource.

+ On the resource, you must have the **Azure AI User** role to access model deployments and create agents. This assignment is conferred automatically for **Owners** when you create the resource. Other users need a specific role assignment.

+ On the resource, you must have the **Azure AI Project Manager** role to create a project connection for MCP authentication and either **Azure AI User** or **Azure AI Project Manager** to use the MCP tool in agents.

+ For integrated operations, ensure your [search service identity](search-how-to-managed-identities.md) has the **Cognitive Services User** role on the resource.

---

## Components of the solution

This solution consists of the following integrated components:

+ External data from anywhere, but we recommend [data sources used for integrated indexing](search-data-sources-gallery.md).

+ Azure AI Search hosts your indexed content and provides the agentic retrieval engine (knowledge base that references a knowledge source).

+ Azure OpenAI hosts an LLM used by the knowledge base and any embedding models used by vectorizers in the search index.

+ Foundry hosts the agent configured with the MCP tool, as well as the project connection that stores the MCP endpoint and API credentials for agent-to-knowledge-base communication.

A user initiates query processing by interacting with a client app, such as a chatbot, that calls an agent. The agent uses the MCP tool to orchestrate requests to the knowledge base and synthesize responses. When the chatbot calls the agent, the MCP tool calls the knowledge base in Azure AI Search and sends it back to the agent and chatbot.

## Development tasks

Development tasks for this solution include:

### [Azure AI Search](#tab/search-development)

+ Create a [knowledge source](agentic-knowledge-source-overview.md). Agentic retrieval supports multiple types of knowledge sources, but this solution creates a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md).

+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that maps to your LLM deployment and uses the extractive data output mode. We recommend this output mode for interaction with Foundry Agent Service because it provides the agent with verbatim, unprocessed content for grounding and reasoning. The agent is responsible for synthesizing answers and performing other tasks with this verbatim content.

+ [Call the retrieve action](agentic-retrieval-how-to-retrieve.md) on the knowledge base to process a query, conversation, and override parameters.

+ Parse the response for the parts you want to include in your chat application. For many scenarios, the [content portion](agentic-retrieval-how-to-retrieve.md#review-the-extracted-response) of the response is sufficient.

### [Microsoft Foundry](#tab/foundry-development)

+ Create a project connection and an agent that uses the MCP tool.

+ Use the MCP tool to coordinate calls from the agent to the knowledge base.

---

## Set up your environment

This solution combines an agentic retrieval engine built in Azure AI Search with a custom agent built in Foundry. An agent simplifies development by tracking conversation history and managing the orchestration of tool calls.

For this solution, you need the following information from each resource:

### [Azure AI Search](#tab/search-setup)

+ The endpoint for your search service, which you can find on the **Overview** page in the Azure portal. It should look like this: `https://{your-service-name}.search.windows.net/`

+ An API key for your search service, which you can find on the **Keys and Endpoint** page in the Azure portal. This key is used for MCP authentication between your knowledge base and the agent in Foundry.

### [Azure OpenAI](#tab/aoai-setup)

+ The endpoint for your Azure OpenAI resource, which you can find on the **Keys and Endpoint** page in the Azure portal. It should look like this: `https://{your-resource-name}.openai.azure.com/`

### [Microsoft Foundry](#tab/foundry-setup)

+ The endpoint for your project, which you can find on the **Endpoints** page in the Azure portal. It should look like this: `https://{your-resource-name}.services.ai.azure.com/api/projects/{your-project-name}`

+ The resource ID of your project, which you can find on the **Properties** page in the Azure portal. It should look like this: `/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}`

---

### Create a project connection

Before you can use the MCP tool in an agent, you must create a project connection in Foundry that points to the `mcp_endpoint` of your knowledge base. This endpoint allows the agent to access your knowledge base.

```python
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import ConnectionPropertiesV2BasicResource, CustomKeysConnectionProperties, CustomKeys

project_resource_id = "{project_resource_id}" # e.g. /subscriptions/{subscription}/resourceGroups/{resource_group}/providers/Microsoft.MachineLearningServices/workspaces/{account_name}/projects/{project_name}
parsed = parse_resource_id(project_resource_id)
subscription_id = parsed['subscription']
resource_group = parsed['resource_group']
account_name = parsed['name']
project_name = parsed['child_name_1']
mcp_endpoint = f"{search_service_endpoint}/knowledgebases/{knowledge_base_name}/mcp?api-version=2025-11-01-preview"

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

### Set up an AI project client

Use [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient?view=azure-python-preview&preserve-view=true) to create a client connection to your Foundry project.

```python
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

list(project_client.agents.list())
```

### Create an agent that uses the MCP tool

The next step is to create an agent configured with the MCP tool. When the agent receives a user query, it can call your knowledge base through the MCP tool to retrieve relevant content for response grounding.

The agent definition includes instructions that specify its behavior and the project connection you previously created. For more information, see [Quickstart: Create a new agent](/azure/ai-foundry/agents/quickstart).

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

## Chat with the agent

Your client app uses the Conversations and [Responses](/azure/ai-foundry/openai/how-to/responses) APIs from Azure OpenAI to send user input to the agent. The client creates a conversation and passes each user message to the agent through the Responses API, resembling a typical chat experience.

The agent manages the conversation, determines when to call your knowledge base through the MCP tool, and returns a natural-language response (with references to the retrieved content) to the client app.

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

## Improve data quality

By default, search results from your knowledge base are consolidated into a large unified string that you can pass to the agent for grounding. Azure AI Search provides the following indexing and relevance-tuning features to help you generate high-quality results. You can implement these features in the search index, and the improvements in search relevance are evident in the quality of the response returned during retrieval.

+ [Scoring profiles](index-add-scoring-profiles.md) provide built-in boosting criteria. Your index must specify a default scoring profile, which is used by the retrieval engine when queries include fields associated with that profile.

+ [Semantic configuration](semantic-how-to-configure.md) is required, but you determine which fields are prioritized and used for ranking.

+ For plain-text content, you can use [analyzers](index-add-custom-analyzers.md) to control tokenization during indexing.

+ For [multimodal or image content](multimodal-search-overview.md), you can use image verbalization for LLM-generated descriptions of your images or classic OCR and image analysis via skillsets during indexing.

## Control the number of subqueries

The LLM that powers your knowledge base determines the number of subqueries based on the following factors:

+ User query
+ Chat history
+ Semantic ranker input constraints

As the developer, you can control the number of subqueries by [setting the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). The reasoning effort determines the level of LLM processing for query planning, ranging from minimal (no LLM processing) to medium (deeper search and follow-up iterations).

## Control the context sent to the agent

The Responses API controls what is sent to the agent and knowledge base. To optimize performance and relevance, adjust your agent instructions to summarize or filter the chat history before sending it to the MCP tool.

## Control costs and limit operations

For insights into the query plan, look at output tokens in the [activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array) of knowledge base responses.

## Tips for improving performance

+ Summarize message threads.

+ Use `gpt-4.1-mini` or a smaller model that performs faster.

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
