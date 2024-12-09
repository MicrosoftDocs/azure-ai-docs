---
title: Control AI model deployment with custom policies
titleSuffix: Azure AI Foundry
description: "Learn how to use custom Azure Policies to control Azure AI services and Azure OpenAI model deployment with Azure AI Foundry."
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-studio
ms.topic: how-to #Don't change
ms.date: 10/25/2024

#customer intent: As an admin, I want control what Azure AI services and Azure OpenAI models can be deployed by my developers.

---

# Control AI model deployment with custom policies in Azure AI Foundry portal

When using models from Azure AI services and Azure OpenAI with Azure AI Foundry, you might need to use custom policies to control what models your developers can deploy. Custom Azure Policies allow you to create policy definitions that meet your organization's unique requirements. This article shows you how to create and assign an example custom policy to control model deployment.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/) before you begin.
- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.
- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Create a custom policy

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Authoring**, **Definitions**, and then select **+ Policy definition** from the top of the page.
1. In the **Policy Definition** form, use the following values:

    - **Definition location**: Select the subscription or management group where you want to store the policy definition.
    - **Name**: Enter a unique name for the policy definition. For example, `Custom allowed Azure AI services and Azure OpenAI models`.
    - **Description**: Enter a description for the policy definition.
    - **Category**: You can either create a new category or use an existing one. For example, "AI model governance."
    - **Policy rule**: Enter the policy rule in JSON format. The following example shows a policy rule that allows the deployment of specific Azure AI services and Azure OpenAI models:

        > [!TIP]
        > Azure AI services was originally named Azure Cognitive Services. This name is still used internally by Azure, such as this custom policy where you see a value of `Microsoft.CognitiveServices`. Azure OpenAI is part of Azure AI services, so this policy also applies to Azure OpenAI models.

        ```json
        {
              "mode": "All",
              "policyRule": {
                "if": {
                  "allOf": [
                    {
                      "field": "type",
                      "equals": "Microsoft.CognitiveServices/accounts/deployments"
                    },
                    {
                      "not": {
                        "value": "[concat(field('Microsoft.CognitiveServices/accounts/deployments/model.name'), ',', field('Microsoft.CognitiveServices/accounts/deployments/model.version'))]",
                        "in": "[parameters('allowedModels')]"
                      }
                    }
                  ]
                },
                "then": {
                  "effect": "deny"
                }
              },
              "parameters": {
                "allowedModels": {
                  "type": "Array",
                  "metadata": {
                    "displayName": "Allowed AI models",
                    "description": "The list of allowed models to be deployed."
                  }
                }
              }
        }
        ```

1. Select **Save** to save the policy definition. After saving, you arrive at the policy definition's overview page.
1. From the policy definition's overview page, select **Assign policy** to assign the policy definition.
1. From the **Assign policy** page, use the following values on the **Basics** tab:

    - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
    - **Policy definition**: This field is prepopulated with the title of policy definition you created previously.
    - **Assignment name**: Enter a unique name for the assignment.
    - **Policy enforcement**: Make sure that the **Policy enforcement** field is set to **Enabled**. If it isn't enabled, the policy isn't enforced.

    Select **Next** at the bottom of the page, or the **Parameters** tab at the top of the page.
1. From the **Parameters** tab, set **Allowed AI models** to the list of models that you want to allow. The list should be a comma-separated list of model names and approved versions, surrounded by square brackets. For example, `["gpt-4,0613", "gpt-35-turbo,0613"]`.

    > [!TIP]
    > You can find the model names and their versions in the [Azure AI Foundry Model Catalog](https://ai.azure.com/explore/models). Select the model to view the details, and then copy the model name and their version in the title.

1. Optionally, select the **Non-compliance messages** tab at the top of the page and set a custom message for noncompliance.
1. Select **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.
1. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't in the list of allowed models.

## Verify policy assignment

To verify that the policy is assigned, navigate to **Policy** in the Azure portal, and then select **Assignments** under **Authoring**. You should see the policy listed.

## Monitor compliance

To monitor compliance with the policy, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Compliance**. Each policy assignment is listed with the compliance status. To view more details, select the policy assignment.

## Update the policy assignment

To update an existing policy assignment with new models, follow these steps:

1. From the [Azure portal](https://portal.azure.com), select **Policy** from the left side of the page. You can also search for **Policy** in the search bar at the top of the page.
1. From the left side of the Azure Policy Dashboard, select **Assignments** and find the existing policy assignment. Select the ellipsis (...) next to the assignment and select **Edit assignment**.
1. From the **Parameters** tab, update the **Allowed models** parameter with the new models.
1. From the **Review + Save** tab, select **Save** to update the policy assignment.

## Best practices

- **Obtaining model names**: Use the [Azure AI Foundry Model Catalog](https://ai.azure.com/explore/models), then select the model to view details. Use the model name in the title with the policy.
- **Granular scoping**: Assign policies at the appropriate scope to balance control and flexibility. For example, apply at the subscription level to control all resources in the subscription, or apply at the resource group level to control resources in a specific group.
- **Policy naming**: Use a consistent naming convention for policy assignments to make it easier to identify the purpose of the policy. Include information such as the purpose and scope in the name.
- **Documentation**: Keep records of policy assignments and configurations for auditing purposes. Document any changes made to the policy over time.
- **Regular reviews**: Periodically review policy assignments to ensure they align with your organization's requirements.
- **Testing**: Test policies in a nonproduction environment before applying them to production resources.
- **Communication**: Make sure developers are aware of the policies in place and understand the implications for their work.

## Related content

- [Azure Policy overview](/azure/governance/policy/overview)
- [Azure AI Foundry model catalog](model-catalog-overview.md)
- [Azure AI services documentation](/azure/ai-services)

