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

# Conceptual
# Optimize model selection with Model Router routing modes (preview)


# How to

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