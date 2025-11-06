---
title: "Quickstart: Create a guardrail policy"
description: These instructions guide you in creating a guardrail policy for your model deployments in Azure AI Foundry. This policy allows you to govern the usage of guardrail controls across your subscription.
#customer intent: As a subscription owner, I want to manage guardrail policies in Azure AI Foundry so that I can monitor compliance status in the Foundry Control Plane.
author: gregharen
ms.author: scottpolly
ms.reviewer: gregharen
ms.date: 11/05/2025
ms.topic: quickstart
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Quickstart: Create a guardrail policy

In this quickstart, you create an Azure Policy in Azure AI Foundry to govern the use of guardrail controls for model deployments across your subscription.

## Prerequisites

**Azure resources:**

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- An Azure AI Foundry project. If you don't have one, [create a project](../../how-to/create-projects.md).
- At least one agent deployed in your Azure AI Foundry project and registered in Foundry Control Plane.

**Required permissions:**

- You must have the appropriate roles to create an Azure Policy for your subscription. You can learn more about Azure Policy roles here: [Overview of Azure Policy - Azure Policy \| Microsoft Learn](/azure/governance/policy/overview#azure-policy-and-azure-rbac)

> [!NOTE]
> This capability is available only in the Azure AI Foundry (new) portal. Look for :::image type="icon" source="../media/version-banner/new-foundry.png" border="false"::: in the portal banner to confirm you're using Azure AI Foundry (new).

## Create the guardrail policy

1. [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)].
1. Select **Operate** from the upper-right navigation menu.
1. Navigate to the Compliance page under the Operate tab in the left navigation.

     :::image type="content" source="media/quickstart-create-a-guardrail-policy/compliance-tab.png" alt-text="Screenshot of the Compliance pane of the Foundry Control Plane." lightbox="media/quickstart-create-a-guardrail-policy/compliance-tab.png":::

1. Once there, select "Create new policy".

1. Select and add the controls to be added to the policy. Guardrail controls include content safety filters, prompt shields, and groundedness checks that help ensure your AI models operate safely and responsibly. These controls represent the minimum settings required for a model deployment to be considered compliant with the policy. As you configure each control, select "Add control" to add it to the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/create-new-policy.png" alt-text="A screenshot of the Create Policy dialog." lightbox="media/quickstart-create-a-guardrail-policy/create-new-policy.png":::

1. Select "Next" to move to scope selection. You can scope your policy to a single subscription or a resource group. Select the desired scope and select the "select" button to pick a subscription or resource group from a list of resources that you have access to.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-scope.png" alt-text="Screenshot of the scope selection page showing subscription and resource group options." lightbox="media/quickstart-create-a-guardrail-policy/select-scope.png":::

1. Pick the desired subscription or resource group to apply to the policy and select the "select" button.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/subscription-selection.png" alt-text="Screenshot of the subscription or resource group selection dialog." lightbox="media/quickstart-create-a-guardrail-policy/subscription-selection.png":::

1. Select the "Next" button to add exceptions to the policy. The exception options depend on your scope selection:
   - If you scoped to a **subscription**, you can create exceptions for entire resource groups or individual model deployments within that subscription.
   - If you scoped to a **resource group**, you can only create exceptions for individual model deployments.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/select-exception.png" alt-text="Screenshot of the exceptions configuration page." lightbox="media/quickstart-create-a-guardrail-policy/select-exception.png":::

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/resource-group-exception.png" alt-text="Screenshot of the exceptions interface showing resource group and model deployment options." lightbox="media/quickstart-create-a-guardrail-policy/resource-group-exception.png":::

1. Once all exceptions have been added, select "Next" to move to the review stage. Here, you name your policy and review the scope, exceptions, and controls that define the policy. Once ready, select submit to create the policy.

    :::image type="content" source="media/quickstart-create-a-guardrail-policy/submit-policy.png" alt-text="Screenshot of the review and submit page for the guardrail policy." lightbox="media/quickstart-create-a-guardrail-policy/submit-policy.png":::

## Verify your policy

After you submit your policy, verify that it was created successfully:

1. In the Compliance tab, locate your newly created policy in the policy list.
1. Check that the policy name, scope, and status are displayed correctly.

> [!NOTE]
> It takes some time for Azure Policy to perform a compliance scan. Initial compliance results might not appear immediately after policy creation.

## Related content

Now that you've created your guardrail policy, explore these next steps:

- [Monitor compliance status for your guardrails](../../how-to/monitor-compliance.md)
- [Edit or update existing guardrail policies](../../how-to/manage-guardrail-policies.md)
- [Deploy agents with guardrail controls](../../how-to/deploy-agents-with-guardrails.md)

> [!NOTE]
> When you create a policy assignment in Azure AI Foundry, the system creates a series of individual policies and associates them to a policy initiative. In the Foundry portal, you view the status of the policy initiative rather than individual policies. You can also review and manage these policies directly in Azure Policy via the Azure portal.
