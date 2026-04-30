---
title: "Configure Agent 365 data collection for Microsoft Foundry"
description: "Learn how to enable or disable Microsoft Agent 365 data collection on a Foundry resource, and how to enforce settings across a subscription with Azure Policy."
author: deeikele
ms.author: deeikele
ms.reviewer: jburchel
ms.date: 03/19/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
#CustomerIntent: As an IT admin, I want to control whether Foundry agent data is sent to Agent 365 so that I can meet my organization's data governance and residency requirements.
---

# Configure Agent 365 data collection for Microsoft Foundry

When Microsoft Agent 365 (A365) is enabled for your organization, Foundry resources can send agent activity data to the Agent 365 control plane. This data powers agent registry, analytics, and security features in Agent 365. For an overview of how Foundry integrates with Agent 365 and how data flows between the two platforms, see [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md).

This article explains how the enablement model works, how to opt out an individual Foundry resource, and how to use Azure Policy to enforce a consistent configuration across an Azure subscription.

## Prerequisites

- An Azure subscription with at least one Foundry resource (`Microsoft.CognitiveServices/accounts`).
- **Owner** or **Contributor** role on the Foundry resource (to modify resource properties).
- For the Azure Policy section: permissions to create and assign policy definitions at the subscription or management-group scope.

## Understand the enablement model

Agent 365 data collection on a Foundry resource is tracked by two properties in the resource provider configuration:

| Property | Type | Description |
|---|---|---|
| `a365LoggingEnabled` | Boolean | User-controlled property to set whether agent activity data is sent to Agent 365 for this Foundry resource. Accepted values: `true`, `false`. |
| `a365Status` | String | Read-only system property showing enablement status after licensing and consent checks. Possible values: `Enabled`, `Disabled`, `NotLicensed`. |

These properties are part of the `Microsoft.CognitiveServices/accounts` resource type and can be read or modified through the Azure Resource Manager API, Azure CLI, Azure PowerShell, or the Azure portal.

> [!IMPORTANT]
> Data collection requires **both** an active Agent 365 license **and**
> tenant-level A365 consent **and** `a365LoggingEnabled` set to `true`.
> No data is ingested unless the customer has completed the Agent 365
> consent flow and holds a valid license. Setting `a365LoggingEnabled`
> to `true` alone doesn't trigger data collection.

### Default state

When Agent 365 is enabled for an Entra tenant, Foundry resources in the
same Azure tenant have `a365LoggingEnabled` set to `true` by default.
Organizations must explicitly opt out to disable data collection on each
resource. You can use Azure Policy to deny data collection for select Azure
subscriptions or Azure management groups.

### Scope of the setting

The `a365LoggingEnabled` setting applies at the **Foundry resource level**.
Every Foundry project and every prompt agent contained within that resource
inherits the same data-collection setting. There's no per-project or
per-agent override.

[Hosted Agents](./deploy-hosted-agent.md) require manual configuration of Agent 365 by packing and configuring the Agent 365 SDK along with your agent code. Without manual configuration steps, data will not flow. Explicit Agent 365 SDK configurations in hosted agents override logging disablement settings on the Foundry resource level.

## Disable data collection on a Foundry resource

To stop sending agent activity data from a specific Foundry resource to
Agent 365, set `a365LoggingEnabled` to `false`.

### [Azure CLI](#tab/azure-cli)

```azurecli
az resource update \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --resource-type Microsoft.CognitiveServices/accounts \
  --api-version 2026-03-15-preview \
  --set properties.a365LoggingEnabled=false
```

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
$resource = Get-AzResource `
  -ResourceGroupName <resource-group> `
  -ResourceName <foundry-resource-name> `
  -ResourceType Microsoft.CognitiveServices/accounts `
  -ApiVersion 2026-03-15-preview

$resource.Properties.a365LoggingEnabled = false

Set-AzResource -ResourceId $resource.ResourceId `
  -ApiVersion 2026-03-15-preview `
  -Properties $resource.Properties -Force
```

### [REST API](#tab/rest-api)

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{accountName}?api-version=2026-03-15-preview

{
  "properties": {
    "a365LoggingEnabled": false
  }
}
```

### [Bicep](#tab/bicep)

```bicep
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2026-03-15-preview' = {
  name: '<foundry-resource-name>'
  location: '<location>'
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    a365LoggingEnabled: false
  }
}
```

### [Terraform (AzAPI)](#tab/azapi)

```hcl
resource "azapi_update_resource" "disable_agent365" {
  type        = "Microsoft.CognitiveServices/accounts@2026-03-15-preview"
  resource_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"

  body = {
    properties = {
      a365LoggingEnabled = false
    }
  }
}
```

---

After you disable logging, the setting takes effect for all projects and agents within that Foundry resource. No agent activity data is sent to Agent 365 from that resource going forward.

## Enable data collection on a Foundry resource

To opt a resource back in, set `a365LoggingEnabled` to `true`.

### [Azure CLI](#tab/azure-cli)

```azurecli
az resource update \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --resource-type Microsoft.CognitiveServices/accounts \
  --api-version 2026-03-15-preview \
  --set properties.a365LoggingEnabled=true
```

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
$resource = Get-AzResource `
  -ResourceGroupName <resource-group> `
  -ResourceName <foundry-resource-name> `
  -ResourceType Microsoft.CognitiveServices/accounts `
  -ApiVersion 2026-03-15-preview

$resource.Properties.a365LoggingEnabled = true

Set-AzResource -ResourceId $resource.ResourceId `
  -ApiVersion 2026-03-15-preview `
  -Properties $resource.Properties -Force
```

### [REST API](#tab/rest-api)

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{accountName}?api-version=2026-03-15-preview

{
  "properties": {
    "a365LoggingEnabled": true
  }
}
```

### [Bicep](#tab/bicep)

```bicep
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2026-03-15-preview' = {
  name: '<foundry-resource-name>'
  location: '<location>'
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    a365LoggingEnabled: true
  }
}
```

### [Terraform (AzAPI)](#tab/azapi)

```hcl
resource "azapi_update_resource" "enable_agent365" {
  type        = "Microsoft.CognitiveServices/accounts@2026-03-15-preview"
  resource_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"

  body = {
    properties = {
      a365LoggingEnabled = true
    }
  }
}
```

---

## Related content

- [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md)
- [Publish an agent as a digital worker in Agent 365](agent-365.md)
- [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md)
- [Agent 365 overview](/microsoft-agent-365/overview)
