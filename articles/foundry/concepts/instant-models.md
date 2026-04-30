---
title: "Instant models in Microsoft Foundry (preview)"
description: "Learn about Instant models in Microsoft Foundry, which let you call any supported model by name without creating a deployment first."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 04/30/2026
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
ms.custom:
  - build-2025
# customer intent: As a developer, I want to understand how Instant models work so that I can call models without creating deployments first.
---

# Instant models in Microsoft Foundry (preview)

Instant models let you call any supported model by name without creating a deployment first. Create a Foundry project, start coding, and use any available model immediately.

With Instant models, the typical workflow is straightforward: create a Foundry project, write code that references a model by name, and run inference. No deployment step required.

Deployments aren't going away. They remain the right choice when you need fine-grained quota control, provisioned throughput (PTU), or advanced enterprise capabilities. Instant models simplify the getting-started experience so that deployments become something you level up to, not a gate you must pass before you can use a model.

## How Instant models work

When you call a model by name through the Foundry API, the platform routes your request to available global capacity for that model. No deployment resource is created, and no deployment configuration is required. The following sections describe model name resolution and the developer interface.

### Model name resolution

| What you provide | What happens |
|---|---|
| Model name only (for example, `gpt-4o`) | Routes to the latest evergreen version of that model |
| Model name + version (for example, `gpt-4o-2024-05-13`) | Routes to the specific version you requested |

Version pinning is opt-in. By default, you always get the latest version. If your application requires stability on a specific version, include the version string in the model name.

### API and SDK interface

The API and SDK interface for Instant models is identical to the interface for deployments. Existing code that targets a deployment name works with Instant models when you replace the deployment name with the model name.

## Global quota

Instant models draw from a per-model **global quota** pool assigned to your subscription. This quota is separate from the regional quota used by standard deployments. The following sections explain how global quota works and how it interacts with deployments.

### How global quota differs from regional quota

| Aspect | Regional quota (deployments) | Global quota (Instant models) |
|---|---|---|
| Scope | Per region, per deployment | Single pool across regions |
| Partitioning | You divide quota among deployments | No partitioning — shared across all usage |
| Reservation | Deployments reserve their allocated portion | No reservation needed |

### Quota sharing between deployments and Instant models

Deployments and Instant models share the same underlying global capacity. When you create a deployment, it reserves a portion of your global quota. Instant models use whatever capacity remains.

```
Global Quota Pool:                1,000 units
  Deployment A reserves:            -400 units
                                  ----------
  Available for Instant models:     600 units
```

If your Instant model usage exceeds the remaining capacity, you receive a throttling error. You can then wait for capacity to free up, request a quota increase, or create a deployment with reserved capacity.

### Quota is per model

Each model has its own global quota allocation. Usage of one model doesn't consume quota assigned to a different model.

## Which models support Instant models?

Instant model availability depends on global quota support:

- **New models** — Supported by default. New model releases are built with global quota from the start.
- **Existing models** — Not initially supported. Older models require additional scaling work. Coverage improves naturally as newer models replace older ones.

> [!NOTE]
> During the preview, Instant models are available in a single region. Broader regional availability requires a global rate-limiting solution that is planned for general availability.

## When to use Instant models vs. deployments

Use the following guidance to decide between Instant models and deployments.

| Scenario | Recommended approach |
|---|---|
| Getting started, prototyping, or experimentation | Instant models |
| Using the latest model immediately after release | Instant models |
| Need reserved capacity or predictable throughput | Deployment |
| Require provisioned throughput (PTU) | Deployment |
| Need data residency in a specific region | Deployment |
| Fine-grained quota partitioning across teams | Deployment |

Instant models and deployments can coexist in the same project. You can start with Instant models and create deployments later as your requirements evolve.

## Enterprise controls

Existing governance capabilities continue to work with Instant models:

| Capability | How it works |
|---|---|
| Block specific models or providers | Azure Policy definitions apply to Instant models the same way they apply to deployments |
| Pin to a model version | Include the version string in the model name |
| Disable Instant models entirely | Administrators can turn off Instant models at the subscription level through Azure Policy |

> [!IMPORTANT]
> Custom Responsible AI (RAI) policies at the project level aren't supported for Instant models during the preview. If you need custom content filtering policies, use a deployment.

## Deployment name collisions

To prevent ambiguity, new deployments can't use a name that matches an existing model name. If you have an existing deployment whose name collides with a model name, the deployment takes precedence and Instant model access for that model name is unavailable in that project.

## Limitations during preview

- Available in a single region only.
- Global rate limiting across regions isn't available yet. General availability requires a global rate-limiting solution.
- Custom RAI policies and guardrails aren't configurable for Instant models.
- Global metric aggregation across regions isn't available during preview.
- Only models with global quota support are eligible.

## Related content

- [Deployment overview for Microsoft Foundry Models](deployments-overview.md)
- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Manage quotas for Foundry resources](../how-to/quota.md)
- [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)
