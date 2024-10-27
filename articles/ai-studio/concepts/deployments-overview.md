---
title: Deploy models in Azure AI studio
titleSuffix: Azure AI Studio
description: Learn about deploying models in Azure AI studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: concept-article
ms.date: 10/21/2024
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Overview: Deploy AI models in Azure AI Studio

The model catalog in Azure AI studio is the hub to discover and use a wide range of models for building generative AI applications. Models needs to be deployed to make them available for receiving inference requests. The process of interacting with a deployed model is called *inferencing*. Azure AI Studio offer a comprehensive suite of deployment options for those models depending on your needs and model requirements.

## Deploying models

Deployment options vary depending on the model type:

* **Azure OpenAI models:** The latest OpenAI models that have enterprise features from Azure.
* **Models as a Service models:** These models don't require compute quota from your subscription. This option allows you to deploy your Model as a Service (MaaS). You use a serverless API deployment and are billed per token in a pay-as-you-go fashion.
* **Open and custom models:** The model catalog offers access to a large variety of models across modalities that are of open access. You can host open models in your own subscription with a managed infrastructure, virtual machines, and the number of instances for capacity management. There's a wide range of models from Azure OpenAI, Hugging Face, and NVIDIA.

Azure AI studio offers 4 different deployment options:

|Name                           | Azure OpenAI Service | Azure AI model inference service | Serverless API | Managed compute |
|-------------------------------|----------------------|-------------------|----------------|-----------------|
| Which models can be deployed? | [Azure OpenAI models](../ai-services/openai/concepts/models.md)        | [Azure OpenAI models and Models as a Service](../ai-services/model-inference.md#models) | [Models as a Service](../how-to/model-catalog-overview.md#content-safety-for-models-deployed-via-serverless-apis) | [Open and custom models](../how-to/model-catalog-overview.md#availability-of-models-for-deployment-as-managed-compute) |
| Deployment resource           | Azure OpenAI service | Azure AI services | AI project | AI project |
| Best suited when              | You are planning to use only OpenAI models | You are planning to take advantage of the flagship models in Azure AI catalog, including OpenAI. | You are planning to use a single model from an specific provider (excluding OpenAI). | If you plan to use open models and you have enough compute quota available in your subscription. |
| Billing bases                 | Token usage          | Token usage       | Token usage<sup>1</sup>      | Compute core hours<sup>2</sup> |
| Deployment instructions       | [Deploy to Azure OpenAI Service](../how-to/deploy-models-openai.md) | [Deploy to Azure AI model inference](../ai-services/how-to/create-model-deployments.md) | [Deploy to Serverless API](../how-to/deploy-models-serverless.md) | [Deploy to Managed compute](../how-to/deploy-models-managed.md) |

<sup>1</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in pay-as-you-go. After you delete the endpoint, no further charges accrue.

<sup>2</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.

> [!TIP]
> To learn more about how to track costs, see [Monitor costs for models offered through Azure Marketplace](../how-to/costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

### How should I think about deployment options?

Azure AI studio encourage customers to explore the deployment options and pick the one that best suites their business and technical needs. In general you can use the following thinking process:

1. Start with the deployment options that has the bigger scopes. This allow you to iterate and prototype faster in your application without having to rebuild your architecture each time you decide to change something. [Azure AI model inference service](../ai-services/model-inference.md) is a deployment target that supports all the flagship models in the Azure AI catalog, including latest innovation from Azure OpenAI.

2. If you are looking to use an specific model:

   1. If you are interested in OpenAI models, use the Azure OpenAI Service which offers a wide range of capabilities for them and it's specifically designed for them.

   2. If you are interested in a particular model from Models as a Service and you don't expect to use any other type of model, use [Serverless API endpoints](../how-to/deploy-models-serverless.md) which allows deployment of a single model under a unique set of endpoint URL and keys.

3. If your model is not available in Models as a Service and you have compute quota available in your subscription, use [Managed Compute](../how-to/deploy-models-managed.md) which support deployment of open and custom models. It also allows high level of customization of the deployment inference server, protocols, and detailed configuration. 

> [!TIP]
> Each deployment option may offer different capabilities in terms of networking, security, and additional features like content safety. Review the documentation for each of them to understand their limitations. 


## Related content

- [Add and configure models to the Azure AI model inference service](../ai-services/how-to/create-model-deployments.md)
- [Deploy Azure OpenAI models with Azure AI Studio](../how-to/deploy-models-openai.md)
- [Deploy open models with Azure AI Studio](../how-to/deploy-models-open.md)
- [Model catalog and collections in Azure AI Studio](../how-to/model-catalog-overview.md)
