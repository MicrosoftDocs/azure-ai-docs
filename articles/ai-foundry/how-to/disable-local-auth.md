---
title: Disable Shared Key Access to the Hub Storage Account
titleSuffix: Azure AI Foundry
description: Disable shared-key access to the default storage account used by your Azure AI Foundry hub and projects.
ms.author: jburchel 
author: jonburchel 
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 10/01/2025
ms.reviewer: meerakurup
ai-usage: ai-assisted
#customer intent: As an admin, I want to disable shared-key access to my resources to improve security.
---

# Disable shared-key access for your hub's storage account (preview)

> [!NOTE]
> The information provided in this article is specific to a [!INCLUDE [hub](../includes/hub-project-name.md)] and doesn't apply to an [!INCLUDE [fdp](../includes/fdp-project-name.md)]. For more information, see [Types of projects](../what-is-azure-ai-foundry.md#project-types).

An [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) hub defaults to using a shared key to access its default Azure Storage account. With key-based authorization, anyone who has the key and access to the storage account can access data.

To reduce the risk of unauthorized access, disable key-based authorization and instead use Microsoft Entra ID for authorization. This configuration uses a Microsoft Entra ID value to authorize access to the storage account. The identity used to access storage is either the user's identity or a managed identity. The user's identity is used to view data in Azure Machine Learning studio or to run a notebook while authenticated with the user's identity. Machine Learning uses a managed identity to access the storage account - for example, when the managed identity runs a training job.

Use of your hub with a shared-key disabled storage account is currently in preview.

[!INCLUDE [machine-learning-preview-generic-disclaimer](../../machine-learning/includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

You need an existing storage account with shared-key authorization disabled. For more information about the process and implications of disabling shared-key authorization for your storage account, see [Prevent shared-key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent).

# [Azure portal](#tab/portal)

Not applicable.

# [Python SDK](#tab/python)

1. [Install the SDK v2](https://aka.ms/sdk-v2-install).

    > [!IMPORTANT]
    > The steps in this article require the `azure-ai-ml` Python package, version 1.17.0. To determine the installed package version, use the `pip list` command from your Python development environment.

1. Install `azure-identity`: `pip install azure-identity`. If you're working in a notebook cell, use `%pip install azure-identity`.

1. Provide your subscription details:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=subscription_id)]

1. Get a handle to the subscription. All the Python code in this article uses `ml_client`.

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=ml_client)]
      
    - (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID that you want to use into `DefaultAzureCredential`. Find your tenant ID in the [Azure portal](https://portal.azure.com) under **Microsoft Entra ID** > **External Identities**.
                
      ```python
      DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
      ```
                
    - (Optional) If you're working in the [Azure Government - US](https://azure.microsoft.com/explore/global-infrastructure/government/) or [Azure operated by 21Vianet](/azure/china/overview-operations) regions, you must specify the cloud into which you want to authenticate. You can specify these regions in `DefaultAzureCredential`.
                
      ```python
      from azure.identity import AzureAuthorityHosts
      DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT))
      ```

# [Azure CLI](#tab/cli)

To use the CLI commands in this document, you need the [Azure CLI](/cli/azure/install-azure-cli) and the [Azure Machine Learning extension](../../machine-learning/how-to-configure-cli.md).

If you use [Azure Cloud Shell](https://azure.microsoft.com//features/cloud-shell/), the CLI is accessed through the browser and it lives in the cloud.

> [!IMPORTANT]
> The steps in this article require the Azure CLI Extension for Machine Learning, version 2.27.0 or later. To determine the version of the extension that you installed, use the `az version` command from the Azure CLI. In the extensions collection that returns, find the `ml` extension. This code sample shows an example return value:
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

# [ARM template](#tab/armtemplate)

- An existing Azure Key Vault instance.
- The Azure Resource Manager ID for both the storage account and the key vault to be used with the hub.

---

## Create a new hub

When you create a new hub, the creation process can automatically disable shared-key access. You can also create a storage account, disable shared-key access, and use it during hub creation.

This section shows you how to create a hub with identity-based access to the storage account.

# [Azure portal](#tab/portal)

1. In the Azure portal, search for `Azure AI Foundry`. On the left menu, select **AI Hubs**, and select **+ Create** > **Hub**.

    :::image type="content" source="../media/how-to/hubs/create-hub.png" alt-text="Screenshot that shows the Azure AI Foundry portal." lightbox="../media/how-to/hubs/create-hub.png":::

1. On the **Basics** tab, enter the hub details, and select the **Storage** tab. Select the storage account that you previously created.

    :::image type="content" source="../media/disable-local-auth/ai-hub-storage.png" alt-text="Screenshot that shows hub creation by using the previously created storage account." lightbox="../media/disable-local-auth/ai-hub-storage.png":::

1. On the **Identity** tab, set **Storage account access** to **Identity-based access**. Enable **Disable shared key access**.

    :::image type="content" source="../media/disable-local-auth/ai-hub-identity-based-access.png" alt-text="Screenshot that shows hub creation by using Identity-based storage access." lightbox="../media/disable-local-auth/ai-hub-identity-based-access.png":::

1. Continue the hub creation process. As the hub is created, the managed identity is automatically assigned the permissions it needs to access the storage account.

# [Python SDK](#tab/python)

When you create your hub with the SDK, set `system_datastores_auth_mode="identity"` for the hub. To use a pre-existing storage account, use the `storage_account` parameter to specify the Resource Manager ID of an existing storage account:

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
    storage_account="{existing_storage_account with AllowSharedKeyAccess=false}",
    system_datastores_auth_mode="identity",
)

created_hub = ml_client.workspaces.begin_create(ws_hub).result()
print(created_hub)
```

# [Azure CLI](#tab/cli)

To create a new hub with Microsoft Entra ID authorization for the storage account, use a YAML configuration file that sets `system_datastores_auth_mode` to `identity`. You can also specify the Resource Manager ID of an existing storage account with the `storage_account` entry.

This example YAML file shows how to set the hub to use a managed identity and an existing storage account:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/workspace.schema.json
name: mlw-basicex-prod
location: eastus
display_name: Bring your own dependent resources-example
description: This configuration specifies a workspace configuration with existing dependent resources
storage_account: <your-storage-account-resource-id>
system_datastores_auth_mode: identity
tags:
  purpose: demonstration
```

You can use this YAML file with the `az ml workspace create` command and the `--file` parameter:

```azurecli-interactive
az ml workspace create -g <resource-group-name> --kind hub --file workspace.yml
```

# [ARM template](#tab/armtemplate)

In the JSON template example, substitute your own values for the following placeholders:

- `<workspace-name>`
- `<workspace-friendly-name>`
- `<storage-account-arm-resource-id>`
- `<key-vault-arm-resource-id>`

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources":
    [
        {
            "type": "Microsoft.MachineLearningServices/workspaces",
            "apiVersion": "2024-04-01",
            "name": "<workspace-name>",
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
                "friendlyName": "<workspace-friendly-name>",
                "storageAccount": "<storage-account-arm-resource-id>",
                "keyVault": "<key-vault-arm-resource-id>",
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

For information about how to deploy an Azure Resource Manager template (ARM template), see the following articles:

- [Tutorial: Deploy a local ARM template by using the Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template)
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal)

After you create the hub, identify all the users who need to use it, such as data scientists. The users must be assigned the Storage Blob Data Contributor and Storage File Data Privileged Contributor roles in Azure role-based access control (RBAC) for the storage account. If the users need only read access, use the Storage Blob Data Reader and Storage File Data Privileged Reader roles instead. For more information, see [Role assignments](#scenarios-for-hub-storage-account-role-assignments).

---

## Update an existing hub

If you have an existing Azure AI Foundry hub, use the steps in this section to update the hub to use Microsoft Entra ID to authorize access to the storage account. Then disable shared-key access on the storage account.

# [Azure portal](#tab/portal)

1. Go to the Azure portal and select **Azure AI Foundry hub**.
1. On the left menu, select **Properties**. At the bottom of the pane, set **Storage account access** to **Identity-based access**. Select **Save** at the top of the pane to save the configuration.

    :::image type="content" source="../media/disable-local-auth/update-existing-hub-identity-based-access.png" alt-text="Screenshot that shows selection of Identity-based access." lightbox="../media/disable-local-auth/update-existing-hub-identity-based-access.png":::

# [Python SDK](#tab/python)

To update an existing hub, set `system_datastores_auth_mode = "identity"` for the hub. The following code sample shows an update of a hub named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "identity"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To update an existing hub, use the `az ml workspace update` command and specify `--system-datastores-auth-mode identity`. The following example shows an update of a hub named `myhub`:

```azurecli-interactive
az ml workspace update --name myhub --system-datastores-auth-mode identity
```

# [ARM template](#tab/armtemplate)

In the JSON template example, substitute your own values for the following placeholders:

- *[workspace name]*
- *[workspace friendly name]*
- *[Storage Account ARM resource ID]*
- *[Key Vault ARM resource ID]*

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

For information about how to deploy an ARM template, see the following articles:

- [Tutorial: Deploy a local ARM template by using the Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template)
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal)

---

### Assign roles to users

After you update the hub, update the storage account to disable shared-key access. For more information, see [Prevent shared-key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent).

You must also identify all the users who need access to the default datastores, such as data scientists. The users must be assigned the Storage Blob Data Contributor and Storage File Data Privileged Contributor roles in Azure RBAC for the storage account. If the users need only read access, use the Storage Blob Data Reader and Storage File Data Privileged Reader roles instead. For more information, see the [Role assignments](#scenarios-for-hub-storage-account-role-assignments) section.

## Revert to using shared keys

To revert a hub back to using shared keys to access the storage account, use the following information.

# [Azure portal](#tab/portal)

1. Go to **Properties** and select **Credential-based access**.

   :::image type="content" source="../media/disable-local-auth/update-existing-hub-credential-based-access.png" alt-text="Screenshot that shows selection of Credential-based access." lightbox="../media/disable-local-auth/update-existing-hub-credential-based-access.png":::

1. Select **Save**.

# [Python SDK](#tab/python)

To configure the hub to use a shared key again, set `system_datastores_auth_mode = "accesskey"` for the hub. This code updates a hub named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "accesskey"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To configure the hub to use a shared key again, use the `az ml workspace update` command and specify `--system-datastores-auth-mode accesskey`. This example updates a hub named `myhub`:

```azurecli-interactive
az ml workspace update --name myhub --system-datastores-auth-mode accesskey
```

# [ARM template](#tab/armtemplate)

If you have an existing Azure AI Foundry hub, use the steps in this section to update the hub to use Microsoft Entra ID to authorize access to the storage account. Then, disable shared-key access on the storage account.

In the JSON template example, substitute your own values for the following placeholders:

- *[workspace name]*
- *[workspace friendly name]*
- *[Storage Account ARM resource ID]*
- *[Key Vault ARM resource ID]*

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

For information on how to deploy an ARM template, see the following articles:

- [Tutorial: Deploy a local ARM template using Azure CLI or Azure PowerShell](/azure/azure-resource-manager/templates/deployment-tutorial-local-template).
- [Quickstart: Create and deploy ARM templates by using the Azure portal](/azure/azure-resource-manager/templates/quickstart-create-templates-use-the-portal).

After you create the hub, identify all the users who will use it, such as data scientists. The users must be assigned the Storage Blob Data Contributor and Storage File Data Privileged Contributor roles in Azure RBAC for the storage account. If the users need only read access, use the Storage Blob Data Reader and Storage File Data Privileged Reader roles instead. For more information, see the [Role assignments](#scenarios-for-hub-storage-account-role-assignments) section.

---

After you revert the hub, update the storage account to enable shared key access. For more information, see [Prevent shared-key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent).

## Scenarios for hub storage account role assignments

To work with a storage account with disabled shared-key access, you need to grant more roles to either your users or the managed identity for your hub. Hubs have a system-assigned managed identity by default. Some scenarios require a user-assigned managed identity. This table summarizes the scenarios that require extra role assignments.

| Scenario | Microsoft Entra ID | Required roles | Notes |
| ----- | ----- | ----- | ----- |
| Azure AI Speech | User's identity | Storage Blob Data Contributor </br>Storage File Data Privileged Contributor | |
| Models as a service | System-assigned managed identity | Storage Blob Data Contributor | The hub's managed identity. </br>Automatically assigned the role when you provision the hub. </br>Don't manually change this role assignment. |
| Azure AI Search | System-assigned managed identity | Storage Blob Data Contributor | The hub's managed identity. </br>Automatically assigned the role when you provision the hub. </br>Don't manually change this role assignment. |
| Fine-tuning of open-source software models | User-assigned managed identity | Storage Blob Data Contributor | |
| Prompt flow | User's identity | Storage Blob Data Contributor </br>Storage File Data Privileged Contributor | |
| Add and manage your own data | User's identity | Storage Blob Data Contributor | |

## Related content

- [Prevent shared-key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent)
- [Create an Azure AI Foundry hub](develop/create-hub-project-sdk.md)
