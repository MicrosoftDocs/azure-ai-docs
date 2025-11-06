---
title: Connect your Content Understanding resource with Foundry models
titleSuffix: Azure AI services
description: Describes the requirements and flexibility of specifying Gen AI model and deployment information for Content Understanding analyzers 
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/26/2025
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.custom:
  - ignite-2025
---

# Connect your Content Understanding analyzer to Foundry model deployments

Content Understanding uses your Foundry model deployments for all operations that require a Generative AI model. This approach enables you to maximize your use of the capacity provisioned and aggregate capacity into fewer deployments if needed. You can also pick the model that fits your scenario best for price and latency. 

You're billed for all tokens (input and output) processed by the connected deployment, and Content Understanding only bills you for the Content-Understanding-specific meters. See [pricing explainer](../overview/pricing-explainer.md) to learn more about the billing model.

The service requires a `chat completion` model and `embeddings` model and supports a few different options for each. Some analyzers have a dependency on a specific model.

## Supported models

The service is periodically updated to add support for more models. The currently supported models are:

| Model Type | Model | Version |
|--|--|--|
|Chat Completion | gpt-4o | `2024-08-06` |
|Chat Completion | gpt-4o | `2024-11-20` |
|Chat Completion | gpt-4o-mini | `2024-11-20` |
|Chat Completion | gpt-4.1 | `2024-11-20` |
|Chat Completion | gpt-4.1-mini | `2024-11-20` |
|Chat Completion |gpt-4.1-nano | `2024-11-20` |
|Embeddings | text-embedding-3-small |  |
|Embeddings | text-embedding-3-large |  |
|Embeddings | text-embedding-ada-002 |  |

## Configure models and deployments

Content Understanding analyzers that utilize Generative AI (Gen AI) models now require explicit specification of both the model and deployment details. These details can be configured at the resource level, applying to all operations by default, or can be overridden for individual analyze operations as needed. This approach provides organizations with the flexibility to support multiple business teams, enabling each team to use the same analyzer with different Gen AI models or deployments according to their specific requirements.

The model and deployment definition is a multi-step process.

1. You can specify the deployments to use on the resource via a ```PATCH``` request. We recommend that you set this default model and deployment to ensure your analyzers always have a valid model deployment to use. To set the default deployment, update the Content Understanding resource with the deployments. GPT4.1 is a recommended model for use with the Foundry and the Studio. You can experiment or use any of the supported chat completion models in addition to GPT4.1. The embeddings models are used when you use labeled samples or in-context learning to improve the quality of your analyzer.
    
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

1. Define the models that a specific analyzer should use when building the analyzer. At build time, associate each analyzer with a specific chat completion model and an embeddings model. This configuration provides the flexibility of picking a model that provides the best results at the lowest cost. The analyzer definition only associates a model with the analyzer and not the deployment. 
    
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

1. At analyze time, connect the model that the analyzer should use with the deployment. If you have defaults defined on the resource, no `modelDeplyments` are needed, if no defaults are defined on the resource, or you want to override the defaults, provide the `modelDeployments` to use.
    
    ``` JSON
    POST /myReceipt:analyze
    {
    
      "modelDeployments": {
        "gpt-4.1": "myGpt41Deployment"
      }
    }
    
    ```

    > [!NOTE]
    > [Prebuilt analyzers](../concepts/prebuilt-analyzers.md) require a specific model. See the models catalog for the models each prebuilt works with.

Your analyzer is now connected to a Foundry model deployment and ready for use.

## Test the analyzer

Submit an analyze request for the analyzer and validate that the response is accurate. In addition to the content and fields in the response, the response object contains a `usage` property that includes information on tokens consumed on your deployment. You can validate this data against your usage data on the deployment to correlate the usage from Content Understanding with the model deployment.

``` JSON
{
  "usage": {
    "documentPagesMinimal": 3, // The number of document pages processed at the minimal level (txt, xlsx, html, and other digital file types)
    "documentPagesBasic": 2, // The number of document pages processed at the basic level (read)
    "documentPagesStandard": 1, // The number of document pages processed at the standard level (layout)
    "audioHours": 0.234,
    "videoHours": 0.123,
    "contextualizationToken": 1000,
    "tokens": {
      "gpt-4.1-input": 1234,
      "gpt-4.1-output": 2345,
      "text-embedding-3-large": 3456
    }
  }
}
```


## Related content

* [Learn more about Content Understanding pricing](../overview/pricing-explainer.md)

* [Learn more Content Understanding analyzers](analyzer-reference.md)