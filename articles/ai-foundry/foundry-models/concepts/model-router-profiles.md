---
title: Optimize model selection with Model Router routing modes
titleSuffix: Azure AI Foundry
description: Learn how to choose and apply Model Router routing modes (balanced, quality, cost) to optimize model selection for accuracy or cost.
author: pafarley
ms.author: pafarley
manager: nitinme
ms.date: 11/06/2025
ms.service: azure-ai-foundry
ms.topic: concept
ai-usage: ai-assisted
# ms.custom: add custom flags if needed
---

# Optimize model selection with Model Router routing modes (preview)

Model Router can automatically choose among a set of foundation models for each request. Routing modes let you bias those choices toward higher quality or lower cost while preserving a baseline performance guarantee. This article explains the available modes, how they work, and how to configure them at deployment time or override them per request.

> [!NOTE]
> Routing modes are currently in **preview**. APIs, thresholds, or mode semantics might change before general availability. Confirm version numbers and availability before broad adoption. [TO VERIFY]

## When to use routing modes

Use routing modes if you:
* Want a simple “set-and-go” optimization without manually benchmarking every model.
* Need to reduce spend while retaining near-maximum quality.
* Need consistent access to the highest-quality model for critical workloads.
* Want to A/B test quality vs. cost trade-offs through per-request overrides.

If you don’t set a mode explicitly, the deployment defaults to the balanced strategy.

## Available routing modes

| Mode | Objective | Selection logic (conceptual) | Typical use cases | Trade-offs |
|------|-----------|------------------------------|-------------------|------------|
| Balanced (default) | Maintain near-best quality with cost sensitivity | Includes any candidate model whose estimated accuracy is within ~1% of the top model’s accuracy | General-purpose applications, mixed workloads | Slightly higher cost than strict cost mode; not always the single top-quality model |
| Quality | Always choose the highest-quality model | Equivalent to a strict selection (α = 0) picking the top model | Mission‑critical tasks, legal/risk reviews, complex reasoning | Highest cost among modes |
| Cost | Minimize cost while staying within a broader acceptable quality band | Includes models within ~5% of best estimated accuracy, then chooses lower-cost candidate | High-volume workloads, exploratory or background processing | Possible small quality reduction vs. balanced/quality |

> [!IMPORTANT]
> The ±1% and ±5% quality deltas are internal target thresholds for in-domain evaluation sets. Actual realized differences can vary by domain, prompt style, and data distribution. Validate against your own test set. [TO VERIFY]

## How routing works (conceptual)

Internally, the Model Router:
1. Estimates posterior performance (for example, accuracy or a composite quality score) for each candidate model on relevant in-domain signals.  
2. Computes the best (top) model score.
3. Applies a mode-specific threshold (α) to build a candidate pool:
   * Quality: α = 0 (top model only).
   * Balanced: α tuned so accepted models are within ~1% of top score.
   * Cost: α tuned so accepted models are within ~5% of top score.
4. Among candidates, applies secondary ordering (such as relative cost) as defined by the mode to choose the final model.

No user tuning of α is required in these predefined modes. Custom thresholds are out of scope for this release. [TO VERIFY feasibility of future custom thresholds]

## Configuration options

You can set the routing mode:
* At **deployment time** (static default).
* Per **individual request** (header override) if overrides are enabled for that deployment.

### Deployment-level configuration (Control Plane / ARM)

Specify the `routing.mode` property when you create or update the deployment.

#### Example (Azure CLI)

```bash
az resource create \
  --resource-group <rg-name> \
  --namespace Microsoft.CognitiveServices \
  --parent accounts/<account-name> \
  --resource-type deployments \
  --name <deployment-name> \
  --api-version 2024-03-01-preview \
  --properties '{
    "sku": { "name": "GlobalStandard", "capacity": 10 },
    "properties": {
      "model": {
        "format": "OpenAI",
        "name": "ModelRouter",
        "version": "2025-02-26-preview"
      },
      "routing": {
        "mode": "quality"
      }
    }
  }'
```

Update an existing deployment’s mode:

```bash
az resource update \
  --resource-group <rg-name> \
  --namespace Microsoft.CognitiveServices \
  --parent accounts/<account-name> \
  --resource-type deployments \
  --name <deployment-name> \
  --api-version 2024-03-01-preview \
  --set properties.routing.mode=cost
```

#### Example (ARM-style JSON body)

```json
{
  "sku": { "name": "GlobalStandard", "capacity": 10 },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "ModelRouter",
      "version": "2025-02-26-preview"
    },
    "routing": {
      "mode": "balanced"
    }
  }
}
```

Valid values: `balanced`, `quality`, `cost` (case-insensitive).  
If omitted, the service defaults to `balanced`.

### Per-request override (data plane)

Add the `model-router-mode` header to a request to override the deployment’s default for that single call.

#### Request example

```
POST /v1/chat/completions HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
model-router-mode: cost

{
  "messages": [
    { "role": "user", "content": "Summarize this article." }
  ]
}
```

#### Response headers

The router returns the header:

```
model-router-effective-mode: cost
```

This echoes the effective mode after merging deployment defaults and any valid override.

### Validation and errors

| Condition | HTTP status | Error code | Notes |
|-----------|-------------|-----------|-------|
| Unsupported `model-router-mode` value | 400 | `invalidRoutingMode` | Value not in balanced/quality/cost |
| Per-request overrides disabled (deployment policy) | 400 | `headerNotAllowed` | Remove header or enable overrides |
| Case variation | 200 | — | Value normalized internally (`Quality` → `quality`) |

(Confirm whether per-request overrides can be disabled by policy and link to policy doc when available.) [TO VERIFY]

## Best practices

* Benchmark: Run a small evaluation set under `balanced` vs. `cost` to quantify quality delta before large-scale shift.
* Log effective mode: Persist `model-router-effective-mode` for analytics and auditing.
* Start conservative: Move from `quality` → `balanced` → `cost` only after confirming acceptable outputs.
* Mixed workloads: Use deployment default = `balanced` and override individual background requests with `cost`.
* Guardrails: For safety-critical tasks, keep `quality` and add post-processing validation.

## Limitations

* Custom numeric thresholds (e.g., “within 2.5%”) aren’t supported in this release. [TO VERIFY]
* Mode impact depends on coverage of internal evaluation signals for your domain.
* New preview model versions can slightly shift internal quality rankings; re-check KPIs after upgrading router version (`version: 2025-02-26-preview`). [TO VERIFY version and GA timeline]

## FAQ

**Can I combine quality and cost criteria directly?**  
Not with predefined modes. Each mode encodes a fixed optimization pattern. Use per-request overrides plus workload segmentation to approximate hybrid behavior.

**Does `quality` always mean the largest model?**  
Usually, but the selection depends on internal quality scoring, which can incorporate more than parameter count.

**What if I must guarantee a specific model (e.g., for regulatory reasons)?**  
Deploy that model directly instead of routing, or ensure your candidate pool is constrained (future feature for candidate restriction). [TO VERIFY candidate restriction roadmap]

## Troubleshooting

| Symptom | Possible cause | Action |
|---------|----------------|--------|
| 400 `invalidRoutingMode` | Typo in header value | Use `balanced`, `quality`, or `cost` |
| 400 `headerNotAllowed` | Overrides disabled | Remove header or enable overrides at deployment |
| Higher cost than expected in `balanced` | Narrow candidate pool still dominated by top-cost model | Test `cost` mode; verify quality tolerance |
| Quality drop larger than expected in `cost` mode | Domain differs from internal tuning set | Re-evaluate; consider `balanced` or `quality` for that segment |

## Next steps

* Learn how to [Deploy the Model Router](./model-router-deploy.md) [TO VERIFY link].
* Explore guidance on [Evaluating model quality](./model-quality-evaluation.md) [TO VERIFY link].
* Review [Cost optimization strategies](../concepts/cost-optimization.md) [TO VERIFY link].

---

> [!TIP]
> Provide feedback or request additional routing strategies (for example, latency-optimized) through your Azure support channel. [TO VERIFY support pathway]