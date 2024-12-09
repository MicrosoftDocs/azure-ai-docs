---
title: How to create a hub using the Azure Machine Learning SDK/CLI
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to create an AI Foundry hub using the Azure Machine Learning SDK and Azure CLI extension.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom: build-2024, devx-track-azurecli
ms.topic: how-to
ms.date: 11/21/2024
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
---

# Create a hub using the Azure Machine Learning SDK and CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to create the following AI Foundry resources using the Azure Machine Learning SDK and Azure CLI (with machine learning extension):
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

## Create the AI Foundry hub and AI Services connection

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

After creating your own AI Services, you can connect it to your hub:

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import AzureAIServicesConnection

# constrict an AI Services connection
my_connection_name = "myaiservivce"
my_endpoint = "demo.endpoint" # this could also be called target
my_api_keys = None # leave blank for Authentication type = AAD
my_ai_services_resource_id = "" # ARM id required

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
    endpoint: https://contoso.cognitiveservices.azure.com/
    api_key: XXXXXXXXXXXXXXX
    ```

- Credential-less

    ```yml    
    name: myazai_apk
    type: azure_ai_services
    endpoint: https://contoso.cognitiveservices.azure.com/
    ```

---

## Create an AI Foundry hub using existing dependency resources

You can also create a hub using existing resources such as Azure Storage and Azure Key Vault. In the following examples, replace the example string values with your own values:

> [!TIP]
> You can retrieve the resource ID of the storage account and key vault from the Azure Portal by going to the resource's overview and selecting __JSON view__. The resource ID is located in the __id__ field. You can also use the Azure CLI to retrieve the resource ID. For example, `az storage account show --name {my_storage_account_name} --query "id"` and `az keyvault show --name {my_key_vault_name} --query "id"`.

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
