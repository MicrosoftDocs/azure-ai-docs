---
title: Connect to your own storage
titleSuffix: Azure AI Foundry
ms.reviewer: andyaviles
description: Learn how to bring your own storage to Azure AI Foundry for agents, evaluations, datasets, and other capabilities.
#customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own storage instead of Microsoft-managed storage.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to
ms.date: 10/27/2025
ai-usage: ai-assisted
---

# Connect to your own storage

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Azure AI Foundry brings Agents, Azure OpenAI, Speech, and Language services together under one unified resource type. Bring-your-own-storage (BYOS) lets you route data produced by these capabilities to an Azure Storage account that you own and govern. The configuration patterns align with (and provide backwards compatibility to) earlier standalone Speech and Language resource types.

This article shows you how to connect your storage to Azure AI Foundry by using two overarching approaches:

1. Connections + (optional) capability hosts (recommended baseline for most features)
2. userOwnedStorage field (Speech and Language only)

Connections provide the shared data pointer; capability hosts optionally override/explicitly bind a specific feature (for example, Agents standard setup) to one connection among several. The userOwnedStorage field is a resource-level binding used only by Speech and Language.

## Prerequisites

Before connecting your storage, ensure you have:

- An Azure subscription with an active Azure AI Foundry resource
- An Azure Storage account in the same subscription (Blob Storage supported)
- Contributor or Owner permissions on both the Azure AI Foundry resource and the storage account
- Clarity on which features you plan to use (Agents, Evaluations, Datasets, Content Understanding, Speech, Language)
- (Optional) A plan for customer-managed keys (CMK) encryption on the storage account

> [!TIP]
> See [Azure Storage documentation](/azure/storage/) for guidance on security, networking, and encryption options.

## Understand storage connection approaches

| Approach | What it is | Features supported | Scope | When to use |
|----------|------------|--------------------|-------|-------------|
| Connections (shared data pointer) | Sub-resource holding endpoint + auth; grants project users indirect access | Agents, Evaluations, Datasets, Content Understanding | Resource or project level | Default pattern for most scenarios |
| Capability hosts (feature override binding) | Explicit per-feature binding selecting which connection a feature uses | Agents (standard setup) | Resource and project level | When multiple connections exist and you must force one for Agents |
| userOwnedStorage field (resource storage binding) | Resource property assigning one storage account for Speech & Language (shared) | Speech, Language | Resource level only | To enable customer-managed storage for Speech & Language at creation time |

### Connections

Connections are lightweight sub-resources that store the external service's endpoint plus authentication details. After you create one, users with project permissions can use the data without needing direct role assignments on the storage account. Use connections as the baseline pattern for most scenarios; add a capability host only when you need to explicitly bind a feature to one connection among several.

### Capability hosts

Capability hosts are optional feature-level bindings that reference an existing connection. For Agents standard setup, a capability host directs agent data to your chosen connection instead of Microsoft-managed storage. Without a capability host, Agents use Microsoft-managed storage by default.

See [Capability hosts](../agents/concepts/capability-hosts.md) for conceptual details.

### userOwnedStorage field (Speech & Language)

The `userOwnedStorage` field is set during resource creation to bind one storage account for Speech and Language capabilities. Speech and Language share the account (different containers) and the setting applies to all projects in the resource. You cannot change or remove it later.

If strict data isolation is required between Speech and Language scenarios, create separate Azure AI Foundry resources with different storage accounts.

> [!IMPORTANT]
> If you delete or move (change resource ID of) the storage account bound by `userOwnedStorage`, Speech and Language stop functioning. Consider attempting account recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover). Otherwise you must recreate the Azure AI Foundry resource.

## Create a storage connection

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
2. Open your Azure AI Foundry resource or project.
3. In the left navigation, select **Connections** (or **Connected resources**).
4. Select **+ New connection**.
5. Choose **Azure Blob Storage**.
6. Provide:
   - Name
   - Subscription
   - Storage account
   - Authentication method (system-assigned managed identity recommended)
7. Select **Create**.

The connection is now available to Agents (when not overridden), Evaluations, Datasets, and Content Understanding.

## Configure capability host for Agents (combined resource + project steps)

You create two capability hosts—one at the resource level and one at the project level—each referencing the same connection chain so Agents route to your storage.

1. Create a resource-level connection (as above) if not already present.
2. Create a resource-level capability host referencing that connection.
3. Create (or open) a project under the resource.
4. Create a project-level capability host referencing the resource-level capability host.
5. Verify Agents data now writes to the bound storage account.

> [!NOTE]
> A future UX flow will streamline these steps directly in the portal.

### Example (Azure CLI) *(illustrative)*
```bash
# Placeholder example; adjust for actual CLI verbs when published
az ai-foundry capability-host create \
  --resource-name MyFoundryResource \
  --name agents-host \
  --feature agents \
  --connection-id /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/MyFoundryResource/connections/myblobconnection
```

### Example (PowerShell) *(illustrative)*
```powershell
New-AIFCapabilityHost -ResourceName MyFoundryResource -Name agents-host -Feature agents -ConnectionId "/subscriptions/<sub>/resourceGroups/<rg>/.../connections/myblobconnection"
```

### ARM template snippet *(illustrative)*
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

See the sample repository for evolving end-to-end infrastructure examples: [Infrastructure setup samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup).

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

Create the role assignment on the Azure Storage account for the Foundry resource (account) managed identity—not the project managed identity. Assign `Storage Blob Data Contributor`.

## Configure Content Understanding

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
2. Open the resource.
3. Select **Content Understanding**.
4. Choose the existing storage connection.

> [!NOTE]
> Programmatic configuration options for Content Understanding are under evaluation.

## End-to-end customer-managed storage checklist

1. Create resource with `userOwnedStorage` (if Speech/Language needed).
2. Create storage connection (connections).
3. Create resource-level capability host (Agents override when needed).
4. Create project-level capability host (Agents override at project).
5. Bind Content Understanding to the storage connection.

After these steps all features (Agents, Evaluations, Datasets, Content Understanding, Speech, Language) route to customer-managed storage.

## Related content

- [Capability hosts for Agents](../agents/concepts/capability-hosts.md)
- [Understanding Agents standard setup](../agents/concepts/standard-agent-setup.md)
- [Add connections to your project](connections-add.md)
- [Recover a storage account](/azure/storage/common/storage-account-recover)
- [Azure Storage documentation](/azure/storage/)
- [Infrastructure setup samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup)
- [Connect storage for Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal)