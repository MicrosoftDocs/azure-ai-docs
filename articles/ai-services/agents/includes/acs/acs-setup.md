## Setup: Create an agent that can use an existing Azure AI Search index

#### 1. Prerequisite: Have an existing Azure AI Search index
A prerequisite of using the Azure AI Search tool is to have an existing Azure AI Search index. If you don't have an existing index, you can create one in the Azure portal or via REST API.
-  [Quickstart: Create a vector index using the Azure portal](../../../../search/search-get-started-portal-import-vectors.md)
- [Quickstart: Create a vector index using REST API](../../../../search/search-get-started-vector.md)


#### 2. Complete the agent setup
- **Option 1: Standard Agent Setup using existing AI Search resource** If you want your agent to use an existing AI Search resource to create new indexes or bring existing ones you should use the [standard agent setup and add your AI Search resource ID](../../quickstart.md). 
    - You can provide your Azure AI Search resource ID in the bicep file. Your resource ID should be in the format: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}`.
- **Option 2: Standard Agent Setup** If you want to create a new Azure AI Search resource for your agents to use when creating new indexes follow the [standard agent setup](../../quickstart.md).


#### 3. Create a project connection to the Azure AI Search resource with the index you want to use
If you already connected the AI Search resource that contains the index you want to use to your project, skip this step.

##### Get your Azure AI Search resource connection key and endpoint
- Access your Azure AI Search resource.
     - In the Azure portal, navigate to the AI Search resource that contains the index you want to use. 
- Copy the connection endpoint.
    - In the Overview tab, copy the URL of your resource. The URL should be in the format `https://<your-resource-name>.search.windows.net/`.
     :::image type="content" source="../../media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../media/tools/ai-search/connection-endpoint.png":::

- Verify API Acccess control is set to **Both** and copy one of the keys under **Manage admin keys**. 
    - From the left-hand navigation bar, scroll down to the Settings section and select **Keys**. 
    - Under the **API Access Control** section, ensure the option **Both** API key and Role-based access control is selected.
    - If you want the connection to use API Keys for authentication, copy one of the keys under **Manage admin keys**.
    :::image type="content" source="../../media/tools/ai-search/acs-azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../media/tools/ai-search/acs-azure-portal.png":::

##### Create an Azure AI Search project connection

# [Azure CLI](#tab/azurecli)
```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_hub_name}
```

You can use either an API key or credential-less YAML configuration file. For more information on the YAML configuration file, see the [Azure AI Search connection YAML schema](../../../../machine-learning/reference-yaml-connection-ai-search.md):
- API Key example:

    ```yml
    name: myazaics_apk
    type: azure_ai_search
    endpoint: https://contoso.search.windows.net/
    api_key: XXXXXXXXXXXXXXX
    ```

- Credential-less

    ```yml    
    name: myazaics_ei
    type: azure_ai_search
    endpoint: https://contoso.search.windows.net/
    ```

# [Python](#tab/python)
```python
from azure.ai.ml.entities import AzureAISearchConnection

# constrict an Azure AI Search connection
my_connection_name = "myaiservivce"
my_endpoint = "demo.endpoint" # this could also be called target
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
 :::image type="content" source="../../media/tools/ai-search/select-acs.png" alt-text="A screenshot of the Azure AI Search connection type the user should select." lightbox="../../media/tools/ai-search/select-acs.png":::

4. Provide the required connection details for the Azure AI Search resource you want to use. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, click **Add connection**.
:::image type="content" source="../../media/tools/ai-search/acs-connection-2.png" alt-text="A screenshot the required fields to add a new Azure AI Search connection." lightbox="../../media/tools/ai-search/acs-connection-2.png":::

5. Verify that the connection was successfully created and now appears in the project's Connections tab.
:::image type="content" source="../../media/tools/ai-search/success-acs-connection.png" alt-text="A screenshot of the project connections page with a new Azure AI Search connection added." lightbox="../../media/tools/ai-search/success-acs-connection.png":::
---

