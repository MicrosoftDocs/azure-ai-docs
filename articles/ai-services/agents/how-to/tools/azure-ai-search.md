---
title: 'How to use an existing AI Search index with the Azure AI Search tool'
titleSuffix: Azure AI Foundry
description: Learn how to use Agents Azure AI Search tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/11/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Use an existing AI Search index with the Azure AI Search tool

Use an existing Azure AI Search index with the agent's Azure AI Search tool.

> [!NOTE] 
> Azure AI Search indexes must meet the following requirements:
> - The index must contain at least one searchable & retrievable text field (type Edm.String) 
> - The index must contain at least one searchable vector field (type Collection(Edm.Single)) 
> - The index is assumed to be configured properly

## Search types
You can specify the search type for your index by choosing one of the following
- Simple
- Semantic
- Vector
- Hybrid (Vector + Keyword)
- Hybrid (Vector + Keyword + Semantic)


**Indexes without a specified search type**
- By default, the Azure AI Search tool runs a hybrid search (keyword + vector) on all text fields 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Setup

### Prerequisite: Have an existing Azure AI Search index
A prerequisite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal using the import and vectorize data wizard.
-  [Quickstart: Create a vector index with the import and vectorize data wizard in the Azure portal](../../../../search/search-get-started-portal-import-vectors.md)

### Create a project connection to the Azure AI Search resource with the index you want to use
Once you have completed the agent setup, you must create a project connection to the Azure AI Search resource that contains the index you want to use. 

If you already connected the AI Search resource that contains the index you want to use to your project, skip this step. 

#### Get your Azure AI Search resource connection key and endpoint
1. Access your Azure AI Search resource.
     - In the Azure portal, navigate to the AI Search resource that contains the index you want to use. 
2. Copy the connection endpoint.
    - In the Overview tab, copy the URL of your resource. The URL should be in the format `https://<your-resource-name>.search.windows.net/`.
     :::image type="content" source="../../media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../media/tools/ai-search/connection-endpoint.png":::

3. Verify API Access control is set to **Both** and copy one of the keys under **Manage admin keys**. 
    - From the left-hand navigation bar, scroll down to the Settings section and select **Keys**. 
    - Under the **API Access Control** section, ensure the option **Both** API key and Role-based access control is selected.
    - If you want the connection to use API Keys for authentication, copy one of the keys under **Manage admin keys**.
    :::image type="content" source="../../media/tools/ai-search/azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/azure-portal.png":::

#### Create an Azure AI Search project connection
If you use Microsoft Entra ID for the connection authentication type, you need to manually assign the project managed identity the roles Search Index Data Contributor and Search Service Contributor to the Azure AI Search resource. The connection **name** must be the AI Search **index** name. 

# [Azure CLI](#tab/azurecli)

**Create the following connections.yml file**


You can use either an API key or credential-less YAML configuration file. Replace the placeholders for ```name```, ```endpoint``` and ```api_key``` with your Azure AI Search resource values. For more information on the YAML configuration file, see the [Azure AI Search connection YAML schema](../../../../machine-learning/reference-yaml-connection-ai-search.md). 
- API Key example:

    ```yml
    name: my_project_acs_connection_keys
    type: azure_ai_search
    endpoint: https://contoso.search.windows.net/
    api_key: XXXXXXXXXXXXXXX
    ```

- Credential-less

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
Replace the placeholders ```my_connection_name```, ```my_endpoint```, and ```my_key``` (optional)  with your Azure AI Search connection details and run the following code to create a project connection to your Azure AI Search resource.
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
1. In Azure AI Foundry, navigate to the project you created in the agent setup. Click on **Open in management center**.
    :::image type="content" source="../../media/tools/ai-search/project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../../media/tools/ai-search/project-studio.png":::

2. Click on the **Connections** tab and select **Add Connection**.
 :::image type="content" source="../../media/tools/ai-search/project-connections-page.png" alt-text="A screenshot of the project connections page." lightbox="../../media/tools/ai-search/project-connections-page.png":::

3. Select **Azure AI Search**.
 :::image type="content" source="../../media/tools/ai-search/select.png" alt-text="A screenshot of the Azure AI Search connection type the user should select." lightbox="../../media/tools/ai-search/select.png":::

4. Provide the required connection details for the Azure AI Search resource you want to use. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, click **Add connection**.
:::image type="content" source="../../media/tools/ai-search/connection-2.png" alt-text="A screenshot the required fields to add a new Azure AI Search connection." lightbox="../../media/tools/ai-search/connection-2.png":::

5. Verify that the connection was successfully created and now appears in the project's Connections tab.
:::image type="content" source="../../media/tools/ai-search/success-connection.png" alt-text="A screenshot of the project connections page with a new Azure AI Search connection added." lightbox="../../media/tools/ai-search/success-connection.png":::
---

Now that you have created a project connection to your Azure AI Search resource, you can configure and start using the Azure AI Search tool with the SDK. See the code examples tab to get started.

-------------------------
## Add the Azure AI Search tool to an agent

You can add the Azure AI Search tool to an agent programmatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal:

1. In the **Agents** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Azure AI Search** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

## Next steps

* See examples on how to use the [Azure AI Search tool](./azure-ai-search-samples.md). 
