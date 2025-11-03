---
title: Manage compliance and security in Azure AI Foundry
ms.reviewer: gregharen
description: Discover how to manage compliance and secure your Azure AI Foundry assets using guardrail policies, Microsoft Defender for Cloud, and Purview Data Security.
author: s-polly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 10/31/2025
ai-usage: ai-assisted

#CustomerIntent: As a developer, I want ensure compliance and security of my assets within Azure AI Foundry so that I avoid any security and compliance issues.
---

# Manage compliance and security in Azure AI Foundry

Learn how Azure AI Foundry Control Plane helps you manage the compliance and security of your assets across subscriptions. You can use guardrail policies and guardrail management, integrate with Microsoft Defender for Cloud, and integrate with Microsoft Purview.

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

- An Azure AI Foundry project. If you don't have one, [create a project](../../how-to/create-projects.md).

- This capability is available only in the Azure AI Foundry (new) portal. Look for :::image type="icon" source="../media/version-banner/new-foundry.png" border="false"::: in the portal banner to confirm you're using Azure AI Foundry (new).

- If you use agents, you need Agents v2 or later for full compliance feature support. <!--need to verify this and expand>

- Appropriate permissions based on the tasks you want to perform:
  - To **view** compliance status and guardrail policies: No special permissions required beyond project access.
  - To **create or edit** guardrail policies: You must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level. See [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac).
  - To **enable Microsoft Defender for Cloud**: Appropriate permissions on your Azure subscription to configure security settings.
  - To **configure Purview integration**: Cognitive Services Security Integration Administrator role (can be assigned by the Subscription Owner).

> [!NOTE]
> Additional prerequisites for specific features are listed in their respective sections.

## Create, review, and manage guardrail policies

Guardrail policies let you mandate minimum guardrail controls for your model deployments across a subscription or within a resource group. Guardrail controls include content filtering, abuse monitoring, and other safety measures that protect your model deployments from generating harmful content or being misused.

To learn more about guardrail policies, visit \[Link to Understanding Guardrail Policies doc\]. <!-- link to be added when doc is created -->

> [!NOTE]
> Most users don't have permission to create guardrail policies because they need the appropriate Azure RBAC roles for Azure Policy. See [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac). Most users in Azure AI Foundry can still view the compliance status of individual guardrail policies and model deployments.

### View and fix compliance violations

Determine whether any model deployments are non-compliant with organizational guardrail policies. To assess compliance status and address issues, follow these steps:

1. Navigate to **Operate** > **Compliance**.

1. On the **Policies** tab, review all applicable guardrail policies within your subscription and project. To expand the scope beyond a single project, adjust the project filter to **All projects** for an overview of the entire subscription. You can also switch the subscription being viewed.

1. Identify any non-compliant guardrail policy by locating those with a **Violations detected** value in the **Policy Compliance** column.

1. When a guardrail policy is selected, refer to the right-hand side panel and select an asset to compare its guardrail settings with the requirements specified in the guardrail policy.

1. To update the guardrail configuration of a non-compliant asset, select **Fix now**. This opens the model deployment's guardrail configuration page where you can adjust settings to meet the guardrail policy requirements. After saving your changes, the compliance status updates within a few minutes.

Additionally, compliance status can be reviewed by asset rather than by guardrail policy:

1. Navigate to **Operate** > **Compliance**.

1. Select **Assets** using the **Policy/Assets** toggle in the table.

1. Review model deployments within the chosen subscription and project.

1. In the **Policy Compliance** column, examine any assets marked as **Violation detected**. Select these rows to access further details. Note that assets may appear multiple times if subject to several guardrail policies.

1. In the right-hand panel displayed when an asset is selected, review the governing guardrail policies and the specifics of any non-compliant guardrail policy.

1. Select **View in Build** to modify the guardrail configuration and bring the model deployment into compliance. Review all relevant guardrail policies for each asset to ensure all necessary adjustments are made to achieve full compliance.

### Create a guardrail policy

To create a guardrail policy, follow these steps:

1. Select **Operate** > **Compliance**.

1. Select **Create new policy**.

1. Choose and configure controls (such as content filters, prompt shields, or abuse detection), selecting **Add control** after each.

1. Select **Next** to set the policy scope. The scope determines which resources the policy applies to—choose a subscription to apply broadly, or a specific resource group for targeted governance.

1. Select **Next** to add exceptions for model deployments or, if scoped to a subscription, resource groups. Exceptions allow you to exclude specific model deployments or resource groups from the policy requirements. Use exceptions for testing environments or legacy deployments that can't meet new requirements.

1. Select **Next** when exceptions are complete.

1. Enter a descriptive policy name. This name appears in the compliance dashboard.

1. Select **Create** to finalize your guardrail policy.

1. Allow up to 30 minutes for the guardrail policy to appear in the Azure AI Foundry portal. Compliance results show once Azure Policy scans, timing varies by scope size and resources.

After creating the guardrail policy, you see it listed in the **Policies** tab. The compliance status updates automatically as Azure Policy evaluates your resources.

### Edit a guardrail policy

To edit an existing guardrail policy, follow these steps:

1. Select **Operate** > **Compliance**.

1. On the **Policies** tab, locate and select the guardrail policy you want to edit.

1. Select **Edit policy** from the guardrail policy details panel.

1. Modify the controls, scope, or exceptions as needed.

1. Select **Save** to apply your changes.

1. Allow up to 30 minutes for the updated guardrail policy to take effect. Compliance results update once Azure Policy reevaluates your resources.

## Review guardrails across your subscription

When monitoring your model deployments for compliance, it's useful to review and compare the different guardrail controls set up for your assets throughout a project or subscription, even if they're not directly linked to guardrail policy compliance. This process helps you spot gaps in guardrail policy assignments, like missing controls. You can also uncover potential risks that may have gone unnoticed—such as subscriptions lacking content filtering entirely.

Here's how you can do this:

1. Select **Operate** > **Compliance**.

1. Select the **Guardrails** tab.

1. Check that your scope is correct by reviewing and adjusting the subscription and project dropdowns as needed.

1. Examine the configurations across your projects, using column sorting to quickly find issues (for example, seeing which filters are disabled).

1. If you find a problem, choose one of these options:

   **Option 1: Update individual deployments**
   
   1. Select **Build** > **Guardrails** in the relevant project.
   1. Update existing guardrail settings or add new ones for your model deployments.
   
   **Option 2: Create a guardrail policy for enforcement**
   
   1. Select **Operate** > **Compliance** > **Policy**.
   1. Create a new guardrail policy to enforce guardrail requirements across all deployments.

## Set up security recommendations and alerts

You can review gaps in your security posture and recommendations for remediation, provided by Microsoft Defender for Cloud. Your security posture represents the overall security status of your Azure resources, including potential vulnerabilities, misconfigurations, and recommended improvements. Defender assesses your resources and workloads against built-in and custom security standards. 

To receive security posture recommendations from Microsoft Defender for Cloud, [enable it on your Azure subscription](/azure/defender-for-cloud/connect-azure-subscription). To receive threat protection alerts for jailbreak attacks based on Azure AI Foundry's user input attack risk detection, [enable threat protection for AI services](/azure/defender-for-cloud/ai-onboarding). Jailbreak attacks attempt to bypass AI safety measures by using carefully crafted prompts. Azure AI Foundry detects these attack patterns in user input.

### Review your security recommendations

To review Defender security recommendations, follow these steps:

1. Select **Operate** > **Compliance**.

1. Select the **Security** tab.

1. [Enable Microsoft Defender for Cloud](/azure/defender-for-cloud/connect-azure-subscription) for your subscription if you haven't already done so.

1. View recommendations in the **Microsoft Defender for Cloud** section, including the affected resource and the associated risk level. Recommendations might include enabling additional security features, fixing misconfigurations, or addressing potential vulnerabilities in your AI deployments.

1. Select a recommendation to view details and links to take action to remediate in Azure Portal.

### Opt into Purview Data Security Posture Management

To use Purview Data Security Posture Management for Azure AI Foundry, you need:

- Microsoft Purview with E5 license.

- Cognitive Services Security Integration Administrator role. This role can be assigned by the Subscription Owner.

In addition to Azure AI Foundry's security offerings, you can opt into enterprise-grade data security, compliance, and governance provided by Microsoft Purview. Once this integration is enabled for a subscription, app and agent interaction data is sent to Purview. The data is subject to policies created in the Microsoft Purview compliance portal by your tenant's data security administrator. Apps and agents in Azure AI Foundry within the subscription might also be subject to blocking based on Purview policies, meaning requests to these apps and agents can be prevented if they violate your organization's data governance policies.

To enable Purview:

1. Select **Operate** > **Compliance**.

1. Select the **Security** tab.

1. Select the enablement toggle next to **Microsoft Purview**.

1. Create Purview policies to govern Azure AI Foundry apps and agents in the [Microsoft Purview compliance portal](https://purview.microsoft.com).

## Related content

- [Overview of Azure Policy](/azure/governance/policy/overview)
- [Microsoft Defender for Cloud documentation](/azure/defender-for-cloud/)
- [Microsoft Purview data security and compliance](/purview/)
