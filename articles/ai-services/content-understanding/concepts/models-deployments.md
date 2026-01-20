---
title: Connect your Content Understanding resource with Foundry models
titleSuffix: Foundry Tools
description: Describes the requirements and flexibility of specifying Gen AI model and deployment information for Content Understanding analyzers 
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/26/2025
ms.service: azure-ai-content-understanding
ms.topic: article
ms.custom:
  - ignite-2025
---

# Connect your Content Understanding analyzer to Foundry model deployments

Azure Content Understanding in Foundry Tools uses your Foundry model deployments for all operations that require a Generative AI model. This approach enables you to maximize your use of the capacity provisioned and aggregate capacity into fewer deployments if needed. You can also pick the model that fits your scenario best for price and latency. 

You're billed for all tokens (input and output) processed by the connected deployment, and Content Understanding only bills you for Content-Understanding-specific meters. See the [pricing explainer](../pricing-explainer.md) to learn more about the billing model.

The service requires a `chat completion` model and `embeddings` model and supports a few different options for each.

## Supported models

The service is periodically updated to add support for more models. The currently supported models can be found at [Service Limits - Supported generative models](../service-limits.md#supported-generative-models). 

## Set default deployments at the resource level

You can define default model deployments at the resource level by using a `PATCH` request. When you set defaults, you don't need to pass model deployments with every analyzer request.

**Step 1:** Set the default deployments on the resource.

``` json
PATCH /contentunderstanding/defaults
{
  // Specify the default model deployments for each completion and embedding model you plan to use
  "modelDeployments": {
    // This dictionary is formatted as "model name": "deployment name"
    "gpt-4.1": "gpt-4.1-deployment",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "text-embedding-3-large": "text-embedding-3-large-deployment",
    "text-embedding-ada-002": "text-embedding-ada-002"
  }
}
```

**Step 2:** Call the analyzer without specifying model deployments.

``` json
POST /myReceipt:analyze
{
  // No modelDeployments needed - uses resource defaults
}
```

When you have defaults defined on the resource, you can still override them for a specific request by providing `modelDeployments` in the analyze call.

## Define models for your analyzer

When you create a custom analyzer, specify which chat completion and embeddings models the analyzer should use. This configuration provides the flexibility of picking a model that provides the best results at the lowest cost. The analyzer definition associates a model name with the analyzer definition but not a specific model deployment. 

``` json
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
> GPT-4.1 is a recommended model for use with Foundry and the Studio. You can experiment or use any of the supported chat completion models in addition to GPT-4.1. The embeddings models are used when you use labeled samples or in-context learning to improve the quality of your analyzer.

## Test the analyzer and review usage

When you submit an analyze request for the analyzer, the response object contains a `usage` property. This property includes information on tokens consumed on your deployment and other billing usage incurred by the analyzer. You can validate this data against your usage data on the deployment to correlate the usage from Content Understanding with the model deployment.

``` json
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

* [Learn more about Content Understanding pricing](../pricing-explainer.md)
* [Learn more about Content Understanding analyzers](analyzer-reference.md)