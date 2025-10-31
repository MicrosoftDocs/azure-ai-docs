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

- You're using the new Azure AI Foundry user interface.

- You migrated or started migrating to Agents v2.

- You have the appropriate Azure RBAC roles to take the actions outlined in this article.

## Create, review, and manage guardrail policies

Guardrail policies let you mandate minimum guardrail controls for your model deployments across a subscription or within a resource group.

To learn more about guardrail policies, visit \[Link to Understanding Guardrail Policies doc\]. <!-- link to be added when doc is created -->

> [!NOTE]
> Most users don't have permission to create policies because they need the appropriate Azure RBAC roles for Azure Policy. See [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac). Most users in Azure AI Foundry can still view the compliance status of individual policies and model deployments.

### View and fix compliance violations

Determine whether any model deployments are non-compliant with organizational policies. To assess compliance status and address issues, follow these steps:

1. Navigate to **Operate** > **Compliance**.

1. On the **Policies** tab, review all applicable policies within your subscription and project. To expand the scope beyond a single project, adjust the project filter to **All projects** for an overview of the entire subscription. You can also switch the subscription being viewed.

1. Identify any non-compliant policy by locating those with a **Violations detected** value in the **Policy Compliance** column.

1. When a policy is selected, refer to the right-hand side panel and select an asset to compare its guardrail settings with the requirements specified in the policy.

1. To update the guardrail configuration of a non-compliant asset, select **Fix now**. This redirects you to the asset's configuration edit page.

Additionally, compliance status can be reviewed by asset rather than by policy:

1. Navigate to **Operate** > **Compliance**.

1. Select **Assets** using the **Policy/Assets** toggle in the table.

1. Review model deployments within the chosen subscription and project.

1. In the **Policy Compliance** column, examine any assets marked as **Violation detected**. Select these rows to access further details. Note that assets may appear multiple times if subject to several policies.

1. In the right-hand panel displayed when an asset is selected, review the governing policies and the specifics of any non-compliant policy.

1. Select **View in Build** to modify the guardrail configuration and bring the model deployment into compliance. Review all relevant policies for each asset to ensure all necessary adjustments are made to achieve full compliance.

To create a policy, follow these steps. Ensure you have the proper RBAC to create policies, as found here: [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac)

1. Select **Operate** > **Compliance**.

1. Select **Create new policy**.

1. Choose and configure controls, selecting **Add control** after each.

1. Select **Next** to set the policy scope—select one subscription or resource group.

1. Select **Next** to add exceptions for model deployments or, if scoped to a subscription, resource groups.

1. Select **Next** when exceptions are complete.

1. Enter a policy name (display ID).

1. Finalize to create your policy.

1. Allow up to 30 minutes for the policy to appear in the Azure AI Foundry portal. Compliance results show once Azure Policy scans, timing varies by scope size and resources.

If you want to edit a policy, take the following steps. You need the same roles to edit a policy that are required to create a policy.

1. Select **Operate** > **Compliance**.

1. Select **Create new policy**.

1. Choose and configure controls, selecting **Add control** after each.

1. Select **Next** to set the policy scope—select one subscription or resource group.

1. Select **Next** to add exceptions for model deployments or, if scoped to a subscription, resource groups.

1. Select **Next** when exceptions are complete.

1. Enter a policy name (display ID).

1. Finalize to create your policy.

1. Allow up to 30 minutes for the policy to appear in the Azure AI Foundry portal. Compliance results show once Azure Policy scans, timing varies by scope size and resources.

## Review guardrails across your subscription

When monitoring your model deployments for compliance, it's useful to review and compare the different guardrail controls set up for your assets throughout a project or subscription, even if they're not directly linked to policy compliance. This process helps you spot any gaps in policy assignments, like missing controls, and uncover potential risks that may have gone unnoticed—such as subscriptions lacking content filtering entirely.

Here's how you can do this:

1. Select **Operate** > **Compliance**.

1. Select the **Guardrails** tab.

1. Check that your scope is correct by reviewing and adjusting the subscription and project dropdowns as needed.

1. Examine the configurations across your projects, using column sorting to quickly find issues (for example, seeing which filters are disabled).

1. If you find a problem, you have two choices to address it:

    - Select **Build** > **Guardrails** in the relevant project to update existing guardrail settings or add new ones for your model deployments, making sure they're equipped to handle the risks you've identified.

    - Select **Operate** > **Compliance** > **Policy** to create a new policy that guarantees your model deployments always have the necessary guardrail controls, and that you can continue to monitor them for compliance.

## Set up security recommendations and alerts

In addition to reviewing the safety, security, and compliance of your Azure AI Foundry assets via the Azure AI Foundry Control Plane, you can review gaps in your security posture and recommendations for remediation, provided by Microsoft Defender for Cloud. Defender assesses your resources and workloads against built-in and custom security standards. To receive security posture recommendations from Microsoft Defender for Cloud, [enable it on your Azure subscription](/azure/defender-for-cloud/connect-azure-subscription). To receive threat protection alerts for jailbreak attacks based on Azure AI Foundry's user input attack risk detection, additionally [enable threat protection for AI services](/azure/defender-for-cloud/ai-onboarding).

## Review your security recommendations

To review Defender security recommendations, follow these steps:

1. Select **Operate** > **Compliance**.

1. Select the **Security** tab.

1. [Enable Microsoft Defender for Cloud](/azure/defender-for-cloud/connect-azure-subscription) for your subscription if you haven't already done so.

1. View recommendations in the **Microsoft Defender for Cloud** section, including the affected resource and the associated risk level.

1. Select a recommendation to view details and links to take action to remediate in Azure Portal.

## Opt into Purview Data Security Posture Management for Azure AI Foundry

Prerequisites:

- Microsoft Purview with E5 license.

- Cognitive Services Security Integration Administrator role. This can be assigned by the Subscription Owner.

In addition to Azure AI Foundry's security offerings, you can opt into enterprise-grade data security, compliance, and governance provided by Microsoft Purview. Once this integration is enabled for a subscription, app and agent interaction data is sent to Purview, subject to policies created in the Purview Portal by your tenant's data security administrator. Apps and agents in Azure AI Foundry within the subscription might also be subject to blocking based on Purview policies.

To enable Purview:

1. Select **Operate** > **Compliance**.

1. Select the **Security** tab.

1. Select the enablement toggle next to **Microsoft Purview**.

1. Purview policies to govern Azure AI Foundry apps and agents can then be created in the Purview Portal.



- link.md

- link.md

- link.md
