---
title: Built-in policy for model deployment (Preview)
description: Manage AI model deployment in Azure AI Foundry Portal with built-in Azure Policy definitions. Learn how to govern and manage model deployments effectively.
#customer intent: As an IT admin, I want to control the deployment of AI models in Azure AI Foundry Portal so that I can ensure compliance with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 09/22/2025
ms.topic: how-to
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Built-in policy for model deployment in Azure AI Foundry portal (Preview)

Azure Policy provides built-in policy definitions that help you govern the deployment of AI models in Azure AI Foundry Portal. You can use
these policies to control what models your developers can deploy in Azure AI Foundry portal.

## Prerequisites

- An Azure account with an active subscription. If you don't have one, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Your
  Azure account lets you access the Azure AI Foundry portal.

- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.

- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Enable the policy

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also
   search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Authoring**, **Definition**, and then search for `\[Preview\]: Cognitive Services Deployments should only use approved Registry Models` in the search bar within the page. You can also directly navigate to [policy definition creation page](https://ms.portal.azure.com/#view/Microsoft_Azure_Policy/PolicyDetail.ReactView/id/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2Faafe3651-cb78-4f68-9f81-e7e41509110f/version/1.0.0-preview/scopes~/%5B%22%2Fsubscriptions%2Fa4393d89-7e7f-4b0b-826e-72fc42c33d1f%22%2C%22%2Fsubscriptions%2Fd128f140-94e6-4175-87a7-954b9d27db16%22%2C%22%2Fsubscriptions%2F562da9fc-fd6e-4f24-a6aa-99827a7f6f91%22%5D/contextRender~/false).

1. Select on **Assign** to assign the policy:

   - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
   - **Policy definition**: this section should already have a value of `\[Preview\]: Cognitive Services Deployments should only use approved Registry Models`.
   - **Assignment name**: Enter a unique name for the assignment.

   The rest of the fields can be left as their default values or you can customize as needed for your organization.

1. Select **Next** at the bottom of the page or the **Parameters** tab at the top of the page.

1. In the **Parameters** tab, deselect **Only show parameters that needs input or review** to see all fields:

   - **Effect**: Set to [**Deny**](/azure/governance/policy/concepts/effect-deny).

     > [!NOTE]
     > Using the [**audit**](/azure/governance/policy/concepts/effect-audit) option allows you to configure the policy to log information to your own compliance dashboard.

   - **Allowed Models Publishers**: This field expects a list of **publisher's name** in quotation and separated by commas. Here's an example that shows where to find a publisher name:

     1. Go to [Azure AI Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in Foundry Portal
     1. Select a model (for example, GPT-5).
     1. You find publisher name on the model card as shown in the following screenshot. For example, in this case it's `OpenAI`.

        :::image type="content" source="media/model-deployment-policy/gpt-5-model-card.png" alt-text="Screenshot of Azure AI Foundry model catalog showing a model card with the publisher name highlighted.":::

   - **Allowed Asset Ids**: This field expects a list of **model asset ids** in quotation and separated by commas.

     To get the model asset ID strings and model publishers' name use the following steps:

     1. Go to the [Azure AI Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview).
     1. For each model you want to allow, select the model to view the details. In the model detail information, copy the **Model ID** value. For example, the value might look like `azureml://registries/azure-openai/models/gpt-35-turbo/versions/3` for GPT-3.5-Turbo model.

        > [!IMPORTANT]
        > The model ID value must be an exact match for the model. If the model ID isn't an exact match, policy doesn't work as expected.

     1. Select **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.
     1. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't on the list of allowed models.

## Monitor compliance

To monitor compliance with the policy, follow these steps:

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Compliance**. Each policy assignment is listed with the compliance status. To view more details, select the policy assignment.

## Update the policy assignment

To update an existing policy assignment with new models, follow these steps:

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Assignments** and find the existing policy assignment. Select the ellipsis (...) next to the assignment and select **Edit assignment**.
1. From the **Parameters** tab, update the **Allowed models** parameter with the new model IDs.
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
- [Azure AI Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview)
