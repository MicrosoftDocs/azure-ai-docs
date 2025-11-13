---
title: Connect your own storage to Speech/Language (Preview)
titleSuffix: Microsoft Foundry
description: Configure customer-managed storage for Speech and Language capabilities in a Microsoft Foundry resource at creation time.
#customer intent: As a developer, I want to use my own storage account for Speech and Language so I can apply security and compliance policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: andyaviles
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to
ms.date: 11/18/2025
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Connect your own storage for Speech and Language services (Preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Microsoft Foundry unifies Agents, Azure OpenAI, Speech, and Language capabilities under a single resource type. For Speech and Language, bring-your-own-storage (BYOS) is enabled through a resource-level binding set at creation time (`userOwnedStorage`). This binding provides backward compatibility with earlier standalone Speech and Language resource patterns while centralizing management.

Use this article when you specifically need Speech and Language data to land in an Azure Storage account you own. For the broader approaches (connections, capability hosts, and when to use them for other features), see [Connect to your own storage](bring-your-own-azure-storage-foundry.md).


## Prerequisites

Before you begin:

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

- An Azure Storage account (Blob) in a region supported by your Foundry resource.
- Permissions: Owner or Contributor on both the Foundry resource (or resource group) and the Storage account.
- Decision to use customer-managed keys (CMK) encryption (optional) on the storage account.
- Understanding of the restrictions below.

> [!TIP]
> Review [Azure Storage documentation](/azure/storage/) for encryption, networking, and advanced security options.

## Understand restrictions

Consider these constraints before configuring `userOwnedStorage`:

| Restriction | Details |
|-------------|---------|
| Single account | You can set only one storage account for Speech & Language. |
| Creation time only | Must be set during resource creation; cannot be added or changed afterward. |
| Non-removable | You cannot remove or swap the storage account post-creation. |
| Deletion impact | If the storage account is deleted or moved (resource ID changes), Speech & Language stop functioning. Attempt [storage account recovery](/azure/storage/common/storage-account-recover) first; otherwise you must recreate the Foundry resource. |
| Shared across both capabilities | Speech and Language share the same account (distinct containers). For strict isolation, create separate Foundry resources and storage accounts. |
| Data access scope | Any user with access to the Foundry resource can access Speech & Language outputs; project-level isolation doesn’t apply for this binding. |

## Configure authentication

Speech and Language support only Azure role-based access control (RBAC) via the resource’s managed identity.

1. Ensure the Foundry resource has a system-assigned managed identity.
2. On the storage account, assign the `Storage Blob Data Contributor` role to the Foundry resource’s managed identity.
3. Do NOT assign the role to individual project identities for this scenario.

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

### Example (PowerShell) – role assignment

```powershell
$storage = "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storageName>"
$foundry = "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<foundryName>"

$principalId = (Get-AzResource -ResourceId $foundry).Identity.PrincipalId
New-AzRoleAssignment -ObjectId $principalId -RoleDefinitionName "Storage Blob Data Contributor" -Scope $storage
```

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

### Sample repository

See the infrastructure examples (including Speech/Language storage) in the [Foundry samples repository](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/02-storage-speech-language).

## Speech integration details

Speech scenarios (Speech-to-Text batch/real-time, Custom Speech, Text-to-Speech, Custom Voice) conform to guidance in [Bring your own storage (BYOS) Speech resource](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal). When `userOwnedStorage` is set, those outputs route to the bound storage account containers.

### Customer-managed keys (CMK)

If you configure [customer-managed keys](/azure/storage/common/customer-managed-keys-overview) encryption on the storage account, Speech data written there uses those keys. If `userOwnedStorage` isn’t set, Speech falls back to Microsoft-managed storage and doesn’t inherit CMK settings from the Foundry resource.

## Language integration details

The `userOwnedStorage` binding mirrors historical Language resource behavior with one key difference: you cannot update or replace the storage account after deletion or move. In standalone Language resources an update is possible; in the unified Foundry resource it is not—plan lifecycle mitigation accordingly.

## Shared storage configuration

Speech and Language share the same storage account (different container naming conventions keep data logically separated). Because access is at the resource scope, any resource-level user can reach both sets of outputs. For stricter separation, deploy distinct resources.

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
- [Samples: infrastructure setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup)
- [Terraform cognitive_account](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account)
- [Speech BYOS resource guidance](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal)
