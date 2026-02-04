---
title: Manage compliance and security in Microsoft Foundry
ms.reviewer: gregharen
description: Discover how to manage compliance and secure your Microsoft Foundry assets using guardrail policies, Microsoft Defender for Cloud, and Purview Data Security.
author: s-polly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/23/2026
ai-usage: ai-assisted
ms.custom: dev-focus

#CustomerIntent: As a developer, I want to ensure compliance and security of my assets within Microsoft Foundry so that I avoid any security and compliance issues.
---

# Manage compliance and security in Microsoft Foundry

Learn how Foundry Control Plane helps you manage compliance, enforce guardrail controls, and integrate security tooling such as Microsoft Defender for Cloud across subscriptions.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use the compliance workspace tabs to reach the right surface quickly.

| Tab | Navigation | Outcome |
| --- | --- | --- |
| Policies | **Operate** > **Compliance** > **Policies** | Review guardrail policies, check compliance, and create or edit enforcement rules. |
| Assets | **Operate** > **Compliance** > **Assets** | Inspect individual model deployments, view policy violations, and jump to remediation. |
| Guardrails | **Operate** > **Compliance** > **Guardrails** | Compare guardrail configurations across deployments and spot coverage gaps. |
| Security | **Operate** > **Compliance** > **Security** | Review Microsoft Defender for Cloud recommendations and manage Microsoft Purview enablement. |

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]
- If you use agents, you need Agents v2 or later for full compliance feature support. 

- Appropriate permissions based on the tasks you want to perform:
  - To **view** compliance status and guardrail policies: No special permissions required beyond project access.
  - To **create or edit** guardrail policies: You must be an [**Owner**](/azure/role-based-access-control/built-in-roles#owner) or [**Resource Policy Contributor**](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level. See [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac).
  - To **enable Microsoft Defender for Cloud**: You need the **Security Admin** role or be a subscription **Owner** so you can turn on Defender plans and agentless protections.
  - To **configure Purview integration**: The **Azure AI Account Owner** role is required.

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## Create, review, and manage guardrail policies

Guardrail policies let you mandate minimum guardrail controls for your model deployments across a subscription or within a resource group. Guardrail controls include content filtering, abuse monitoring, and other safety measures that protect your model deployments from generating harmful content or being misused.

To learn more about guardrail policies, visit [Guardrails and controls overview](../guardrails/guardrails-overview.md). 

> [!NOTE]
> Most users don't have permission to create guardrail policies because they need the appropriate Azure RBAC roles for Azure Policy. See [Overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac). Most users in Foundry can still view the compliance status of individual guardrail policies and model deployments.

> [!TIP]
> Access the compliance workspace by selecting **Operate** in the top navigation, then choosing **Compliance** in the left pane. Use the subscription and project filters to scope your view before switching tabs.

### View and fix compliance violations

Determine whether any model deployments don't comply with organizational guardrail policies. To assess compliance status and address issues, follow these steps:

1. Select the **Policies** tab. Review all applicable guardrail policies within your subscription and project. To expand the scope beyond a single project, adjust the project filter to **All projects** for an overview of the entire subscription. You can also switch subscriptions.

1. Identify any noncompliant guardrail policy by locating those with a **Violations detected** value in the **Policy Compliance** column.

1. Select a guardrail policy. Refer to the right-hand side panel and select an asset to compare its guardrail settings with the requirements that the guardrail policy specifies.

1. To update the guardrail configuration of a noncompliant asset, select **Fix now**. This selection opens the model deployment's guardrail configuration page where you can adjust settings to meet the guardrail policy requirements. After saving your changes, the compliance status updates within a few minutes.

Additionally, you can review compliance status by asset rather than by guardrail policy:

1. Select the **Assets** tab by using the **Policy/Assets** toggle.

1. Review model deployments within the chosen subscription and project.

1. Examine any assets marked as **Violation detected** in the **Policy Compliance** column. Select these rows to access further details. Assets might appear multiple times if they're subject to several guardrail policies.

1. Review the governing guardrail policies and the specifics of any noncompliant guardrail policy in the right-hand panel.

1. Select **View in Build** to modify the guardrail configuration and bring the model deployment into compliance. Review all relevant guardrail policies for each asset to ensure all necessary adjustments are made to achieve full compliance.

### Create a guardrail policy

To create a guardrail policy, follow these steps:

1. In the compliance workspace, select **Create new policy**.

1. Choose and configure controls, such as content filters, prompt shields, or abuse detection. Select **Add control** after configuring each control.

1. Select **Next** to set the policy scope. The scope determines which resources the policy applies to. Choose a subscription to apply the policy broadly, or choose a specific resource group for targeted governance.

1. Select **Next** to add exceptions for model deployments or, if scoped to a subscription, resource groups. You can exclude specific model deployments or resource groups from the policy requirements. Use exceptions for testing environments or legacy deployments that can't meet new requirements.

1. Select **Next** when exceptions are complete.

1. Enter a descriptive policy name. This name appears in the compliance dashboard.

1. Select **Create** to finalize your guardrail policy.

1. Allow up to 30 minutes for the guardrail policy to appear in the Foundry portal. Compliance results appear once Azure Policy completes its scan. The duration of the scan varies by scope size and resources.

After you create the guardrail policy, you see it listed in the **Policies** tab. The compliance status updates automatically as Azure Policy evaluates your resources.

### Edit a guardrail policy

To edit an existing guardrail policy, follow these steps:

1. In the compliance workspace, select the **Policies** tab. Locate and select the guardrail policy you want to edit.

1. Select **Edit policy** from the guardrail policy details panel.

1. Modify the controls, scope, or exceptions as needed.

1. Select **Save** to apply your changes.

1. Wait up to 30 minutes for the updated guardrail policy to take effect. Compliance results update once Azure Policy reevaluates your resources.

## Review guardrails across your subscription

When you monitor your model deployments for compliance, review and compare the different guardrail controls for your assets throughout a project or subscription. Even if the controls aren't directly linked to guardrail policy compliance, this process helps you spot gaps in guardrail policy assignments, like missing controls. You can also uncover potential risks that might go unnoticed - such as subscriptions lacking content filtering entirely.

Here's how you can do this:
1. In the compliance workspace, select the **Guardrails** tab.

1. Check that your scope is correct by reviewing and adjusting the subscription and project dropdowns as needed.

1. Examine the configurations across your projects, using column sorting to quickly find problems. For example, you can see which filters are disabled.

1. If you find a problem, choose one of these options:

   **Option 1: Update individual deployments**

   1. Select **Build** from the upper-right navigation.
   1. Select **Guardrails** in the relevant project.
   1. Update existing guardrail settings or add new ones for your model deployments.

   **Option 2: Create a guardrail policy for enforcement**

   1. In the compliance workspace, select the **Policies** tab.
   1. Create a new guardrail policy to enforce guardrail requirements across all deployments.

## Set up security recommendations and alerts

Microsoft Defender for Cloud provides security posture gaps and recommendations for remediation. Your security posture represents the overall security status of your Azure resources, including potential vulnerabilities, misconfigurations, and recommended improvements. Defender assesses your resources and workloads against built-in and custom security standards. 

To get security posture recommendations from Microsoft Defender for Cloud, [enable it on your Azure subscription](/azure/defender-for-cloud/connect-azure-subscription). To get threat protection alerts for jailbreak attacks based on Foundry's user input attack risk detection, [enable threat protection for Foundry Tools](/azure/defender-for-cloud/ai-onboarding). Jailbreak attacks attempt to bypass AI safety measures by using carefully crafted prompts. Foundry detects these attack patterns in user input.  

### Review your security recommendations

To review Defender security recommendations, follow these steps:
1. In the compliance workspace, select the **Security** tab.

1. [Enable Microsoft Defender for Cloud](/azure/defender-for-cloud/connect-azure-subscription) for your subscription if you need to do so.

1. View recommendations in the **Microsoft Defender for Cloud** section, including the affected resource and the associated risk level. Recommendations might include enabling additional security features, fixing misconfigurations, or addressing potential vulnerabilities in your AI deployments.

1. Select a recommendation to view details and links to take action to remediate in Azure portal.

## Enable enterprise-grade data security and compliance for Foundry with Microsoft Purview [Preview]

> [!NOTE]
> This feature requires a Microsoft Purview license in the tenant. To learn about Microsoft Purview, see [Microsoft Purview DSPM for AI](/purview/ai-microsoft-purview).

By enabling Microsoft Purview on your Azure subscription, you can access, process, and store prompt and response data – including associated metadata – from Microsoft Foundry apps and agents. This integration supports key data security and compliance scenarios such as:

- Microsoft Purview Audit
- Sensitive information type (SIT) classification
- Analytics and Reporting through Microsoft Purview DSPM for AI
- Insider Risk Management
- Communication Compliance
- Data Lifecycle Management
- eDiscovery

This capability helps your organization manage and monitor AI-generated data in alignment with enterprise policies and regulatory requirements.

> [!NOTE]
> 1. Purview Data Security Policies for Foundry Services interactions are supported for those API calls that use Microsoft Entra ID authentication with a user-context token, or for API calls that explicitly include user context. To learn more, see [Gain end-user context for Azure AI API calls](../../openai/latest.md#azureusersecuritycontext). For all other authentication scenarios, user interactions captured in Purview show up only in Purview Audit and AI Interactions with classifications within DSPM for AI Activity Explorer.
>
> 1. Purview Audit is included as part of Microsoft Purview license for Foundry services. For data security policies setup in Purview by your enterprise security admins, billing is based on [pay-as-you-go](https://azure.microsoft.com/pricing/details/purview/) meters.
>
> 1. Integration with Purview for the above features in Microsoft Foundry doesn't yet support Network Isolation.
>
> 1. Integration with Purview is currently available only for calls made on the OpenAI Completions API.

### Enable Purview in Foundry

**Prerequisite:** You must have the **Azure AI Account Owner** role to enable Purview integration.

To enable Purview in Foundry:
1. Go to **Operate** > **Compliance**.
1. Select the **Security posture** tab.
1. Select the Azure subscription.
1. Enable **Microsoft Purview** with the toggle.

    :::image type="content" source="media/how-to-manage-compliance-security/microsoft-purview-toggle.png" alt-text="Screenshot of the Microsoft Purview enablement toggle in the Compliance Security tab":::

Repeat the preceding steps for other Azure subscriptions, as appropriate.



## Related content

- [Overview of Azure Policy](/azure/governance/policy/overview)
- [Microsoft Defender for Cloud documentation](/azure/defender-for-cloud/)

