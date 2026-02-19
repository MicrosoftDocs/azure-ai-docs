---
title: "Quickstart: Create a Guardrail policy"
description: Learn how to create a guardrail policy for model deployments in Microsoft Foundry so that you can govern the usage of guardrail controls across your subscription.
author: gregharen
ms.author: scottpolly
ms.reviewer: gregharen
ms.date: 02/19/2026
ms.topic: quickstart
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a subscription owner, I want to manage guardrail policies in Microsoft Foundry so that I can monitor compliance status in Foundry Control Plane.
---

# Quickstart: Create a Guardrail policy

In this quickstart, you create a policy in Microsoft Foundry to govern the use of guardrail controls for model deployments across your subscription.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/) before you begin.

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- The appropriate roles for using Azure Policy to create a policy for your subscription. You can learn more about Azure Policy roles in the [overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac).

> [!NOTE]
> This capability is available only in the [Microsoft Foundry (new) portal](../../what-is-foundry.md#microsoft-foundry-portals).

## Create the guardrail policy

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. On the toolbar, select **Operate**.

1. On the left pane, select **Compliance**.

1. Select **Create policy**.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/compliance-tab.png" alt-text="Screenshot of the Compliance pane of Foundry Control Plane." lightbox="media/quickstart-create-a-guardrail-policy/compliance-tab.png":::

1. Select the controls to add to the policy. Guardrail controls include content safety filters, prompt shields, and groundedness checks. These controls represent the minimum settings required for a model deployment to be considered compliant with the policy.

   As you configure each control, select **Add control** to add it to the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/create-new-policy.png" alt-text="Screenshot of the area for adding controls." lightbox="media/quickstart-create-a-guardrail-policy/create-new-policy.png":::

1. Select **Next** to move to scope selection. You can scope your policy to a single subscription or a resource group.

   Select a scope, select the subscription or resource group that you want to apply to the policy, and then choose **Select**.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-scope.png" alt-text="Screenshot of the area for selecting a scope." lightbox="media/quickstart-create-a-guardrail-policy/select-scope.png":::

1. Select **Next** to add exceptions to the policy. The exception options depend on your scope selection:
   - If you scoped to a *subscription*, you can create exceptions for entire resource groups or individual model deployments within that subscription.
   - If you scoped to a *resource group*, you can create exceptions only for individual model deployments.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-exception.png" alt-text="Screenshot of the area for configuring exceptions." lightbox="media/quickstart-create-a-guardrail-policy/select-exception.png":::

1. Select **Next** to move to the review stage. Enter a name for your policy and review the scope, exceptions, and controls. When you're ready, select **Submit** to create the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/submit-policy.png" alt-text="Screenshot of the area for reviewing and submitting a guardrail policy." lightbox="media/quickstart-create-a-guardrail-policy/submit-policy.png":::

## Verify your policy

After you submit your policy, verify that it was created successfully:

1. On the **Compliance** pane, select the **Policies** tab.

1. Locate your newly created policy in the policy list.

1. Check that the policy name, scope, and status are correct.

> [!NOTE]
> It takes some time for Azure Policy to perform a compliance scan. Initial compliance results might not appear immediately after policy creation.

> [!TIP]
> If you receive a permissions error when creating a policy, verify that you have the [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) role at the subscription or resource group level.

## Clean up resources

If you no longer need the guardrail policy, you can delete it:

1. On the **Compliance** pane, select the **Policies** tab.

1. Select the policy that you want to remove.

1. Select **Delete**, and then confirm the deletion.

> [!NOTE]
> Deleting a policy in the Foundry portal also removes the associated policy assignment in Azure Policy.

## Related content

- [Manage compliance and security in Microsoft Foundry](how-to-manage-compliance-security.md)
- [What is Microsoft Foundry Control Plane?](overview.md)
- [Enforce token limits for models](how-to-enforce-limits-models.md)
