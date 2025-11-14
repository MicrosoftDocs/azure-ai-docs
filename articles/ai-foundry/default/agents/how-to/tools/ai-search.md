---
title: 'How to use an AI Search index with the agents API'
titleSuffix: Microsoft Foundry
description: Learn how to use Agents Azure AI Search tool for the agents API.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/12/2025
author: haileytap
ms.author: haileytapia
ms.reviewer: aahi
ms.custom: azure-ai-agents
---

# Azure AI Search tool for agents 

> [!NOTE]
> There are new ways to add knowledge to your agent. For the latest recommended approach, see [Use knowledge to improve retrieval quality in Microsoft Foundry Agent Service](./knowledge-retrieval.md).

The [Azure AI Search](/azure/search/search-what-is-azure-search) tool in Microsoft Foundry Agent Service connects an agent to a new or existing search index. You can use this tool to retrieve and summarize your indexed documents, grounding the agent's responses in your proprietary content.

## Prerequisites

+ The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

+ An [Azure AI Search index configured for vector search](../../../../../search/search-get-started-portal-import-vectors.md). The index must include:

    + One or more `Edm.String` (text) fields attributed as searchable and retrievable.

    + One or more `Collection(Edm.Single)` (vector) fields attributed as searchable.

## Code example

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AzureAISearchAgentTool,
    PromptAgentDefinition,
    AzureAISearchToolResource,
    AISearchIndexResource,
    AzureAISearchQueryType,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="""You are a helpful assistant. You must always provide citations for
            answers using the tool and render them as: `[message_idx:search_idx†source]`.""",
            tools=[
                AzureAISearchAgentTool(
                    azure_ai_search=AzureAISearchToolResource(
                        indexes=[
                            AISearchIndexResource(
                                project_connection_id=os.environ["AI_SEARCH_PROJECT_CONNECTION_ID"],
                                index_name=os.environ["AI_SEARCH_INDEX_NAME"],
                                query_type=AzureAISearchQueryType.SIMPLE,
                            ),
                        ]
                    )
                )
            ],
        ),
        description="You are a helpful agent.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input(
        """Enter your question for the AI Search agent available in the index
        (e.g., 'Tell me about the mental health services available from Premera'): \n"""
    )

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(
                                f"URL Citation: {annotation.url}, "
                                f"Start index: {annotation.start_index}, "
                                f"End index: {annotation.end_index}"
                            )
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```


## Limitations

+ To use the Azure AI Search tool in the Microsoft Foundry portal behind a virtual network, you must create an agent using the SDK or REST API. After you create the agent programmatically, you can then use it in the portal. 

+ The Azure AI Search tool can only target one index.
  
+ A Microsoft Foundry resource with basic agent deployments does not support private Azure AI Search resources, nor Azure AI Search  with public network access disabled and a private endpoint. To use a private Azure AI Search tool with your agents, deploy the standard agent with virtual network injection.

+ Your Azure AI Search resource and Microsoft Foundry Agent need to be in the same tenant.

## Setup

In this section, you create a connection between the Microsoft Foundry project that contains your agent and the Azure AI Search service that contains your index.

If you already connected your project to your search service, skip this section. 

### Get search service connection details

The project connection requires the endpoint of your search service and either key-based authentication or keyless authentication with Microsoft Entra ID.

For keyless authentication, you must enable role-based access control (RBAC) and assign roles to your project's managed identity. Although this method involves extra steps, it enhances security by eliminating the need for hard-coded API keys.

Select the tab for your desired authentication method.

#### [Key-based authentication](#tab/keys)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. To get the endpoint:

    1. From the left pane, select **Overview**.
    
    1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

        :::image type="content" source="../../../../agents/media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search/connection-endpoint.png":::

1. To get the API key:

    1. From the left pane, select **Settings** > **Keys**.

    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

        :::image type="content" source="../../../../agents/media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search\azure-portal.png":::

    1. Make a note of one of the keys under **Manage admin keys**.

#### [Keyless authentication](#tab/keyless)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. To get the endpoint:

    1. From the left pane, select **Overview**.
    
    1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

        :::image type="content" source="../../../../agents/media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search/connection-endpoint.png":::

1. To enable RBAC:

    1. From the left pane, select **Settings** > **Keys**.

    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

        :::image type="content" source="../../../../agents/media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search\azure-portal.png":::

1. To assign the necessary roles:

    1. From the left pane, select **Access control (IAM)**.

    1. Select **Add** > **Add role assignment**.

    1. Assign the **Search Index Data Contributor** role to the managed identity of your project.

    1. Repeat the role assignment for **Search Service Contributor**.

---

### Create the project connection

The next step is to create the project connection using the search service details you gathered. The connection name must be the name of your search index.

You can use the Microsoft AI Foundry portal, or one of the following options.

#### [Azure CLI](#tab/azurecli)

**Create the following connections.yml file:**

You can use a YAML configuration file for both key-based and keyless authentication. Replace the ```name```, ```endpoint```, and ```api_key``` (optional) placeholders with your search service details. For more information, see the [Azure AI Search connection YAML schema](../../../../../machine-learning/reference-yaml-connection-ai-search.md). 

Here's a key-based example:

```yml
name: my_project_acs_connection_keys
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
api_key: XXXXXXXXXXXXXXX
```

Here's a keyless example:

```yml    
name: my_project_acs_connection_keyless
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
```

**Then, run the following command:**

Replace ```my_resource``` with the resource group that contains your project and ```my_project_name``` with the name of your project.

```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_project_name}
```

#### [Python](#tab/pythonsdk)

Replace the ```my_connection_name```, ```my_endpoint```, and ```my_key``` (optional) placeholders with your search service details, and then run the following code:

```python
from azure.ai.ml.entities import AzureAISearchConnection

# Create an Azure AI Search project connection
my_connection_name = "my-connection-name"
my_endpoint = "my-endpoint" # This could also be called target
my_api_keys = None # Leave blank for Authentication type = AAD

my_connection = AzureAISearchConnection(name=my_connection_name,
                                    endpoint=my_endpoint, 
                                    api_key= my_api_keys)

# Create the connection
ml_client.connections.create_or_update(my_connection)
```

---
