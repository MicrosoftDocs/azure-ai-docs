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
  - build-2025
# customer intent: As a developer, I want to understand how instant models work so that I can call models without creating deployments first.
---

# Instant models in Microsoft Foundry (preview)

Instant models let you call any supported model by name — no deployment required. Create a Foundry project, start coding, and use any available model immediately.

## Start using models instantly

With instant models, the workflow is:

1. Create a Foundry project in **West US 3** (the only supported region during preview).
1. Use a supported instant model name in your code. No deployment needed. The same API, SDK, and client you already use for deployments works with instant models. No second SDK, no separate client, no configuration changes.

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

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/chat-with-agent/src/main/java/com/azure/ai/agents/ChatWithAgent.java":::

# [REST API](#tab/rest)

The only change from deployment-based code is the `model` parameter. In the code below, replace `"gpt-5-mini"` with the name any instant model.
Also replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-responses.sh":::

# [Foundry portal](#tab/portal)

1. On the Home page of your project, select **Explore playgrounds**.
    
    :::image type="content" source="../media/instant-models/playground.png" alt-text="Screenshot of Explore playgrounds card with description to test models and get API key and endpoint.":::

1. Use the **Model** dropdown in the playground to switch among deployed and instant models.

---


### Why instant models matter

- **Switch models by changing one string** — use any instant model name in the `model=` line, without creating or deleting deployments.
- **Same API and SDK** — the same `responses.create()` calls work for both instant models and deployments.
- **Works with your dev tools** — instant models integrate with Foundry CLI, VS Code, and CI/CD pipelines the same way deployments do.

Deployments aren't going away. They remain the right choice when you need reserved throughput, custom content filters, data residency, or advanced enterprise configurations. Instant models simplify the getting-started experience so that deployments become something you level up to, not a gate you must pass before you can use a model.

## Supported models

<!-- [TODO] Add specific model list before publish -->

New models support instant access by default when they're released. Support for additional models is considered based on customer demand.

To see all models that support instant access, open the [Foundry model catalog](https://ai.azure.com/explore/models) and filter **Deployment options** to **Instant**.

> [!NOTE]
> During the preview, instant models are available in projects in **West US 3** only.

## When to use instant models vs. deployments

| Scenario | Recommended approach |
|---|---|
| Getting started, prototyping, or experimentation | Instant models |
| Using the latest model immediately after release | Instant models |
| Need reserved capacity or predictable throughput | Deployment |
| Require provisioned throughput (PTU) | Deployment |
| Need data residency in a specific region | Deployment |
| Custom content filtering policies | Deployment |
| Endpoint-specific configuration (for example, custom RAI, version locks per endpoint) | Deployment |
| Fine-grained quota partitioning across teams | Deployment |
| Fine-tuned models | Deployment |

Instant models and deployments can coexist in the same project. You can start with instant models and create deployments later as your requirements evolve.

## Model versions

By default, instant models route to the latest evergreen version of a model. To pin to a specific version, append the version date to the model name as a hyphenated suffix:

| What you pass as `model` | Behavior |
|---|---|
| `model-name` | Routes to the latest version |
| `model-name-2025-04-01` | Routes to that specific version |

<!-- [TODO] Confirm version suffix format (hyphen vs. other delimiter) before publish -->

Version pinning is opt-in. If your application requires stability, include the version suffix. Otherwise, you always get the latest version automatically.

## How quota is consumed

Instant models draw from a per-model **global quota** pool assigned to your subscription. This quota is separate from the regional quota used by standard deployments.

- You don't allocate or partition global quota — it's shared automatically across all instant model usage in your subscription.
- Global Standard deployments reserve a portion of your global quota. Instant models use whatever capacity remains.
- Other deployment types (Regional Standard, Provisioned) use separate regional quota and don't affect your instant model capacity.
- If instant model requests are throttled, you can request a quota increase or create a deployment with reserved capacity.

For more details on how global and regional quota interact, see [Manage and increase quotas](../how-to/quota.md).

## Enterprise controls

| Capability | How it works |
|---|---|
| Block specific models or providers | Azure Policy definitions apply to instant models the same way they apply to deployments |
| Pin to a model version | Append the version suffix to the model name (see [Model versions](#model-versions)) |
| Disable instant models entirely | Administrators can turn off instant models at the subscription level through Azure Policy |

> [!IMPORTANT]
> Custom Responsible AI (RAI) policies at the project level aren't supported for instant models during the preview. If you need custom content filtering policies, use a deployment.

## Deployment name collisions

New deployments can't use a name that matches an existing model name. If you have an existing deployment whose name collides with a model name, the deployment takes precedence and instant model access for that model name is unavailable in that project.

## Limitations during preview

- Available in **West US 3** only.
- Fine-tuned models aren't supported. To use a fine-tuned model, create a deployment.
- Custom RAI policies and content filters aren't configurable for instant models.
- Only the models listed in [Supported models](#supported-models) are eligible.

## Related content

- [Deployment overview for Microsoft Foundry Models](deployments-overview.md)
- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Manage quotas for Foundry resources](../how-to/quota.md)
- [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)
