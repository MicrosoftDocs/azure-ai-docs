---
title: Built-in policy for model deployment
description: Manage AI model deployment in Microsoft Foundry portal with built-in Azure Policy definitions. Learn how to govern and manage model deployments effectively.
monikerRange: 'foundry-classic || foundry'
#customer intent: As an IT admin, I want to control the deployment of AI models in Microsoft Foundry portal so that I can ensure compliance with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 01/05/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Built-in policy for model deployment in Microsoft Foundry portal

[!INCLUDE [version-banner](../includes/version-banner.md)]

Azure Policy provides built-in policy definitions that help you govern the deployment of AI models in Microsoft Foundry portal. You can use
these policies to control what models your developers can deploy in the Foundry portal.

## Prerequisites

- An Azure account with an active subscription. If you don't have one, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Your
  Azure account lets you access the Foundry portal.

- Permissions to create and assign policies. To create and assign policies, you must be an [Owner](/azure/role-based-access-control/built-in-roles#owner) or [Resource Policy Contributor](/azure/role-based-access-control/built-in-roles#resource-policy-contributor) at the Azure subscription or resource group level.

- Familiarity with Azure Policy. To learn more, see [What is Azure Policy?](/azure/governance/policy/overview).

## Assign the policy 

# [Azure CLI](#tab/cli)

Use Azure CLI to find the built-in policy definition and assign it at a scope.

1. Sign in and select the subscription you want to work in:

    ```azurecli
    az login
    az account set --subscription "<subscription-id>"
    ```

1. Find the policy definition ID for the built-in definition:

    ```azurecli
    az policy definition list \
       --query "[?displayName=='Cognitive Services Deployments should only use approved Registry Models'].{name:name, id:id}" \
       --output table
    ```

    Expected result: a row that includes the policy `id`.

1. Create a parameters file (example):

    ```json
    {
       "effect": {
          "value": "Deny"
       },
       "allowedModelsPublishers": {
          "value": ["OpenAI"]
       },
       "allowedAssetIds": {
          "value": [
             "azureml://registries/azure-openai/models/gpt-35-turbo/versions/3"
          ]
       }
    }
    ```

    Expected result: a JSON file that matches your approved publisher names and model IDs.

    > [!IMPORTANT]
    > The parameter names in this example must match the policy definition you assign. If they differ in your tenant, update the JSON keys to match the policy definition parameters.

1. Assign the policy at a scope (example: subscription scope):

    ```azurecli
    az policy assignment create \
       --name "allow-only-approved-registry-models" \
       --display-name "Allow only approved registry models" \
       --scope "/subscriptions/<subscription-id>" \
       --policy "<policy-definition-id>" \
       --params @params.json
    ```

    Expected result: the command returns a JSON payload that includes the assignment `id`.

Reference:
- [az policy definition list](/cli/azure/policy/definition#az-policy-definition-list)
- [az policy assignment create](/cli/azure/policy/assignment#az-policy-assignment-create)
- [Azure Policy assignments](/azure/governance/policy/concepts/assignment-structure)

# [Azure portal](#tab/azureportal)

1. From the [Azure portal](https://portal.azure.com/), select **Policy** from the left side of the page. You can also
   search for **Policy** in the search bar at the top of the page.

1. From the left side of the Azure Policy Dashboard, select **Authoring** > **Definitions**. Then search for `Cognitive Services Deployments should only use approved Registry Models`.

1. Select **Assign** to assign the policy:

   - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
   - **Policy definition**: This section already has a value of `Cognitive Services Deployments should only use approved Registry Models`.
   - **Assignment name**: Enter a unique name for the assignment.

   You can keep the default values for the rest of the fields or customize them as needed for your organization.

1. Select **Next** at the bottom of the page or the **Parameters** tab at the top of the page.

1. In the **Parameters** tab, clear **Only show parameters that need input or review** to see all fields:

   - **Effect**: Set to [**Deny**](/azure/governance/policy/concepts/effect-deny).

     > [!NOTE]
     > By using the [**audit**](/azure/governance/policy/concepts/effect-audit) option, you can configure the policy to log information to your own compliance dashboard.

   - **Allowed Models Publishers**: Enter a list of publisher names in quotes, separated by commas. Here's an example that shows where to find a publisher name:

     ::: moniker range="foundry-classic"

     1. Go to the [Foundry model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in the Foundry portal:
     1. Select a model (for example, GPT-5).
     1. You find publisher name on the model card as shown in the following screenshot. For example, in this case it's `OpenAI`.

        :::image type="content" source="media/model-deployment-policy/gpt-5-model-card.png" alt-text="Screenshot of model catalog showing a model card with the publisher name highlighted.":::

     ::: moniker-end

     ::: moniker range="foundry"

     1. Go to the [model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in the Foundry portal.
     1. Select a model (for example, GPT-5).
     1. You find publisher name on the model card as shown in the following screenshot. For example, in this case it's `OpenAI`.

        :::image type="content" source="media/model-deployment-policy/gpt-5-model-card.png" alt-text="Screenshot of model catalog showing a model card with the publisher name highlighted.":::

     ::: moniker-end

   - **Allowed Asset Ids**: Enter a list of model asset IDs in quotes, separated by commas.

     To get the model asset ID strings and model publisher names, use the following steps:

     1. Go to the [model catalog](https://ai.azure.com/explore/models).
     1. For each model you want to allow, select the model to view the details. In the model detail information, copy the **Model ID** value. For example, the value might look like `azureml://registries/azure-openai/models/gpt-35-turbo/versions/3` for GPT-3.5-Turbo model.

        > [!IMPORTANT]
        > The model ID value must be an exact match for the model. If the model ID isn't an exact match, the policy doesn't work as expected.

     1. Select the **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.
     1. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't on the list of allowed models.

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

## Related content

- [Azure Policy overview](/azure/governance/policy/overview)
- [Model catalog overview](/azure/ai-foundry/how-to/model-catalog-overview)
