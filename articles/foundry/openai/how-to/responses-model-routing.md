---
title: Auto and direct model routing with the Responses API
description: "Use the Responses API as a single interface to call any model in Microsoft Foundry, from automatic selection with model router to deterministically named models."
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 05/01/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Auto and direct model routing with the Responses API

The Responses API is the programmatic interface for every model in Microsoft Foundry. Pass `model-router` in the `model` field to let Foundry pick the best model automatically. Or pass a specific model name for deterministic control. The code is the same—only the `model` value changes.

> [!NOTE]
> You pass your deployment name to the `model` parameter. In most cases the deployment name matches the model name. For example, a `gpt-4.1-mini` deployment is called `"gpt-4.1-mini"`.

## Prerequisites

- A Foundry project with a `model-router` deployment. See [Deploy model router](model-router.md#deploy-a-model-router-model).
- At least one named model deployment for deterministic calls (for example, `gpt-4.1-mini`). See [Deploy a model](/azure/ai-foundry/openai/how-to/create-resource).
- Familiarity with the [Responses API](responses.md).
- Python 3.9+
- The Foundry SDK:

  ```bash
  pip install "azure-ai-projects>=2.0.0"
  ```

## Call models through the Responses API

The following sample calls several models through the same `responses.create()` interface, starting with `model-router` for automatic selection, then named models for deterministic control.

```python
import os
import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create the Foundry project client
project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

deployments = ["model-router", "gpt-5.2", "grok-4-fast-reasoning", "gpt-5-mini", "Deepseek-V3.2"]
prompt = "Explain retrieval-augmented generation in one sentence."

print(f"{'Deployment':<22} {'Responded':<22} {'Latency':>8}  Response")
print("-" * 100)

# Get an OpenAI-compatible client that works with all Foundry models
with project.get_openai_client() as client:
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

The following table shows a sample output. Actual latency and response text vary per request.

| Deployment | Responded | Latency | Response |
|---|---|---|---|
| model-router | gpt-4.1-nano | 0.59 s | It combines retrieval of relevant documents with generati... |
| gpt-5.2 | same | 0.78 s | Retrieval-augmented generation enhances model output by firs... |
| grok-4-fast-reasoning | same | 0.65 s | It is a technique that grounds language model responses in... |
| gpt-5-mini | same | 0.67 s | It retrieves external knowledge to augment a model's genera... |
| Deepseek-V3.2 | same | 1.14 s | It augments model generation by first retrieving relevant do... |

See the first row: `model-router` didn't target a specific model, but the `Responded` column shows that it selected `gpt-4.1-nano`. For the named models that follow, the two columns match; The code is identical in every case.

> [!TIP]
> The `response.model` field always returns the model that handled the request. Use it for logging, cost attribution, or debugging routing decisions.

## Routing strategies

Every call goes through `responses.create()`. The `model` value is the only decision point.

| Use case | `model` value| Result |
|---|---|---|
| The best model for each request, optimized by cost or quality | `"model-router"` | Foundry evaluates the prompt and selects the best model from your configured pool |
| A specific model for compliance, reproducibility, or benchmarking | The model name (`"gpt-5-2"`, `"Deepseek-V3.2"`) | Foundry routes to exactly that model |
| To switch between strategies | Change one string | The rest of the code stays identical |

Use `model-router` as your default. Customize your model router deployment with optional settings. See [Model router deployment options](model-router.md#optional-customize-deployment-settings).

Switch to a named model only when you need deterministic control.


## Built-in enterprise capabilities

Every `responses.create()` call, whether routed through `model-router` or targeting a named model, automatically includes:

- **Automatic failover**—When using `model-router`, if the selected model encounters a transient issue, model router transparently redirects the request to the next most appropriate model. No disruption to your application, no retry logic required. If you configure a model subset, that subset also serves as your fallback set — select at least two models to benefit from failover.
- **Prompt caching**—Model router supports prompt caching. When model router delegates a request to a model that supports prompt caching, cached tokens are used automatically. Combined with model router's right-fit model selection, you get an extra efficiency lift: the optimal model for the task *and* reduced token costs on repeated prompt prefixes — no configuration needed.
- **Content filtering**—Configurable content safety applied to inputs and outputs without extra API parameters.
- **Role-based access control**—Azure role-based access control governs who can call which deployments. No separate API key management.
- **Observability and tracing**—Every request is logged with the selected model, latency, and token usage. Integrate with Azure Monitor or your existing observability stack.
- **Data residency and compliance**—Traffic stays within your Azure region. No data leaves your tenant boundary.
- **Rate limiting and quotas**—Per-deployment token-per-minute limits protect your workloads from noisy neighbors.

These capabilities apply uniformly across all models in the catalog. You don't opt in or configure them per request—they're part of the platform.

## Related content

- [Use model router for Microsoft Foundry](model-router.md) — deployment, routing modes, model subsets
- [Use the Azure OpenAI Responses API](responses.md) — streaming, tools, stored responses
- [Microsoft Foundry SDKs and endpoints](../../how-to/develop/sdk-overview.md#foundry-sdk) — client setup and endpoint patterns
