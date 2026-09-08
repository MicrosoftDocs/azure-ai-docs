---
title: Manage automatic upgrades from Azure OpenAI to Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Check whether an Azure OpenAI resource is scheduled for automatic upgrade to Microsoft Foundry, opt out, and prepare for rollback.
ms.author: deeikele
author: deeikele
ms.reviewer: sdgilley
ms.date: 08/19/2026
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: how-to
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Manage automatic upgrades from Azure OpenAI to Microsoft Foundry

Microsoft automatically upgrades eligible Azure OpenAI resources to Microsoft Foundry resources. In this article, you check whether a resource is scheduled for automatic upgrade, defer or opt out of the upgrade, and prepare for rollback.

The backend upgrade expands access to models and Foundry capabilities, including [Foundry Agent Service](../agents/overview.md), [evaluations](evaluate-generative-ai-app.md), and [fine-tuning](../openai/how-to/fine-tuning.md). You don't pay more for existing Azure OpenAI functionality after the upgrade. New Foundry capabilities that you use might have separate pricing. Your resource keeps its name, managed identity, endpoint, keys, security settings, permissions, Azure OpenAI v1 endpoint access, fine-tuning jobs, batches, and stored completions.

If your Azure OpenAI resource isn't eligible for auto-upgrade, you can still start the upgrade yourself by using the [opt-in process](upgrade-azure-openai.md).

## Prerequisites

- An existing Azure OpenAI resource.
- Permission to read the resource and its Azure Resource Manager JSON.
- A role that includes `Microsoft.CognitiveServices/accounts/write` if you plan to opt out. Assign permissions at the narrowest scope that meets your needs.
- Your existing Bicep or Terraform configuration if you plan to opt out by using infrastructure as code. Don't deploy the examples in this article as standalone resource definitions.
- Azure CLI 2.14.0 or later with Bicep installed, permission to validate deployments, and permission to update the existing account for the Bicep approach.
- Terraform with the Azure AzAPI provider configured for the target subscription and the existing Azure OpenAI resource ID for the Terraform approach.
- API version `2026-01-15-preview` when you inspect or update the `foundryAutoUpgrade` property. This API version and property are in preview.

## Review auto-upgrade status

Resources selected for auto-upgrade show a notice in the Azure portal. They also include a `foundryAutoUpgrade` block in their Azure Resource Manager resource properties. Resources that aren't yet selected show no such notice or property.

### Check status in the Azure portal

To check whether your resource is selected:

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. Open your Azure OpenAI resource.
1. Select **Resource upgrade** in the left-side navigation.

### Inspect the resource JSON

To inspect the resource properties:

1. Open the **Overview** page.
1. Open **JSON view**.
1. Select API version `2026-01-15-preview`.

A resource scheduled for auto-upgrade shows the following block in its JSON properties:

```json
"foundryAutoUpgrade": {
  "mode": "Enabled",
  "plannedByMicrosoft": true,
  "scheduledAt": "2026-04-15T00:00:00Z",
  "statusReason": "<service-provided-status>"
}
```

Reference: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/2026-01-15-preview/accounts)

The public API contract doesn't enumerate `statusReason` values. Use the **Resource upgrade** page to interpret the current state. Don't build automation that depends on a specific `statusReason` value.

If the response doesn't contain `foundryAutoUpgrade`, it doesn't provide an automatic-upgrade schedule. The public API contract doesn't define property absence as a conclusive selection state, so don't use absence as the sole signal in automation.

## Defer or opt out of automatic upgrade

If your resource is selected for automatic upgrade, use the Azure portal to defer the upgrade or set `foundryAutoUpgrade.mode` to `Disabled` in your existing deployment definition. The public API contract describes `Disabled` as opting out of automatic upgrade.

Use the Azure portal to defer a scheduled upgrade. Use Bicep or Terraform to opt out by setting `foundryAutoUpgrade.mode` to `Disabled` in your existing deployment definition.

# [Azure portal](#tab/azportal-opt-out)

1. Sign in to the [Azure portal](https://portal.azure.com/).
1. Open your Azure OpenAI resource.
1. Select **Resource upgrade**.
1. Select **Defer upgrade**.
1. Return to **Resource upgrade** and verify that the page reflects your change.

# [Azure Bicep](#tab/bicep-opt-out)

Add the `foundryAutoUpgrade` block to your existing Bicep resource definition. Keep all other properties unchanged.

```bicep
// Add this object to the existing properties block.
foundryAutoUpgrade: {
  mode: 'Disabled'
}
```

Reference: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/2026-01-15-preview/accounts)

Preview the deployment before you apply it. Replace the placeholders with the values for your existing deployment.

```azurecli
az deployment group what-if --resource-group <resource-group> --template-file <template-file> --parameters @<parameters-file>
```

Reference: [Preview Azure deployment changes](/azure/azure-resource-manager/templates/deploy-what-if)

> [!NOTE]
> ARM what-if can report changes to server-defaulted properties. Compare unexpected results with the current resource JSON, and don't treat what-if output as a guarantee of final service behavior.

Confirm that the preview updates the existing account and doesn't replace or delete it. Then deploy the template by using your existing deployment process. After the deployment completes, inspect the resource JSON and verify that `foundryAutoUpgrade.mode` is `Disabled`.

# [Terraform with AzAPI](#tab/terraform-opt-out)

The AzureRM `azurerm_cognitive_account` resource doesn't expose the preview `foundryAutoUpgrade` property. Use AzAPI to update that property on your existing account.

```terraform
# Accept the existing Azure OpenAI resource ID.
variable "azure_openai_resource_id" {
  type = string
}

# Disable automatic upgrade on the existing resource.
resource "azapi_update_resource" "disable_foundry_auto_upgrade" {
  type        = "Microsoft.CognitiveServices/accounts@2026-01-15-preview"
  resource_id = var.azure_openai_resource_id

  body = {
    properties = {
      foundryAutoUpgrade = {
        mode = "Disabled"
      }
    }
  }
}
```

Reference: [AzAPI update resource](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/update_resource)

Run `terraform plan -out=tfplan`. Confirm that the plan updates the existing account and doesn't replace or delete it. Then run `terraform apply tfplan`. After the apply operation completes, inspect the resource JSON and verify that `foundryAutoUpgrade.mode` is `Disabled`.

---

## Check eligibility and upgrade constraints

Auto-upgrade rolls out in stages based on technical readiness and observed usage patterns. This staged approach helps ensure a predictable, low-disruption experience as support expands.

Review these constraints before you upgrade:

- Resources that use private networking or customer-managed key (CMK) encryption aren't selected at first. Review the [manual upgrade requirements](upgrade-azure-openai.md) before manually upgrading one of these resources.
- Foundry doesn't support a Weights & Biases integration.
- Private network setups require DNS resolution for the `<custom-domain>.openai.azure.com`, `<custom-domain>.services.ai.azure.com`, and `<custom-domain>.cognitiveservices.azure.com` FQDNs. Update the private endpoint's IP configurations, or delete and re-create the private endpoint.

For details, see [Upgrade from Azure OpenAI to Microsoft Foundry](upgrade-azure-openai.md).

## Roll back an auto-upgraded resource

If your resource was auto-upgraded and you need to return to Azure OpenAI, follow the rollback steps in [Upgrade from Azure OpenAI to Microsoft Foundry](upgrade-azure-openai.md). Before you roll back, delete any Foundry-specific sub-resources that prevent rollback, such as projects, connections, and non-Azure OpenAI model deployments. Also confirm that your subscription has capacity below the limit of 30 Azure OpenAI resources in the target region.

After rollback, verify that the resource is shown as Azure OpenAI and that its existing endpoint, deployments, networking settings, and identity configuration remain available.

## Troubleshoot automatic upgrade

| Issue | Resolution |
| --- | --- |
| **Resource upgrade** and `foundryAutoUpgrade` aren't present | The resource isn't currently selected. Use the [opt-in upgrade process](upgrade-azure-openai.md) if you need to upgrade now. |
| You can't opt out | Confirm that your role includes `Microsoft.CognitiveServices/accounts/write` on the resource. |
| A Bicep or Terraform plan replaces the resource | Stop the deployment. Confirm that you are updating the existing resource definition and preserving its current properties. |
| Azure CLI can't produce a what-if result | Confirm that Azure CLI 2.14.0 or later and Bicep are installed and that your identity has deployment-validation and resource-write permissions. |
| Terraform can't initialize or resolve `azapi_update_resource` | Confirm that Terraform and the Azure AzAPI provider are configured for the target subscription, initialize the working directory, and verify that `azure_openai_resource_id` contains the existing account ID. |
| A private network blocks upgrade | Follow the private network steps in [Upgrade from Azure OpenAI to Microsoft Foundry](upgrade-azure-openai.md) before you manually upgrade. |
| Customer-managed keys block upgrade | Review the customer-managed key requirements in [Upgrade from Azure OpenAI to Microsoft Foundry](upgrade-azure-openai.md). |
| A Weights & Biases integration blocks upgrade | Remove or replace the integration before you upgrade. Foundry resources don't support this integration. |
| Upgrade exceeds the regional resource limit | Confirm that the subscription has fewer than 100 `AIServices` resources in the target region. |
| Rollback exceeds the regional resource limit | Confirm that the subscription has fewer than 30 Azure OpenAI resources in the target region. |

## Review Foundry governance and security guidance

If your organization needs more time to complete security reviews or update governance controls, complete these actions before your scheduled upgrade date:

1. Review existing Azure RBAC assignments and Azure Policy controls. Azure OpenAI and Microsoft Foundry resources use the same Azure resource type and management APIs, so these controls continue to apply after upgrade.
1. Identify broad permissions that also apply to the expanded Foundry model set.
1. Use Azure Policy to constrain which models teams can deploy. For details, see [Built-in policy for model deployment](model-deployment-policy.md).
1. Approve Foundry capabilities in phases, such as non-OpenAI models, Agent Service, and Foundry Tools.
1. For teams that need only Azure OpenAI data actions, use **Cognitive Services OpenAI User**. For Foundry project development, use **Foundry User** or **Foundry Owner**, as appropriate. Use a custom role when the built-in roles grant broader access than the team requires.

[!INCLUDE [role-rename-note](../includes/role-rename-note.md)]

For more upgrade-specific guidance, see [Considerations for RBAC and policy during upgrade](upgrade-azure-openai.md#considerations-for-rbac-and-policy-during-upgrade). For broader security and governance guidance, see [Manage compliance and security in Microsoft Foundry](../control-plane/how-to-manage-compliance-security.md).

## Related content

- [Upgrade from Azure OpenAI to Microsoft Foundry (opt-in)](upgrade-azure-openai.md)
- [`Microsoft.CognitiveServices/accounts` template reference](/azure/templates/microsoft.cognitiveservices/2026-01-15-preview/accounts)
- [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md)