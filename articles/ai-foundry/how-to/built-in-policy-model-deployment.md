---
title: Control AI model deployment with built-in policies
titleSuffix: Azure AI Foundry
description: "Learn how to use built-in Azure policies to control what managed AI Services (standard deployment) and Model-as-a-Platform (MaaP) AI models can be deployed in Azure AI Foundry portal."
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-foundry
ms.topic: how-to #Don't change
ms.date: 02/19/2025

#customer intent: As an admin, I want control what Managed AI Services (standard deployment) and Model-as-a-Platform (MaaP) AI models can be deployed by my developers.

---

# Control AI model deployment with built-in policies in Azure AI Foundry portal

Azure Policy provides built-in policy definitions that help you govern the deployment of AI models in Managed AI Services (standard deployment) and Model-as-a-Platform (MaaP). You can use these policies to control what models your developers can deploy in Azure AI Foundry portal.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/) before you begin.
- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.
- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Enable the policy

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Authoring**, **Definition**, and then search for "[Preview]: Azure Machine Learning Deployments should only use approved Registry Models" in the search bar within the page. You can also directly navigate to [policy definition creation page](https://portal.azure.com/#blade/Microsoft_Azure_Policy/PolicyDetailBlade/definitionId/%2Fproviders%2FMicrosoft.Authorization%2FpolicyDefinitions%2F12e5dd16-d201-47ff-849b-8454061c293d).
1. Select on **Assign** to assign the policy to the management group:

    - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
    - **Policy definition**: this section should already have a value of "**[Preview]: Azure Machine Learning Deployments should only use approved Registry Models**".
    - **Assignment name**: Enter a unique name for the assignment.

    The rest of the fields can be left as their default values or you can customize as needed for your organization.

1. Select **Next** at the bottom of the page or the **Parameters** tab at the top of the page.
1. In the **Parameters** tab, deselect **Only show parameters that needs input or review** to see all fields:

    - **Effect**: Set to [**Deny**](/azure/governance/policy/concepts/effect-deny).
        > [!NOTE]
        > Using the [audit](/azure/governance/policy/concepts/effect-audit) option allows you to configure the policy to log information to your own compliance dashboard.
    - **Allowed Models Publishers**: This field expects a list of **publisher's name** in quotation and separated by commas.
    - **Allowed Asset Ids**: This field expects a list of **model asset ids** in quotation and separated by commas.

        To get the model asset ID strings and model publishers' name use the following steps:

        1. Go to the [Azure AI Foundry model catalog](model-catalog-overview.md).


        1. For each model you want to allow, select the model to view the details. In the model detail information, copy the **Model ID** value. For example, the value might look like `azureml://registries/azure-openai/models/gpt-35-turbo/versions/3` for GPT-3.5-Turbo model. The provided names are also *Collections* in model catalog. For example, the publisher for "Meta-Llama-3.1-70B-Instruct" model is Meta. 
        
            > [!IMPORTANT]
            > The model ID value must be an exact match for the model. If the model ID is not an exact match, the model won't be allowed.


1. Select **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.
1. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't in the list of allowed models.

## Monitor compliance

To monitor compliance with the policy, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Compliance**. Each policy assignment is listed with the compliance status. To view more details, select the policy assignment.

## Update the policy assignment

To update an existing policy assignment with new models, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
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
- [Azure AI Foundry model catalog](model-catalog-overview.md)
