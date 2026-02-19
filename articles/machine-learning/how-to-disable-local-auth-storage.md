---
title: "Disable shared key access to the workspace storage account"
titleSuffix: Azure Machine Learning
description: "Disable shared key access to the default storage account used by your Azure Machine Learning workspace."
ms.author: scottpolly
author: shshubhe
ms.reviewer: shshubhe
ms.service: azure-machine-learning
ms.subservice: core
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 1/30/2026

#customer intent: As an admin, I want to disable shared key access to my resources to improve security.
---

# Disable shared key access for your workspace's storage account

An Azure Machine Learning workspace uses a shared key to access its default Azure Storage account. With key-based authorization, anyone who has the key and access to the storage account can access data.

To reduce the risk of unauthorized access, you can disable key-based authorization and instead use Microsoft Entra ID for authorization. This configuration uses a Microsoft Entra ID value to authorize access to the storage account. The identity used to access storage is either the user's identity or a managed identity. The user's identity is used to view data in the Azure Machine Learning studio or run a notebook while authenticated with the user's identity. The Azure Machine Learning service uses a managed identity to access the storage account - for example, when running a training job as the managed identity.


## Prerequisites

- For more information about the process and implications of disabling shared key authorization for your storage account, visit the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) resource.

# [Azure portal](#tab/portal)

Not applicable.

# [Python SDK](#tab/python)

1. [Install the SDK v2](https://aka.ms/sdk-v2-install).

    > [!IMPORTANT]
    > This article requires the **azure-ai-ml Python package, version 1.17.0**. To check the installed package version, use the `pip list` command from your Python development environment.

1. Install azure-identity: `pip install azure-identity`. If you're working in a notebook cell, use `%pip install azure-identity`.

1. Provide your subscription details:

    [!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=subscription_id)]

1. Get a handle to the subscription. All the Python code in this article uses `ml_client`:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=ml_client)]
      
    - (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you wish to use into the `DefaultAzureCredential`. Find your tenant ID from the [Azure portal](https://portal.azure.com), under __Microsoft Entra ID, External Identities__.
    
    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
                
    - (Optional) If you're working in the [Azure Government - US](https://azure.microsoft.com/explore/global-infrastructure/government/) or [Azure operated by 21Vianet](/azure/china/overview-operations) regions, you must specify the cloud into which you want to authenticate. You can specify these regions in `DefaultAzureCredential`.

    ```python
    from azure.identity import AzureAuthorityHosts
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT))
    ```

# [Azure CLI](#tab/cli)

To use the CLI commands in this document, you need the [Azure CLI](/cli/azure/install-azure-cli) and the [ml extension](how-to-configure-cli.md).

If you use the [Azure Cloud Shell](https://azure.microsoft.com//features/cloud-shell/), you access the CLI through the browser, and it lives in the cloud.

> [!IMPORTANT]
> The steps in this article require the **Azure CLI extension for machine learning, version 2.27.0**. To determine the version of the extension you installed, use the `az version` command from the Azure CLI. In the extensions collection that's returned, find the `ml` extension. This code sample shows an example return value:
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

Not applicable.

---

## Create a new workspace

When you create a new workspace, the creation process can automatically disable shared key access. Or you can create an Azure Storage account, disable shared key access, and use it during workspace creation.

# [Azure portal](#tab/portal)

1. In Azure Machine Learning studio, select **Create with customized networking, encryption identity, dependent resources or tags**.

    :::image type="content" source="./media/how-to-disable-local-auth-storage/create-new-workspace-azure-portal-first-step.png" alt-text="Screenshot showing selection of the Create with customized networking, encryption identity, dependent resources or tags dropdown option." lightbox="./media/how-to-disable-local-auth-storage/create-new-workspace-azure-portal-first-step.png":::

1. From the __Basics__ tab, select the __Storage account__ you created previously.

    :::image type="content" source="./media/how-to-disable-local-auth-storage/workspace-basics-storage-account.png" alt-text="Screenshot of workspace creation using the previously created storage account." lightbox="./media/how-to-disable-local-auth-storage/workspace-basics-storage-account.png":::

1. From the __Identity__ tab, in the __Storage account access__ section, set __Storage account access type__ to __identity-based__.

    :::image type="content" source="./media/how-to-disable-local-auth-storage/workspace-identity-based-access.png" alt-text="Screenshot of workspace creation using identity-based storage access." lightbox="./media/how-to-disable-local-auth-storage/workspace-identity-based-access.png":::

1. Continue the workspace creation process as usual. As the workspace is created, the managed identity is automatically assigned the permissions it needs to access the storage account.

# [Python SDK](#tab/python)

When you create your workspace with the SDK, set `system_datastores_auth_mode="identity"`. To use a preexisting storage account, use the `storage_account` parameter to specify the Azure Resource Manager ID of an existing storage account:

```python
# Creating a unique workspace name with current datetime to avoid conflicts
from azure.ai.ml.entities import Workspace
import datetime

# Azure Resource Manager ID of the storage account
storage_account = "<your_storage_account>"

basic_workspace_name = "mlw-basic-prod-" + datetime.datetime.now().strftime(
    "%Y%m%d%H%M"
)

ws_basic = Workspace(
    name=basic_workspace_name,
    location="eastus",
    display_name="Basic workspace-example",
    description="This example shows how to create a basic workspace",
    hbi_workspace=False,
    tags=dict(purpose="demo"),
    storage_account=storage_account,
    system_datastores_auth_mode="identity"
)

ws_basic = ml_client.workspaces.begin_create(ws_basic).result()
print(ws_basic)
```

# [Azure CLI](#tab/cli)

To create a new workspace with Microsoft Entra ID authorization for the storage account, use a YAML configuration file that meets these requirements sets `system_datastores_auth_mode` to `identity`. You can also specify the Azure Resource ID value of an existing storage account with the `storage_account` entry.

This example YAML file shows how to set the workspace to use a managed identity and an existing storage account:

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
az ml workspace create -g <resource-group-name> --file workspace.yml
```

# [ARM template](#tab/armtemplate)

In the following JSON template example, substitute your own values for the following placeholders:

In the JSON code sample shown here, substitute your own values for

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
            "kind": "Default",
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

After you create the workspace, identify all the users that will use it - for example, Data Scientists. Assign these users the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, visit the [role assignments](#scenarios-for-role-assignments) resource in this document.

---

## Update an existing workspace

If you have an existing Azure Machine Learning workspace, use the steps in this section to update the workspace to use Microsoft Entra ID to authorize access to the storage account. Then, disable shared key access on the storage account.

# [Azure portal](#tab/portal)

To update an existing workspace, go to **Properties** and select **Identity-based access**.

:::image type="content" source="./media/how-to-disable-local-auth-storage/update-an-existing-workspace-identity-based-access.png" alt-text="Screenshot showing selection of Identity-based access." lightbox="./media/how-to-disable-local-auth-storage/update-an-existing-workspace-identity-based-access.png":::

Select **Save** to save this choice.

# [Python SDK](#tab/python)

To update an existing workspace, set the `system_datastores_auth_mode = "identity"` for the workspace. This code sample shows an update of a workspace named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "identity"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To update an existing workspace, use the `az ml workspace update` command and specify `--system-datastores-auth-mode identity`. This example shows an update of a workspace named `myworkspace`:

```azurecli-interactive
az ml workspace update --name myworkspace --system-datastores-auth-mode identity
```

# [ARM template](#tab/armtemplate)

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
            "kind": "Default",
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

After updating the workspace, update the storage account to disable shared key access. For more information about disabling shared key access, see the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) article.

You must also identify all the users that need access to the default datastores - for example, Data Scientist. These users must be assigned the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, see the [role assignments](#scenarios-for-role-assignments) resource in this document.

## Revert to use shared keys

To revert a workspace back to use of shared keys to access the storage account, use this information:

# [Azure portal](#tab/portal)

To update an existing workspace, go to **Properties** and select **Credential-based access**.

:::image type="content" source="./media/how-to-disable-local-auth-storage/update-an-existing-workspace-credential-based-access.png" alt-text="Screenshot showing selection of Credential-based access." lightbox="./media/how-to-disable-local-auth-storage/update-an-existing-workspace-credential-based-access.png":::

Select **Save** to save this choice.

# [Python SDK](#tab/python)

To configure the workspace to use a shared key again, set the `system_datastores_auth_mode = "accesskey"` for the workspace. The following code demonstrates updating a workspace named `test-ws1`:

```python
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
ws = ml_client.workspaces.get(name="test-ws1")
ws.system_datastores_auth_mode = "accesskey"
ws = ml_client.workspaces.begin_update(workspace=ws).result()
```

# [Azure CLI](#tab/cli)

To configure the workspace to use a shared key again, use the `az ml workspace update` command and specify `--system-datastores-auth-mode accesskey`. The following example demonstrates updating a workspace named `myworkspace`.

```azurecli-interactive
az ml workspace update --name myworkspace --system-datastores-auth-mode accesskey
```

# [ARM template](#tab/armtemplate)

To revert the workspace to use shared keys for storage account access, use the following ARM template.

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
            "kind": "Default",
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

After you create the workspace, identify all the users that will use it - for example, Data Scientists. Assign these users the __Storage Blob Data Contributor__ and __Storage File Data Privileged Contributor__ roles in Azure role-based access control for the storage account. If these users only need read access, use the __Storage Blob Data Reader__ and __Storage File Data Privileged Reader__ roles instead. For more information, visit the [role assignments](#scenarios-for-role-assignments) resource in this document.

---

After reverting the workspace, you can re-enable shared key access on the storage account if it was previously disabled. For more information about managing shared key access, visit the [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent) article.

## Scenarios for role assignments

To work with a storage account that has disabled shared key access, you might need to grant more roles to either your users or the managed identity for your hub. Hubs have a system-assigned managed identity by default. However, some scenarios require a user-assigned managed identity. This table summarizes the scenarios that require extra role assignments:

| Scenario | Microsoft Entra ID |Required roles | Notes |
|---------|------|-------|-----|
| Managed online endpoint | System-assigned managed identity | Storage Blob Data Contributor | Automatically assigned the role when provisioned. </br>Don't manually change this role assignment. |
| Monitoring (evaluating model quality/perf) | User-assigned managed identity | Storage Blob Data Contributor | If an existing user-assigned managed identity is presently used by the workspace, verify that it has an assigned Storage Data Blob Contributor role.<br>The user-assigned managed identity is in addition to the system-assigned managed identity for your workspace. For information about how to add the managed identity to the workspace, visit [Add a user-assigned managed identity](how-to-identity-based-service-authentication.md#add-a-user-assigned-managed-identity-to-a-workspace-in-addition-to-a-system-assigned-identity).<br>|
| Model Registry and ML Flow | User-assigned managed identity | Storage Blob Data Contributor | Create compute cluster that uses the user-assigned identity.<br>* In case of model as input/output for a job, separately create an UAMI, add "Storage Data Contributor" role to underlying storage, and associate that UAMI when creating Compute Cluster. The job will then successfully run<br>* In case of registration of a model from local files, the user needs the "Storage Data Contributor" role for the  underlying storage<br>* Model package scenarios have known issues and are not supported at this time. |
| Parallel Run Step (PRS) | User-assigned managed identity | Storage Table Data Contributor<br><br>Storage Queue Data Contributor| |
| Data Labeling | User's identity | Storage Blob Data Contributor |  |
| Studio: create datasets, browse data |  User's identity | Storage Blob Data Contributor |  |
| Compute Instance | User's identity | Storage File Data Privileged Contributor |  |
| Studio: notebooks | User's identity | Storage File Data Privileged Contributor |  |
| Studio: notebook's file explorer | User's identity | Storage File Data Privileged Contributor |  |
| PromptFlow | User's identity | Storage Blob Data Contributor</br>Storage File Data Privileged Contributor |  |
| Data: datastores and datasets | User's identity | Storage Blob Data Contributor |  |

## Limitations
- Creating a compute instance with system-assigned managed identity isn't supported for identity-based workspaces. If the workspace's storage account access type is identity-based access, compute instances currently don't support system assigned identity to mount data store. Use user assigned identity to create the compute instance, and make sure the user-assigned identity has **Storage File Data Privileged Contributor** on the storage account.

- `git clone` operations in identity-based Azure Machine Learning workspaces are slow or fail, especially for repositories with many small files. The recommended workarounds are to clone into a local directory such as `/tmp` and then copy or symlink files, or to use credential-based access.

## Related content

- [Prevent shared key authorization for an Azure Storage account](/azure/storage/common/shared-key-authorization-prevent)
- [Create an Azure Machine Learning workspace](how-to-manage-workspace.md)
