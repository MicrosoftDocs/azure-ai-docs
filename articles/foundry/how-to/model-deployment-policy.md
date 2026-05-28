---
title: "Built-in policies for model deployment"
description: "Govern AI model deployment in Microsoft Foundry portal with built-in Azure Policy definitions. Approve specific models and enforce eligibility requirements such as source and lifecycle status."
#customer intent: As an IT admin, I want to control the deployment of AI models in Microsoft Foundry portal so that I can ensure compliance with organizational policies.
author: jonburchel
ms.author: jburchel
ms.reviewer: aashishb
ms.date: 05/29/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.custom:
  - dev-focus
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Built-in policies for model deployment in Microsoft Foundry portal

[!INCLUDE [model-deployment-policy 1](../includes/how-to-model-deployment-policy-1.md)]

Microsoft Foundry provides two built-in Azure Policy definitions to help you govern which models can be deployed in your organization:

| Policy | Purpose | Status |
|---|---|---|
| **Foundry model deployments should only use approved models** | Restrict deployments to a specific list of models or publishers that your organization has explicitly approved. | Generally available |
| **Foundry model deployments must meet eligibility requirements** | Restrict deployments based on model attributes such as source (Direct from Azure) and lifecycle status (Preview). | Preview |

Both policies are evaluated at **deployment time**. Models are not hidden from the catalog — instead, the **Deploy** action is disabled with a clear reason when a policy blocks the deployment. You can assign one or both policies depending on your governance needs.

> [!NOTE]
> These policies also govern the underlying models that [model router](../../openai/how-to/model-router-agents.md) selects from. Model router only routes requests to models that satisfy your assigned policies, so the same approval and eligibility rules apply whether you deploy a model directly or use model router to pick one per request.

## How these policies work together

The two policies are complementary and address different governance questions:

- **Approved models** answers *"Is this exact model on my organization's allow-list?"* — based on model identity.
- **Eligibility requirements** answers *"Does this model meet my organization's standards for source and maturity?"* — based on model attributes.

If both policies are assigned and a model is non-compliant with both, the **Deploy** experience shows the highest-priority reason first (approval, then eligibility), so users get one clear, actionable message.

## Foundry model deployments should only use approved models

Use this policy to restrict deployments to a specific list of models or publishers that your organization has explicitly approved.

> [!NOTE]
> This policy was previously named *Cognitive Services Deployments should only use approved Registry Models*. The policy definition ID is unchanged, so existing assignments continue to work without any action.

### Assign the approved-models policy

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
       --query "[?displayName=='Foundry model deployments should only use approved models'].{name:name, id:id}" \
       --output table
    ```

    Expected result: a row that includes the policy `id`.

1. Create a parameters file (example):

    ```json
    {
       "effect": {
          "value": "Deny"
       },
       "allowedPublishers": {
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
       --name "allow-only-approved-models" \
       --display-name "Allow only approved models" \
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

1. From the left side of the Azure Policy Dashboard, select **Authoring** > **Definitions**. Then search for `Foundry model deployments should only use approved models`.

1. Select **Assign** to assign the policy:

   - **Scope**: Select the scope where you want to assign the policy. The scope can be a management group, subscription, or resource group.
   - **Policy definition**: This section already has a value of `Foundry model deployments should only use approved models`.
   - **Assignment name**: Enter a unique name for the assignment.

   You can keep the default values for the rest of the fields or customize them as needed for your organization.

1. Select **Next** at the bottom of the page or the **Parameters** tab at the top of the page.

1. In the **Parameters** tab, clear **Only show parameters that need input or review** to see all fields:

   - **Effect**: Set to [**Deny**](/azure/governance/policy/concepts/effect-deny).

     > [!NOTE]
     > By using the [**audit**](/azure/governance/policy/concepts/effect-audit) option, you can configure the policy to log information to your own compliance dashboard before enforcing the policy.

   - **Allowed Models Publishers**: Enter a list of publisher names in quotes, separated by commas. Here's an example that shows where to find a publisher name:

     1. Go to the [model catalog](/azure/ai-foundry/how-to/model-catalog-overview) in the Foundry portal.
     1. Select a model (for example, GPT-5).
     1. You find publisher name on the model card as shown in the following screenshot. For example, in this case it's `OpenAI`.

        :::image type="content" source="media/model-deployment-policy/gpt-5-model-card.png" alt-text="Screenshot of model catalog showing a model card with the publisher name highlighted.":::

   - **Allowed Asset Ids**: Enter a list of model asset IDs in quotes, separated by commas.

     To get the model asset ID strings and model publisher names, use the following steps:

     1. Go to the [model catalog](https://ai.azure.com/explore/models).
     1. For each model you want to allow, select the model to view the details. In the model detail information, copy the **Model ID** value. For example, the value might look like `azureml://registries/azure-openai/models/gpt-35-turbo/versions/3` for GPT-3.5-Turbo model.

        > [!IMPORTANT]
        > The model ID value must be an exact match for the model. If the model ID isn't an exact match, the policy doesn't work as expected.

     1. Select the **Review + create** tab and verify that the policy assignment is correct. When ready, select **Create** to assign the policy.
     1. Notify your developers that the policy is in place. They receive an error message if they try to deploy a model that isn't on the list of allowed models.

---

## Foundry model deployments must meet eligibility requirements (preview)

> [!IMPORTANT]
> This policy is in **preview**. Preview features are made available for use, testing, and feedback purposes. Don't use them for production workloads. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Use this policy to restrict deployments based on **model attributes** rather than specific model identity. This is useful when you want to enforce broader organizational standards — for example, "no preview models in production" or "only Microsoft-direct models" — without maintaining an explicit allow-list.

The policy currently supports the following attributes:

| Parameter | Type | Default | Behavior when `true` |
|---|---|---|---|
| `onlyAllowDirectFromAzure` | Boolean | `false` | Denies deployment of models that are not Direct from Azure. |
| `denyPreviewModels` | Boolean | `false` | Denies deployment of models whose lifecycle status is Preview. |

Both parameters default to `false`, so an unconfigured assignment imposes no restrictions. Enable the toggles that match your organization's posture.

### Assign the eligibility policy

# [Azure CLI](#tab/cli)

1. Sign in and select the subscription you want to work in:

    ```azurecli
    az login
    az account set --subscription "<subscription-id>"
    ```

1. Find the policy definition ID:

    ```azurecli
    az policy definition list \
       --query "[?displayName=='Foundry model deployments must meet eligibility requirements'].{name:name, id:id}" \
       --output table
    ```

1. Create a parameters file (example — block Preview models, allow any source):

    ```json
    {
       "effect": {
          "value": "Deny"
       },
       "onlyAllowDirectFromAzure": {
          "value": false
       },
       "denyPreviewModels": {
          "value": true
       }
    }
    ```

1. Assign the policy:

    ```azurecli
    az policy assignment create \
       --name "foundry-model-eligibility" \
       --display-name "Foundry model eligibility" \
       --scope "/subscriptions/<subscription-id>" \
       --policy "<policy-definition-id>" \
       --params @params.json
    ```

# [Azure portal](#tab/azureportal)

1. From the [Azure portal](https://portal.azure.com/), select **Policy**.
1. Select **Authoring** > **Definitions** and search for `Foundry model deployments must meet eligibility requirements`.
1. Select **Assign**.
1. On the **Basics** tab, set the **Scope** (management group, subscription, or resource group) and an **Assignment name**.
1. On the **Parameters** tab, clear **Only show parameters that need input or review** to see all fields:

   - **Effect**: Set to [**Deny**](/azure/governance/policy/concepts/effect-deny) to block non-compliant deployments, or [**Audit**](/azure/governance/policy/concepts/effect-audit) to log them without blocking.
   - **Only Allow Direct From Azure**: Set to `true` to deny deployment of models that are not Direct from Azure. Default is `false`.
   - **Deny Preview Models**: Set to `true` to deny deployment of models whose lifecycle status is Preview. Default is `false`.

1. Select **Review + create** and then **Create** to assign the policy.

---

## What developers see when a deployment is blocked

When a developer attempts to deploy a model that is blocked by either policy, the **Deploy** action is disabled and a message explains why. The model itself remains visible in the catalog so the developer understands what was attempted.

| Scenario | What the developer sees |
|---|---|
| Model is approved and eligible | Deploy enabled. |
| Model is not on the approved list | Deploy disabled — message indicates the model is not approved by the organization, with a pointer to contact the subscription or Foundry administrator. |
| Model is approved but does not meet eligibility (for example, a Preview model when `denyPreviewModels` is on) | Deploy disabled — message indicates the model does not meet the organization's eligibility requirements (source or lifecycle status), with a pointer to contact the administrator. |
| Multiple policies block the deployment | Deploy disabled — the highest-priority reason is shown (approval, then eligibility). |

Each message includes the **policy name** and **assignment ID** so administrators can quickly identify which policy is enforcing the restriction.

[!INCLUDE [model-deployment-policy 2](../includes/how-to-model-deployment-policy-2.md)]
