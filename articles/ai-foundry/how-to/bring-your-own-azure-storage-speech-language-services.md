---
title: Connect your own storage to Speech/Language (Preview)
titleSuffix: Microsoft Foundry
description: Configure customer-managed storage for Speech and Language capabilities in a Microsoft Foundry resource at creation time.
#customer intent: As a developer, I want to use my own storage account for Speech and Language so I can apply security and compliance policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025, dev-focus
ms.topic: how-to
ms.date: 02/02/2026
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Connect your own storage for Speech and Language services (Preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Configure bring-your-own-storage (BYOS) for Speech and Language capabilities in a Foundry resource by setting the `userOwnedStorage` binding at creation time. This binding routes Speech and Language data to your Azure Storage account while maintaining backward compatibility with earlier standalone resource patterns.

> [!TIP]
> Use this article when you specifically need Speech and Language data to land in storage you own. For the broader approaches (connections, capability hosts), see [Connect to your own storage](bring-your-own-azure-storage-foundry.md).


## Prerequisites

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- An Azure Storage account (Blob) in a region supported by your Foundry resource.
- **Resource group permissions**: `Owner` or `Contributor` role on the resource group containing the Foundry resource.
- **Storage account permissions**: `Storage Blob Data Contributor` role on the storage account (assigned to the Foundry resource's managed identity).
- (Optional) Customer-managed keys (CMK) configured on the storage account if you require CMK encryption.

> [!IMPORTANT]
> Set the `userOwnedStorage` binding when you create the resource. You can't change this binding later. Review the [restrictions](#understand-restrictions) before proceeding.

## Understand restrictions

Review these constraints before configuring `userOwnedStorage`:

| Restriction | Details |
|-------------|---------|
| Single account | You can set only one storage account for Speech & Language. |
| Creation time only | Must be set during resource creation; can't add or change afterward. |
| Non-removable | You can't remove or swap the storage account post-creation. |
| Deletion impact | If you delete or move the storage account (resource ID changes), Speech & Language stop functioning. Attempt [storage account recovery](/azure/storage/common/storage-account-recover) first; otherwise you must recreate the Foundry resource. |
| Shared across both capabilities | Speech and Language share the same account (distinct containers). For strict isolation, create separate Foundry resources and storage accounts. |
| Data access scope | Any user with access to the Foundry resource can access Speech & Language outputs; project-level isolation doesn’t apply for this binding. |

## Configure authentication

Speech and Language support only Azure role-based access control (RBAC) through the resource’s managed identity.

1. Ensure the Foundry resource has a system-assigned managed identity.
1. On the storage account, assign the `Storage Blob Data Contributor` role to the Foundry resource’s managed identity.
1. Don't assign the role to individual project identities for this scenario.

API key–based authentication isn't supported.

### Example (Azure CLI) – role assignment

```bash
STORAGE_ID=/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storageName>
FOUNDRY_ID=/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<foundryName>

# Assign Storage Blob Data Contributor
az role assignment create \
  --assignee-object-id $(az resource show --ids $FOUNDRY_ID --query identity.principalId -o tsv) \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope $STORAGE_ID
```

If successful, the command returns a JSON object with the role assignment details including `principalId` and `roleDefinitionId`.

**Reference**: [az role assignment create](/cli/azure/role/assignment#az-role-assignment-create) | [az resource show](/cli/azure/resource#az-resource-show)

### Example (PowerShell) – role assignment

```powershell
$storage = "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storageName>"
$foundry = "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<foundryName>"

$principalId = (Get-AzResource -ResourceId $foundry).Identity.PrincipalId
New-AzRoleAssignment -ObjectId $principalId -RoleDefinitionName "Storage Blob Data Contributor" -Scope $storage
```

If successful, the command returns a `RoleAssignment` object with the `DisplayName`, `ObjectId`, and `Scope` properties.

**Reference**: [New-AzRoleAssignment](/powershell/module/az.resources/new-azroleassignment) | [Get-AzResource](/powershell/module/az.resources/get-azresource)

## Create resource with storage account

Set the `userOwnedStorage` field during resource creation.

### Bicep template snippet

```bicep
resource storage 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageName
}

resource foundry 'Microsoft.CognitiveServices/accounts@2025-05-01-preview' = {
  name: foundryName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    userOwnedStorage: {
      storageResourceId: storage.id
    }
  }
}
```

**Reference**: [Microsoft.CognitiveServices/accounts](/azure/templates/microsoft.cognitiveservices/accounts) | [Microsoft.Storage/storageAccounts](/azure/templates/microsoft.storage/storageaccounts)

### ARM template snippet

```json
{
  "type": "Microsoft.CognitiveServices/accounts",
  "apiVersion": "2025-05-01-preview",
  "name": "[parameters('foundryName')]",
  "location": "[parameters('location')]",
  "kind": "AIServices",
  "identity": { "type": "SystemAssigned" },
  "sku": { "name": "S0" },
  "properties": {
    "userOwnedStorage": {
      "storageResourceId": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageName'))]"
    }
  }
}
```

**Reference**: [Microsoft.CognitiveServices/accounts](/azure/templates/microsoft.cognitiveservices/accounts) | [ARM template functions](/azure/azure-resource-manager/templates/template-functions)

### Terraform snippet

Refer to the [Terraform cognitive_account documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account).

```hcl
resource "azurerm_cognitive_account" "foundry" {
  name                = var.foundry_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "AIServices"
  sku_name            = "S0"

  # userOwnedStorage equivalent
  storage {
    resource_id = azurerm_storage_account.speechlang.id
  }

  identity {
    type = "SystemAssigned"
  }
}
```

**Reference**: [azurerm_cognitive_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account) | [azurerm_storage_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account)

### Sample repository

See the infrastructure examples (including Speech/Language storage) in the [Foundry samples repository](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/02-storage-speech-language).

## Speech integration details

Speech scenarios (Speech-to-Text batch or real-time, Custom Speech, Text-to-Speech, Custom Voice) conform to the guidance in [Bring your own storage (BYOS) Speech resource](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal). When you set `userOwnedStorage`, those outputs route to the bound storage account containers.

### Customer-managed keys (CMK)

If you configure [customer-managed keys](/azure/storage/common/customer-managed-keys-overview) encryption on the storage account, Speech data written there uses those keys. If you don't set `userOwnedStorage`, Speech falls back to Microsoft-managed storage and doesn't inherit CMK settings from the Foundry resource.

## Language integration details

The `userOwnedStorage` binding mirrors historical Language resource behavior with one key difference: you can't update or replace the storage account after deletion or move. In standalone Language resources, an update is possible. In the unified Foundry resource, it isn't. Plan lifecycle mitigation accordingly.

## Shared storage configuration

Speech and Language share the same storage account. Different container naming conventions keep data logically separated. Because access is at the resource scope, any resource-level user can reach both sets of outputs. For stricter separation, deploy distinct resources.

## Verify the configuration

After creating the resource with `userOwnedStorage`, confirm the binding is active:

1. In the [Azure portal](https://portal.azure.com), go to your Foundry resource.
1. Select **Resource Management** > **Properties** and verify the **User Owned Storage** field displays your storage account resource ID.
1. Run a test Speech or Language operation (for example, a batch transcription job) and confirm the output appears in a container within your storage account.

If the storage binding isn't visible or operations fail, see the troubleshooting section.

## Troubleshooting

| Issue | Mitigation |
|-------|------------|
| Accidental deletion of storage account | Attempt [recovering the account](/azure/storage/common/storage-account-recover). If unsuccessful, recreate the Foundry resource. |
| Role assignment missing | Re-run RBAC role assignment for the resource managed identity on the storage account. |
| Moved storage to new subscription | Recreate resource; moving changes the resource ID and breaks binding. |

## Related content

- [Connect to your own storage (overview)](bring-your-own-azure-storage-foundry.md)
- [Capability hosts for Agents](../agents/concepts/capability-hosts.md)
- [Recover a storage account](/azure/storage/common/storage-account-recover)
- [Azure Storage documentation](/azure/storage/)
- [Samples: infrastructure setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples)
- [Terraform cognitive_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account)
- [Speech BYOS resource guidance](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal)
