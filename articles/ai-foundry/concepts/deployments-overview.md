---
title: Deployment options for Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn about deployment options for Microsoft Foundry Models including standard, serverless API, and managed compute deployments.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 01/30/2026
ms.author: mopeakande
author: msakande
manager: nitinme
#CustomerIntent: As a developer or AI practitioner, I want to understand the different deployment options available for Microsoft Foundry Models so that I can choose the most appropriate deployment method for my specific use case, requirements, and infrastructure needs.
---

# Deployment overview for Microsoft Foundry Models

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The model catalog in Microsoft Foundry is the hub to discover and use a wide range of Foundry Models for building generative AI applications. You need to deploy models to make them available for receiving inference requests. Foundry offers a comprehensive suite of deployment options for Foundry Models, depending on your needs and model requirements.

## Deployment options

Foundry provides several deployment options depending on the type of models and resources you need to provision. The following deployment options are available:

- Standard deployment in Foundry resources
- Deployment to serverless API endpoints
- Deployment to managed computes

Foundry portal might automatically pick a deployment option based on your environment and configuration. Use Foundry resources for deployment whenever possible. 
Models that support multiple deployment options default to Foundry resources for deployment. To access other deployment options, use the Azure CLI or Azure Machine Learning SDK for deployment.

### Standard deployment in Foundry resources

Foundry resources is **the preferred deployment option** in Foundry. It offers the widest range of capabilities, including regional, data zone, or global processing, and it offers standard and [provisioned throughput (PTU)](../openai/concepts/provisioned-throughput.md) options. Flagship models in Foundry Models support this deployment option.

This deployment option is available in:

* Foundry resources
* Azure OpenAI resources<sup>1</sup>
* Azure AI hub, when connected to a Foundry resource

<sup>1</sup>If you use Azure OpenAI resources, the model catalog shows only Azure OpenAI in Foundry Models for deployment. You can get the full list of Foundry Models by upgrading to a Foundry resource.

To get started with standard deployment in Foundry resources, see [How-to: Deploy models to Foundry Models](../foundry-models/how-to/create-model-deployments.md).

### Serverless API endpoint

This deployment option is available **only in** [AI Hub resources](ai-resources.md). It allows you to create dedicated endpoints to host the model, accessible through an API. Foundry Models support serverless API endpoints with pay-as-you-go billing, and you can create only regional deployments for serverless API endpoints.

To get started with deployment to a serverless API endpoint, see [Deploy models as serverless API deployments](../how-to/deploy-models-serverless.md).

### Managed compute

This deployment option is available **only in** [AI Hub resources](ai-resources.md). It allows you to create a dedicated endpoint to host the model in a **dedicated compute**. You need to have compute quota in your subscription to host the model, and you're billed per compute uptime. 

Managed compute deployment is required for model collections that include:

* Hugging Face
* NVIDIA inference microservices (NIMs)
* Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
* Databricks
* Custom models

To get started, see [How to deploy and inference a managed compute deployment](../how-to/deploy-models-managed.md) and [Deploy Foundry Models to managed compute with pay-as-you-go billing](../how-to/deploy-models-managed-pay-go.md).

## Capabilities for the deployment options

Use [Standard deployments in Foundry resources](#standard-deployment-in-foundry-resources) whenever possible. This deployment option provides the most capabilities among the available deployment options. The following table lists details about specific capabilities for each deployment option:

| Capability                    | Standard deployment in Foundry resources | Serverless API Endpoint | Managed compute |
|-------------------------------|--------------------------------------------------|------------------------|-----------------|
| Which models can be deployed? | [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) <br> [Foundry Models from partners and community](../foundry-models/concepts/models-from-partners.md) | [Foundry Models with pay-as-you-go billing](../how-to/deploy-models-serverless-availability.md) | [Open and custom models](../how-to/deploy-models-managed.md) |
| Deployment resource           | Foundry resource                         | AI project (in AI hub resource) | AI project (in AI hub resource) |
| Requires AI Hubs              | No                                               | Yes                   | Yes            |
| Data processing options       | Regional <br /> Data-zone  <br /> Global         | Regional              | Regional       |
| Private networking            | Yes                                              | Yes                   | Yes            |
| Content filtering             | Yes                                              | Yes                   | No             |
| Custom content filtering      | Yes                                              | No                    | No             |
| Key-less authentication       | Yes                                              | No                    | No             |
| Billing bases                 | Token usage & [provisioned throughput units](../openai/concepts/provisioned-throughput.md) | Token usage<sup>2</sup> | Compute core hours<sup>3</sup> |

<sup>2</sup> A minimal endpoint infrastructure is billed per minute. You aren't billed for the infrastructure that hosts the model in serverless deployment. After you delete the endpoint, no further charges accrue.

<sup>3</sup> Billing is on a per-minute basis, depending on the product tier and the number of instances used in the deployment since the moment of creation. After you delete the endpoint, no further charges accrue.


## Related content

* [Deployment types in Foundry Models](../foundry-models/concepts/deployment-types.md)
* [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md)
* [Deploy Microsoft Foundry Models to managed compute with pay-as-you-go billing](../how-to/deploy-models-managed-pay-go.md)
* [Explore Foundry Models](foundry-models-overview.md)
