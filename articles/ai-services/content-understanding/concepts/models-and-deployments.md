---
title: Connect your Content Understanding resource with Foundry models
titleSuffix: Azure AI services
description: Describes the requirements and flexibility of specifying Gen AI model and deployment information for Content Understanding analyzers 
author: PatrickFarley 
ms.author: vkurpad
manager: nitinme
ms.date: 10/26/2025
ms.service: azure-ai-content-understanding
ms.topic: concept
ms.custom:
  - ignite-2025
---

# Connect your Content Understanding analyzer to Foundry model deployments

Content Understanding uses your Foundry model deployments for all operations that require a Gen AI model. This enables you to maximize your use of the capacity provisioned and aggregate capacity into fewer deployments if needed. You can also pick the model that fits your scenario the best for price and latency. You will be billed for all tokens, input and output on the deployment connected and Content Understanding will only bill you for the Content Understanding specific meters. See [pricing explainer](pricing-explainer.md) to learn more about the billing model.

The service requires a `chat completion` model and `embeddings` model and supports a few differet options for each. Some analyzers also have a dependency on a specifc model.

## Supported models

The services is periodically updated to add support for models. The currently supported models are

| Model Type | Model | Version |
|--|--|--|
|Chat Completion | gpt-4o | 2024-08-06 |
|Chat Completion | gpt-4o | 2024-11-20 |
|Chat Completion | gpt-4o-mini | 2024-11-20 |
|Chat Completion | gpt-4.1 | 2024-11-20 |
|Chat Completion | gpt-4.1-mini | 2024-11-20 |
|Chat Completion |gpt-4.1-nano | 2024-11-20 |
|Embeddings | text-embedding-3-small |  |
|Embeddings | text-embedding-3-large |  |
|Embeddings | text-embedding-ada-002 |  |

## Configuring models and deployments

Content Understanding analyzers that utilize Generative AI (Gen AI) models now require explicit specification of both the model and deployment details. These details can be configured at the resource level, applying to all operations by default, or can be overridden for individual analyze operations as needed. This approach provides organizations with the flexibility to support multiple business teams, enabling each team to use the same analyzer with different Gen AI models or deployments according to their specific requirements.

The model and deployment definition is a multi step process.

* **Step 1** You can specify the deployments to use on the resource via a ```PATCH``` request. It is recommended that you set this default model and deployment to ensure your analyzers always have a valid model deployment to use. To set the default deployment, update the Content Understanding resource with the deployments. GPT4.1 is a recommended model for use with the Foundry and the Studio. You can experiment or use any of the supported chat completion models in addition to GPT4.1. The embeddings model are used when you use labeled samples or in-context learning to improve the quality of your analyzer.

``` JSON
PATCH /contentunderstanding/defaults
{
  // Specify the default model deployments for each LLM/embedding model. The format is "model name": "deployment name"
  "modelDeployments": {
    "gpt-4.1": "gpt-4.1-deployment",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "text-embedding-ada-002":  "text-embedding-ada-002"
  }
}

```

* **Step 2** Define the models that a specific analyzer should use when building the analyzer. At build time, associate each analyzer with a specific chat completion model and an embeddings model. This provides the flexibility of picking a model that provides the best results at the lowest cost. The analyzer defintion only assoicates a model with the analyzer and not the deployment. 

``` JSON

{
"analyzerId": "myReceipt",
    // Specify the LLM/embedding models used by this analyzer. 
    "models": {
      "completion": "gpt-4.1",
      "embedding": "text-embedding-ada-002"
    }
  "config": {
    
  },
  // Complete analyzer definition
}

```

* **Step 3** At analyze time, connect the model that the analyzer should use with the deployment. If you have defaults defined on the resource, no `modelDeplyments` are needed, if no defaults are defined on the resource, or you want to override the defaults, provide the `modelDeployments` to use.

``` JSON
POST /myReceipt:analyze
{

  "modelDeployments": {
    "gpt-4.1": "myGpt41Deployment"
  }
}

```

> [!NOTE]
> [Prebuilt analyzers](./concepts/analyzers.md) require a specific model. Please see the models catalog for the models each prebuilt works with.

You have now connected your Content Understanding analyzer with a Foundry model deployment to use. 

## Testing the analyzer

Submit an analyze request for the analyzer and validate that the response is accuate. In addition to the content and fields in the response, the response object contains a `usage` property that includes information on tokens consumed on yoru deployment. You can validate this against your usage data on the deployment to corelate the usage from Content Understanding with the model deployment. 2Code has comments. Press enter to view.

``` JSON
{
  "usage": {
    "documentPages": 2,
    "tokens": {
      "contextualization": 2000,
      "input": 10400,
      "output": 360
    }
  }
}
```


## Next steps

* [Learn more about Content Understanding pricing](../pricing-explainer.md)

* [Learn more Content Understanding analyzers](analyzer-reference.md)