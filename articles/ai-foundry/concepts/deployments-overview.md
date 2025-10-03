---
title: Deployment options for Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about deployment options for Azure AI Foundry Models including standard, serverless API, and managed compute deployments.
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 09/22/2025
ms.author: mopeakande
author: msakande
manager: nitinme
#CustomerIntent: As a developer or AI practitioner, I want to understand the different deployment options available for Azure AI Foundry Models so that I can choose the most appropriate deployment method for my specific use case, requirements, and infrastructure needs.
---

# Deployment overview for Azure AI Foundry Models

The model catalog in Azure AI Foundry is the hub to discover and use a wide range of Foundry Models for building generative AI applications. You need to deploy models to make them available for receiving inference requests. Azure AI Foundry offers a comprehensive suite of deployment options for Foundry Models, depending on your needs and model requirements.

## Deployment options

Azure AI Foundry provides several deployment options depending on the type of models and resources you need to provision. The following deployment options are available:

- Standard deployment in Azure AI Foundry resources
- Deployment to serverless API endpoints
- Deployment to managed computes

Azure AI Foundry portal might automatically pick a deployment option based on your environment and configuration. Use Azure AI Foundry resources for deployment whenever possible. 
Models that support multiple deployment options default to Azure AI Foundry resources for deployment. To access other deployment options, use the Azure CLI or Azure Machine Learning SDK for deployment.

### Standard deployment in Azure AI Foundry resources

Azure AI Foundry resources (formerly referred to as Azure AI Services resources), is **the preferred deployment option** in Azure AI Foundry. It offers the widest range of capabilities, including regional, data zone, or global processing, and it offers standard and [provisioned throughput (PTU)](../../ai-services/openai/concepts/provisioned-throughput.md) options. Flagship models in Azure AI Foundry Models support this deployment option.

This deployment option is available in:

* Azure AI Foundry resources
* Azure OpenAI resources<sup>1</sup>
* Azure AI hub, when connected to an Azure AI Foundry resource

<sup>1</sup>If you use Azure OpenAI resources, the model catalog shows only Azure OpenAI in Foundry Models for deployment. You can get the full list of Foundry Models by upgrading to an Azure AI Foundry resource.

To get started with standard deployment in Azure AI Foundry resources, see [How-to: Deploy models to Azure AI Foundry Models](../foundry-models/how-to/create-model-deployments.md).

### Serverless API endpoint

This deployment option is available **only in** [Azure AI hub resources](ai-resources.md). It allows you to create dedicated endpoints to host the model, accessible through an API. Azure AI Foundry Models support serverless API endpoints with pay-as-you-go billing, and you can create only regional deployments for serverless API endpoints.

To get started with deployment to a serverless API endpoint, see [Deploy models as serverless API deployments](../how-to/deploy-models-serverless.md).

### Managed compute

This deployment option is available **only in** [Azure AI hub resources](ai-resources.md). It allows you to create a dedicated endpoint to host the model in a **dedicated compute**. You need to have compute quota in your subscription to host the model, and you're billed per compute uptime. 

Managed compute deployment is required for model collections that include:

* Hugging Face
* NVIDIA inference microservices (NIMs)
* Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
* Databricks
* Custom models

To get started, see [How to deploy and inference a managed compute deployment](../how-to/deploy-models-managed.md) and [Deploy Azure AI Foundry Models to managed compute with pay-as-you-go billing](../how-to/deploy-models-managed-pay-go.md).

## Capabilities for the deployment options

Use [Standard deployments in Azure AI Foundry resources](#standard-deployment-in-azure-ai-foundry-resources) whenever possible. This deployment option provides the most capabilities among the available deployment options. The following table lists details about specific capabilities for each deployment option:

| Capability                    | Standard deployment in Azure AI Foundry resources | Serverless API Endpoint | Managed compute |
|-------------------------------|--------------------------------------------------|------------------------|-----------------|
| Which models can be deployed? | [Foundry Models](../../ai-foundry/foundry-models/concepts/models.md) | [Foundry Models with pay-as-you-go billing](../how-to/model-catalog-overview.md) | [Open and custom models](../how-to/model-catalog-overview.md#availability-of-models-for-deployment-as-managed-compute) |
| Deployment resource           | Azure AI Foundry resource                         | AI project (in AI hub resource) | AI project (in AI hub resource) |
| Requires AI Hubs              | No                                               | Yes                   | Yes            |
| Data processing options       | Regional <br /> Data-zone  <br /> Global         | Regional              | Regional       |
| Private networking            | Yes                                              | Yes                   | Yes            |
| Content filtering             | Yes                                              | Yes                   | No             |
| Custom content filtering      | Yes                                              | No                    | No             |
| Key-less authentication       | Yes                                              | No                    | No             |
| Billing bases                 | Token usage & [provisioned throughput units](../../ai-services/openai/concepts/provisioned-throughput.md) | Token usage<sup>2</sup> | Compute core hours<sup>3</sup> |

<sup>2</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in serverless deployment. After you delete the endpoint, no further charges accrue.

<sup>3</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.


## Related content

* [Configure your AI project to use Foundry Models](../../ai-foundry/foundry-models/how-to/quickstart-ai-project.md)
* [Deployment types in Azure AI Foundry Models](../foundry-models/concepts/deployment-types.md)
* [Deploy Azure OpenAI models with Azure AI Foundry](../how-to/deploy-models-openai.md)
* [Deploy open models with Azure AI Foundry](../how-to/deploy-models-managed.md)
* [Explore Azure AI Foundry Models](../how-to/model-catalog-overview.md)
