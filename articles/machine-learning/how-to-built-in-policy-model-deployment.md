---
title: Control AI model deployment with built-in policies
titleSuffix: Azure Machine Learning
description: "Learn how to use built-in Azure policies to control what managed Foundry Tools (standard deployment) and Model-as-a-Platform (MaaP) AI models can be deployed."
author: s-polly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.topic: how-to #Don't change
ms.date: 02/19/2025

#customer intent: As an admin, I want control what Managed Foundry Tools (standard deployment) and Model-as-a-Platform (MaaP) AI models can be deployed by my developers.

---

# Control AI model deployment with built-in policies in Azure Machine Learning

Azure Policy provides built-in policy definitions that help you govern the deployment of AI models in Managed Foundry Tools (standard deployment) and Model-as-a-Platform (MaaP). You can use these policies to control what models your developers can deploy.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.
- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Enable the policy

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Authoring**, **Assignments**, and then select **Assign policy** from the top of the page.
1. In the **Policy Assignment** form, use the following values:

    - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
    - **Policy definition**: Select the ellipse (...) and search for **Allowed models for AI model deployment**. Select the policy definition from the list. For example, **Allowed models for AI model deployment in standard deployment and MaaP**.
    - **Assignment name**: Enter a unique name for the assignment.

    The rest of the fields can be left as their default values or you can customize as needed for your organization.

1. Select **Next** at the bottom of the page or the **Parameters** tab at the top of the page.
1. In the **Parameters** tab, use the following fields:

    - **Allowed models**: This field expects the **model ID strings**, separated by commas. To get the model ID strings, use the following steps:

        1. Go to the [Azure Machine Learning Model Catalog](https://ml.azure.com/model/catalog) for your workspace.
        
            > [!NOTE]
            > You must have an Azure Machine Learning workspace to access the Model Catalog.

        1. For each model you want to allow, select the model to view the details. In the model detail information, copy the **Model ID** value. For example, the value might look like `azureml://registries/azure-openai/models/gpt-35-turbo/versions/3`.
        
            > [!IMPORTANT]
            > The model ID value must be an exact match for the model. If the model ID is not an exact match, the model won't be allowed.

    - **Effect**: This field determines whether the policy [audits](/azure/governance/policy/concepts/effect-audit) or [denies](/azure/governance/policy/concepts/effect-deny) the use of the models listed in the **Allowed models** field.

1. Optionally, select the **Non-compliance messages** tab at the top of the page and set a custom message for noncompliance.
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
- [Azure Machine Learning model catalog](concept-model-catalog.md)
