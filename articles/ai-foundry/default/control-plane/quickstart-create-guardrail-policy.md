---
title: "Quickstart: Create a guardrail policy"
description: These instructions guide you in creating a guardrail policy for your model deployments in Microsoft Foundry. This policy allows you to govern the usage of guardrail controls across your subscription.
author: gregharen
ms.author: scottpolly
ms.reviewer: gregharen
ms.date: 11/05/2025
ms.topic: quickstart
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a subscription owner, I want to manage guardrail policies in Microsoft Foundry so that I can monitor compliance status in the Foundry Control Plane.
---

# Quickstart: Create a guardrail policy

In this quickstart, you create an Azure Policy in Microsoft Foundry to govern the use of guardrail controls for model deployments across your subscription.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]


**Required permissions:**

- You must have the appropriate roles to create an Azure Policy for your subscription. You can learn more about Azure Policy roles here: [Overview of Azure Policy - Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac)

> [!NOTE]
> This capability is available only in the [Microsoft Foundry (new) portal](../../what-is-azure-ai-foundry.md#microsoft-foundry-portals). 

## Create the guardrail policy

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]

1. Select **Operate** from the upper-right navigation.

1. Select **Compliance** in the left pane.

1. Select **Create policy**.

     :::image type="content" source="media/quickstart-create-a-guardrail-policy/compliance-tab.png" alt-text="Screenshot of the Compliance pane of the Foundry Control Plane." lightbox="media/quickstart-create-a-guardrail-policy/compliance-tab.png":::

1. Select the controls to be added to the policy. Guardrail controls include content safety filters, prompt shields, and groundedness checks that help ensure your AI models operate safely and responsibly. These controls represent the minimum settings required for a model deployment to be considered compliant with the policy. As you configure each control, select **Add control** to add it to the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/create-new-policy.png" alt-text="A screenshot of the Create Policy dialog." lightbox="media/quickstart-create-a-guardrail-policy/create-new-policy.png":::

1. Select **Next** to move to scope selection. You can scope your policy to a single subscription or a resource group. Select the desired scope and then select a subscription or resource group from a list of resources that you have access to.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-scope.png" alt-text="Screenshot of the scope selection page showing subscription and resource group options." lightbox="media/quickstart-create-a-guardrail-policy/select-scope.png":::

1. Pick the desired subscription or resource group to apply to the policy and select **Select**.

1. Select **Next** to add exceptions to the policy. The exception options depend on your scope selection:
   - If you scoped to a **subscription**, you can create exceptions for entire resource groups or individual model deployments within that subscription.
   - If you scoped to a **resource group**, you can only create exceptions for individual model deployments.

        :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-exception.png" alt-text="Screenshot of the exceptions configuration page." lightbox="media/quickstart-create-a-guardrail-policy/select-exception.png":::

1. Once all exceptions have been added, select **Next** to move to the review stage. Here, you name your policy and review the scope, exceptions, and controls that define the policy. Once ready, select **Submit** to create the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/submit-policy.png" alt-text="Screenshot of the review and submit page for the guardrail policy." lightbox="media/quickstart-create-a-guardrail-policy/submit-policy.png":::

## Verify your policy

After you submit your policy, verify that it was created successfully:

1. Select the **Policies** tab in the **Compliance** pane.

1. Locate your newly created policy in the policy list.

1. Check that the policy name, scope, and status are displayed correctly.

> [!NOTE]
> It takes some time for Azure Policy to perform a compliance scan. Initial compliance results might not appear immediately after policy creation.

## Related content

Now that you've created your guardrail policy, explore these next steps:

- [Register and manage custom agents](register-custom-agent.md)

> [!NOTE]
> When you create a policy assignment in Foundry, the system creates a series of individual policies and associates them to a policy initiative. In the Foundry portal, you view the status of the policy initiative rather than individual policies. You can also review and manage these policies directly in Azure Policy via the Azure portal.
