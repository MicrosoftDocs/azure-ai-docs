---
title: Deploy models in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn about deploying models in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 03/24/2025
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Overview: Deploy AI models in Azure AI Foundry portal

The model catalog in Azure AI Foundry portal is the hub to discover and use a wide range of models for building generative AI applications. Models need to be deployed to make them available for receiving inference requests. Azure AI Foundry offers a comprehensive suite of deployment options for models, depending on your needs and model requirements.

## Deploying models

Deployment options vary depending on the model offering:

* **Azure OpenAI in Azure AI Foundry Models:** The latest OpenAI models that have enterprise features from Azure with flexible billing options.
* **Standard deployment:** These models don't require compute quota from your subscription and are billed per token in a pay-as-you-go fashion. 
* **Open and custom models:** The model catalog offers access to a large variety of models across modalities, including models of open access. You can host open models in your own subscription with a managed infrastructure, virtual machines, and the number of instances for capacity management.

Azure AI Foundry offers four different deployment options:

|Name                           | Azure OpenAI | Azure AI model inference | Standard deployment | Managed compute |
|-------------------------------|----------------------|-------------------|----------------|-----------------|
| Which models can be deployed? | [Azure OpenAI models](../../ai-services/openai/concepts/models.md)        | [Azure OpenAI models and Standard deployment](../../ai-foundry/model-inference/concepts/models.md) | [Standard deployment](../how-to/model-catalog-overview.md#content-safety-for-models-deployed-via-serverless-apis) | [Open and custom models](../how-to/model-catalog-overview.md#availability-of-models-for-deployment-as-managed-compute) |
| Deployment resource           | Azure OpenAI resource | Azure AI services resource | AI project resource | AI project resource |
| Requires Hubs/Projects        | No | No | Yes | Yes |
| Data processing options       | Regional <br /> Data-zone  <br /> Global | Global | Regional | Regional |
| Private networking            | Yes | Yes | Yes | Yes |
| Content filtering             | Yes | Yes | Yes | No  |
| Custom content filtering      | Yes | Yes | No  | No  |
| Key-less authentication       | Yes | Yes | No  | No  |
| Best suited when              | You're planning to use only OpenAI models | You're planning to take advantage of the flagship models in Azure AI catalog, including OpenAI. | You're planning to use a single model from a specific provider (excluding OpenAI). | If you plan to use open models and you have enough compute quota available in your subscription. |
| Billing bases                 | Token usage & [provisioned throughput units](../../ai-services/openai/concepts/provisioned-throughput.md)        | Token usage       | Token usage<sup>1</sup>      | Compute core hours<sup>2</sup> |
| Deployment instructions       | [Deploy to Azure OpenAI](../how-to/deploy-models-openai.md) | [Deploy to Azure AI model inference](../model-inference/how-to/create-model-deployments.md) | [Deploy to Standard deployment](../how-to/deploy-models-serverless.md) | [Deploy to Managed compute](../how-to/deploy-models-managed.md) |

<sup>1</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in pay-as-you-go. After you delete the endpoint, no further charges accrue.

<sup>2</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.

> [!TIP]
> To learn more about how to track costs, see [Monitor costs for models offered through Azure Marketplace](../how-to/costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

### How should I think about deployment options?

Azure AI Foundry encourages you to explore various deployment options and choose the one that best suites your business and technical needs. In general, Consider using the following approach to select a deployment option:

* Start with [Azure AI model inference](../../ai-foundry/model-inference/overview.md), which is the option with the largest scope. This option allows you to iterate and prototype faster in your application without having to rebuild your architecture each time you decide to change something. If you're using Azure AI Foundry hubs or projects, enable this option by [turning on the Azure AI model inference feature](../model-inference/how-to/quickstart-ai-project.md#configure-the-project-to-use-azure-ai-model-inference).

* When you're looking to use a specific model:

   * If you're interested in Azure OpenAI models, use Azure OpenAI in Foundry Models. This option is designed for Azure OpenAI models and offers a wide range of capabilities for them.

   * If you're interested in a particular model from serverless pay per token offer, and you don't expect to use any other type of model, use [Standard deployment](../how-to/deploy-models-serverless.md). Standard deployments allow deployment of a single model under a unique set of endpoint URL and keys.

* When your model isn't available in standard deployment and you have compute quota available in your subscription, use [Managed Compute](../how-to/deploy-models-managed.md), which supports deployment of open and custom models. It also allows a high level of customization of the deployment inference server, protocols, and detailed configuration.


## Related content

* [Configure your AI project to use Azure AI model inference](../../ai-foundry/model-inference/how-to/quickstart-ai-project.md)
* [Add and configure models to Azure AI model inference](../model-inference/how-to/create-model-deployments.md)
* [Deploy Azure OpenAI models with Azure AI Foundry](../how-to/deploy-models-openai.md)
* [Deploy open models with Azure AI Foundry](../how-to/deploy-models-managed.md)
* [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
