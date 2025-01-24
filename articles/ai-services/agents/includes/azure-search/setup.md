---
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 12/10/2024
---

## Setup: Create an agent that can use an existing Azure AI Search index

#### Prerequisite: Have an existing Azure AI Search index
A prerequisite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal using the import and vectorize data wizard.
-  [Quickstart: Create a vector index with the import and vectorize data wizard in the Azure portal](../../../../search/search-get-started-portal-import-vectors.md)


#### Complete the agent setup
- **Option 1: Standard Agent Setup using an existing AI Search resource** If you want your agent to use an existing AI Search resource to create new indexes or bring existing ones you should use the [standard agent setup and add your AI Search resource ID](../../quickstart.md). 
    - You can provide your Azure AI Search resource ID in the bicep file. Your resource ID should be in the format: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}`.
- **Option 2: Standard Agent Setup** If you want to create a new Azure AI Search resource for your agents to use when creating new indexes follow the [standard agent setup](../../quickstart.md).


#### Create a project connection to the Azure AI Search resource with the index you want to use
Once you have completed the standard agent setup, you must create a project connection to the Azure AI Search resource that contains the index you want to use. 

If you already connected the AI Search resource that contains the index you want to use to your project, skip this step. 

##### Get your Azure AI Search resource connection key and endpoint
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

##### Create an Azure AI Search project connection
If you use Microsoft Entra ID for the connection authentication type, you need to manually assign the project managed identity the roles Search Index Data Contributor and Search Service Contributor to the Azure AI Search resource.

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