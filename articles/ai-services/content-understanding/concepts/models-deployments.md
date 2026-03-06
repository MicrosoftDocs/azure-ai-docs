---
title: Model deployment options for Content Understanding analyzers
titleSuffix: Foundry Tools
description: Learn how Content Understanding maps analyzer models to Foundry deployments, and how defaults and request-level overrides interact.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 03/06/2026
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

The service is periodically updated to add support for more models. The currently supported models are listed in [Service limits - Supported generative models](../service-limits.md#supported-generative-models).

## How model selection works

When you create a custom analyzer, you specify which chat completion model and
embedding model it uses. This association is made using a deployment alias rather than directly with a specific deployment-name.

```jsonc
{
  "analyzerId": "myReceipt",
  "models": {
    // Specifies the completion and embedding models used by this analyzer.
    "completion": "gpt-4.1",
    "embedding": "text-embedding-ada-002"
  },
  "config": {

  }
  // Complete analyzer definition
}
```

> [!TIP]
> GPT-4.1 is a recommended model for use with Foundry and the Studio. You can
> use any supported chat completion model that fits your quality, latency, and
> cost goals. Embedding models are used when you use labeled samples or
> in-context learning to improve analyzer quality.

## Two ways to provide model deployments

As a customer, you have two options:

1. **Option 1:** Set default model deployments at the resource level.
1. **Option 2:** Pass model deployment pointers in every analyze request.

If you set resource defaults, you can still override those defaults for a
single request by including `modelDeployments` in that request.

### Option 1: Set default deployments at the resource level

After you set defaults, analyze requests can omit `modelDeployments`. Choose
one of the following setup methods:

# [REST API or code](#tab/rest-api)

Use `PATCH /contentunderstanding/defaults` to set model deployment defaults at
the resource level.

```jsonc
PATCH /contentunderstanding/defaults
{
  // Specify default model deployments as "model name": "deployment name"
  "modelDeployments": {
    "gpt-4.1": "gpt-4.1-deployment",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "text-embedding-3-large": "text-embedding-3-large-deployment",
    "text-embedding-ada-002": "text-embedding-ada-002"
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

For the full onboarding flow, see [Quickstart: Try out Content Understanding
Studio](../quickstart/content-understanding-studio.md).

1. Open [Content Understanding Studio](https://aka.ms/cu-studio).
1. Select the **Settings** gear icon in the upper-right corner.
1. Select **Add resource** to open the **Add new connected resource** dialog.
1. To connect a resource, select the subscription, resource group, and Foundry resource in the dialog.
:::image type="content" source="../media/how-to/bring-your-own-cross-resource-capacity/connect-microsoft-foundry-resource-search-select-and-add-connection.png" alt-text="Screenshot of the Add new connected resource dialog with subscription, resource group, resource name, and automatic deployment option." lightbox="../media/how-to/bring-your-own-cross-resource-capacity/connect-microsoft-foundry-resource-search-select-and-add-connection.png" :::
1. Optional: Select **Enable auto-deployment for required models if no default deployment available**.
1. Select **Next**, review mappings, and then save.



Studio can configure defaults for supported models such as `gpt-4.1`,
`gpt-4.1-mini`, and `text-embedding-3-large`. If the selected resource doesn't
already have the required deployments, Studio can deploy them when
auto-deployment is enabled.

---

### Option 2: Pass model deployments in each analyze request

Use this option when you want each request to explicitly point to model
deployments by passing a `modelDeployments` object in the analyze request. This
approach gives you maximum flexibility to use different deployments for
different requests and doesn't require resource defaults.

```jsonc
POST /contentunderstanding/analyzers/prebuilt-invoice:analyze
{
  "inputs": [
    {
      "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"
    }
  ],
  // Specify the model deployments for this request
  "modelDeployments": {
    "gpt-4.1": "gpt-4.1",
    "text-embedding-3-large": "text-embedding-3-large"
  }
}
```

The `modelDeployments` values in this analyze request override any defaults that
you configured at the resource level.

## Usage and billing data

Analyze responses include a `usage` property. This property reports token usage
for your connected deployment and other Content Understanding usage meters.
You can compare these values with deployment usage data to correlate consumption
from Content Understanding with your model deployment.

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
      "gpt-4.1-input": 1234, /*Completion model Input and output tokens consumed*/
      "gpt-4.1-output": 2345,
      "text-embedding-3-large": 3456 /*Embedding tokens consumed*/
    }
  }
}
```

For details on how billing works for Content Understanding, see the [pricing explainer](../pricing-explainer.md).


## Related content

* [Learn more about Content Understanding pricing](../pricing-explainer.md).
* [Learn more about Content Understanding analyzers](analyzer-reference.md).