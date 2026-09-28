---
title: Include file
description: Include file
author: s-polly
ms.reviewer: andyaviles
ms.author: scottpolly
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/18/2026
ms.custom: include
ai-usage: ai-assisted
---

## Configure agent storage

Declare your storage account in the capability settings on the Foundry account or project. Agent Service provisions the required underlying infrastructure and the connection to that account, so you don't create or bind a connection for agent files yourself.

1. Get the full Azure resource ID of your storage account.
1. Set `blobStore` in `capabilitySettings` on the Foundry account to establish the default for its projects.
1. Create or open a project. The project inherits the account value unless you override `blobStore` on the project.
1. Verify that agent data now writes to your storage account.

### Example (Bicep)

The following `properties` block sets the storage account that agents use for files. Use it with API version `2026-07-15-preview`.

```bicep
properties: {
  allowProjectManagement: true
  customSubDomainName: accountName
  capabilitySettings: {
    blobStore: storageAccountId
  }
}
```

The identity that runs this deployment needs **Storage Blob Data Contributor** on the storage account, in addition to permission to create the Foundry account. For the full permission model, see [Configure agent capability settings](../how-to/configure-capability-settings.md#permissions).

## Verify your storage configuration

After you configure storage connections and capability settings, confirm that data routes to your storage account:

1. Sign in to the [Azure portal](https://portal.azure.com) and open your storage account.
1. Navigate to **Containers** under **Data storage**.
1. Create a test agent in your Foundry project and run a simple interaction.
1. Return to the storage account and refresh the **Containers** view.
1. Verify that new containers or blobs appear in your storage account.

If data doesn't appear in your storage account, check the following:

- A GET on the project returns the `blobStore` value you expect, either set on the project or inherited from the account.
- The project managed identity has the required storage roles: **Storage Account Contributor** on the storage account, **Storage Blob Data Contributor** on the `<workspaceId>-azureml-blobstore` container, and **Storage Blob Data Owner** on the `<workspaceId>-agents-blobstore` container. See [Standard agent setup](../agents/concepts/standard-agent-setup.md) for the complete role list.
- Network settings on the storage account allow access from Microsoft Foundry.

## Set userOwnedStorage for Speech and Language

Set the field during resource creation—via Bicep, ARM, Terraform, CLI, or PowerShell.

### Bicep example
```bicep
resource foundry 'Microsoft.CognitiveServices/accounts@2026-07-01' = {
  name: myFoundryName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  properties: {
    userOwnedStorage: [
      {
        resourceId: storageAccount.id
      }
    ]
  }
}
```

### Terraform snippet
Refer to [Terraform cognitive_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account).
```hcl
resource "azurerm_cognitive_account" "foundry" {
  name                = var.foundry_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "AIServices"
  sku_name            = "S0"

  storage { # userOwnedStorage equivalent
    storage_account_id = azurerm_storage_account.speechlang.id
  }
}
```

### Role assignment

Create the role assignment on the Azure Storage account for the Foundry project managed identity. Assign the `Storage Blob Data Contributor` role so the project identity can read and write blobs in your storage account.

```azurecli
az role assignment create \
  --assignee <project-managed-identity-principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account-name>
```
