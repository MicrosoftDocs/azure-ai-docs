---
title: "Deployment overview for Microsoft Foundry Models"
description: "Learn about deployment options for Microsoft Foundry Models: serverless API deployments for Foundry Models and managed compute for open-source and custom models."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 08/06/2026
ms.author: aashcraft
author: alvinashcraft
manager: mcleans
ai-usage: ai-assisted
#CustomerIntent: As a developer or AI practitioner, I want to understand the deployment options available for Microsoft Foundry Models so that I can choose the right deployment method for my models and use case.
---

# Deployment overview for Microsoft Foundry Models

Microsoft Foundry Models is the hub for discovering and deploying a wide range of AI models for generative AI applications. To make a model available for inference requests, you deploy it. Foundry offers two deployment options depending on the model type and your infrastructure needs.

[!INCLUDE [try-instant-models](../includes/try-instant-models.md)]

## Deployment options

Foundry provides two deployment options:

- **Serverless API** — For Foundry Models, including [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md). This option is the preferred and most capable deployment path. It includes the standard, provisioned throughput, batch, and developer deployment types.
- **Managed compute (preview)** — For open-source, partner, and custom models that run on dedicated GPU capacity that Foundry manages for you.

Foundry selects the appropriate deployment option based on the model you choose.

If you only need to try a supported model, you can skip deployment entirely and use [instant access (preview)](instant-models.md), which calls models by name without creating a Serverless API or managed compute deployment.

:::image type="content" source="media/deployments-overview/deployment-options-hierarchy.png" alt-text="Diagram that shows choosing between instant access, Serverless API deployment types by launch order, and managed compute." lightbox="media/deployments-overview/deployment-options-hierarchy.png":::

For a full capability comparison, see [Deployment option comparison](#deployment-option-comparison).

## Serverless API

Serverless API is **the preferred deployment option** in Foundry. It supports the widest range of capabilities and deployment types.

### Which models use serverless API deployments?

All Foundry Models, including [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md), use serverless API deployments. Foundry Models sold by Azure include all Azure OpenAI models and selected models from top providers that are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. Models from partners and community that use serverless API deployments include Anthropic models and specific models from partners like Mistral, Cohere, and Meta.

### Serverless API capabilities

Serverless API deployments support:

- **Multiple deployment types (or deployment SKUs)** — Global Standard, Data Zone Standard, Standard (single region), provisioned, batch, and more. Each type controls where data is processed and how you pay. For details, see [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md).
- **Data processing flexibility** — Choose regional, data zone (US, EU, or APAC), or global processing based on your compliance requirements.
- **Content filtering** — Built-in Azure AI Content Safety filters with customizable configurations.
- **Keyless authentication** — Microsoft Entra ID (recommended) and key-based authentication.
- **Private networking** — Virtual network integration for secure access.
- **Provisioned throughput** — Reserve capacity with provisioned throughput units (PTUs) for predictable, low-latency performance. For details, see [Provisioned throughput](../openai/concepts/provisioned-throughput.md).

### Resource requirements

Serverless API deployments are available in:

- **Foundry resources** — The primary resource type for new Foundry projects. No AI Hub required.
- **Azure OpenAI resources** — If you use Azure OpenAI resources, the model catalog shows only Azure OpenAI models for deployment. Upgrade to a Foundry resource for access to the full set of Foundry Models.

To get started with serverless API deployment, see [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md) or [Deploy models using Azure CLI and Bicep](../foundry-models/how-to/create-model-deployments.md).

## Managed compute deployment (preview)

> [!NOTE]
> Managed compute in Foundry is currently in public preview.
> This preview is provided without a service-level agreement, and we don't recommend it for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Managed compute in Foundry (preview) is a managed GPU platform-as-a-service (PaaS) that hosts open-source and custom-weight models on dedicated GPU capacity. You access managed compute deployments through the same Foundry project endpoint as other deployment types, with no virtual machines, clusters, or serving runtimes to own. Foundry sizes the deployment, provisions the accelerators, and keeps the runtime patched.

> [!IMPORTANT]
> Managed compute supports open-source, partner, industry, and custom models. Managed compute deployments are served on the **unified Foundry project endpoint**, using the same authentication, networking, and SDK surface.

### Which models use managed compute?

You can deploy models from the Hugging Face Collection by using managed compute. Examples include:

- Qwen models
- NVIDIA Nemotron models
- Selected Meta models
- Selected Mistral models

Microsoft Foundry's catalog includes a large and growing selection of open-source and partner models. For the current catalog, see the [model catalog](https://ai.azure.com/explore/models).

### Managed compute capabilities

Managed compute (Preview) supports:

- **Unified Foundry endpoint and authentication** — Use the same project endpoint, API keys, Microsoft Entra ID, and private networking as pay-per-token and provisioned throughput deployments. Inference routes use `<endpoint>/managed-deployments/<deployment-name>/`. Chat-completions-compatible runtimes also work on the standard `/openai/v1/` route with the OpenAI SDK.
- **Model-instance sizing** — Deployments are sized in model-centric terms. You don't need to pick virtual machine SKUs, because Foundry chooses GPUs per instance based on model size, architecture, context length, and whether the workload is optimized for latency or throughput.
- **Optimized inference runtimes** — Microsoft-curated vLLM, SGLang, and NVIDIA NIM containers with continuous batching and tensor parallelism.
- **Accelerator families** — A100 (80 GB), H100 (80 GB), and MI300X (192 GB).
- **Auto-scaling and scale-to-zero** — Auto-scale from live traffic or scale manually. Configure an idle timeout so the deployment scales to zero when no traffic arrives, making billing stop immediately.
- **Microsoft-managed runtimes** — Microsoft owns serving runtimes, base container images, and security patches. Updates are applied to live deployments automatically.
- **Observability metrics** — Each deployment emits API call count by status code and response-time percentiles. Chat-completion models also emit input and output token counts, time-to-first-token (TTFT) percentiles, and total response-time percentiles, grouped by time.

### Billing and quota

Managed compute billing is hourly per accelerator SKU, with throughput per GPU as the underlying billing unit. Auto-scale and scale-to-zero align cost with actual traffic so that billing stops immediately when instances scale down.

Quota is granted per accelerator SKU per region through the **Foundry quota process** and is **separate from Azure VM quota**. Azure virtual machines are an infrastructure-as-a-service (IaaS) offering with regional SKUs; managed compute is a PaaS offering that leads with Global and Data Zone processing. Existing Azure VM quota can't be applied to a managed compute deployment.

Managed compute is currently available for global deployment. For rate estimates, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).


### Get started

To get started with managed compute deployment, see [Deploy open-source models with managed compute](../how-to/deploy-models-managed.md).

## Deployment option comparison

Use [Serverless API](#serverless-api) whenever possible. The following table compares capabilities across the two deployment options:

> [!NOTE]
> Instant access (preview) isn't a deployment option in this comparison. It calls supported models by name without creating a Serverless API or managed compute deployment.

| Capability | Serverless API | Managed compute |
|---|---|---|
| Which models can be deployed? | All Foundry Models, including [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md) and [select Models from partners and community](../foundry-models/concepts/models-from-partners.md) | Open-source and partner models from the model catalog, NVIDIA NIM, and industry models |
| Deployment resource | Foundry resource | Foundry project |
| Requires AI Hub | No | No |
| Data processing options | Regional, data zone, global | Global |
| Private networking | Yes | Yes |
| Content filtering | Built-in and customizable | Not available in public preview |
| Keyless authentication | Yes (Microsoft Entra ID and key-based) | Yes (Microsoft Entra ID and key-based) |
| Billing | Token usage or [provisioned throughput units](../openai/concepts/provisioned-throughput.md) | Hourly per accelerator SKU |


> [!TIP]
> For detailed pricing information, see [Plan and manage costs for Microsoft Foundry](manage-costs.md).

## Related content

- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../foundry-models/how-to/deploy-foundry-models.md)
- [Deploy models using Azure CLI and Bicep](../foundry-models/how-to/create-model-deployments.md)
- [Foundry Models sold by Azure](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Foundry Models from partners and community](../foundry-models/concepts/models-from-partners.md)
- [Microsoft Foundry Models overview](foundry-models-overview.md)
- [Managed compute in Microsoft Foundry](managed-compute-overview.md)
