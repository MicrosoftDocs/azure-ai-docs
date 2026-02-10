---
title: Manage Compliance and Security in Microsoft Foundry
ms.reviewer: gregharen
description: Discover how to manage compliance and secure your Microsoft Foundry assets by using guardrail policies, Microsoft Defender for Cloud, and Microsoft Purview DSPM.
author: s-polly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/23/2026
ai-usage: ai-assisted
ms.custom: dev-focus

#customer intent: As a developer, I want to ensure compliance and security of my assets within Microsoft Foundry so that I avoid any security and compliance issues.
---

# Manage compliance and security in Microsoft Foundry

Learn how Microsoft Foundry Control Plane helps you manage compliance, enforce guardrail controls, and integrate security tooling such as Microsoft Defender for Cloud across subscriptions.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use the compliance workspace tabs to reach the right surface quickly.

| Tab | Navigation | Outcome |
| --- | --- | --- |
| **Policies** | **Operate** > **Compliance** > **Policies** | Review guardrail policies, check compliance, and create or edit enforcement rules. |
| **Assets** | **Operate** > **Compliance** > **Assets** | Inspect individual model deployments, view policy violations, and jump to remediation. |
| **Guardrails** | **Operate** > **Compliance** > **Guardrails** | Compare guardrail configurations across deployments and spot coverage gaps. |
| **Security** | **Operate** > **Compliance** > **Security** | Review Defender for Cloud recommendations and manage Microsoft Purview enablement. |

## Prerequisites

[!INCLUDE [control-plane-prereqs](../includes/control-plane-prereqs.md)]

- Any agents that you want to use. Be sure to use the latest agent versions for full support of compliance features.

- Appropriate permissions based on the tasks that you want to perform:
  - **To view compliance status and guardrail policies**: No special permissions are required beyond project access.
  - **To create or edit guardrail policies**: You must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level. See the [overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac).
  - **To enable Defender for Cloud**: You need the Security Admin role or the Owner role for a subscription so that you can turn on Defender plans and agentless protections.
  - **To configure Microsoft Purview integration**: You need the Azure AI Account Owner role.

[!INCLUDE [capability-new-portal](../includes/capability-new-portal.md)]

## Create, review, and manage guardrail policies

You can use guardrail policies to mandate minimum guardrail controls for your model deployments across a subscription or within a resource group. Guardrail controls include content filtering, abuse monitoring, and other safety measures that help protect your model deployments from generating harmful content or being misused.

To learn more about guardrail policies, see [Guardrails and controls overview in Microsoft Foundry](../guardrails/guardrails-overview.md).

Most users don't have permission to create guardrail policies because they need the appropriate Azure role-based access control (RBAC) roles for Azure Policy. See the [overview of Azure Policy](/azure/governance/policy/overview#azure-policy-and-azure-rbac). Most users in Foundry can still view the compliance status of individual guardrail policies and model deployments.

> [!TIP]
> Access the compliance workspace by selecting **Operate** on the toolbar, and then selecting **Compliance** on the left pane. Use the subscription and project filters to scope your view before you switch tabs.

### View and fix compliance violations

Determine whether any model deployments don't comply with organizational guardrail policies. To assess compliance status and address issues, follow these steps:

1. Select the **Policies** tab. Review all applicable guardrail policies within your subscription and project.

   To expand the scope beyond a single project, adjust the project filter to **All projects** for an overview of the entire subscription. You can also switch subscriptions.

1. Identify any noncompliant guardrail policy by locating policies that have a **Violations detected** value in the **Policy Compliance** column.

1. Select a guardrail policy. On the information pane that appears, select an asset to compare its guardrail settings with the requirements that the guardrail policy specifies.

1. To update the guardrail configuration of a noncompliant asset, select **Fix now**. This selection opens the model deployment's guardrail configuration pane, where you can adjust settings to meet the guardrail policy requirements.

   After you save your changes, the compliance status is updated within a few minutes.

You can also review compliance status by asset rather than by guardrail policy:

1. Select the **Assets** tab by using the **Policy/Assets** toggle.

1. Review model deployments within the chosen subscription and project.

1. Examine any assets marked as **Violation detected** in the **Policy Compliance** column. Select these rows to access further details. Assets might appear multiple times if they're subject to several guardrail policies.

1. On the information pane, review the governing guardrail policies and the specifics of any noncompliant guardrail policy.

1. Select **View in Build** to modify the guardrail configuration and bring the model deployment into compliance. Review all relevant guardrail policies for each asset to ensure that you make all necessary adjustments to achieve full compliance.

### Create a guardrail policy

1. In the compliance workspace, select **Create new policy**.

1. Choose and configure controls, such as content filters, prompt shields, or abuse detection. Select **Add control** after you configure each control.

1. Select **Next** to set the policy scope. The scope determines which resources the policy applies to. Choose a subscription to apply the policy broadly, or choose a specific resource group for targeted governance.

1. Select **Next** to add exceptions for model deployments or, if the policy is scoped to a subscription, resource groups. You can exclude specific model deployments or resource groups from the policy requirements. Use exceptions for testing environments or legacy deployments that can't meet new requirements.

1. Select **Next** when you finish adding exceptions.

1. Enter a descriptive policy name. This name appears in the compliance dashboard.

1. Select **Create** to finalize your guardrail policy.

1. Allow up to 30 minutes for the guardrail policy to appear in the Foundry portal. Compliance results appear after Azure Policy completes its scan. The duration of the scan varies by scope size and resources.

After you create the guardrail policy, it's listed on the **Policies** tab. The compliance status is updated automatically as Azure Policy evaluates your resources.

### Edit a guardrail policy

1. In the compliance workspace, select the **Policies** tab. Locate and select the guardrail policy that you want to edit.

1. On the pane that shows guardrail policy details, select **Edit policy**.

1. Modify the controls, scope, or exceptions as needed.

1. Select **Save** to apply your changes.

1. Wait up to 30 minutes for the updated guardrail policy to take effect. Compliance results are updated after Azure Policy reevaluates your resources.

## Review guardrails across your subscription

When you monitor your model deployments for compliance, review and compare the guardrail controls for your assets throughout a project or subscription. Even if the controls aren't directly linked to guardrail policy compliance, this process helps you spot gaps in guardrail policy assignments, like missing controls. You can also uncover potential risks that might go unnoticed, such as subscriptions that lack content filtering entirely.

Here's how you can do this task:

1. In the compliance workspace, select the **Guardrails** tab.

1. Check that your scope is correct by reviewing and adjusting the subscription and project dropdown lists as needed.

1. Examine the configurations across your projects by using column sorting to quickly find problems. For example, you can see which filters are disabled.

1. If you find a problem, choose one of these options:

   - Update individual deployments:

     1. On the toolbar, select **Build**.
     1. In the relevant project, select **Guardrails**.
     1. Update existing guardrail settings or add new ones for your model deployments.

   - Create a guardrail policy for enforcement:

     1. In the compliance workspace, select the **Policies** tab.
     1. Create a new guardrail policy to enforce guardrail requirements across all deployments.

## Set up security recommendations and alerts

Defender for Cloud provides security posture gaps and recommendations for remediation. Your security posture represents the overall security status of your Azure resources, including potential vulnerabilities, misconfigurations, and recommended improvements. Defender assesses your resources and workloads against built-in and custom security standards.

To get security posture recommendations from Defender for Cloud, [enable it on your Azure subscription](/azure/defender-for-cloud/connect-azure-subscription). To get threat protection alerts for jailbreak attacks based on risk detection in Foundry for user input attacks, [enable threat protection for Foundry Tools](/azure/defender-for-cloud/ai-onboarding). Jailbreak attacks attempt to bypass AI safety measures by using carefully crafted prompts. Foundry detects these attack patterns in user input.  

To review Defender security recommendations, follow these steps:

1. In the compliance workspace, select the **Security** tab.

1. [Enable Defender for Cloud](/azure/defender-for-cloud/connect-azure-subscription) for your subscription if you need to do so.

1. View recommendations in the **Microsoft Defender for Cloud** section, including the affected resource and the associated risk level. Recommendations might include enabling more security features, fixing misconfigurations, or addressing potential vulnerabilities in your AI deployments.

1. Select a recommendation to view details, and select links to take remediation action in the Azure portal.

## Enable enterprise-grade data security and compliance for Foundry with Microsoft Purview (preview)

By enabling Microsoft Purview on your Azure subscription, you can access, process, and store prompt and response data from Microsoft Foundry apps and agents. The data includes associated metadata. This integration supports key data security and compliance scenarios, such as:

- Microsoft Purview Audit
- Sensitive information type (SIT) classification
- Analytics and reporting through Microsoft Purview Data Security Posture Management (DSPM) for AI
- Microsoft Purview Insider Risk Management
- Microsoft Purview Communication Compliance
- Microsoft Purview Data Lifecycle Management
- Microsoft Purview eDiscovery

This capability helps your organization manage and monitor AI-generated data in alignment with enterprise policies and regulatory requirements. Keep these considerations in mind:

- Microsoft Purview Data Security Policies for Foundry Services interactions are supported for API calls that use Microsoft Entra ID authentication with a user-context token, or for API calls that explicitly include user context. To learn more, see [AzureUserSecurityContext](../../openai/latest.md#azureusersecuritycontext). For all other authentication scenarios, user interactions captured in Microsoft Purview appear only in Microsoft Purview Audit and AI interactions with classifications within DSPM for the AI activity explorer.

- Microsoft Purview Audit is included as part of the Microsoft Purview license for Foundry services. For setup of data security policies in Microsoft Purview by your enterprise security admins, billing is based on [pay-as-you-go](https://azure.microsoft.com/pricing/details/purview/) meters.

- Integration with Microsoft Purview for the preceding features in Foundry doesn't yet support network isolation.

- Integration with Microsoft Purview is currently available for calls made through the Microsoft Foundry inference endpoint (aka OpenAI-compatible chat completions API or /chat/completions endpoint). Every model deployed through Foundry's managed inference stack is covered by Purview.

This feature requires a Microsoft Purview license in the tenant. To learn about Microsoft Purview, see [Microsoft Purview data security and compliance protections for generative AI apps](/purview/ai-microsoft-purview).

### Enable Microsoft Purview in Foundry

You must have the Azure AI Account Owner role to enable Microsoft Purview integration.

To enable Microsoft Purview in Foundry:

1. On the toolbar, select **Operate**.

1. On the left pane, select **Compliance**.

1. Select the **Security posture** tab.

1. Select the Azure subscription.

1. Turn on the **Microsoft Purview** toggle.

    :::image type="content" source="media/how-to-manage-compliance-security/microsoft-purview-toggle.png" alt-text="Screenshot of the toggle for enabling Microsoft Purview on the tab for security posture.":::

Repeat the preceding steps for other Azure subscriptions, as appropriate.

## Related content

- [What is Azure Policy?](/azure/governance/policy/overview)
- [Microsoft Defender for Cloud documentation](/azure/defender-for-cloud/)
