---
title: Deployment options for Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about deployment options for Azure AI Foundry Models.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 06/26/2025
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# Deployment overview for Azure AI Foundry Models

The model catalog in Azure AI Foundry is the hub to discover and use a wide range of Foundry Models for building generative AI applications. Models need to be deployed to make them available for receiving inference requests. Azure AI Foundry offers a comprehensive suite of deployment options for Foundry Models, depending on your needs and model requirements.

## Deployment options

Azure AI Foundry provides several deployment options depending on the type of models and resources you need to provision. The following deployment options are available:

- Standard deployment in Azure AI Foundry resources
- Deployment to serverless API endpoints
- Deployment to managed computes

### Standard deployment in Azure AI Foundry resources

Azure AI Foundry resources (formerly referred to as Azure AI model inference, in Azure AI Services), is **the preferred deployment option** in Azure AI Foundry. It offers the widest range of capabilities, including regional, data zone, or global processing, and it offers standard and [provisioned throughput (PTU)](../../ai-services/openai/concepts/provisioned-throughput.md) options. Flagship models in Azure AI Foundry Models support this deployment option.

This deployment option is available in:

* Azure AI Foundry resources
* Azure OpenAI resources<sup>1</sup>
* Azure AI hub, when connected to an Azure AI Foundry resource (requires the [Deploy models to Azure AI Foundry resources](#configure-azure-ai-foundry-portal-for-deployment-options) feature to be turned on).

<sup>1</sup>If you're using Azure OpenAI resources, the model catalog shows only Azure OpenAI in Foundry Models for deployment. You can get the full list of Foundry Models by upgrading to an Azure AI Foundry resource.

To get started with standard deployment in Azure AI Foundry resources, see [How-to: Deploy models to Azure AI Foundry Models](../foundry-models/how-to/create-model-deployments.md).

### Serverless API endpoint

This deployment option is available **only in** [Azure AI hub resources](ai-resources.md) and it allows the creation of dedicated endpoints to host the model, accessible via API. Azure AI Foundry Models support serverless API endpoints with pay-as-you-go billing. 

Only regional deployments can be created for serverless API endpoints, and to use it, you _must_ **turn off** the "Deploy models to Azure AI Foundry resources" option.

To get started with deployment to a serverless API endpoint, see [Deploy models as serverless API deployments](../how-to/deploy-models-serverless.md).

### Managed compute

This deployment option is available **only in** [Azure AI hub resources](ai-resources.md) and it allows the creation of a dedicated endpoint to host the model in a **dedicated compute**. You need to have compute quota in your subscription to host the model, and you're billed per compute uptime. 

Managed compute deployment is required for model collections that include:

* Hugging Face
* NVIDIA inference microservices (NIMs)
* Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
* Databricks
* Custom models

To get started, see [How to deploy and inference a managed compute deployment](../how-to/deploy-models-managed.md) and [Deploy Azure AI Foundry Models to managed compute with pay-as-you-go billing](../how-to/deploy-models-managed-pay-go.md).

## Capabilities for the deployment options

We recommend using [Standard deployments in Azure AI Foundry resources](#standard-deployment-in-azure-ai-foundry-resources) whenever possible, as it offers the largest set of capabilities among the available deployment options. The following table lists details about specific capabilities available for each deployment option:

| Capability                    | Azure OpenAI | Standard deployment in Azure AI Foundry resources| Serverless API Endpoint | Managed compute |
|-------------------------------|----------------------|-------------------|----------------|-----------------|
| Which models can be deployed? | [Azure OpenAI models](../../ai-services/openai/concepts/models.md)        | [Foundry Models](../../ai-foundry/foundry-models/concepts/models.md) | [Foundry Models with pay-as-you-go billing](../how-to/model-catalog-overview.md) | [Open and custom models](../how-to/model-catalog-overview.md#availability-of-models-for-deployment-as-managed-compute) |
| Deployment resource           | Azure OpenAI resource | Azure AI Foundry resource  | AI project (in AI hub resource) | AI project (in AI hub resource) |
| Requires AI Hubs              | No | No | Yes | Yes |
| Data processing options       | Regional <br /> Data-zone  <br /> Global | Regional <br /> Data-zone  <br /> Global | Regional | Regional |
| Private networking            | Yes | Yes | Yes | Yes |
| Content filtering             | Yes | Yes | Yes | No  |
| Custom content filtering      | Yes | Yes | No  | No  |
| Key-less authentication       | Yes | Yes | No  | No  |
| Billing bases                 | Token usage & [provisioned throughput units](../../ai-services/openai/concepts/provisioned-throughput.md)        | Token usage & [provisioned throughput units](../../ai-services/openai/concepts/provisioned-throughput.md)       | Token usage<sup>1</sup>      | Compute core hours<sup>2</sup> |

<sup>1</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in standard deployment. After you delete the endpoint, no further charges accrue.

<sup>2</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.

## Configure Azure AI Foundry portal for deployment options

Azure AI Foundry portal might automatically pick up a deployment option based on your environment and configuration. We recommend using Azure AI Foundry resources for deployment whenever possible. To do that, ensure that the **Deploy models to Azure AI Foundry resources** feature is **turned on**. 

:::image type="content" source="../media/concepts/deployments-overview/docs-flag-enable-foundry.png" alt-text="A screenshot showing the steps to enable deployment to Azure AI Foundry resources in the Azure AI Foundry portal." lightbox="../media/concepts/deployments-overview/docs-flag-enable-foundry.png":::

Once the **Deploy models to Azure AI Foundry resources** feature is enabled, models that support multiple deployment options default to deploy to Azure AI Foundry resources for deployment. To access other deployment options, either disable the feature or use the Azure CLI or Azure Machine Learning SDK for deployment. You can disable and enable the feature as many times as needed without affecting existing deployments.

## Related content

* [Configure your AI project to use Foundry Models](../../ai-foundry/foundry-models/how-to/quickstart-ai-project.md)
* [Add and configure models to Foundry Models](../foundry-models/how-to/create-model-deployments.md)
* [Deploy Azure OpenAI models with Azure AI Foundry](../how-to/deploy-models-openai.md)
* [Deploy open models with Azure AI Foundry](../how-to/deploy-models-managed.md)
* [Explore Azure AI Foundry Models](../how-to/model-catalog-overview.md)
