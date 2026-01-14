---
title: How to create a hub using the Azure Machine Learning SDK/CLI
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to create a Microsoft Foundry hub using the Azure Machine Learning SDK and Azure CLI extension.
ms.service: azure-ai-foundry
ms.custom: build-2024, devx-track-azurecli, dev-focus
ms.topic: how-to
ms.date: 12/23/2025
ai-usage: ai-assisted
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
---

# Create a hub by using the Azure Machine Learning SDK and CLI

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, you learn how to create the following [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) resources by using the Azure Machine Learning SDK and Azure CLI (with machine learning extension):
- A Foundry hub
- A Foundry connection

> [!NOTE]
> A hub is used only for a **[!INCLUDE [hub](../../includes/hub-project-name.md)]**. A **[!INCLUDE [fdp](../../includes/fdp-project-name.md)]** doesn't use a hub. For more information, see [Types of projects](../../what-is-foundry.md#types-of-projects).

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- **RBAC roles**: You must have the **Contributor** or **Owner** role on your Azure subscription or resource group to create a hub. If you're creating a connection to existing resources, ensure you have **Contributor** access to those resources as well.
- **For Python SDK**: [Azure Machine Learning Python SDK (v2.0 or later)](https://pypi.org/project/azure-ai-ml/), [Azure Identity Python SDK](https://pypi.org/project/azure-identity/), and Python 3.8 or later.
- **For Azure CLI**: [Azure CLI](/cli/azure/install-azure-cli) and [Azure Machine Learning extension](/azure/machine-learning/how-to-configure-cli).
- If connecting to existing resources: Azure Storage account or Azure Key Vault must already exist in the same subscription (same resource group, or in another resource group that you have access to).

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

1. Verify your authentication by listing existing hubs:

    ```azurecli
    az ml workspace list --resource-group <your-resource-group-name>
    ```

    If the command succeeds and displays any existing hubs, your authentication is configured correctly.

---

## Create the Foundry hub and Microsoft Foundry connection

Use the following examples to create a new hub. Replace example string values with your own values:

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Hub

my_hub_name = "myexamplehub"
my_location = "East US"
my_display_name = "My Example Hub"

# Construct a basic hub
my_hub = Hub(
    name=my_hub_name,
    location=my_location,
    display_name=my_display_name
)

# Create the hub and wait for completion
created_hub = ml_client.workspaces.begin_create(my_hub).result()
print(f"Created hub: {created_hub.name}")
```

This code creates a new hub with the specified name, location, and display name. Azure automatically provisions associated Azure Storage and Azure Key Vault resources.

**References**: [`Hub`](/python/api/azure-ai-ml/azure.ai.ml.entities.hub), [MLClient.workspaces.begin_create](/azure/machine-learning/reference-azure-machine-learning-cli)

# [Azure CLI](#tab/azurecli)

```azurecli
az ml workspace create --kind hub --resource-group <your-resource-group> --name <your-hub-name>
```

Replace `<your-resource-group>` with your Azure resource group name and `<your-hub-name>` with a unique name for your hub. Azure automatically creates associated storage and key vault resources.

**References**: [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)

---

## Create a Foundry connection

After creating your own [Foundry resource](../../../ai-services/multi-service-resource.md?context=%2Fazure%2Fai-foundry%2Fcontext%2Fcontext) or [Azure OpenAI resource](../../openai/how-to/create-resource.md) in the same resource group, you can connect it to your hub. You can also connect [Azure AI Search](../../../search/search-create-service-portal.md) from any resource group in your same subscription.

# [Python SDK](#tab/python)

1. Include your hub in your `ml_client` connection:

    * Enter your subscription details. For `<AML_WORKSPACE_NAME>`, enter your hub name:
    
        [!notebook-python[](~/azureml-examples-main/sdk/python/resources/connections/connections.ipynb?name=details)]

    * Get a handle to the hub:

        [!notebook-python[](~/azureml-examples-main/sdk/python/resources/connections/connections.ipynb?name=ml_client)]

1. Use `ml_client` to create the connection to your Foundry Tools. You can find endpoints in [Azure portal](https://portal.azure.com) under **Resource management > Keys and endpoints**. For a Foundry resource, use the **AI Services** endpoint. For Azure AI Search, use the URL for the endpoint.

    ```python
    from azure.ai.ml.entities import AzureAIServicesConnection

    # Construct a connection to Azure AI Services
    my_connection_name = "my-ai-services-connection"  # Any name you want
    aiservices_resource_name = "<your-resource-name>"  # From Azure portal
    my_endpoint = "<your-endpoint>"  # From Azure portal
    my_api_keys = None  # Leave blank to use Azure Entra ID (AAD) authentication
    my_ai_services_resource_id = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{aiservices_resource_name}"

    my_connection = AzureAIServicesConnection(
        name=my_connection_name,
        endpoint=my_endpoint,
        api_key=my_api_keys,
        ai_services_resource_id=my_ai_services_resource_id
    )

    # Create the connection
    ml_client.connections.create_or_update(my_connection)
    print(f"Created connection: {my_connection.name}")
    ```

    **References**: [`AzureAIServicesConnection`](/python/api/azure-ai-ml/azure.ai.ml.entities.azureaiservicesconnection), [MLClient.connections](/azure/machine-learning/reference-azure-machine-learning-cli)

# [Azure CLI](#tab/azurecli)

```azurecli
az ml connection create --file connection.yml --resource-group <your-resource-group> --workspace-name <your-hub-name>
```

You can use either an API key or Azure Entra ID (AAD) authentication. Create a YAML configuration file named `connection.yml`:

**API key example**:

```yaml
name: my-ai-services-connection
type: azure_ai_services
endpoint: <your-endpoint>
api_key: <your-api-key>
ai_services_resource_id: /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<resource-name>
```

**AAD (credential-less) example**:

```yaml
name: my-ai-services-connection
type: azure_ai_services
endpoint: <your-endpoint>
ai_services_resource_id: /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<resource-name>
```

For detailed schema information, see the [Azure AI Services connection YAML schema](/azure/machine-learning/reference-yaml-connection-ai-services).

**References**: [az ml connection create](/cli/azure/ml/connection#az-ml-connection-create)

---

## Create a hub with existing dependency resources

By default, a hub automatically creates associated Azure Storage and Azure Key Vault resources. If you want to reuse existing Azure Storage or Azure Key Vault resources, you can specify them during hub creation. In the following examples, replace the placeholder values with your own resource IDs:

> [!TIP]
> You can retrieve the resource ID of the storage account and key vault from the Azure portal by going to the resource's overview and selecting __JSON view__. The resource ID is located in the __id__ field. You can also use the Azure CLI to retrieve the resource ID. For example, use `az storage account show --name {my_storage_account_name} --query "id"` and `az keyvault show --name {my_key_vault_name} --query "id"`.

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Hub

my_hub_name = "myexamplehub"
my_location = "East US"
my_display_name = "My Example Hub"
my_resource_group = "myresourcegroupname"
my_storage_account_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
my_key_vault_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.KeyVault/vaults/<key-vault-name>"

# Construct a hub with existing dependency resources
my_hub = Hub(
    name=my_hub_name,
    location=my_location,
    display_name=my_display_name,
    resource_group=my_resource_group,
    storage_account_id=my_storage_account_id,
    key_vault_id=my_key_vault_id
)

# Create the hub
created_hub = ml_client.workspaces.begin_create(my_hub).result()
print(f"Created hub with existing resources: {created_hub.name}")
```

To find resource IDs for existing resources, visit the [Azure portal](https://portal.azure.com), navigate to the resource's **Overview** page, and select **JSON view**. The resource ID appears in the **id** field. Alternatively, use Azure CLI:

```azurecli
# Get Storage account resource ID
az storage account show --name <storage-account-name> --resource-group <resource-group> --query "id"

# Get Key Vault resource ID
az keyvault show --name <key-vault-name> --resource-group <resource-group> --query "id"
```

**References**: [`Hub`](/python/api/azure-ai-ml/azure.ai.ml.entities.hub)

# [Azure CLI](#tab/azurecli)

```azurecli
az ml workspace create --kind hub --resource-group <your-resource-group> --name <your-hub-name> --location <location> --storage-account <storage-account-resource-id> --key-vault <key-vault-resource-id>
```

Replace the angle-bracket placeholders with your own values. To find resource IDs, use:

```azurecli
# Get Storage account resource ID
az storage account show --name <storage-account-name> --resource-group <resource-group> --query "id"

# Get Key Vault resource ID
az keyvault show --name <key-vault-name> --resource-group <resource-group> --query "id"
```

**References**: [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create)

---

## Update Azure Application Insights and Azure Container Registry

To use custom environments for Prompt Flow, you need to configure an Azure Container Registry for your hub. To use Azure Application Insights for Prompt Flow deployments, you need to configure an Azure Application Insights resource for your hub. Updating the workspace-attached Azure Container Registry or Application Insights resources might break lineage of previous jobs, deployed inference endpoints, or your ability to rerun earlier jobs in the workspace. After association with a Foundry hub, Azure Container Registry and Application Insights resources can't be disassociated (set to null).

You can use the Azure portal, Azure SDK/CLI options, or the infrastructure-as-code templates to update both Azure Application Insights and Azure Container Registry for the hub.

# [Python SDK](#tab/python)

```python
from azure.ai.ml.entities import Hub

my_app_insights = "{APPLICATION_INSIGHTS_ARM_ID}"
my_container_registry = "{CONTAINER_REGISTRY_ARM_ID}"

# construct a hub with Application Insights and Container Registry
my_hub = Hub(name="myexamplehub", 
             location="East US", 
             application_insights=my_app_insights,
             container_registry=my_container_registry)

# update_dependent_resources is used to give consent to update the workspace dependent resources.
updated_hub = ml_client.workspaces.begin_update(workspace=my_hub, update_dependent_resources=True).result()
print(f"Hub updated: {updated_hub.name}")
```

This script updates an existing hub with the specified Application Insights and Container Registry resources. The `update_dependent_resources=True` parameter confirms the update.

Reference: [Hub](/python/api/azure-ai-ml/azure.ai.ml.entities.hub), [MLClient.workspaces.begin_update()](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-mlclient)

# [Azure CLI](#tab/azurecli)

```azurecli
az ml workspace update -n "myexamplehub" -g "{MY_RESOURCE_GROUP}" -a "APPLICATION_INSIGHTS_ARM_ID" -u
```

This command updates the hub named "myexamplehub" with the specified Application Insights resource. The `-u` flag grants consent to update dependent resources.

Reference: [az ml workspace update](/cli/azure/ml/workspace#az-ml-workspace-update)

---

## Related content

- [Get started building a chat app using the prompt flow SDK](../../quickstarts/get-started-code.md)
- [Work with the Foundry for Visual Studio Code extension (Preview)](get-started-projects-vs-code.md)
- [Configure a managed network](../configure-managed-network.md?tabs=python)
