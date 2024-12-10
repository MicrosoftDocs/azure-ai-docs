##### Create an Azure AI Search project connection

# [Azure CLI](#tab/azurecli)
```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_hub_name}
```

You can use either an API key or credential-less YAML configuration file. For more information on the YAML configuration file, see the [Azure AI Search connection YAML schema](../../../machine-learning/reference-yaml-connection-ai-search.md):
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
    :::image type="content" source="../media/tools/ai-search/project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../media/tools/ai-search/project-studio.png":::

2. Click on the **Connections** tab and select **Add Connection**.
 :::image type="content" source="../media/tools/ai-search/project-connections-page.png" alt-text="A screenshot of the project connections page." lightbox="../media/tools/ai-search/project-connections-page.png":::

3. Select **Azure AI Search**.
 :::image type="content" source="../media/tools/ai-search/select-acs.png" alt-text="A screenshot of the Azure AI Search connection type the user should select." lightbox="../media/tools/ai-search/select-acs.png":::

4. Provide the required connection details for the Azure AI Search resource you want to use. Both Managed Identity and Key-based authentication are supported. Once all the fields are filled in, click **Add connection**.
:::image type="content" source="../media/tools/ai-search/acs-connection-2.png" alt-text="A screenshot the required fields to add a new Azure AI Search connection." lightbox="../media/tools/ai-search/acs-connection-2.png":::

5. Verify that the connection was successfully created and now appears in the project's Connections tab.
:::image type="content" source="../media/tools/ai-search/success-acs-connection.png" alt-text="A screenshot of the project connections page with a new Azure AI Search connection added." lightbox="../media/tools/ai-search/success-acs-connection.png":::

---
