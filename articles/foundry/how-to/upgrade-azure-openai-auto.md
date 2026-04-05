---
title: Auto-upgrade of Azure OpenAI resources to Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how auto-upgrade from Azure OpenAI to Microsoft Foundry works for eligible resources, including status codes, defer options, and rollback.
ms.author: deeikele
author: deeikele
ms.reviewer: sdgilley
ms.date: 03/13/2026
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Auto-upgrade Azure OpenAI resources to Microsoft Foundry

Microsoft is automatically upgrading eligible Azure OpenAI resources to Microsoft Foundry resources. This service backend upgrade gives you access to a broader set of models, [Foundry Agent Service](../agents/overview.md), [Evaluations](evaluate-generative-ai-app.md), [Fine-Tuning](../openai/how-to/fine-tuning.md) availability with more models, and deeper integration across the Microsoft ecosystem.

Upgrading doesn't increase your costs. Your Azure resource name, managed identity, endpoint, keys, and existing settings and state remain the same, including security configurations and permissions, Azure OpenAI v1 endpoint access and API keys, and existing fine-tuning jobs, batches, stored completions, and files.

Auto-upgrade applies only to eligible resources. If your resource is selected, your subscription owner receives advance notice and can review your scheduled date, defer the upgrade, or roll back after the upgrade completes.

If your Azure OpenAI resource isn't eligible for auto-upgrade, you can still start the upgrade yourself by using the [opt-in process](upgrade-azure-openai.md).

## Review auto-upgrade status

Resources selected for auto-upgrade show a notice in the Azure portal.
They also include a `foundryAutoUpgrade` block in their Azure Resource
Manager resource properties. Resources that aren't yet selected show no
such notice or property.

To check whether your resource is selected:

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. Open your Azure OpenAI resource.
1. Select **Resource upgrade** in the left-side navigation.

You can also inspect the resource JSON:

1. Open the **Overview** page.
1. Open **JSON view**.
1. Select API version `2026-01-15-preview`.

A resource scheduled for auto-upgrade shows the following block in its
JSON properties:

```json
"foundryAutoUpgrade": {
  "mode": "Enabled",
  "scheduledAt": "2026-04-15T00:00:00Z",
  "status": "Eligible"
}
```

If you see only the opt-in upgrade experience and no auto-upgrade notice
or `foundryAutoUpgrade` property, your resource isn't yet selected for
auto-upgrade.

## Understand eligibility and status codes

Auto-upgrade is rolled out in stages based on technical readiness and
observed usage patterns. This staged approach helps ensure a predictable,
low-disruption experience as support expands.

Resources that use Azure security configurations, such as private
networking or customer-managed key (CMK) encryption, aren't selected at
first. As zero-touch support for these configurations becomes available,
those resources can be selected later.

If your resource uses security features and is selected in a later wave,
you still receive advance notice before the scheduled upgrade date so you
have time to review and adapt governance controls.

If your resource doesn't show the `foundryAutoUpgrade` block, it isn't
currently selected for auto-upgrade. If the block is present, use the
following status codes to understand your upgrade state.

| Status | Meaning |
|---|---|
| `Eligible` | Your resource is scheduled for auto-upgrade on the date in `scheduledAt`. |
| `Completed` | Auto-upgrade completed successfully. Your resource is now a Foundry resource, and `scheduledAt` is `null`. |
| `DeferredByCustomer` | You deferred auto-upgrade. `scheduledAt` is `null`. |
| `RolledBack` | The resource was upgraded to Foundry and then rolled back to Azure OpenAI. `scheduledAt` is `null`. |
| `Failed: CustomerManagedKeys` | The resource isn't currently eligible for auto-upgrade because it uses customer-managed keys and isn't in an [allow-listed subscription](upgrade-azure-openai.md#limitations). |
| `Failed: PrivateNetworking` | The resource isn't yet eligible for auto-upgrade because it uses private networking. Manually upgrade to configure two additionally required DNS zones.|
| `Failed: WeightsAndBiases` | The resource isn't eligible for auto-upgrade because it has a Weights & Biases (W&B) integration. W&B isn't supported on a Foundry resource. |

When `status` starts with `Failed`, the value identifies why the resource isn't yet eligible for auto-upgrade. Once support is available for that configuration, the resource can return to `Eligible` with a new scheduled date.

## Defer auto-upgrade

If your resource is selected for auto-upgrade, you can defer it in Azure
portal or by updating your existing deployment template.

# [Azure portal](#tab/azportal-defer)

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. Open your Azure OpenAI resource.
1. Select **Resource upgrade**.
1. Select **Defer upgrade**.

# [Azure Bicep](#tab/bicep-defer)

Add the `foundryAutoUpgrade` block to your existing Bicep resource
definition and redeploy. Keep your existing properties unchanged.

```bicep
resource account 'Microsoft.CognitiveServices/accounts@2026-01-15-preview' = {
  name: accountName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  // ... keep your existing resource configuration
  properties: {
    // ... keep your existing properties
    foundryAutoUpgrade: {
      mode: 'Deferred'
    }
  }
}
```

Run the updated template using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli)
or your [Visual Studio Code extension for
Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep).

**References**: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/accounts),
[Bicep CLI documentation](/azure/azure-resource-manager/bicep/bicep-cli)

# [Terraform](#tab/terraform-defer)

Update your existing AzureRM or AzAPI resource definition to include
`foundryAutoUpgrade.mode = "Deferred"`, then run `terraform apply`.

> [!IMPORTANT]
> When using the [AzureRM resource provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account.html), ensure you use a version greater than 4.57.0 of your Terraform CLI client for a non-destructive resource update.

---

## Roll back an auto-upgraded resource

If your resource was auto-upgraded and you need to return to Azure
OpenAI, follow the rollback steps in [Upgrade from Azure OpenAI to
Microsoft Foundry](upgrade-azure-openai.md#roll-back-to-azure-openai).
Before you roll back, delete any Foundry-specific sub-resources that
prevent rollback, such as projects, connections, and non-Azure OpenAI
model deployments.

## Review Foundry governance and security guidance

If your organization needs more time to complete security reviews or
update governance controls, use these guidelines before your scheduled
upgrade date:

- Microsoft Foundry provides a broader set of capabilities than Azure
  OpenAI, and both resource variants use the same Azure resource type
  and management APIs. Existing Azure RBAC assignments and Azure Policy
  controls continue to apply after upgrade.
- Broad Azure RBAC permissions that supported OpenAI model operations will also apply to the broader model set after the upgrade. To constrain model access, use Azure Policy for model deployment governance. For details, see
  [Built-in policy for model deployment](model-deployment-policy.md).
- Consider approving Foundry capabilities in phases, for example, broader non-OpenAI model access first, then Agent service, then Foundry tools. Use narrower built-in roles (for example 'Cognitive Services OpenAI User') or custom roles to grant only the access each team
  needs. For role guidance, see [Role-based access control for Microsoft
  Foundry](../concepts/rbac-foundry.md).

For more upgrade-specific guidance, see [Considerations for RBAC and
policy during
upgrade](upgrade-azure-openai.md#considerations-for-rbac-and-policy-during-upgrade).
For broader security and governance guidance, see [Manage compliance and
security in Microsoft
Foundry](../control-plane/how-to-manage-compliance-security.md).

## Related content

- [Upgrade from Azure OpenAI to Microsoft Foundry (opt-in)](upgrade-azure-openai.md)