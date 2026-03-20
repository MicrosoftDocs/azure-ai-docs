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

When Microsoft Agent 365 (A365) is enabled for your organization, Foundry resources can send agent activity data to the Agent 365 control plane. This data powers agent registry, analytics, and security features in Agent 365.

This article explains how the enablement model works, how to opt out an individual Foundry resource, and how to use Azure Policy to enforce a consistent configuration across an Azure subscription.

## Prerequisites

- An Azure subscription with at least one Foundry resource (`Microsoft.CognitiveServices/accounts`).
- **Owner** or **Contributor** role on the Foundry resource (to modify resource properties).
- For the Azure Policy section: permissions to create and assign policy definitions at the subscription or management-group scope.

## Understand the enablement model

Agent 365 data collection on a Foundry resource is controlled by two properties in the resource provider configuration:

| Property | Type | Description |
|---|---|---|
| `agent365Config.ingestionEndpoint` | String | The Agent 365 ingestion endpoint for the tenant, in the format `<entra-tenant-id>.agent365.com`. |
| `agent365Config.loggingEnabled` | String | Controls whether agent activity data is sent to Agent 365. Accepted values: `enabled`, `disabled`. |

These properties are part of the `Microsoft.CognitiveServices/accounts` resource type and can be read or modified through the Azure Resource Manager API, Azure CLI, Azure PowerShell, or the Azure portal.

> [!IMPORTANT]
> Data collection requires **both** an active Agent 365 license **and** tenant-level A365 consen **and** `loggingEnabled` set to `enabled`. No data is ingested unless the customer has completed the Agent 365 consent flow and holds a valid license. Setting the property to `enabled` alone doesn't trigger data collection.

### Default state

When Agent 365 is enabled for a tenant, Foundry resources have `loggingEnabled` set to `disabled` by default. Organizations must explicitly opt in to data collection on each resource, or use an Azure Policy to enable it at scale.

### Scope of the setting

The `agent365Config` setting applies at the **Foundry resource level**. Every Foundry project and every agent contained within that resource inherits the same data-collection setting. There's no per-project or per-agent override.

## Disable data collection on a Foundry resource

To stop sending agent activity data from a specific Foundry resource to Agent 365, set `loggingEnabled` to `disabled`.

### [Azure CLI](#tab/azure-cli)

```azurecli
az resource update \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --resource-type Microsoft.CognitiveServices/accounts \
  --set properties.agent365Config.loggingEnabled=disabled
```

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
$resource = Get-AzResource `
  -ResourceGroupName <resource-group> `
  -ResourceName <foundry-resource-name> `
  -ResourceType Microsoft.CognitiveServices/accounts

$resource.Properties.agent365Config.loggingEnabled = "disabled"

Set-AzResource -ResourceId $resource.ResourceId `
  -Properties $resource.Properties -Force
```

### [REST API](#tab/rest-api)

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{accountName}?api-version=2024-10-01

{
  "properties": {
    "agent365Config": {
      "loggingEnabled": "disabled"
    }
  }
}
```

### [Bicep](#tab/bicep)

```bicep
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '<foundry-resource-name>'
  location: '<location>'
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    agent365Config: {
      loggingEnabled: 'disabled'
    }
  }
}
```

### [Terraform (AzAPI)](#tab/azapi)

```hcl
resource "azapi_update_resource" "disable_agent365" {
  type        = "Microsoft.CognitiveServices/accounts@2024-10-01"
  resource_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"

  body = {
    properties = {
      agent365Config = {
        loggingEnabled = "disabled"
      }
    }
  }
}
```

---

After you disable logging, the setting takes effect for all projects and agents within that Foundry resource. No agent activity data is sent to Agent 365 from that resource going forward.

## Enable data collection on a Foundry resource

To opt a resource back in, set `loggingEnabled` to `enabled` and provide the ingestion endpoint for your tenant.

### [Azure CLI](#tab/azure-cli)

```azurecli
az resource update \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --resource-type Microsoft.CognitiveServices/accounts \
  --set properties.agent365Config.ingestionEndpoint="<entra-tenant-id>.agent365.com" \
  --set properties.agent365Config.loggingEnabled=enabled
```

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
$resource = Get-AzResource `
  -ResourceGroupName <resource-group> `
  -ResourceName <foundry-resource-name> `
  -ResourceType Microsoft.CognitiveServices/accounts

$resource.Properties.agent365Config.ingestionEndpoint = "<entra-tenant-id>.agent365.com"
$resource.Properties.agent365Config.loggingEnabled = "enabled"

Set-AzResource -ResourceId $resource.ResourceId `
  -Properties $resource.Properties -Force
```

### [REST API](#tab/rest-api)

```http
PATCH https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.CognitiveServices/accounts/{accountName}?api-version=2024-10-01

{
  "properties": {
    "agent365Config": {
      "ingestionEndpoint": "<entra-tenant-id>.agent365.com",
      "loggingEnabled": "enabled"
    }
  }
}
```

### [Bicep](#tab/bicep)

```bicep
resource foundryAccount 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '<foundry-resource-name>'
  location: '<location>'
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    agent365Config: {
      ingestionEndpoint: '<entra-tenant-id>.agent365.com'
      loggingEnabled: 'enabled'
    }
  }
}
```

### [Terraform (AzAPI)](#tab/azapi)

```hcl
resource "azapi_update_resource" "enable_agent365" {
  type        = "Microsoft.CognitiveServices/accounts@2024-10-01"
  resource_id = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"

  body = {
    properties = {
      agent365Config = {
        ingestionEndpoint = "<entra-tenant-id>.agent365.com"
        loggingEnabled    = "enabled"
      }
    }
  }
}
```

---

## Enforce data collection settings with Azure Policy

You can use an Azure Policy with a `modify` effect to automatically configure Agent 365 data collection on every Foundry resource in a subscription or management group. This approach is useful when you want to ensure that all Foundry resources conform to a single data-collection posture.

The following custom policy definition sets the ingestion endpoint and logging state on every `Microsoft.CognitiveServices/accounts` resource.

### Create the policy definition

Save the following JSON as a file (for example, `agent365-policy.json`):

```json
{
  "properties": {
    "displayName": "Configure Agent 365 data collection for Foundry resources",
    "description": "Automatically configures the Agent 365 ingestion endpoint and logging setting on all Microsoft.CognitiveServices/accounts resources.",
    "policyType": "Custom",
    "mode": "Indexed",
    "parameters": {
      "agents365IngestionEndpoint": {
        "type": "String",
        "metadata": {
          "displayName": "Agent 365 ingestion endpoint",
          "description": "The Agent 365 ingestion endpoint for your tenant, for example '<entra-tenant-id>.agent365.com'."
        }
      },
      "loggingEnabled": {
        "type": "String",
        "metadata": {
          "displayName": "Enable Agent 365 logging",
          "description": "Set to 'enabled' to send agent activity data to Agent 365, or 'disabled' to stop data collection."
        },
        "allowedValues": [
          "enabled",
          "disabled"
        ],
        "defaultValue": "disabled"
      }
    },
    "policyRule": {
      "if": {
        "field": "type",
        "equals": "Microsoft.CognitiveServices/accounts"
      },
      "then": {
        "effect": "modify",
        "details": {
          "roleDefinitionIds": [
            "/providers/Microsoft.Authorization/roleDefinitions/b24988ac-6180-42a0-ab88-20f7382dd24c"
          ],
          "operations": [
            {
              "operation": "addOrReplace",
              "field": "properties.agent365Config.ingestionEndpoint",
              "value": "[parameters('agents365IngestionEndpoint')]"
            },
            {
              "operation": "addOrReplace",
              "field": "properties.agent365Config.loggingEnabled",
              "value": "[parameters('loggingEnabled')]"
            }
          ]
        }
      }
    }
  }
}
```

> [!NOTE]
> The policy uses the **Contributor** built-in role (`b24988ac-…-20f7382dd24c`) to perform the `modify` operation. The managed identity created during policy assignment needs this role on the target scope.

### Deploy the policy

### [Azure CLI](#tab/azure-cli)

```azurecli
# Create the policy definition
az policy definition create \
  --name "configure-agent365-foundry" \
  --display-name "Configure Agent 365 data collection for Foundry resources" \
  --rules agent365-policy.json \
  --mode Indexed

# Assign the policy to a subscription
az policy assignment create \
  --name "agent365-foundry-assignment" \
  --policy "configure-agent365-foundry" \
  --scope "/subscriptions/<subscription-id>" \
  --mi-system-assigned \
  --location <location> \
  --params '{ "agents365IngestionEndpoint": { "value": "<entra-tenant-id>.agent365.com" }, "loggingEnabled": { "value": "disabled" } }'
```

### [Azure PowerShell](#tab/azure-powershell)

```azurepowershell
# Create the policy definition
$definition = New-AzPolicyDefinition `
  -Name "configure-agent365-foundry" `
  -DisplayName "Configure Agent 365 data collection for Foundry resources" `
  -Policy "agent365-policy.json" `
  -Mode Indexed

# Assign the policy to a subscription
New-AzPolicyAssignment `
  -Name "agent365-foundry-assignment" `
  -PolicyDefinition $definition `
  -Scope "/subscriptions/<subscription-id>" `
  -Location <location> `
  -IdentityType SystemAssigned `
  -PolicyParameterObject @{
    agents365IngestionEndpoint = "<entra-tenant-id>.agent365.com"
    loggingEnabled            = "disabled"
  }
```

---

After assignment, the policy evaluates existing resources and remediates them during the next compliance evaluation cycle. New Foundry resources automatically receive the configured settings at creation time.

To disable data collection across all Foundry resources in the subscription, set the `loggingEnabled` parameter to `disabled` in the policy assignment. To enable it, set the parameter to `enabled`.

## Verify data collection status

To confirm the current Agent 365 data-collection configuration on a Foundry resource:

```azurecli
az resource show \
  --resource-group <resource-group> \
  --name <foundry-resource-name> \
  --resource-type Microsoft.CognitiveServices/accounts \
  --query properties.agent365Config
```

The output shows the current `ingestionEndpoint` and `loggingEnabled` values.

## Related content

- [Microsoft Agent 365 integration with Foundry](../concepts/agent-365-integration.md)
- [Publish an agent as a digital worker in Agent 365](agent-365.md)
- [Agent identity concepts in Microsoft Foundry](../concepts/agent-identity.md)
- [Agent 365 overview](/microsoft-agent-365/overview)
