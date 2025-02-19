---
title: How to deploy Stability AI family of models with AI Foundry
titleSuffix: Azure AI Foundry
description: How to deploy Stability AI family of models with AI Foundry
manager: scottpolly
ms.service: azure-machine-learning
ms.topic: how-to
ms.date: 01/23/2025
ms.author: timanghn
author: tinaem
ms.reviewer: ssalgado
reviewer: ssalgadodev
ms.custom: references_regions
---

# How to deploy Stability AI family of models with AI Foundry

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to use Azure AI Foundry to deploy Stability AI collection of models as a serverless API with pay-as-you-go billing.

The Stability AI collection of models include Stable Image Core, Stable Image Ultra and Stable Diffusion 3.5 Large. 

### Stable Diffusion 3.5 Large

At 8.1 billion parameters, with superior quality and prompt adherence, this base model is the most powerful in the Stable Diffusion family and is ideal for professional use cases at 1 megapixel resolution. 

Stable Diffusion 3.5 large supports text and image prompt inputs for image generations. 

### Stable Image Core

Leveraging an enhanced version of SDXL, Stable Image Core, delivers exceptional speed and efficiency while maintaining the high-quality output synonymous with Stable Diffusion models.

Stable Image Core supports text prompt inputs only for image generations.

### Stable Image Ultra

Powered by the advanced capabilities of Stable Diffusion 3.5 Large, Stable Image Ultra sets a new standard in photorealism. Stable Image Ultra is ideal for product imagery in marketing and advertising. It also excels in typography, dynamic lighting, and vibrant color rendering.

Stable Image Ultra supports text prompt inputs only for image generations.

[!INCLUDE [models-preview](../includes/models-preview.md)]


## Deploy a Stability AI model as a serverless API

Stability AI models in the model catalog can be deployed as a serverless API with pay-as-you-go billing, providing a way to consume them as an API without hosting them on your subscription, while keeping the enterprise security and compliance organizations need. This deployment option doesn't require quota from your subscription. 


### Prerequisites

To use Stability AI models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Stability AI models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](deploy-models-serverless.md)

### Consume Stability AI models as a serverless API

1. In the **workspace**, select **Endpoints** > **Serverless endpoints**.
1. Find and select the `Stable Diffusion 3.5 Large` deployment you created.
1. Copy the **Target** URL and the **Key** token values.
1. Make an API request based on the type of model you deployed. To see an example request, see the [reference section](#reference-for-stability-ai-models-deployed-as-a-serverless-api). 

### Reference for Stability AI models deployed as a serverless API

Stability AI models on Models as a Service implement the [Azure AI Model Inference API](../reference/reference-model-inference-api.md) on the route `/image/generations` 

#### Request example 

```
{
      "prompt": "A photo of a cat",
      "negative_prompt": "A photo of a dog",
      "image_prompt": {
        "image": "puqkvvlvgcjyzughesnkena",
        "strength": 1
        },
      "size": "1024x1024",
      "output_format": "png",
      "seed": 26
}
```

#### Response

```
{
    "image": "iVBORw0KGgoAAAANSUhEUgAABgA...",
    "created": 1739161682
}
```

Follow this link for a full encoded [image generation response](https://github.com/MicrosoftDocs/azure-ai-docs-pr/pull/2896/$0). 

## Cost and quotas

### Cost and quota considerations for Stability AI models deployed as a serverless API

The Stability AI models are deployed as a serverless API and is offered by Stability AI through Azure Marketplace and integrated with AI Foundry for use. You can find Azure Marketplace pricing when deploying or fine-tuning models.

Each time a workspace subscribes to a given model offering from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference and fine-tuning; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](./costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

## Content filtering

Models deployed as a serverless API are protected by Azure AI content safety. When deployed to managed compute, you can opt out of this capability. With Azure AI content safety enabled, both the prompt and completion pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Learn more about [Azure AI Content Safety](/azure/ai-services/content-safety/overview).

## Related content

- [Model Catalog and Collections](./model-catalog-overview.md)
- [Plan and manage costs for Azure AI Foundry](./costs-plan-manage.md)
