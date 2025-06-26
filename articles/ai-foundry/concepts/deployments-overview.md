---
title: Deploy models in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn about deploying models in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 06/26/2025
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Overview: Deploy AI models in Azure AI Foundry

The model catalog in Azure AI Foundry is the hub to discover and use a wide range of models for building generative AI applications. Models need to be deployed to make them available for receiving inference requests. Azure AI Foundry offers a comprehensive suite of deployment options for models, depending on your needs and model requirements.

## Deployment options

Azure AI Foundry provides multiple deployment options depending on the type of resources and models that you need to provision. The following 3 deployment options are available:

### Standard deployments in Azure AI Foundry resources

Formerly known Azure AI model inference in Azure AI Services, is **the preferred deployment option** in Azure AI Foundry. It offers the biggest range of options including regional, data zone, or global processing; and standard and provisioned (PTU) options. Flagship models in Azure AI Foundry Models support this deployment option.

This deployment option is available in:

* Azure OpenAI resources<sup>1</sup>
* Azure AI Foundry resources (formerly known Azure AI Services)
* Azure AI Hub when connected to an Azure AI Foundry resource (requires the feature [Deploy models to Azure AI Foundry resources](#configure-azure-ai-foundry-portal-for-deployment-options) on).

<sup>1</sup>If you are using Azure OpenAI resources, the model catalog only shows Azure OpenAI models for deployment. You can get the full list of models by upgrading to an Azure AI Foundry resource.

To get started, see [How-to: Deploy models to Azure AI Foundry Models](../model-inference/how-to/create-model-deployments.md).

### Serverless API Endpoint

This option is available **only in Azure AI Hubs resources** and it allows the creation of dedicated endpoints to host the model, accessible via API with pay-as-you-go billing. It's supported by Azure AI Foundry Models with pay-as-you-go billing. Only regional deployments can be created for Serverless API Endpoints. It requires the feature [Deploy models to Azure AI Foundry resources](#configure-azure-ai-foundry-portal-for-deployment-options) **off**.

To get started, see [How-to: Deploy models to Serverless API Endpoints](../model-inference/how-to/create-model-deployments.md)

### Managed Compute

This option is available **only in Azure AI Hubs resources** and it allows the creation of dedicated endpoint to host the model in **dedicated compute**. You need to have compute quota in your subscription to host the model and you are billed per compute up-time. 

This option is required for the following model collections:

* Hugging Face
* NVIDIA NIMs
* Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
* Databricks
* Custom models

To get started, see [How-to: Deploy to Managed compute](../how-to/deploy-models-managed.md).

## Features

We recommend using Standard deployments in Azure AI Foundry resources (formerly known Azure AI model inference in Azure AI Services) whenever possible as it offers the larger set of features. The following table shows details about specific features available on each deployment option:

| Feature                       | Azure OpenAI | Azure AI Foundry | Serverless API Endpoint | Managed compute |
|-------------------------------|----------------------|-------------------|----------------|-----------------|
| Which models can be deployed? | [Azure OpenAI models](../../ai-services/openai/concepts/models.md)        | [Azure OpenAI models and Foundry Models with pay-as-you-go billing](../../ai-foundry/model-inference/concepts/models.md) | [Foundry Models with pay-as-you-go billing](../how-to/model-catalog-overview.md) | [Open and custom models](../how-to/model-catalog-overview.md#availability-of-models-for-deployment-as-managed-compute) |
| Deployment resource           | Azure OpenAI resource | Azure AI Foundry resource (formerly known Azure AI Services) | AI project (in AI Hub resource) | AI project (in AI Hub resource) |
| Requires AI Hubs              | No | No | Yes | Yes |
| Data processing options       | Regional <br /> Data-zone  <br /> Global | Regional <br /> Data-zone  <br /> Global | Regional | Regional |
| Private networking            | Yes | Yes | Yes | Yes |
| Content filtering             | Yes | Yes | Yes | No  |
| Custom content filtering      | Yes | Yes | No  | No  |
| Key-less authentication       | Yes | Yes | No  | No  |
| Billing bases                 | Token usage & [provisioned throughput units](../../ai-services/openai/concepts/provisioned-throughput.md)        | Token usage       | Token usage<sup>1</sup>      | Compute core hours<sup>2</sup> |

<sup>1</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in standard deployment. After you delete the endpoint, no further charges accrue.

<sup>2</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.

## Configure Azure AI Foundry portal for deployment options

Azure AI Foundry portal may automatically pick up a deployment option based on your environment and configuration. When possible, we default to the most convenient deployment option available to you.

We recommend using Azure AI Foundry resources (formerly known Azure AI Services) for deployment whenever possible. To do that, ensure you have the feature **Deploy models to Azure AI Foundry resources** on. 

:::image type="content" source="../model-inference/media/models/docs-flag-enable-foundry.gif" alt-text="An animation showing how to enable deployment to Azure AI Foundry resources (formerly known Azure AI Services)." lightbox="../model-inference/media/models/docs-flag-enable-foundry.gif":::

Notice that once enabled, models that support multiple deployment options will default to deploy to Azure AI Foundry resources for deployment. To access other deployment options, either disable the feature or use the Azure CLI or Azure Machine Learning SDK for deployment. You can disable and enable the feature as many times as needed. Existing deployments won't be affected.

## Related content

* [Configure your AI project to use Foundry Models](../../ai-foundry/model-inference/how-to/quickstart-ai-project.md)
* [Add and configure models to Foundry Models](../model-inference/how-to/create-model-deployments.md)
* [Deploy Azure OpenAI models with Azure AI Foundry](../how-to/deploy-models-openai.md)
* [Deploy open models with Azure AI Foundry](../how-to/deploy-models-managed.md)
* [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
