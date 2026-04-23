---
title: "Deployment overview for Microsoft Foundry Models"
description: "Learn about deployment options for Microsoft Foundry Models, including standard deployments in Foundry resources and managed compute for partner and community models."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 04/03/2026
ms.author: mopeakande
author: msakande
manager: nitinme
ai-usage: ai-assisted
#CustomerIntent: As a developer or AI practitioner, I want to understand the deployment options available for Microsoft Foundry Models so that I can choose the right deployment method for my models and use case.
---

# Deployment overview for Microsoft Foundry Models

Microsoft Foundry Models is the hub for discovering and deploying a wide range of AI models for generative AI applications. To make a model available for inference requests, you deploy it. Foundry offers two deployment options depending on the model type and your infrastructure needs.

## Deployment options

Foundry provides two deployment options:

- **Standard deployment in Foundry resources** — For Foundry Models, including [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) (also known as Azure Direct Models, or ADM) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md). This option is the preferred and most capable deployment path.
- **Managed compute deployment** — Available for all non-ADM models, including some models from partner and community, and custom models.

The Foundry portal automatically selects the appropriate deployment option based on the model you choose. Foundry Models deploy through Foundry resources. All other models deploy on managed compute.

| | Standard deployment in Foundry resources | Managed compute |
|---|---|---|
| **Models** | [ADM models](../foundry-models/concepts/models-sold-directly-by-azure.md) (Azure OpenAI + partner models billed through Azure) and select Models from partners and community(../foundry-models/concepts/models-from-partners.md)| Other models in the model catalog from partners and custom models.  For example, models from Hugging Face, NVIDIA NIMs, industry models, and Databricks. |
| **Billing** | Token usage or [provisioned throughput units (PTU)](../openai/concepts/provisioned-throughput.md) | Compute core hours (per-minute, per-instance) |
| **Data processing** | Regional, data zone, or global | Regional only |
| **Content filtering** | Built-in and customizable | Via Azure AI Content Safety APIs |

## Standard deployment in Foundry resources

Standard deployment in Foundry resources is **the preferred deployment option** in Foundry. It supports the widest range of capabilities and deployment types.

### Which models use standard deployment?

All Foundry Models, including [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md) use standard deployment. Foundry Models sold directly by Azure include all Azure OpenAI models and selected models from top providers that are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. Select Models from partners and community that use standard deployment include Anthropic models, and specific models from partners like Mistral, Cohere, and Meta.

### Capabilities

Standard deployment supports:

- **Multiple deployment types** — Global Standard, Data Zone Standard, Regional Standard, Provisioned, Batch, and more. Each type controls where data is processed and how you pay. For details, see [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md).
- **Data processing flexibility** — Choose regional, data zone (US or EU), or global processing based on your compliance requirements.
- **Content filtering** — Built-in Azure AI Content Safety filters with customizable configurations.
- **Keyless authentication** — Microsoft Entra ID (recommended) and key-based authentication.
- **Private networking** — Virtual network integration for secure access.
- **Provisioned throughput** — Reserve capacity with PTUs for predictable, low-latency performance. For details, see [Provisioned throughput](../openai/concepts/provisioned-throughput.md).

### Resource requirements

Standard deployment is available in:

- **Foundry resources** — The primary resource type for new Foundry projects. No AI Hub required.
- **Azure OpenAI resources** — If you use Azure OpenAI resources, the model catalog shows only Azure OpenAI models for deployment. Upgrade to a Foundry resource for access to the full set of Foundry Models.

To get started with deployment, see [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md) or [Deploy models using Azure CLI and Bicep](../foundry-models/how-to/create-model-deployments.md).

## Managed compute deployment

Managed compute deployment creates a dedicated endpoint that hosts the model on dedicated compute resources. This option is required for **all non-ADM models**.

> [!IMPORTANT]
Managed compute deployment creates a dedicated endpoint that hosts the model on dedicated compute resources. This option is required for models that don't belong to the category of [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md), such as custom models and industry models.

### Which models use managed compute?

Examples of model collections that require managed compute include:

- Hugging Face
- Some Meta models
- Some Mistral models
- NVIDIA inference microservices (NIMs)
- Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
- Databricks
- Custom models



### Capabilities

Managed compute supports:

- **Dedicated compute resources** — Model weights are deployed to dedicated virtual machines. A managed compute endpoint can host one or more deployments and exposes a REST API for inference.
- **Private networking** — Virtual network integration for secure access.
- **Key and Microsoft Entra authentication** — Secure access to your deployed endpoint.
- **Content safety** — Use the [Azure AI Content Safety](../../ai-services/content-safety/overview.md) service APIs to screen model responses. Content safety is billed separately.

### Billing and quota

Managed compute billing is based on compute core hours. You're billed per minute depending on the product tier and the number of instances in the deployment. After you delete the endpoint, no further charges accrue.

You need compute quota in your Azure subscription for the specific virtual machine products required to run the model. Some models allow deployment to a temporarily shared quota for testing.

### Get started

- [Deploy and infer with a managed compute deployment (classic)](../../foundry-classic/how-to/deploy-models-managed.md)
- [Deploy Foundry Models to managed compute with pay-as-you-go billing (classic)](../../foundry-classic/how-to/deploy-models-managed-pay-go.md)

## Deployment option comparison

Use [Standard deployment in Foundry resources](#standard-deployment-in-foundry-resources) whenever possible. The following table compares capabilities across the two deployment options:

| Capability | Standard deployment in Foundry resources | Managed compute |
|---|---|---|
| Which models can be deployed? | All Foundry Models, including [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md) | Custom models, industry models, and some partner models |
| Deployment resource | Foundry resource | AI project (hub-based, classic portal) |
| Requires AI Hub | No | Yes |
| Data processing options | Regional, data zone, global | Regional |
| Private networking | Yes | Yes |
| Content filtering | Built-in and customizable | Via Azure AI Content Safety APIs |
| Keyless authentication | Yes (Microsoft Entra ID) | Key-based and Microsoft Entra |
| Billing | Token usage or [provisioned throughput units](../openai/concepts/provisioned-throughput.md) | Compute core hours |

> [!TIP]
> For detailed pricing information, see [Plan and manage costs for Foundry Tools](manage-costs.md).

## Related content

- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md)
- [Deploy models using Azure CLI and Bicep](../foundry-models/how-to/create-model-deployments.md)
- [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Foundry Models from partners and community](../foundry-models/concepts/models-from-partners.md)
- [Microsoft Foundry Models overview](foundry-models-overview.md)
- [Plan and manage costs for Foundry Tools](manage-costs.md)
