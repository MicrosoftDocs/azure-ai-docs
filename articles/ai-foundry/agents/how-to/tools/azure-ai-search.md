---
title: 'How to use an existing AI Search index with the Azure AI Search tool'
titleSuffix: Azure AI Foundry
description: Learn how to use Agents Azure AI Search tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 08/07/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Use an existing AI Search index with the Azure AI Search tool

You can use an existing Azure AI Search index with the agent's Azure AI Search tool.

> [!TIP]
> You can create a new index without leaving the Azure AI Foundry portal. For more information, see the [Add the Azure AI Search tool to an agent](#add-the-azure-ai-search-tool-to-an-agent) section.

Azure AI Search indexes must be configured properly and meet the following requirements:
- The index must contain at least one searchable & retrievable text field (type Edm.String) 
- The index must contain at least one searchable vector field (type Collection(Edm.Single)) 

## Search types

You can specify the search type for your index by choosing one of the following
- Simple
- Semantic
- Vector
- Hybrid (Vector + Keyword)
- Hybrid (Vector + Keyword + Semantic)

You can have indexes without a specified search type. By default, the Azure AI Search tool runs a hybrid search (keyword + vector) on all text fields.

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Setup

### Prerequisite: Have an existing Azure AI Search index
A prerequisite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal using the import and vectorize data wizard.
-  [Quickstart: Create a vector index with the import and vectorize data wizard in the Azure portal](../../../../search\search-get-started-portal-import-vectors.md)

### Create a project connection to the Azure AI Search resource with the index you want to use
Once you complete the agent setup, you must create a project connection to the Azure AI Search resource that contains the index you want to use. 

If you already connected the AI Search resource that contains the index you want to use to your project, skip this step. 

#### Get your Azure AI Search resource connection key and endpoint
1. Access your Azure AI Search resource.
     - In the Azure portal, navigate to the AI Search resource that contains the index you want to use. 
2. Copy the connection endpoint.
    - In the Overview tab, copy the URL of your resource. The URL should be in the format `https://<your-resource-name>.search.windows.net/`.
     :::image type="content" source="../../media/tools/ai-search\connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../media/tools/ai-search\connection-endpoint.png":::

3. Verify API Access control is set to **Both** and copy one of the keys under **Manage admin keys**. 
    - From the left-hand navigation bar, scroll down to the Settings section and select **Keys**. 
    - Under the **API Access Control** section, ensure the option **Both** API key and Role-based access control is selected.
    - If you want the connection to use API Keys for authentication, copy one of the keys under **Manage admin keys**.
    :::image type="content" source="../../media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search\azure-portal.png":::

#### Create an Azure AI Search project connection
If you use Microsoft Entra ID for the connection authentication type, you need to manually assign the project managed identity the roles Search Index Data Contributor and Search Service Contributor to the Azure AI Search resource. The connection **name** must be the AI Search **index** name. 

# [Azure CLI](#tab/azurecli)

**Create the following connections.yml file**

You can use either an API key or keyless YAML configuration file. Replace the ```name```, ```endpoint```, and ```api_key``` placeholders with your Azure AI Search resource values. For more information on the YAML configuration file, see the [Azure AI Search connection YAML schema](../../../../machine-learning\reference-yaml-connection-ai-search.md). 

Here's an API Key example:

```yml
name: my_project_acs_connection_keys
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
api_key: XXXXXXXXXXXXXXX
```

Here's a keyless example:

```yml    
name: my_project_acs_connection_credentialless
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
```

**Then, run the following command:**

Replace ```my_resource``` and ```my_project_name``` with your resource group and project name created in the agent setup.

```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_project_name}
```

# [Python](#tab/pythonsdk)

To create a project connection to your Azure AI Search resource, replace the ```my_connection_name```, ```my_endpoint```, and ```my_key``` (optional) placeholders with your Azure AI Search connection details and run the following code:

```python
from azure.ai.ml.entities import AzureAISearchConnection

# create an Azure AI Search project connection
my_connection_name = "my-connection-name"
my_endpoint = "my-endpoint" # this could also be called target
my_api_keys = None # leave blank for Authentication type = AAD

my_connection = AzureAISearchConnection(name=my_connection_name,
                                    endpoint=my_endpoint, 
                                    api_key= my_api_keys)

# Create the connection
ml_client.connections.create_or_update(my_connection)
```

# [Azure AI Foundry](#tab/azureaifoundry)

1. In Azure AI Foundry, navigate to the project you created in the agent setup. Select **Open in management center**.
    :::image type="content" source="../../media/tools/ai-search\project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../../media/tools/ai-search\project-studio.png":::

1. Select the **Connections** tab and then select **Add Connection**.
 :::image type="content" source="../../media/tools/ai-search\project-connections-page.png" alt-text="A screenshot of the project connections page." lightbox="../../media/tools/ai-search\project-connections-page.png":::

1. Select **Azure AI Search**.
 :::image type="content" source="../../media/tools/ai-search\select.png" alt-text="A screenshot of the Azure AI Search connection type the user should select." lightbox="../../media/tools/ai-search\select.png":::

1. Provide the required connection details for the Azure AI Search resource you want to use. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, select **Add connection**.
:::image type="content" source="../../media/tools/ai-search\connection-2.png" alt-text="A screenshot the required fields to add a new Azure AI Search connection." lightbox="../../media/tools/ai-search\connection-2.png":::

1. Verify that the connection was successfully created and now appears in the project's Connections tab.
:::image type="content" source="../../media/tools/ai-search\success-connection.png" alt-text="A screenshot of the project connections page with a new Azure AI Search connection added." lightbox="../../media/tools/ai-search\success-connection.png":::
---

Now that you created a project connection to your Azure AI Search resource, you can configure and start using the Azure AI Search tool with the SDK. See the code examples tab to get started.

-------------------------
## Add the Azure AI Search tool to an agent

You can add the Azure AI Search tool to an agent programmatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal:

1. In the **Agents** screen for your agent, scroll down the **Setup** pane. Then select **Knowledge** > **+ Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Azure AI Search**. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

1. Under **Connect to an index**, you can either select an existing Azure AI Search connection or create a new one. Let's select **Indexes that are not part of this project**.
1. Select an existing Azure AI Search connection. You can create a new one in the Azure portal and then return to this wizard.
1. After you select the connection, you can select or create an index to use with the Azure AI Search tool. Let's select **Create a new index**.

    > [!TIP]
    > You can create a new index without leaving the Azure AI Foundry portal. If you select **Create a new index**, you're prompted to provide the index name and select the search type.

    :::image type="content" source="../../media/tools/knowledge-tools-ai-search-connect-index.png" alt-text="A screenshot with the option to connect to an index that doesn't yet exist in the project." lightbox="../../media/tools/knowledge-tools-ai-search-connect-index.png":::

1. Enter the index name, connect your data, choose an embedding model, and agree to the terms. Then select **Create index**.

    :::image type="content" source="../../media/tools/knowledge-tools-ai-search-create-index.png" alt-text="A screenshot with the option to create a new index in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-ai-search-create-index.png":::

1. The index is created and connected to the [Azure AI Search](/azure/search/) service. You can now use the index with the Azure AI Search tool in your agent. You can also use the index outside of the agent, such as the Azure AI Search REST API or SDKs.


## Limitations

Currently, if you want to use the Azure AI Search tool in the Azure AI Foundry portal behind a virtual network, you must create an agent using the SDK or REST API. After creating the agent in a code-based manner, you can then use it in the portal. 

The Azure AI Search tool can only include one search index. If you want to utilize multiple indexes, consider using [connected agents](../connected-agents.md) with an Azure AI search index configured with each agent.

## Next steps

* See examples on how to use the [Azure AI Search tool](azure-ai-search-samples.md). 
