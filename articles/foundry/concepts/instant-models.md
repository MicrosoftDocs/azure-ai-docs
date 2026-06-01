---
title: "Instant models in Microsoft Foundry (preview)"
description: "Learn about instant models in Microsoft Foundry, which let you call any supported model by name without creating a deployment first."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 05/18/2026
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
ms.custom:
  - update-code1
# customer intent: As a developer, I want to understand how instant models work so that I can call models without creating deployments first.
---

# Instant models in Microsoft Foundry (preview)

Instant models let you call any supported model by name — no deployment required. Create a Foundry project, start coding, and use any available model immediately.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- [!INCLUDE [foundry-sign-in](../includes/foundry-sign-in.md)]
- A Foundry project in **West US 3** (the only supported region for instant models during preview). If you need to create a project, see [Create a project](../how-to/create-projects.md).
- The **Foundry User** role on the project or account.

[!INCLUDE [foundry-role-rename-note](../includes/role-rename-note.md)]

## Start using models instantly

With instant models, the workflow is simple — use a supported instant model name in your code. No deployment needed. The same API, SDK, and client you already use for deployments works with instant models. No second SDK, no separate client, no configuration changes.

# [Python](#tab/python)

The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/responses/quickstart-responses.py":::

 # [C#](#tab/csharp)

 The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/responses/quickstart-responses.cs":::

# [TypeScript](#tab/typescript)

The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/responses/src/quickstart-responses.ts":::

# [Java](#tab/java)

The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/responses/src/main/java/com/azure/ai/agents/CreateResponse.java":::

# [REST API](#tab/rest)

The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.
Also replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-responses.sh":::

# [Foundry portal](#tab/portal)

1. On the Home page of your project, select **Test in playground**. (This might instead be labeled **Explore playgrounds**).
    
    <!-- :::image type="content" source="../media/instant-models/playground.png" alt-text="Screenshot of Test in playground card with description to test models and get API key and endpoint."::: -->

1. Use the **Model** dropdown in the playground to switch among deployed and instant models.

---


### Why instant models matter

- **Switch models by changing one string** — use any instant model name in the `model=` line, without creating or deleting deployments.
- **Same API and SDK** — the same calls work for both instant models and deployments.
- **Works with your dev tools** — instant models integrate with Foundry CLI, VS Code, and CI/CD pipelines the same way deployments do.

Deployments aren't going away. They remain the right choice when you need reserved throughput, custom content filters, data residency, or advanced enterprise configurations. Instant models simplify the getting-started experience so that deployments become something you level up to, not a gate you must pass before you can use a model.

## Supported models

New models support instant access by default when they're released. Support for additional models is considered based on customer demand.

To see all models that support instant access:

1. Open a project in **West US 3** in the new Foundry experience, 
1. Select **Discover** in the upper-right navigation, then **Models** in the left pane.
1. In the model catalog, select **Instant** under **Development options** to view the available instant models.

You can also list instant models programmatically:

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
LOCATION="westus3"

az rest --method get \
  --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/providers/Microsoft.CognitiveServices/locations/$LOCATION/models?api-version=2025-06-01" \
  --output json \
| jq -r '(.value // .models // .)[]
  | select((.model.capabilities.instant // "false" | tostring | ascii_downcase) == "true")
  | .model.name' \
| sort -u
```

> [!NOTE]
> During the preview, instant models are available in projects in **West US 3** only.

> [!NOTE]
> Some instant models might appear in the list even if your subscription has no
> quota for them. For more information, see
> [Quotas and limits for Foundry Models](../foundry-models/quotas-limits.md).

## When to use instant models vs. deployments

| Scenario | Recommended approach |
|---|---|
| Getting started, prototyping, or experimentation | Instant models |
| Using the latest model immediately after release | Instant models |
| Need reserved capacity or [predictable throughput](../foundry-models/concepts/deployment-types.md) | Deployment |
| Require [provisioned throughput (PTU)](../openai/concepts/provisioned-throughput.md) | Deployment |
| Need [data residency](../foundry-models/concepts/deployment-types.md) in a specific region | Deployment |
| Custom [content filtering](../guardrails/guardrails-overview.md) policies per model | Deployment |
| Custom [guardrails](../guardrails/guardrails-overview.md) per model | Deployment |
| Endpoint-specific configuration (for example, version locks per endpoint) | Deployment |
| Fine-grained [quota](../how-to/quota.md) partitioning across teams | Deployment |
| [Fine-tuned models](../fine-tuning/fine-tune-cli.md) | Deployment |

Instant models and deployments can coexist in the same project. You can start with instant models and create deployments later as your requirements evolve.

## Model versions

By default, instant models route to the latest evergreen version of a model. To pin to a specific version, append the version date to the model name as a hyphenated suffix:

| What you pass as `model` | Behavior |
|---|---|
| `model-name` | Routes to the latest version |
| `model-name-2025-04-01` | Routes to that specific version |

Version pinning is opt-in. If your application requires stability, include the version suffix. Otherwise, you always get the latest version automatically.

## How quota is consumed

Instant models draw from a per-model **global quota** pool assigned to your subscription. This quota is separate from the regional quota used by standard deployments.

- You don't allocate or partition global quota — it's shared automatically across all instant model usage in your subscription.
- Global Standard deployments reserve a portion of your global quota. Instant models use whatever capacity remains.
- Other deployment types (Regional Standard, Provisioned) use separate regional quota and don't affect your instant model capacity.
- If instant model requests are throttled, you can request a quota increase or create a deployment with reserved capacity.

For more details on how global and regional quotas interact, see [Manage and increase quotas](../how-to/quota.md).

## Enterprise controls

| Capability | How it works |
|---|---|
| Block specific models or providers | Azure Policy definitions apply to instant models the same way they apply to deployments |
| Pin to a model version | Append the version suffix to the model name (see [Model versions](#model-versions)) |
| Disable instant models entirely | Administrators can turn off instant models at the subscription level through Azure Policy |

To remove instant models from an account, configure the settings through Bicep
or ARM REST.

### [REST API](#tab/rest-api)

Update your account with:

```http
PATCH https://management.azure.com/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}?api-version=2026-01-15-preview
Authorization: Bearer {arm_token}
Content-Type: application/json
```

Use this request body to effectively shut off instant model access:

```json
{
  "properties": {
    "instant": {
      "raiPolicyName": "Microsoft.DefaultV2",
      "modelAllowList": []
    }
  }
}
```

### [Bicep](#tab/bicep)

Update your existing account resource with an `instant` block:

```bicep
resource account 'Microsoft.CognitiveServices/accounts@2026-01-15-preview' = {
  name: accountName
  location: location
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  // Keep your existing account properties and add instant settings.
  properties: {
    instant: {
      raiPolicyName: 'Microsoft.DefaultV2'
      modelAllowList: []
    }
  }
}
```

---

> [!IMPORTANT]
> All instant models use default [guardrails](../guardrails/guardrails-overview.md) and content filters. However, you can't configure custom guardrails or Responsible AI (RAI) policies on a per-model basis for instant models. You can set a default RAI policy at the account level through the API, but that policy applies uniformly to all instant models. If you need different content filtering policies for individual models, use a deployment.

## Deployment name collisions

New deployments can't use a name that matches an existing model name. If you have an existing deployment whose name collides with a model name, the deployment takes precedence and instant model access for that model name is unavailable in that project.

## Limitations during preview

- Available in **West US 3** only.
- Fine-tuned models aren't supported. To use a fine-tuned model, create a deployment.
- [Guardrails](../guardrails/guardrails-overview.md), custom RAI policies, and content filters aren't configurable for instant models.
- Only the models listed in [Supported models](#supported-models) are eligible.

## Related content

- [Deployment overview for Microsoft Foundry Models](deployments-overview.md)
- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Manage quotas for Foundry resources](../how-to/quota.md)
- [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)
