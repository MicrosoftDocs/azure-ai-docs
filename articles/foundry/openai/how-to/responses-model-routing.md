---
title: Auto and direct model routing with the Responses API
description: "Use the Responses API as a single interface to call any model in Microsoft Foundry, from automatic selection with model router to deterministic named models."
author: yourGitHubAlias
ms.author: yourMsAlias
ms.date: 05/01/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Auto and direct model routing with the Responses API

The Responses API is the single calling interface for every model in Microsoft Foundry. Pass `model-router` to let Foundry pick the best model automatically. Pass a specific model name for deterministic control. The code is the same — only the `model` value changes.

> [!NOTE]
> You pass your deployment name to the `model` parameter. In most cases the deployment name matches the model name (for example, a `gpt-4.1-mini` deployment is called `"gpt-4.1-mini"`).

## Prerequisites

- A Foundry project with a `model-router` deployment. See [Deploy model router](model-router.md#deploy-a-model-router-model).
- At least one named model deployment for deterministic calls (for example, `gpt-4.1-mini`). See [Deploy a model](create-resource.md).
- Familiarity with the [Responses API](responses.md).
- Python 3.9+
- The OpenAI Python package:

  ```bash
  pip install openai>=1.75.0
  ```

## Call models through the Responses API

The following sample calls several models through the same `responses.create()` interface — starting with `model-router` for automatic selection, then named models for deterministic control. The only difference is the `model` value.

```python
import os
import time
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["PROJECT_ENDPOINT"],
    api_version="2025-04-01-preview",
)

deployments = ["model-router", "gpt-5.2", "grok-4-fast-reasoning", "gpt-5-mini", "Deepseek-V3.2"]
prompt = "Explain retrieval-augmented generation in one sentence."

print(f"{'Deployment':<22} {'Responded':<22} {'Latency':>8}  Response")
print("-" * 100)

for name in deployments:
    start = time.time()
    response = client.responses.create(model=name, input=prompt)
    elapsed = time.time() - start

    responded_model = response.model
    print(
        f"{name:<22} {responded_model:<22} {elapsed:>7.2f}s  "
        f"{response.output_text[:60]}"
    )
```

The following is sample output. Actual latency and response text vary per request.

| Deployment | Responded | Latency | Response |
|---|---|---|---|
| model-router | gpt-4.1-nano | 0.59s | RAG combines retrieval of relevant documents with generati... |
| gpt-5.2 | same | 0.78s | Retrieval-augmented generation enhances LLM output by firs... |
| grok-4-fast-reasoning | same | 0.65s | RAG is a technique that grounds language model responses in... |
| gpt-5-mini | same | 0.67s | It retrieves external knowledge to augment a model's genera... |
| Deepseek-V3.2 | same | 1.14s | RAG augments LLM generation by first retrieving relevant do... |

The first row is the key insight: `model-router` didn't target a specific model, but the `Responded` column shows Foundry selected `gpt-4.1-nano` on your behalf. For the named models that follow, the two columns match — you asked for a specific model and got it. The code is identical in every case.

> [!TIP]
> The `response.model` field always returns the model that handled the request. Use it for logging, cost attribution, or debugging routing decisions.

## One API, two routing strategies

Every call goes through `responses.create()`. The `model` value is the only decision point.

| When you need | Set `model` to | What happens |
|---|---|---|
| The best model for each request, optimized by cost or quality | `"model-router"` | Foundry evaluates the prompt and selects the best model from your configured pool |
| A specific model for compliance, reproducibility, or benchmarking | The model name (`"gpt-5-2"`, `"Deepseek-V3.2"`) | Foundry routes to exactly that model |
| To switch between strategies | Change one string | The rest of the code stays identical |

Use `model-router` as your default. Switch to a named model only when you need deterministic control.

## Configure the model router deployment

The model router deployment supports three routing modes that control how it selects the underlying model:

- **Balanced** (default) — Optimizes cost while maintaining quality. Best for most workloads.
- **Quality** — Prioritizes the strongest model. Use for critical tasks like legal review or complex reasoning.
- **Cost** — Prioritizes the cheapest capable model. Use for high-volume workloads like classification or simple Q&A.

You can also restrict routing to a subset of models. For configuration details, see [Use model router](model-router.md#optional-change-the-routing-mode).

## Built-in enterprise capabilities

Every `responses.create()` call — whether routed through `model-router` or targeting a named model — automatically includes:

- **Automatic failover** — When using `model-router`, if the selected model encounters a transient issue, model router transparently redirects the request to the next most appropriate model. No disruption to your application, no retry logic required. If you configure a model subset, that subset also serves as your fallback set — select at least two models to benefit from failover.
- **Prompt caching** — Model router supports prompt caching. When model router delegates a request to a model that supports prompt caching, cached tokens are used automatically. Combined with model router's right-fit model selection, you get an additional efficiency lift: the optimal model for the task *and* reduced token costs on repeated prompt prefixes — no configuration needed.
- **Content filtering** — Configurable content safety applied to inputs and outputs without extra API parameters.
- **Role-based access control** — Azure RBAC governs who can call which deployments. No separate API key management.
- **Observability and tracing** — Every request is logged with the selected model, latency, and token usage. Integrate with Azure Monitor or your existing observability stack.
- **Data residency and compliance** — Traffic stays within your Azure region. No data leaves your tenant boundary.
- **Rate limiting and quotas** — Per-deployment token-per-minute limits protect your workloads from noisy neighbors.

These capabilities apply uniformly across all models in the catalog. You don't opt in or configure them per request — they're part of the platform.

## Related content

- [Use model router for Microsoft Foundry](model-router.md) — deployment, routing modes, model subsets
- [Use the Azure OpenAI Responses API](responses.md) — streaming, tools, stored responses
- [Microsoft Foundry SDKs and endpoints](../../how-to/develop/sdk-overview.md) — client setup and endpoint patterns
