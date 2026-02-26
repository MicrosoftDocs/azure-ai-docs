---
title: 'How to use an existing AI Search index with the Azure AI Search tool'
titleSuffix: Microsoft Foundry
description: Learn how to use Agents Azure AI Search tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/15/2025
author: alvinashcraft
ms.author: aashcraft
ms.reviewer: aahi
ms.custom: azure-ai-agents
---

# Azure AI Search tool


> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Azure AI Search tool documentation](../../../default/agents/how-to/tools/ai-search.md).


The [Azure AI Search](/azure/search/search-what-is-azure-search) tool in Agent Service connects an agent to a new or existing search index. You can use this tool to retrieve and summarize your indexed documents, grounding the agent's responses in your proprietary content.

This article describes how to set up the Azure AI Search tool, including creating a project connection and adding the tool to your agent.

## Prerequisites

+ A [Microsoft Foundry agent](../../quickstart.md).

+ An [Azure AI Search index configured for vector search](../../../../search/search-get-started-portal-import-vectors.md). The index must include:

    + One or more `Edm.String` (text) fields attributed as searchable and retrievable.

    + One or more `Collection(Edm.Single)` (vector) fields attributed as searchable.

> [!TIP]
> Instead of using an existing index, you can create an index without leaving the Foundry portal. For more information, see the [Add the tool to an agent](#add-the-tool-to-an-agent) section.

## Usage support

| Azure AI foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Limitations

+ To use the Azure AI Search tool in the Foundry portal behind a virtual network, you must create an agent using the SDK or REST API. After you create the agent programmatically, you can then use it in the portal. 

+ The Azure AI Search tool can only target one index. To use multiple indexes, consider using [connected agents](../connected-agents.md), each with a configured index.
  
+ A Foundry resource with basic agent deployments does not support private Azure AI Search resources, nor Azure AI Search  with public network access disabled and a private endpoint. To use a private Azure AI Search tool with your agents, deploy the standard agent with virtual network injection.

+ Your Azure AI Search resource and Foundry Agent need to be in the same tenant.

## Setup

In this section, you create a connection between the Foundry project that contains your agent and the Azure AI Search service that contains your index.

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

        :::image type="content" source="../../media/tools/ai-search\connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../media/tools/ai-search\connection-endpoint.png":::

1. To get the API key:

    1. From the left pane, select **Settings** > **Keys**.

    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

        :::image type="content" source="../../media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search\azure-portal.png":::

    1. Make a note of one of the keys under **Manage admin keys**.

#### [Keyless authentication](#tab/keyless)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. To get the endpoint:

    1. From the left pane, select **Overview**.
    
    1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

        :::image type="content" source="../../media/tools/ai-search\connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../media/tools/ai-search\connection-endpoint.png":::

1. To enable RBAC:

    1. From the left pane, select **Settings** > **Keys**.

    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

        :::image type="content" source="../../media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search\azure-portal.png":::

1. To assign the necessary roles:

    1. From the left pane, select **Access control (IAM)**.

    1. Select **Add** > **Add role assignment**.

    1. Assign the **Search Index Data Contributor** role to the managed identity of your project.

    1. Repeat the role assignment for **Search Service Contributor**.

---

### Create the project connection

The next step is to create the project connection using the search service details you gathered. The connection name must be the name of your search index. For more information about this step, see [Add a new connection to your project](../../../how-to/connections-add.md).

Select the tab for your desired usage method.

#### [Azure CLI](#tab/azurecli)

**Create the following connections.yml file:**

You can use a YAML configuration file for both key-based and keyless authentication. Replace the ```name```, ```endpoint```, and ```api_key``` (optional) placeholders with your search service details. For more information, see the [Azure AI Search connection YAML schema](../../../../machine-learning\reference-yaml-connection-ai-search.md). 

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

#### [Foundry](#tab/azureaifoundry)
<!--
1. [!INCLUDE [version-sign-in](../../../includes/version-sign-in.md)]
-->
Select your project.

1. On the **Overview** page, select **Open in management center**.

    :::image type="content" source="../../media/tools/ai-search\project-studio.png" alt-text="A screenshot of a project in Foundry." lightbox="../../media/tools/ai-search\project-studio.png":::

1. From the left pane, select **Connected resources**, and then select **New Connection**.
     
    :::image type="content" source="../../media/tools/ai-search\project-connections-page.png" alt-text="A screenshot of the project connections page." lightbox="../../media/tools/ai-search\project-connections-page.png":::

1. Select **Azure AI Search**.

    :::image type="content" source="../../media/tools/ai-search\select.png" alt-text="A screenshot of the Azure AI Search connection type the user should select." lightbox="../../media/tools/ai-search\select.png":::

1. Select **Enter manually**, and then provide the details required by your chosen authentication method. 

    :::image type="content" source="../../media/tools/ai-search\connection-2.png" alt-text="A screenshot the required fields to add a new Azure AI Search connection." lightbox="../../media/tools/ai-search\connection-2.png":::

1. Select **Add connection** to create the project connection.

1. Verify that the connection appears on the **Connected resources** page.

    :::image type="content" source="../../media/tools/ai-search\success-connection.png" alt-text="A screenshot of the project connections page with a new Azure AI Search connection added." lightbox="../../media/tools/ai-search\success-connection.png":::

---

## Add the tool to an agent

You can add the Azure AI Search tool to an agent programmatically or through the Foundry portal. For programmatic examples, see [Use an existing index with the Azure AI Search tool](azure-ai-search-samples.md).

To add the tool through the portal:

1. From the left pane, select **Agents**.

1. Select your agent from the list, and then select **Knowledge** > **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Azure AI Search**. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

1. Under **Connect to an index**, select **Indexes that are not part of this project**.

1. Under **Azure AI Search resource connection**, select the project connection you created in the previous section.

1. Under **Azure AI Search index**, select your vector index.

    > [!TIP]
    > If you don't have an index, select **Create a new index**. You're then prompted to name the index, connect to a data source, select an existing embedding model deployment, and agree to the terms.
    >
    > After you create the index, you can use it both inside and outside your agent. For example, you can use the index with the Azure AI Search REST APIs or SDKs.

1. Under **Display name**, enter the name of your index.

1. Depending on your index configuration, choose one of the following [search types](../../../openai/concepts/use-your-data.md#search-types):

    + **Simple**
    + **Semantic**
    + **Vector**
    + **Hybrid (vector + keyword)**
    + **Hybrid + semantic**

    By default, the Azure AI Search tool runs a hybrid search (vector + keyword) on all text fields.

1. Select **Connect** to add the Azure AI Search tool to your agent.

    :::image type="content" source="../../media/tools/ai-search/connect-tool.png" alt-text="A screenshot of the Connect button in the Foundry portal." lightbox="../../media/tools/ai-search/connect-tool.png":::

## Next step

Try some programmatic examples of configuring and using the Azure AI Search tool:

> [!div class="nextstepaction"]
> [Use an existing index with the Azure AI Search tool](azure-ai-search-samples.md)
