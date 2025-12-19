---
title: 'Tutorial: Create an End-to-End Retrieval Solution'
titleSuffix: Azure AI Search
description: Learn how to design and build a custom agentic retrieval solution where Azure AI Search handles data retrieval for your custom agents in Microsoft Foundry.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-search
ms.topic: tutorial
ms.custom:
  - build-2025
---

# Tutorial: Build an end-to-end agentic retrieval solution using Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This tutorial shows you how to build an intelligent, MCP-enabled solution that integrates Azure AI Search with Foundry Agent Service for knowledge retrieval. You can use this architecture for conversational applications that require complex reasoning over large knowledge domains, such as customer support or technical troubleshooting.

In this tutorial, you:

> [!div class="checklist"]
>
> * Configure role-based access for Azure AI Search and Microsoft Foundry
> * Create a search index, knowledge source, and knowledge base in Azure AI Search
> * Create a project connection to enable MCP communication between Azure AI Search and Microsoft Foundry
> * Create an agent in Microsoft Foundry that uses the MCP tool for retrieval
> * Test the solution by chatting with the agent

The following diagram shows the high-level architecture of this agentic retrieval solution:

:::image type="content" source="media/agentic-retrieval/end-to-end-pipeline.svg" alt-text="Diagram of Azure AI Search integration with Foundry Agent Service via MCP." lightbox="media/agentic-retrieval/end-to-end-pipeline.svg" :::

> [!TIP]
> Want to get started right away? See the [agentic-retrieval-pipeline-example](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/agentic-retrieval-pipeline-example) Python notebook on GitHub. You can clone the notebook to follow along with this tutorial.

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A [Microsoft Foundry project](/azure/ai-foundry/how-to/create-projects) and resource. When you create a project, the resource is automatically created.

+ A [supported LLM](agentic-retrieval-how-to-create-knowledge-base.md#supported-models) deployed to your project. We recommend a minimum token capacity of 100,000. You can find the LLM's capacity and rate limit in the Microsoft Foundry portal. If you want [vectorization at query time](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries), you should also deploy a text embedding model.

+ Preview package versions. For a complete list of versions used in this solution, see the [`requirements.txt`](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/agentic-retrieval-pipeline-example/requirements.txt) file.

## Configure access

Before you begin, make sure you have permissions to access content and operations. We recommend Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, you can use [key-based authentication](search-security-api-keys.md) instead.

To configure access for this solution:

1. Enable a system-assigned managed identity for both your search service and your project (not your project's parent resource). You can do so on the **Identity** page of each resource in the Azure portal.

1. On your search service:

    1. [Enable role-based access](search-security-enable-roles.md).

    1. Assign the **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader** roles to your user account. These roles allow you to create, load, and retrieve on Azure AI Search.

    1. Assign the **Search Index Data Reader** role to your project's managed identity. This role allows the agent to read indexed content during retrieval.

1. On your project's parent resource:

    1. Assign the **Azure AI User** role to your user account. This role allows you to access model deployments and create agents.

    1. Assign the **Azure AI Project Manager** role to your user account. This role allows you to create a project connection for MCP authentication and use the MCP tool in agents.

    1. Assign the **Cognitive Services User** role to your search service's managed identity. This role allows the agent to access the knowledge base in Azure AI Search.

## Understand the solution

This solution combines Azure AI Search and Microsoft Foundry to create an agentic retrieval pipeline:

+ **Azure AI Search** hosts your knowledge base, which uses your LLM deployment to coordinate agentic retrieval from a search index knowledge source. This solution uses the extractive data output mode, which is recommended for integration with Foundry Agent Service because it provides the agent with verbatim, unprocessed content for grounding and reasoning.

+ **Microsoft Foundry** hosts your Azure OpenAI model deployments, project connection, and agent. You create a project connection that points to the MCP endpoint of your knowledge base, and then you create an agent that uses the MCP tool to coordinate retrieval.

A user initiates query processing by interacting with a client app, such as a chatbot, that calls the agent. The agent uses the MCP tool to orchestrate requests to the knowledge base and synthesize responses. When the chatbot calls the agent, the MCP tool calls the knowledge base in Azure AI Search and sends it back to the agent and chatbot.

## Build the solution

To build an end-to-end agentic retrieval solution, follow these steps:

1. [Get service information](#get-service-information)
1. [Set up connections](#set-up-connections)
1. [Load connections](#load-connections)
1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Create a knowledge source](#create-a-knowledge-source)
1. [Create a knowledge base](#create-a-knowledge-base)
1. [Create a project connection](#create-a-project-connection)
1. [Set up an AI project client](#set-up-an-ai-project-client)
1. [Create an agent with the MCP tool](#create-an-agent-with-the-mcp-tool)
1. [Connect to a remote SharePoint knowledge source](#connect-to-a-remote-sharepoint-knowledge-source)
1. [Chat with the agent](#chat-with-the-agent)
1. [Clean up resources](#clean-up-resources)

### Get service information

Start by gathering the following information about your Azure AI Search service and Microsoft Foundry project:

+ The endpoint of your search service, which you can find on the **Overview** page. It should look like this: `https://{your-service-name}.search.windows.net/`

+ The Azure OpenAI endpoint of your project's parent resource, which you can find on the **Endpoints** page. It should look like this: `https://{your-resource-name}.openai.azure.com/`

+ The endpoint of your project, which you can find on the **Endpoints** page. It should look like this: `https://{your-resource-name}.services.ai.azure.com/api/projects/{your-project-name}`

+ The resource ID of your project, which you can find on the **Properties** page. It should look like this: `/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}`

### Set up connections

Create a `.env` file to store your service information as environment variables. This file allows your code to access the necessary endpoints and resource IDs.

```
AZURE_SEARCH_ENDPOINT = https://{your-service-name}.search.windows.net/
AZURE_OPENAI_ENDPOINT = https://{your-resource-name}.openai.azure.com/
PROJECT_ENDPOINT = https://{your-resource-name}.services.ai.azure.com/api/projects/{your-project-name}
PROJECT_RESOURCE_ID = /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/Microsoft.CognitiveServices/accounts/{account-name}/projects/{project-name}
```

### Load connections

Use the following code to load the environment variables from your `.env` file. This code uses the `python-dotenv` package to read the file and set the variables in your environment.

Adjust the other configuration values as needed. Ensure the model names match your deployed models in Microsoft Foundry.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.core.tools import parse_resource_id
from dotenv import load_dotenv
import os

load_dotenv(override=True) # Take environment variables from .env

project_endpoint = os.environ["PROJECT_ENDPOINT"]
project_resource_id = os.environ["PROJECT_RESOURCE_ID"]
project_connection_name = os.getenv("PROJECT_CONNECTION_NAME", "earthknowledgeconnection")
agent_model = os.getenv("AGENT_MODEL", "gpt-4.1-mini")
agent_name = os.getenv("AGENT_NAME", "earth-knowledge-agent")
endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
credential = DefaultAzureCredential()
knowledge_source_name = os.getenv("AZURE_SEARCH_KNOWLEDGE_SOURCE_NAME", "earth-knowledge-source")
index_name = os.getenv("AZURE_SEARCH_INDEX", "earth-at-night")
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_gpt_deployment = os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT", "gpt-4.1-mini")
azure_openai_gpt_model = os.getenv("AZURE_OPENAI_GPT_MODEL", "gpt-4.1-mini")
azure_openai_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
azure_openai_embedding_model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
base_name = os.getenv("AZURE_SEARCH_AGENT_NAME", "earth-knowledge-base")

# Parse the resource ID to extract subscription and other components
parsed_resource_id = parse_resource_id(project_resource_id)
subscription_id = parsed_resource_id['subscription']
resource_group = parsed_resource_id['resource_group']
account_name = parsed_resource_id['name']
project_name = parsed_resource_id['child_name_1']
```

### Create a search index

This step creates a search index that contains plain text and vector content. You can use an existing index, but it must meet the criteria for agentic retrieval workloads. The primary schema requirement is a semantic configuration with a `default_configuration_name`.

For more information about this step, see [Create an index for agentic retrieval in Azure AI Search](agentic-retrieval-how-to-create-index.md).

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizer, AzureOpenAIVectorizerParameters,
    HnswAlgorithmConfiguration, SearchField, SearchIndex,
    SemanticConfiguration, SemanticField, SemanticPrioritizedFields,
    SemanticSearch, VectorSearch, VectorSearchProfile
)

index = SearchIndex(
    name=index_name,
    fields=[
        SearchField(name="id", type="Edm.String", key=True, filterable=True, sortable=True, facetable=True),
        SearchField(name="page_chunk", type="Edm.String", filterable=False, sortable=False, facetable=False),
        SearchField(name="page_embedding_text_3_large", type="Collection(Edm.Single)", stored=False, vector_search_dimensions=3072, vector_search_profile_name="hnsw_text_3_large"),
        SearchField(name="page_number", type="Edm.Int32", filterable=True, sortable=True, facetable=True)
    ],
    vector_search=VectorSearch(
        profiles=[VectorSearchProfile(name="hnsw_text_3_large", algorithm_configuration_name="alg", vectorizer_name="azure_openai_text_3_large")],
        algorithms=[HnswAlgorithmConfiguration(name="alg")],
        vectorizers=[
            AzureOpenAIVectorizer(
                vectorizer_name="azure_openai_text_3_large",
                parameters=AzureOpenAIVectorizerParameters(
                    resource_url=azure_openai_endpoint,
                    deployment_name=azure_openai_embedding_deployment,
                    model_name=azure_openai_embedding_model
                )
            )
        ]
    ),
    semantic_search=SemanticSearch(
        default_configuration_name="semantic_config",
        configurations=[
            SemanticConfiguration(
                name="semantic_config",
                prioritized_fields=SemanticPrioritizedFields(
                    content_fields=[
                        SemanticField(field_name="page_chunk")
                    ]
                )
            )
        ]
    )
)

index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.create_or_update_index(index)
print(f"Index '{index_name}' created or updated successfully")
```

### Upload documents to the index

Currently, the search index is empty. Upload documents to the index so your knowledge base has content to retrieve. This code passes data from NASA's Earth at Night e-book to the search client for indexing.

For more information about this step, see [Pushing data to an index in Azure AI Search](search-what-is-data-import.md#pushing-data-to-an-index).

```python
import requests
from azure.search.documents import SearchIndexingBufferedSender

url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}'")
```

### Create a knowledge source

A knowledge source represents searchable content. This step creates a search index knowledge source that points to the index you previously created. You can also create knowledge sources that ingest data from external sources, such as Azure Blob Storage or Microsoft OneLake, into auto-generated indexes. Alternatively, you can create knowledge sources that access remote, non-indexed content.

For more information about this step, see [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md).

```python
from azure.search.documents.indexes.models import (
    KnowledgeSource,
    SearchIndexKnowledgeSourceParameters
)

# Create a knowledge source that references the search index
knowledge_source_name = "sample-knowledge-source"
knowledge_source = KnowledgeSource(
    name=knowledge_source_name,
    source_type="searchIndex",
    parameters=SearchIndexKnowledgeSourceParameters(
        index_name=index_name
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source_name}' created successfully")
```

### Create a knowledge base

A knowledge base uses agentic to process queries against your knowledge sources. It connects to your LLM deployment to enable intelligent query planning and response generation.

When you create a knowledge base, you specify the LLM model parameters, the knowledge sources to query, and the data output mode: `EXTRACTIVE_DATA` or `ANSWER_SYNTHESIS`. This solution uses extractive data to provide the agent with unprocessed content for grounding and reasoning.

This step also stores the MCP endpoint of your knowledge base in a variable. The agent you create in a later step uses this endpoint to access the knowledge base.

For more information about this step, see [Create a knowledge base for agentic retrieval in Azure AI Search](agentic-retrieval-how-to-create-knowledge-base.md).

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    KnowledgeBase, KnowledgeRetrievalMinimalReasoningEffort,
    KnowledgeRetrievalOutputMode, KnowledgeSourceReference
)

knowledge_base = KnowledgeBase(
    name=base_name,
    knowledge_sources=[
        KnowledgeSourceReference(
            name=knowledge_source_name
        )
    ],
    output_mode=KnowledgeRetrievalOutputMode.EXTRACTIVE_DATA,
    retrieval_reasoning_effort=KnowledgeRetrievalMinimalReasoningEffort()
)


index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.create_or_update_knowledge_base(knowledge_base=knowledge_base)
print(f"Knowledge base '{base_name}' created or updated successfully")

mcp_endpoint = f"{endpoint}/knowledgebases/{base_name}/mcp?api-version=2025-11-01-Preview"
```

### Create a project connection

The Azure AI Search development tasks are now complete. However, before you can create an agent, you must create a project connection in Microsoft Foundry that points to the MCP endpoint of your knowledge base. This endpoint allows the agent to access your knowledge base.

```python
import requests
from azure.identity import get_bearer_token_provider

bearer_token_provider = get_bearer_token_provider(credential, "https://management.azure.com/.default")
headers = {
    "Authorization": f"Bearer {bearer_token_provider()}",
}

response = requests.put(
    f"https://management.azure.com{project_resource_id}/connections/{project_connection_name}?api-version=2025-10-01-preview",
    headers=headers,
    json={
        "name": project_connection_name,
        "type": "Microsoft.MachineLearningServices/workspaces/connections",
        "properties": {
            "authType": "ProjectManagedIdentity",
            "category": "RemoteTool",
            "target": mcp_endpoint,
            "isSharedToAll": True,
            "audience": "https://search.azure.com/",
            "metadata": { "ApiType": "Azure" }
        }
    }
)

response.raise_for_status()
print(f"Connection '{project_connection_name}' created or updated successfully.")
```

### Set up an AI project client

Use [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient?view=azure-python-preview&preserve-view=true) to create a client connection to your Microsoft Foundry project.

```python
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)

list(project_client.agents.list())
```

### Create an agent with the MCP tool

You can now create an agent configured with the MCP tool. When the agent receives a user query, it can call your knowledge base through the MCP tool to retrieve relevant content for response grounding.

The agent definition includes instructions that specify its behavior and the project connection you previously created. Based on our experiments, these instructions are effective in maximizing the accuracy of knowledge base invocations and ensuring proper citation formatting.

For more information about this step, see [Quickstart: Create a new agent](/azure/ai-foundry/agents/quickstart).

```python
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

# Define agent instructions
instructions = """
You are a helpful assistant that must use the knowledge base to answer all the questions from user. You must never answer from your own knowledge under any circumstances.
Every answer must always provide annotations for using the MCP knowledge base tool and render them as: `【message_idx:search_idx†source_name】`
If you cannot find the answer in the provided knowledge base you must respond with "I don't know".
"""

# Create MCP tool with knowledge base connection
mcp_kb_tool = MCPTool(
    server_label="knowledge-base",
    server_url=mcp_endpoint,
    require_approval="never",
    allowed_tools=["knowledge_base_retrieve"],
    project_connection_id=project_connection_name
)

# Create agent with MCP tool
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

### Connect to a remote SharePoint knowledge source

Optionally, if your knowledge base includes a [remote SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-remote.md), you must also include the `x-ms-query-source-authorization` header in the MCP tool connection.

```python
from azure.identity import get_bearer_token_provider

# Create MCP tool with SharePoint authorization header
mcp_kb_tool = MCPTool(
    server_label = "knowledge-base",
    server_url = mcp_endpoint,
    require_approval = "never",
    allowed_tools = ["knowledge_base_retrieve"],
    project_connection_id = project_connection_name,
    headers = {
        "x-ms-query-source-authorization": get_bearer_token_provider(credential, "https://search.azure.com/.default")()
    }
)
```

### Chat with the agent

Your client app uses the Conversations and [Responses](/azure/ai-foundry/openai/how-to/responses) APIs from Azure OpenAI to send user input to the agent. The client creates a conversation and passes each user message to the agent through the Responses API, resembling a typical chat experience.

The agent manages the conversation, determines when to call your knowledge base through the MCP tool, and returns a natural-language response (with references to the retrieved content) to the client app.

```python
# Get the OpenAI client for responses and conversations
openai_client = project_client.get_openai_client()

# Create conversation
conversation = openai_client.conversations.create()

# Send request to trigger the MCP tool
response = openai_client.responses.create(
    conversation = conversation.id,
    input = """
        Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
        Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
    """,
    extra_body = {"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response: {response.output_text}")
```

### Clean up resources

When you work in your own subscription, it's a good idea to finish a project by determining whether you still need the resources you created. Resources that are left running can cost you money.

In the Azure portal, you can manage your Azure AI Search and Microsoft Foundry resources by selecting **All resources** or **Resource groups** from the left pane.

You can also delete individual objects:

```python
# Delete the agent
project_client.agents.delete_version(agent.name, agent.version)
print(f"AI agent '{agent.name}' version '{agent.version}' deleted successfully")

# Delete the knowledge base
index_client.delete_knowledge_base(base_name)
print(f"Knowledge base '{base_name}' deleted successfully")

# Delete the knowledge source
index_client.delete_knowledge_source(knowledge_source=knowledge_source_name)
print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")

# Delete the search index
index_client.delete_index(index)
print(f"Index '{index_name}' deleted successfully")
```

## Improve data quality

By default, search results from your knowledge base are consolidated into a large unified string that can be passed to the agent for grounding. Azure AI Search provides the following indexing and relevance-tuning features to help you generate high-quality results. You can implement these features in the search index, and the improvements in search relevance are evident in the quality of retrieval responses.

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

The Responses API controls what is sent to the agent and knowledge base. To optimize performance and relevance, adjust the agent instructions to summarize or filter the chat history before sending it to the MCP tool.

## Control costs and limit operations

For insights into the query plan, look at output tokens in the [activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array) of knowledge base responses.

## Improve performance

To optimize performance and reduce latency, consider the following strategies:

+ Summarize message threads.

+ Use `gpt-4.1-mini` or a smaller model that performs faster.

+ Set `maxOutputSize` on the [retrieve action](agentic-retrieval-how-to-retrieve.md) to govern the size of the response or `maxRuntimeInSeconds` for time-bound processing.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
