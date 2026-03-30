---
title: "Upgrade Azure OpenAI to Microsoft Foundry (classic)" 
description: "Upgrade your Azure OpenAI resource to Microsoft Foundry to access advanced capabilities including a broader model catalog, agents service, and evaluation tools. Learn how to upgrade seamlessly. (classic)"
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 01/07/2026
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - dev-focus
  - classic-and-new
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Upgrade from Azure OpenAI to Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/upgrade-azure-openai.md)

[!INCLUDE [upgrade-azure-openai 1](../../foundry/includes/how-to-upgrade-azure-openai-1.md)]

## Benefits of upgrading

When you upgrade your Azure OpenAI resource to a Foundry resource, you get access to the following capabilities.

| Feature | Azure OpenAI | Foundry |
|---|---|---|
| Models sold directly by Azure | Azure OpenAI only | Azure OpenAI, Black Forest Labs, DeepSeek, Meta, xAI, Mistral, Microsoft  |
| Partner and community models sold through Marketplace - Stability, Cohere, and others |  | ✅ |
| Azure OpenAI API - batch, stored completions, fine-tuning, evaluation, and more | ✅ | ✅ |
| Agent service | | ✅ |
| Azure Foundry API |  | ✅ |
| Foundry Tools - Speech, Vision, Language, Content Understanding | | ✅ |

Your existing resource configurations and state stay the same, including:

* Resource name
* Azure resource tags
* Network configurations
* Access and identity configurations
* API endpoint and API key
* Custom Domain Name
* Existing state including fine-tuning jobs, batch, stored completions, and more

[!INCLUDE [upgrade-azure-openai 2](../../foundry/includes/how-to-upgrade-azure-openai-2.md)]

## Considerations for RBAC and policy during upgrade

Microsoft Foundry provides a broader set of models and capabilities than an Azure OpenAI resource. If your organization relies on Azure RBAC or Azure Policy, these controls continue to function after upgrade because both resource types use the same management APIs.

However, **IT administrators should review any wildcard role assignments or policies that don't restrict access to a specific resource kind.** These broad definitions might unintentionally grant users access to Foundry-only features immediately after upgrade.

If you plan to roll out non-OpenAI features gradually, update your RBAC role assignments, Azure Policy definitions, and any custom roles before you perform the upgrade. For details on permissions, see [Role Based Access Control](../concepts/rbac-foundry.md).

Post-upgrade behavior depends on your existing governance setup:

|Governance control|Access before upgrade|Access after upgrade|
|---|---|---|
|[Cognitive Services User (RBAC role)](/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-user)|OpenAI features|All Foundry features |
|[Cognitive Services OpenAI User (RBAC role)](/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-openai-user)|OpenAI features|OpenAI features|
|[Custom RBAC roles](/azure/role-based-access-control/custom-roles)|Only features you defined|Only features you defined|
|Model access (no policy applied)|OpenAI models|Any Foundry model|
|[Model access (policy enforced)](model-deployment-policy.md)|Only OpenAI models allowed by policy|Only models you allow through policy|

[!INCLUDE [upgrade-azure-openai 3](../../foundry/includes/how-to-upgrade-azure-openai-3.md)]

## Troubleshooting common issues

Azure resource limits and organizational configurations might require extra steps to complete the upgrade. The following table outlines some of the most common issues along with recommended solutions to help troubleshooting.

|Issue|Solution or mitigation|
|---|---|
|User principal lacks account or write permissions|Get a privileged Azure RBAC role to manage top-level Azure resource. For example, **Owner**, **Contributor**, or **Azure AI Administrator**.| 
|Managed identity isn't enabled on the Azure OpenAI resource|Configure managed identity on your resource by using templates or Azure portal.|
|No permissions to create agents, while you're the owner or contributor on the resource.|An EntraID data plane role is required for development actions including agents. Examples include **Azure AI User**, **Azure AI Project Manager**, or **Azure AI Owner** roles. **Owner** and **Contributor** roles only grant access to management operations in Azure such as managing deployments.|
|An Azure Policy conflict occurred.|Your organization might put constraints on resource configurations. Inspect the details of the policy violation error. Then upgrade your resource via template options for further customization. For example, network configurations for Agents can only be configured via template options such as Azure Bicep.|
|Exceeded number of Azure OpenAI instances of 30 per subscription per region when rolling back.|Delete an Azure OpenAI resource or upgrade it to the Foundry. Then retry rolling back your current resource.|
|Exceeded number of AIServices instances of 100 per subscription per region.|Delete a Foundry resource you might not use in this subscription. Then retry upgrading your current resource.|
|I can't access my resource over the private network|See [private networking configuration](#private-network-configuration) for the required steps.|

[!INCLUDE [upgrade-azure-openai 4](../../foundry/includes/how-to-upgrade-azure-openai-4.md)]

## Related content

* [Choose an Azure resource type for AI foundry](../concepts/resource-types.md)
* [Bicep samples for Foundry common infrastructure configurations](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep)
