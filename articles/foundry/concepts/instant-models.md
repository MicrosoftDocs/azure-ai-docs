---
title: "Instant models in Microsoft Foundry (preview)"
description: "Learn about instant models in Microsoft Foundry, which let you call any supported model by name without creating a deployment first."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 04/30/2026
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
ms.custom:
  - build-2025
# customer intent: As a developer, I want to understand how instant models work so that I can call models without creating deployments first.
---

# Instant models in Microsoft Foundry (preview)

With instant models, your workflow is straightforward: create a Foundry project, write code that references a model by name, and run inference. No deployment step required.

Deployments aren't going away. They remain the right choice when you need fine-grained quota control, provisioned throughput (PTU), or advanced enterprise capabilities. Instant models simplify the getting-started experience so that deployments become something you level up to, not a gate you must pass before you can use a model.

## How instant models work

When you call a model by name through the Foundry API, the platform routes your request to available global capacity for that model. No deployment resource is created, and no deployment configuration is required. The following sections describe model name resolution and the developer interface.

### Model name resolution

| What you provide | What happens |
|---|---|
| Model name only (for example, `gpt-4o`) | Routes to the latest evergreen version of that model |
| Model name + version (for example, `gpt-4o-2024-05-13`) | Routes to the specific version you requested |

Version pinning is opt-in. By default, you always get the latest version. If your application requires stability on a specific version, include the version string in the model name.

### API and SDK interface

The API and SDK interface for instant models is identical to the interface for deployments. Existing code that targets a deployment name works with instant models when you replace the deployment name with the model name.

## Global quota

Instant models draw from a per-model **global quota** pool assigned to your subscription. This quota is separate from the regional quota used by standard deployments. The following sections explain how global quota works and how it interacts with deployments.

### How global quota differs from regional quota

| Aspect | Regional quota (deployments) | Global quota (instant models) |
|---|---|---|
| Scope | Per region, per deployment | Single pool across regions |
| Partitioning | You divide quota among deployments | No partitioning — shared across all usage |
| Reservation | Deployments reserve their allocated portion | No reservation needed |

### Quota sharing between Global Standard deployments and instant models

Global Standard deployments and instant models share the same underlying global capacity. When you create a Global Standard deployment, it reserves a portion of your global quota. Instant models use whatever capacity remains. Other deployment types (Regional Standard, Provisioned) use separate regional quota and don't affect your instant model capacity.

```
Global Quota Pool:                1,000 units
  Global Standard deployment:       -400 units
                                  ----------
  Available for instant models:     600 units
```

If your instant model usage exceeds the remaining capacity, you receive a throttling error. You can then wait for capacity to free up, request a quota increase, or create a deployment with reserved capacity.

### Quota is per model

Each model has its own global quota allocation. Usage of one model doesn't consume quota assigned to a different model.

## Which models support instant models?

<!-- The following models support instant access during the preview:

 [TODO] Add specific model list before publish -->

As new models are released, they support instant access by default. Support for additional models is considered based on customer demand.

> [!NOTE]
> During the preview, instant models are available in projects in South Central US only. 

## When to use instant models vs. deployments

Use the following guidance to decide between instant models and deployments.

| Scenario | Recommended approach |
|---|---|
| Getting started, prototyping, or experimentation | Instant models |
| Using the latest model immediately after release | Instant models |
| Need reserved capacity or predictable throughput | Deployment |
| Require provisioned throughput (PTU) | Deployment |
| Need data residency in a specific region | Deployment |
| Fine-grained quota partitioning across teams | Deployment |

Instant models and deployments can coexist in the same project. You can start with instant models and create deployments later as your requirements evolve.

## Enterprise controls

Existing governance capabilities continue to work with instant models:

| Capability | How it works |
|---|---|
| Block specific models or providers | Azure Policy definitions apply to instant models the same way they apply to deployments |
| Pin to a model version | Include the version string in the model name |
| Disable instant models entirely | Administrators can turn off instant models at the subscription level through Azure Policy |

> [!IMPORTANT]
> Custom Responsible AI (RAI) policies at the project level aren't supported for instant models during the preview. If you need custom content filtering policies, use a deployment.

## Deployment name collisions

To prevent ambiguity, new deployments can't use a name that matches an existing model name. If you have an existing deployment whose name collides with a model name, the deployment takes precedence and instant model access for that model name is unavailable in that project.

## Limitations during preview

- Available in South Central US only.

- Custom RAI policies and guardrails aren't configurable for instant models.
- Only models with global quota support are eligible. This list will initially be small but more added over time.

## Related content

- [Deployment overview for Microsoft Foundry Models](deployments-overview.md)
- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Manage quotas for Foundry resources](../how-to/quota.md)
- [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)
