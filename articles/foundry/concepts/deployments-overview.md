---
title: "Deployment overview for Microsoft Foundry Models"
description: "Learn about deployment options for Microsoft Foundry Models, including standard deployments in Foundry resources and managed compute for partner and community models."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
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

[!INCLUDE [try-instant-models](../includes/try-instant-models.md)]

## Deployment options

Foundry provides two deployment options:

- **Standard deployment in Foundry resources** — For Foundry Models, including [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) (also known as Azure Direct Models, or ADM) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md). This option is the preferred and most capable deployment path.
- **Managed compute deployment** — Available for all OSS models, inlcuding models from partner and community, and custom models.

The Foundry portal automatically selects the appropriate deployment option based on the model you choose. 

| | Standard deployment in Foundry resources | Managed compute |
|---|---|---|
| **Models** | [ADM models](../foundry-models/concepts/models-sold-directly-by-azure.md) (Azure OpenAI + partner models billed through Azure) and select [Models from partners and community](../foundry-models/concepts/models-from-partners.md)| Other models in the model catalog from partners and custom models.  For example, models from Hugging Face, NVIDIA NIMs, industry models, and Databricks. |
| **Billing** | Token usage or [provisioned throughput units (PTU)](../openai/concepts/provisioned-throughput.md) | Compute core hours (per-minute, per-instance) |
| **Data processing** | Regional, data zone, or global | Regional only |
| **Content filtering** | Built-in and customizable | Via Azure AI Content Safety APIs |

## Standard deployment in Foundry resources

Standard deployment in Foundry resources is **the preferred deployment option** in Foundry. It supports the widest range of capabilities and deployment types.

### Which models use standard deployment?

All Foundry Models, including [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md) use standard deployment. Foundry Models sold by Azure include all Azure OpenAI models and selected models from top providers that are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. Select Models from partners and community that use standard deployment include Anthropic models, and specific models from partners like Mistral, Cohere, and Meta.

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

Managed compute is a managed GPU platform-as-a-service (PaaS) that hosts open-source and custom-weight models on dedicated GPU capacity. You access managed compute deployments through the same Foundry project endpoint as other deployment types, with no virtual machines, clusters, or serving runtimes to own. Foundry sizes the deployment, provisions the accelerators, and keeps the runtime patched.

> [!IMPORTANT]
> Managed compute is used for all OSS models — including open-source, partner, industry, and custom models. Managed compute deployments are served on the **unified Foundry project endpoint**, using the same authentication, networking, and SDK surface.

### Which models use managed compute?

Examples of model collections that require managed compute include:

- Hugging Face
- Some Meta models
- Some Mistral models
- NVIDIA inference microservices (NIMs)
- Industry models (Saifr, Rockwell, Bayer, Cerence, Sight Machine, Page AI, SDAIA)
- Databricks
- Custom models

Microsoft Foundry's catalog includes 10,000+ open-source and partner models, with approximately 50 new models published each month.

### Capabilities

Managed compute supports:

- **Unified Foundry endpoint and authentication** — Use the same project endpoint, API keys, Microsoft Entra ID, and private networking as pay-per-token and provisioned throughput deployments. Inference routes use `<endpoint>/managed-deployments/<deployment-name>/`. Chat-completions-compatible runtimes also work on the standard `/openai/v1/` route with the OpenAI SDK.
- **Model-instance sizing** — Deployments are sized in model-centric terms. Foundry picks GPUs per instance based on model size, architecture, context length, and whether the workload is optimized for latency or throughput. You don't pick virtual machine SKUs.
- **Optimized inference runtimes** — Microsoft-curated vLLM, SGLang, and NVIDIA NIM containers with continuous batching, speculative decoding, tensor parallelism, and LoRA hot-swap.
- **Accelerator families** — A100 (80 GB), H100 (80 GB), H200 (141 GB), and MI300X.
- **Auto-scaling and scale-to-zero** — Auto-scale from live traffic or scale manually. Configure an idle timeout so the deployment scales to zero when no traffic arrives; billing stops immediately.
- **Microsoft-managed runtimes** — Microsoft owns serving runtimes, base container images, and security patches. Updates are applied to live deployments automatically.
- **Observability metrics** — Each deployment emits API call count by status code and response-time percentiles. Chat-completion models also emit input and output token counts, time-to-first-token (TTFT) percentiles, and total response-time percentiles, grouped by time.
- **Content filtering** — Not in scope for public preview; planned for revisit before general availability.


### Billing and quota

Managed compute billing is hourly per accelerator SKU, with throughput per GPU as the underlying billing unit. Auto-scale and scale-to-zero align cost with actual traffic — billing stops immediately when instances scale in.

Quota is granted per accelerator SKU per region through the **Foundry quota process** and is **separate from Azure VM quota**. Azure virtual machines are an infrastructure-as-a-service (IaaS) offering with regional SKUs; managed compute is a PaaS offering that leads with Global and Data Zone processing. Existing Azure VM quota can't be applied to a managed compute deployment.

Managed compute is global at launch, with Data Zone and additional regions planned. Per-hour rates, 1-year reserved capacity, and commitment discounts are **(under consideration)**. Final rates will be published at general availability. For estimates, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).


### Get started

- [Deploy and infer with a managed compute deployment (classic)](../../foundry-classic/how-to/deploy-models-managed.md)
- [Deploy Foundry Models to managed compute with pay-as-you-go billing (classic)](../../foundry-classic/how-to/deploy-models-managed-pay-go.md)

## Deployment option comparison

Use [Standard deployment in Foundry resources](#standard-deployment-in-foundry-resources) whenever possible. The following table compares capabilities across the two deployment options:

| Capability | Standard deployment in Foundry resources | Managed compute |
|---|---|---|
| Which models can be deployed? | All Foundry Models, including [Foundry Models sold directly by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md) | Open-source and partner models from the catalog, NVIDIA NIM, and industry models |
| Deployment resource | Foundry resource | Foundry project |
| Requires AI Hub | No | No |
| Data processing options | Regional, data zone, global | Global; Data Zone planned |
| Private networking | Yes | Yes |
| Content filtering | Built-in and customizable | Not in public preview; planned before GA |
| Keyless authentication | Yes (Microsoft Entra ID) | Yes (Microsoft Entra ID) and key-based |
| Billing | Token usage or [provisioned throughput units](../openai/concepts/provisioned-throughput.md) | Hourly per accelerator SKU |

> [!TIP]
> For detailed pricing information, see [Plan and manage costs for Foundry Tools](manage-costs.md).

## Related content

- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md)
- [Deploy models using Azure CLI and Bicep](../foundry-models/how-to/create-model-deployments.md)
- [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Foundry Models from partners and community](../foundry-models/concepts/models-from-partners.md)
- [Microsoft Foundry Models overview](foundry-models-overview.md)
- [Plan and manage costs for Foundry Tools](manage-costs.md)
