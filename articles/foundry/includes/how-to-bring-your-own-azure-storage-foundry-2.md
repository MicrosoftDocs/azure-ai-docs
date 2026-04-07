---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: andyaviles
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Configure capability host for Agents (combined resource + project steps)

You create two capability hosts—one at the resource level and one at the project level—each referencing the same connection chain so Agents route to your storage.

1. Create a resource-level connection (as above) if not already present.
   > [!NOTE]
   > As described in the previous section, select the **Catalog** tab and look for **Azure Blob Storage**.
1. Create a resource-level capability host referencing that connection.
1. Create (or open) a project under the resource.
1. Create a project-level capability host referencing the resource-level capability host.
1. Verify Agents data now writes to the bound storage account.

### Example (REST API)

Use the [Capability Hosts - Create Or Update](/rest/api/azureml/capability-hosts/create-or-update) REST API to create a capability host:

```http
PUT https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource>/capabilityHosts/agents-host?api-version=2025-05-01-preview

{
  "properties": {
    "capabilityHostKind": "Agents",
    "storageConnections": [
      "<connection-arm-resource-id>"
    ]
  }
}
```

Replace `<connection-arm-resource-id>` with the full ARM resource ID of your blob storage connection.

> [!NOTE]
> For Azure CLI and PowerShell, use the REST API through `az rest` or `Invoke-AzRestMethod` until dedicated cmdlets are available.

### ARM template snippet
```json
{
  "type": "Microsoft.CognitiveServices/accounts/capabilityHosts",
  "apiVersion": "2025-05-01-preview",
  "name": "[concat(parameters('foundryName'), '/agents-host')]",
  "properties": {
    "feature": "agents",
    "connectionId": "[resourceId('Microsoft.CognitiveServices/accounts/connections', parameters('foundryName'), 'myblobconnection')]"
  }
}
```

## Configure capability hosts for agents

Set up [capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) to use your storage connection for agents standard setup. You need to configure capability hosts at both the resource and project levels.

### Create resource-level capability host

1. Use the [Azure CLI](/cli/azure/ml/capability-host) or [Azure REST API](/rest/api/azureml/capability-hosts/create-or-update) sample to create a resource-level capability host.

1. Reference your previously created storage connection in the capability host configuration.

1. Set the capability type to support agents.

### Create project-level capability host

After creating your Foundry project:

1. Create a project-level capability host that references the resource-level capability host.

1. Configure the capability host to enable agents functionality.

1. Verify the capability host is properly linked to your storage connection as demonstrated in this [code sample for Standard agent setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/41-standard-agent-setup).

Your agents standard setup now uses your own storage account instead of Microsoft-managed storage.

## Verify your storage configuration

After you configure storage connections and capability hosts, confirm that data routes to your storage account:

1. Sign in to the [Azure portal](https://portal.azure.com) and open your storage account.
1. Navigate to **Containers** under **Data storage**.
1. Create a test agent in your Foundry project and run a simple interaction.
1. Return to the storage account and refresh the **Containers** view.
1. Verify that new containers or blobs appear in your storage account.

If data doesn't appear in your storage account, check the following:

- Both resource-level and project-level capability hosts exist and reference the correct connection.
- The project managed identity has the `Storage Blob Data Contributor` role on the storage account.
- The storage account has `allowSharedKeyAccess` set to `true`.
- Network settings on the storage account allow access from Microsoft Foundry.

## Set userOwnedStorage for Speech and Language

Set the field during resource creation—via Bicep, ARM, Terraform, CLI, or PowerShell.

### Bicep example
```bicep
resource foundry 'Microsoft.CognitiveServices/accounts@2025-05-01-preview' = {
  name: myFoundryName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  properties: {
    userOwnedStorage: {
      storageResourceId: storageAccount.id
    }
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
    resource_id = azurerm_storage_account.speechlang.id
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
