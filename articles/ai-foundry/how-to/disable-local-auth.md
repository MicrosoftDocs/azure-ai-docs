---
title: "Disable shared key access to the hub storage account"
titleSuffix: Azure AI Foundry
description: "Disable shared key access to the default storage account used by your Azure AI Foundry hub and projects."
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 05/09/2025
ms.reviewer: meerakurup
#customer intent: As an admin, I want to disable shared key access to my resources to improve security.
---

# Disable shared key access for your hub's storage account (preview)

> [!NOTE]
> The information provided in this article is specific to a **[!INCLUDE [hub](../includes/hub-project-name.md)]**, and doesn't apply for a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

An [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) hub defaults to use of a shared key to access its default Azure Storage account. With key-based authorization, anyone who has the key and access to the storage account can access data.

To reduce the risk of unauthorized access, you can disable key-based authorization, and instead use Microsoft Entra ID for authorization. This configuration uses a Microsoft Entra ID value to authorize access to the storage account. The identity used to access storage is either the user's identity or a managed identity. The user's identity is used to view data in the Azure Machine Learning studio, or to run a notebook while authenticated with the user's identity. The Azure Machine Learning service uses a managed identity to access the storage account - for example, when running a training job as the managed identity.

Use of your hub with a shared key disabled storage account is currently in preview.

[!INCLUDE [machine-learning-preview-generic-disclaimer](../../machine-learning/includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

- An existing Azure Storage account with shared key authorization disabled. For more information about the process and implications of disabling shared key authorization for your storage account, visit the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) resource.

# [Azure portal](#tab/portal)

Not applicable.

# [Python SDK](#tab/python)

1. [Install the SDK v2](https://aka.ms/sdk-v2-install).

    > [!IMPORTANT]
    > The steps in this article require the **azure-ai-ml Python package, version 1.17.0**. To determine the installed package version, use the `pip list` command from your Python development environment.

1. Install azure-identity: `pip install azure-identity`. If you're working in a notebook cell, use `%pip install azure-identity`.

1. Provide your subscription details:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=subscription_id)]

1. Get a handle to the subscription. All the Python code in this article uses `ml_client`:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=ml_client)]
      
    - (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you wish to use into the `DefaultAzureCredential`. Find your tenant ID from the [Azure portal](https://portal.azure.com), under __Microsoft Entra ID, External Identities__.
                
    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
                
    - (Optional) If you're working in the [Azure Government - US](https://azure.microsoft.com/explore/global-infrastructure/government/) or [Azure China 21Vianet](/azure/china/overview-operations) regions, you must specify the cloud into which you want to authenticate. You can specify these regions in `DefaultAzureCredential`.
                
    ```python
    from azure.identity import AzureAuthorityHosts
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT))
    ```

# [Azure CLI](#tab/cli)

To use the CLI commands in this document, you need the [Azure CLI](/cli/azure/install-azure-cli) and the [ml extension](../../machine-learning/how-to-configure-cli.md).

If you use the [Azure Cloud Shell](https://azure.microsoft.com//features/cloud-shell/), the CLI is accessed through the browser, and it lives in the cloud.

> [!IMPORTANT]
> The steps in this article require the Azure CLI extension for machine learning, version **2.27.0 or greater**. To determine the version of the extension you have installed, use the `az version` command from the Azure CLI. In the extensions collection that's returned, find the `ml` extension. This code sample shows an example return value:
>
> ```json
> {
>     "azure-cli": "2.61.0",
>     "azure-cli-core": "2.61.0",
>     "azure-cli-telemetry": "1.1.0",
>     "extensions": {
>         "ml": "2.27.0"
>     }
> }
> ```

# [ARM Template](#tab/armtemplate)

- An existing Azure Key Vault instance.
- The Azure Resource Manager ID for both the Azure Storage Account and Azure Key Vault to be used with the hub.

---

## Create a new hub

When you create a new hub, the creation process can automatically disable shared key access. You can also create an Azure Storage account, disable shared key access, and use it during hub creation.

# [Azure portal](#tab/portal)

1. From the Azure portal, search for `Azure AI Foundry`. From the left menu, select **AI Hubs**, and then select **+ Create** and **Hub**.

    :::image type="content" source="../media/how-to/hubs/create-hub.png" alt-text="Screenshot of the Azure AI Foundry portal." lightbox="../media/how-to/hubs/create-hub.png":::

1. From the __Basics__ tab, enter the hub details and then select the __Storage__ tab. Select the Azure Storage account that you previously created.

    :::image type="content" source="../media/disable-local-auth/ai-hub-storage.png" alt-text="Screenshot of hub creation using the previously created storage account." lightbox="../media/disable-local-auth/ai-hub-storage.png":::

1. From the __Identity__ tab, set the __Storage account access type__ to __identity-based__ and then enable the __Disable shared key access__ option.

    :::image type="content" source="../media/disable-local-auth/ai-hub-identity-based-access.png" alt-text="Screenshot of hub creation using identity-based storage access." lightbox="../media/disable-local-auth/ai-hub-identity-based-access.png":::

1. Continue the hub creation process. As the hub is created, the managed identity is automatically assigned the permissions it needs to access the storage account.

# [Python SDK](#tab/python)

When you create your hub with the SDK, set `system_datastores_auth_mode="identity"`. To use a preexisting storage account, use the `storage_account` parameter to specify the Azure Resource Manager ID of an existing storage account:

```python
# Creating a unique hub name with current datetime to avoid conflicts
from azure.ai.ml.entities import Hub
import datetime

hub_name = "mlw-hub-prod-" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M"
)

ws_hub = Hub(
    name=hub_name,
    location="eastus",
    display_name="Hub-example",
    description="This example shows how to create a Hub",
    hbi_workspace=False,
    tags=dict(purpose="demo"),
    storage_account= {existing_storage_account with AllowSharedKeyAccess=false},
    system_datastores_auth_mode="identity",
)

created_hub = ml_client.workspaces.begin_create(ws_hub).result()
print(created_hub)
```

# [Azure CLI](#tab/cli)

To create a new hub with Microsoft Entra ID authorization for the storage account, use a YAML configuration file that sets `system_datastores_auth_mode` to `identity`. You can also specify the Azure Resource ID value of an existing storage account with the `storage_account` entry.

This example YAML file shows how to set the hub to use a managed identity and an existing storage account:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/workspace.schema.json
name: mlw-basicex-prod
location: eastus
display_name: Bring your own dependent resources-example
description: This configuration specifies a workspace configuration with existing dependent resources
storage_account: {your storage account resource id}
system_datastores_auth_mode: identity
tags:
  purpose: demonstration
```

This YAML file can be used with the `az ml workspace create` command, with the `--file` parameter:

```azurecli-interactive
az ml workspace create -g <resource-group-name> --kind hub --file workspace.yml
```

# [ARM Template](#tab/armtemplate)

In the following JSON template example, substitute your own values for the following placeholders:

- **[workspace name]**
- **[workspace friendly name]**
- **[Storage Account ARM resource ID]**
- **[Key Vault ARM resource ID]**

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources":
    [
        {
            "type": "Microsoft.MachineLearningServices/workspaces",
            "apiVersion": "2024-04-01",
            "name": "[workspace name]",
            "location": "[resourceGroup().location]",
            "sku":
            {
                "name": "Basic",
                "tier": "Basic"
            },
            "kind": "Hub",
            "identity":
            {
                "type": "SystemAssigned"
            },
            "properties":
            {
                "friendlyName": "[workspace friendly name]",
                "storageAccount": "[Storage Account ARM resource ID]",
                "keyVault": "[Key Vault ARM resource ID]",
                "systemDatastoresAuthMode": "identity",
                "managedNetwork":
                {
                    "isolationMode": "Disabled"
                },
                "publicNetworkAccess": "Enabled"
            }
        }
    ]
}
```

For information on deploying an ARM template, use one of the following articles:
- [Tutorial: Deploy a local ARM template using Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template)
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal)

After you create the hub, identify all the users that will use it - for example, Data Scientists. These users must be assigned the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, visit the [role assignments](#scenarios-for-hub-storage-account-role-assignments) section.

---

## Update an existing hub

If you have an existing Azure AI Foundry hub, use the steps in this section to update the hub to use Microsoft Entra ID, to authorize access to the storage account. Then, disable shared key access on the storage account.

# [Azure portal](#tab/portal)

1. Go to the Azure portal and select the __Azure AI Foundry hub__.
1. From the left menu, select **Properties**. From the bottom of the page, set __Storage account access type__ to __Identity-based__. Select __Save__ from the top of the page to save the configuration.

    :::image type="content" source="../media/disable-local-auth/update-existing-hub-identity-based-access.png" alt-text="Screenshot showing selection of Identity-based access." lightbox="../media/disable-local-auth/update-existing-hub-identity-based-access.png":::



# [Python SDK](#tab/python)

To update an existing hub, set the `system_datastores_auth_mode = "identity"` for the hub. This code sample shows an update of a hub named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "identity"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To update an existing hub, use the `az ml workspace update` command, and specify `--system-datastores-auth-mode identity`. This example shows an update of a hub named `myhub`:

```azurecli-interactive
az ml workspace update --name myhub --system-datastores-auth-mode identity
```

# [ARM Template](#tab/armtemplate)

In the following JSON template example, substitute your own values for the following placeholders:

- **[workspace name]**
- **[workspace friendly name]**
- **[Storage Account ARM resource ID]**
- **[Key Vault ARM resource ID]**

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources":
    [
        {
            "type": "Microsoft.MachineLearningServices/workspaces",
            "apiVersion": "2024-04-01",
            "name": "[workspace name]",
            "location": "[resourceGroup().location]",
            "sku":
            {
                "name": "Basic",
                "tier": "Basic"
            },
            "kind": "Hub",
            "identity":
            {
                "type": "SystemAssigned"
            },
            "properties":
            {
                "friendlyName": "[workspace friendly name]",
                "storageAccount": "[Storage Account ARM resource ID]",
                "keyVault": "[Key Vault ARM resource ID]",
                "systemDatastoresAuthMode": "identity",
                "managedNetwork":
                {
                    "isolationMode": "Disabled"
                },
                "publicNetworkAccess": "Enabled"
            }
        }
    ]
}
```

For information on deploying an ARM template, use one of the following articles:
- [Tutorial: Deploy a local ARM template using Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template)
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal)

---

### Assign roles to users

After you update the hub, update the storage account to disable shared key access. For more information about disabling shared key access, visit the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) article resource.

You must also identify all the users that need access to the default datastores - for example, Data Scientists. These users must be assigned the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, visit the [role assignments](#scenarios-for-hub-storage-account-role-assignments) resource in this document.

## Revert to use shared keys

To revert a hub back to use of shared keys to access the storage account, use this information:

# [Azure portal](#tab/portal)

To update an existing workspace, go to **Properties** and select **Credential-based access**.

:::image type="content" source="../media/disable-local-auth/update-existing-hub-credential-based-access.png" alt-text="Screenshot showing selection of Credential-based access." lightbox="../media/disable-local-auth/update-existing-hub-credential-based-access.png":::

Select **Save** to save this choice.

# [Python SDK](#tab/python)

To configure the hub to use a shared key again, set the `system_datastores_auth_mode = "accesskey"` for the hub. This code demonstrates an update of a hub named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "accesskey"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To configure the hub to once again use a shared key, use the `az ml workspace update` command, and specify `--system-datastores-auth-mode accesskey`. This example demonstrates an update of a hub named `myhub`:

```azurecli-interactive
az ml workspace update --name myhub --system-datastores-auth-mode accesskey
```

# [ARM Template](#tab/armtemplate)

If you have an existing Azure AI Foundry hub, use the steps in this section to update the hub to use Microsoft Entra ID, to authorize access to the storage account. Then, disable shared key access on the storage account.

In the following JSON template example, substitute your own values for the following placeholders:

- **[workspace name]**
- **[workspace friendly name]**
- **[Storage Account ARM resource ID]**
- **[Key Vault ARM resource ID]**

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources":
    [
        {
            "type": "Microsoft.MachineLearningServices/workspaces",
            "apiVersion": "2024-04-01",
            "name": "[workspace name]",
            "location": "[resourceGroup().location]",
            "sku":
            {
                "name": "Basic",
                "tier": "Basic"
            },
            "kind": "Hub",
            "identity":
            {
                "type": "SystemAssigned"
            },
            "properties":
            {
                "friendlyName": "[workspace friendly name]",
                "storageAccount": "[Storage Account ARM resource ID]",
                "keyVault": "[Key Vault ARM resource ID]",
                "systemDatastoresAuthMode": "accesskey",
                "managedNetwork":
                {
                    "isolationMode": "Disabled"
                },
                "publicNetworkAccess": "Enabled"
            }
        }
    ]
}
```

For information on deploying an ARM template, use one of the following articles:
- [Tutorial: Deploy a local ARM template using Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template)
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal)

After you create the hub, identify all the users that will use it - for example, Data Scientists. These users must be assigned the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, visit the [role assignments](#scenarios-for-hub-storage-account-role-assignments) resource in this document.

---

After you revert the hub, update the storage account to enable shared key access. For more information, visit the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) article.

## Scenarios for hub storage account role assignments

To work with a storage account with disabled shared key access, you might need to grant more roles to either your users or the managed identity for your hub. Hubs have a system-assigned managed identity by default. However, some scenarios require a user-assigned managed identity. This table summarizes the scenarios that require extra role assignments:

| Scenario | Microsoft Entra ID | Required roles | Notes |
| ----- | ----- | ----- | ----- |
| AI Speech | Storage Blob Data Contributor </br>Storage File Data Privileged Contributor | |
| Model-as-a-Service | system-assigned managed identity | Storage Blob Data Contributor | The hub's managed identity. </br>Automatically assigned the role when provisioned. </br>Don't manually change this role assignment. |
| Azure Search | system-assigned managed identity | Storage Blob Data Contributor | The hub's managed identity. </br>Automatically assigned the role when provisioned. </br>Don't manually change this role assignment. |
| Fine tuning of OSS models | User-assigned managed identity | Storage Blob Data Contributor | |
| PromptFlow | User's identity | Storage Blob Data Contributor </br>Storage File Data Privileged Contributor | |
| Add and manage your own data | User's identity | Storage Blob Data Contributor | |

## Related content

- [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent)
- [Create an Azure AI Foundry hub](develop/create-hub-project-sdk.md)