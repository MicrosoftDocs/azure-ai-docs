---
title: Model deployment options for Content Understanding analyzers
titleSuffix: Foundry Tools
description: Learn how Content Understanding maps analyzer models to Foundry deployments, and how defaults and request-level overrides interact.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 04/25/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: concept-article
ms.custom:
  - ignite-2025
---

# Model deployment options for Content Understanding analyzers

Azure Content Understanding in Foundry Tools uses your Foundry model deployments for all operations that require a generative AI model. This approach helps you maximize provisioned capacity and consolidate capacity into fewer deployments, if needed. You can also choose the model that best fits your scenario for price and latency.

You're billed for all tokens (input and output) processed by the connected deployment, and Content Understanding only bills you for Content Understanding-specific meters. See the [pricing explainer](../pricing-explainer.md) to learn more about the billing model.

The service requires a `chat completion` model and an `embeddings` model and supports a few different options for each.

## Supported models

The service is periodically updated to add support for more models. The currently supported models are listed in [Service limits - Supported generative models](../service-limits.md#supported-generative-models). Please refer to [Model retirement schedule](../../../foundry/openai/concepts/model-retirement-schedule.md) to track Foundry model lifecycle stage and retirement date.

> [!NEW]
> GPT-5.2 is now supported across all Content Understanding analyzers. Support for additional models will be added in future updates.

### Check supported models per analyzer

Different analyzers support different sets of models. To check which models a specific analyzer supports, use the `GET` analyzers API:

```http
GET /contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01
```

The response includes a `supportedModels` object that lists the valid completion and embedding models for that analyzer:

```jsonc
{
  "analyzerId": "prebuilt-invoice",
  // ...
  "supportedModels": {
    "completion": [
      "gpt-4.1",
      "gpt-5.2"
    ],
    "embedding": [
      "text-embedding-3-large"
    ]
  },
  "models": {
    "completion": "prebuilt-analyzer-completion",
    "embedding": "prebuilt-analyzer-embedding"
  }
}
```

### Model selection for prebuilt analyzers

Prebuilt analyzers use indirection keys instead of direct model names in their `models` section. This allows the service to support model upgrades without changing analyzer definitions.

Prebuilt analyzers reference the following deployment keys:

| Key | Used by |
|---|---|
| `prebuilt-analyzer-completion` | Default for most prebuilt analyzers |
| `prebuilt-analyzer-completion-mini` | Default for selected prebuilt analyzers, e.g. `prebuilt-*Search` |
| `prebuilt-analyzer-embedding` | Prebuilt analyzers that require embeddings |

You map these keys to your actual deployments in the `modelDeployments` configuration (see [Set default deployments](#option-1-set-default-deployments-at-the-resource-level)).

> [!NOTE]
> If your resource already has `gpt-4.1` (or `gpt-4.1-mini`) and `text-embedding-3-large` configured in `modelDeployments`, the service automatically creates the `prebuilt-analyzer-*` keys using those existing deployment values. No manual action is required for existing customers.


## How model selection works

When you create a custom analyzer, you can specify which chat completion model and embedding model it uses.

```jsonc
{
  "analyzerId": "myReceipt",
  "models": {
    // Specifies the completion and embedding models used by this analyzer.
    "completion": "myGpt52Deployment",
    "embedding": "myTextEmbedding3LargeDeployment"
  },
  "config": {

  }
  // Complete analyzer definition
}
```

> [!TIP] 
> GPT-5.2 is a recommended model for use with Foundry and the Studio. You can use any supported chat completion model that fits your quality, latency, and cost goals. Embedding models are used when you use labeled samples or in-context learning to improve analyzer quality.


## Two ways to provide model deployments

As a customer, you have two options:

- **Option 1:** Set default model deployments at the resource level.
- **Option 2:** Pass model deployment pointers in every analyze request.

If you set resource defaults, you can still override those defaults for a single request by including `modelDeployments` in that request.

### Option 1: Set default deployments at the resource level

After you set defaults, analyze requests can omit `modelDeployments`. Choose one of the following setup methods:

# [REST API or code](#tab/rest-api)

Use `PATCH /contentunderstanding/defaults` to set model deployment defaults at the resource level.

```jsonc
PATCH /contentunderstanding/defaults
{
  "modelDeployments": {
    "gpt-5.2": "myGpt52Deployment",
    "text-embedding-3-large": "myTextEmbedding3LargeDeployment",
    // Specify default model deployments as "prebuilt analyzer indirection keys": "deployment name"
    "prebuilt-analyzer-completion": "myGpt52Deployment",
    "prebuilt-analyzer-completion-mini": "myGpt41-miniDeployment",
    "prebuilt-analyzer-embedding": "myTextEmbedding3LargeDeployment"
  }
}
```

Example analyze request that uses resource defaults:

```jsonc
POST /myReceipt:analyze
{
  // No modelDeployments needed - uses resource defaults
}
```

# [Content Understanding Studio](#tab/studio)

For the full onboarding flow, see [Quickstart: Try out Content Understanding Studio](../quickstart/content-understanding-studio.md).

1. Open [Content Understanding Studio](https://aka.ms/cu-studio).
1. Select the **Settings** gear icon in the upper-right corner.
1. Select **Add resource** to open the **Add new connected resource** dialog.
1. To connect a resource, select the subscription, resource group, and Foundry resource in the dialog.
:::image type="content" source="../media/concepts/set-defaults-in-content-understanding-studio.png" alt-text="Screenshot of the Add new connected resource dialog with subscription, resource group, resource name, and automatic deployment option." lightbox="../media/concepts/set-defaults-in-content-understanding-studio.png" :::
1. Optional: Select **Enable auto-deployment for required models if no default deployment available**.
1. Select **Next**, review mappings, and then save.



Studio can configure defaults for supported models such as `gpt-5.2`, `gpt-4.1`, `gpt-4.1-mini`, and `text-embedding-3-large`. If the selected resource doesn't already have the required deployments, Studio can deploy them when auto-deployment is enabled.

---

### Option 2: Pass model deployments in each analyze request

Use this option when you want each request to explicitly point to model deployments by passing a `modelDeployments` object in the analyze request. This approach gives you maximum flexibility to use different deployments for different requests and doesn't require resource defaults.

```jsonc
POST /contentunderstanding/analyzers/{analyzerID}}:analyze
{
  "modelDeployments": {
    "gpt-5.2": "myGpt52Deployment", 
    "text-embedding-3-large": "myTextEmbedding3LargeDeployment",
  // Specify the model deployments for this request
    "prebuilt-analyzer-completion": "myGpt52Deployment",
    "prebuilt-analyzer-embedding": "myTextEmbedding3LargeDeployment"
  }
}
```

The `modelDeployments` values in this analyze request override defaults that you configured at the resource level.


## Usage and billing data

Analyze responses include a `usage` property. This property reports token usage for your connected deployment and other Content Understanding usage meters. You can compare these values with deployment usage data to correlate consumption from Content Understanding with your model deployment.

```jsonc
{
  "usage": {
    "documentPagesMinimal": 3, 
    "documentPagesBasic": 2, 
    "documentPagesStandard": 1, 
    "audioHours": 0.234,
    "videoHours": 0.123,
    "contextualizationToken": 1000,
    "tokens": {
      "gpt-5.2-input": 1234, /*Completion model Input and output tokens consumed*/
      "gpt-5.2-output": 2345,
      "text-embedding-3-large": 3456 /*Embedding tokens consumed*/
    }
  }
}
```

For details on how billing works for Content Understanding, see the [pricing explainer](../pricing-explainer.md).

## Content filtering and Guardrails

Each Foundry model deployment has an associated **Guardrails** instance that evaluates content for safety. Content Understanding surfaces the Guardrails output directly in the analyze response as a `content_filters` array. If a Guardrails instance blocks content, the analyze operation returns an error; if it annotates content, the result passes through with filter metadata attached.

To adjust content filter thresholds or switch from blocking to annotating, update the Guardrails configuration on the model deployment in your Azure AI Foundry project. For more information, see [Content filtering and Guardrails](../overview.md#content-filtering-and-guardrails) and the [`content_filters` response object reference](analyzer-reference.md#content-filter-results-in-the-analyze-response).

## Related content

* [Learn more about Content Understanding pricing](../pricing-explainer.md).
* [Learn more about Content Understanding analyzers](analyzer-reference.md).