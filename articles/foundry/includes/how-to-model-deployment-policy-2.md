---
title: Include file
description: Include file
author: jonburchel
ms.reviewer: aashishb
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Monitor compliance

To monitor compliance with the policy, follow these steps:

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Compliance**. Each policy assignment is listed with the compliance status. To view more details, select the policy assignment.

## Update the policy assignment

To update an existing policy assignment with new models, follow these steps:

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Assignments** and find the existing policy assignment. Select the ellipsis (...) next to the assignment and select **Edit assignment**.
1. From the **Parameters** tab, update **Allowed Asset Ids** and **Allowed Models Publishers** with the new approved model IDs and publisher names.
1. From the **Review + Save** tab, select **Save** to update the policy assignment.

## Best practices

- **Granular scoping**: Assign policies at the appropriate scope to balance control and flexibility. For example, apply at the subscription level to control all resources in the subscription, or apply at the resource group level to control resources in a specific group.
- **Policy naming**: Use a consistent naming convention for policy assignments to make it easier to identify the purpose of the policy. Include information such as the purpose and scope in the name.
- **Tags**: Use tags to categorize and manage your policies. For example, tag policies by environment (dev, test, prod) or by department.
- **Documentation**: Keep records of policy assignments and configurations for auditing purposes. Document any changes made to the policy over time.
- **Regular reviews**: Periodically review policy assignments to ensure they align with your organization's requirements.
- **Testing**: Test policies in a nonproduction environment before applying them to production resources.
- **Communication**: Make sure developers are aware of the policies in place and understand the implications for their work.

## Verify policy effectiveness

After you assign the policy, verify that it works as expected:

1. Wait at least 15 minutes for the policy assignment to take effect. New assignments don't apply instantly.

1. Attempt to deploy a model that isn't on the allowed list. If the policy uses the **Deny** effect, the deployment fails with a policy violation error.

1. Confirm that deploying an approved model still succeeds.

1. Check the **Compliance** dashboard in Azure Policy to verify that the policy evaluates resources correctly. Noncompliant resources appear within one compliance evaluation cycle (typically up to 24 hours).

## Troubleshoot policy assignment failures

| Symptom | Cause | Resolution |
|---|---|---|
| Policy assignment fails with a permissions error | Your account lacks the **Owner** or **Resource Policy Contributor** role at the target scope. | Assign the required role and retry. See [Prerequisites](#prerequisites). |
| Policy doesn't block noncompliant deployments | The policy assignment hasn't propagated yet, or the effect is set to **Audit** instead of **Deny**. | Wait at least 15 minutes, then retry. Verify that the **Effect** parameter is set to **Deny**. |
| Approved model is blocked unexpectedly | The model asset ID or publisher name in the policy parameters doesn't match the model exactly. | Compare the parameter values against the model card in the [model catalog](https://ai.azure.com/explore/models). Asset IDs and publisher names are case-sensitive. |
| Compliance dashboard shows no data | Compliance evaluation hasn't completed yet. Azure Policy evaluates new assignments within 24 hours. | Wait for the next evaluation cycle or trigger an [on-demand evaluation scan](/azure/governance/policy/how-to/get-compliance-data#on-demand-evaluation-scan). |
| Parameter name mismatch error during assignment | The JSON parameter keys don't match the policy definition. | Run `az policy definition show --name "<definition-id>"` to retrieve the exact parameter names from the definition. Use `allowedPublishers` and `allowedAssetIds`. |

## Related content

- [Azure Policy overview](/azure/governance/policy/overview)
- [Model catalog overview](/azure/ai-foundry/how-to/model-catalog-overview)
