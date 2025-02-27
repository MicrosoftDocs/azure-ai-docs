---
title: How to create a hub using the Azure Machine Learning SDK/CLI
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to create an Azure AI Foundry hub using the Azure Machine Learning SDK and Azure CLI extension.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2024, devx-track-azurecli
ms.topic: how-to
ms.date: 02/13/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
---

# Create a hub using the Azure Machine Learning SDK and CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to create the following [Azure AI Foundry](https://ai.azure.com) resources using the Azure Machine Learning SDK and Azure CLI (with machine learning extension):
- An Azure AI Foundry hub
- An Azure AI Services connection

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure AI Foundry](https://azure.microsoft.com/free/) today.

## Set up your environment

Use the following tabs to select whether you're using the Python SDK or Azure CLI:

# [Python SDK](#tab/python)

[!INCLUDE [SDK setup](../../includes/development-environment-config.md)]

# [Azure CLI](#tab/azurecli)

1. If you don't have the Azure CLI and machine learning extension installed, follow the steps in the [Install and set up the machine learning extension](/azure/machine-learning/how-to-configure-cli) article.

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

    ```azurecli
    az login
    ```

    For more information on authenticating, see [Authentication methods](/cli/azure/authenticate-azure-cli).

---

## Create the Azure AI Foundry hub and AI Services connection

Use the following examples to create a new hub. Replace example string values with your own values:

# [Python SDK](#tab/python)

```Python
from azure.ai.ml.entities import Hub

my_hub_name = "myexamplehub"
my_location = "East US"
my_display_name = "My Example Hub"

# construct a basic hub
my_hub = Hub(name=my_hub_name, 
            location=my_location,
            display_name=my_display_name)

created_hub = ml_client.workspaces.begin_create(my_hub).result()

```

# [Azure CLI](#tab/azurecli)

```azurecli
az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name}
```

---

## Create an AI Services connection

After creating your own AI Services, you can connect it to your hub.

# [Python SDK](#tab/python)

1. Your `ml_client` connection now needs to include your hub:

    * Provide your subscription details.  For `<AML_WORKSPACE_NAME>`, use your hub name:
    
        [!notebook-python[](~/azureml-examples-main/sdk/python/resources/connections/connections.ipynb?name=details)]

    * Get a handle to the hub:

        [!notebook-python[](~/azureml-examples-main/sdk/python/resources/connections/connections.ipynb?name=ml_client)]

2. Use `ml_client` to create the connection to your AI Services:

    ```python
    from azure.ai.ml.entities import AzureAIServicesConnection

    # construct an AI Services connection
    my_connection_name = "myaiservivce" # any name you want
    aiservices_resource_name = <resource_name> # copy from Azure AI Foundry portal
    my_endpoint = "<endpoint>" # copy from Azure AI Foundry portal
    my_api_keys = None # leave blank for Authentication type = AAD
    my_ai_services_resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{aiservices_resource_name}"

    my_connection = AzureAIServicesConnection(name=my_connection_name,
                                        endpoint=my_endpoint, 
                                        api_key= my_api_keys,
                                        ai_services_resource_id=my_ai_services_resource_id)

    # Create the connection
    ml_client.connections.create_or_update(my_connection)
    ```

# [Azure CLI](#tab/azurecli)

```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_hub_name}
```

You can use either an API key or credential-less YAML configuration file. For more information on the YAML configuration file, see the [AI Services connection YAML schema](/azure/machine-learning/reference-yaml-connection-ai-services):

- API Key example:

    ```yml
    name: myazai_ei
    type: azure_ai_services
    endpoint: <endpoint for your AI Services>
    api_key: XXXXXXXXXXXXXXX
    ai_services_resource_id: <fully_qualified_resource_id>
    ```

- Credential-less

    ```yml    
    name: myazai_apk
    type: azure_ai_services
    endpoint: <endpoint for your AI Services>
    ai_services_resource_id: <fully_qualified_resource_id>
    ```

The <fully_qualified_resource_id> is the resource ID of your AI Services resource. It is in the format `/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{aiservices_resource_name}`.

---

## Create an Azure AI Foundry hub using existing dependency resources

You can also create a hub using existing resources such as Azure Storage and Azure Key Vault. In the following examples, replace the example string values with your own values:

> [!TIP]
> You can retrieve the resource ID of the storage account and key vault from the Azure portal by going to the resource's overview and selecting __JSON view__. The resource ID is located in the __id__ field. You can also use the Azure CLI to retrieve the resource ID. For example, `az storage account show --name {my_storage_account_name} --query "id"` and `az keyvault show --name {my_key_vault_name} --query "id"`.

# [Python SDK](#tab/python)

```Python
from azure.ai.ml.entities import Hub

my_hub_name = "myexamplehub"
my_location = "East US"
my_display_name = "My Example Hub"
my_resource_group = "myresourcegroupname"
my_storage_account_id = "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/myresourcegroupname/providers/Microsoft.Storage/storageAccounts/mystorageaccountname"
my_key_vault_id = "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/myresourcegroupname/providers/Microsoft.KeyVault/vaults/mykeyvaultname"

# construct a basic hub
my_hub = Hub(name=my_hub_name, 
            location=my_location,
            display_name=my_display_name,
            resource_group=my_resource_group,
            storage_account_id=my_storage_account_id,
            key_vault_id=my_key_vault_id)

created_hub = ml_client.workspaces.begin_create(my_hub).result()
```

# [Azure CLI](#tab/azurecli)

```azurecli
az ml workspace create --kind hub --resource-group {my_resource_group} --name {my_hub_name} --location {hub-region} --storage-account {my_storage_account_id} --key-vault {my_key_vault_id}
```


## Related content

- [Get started building a chat app using the prompt flow SDK](../../quickstarts/get-started-code.md)
- [Work with projects in Visual Studio Code](vscode.md)
- [Configure a managed network](../configure-managed-network.md?tabs=python)
