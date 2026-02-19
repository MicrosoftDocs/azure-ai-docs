---
title: Connect to your own storage
titleSuffix: Microsoft Foundry
ms.reviewer: andyaviles
description: Learn how to bring your own storage to Microsoft Foundry for agents, evaluations, datasets, and other capabilities.
# customer intent: As a developer, I want to set up capability hosts for agents so that I can use my own storage instead of Microsoft-managed storage.
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.custom: ignite-2024, build-2025
ms.topic: how-to
ms.date: 12/05/2025
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Connect to your own storage

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Microsoft Foundry brings Agents, Azure OpenAI, Speech, and Language services together under one unified resource type. Bring-your-own-storage (BYOS) lets you route data produced by these capabilities to an Azure Storage account that you own and govern. The configuration patterns align with (and provide backwards compatibility to) earlier standalone Speech and Language resource types.

This article shows you how to connect your storage to Foundry by using two overarching approaches:

- Connections: recommended baseline for most features. Connections provide the shared data pointer.
- Capability hosts: optionally override/explicitly bind a specific feature (for example, Agents standard setup) to one connection among several.
- userOwnedStorage field: a resource-level binding used only by Speech and Language.

## Prerequisites

Before connecting your storage, ensure you have:

[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

1. An [Azure Storage account](/azure/storage/common/storage-account-create?tabs=azure-portal) in the same subscription (Blob Storage supported).
1. Contributor or Owner permissions on both the Foundry resource and the storage account.
1. Clarity on which features you plan to use (Agents, Evaluations, Datasets, Content Understanding, Speech, Language).
1. (Optional) A plan for customer-managed keys (CMK) encryption on the storage account.

> [!TIP]
> See [Azure Storage documentation](/azure/storage/) for guidance on security, networking, and encryption options.

## Understand storage connection approaches

| Approach | What it is | Features supported | Scope | When to use |
|----------|------------|--------------------|-------|-------------|
| Foundry connections (shared data pointer) | Sub-resource holding endpoint + auth; grants project users indirect access | Agents, Evaluations, Datasets, Content Understanding | Resource or project level | Default pattern for most scenarios |
| Capability hosts (feature override binding) | Explicit per-feature binding selecting which connection a feature uses | Agents (standard setup) | Resource and project level | When multiple connections exist and you must force one for Agents |
| userOwnedStorage field (resource storage binding) | Resource property assigning one storage account for Speech & Language (shared) | Speech, Language | Resource level only | To enable customer-managed storage for Speech & Language at creation time |

### Foundry connections

Foundry connections act as shared data pointers across Foundry capabilities (agents, evaluations, datasets, content understanding). Each connection wraps the target storage endpoint plus authentication so users with project access can use the data without direct storage account permissions. Use connections as the default pattern; create a capability host only when you need to explicitly bind (override) a single feature to one connection among several.

### Capability hosts

[Capability hosts](/azure/ai-foundry/agents/concepts/capability-hosts) bind specific features to designated connections when multiple storage connections exist. They define which storage connection a particular feature uses. Use capability hosts most commonly for agents standard setup. If you don't create capability hosts for agents, Foundry uses Microsoft-managed storage for that feature.

See [Capability hosts](../agents/concepts/capability-hosts.md) for conceptual details.

### userOwnedStorage (resource storage binding)

The `userOwnedStorage` field enables customer-managed storage for Speech and Language capabilities. Set this field during resource creation at the resource level, so all projects within the resource share the same storage account.

Speech and Language capabilities share the storage account but use different containers within it. The setting applies at the resource level and cannot be changed after creation without recreating the resource.

If strict data isolation is required between Speech and Language scenarios, create separate Foundry resources with different storage accounts.

> [!IMPORTANT]
> If you delete or move (change resource ID of) the storage account bound by `userOwnedStorage`, Speech and Language stop functioning. Consider attempting account recovery first: [Recover a storage account](/azure/storage/common/storage-account-recover). Otherwise you must recreate the Foundry resource.

## Create a storage connection

::: moniker range="foundry-classic"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Select your project.
1. In the left pane, select **Connections** (or **Connected resources**).
1. Select **+ New connection**.
1. Choose **Azure Blob Storage**.
1. Provide:
   - Name
   - Subscription
   - Storage account
   - Authentication method (system-assigned managed identity recommended)
1. Select **Create**.

The connection is now available to Agents (when not overridden), Evaluations, Datasets, Content Understanding, Speech, and Language.

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. In the upper right, select **Build**.
1. In the left pane, select **Tools** and then **Connect a tool** in the upper right of the pane.
1. In the **Select a tool** dialog, select the **Catalog** tab and find **Azure Blob Storage**.
1. Select **Create**.

::: moniker-end

> [!NOTE]
> Azure portal (portal.azure.com) steps are version-agnostic and intentionally not wrapped in moniker blocks.

## Configure capability host for Agents (combined resource + project steps)

You create two capability hosts—one at the resource level and one at the project level—each referencing the same connection chain so Agents route to your storage.

1. Create a resource-level connection (as above) if not already present.
   > [!NOTE]
   > As described in the previous section, select the **Catalog** tab and look for **Azure Blob Storage**.
1. Create a resource-level capability host referencing that connection.
1. Create (or open) a project under the resource.
1. Create a project-level capability host referencing the resource-level capability host.
1. Verify Agents data now writes to the bound storage account.

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

1. Use the [Azure CLI](/cli/azure/ml/capability-host) or [Azure REST API](/rest/api/azureml/capability-hosts/create-or-update) sample to create a resource-level capability host.

1. Reference your previously created storage connection in the capability host configuration.

1. Set the capability type to support agents.

### Create project-level capability host

After creating your Foundry project:

1. Create a project-level capability host that references the resource-level capability host.

1. Configure the capability host to enable agents functionality.

1. Verify the capability host is properly linked to your storage connection as demonstrated in this [code sample for Standard agent setup](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/41-standard-agent-setup).

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

Create the role assignment on the Azure Storage account for the Foundry resource managed identity, not the project managed identity. Assign `Storage Blob Data Contributor`.


::: moniker range="foundry-classic"
## Configure Content Understanding

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
1. Open the resource.
1. In the left pane, select **Content Understanding**.
1. Choose the existing storage connection.

> [!NOTE]
> Programmatic configuration options for Content Understanding are under evaluation.
::: moniker-end

::: moniker range="foundry"

::: moniker-end

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
- [Infrastructure setup samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples)
- [Connect storage for Speech/Language](../../ai-services/speech-service/bring-your-own-storage-speech-resource.md?tabs=portal)
