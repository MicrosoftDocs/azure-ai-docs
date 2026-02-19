---
title: Control model deployment with custom policies
titleSuffix: Microsoft Foundry
description: "Learn how to use custom Azure Policies to control Microsoft Foundry and Azure OpenAI in Foundry Models deployment with Microsoft Foundry."
manager: mcleans
ms.service: azure-ai-foundry
ms.topic: how-to #Don't change
ms.date: 01/05/2026
ms.author: jburchel 
author: jonburchel 
ms.reviewer: aashishb
reviewer: aashishb_microsoft
ms.custom: [dev-focus]
ai-usage: ai-assisted
---

# Control model deployment with custom policies

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

When you deploy models in Microsoft Foundry or Azure OpenAI, you might need Azure Policy to control which [deployment types](../concepts/deployment-types.md) are available to users or which specific models they can deploy. This article shows you how to create a custom Azure Policy definition that denies non-approved model deployments.

> [!TIP]
> The steps in this article apply to both a [!INCLUDE [fdp](../../includes/fdp-project-name.md)] and [!INCLUDE [hub](../../includes/hub-project-name.md)].

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.
- Familiarity with Azure Policy.

## Policy rule examples

Use one of the following examples as the starting point for your policy definition. Paste this JSON into the **Policy rule** editor when you create the policy definition.

# [Enforce specific models](#tab/models)

Use this policy to control which specific models and versions are available for deployment.

```json
{
  "mode": "All",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.CognitiveServices/accounts/deployments"
        },
        {
          "not": {
            "value": "[concat(field('Microsoft.CognitiveServices/accounts/deployments/model.name'), ',', field('Microsoft.CognitiveServices/accounts/deployments/model.version'))]",
            "in": "[parameters('allowedModels')]"
          }
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  },
  "parameters": {
    "allowedModels": {
      "type": "Array",
      "metadata": {
        "displayName": "Allowed AI models",
        "description": "The list of allowed models to be deployed."
      }
    }
  }
}
```

This policy denies deployment creation or updates when the model name and version aren't included in the `allowedModels` parameter.

References:
- Reference: [Azure Policy definition structure basics](/azure/governance/policy/concepts/definition-structure-basics)
- Reference: [Azure Policy definition structure policy rule](/azure/governance/policy/concepts/definition-structure-policy-rule)
- Reference: [Azure Policy definition structure aliases](/azure/governance/policy/concepts/definition-structure-alias)
- Reference: [Azure Policy definitions deny effect](/azure/governance/policy/concepts/effect-deny)
- Reference: [Azure Policy definition schema](https://schema.management.azure.com/schemas/2020-10-01/policyDefinition.json)

# [Enforce specific deployment types](#tab/deployments)

Use this policy to control which deployment types are allowed. For example, you can prevent developers from creating deployments that process data outside of an approved region.

```json
{
  "mode": "All",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.CognitiveServices/accounts/deployments"
        },
        {
          "field": "Microsoft.CognitiveServices/accounts/deployments/sku.name",
          "equals": "GlobalStandard"
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

This policy denies creating or updating deployments with the `GlobalStandard` SKU.

References:
- Reference: [Azure Policy definition structure basics](/azure/governance/policy/concepts/definition-structure-basics)
- Reference: [Azure Policy definition structure policy rule](/azure/governance/policy/concepts/definition-structure-policy-rule)
- Reference: [Azure Policy definition structure aliases](/azure/governance/policy/concepts/definition-structure-alias)
- Reference: [Azure Policy definitions deny effect](/azure/governance/policy/concepts/effect-deny)
- Reference: [Azure Policy definition schema](https://schema.management.azure.com/schemas/2020-10-01/policyDefinition.json)

---

> [!NOTE]
> The resource provider name for Foundry Tools and Azure OpenAI is still `Microsoft.CognitiveServices`. Azure Cognitive Services is a former name of Foundry Tools.

## Create and assign a custom policy

Follow these steps to create and assign an example custom policy to control model deployments:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Authoring**, **Definitions**, and then select **+ Policy definition** from the top of the page.

    :::image type="content" source="../media/configure-deployment-policies/create-new-policy.png" alt-text="A screenshot showing how to create a new policy definition in Azure Policies." lightbox="../media/configure-deployment-policies/create-new-policy.png":::

1. In the **Policy Definition** form, use the following values:

    - **Definition location**: Select the subscription or management group where you want to store the policy definition.
    - **Name**: Enter a unique name for the policy definition. For example, `Custom allowed Foundry Tools and Azure OpenAI models`.
    - **Description**: Enter a description for the policy definition.
    - **Category**: You can either create a new category or use an existing one. For example, "AI model governance."

1. On **Policy rule**, paste one of the examples from the [Policy rule examples](#policy-rule-examples) section.

1. Select **Save** to save the policy definition. After saving, you arrive at the policy definition's overview page.

1. From the policy definition's overview page, select **Assign policy** to assign the policy definition.

1. From the **Assign policy** page, use the following values on the **Basics** tab:

    - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
    - **Policy definition**: This field is prepopulated with the title of policy definition you created previously.
    - **Assignment name**: Enter a unique name for the assignment.
    - **Policy enforcement**: Make sure that the **Policy enforcement** field is set to **Enabled**. If it's not enabled, the policy isn't enforced.

    Select **Next** at the bottom of the page, or the **Parameters** tab at the top of the page.

1. Configure the parameters for the policy (if any):

    # [Enforce specific models](#tab/models)

    From the **Parameters** tab, set **Allowed AI models** to a JSON array of strings in the format `"<modelName>,<version>"`. For example, `["gpt-4,0613", "gpt-35-turbo,0613"]`.

    > [!TIP]
    > You can find the model name and version in the [Foundry model catalog](https://ai.azure.com/explore/models). Select a model to view its details.

    # [Enforce specific deployment types](#tab/deployments)

    This policy doesn't require parameters. 

9. Optionally, select the **Non-compliance messages** tab at the top of the page and set a custom message for noncompliance.

10. Select the **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.

11. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't in the list of allowed models.


## Verify policy assignment

To verify that the policy is assigned, go to **Policy** in the Azure portal, and then select **Assignments** under **Authoring**. You should see the policy listed.

To verify that the policy is enforced, try to create a deployment that violates the policy. The request is denied.

## Monitor compliance

To monitor compliance with the policy, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Compliance**. Each policy assignment is listed with the compliance status. To view more details, select the policy assignment. The following example shows the compliance report for a policy that blocks deployments of type *Global standard*.

    :::image type="content" source="../media/configure-deployment-policies/policy-compliance.png" alt-text="A screenshot showing an example of a policy compliance report for a policy that blocks Global standard deployment SKUs." lightbox="../media/configure-deployment-policies/policy-compliance.png":::

## Update the policy assignment

To update an existing policy assignment with new models, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Assignments** and find the existing policy assignment. Select the ellipsis (...) next to the assignment and select **Edit assignment**.
1. From the **Parameters** tab, update the **Allowed models** parameter with the new models.
1. From the **Review + Save** tab, select **Save** to update the policy assignment.

## Best practices

- **Granular scoping**: Assign policies at the appropriate scope to balance control and flexibility. For example, apply at the subscription level to control all resources in the subscription, or apply at the resource group level to control resources in a specific group.
- **Policy naming**: Use a consistent naming convention for policy assignments to make it easier to identify the purpose of the policy. Include information such as the purpose and scope in the name.
- **Documentation**: Keep records of policy assignments and configurations for auditing purposes. Document any changes made to the policy over time.
- **Regular reviews**: Periodically review policy assignments to ensure they align with your organization's requirements.
- **Testing**: Test policies in a nonproduction environment before applying them to production resources.
- **Communication**: Make sure developers are aware of the policies in place and understand the implications for their work.

## Related content

- [Azure Policy overview](/azure/governance/policy/overview)
- [Deployment types](../concepts/deployment-types.md)

