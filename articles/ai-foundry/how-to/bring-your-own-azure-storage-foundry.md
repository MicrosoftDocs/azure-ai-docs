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

- Connections + (optional) capability hosts (recommended baseline for most features)
- userOwnedStorage field (Speech and Language only)

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

| **Approach** | **Features Supported** | **Scope** |
|-------------|------------------------|-----------|
| Foundry connections (shared data pointer) | Agents, Evaluations, Datasets, Content Understanding | Resource or project level |
| Capability hosts (feature override binding) | Agents standard setup (explicit assignment) | Resource and project level |
| userOwnedStorage field (resource storage binding) | Speech, Language | Resource level only |

### Foundry connections

Foundry connections act as shared data pointers across AI Foundry capabilities (agents, evaluations, datasets, content understanding). Each connection wraps the target storage endpoint plus authentication so users with project access can use the data without direct storage account permissions. Use connections as the default pattern; create a capability host only when you need to explicitly bind (override) a single feature to one connection among several.

### Capability hosts

[Capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) bind specific features to designated connections when multiple storage connections exist. They define which storage connection a particular feature uses. Use capability hosts most commonly for agents standard setup. If you don't create capability hosts for agents, AI Foundry uses Microsoft-managed storage for that feature.

See [Capability hosts](../agents/concepts/capability-hosts.md) for conceptual details.

The userOwnedStorage field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account for these capabilities with backwards compatibility to the approach used for Azure Speech and Azure Language resource types.

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

## Configure capability hosts for agents

Set up [capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) to use your storage connection for agents standard setup. You need to configure capability hosts at both the resource and project levels.

### Create resource-level capability host

1. Use the [Azure CLI](/cli/azure/ml/capability-host) or [Azure REST API](/rest/api/azureml/capability-hosts/create-or-update) to create a resource-level capability host.

1. Reference your previously created storage connection in the capability host configuration.

1. Set the capability type to support agents.

### Create project-level capability host

After creating your AI Foundry project:

1. Create a project-level capability host that references the resource-level capability host.

1. Configure the capability host to enable agents functionality.

1. Verify the capability host is properly linked to your storage connection as demonstrated in this [code sample for Standard agent setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup#41-standard-agent-setup).

Your agents standard setup now uses your own storage account instead of Microsoft-managed storage.

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