---
title: Models from partners
author: msakande
ms.author: mopeakande
manager: mcleans
ms.date: 07/24/2026
ms.service: microsoft-foundry
ms.topic: include
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026, classic-and-new
---

Microsoft Foundry Models in the model catalog comprise two main categories, namely *Foundry Models sold by Azure* and *Foundry Models from partners and community*.
This article lists a selection of Foundry Models from partners and community, along with their capabilities, deployment types, and regions of availability, **excluding deprecated and retired models**.
Most Foundry Model providers are trusted third-party organizations, partners, research labs, and community contributors. 

> [!IMPORTANT]
> Models from partners and community that are not sold by Azure are Non-Microsoft Products under the Product Terms.

For a list of Foundry Models sold by Azure, see [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md), and for a list of Foundry Models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/limits-quotas-regions.md).

Foundry Models support several [deployment types](../../foundry-models/concepts/deployment-types.md) to a Foundry resource. Some models in the model catalog require a hub-based project hosted by a Foundry hub for deployment. Selecting those models in the catalog opens them up in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

    > [!IMPORTANT]
    > The following Azure subscriptions can't be used to purchase software as a service (SaaS) offers in Marketplace: Student, Visual Studio Enterprise, or Free credit. For more information on purchasing SaaS offers, see [The SaaS purchase experience](/marketplace/purchase-saas-offer-in-azure-portal#the-saas-purchase-experience).

- A [Microsoft Foundry project](../../how-to/create-projects.md).

[!INCLUDE [marketplace-rbac](../includes/configure-marketplace/rbac.md)]

## Country/region availability

You can access Models from partners and community with pay-as-you-go billing only if your Azure subscription belongs to a billing account in a country or region where the model provider made the offer available (see the "Offer availability region" column of the tables in each model provider's section). Availability varies per model provider and model SKU. If the offer is available in the relevant country or region, you must have a project or hub in the [Azure region](#region-availability-by-deployment-type) where the model is available for deployment or fine-tuning, as applicable.

## Anthropic

Anthropic's flagship product is Claude, a frontier AI model trusted by leading enterprises and millions of users worldwide for complex tasks including coding, agents, financial analysis, research, and office tasks. Claude delivers exceptional performance while maintaining high safety standards.

> [!NOTE]
> [!INCLUDE [claude-versions-description](claude-versions-description.md)] 

#### Subscription type and region support

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

| Model | Type | Capabilities | Offer availability region |
| ------ | ---- | ------------ | ------------------------- |
| `claude-mythos-5`<sup>1</sup> | Messages | - **Input:** text, image, and code <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000 <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br /> - **Tool calling:** Yes (file search, code execution, and more) <br /> - **Response formats:** Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_p` must be at least 0.99. Requests with `top_p` below this threshold are rejected with a 400 error. When `top_p` is omitted, the default (0.99) is used. <br> `top_k`, `temperature`, `thinking={"type":"enabled"}`, `thinking={"type":"disabled"}`, and `output_format` are **not supported**.<br> Minimum cacheable prompt: 512 tokens. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-fable-5` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search, code execution, and more) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_p` must be at least 0.99. Requests with `top_p` below this threshold are rejected with a 400 error. When `top_p` is omitted, the default (0.99) is used. <br> `top_k`, `temperature`, `thinking={"type":"enabled"}`, `thinking={"type":"disabled"}`, and `output_format` are **not supported**. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-mythos-preview`<sup>1</sup> | Messages | - **Input:** text, image, and code <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000 <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br /> - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:** Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_p` must be at least 0.99. Requests with `top_p` below this threshold are rejected with a 400 error. When `top_p` is omitted, the default (0.99) is used. <br> `top_k`and `temperature` are **not supported**.<br> Minimum cacheable prompt: 2048 tokens. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-opus-5`<sup>2</sup> |  Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_k`, `temperature`, and `thinking={"type":"enabled"}` are **not supported**.<br> When `thinking={"type":"disabled"}`, `effort` is capped at `high`. <br> `top_p` must be 0.99; when omitted, the default (0.99) is used. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) <br> US (Hosted on Azure for Data Zone Standard) |
| `claude-opus-4-8` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_k`, `temperature`, and `thinking={"type":"enabled"}` are **not supported**.<br> `top_p` must be 0.99; when omitted, the default (0.99) is used. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) <br> US (Hosted on Azure for Data Zone Standard) |
| `claude-opus-4-7` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_k`, `temperature`, and `thinking={"type":"enabled"}` are **not supported**.<br> `top_p` must be 0.99. When omitted, the default (0.99) is used. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-opus-4-6` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-opus-4-5` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-opus-4-1` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (32,000 max tokens) <br /> - **Context window:** 200,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-sonnet-5` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_k`, `temperature`, and `thinking={"type":"enabled"}` are **not supported**.<br>`output_format` supported only for `thinking={"type":"adaptive"}`.<br> `top_p` must be 0.99. When omitted, the default (0.99) is used. | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) <br> US (Hosted on Azure for Data Zone Standard) |
| `claude-sonnet-4-6` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-sonnet-4-5` | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |
| `claude-haiku-4-5` | Messages | - **Input:**  text and image  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) (except Belarus and Russia) |

<sup>1</sup> [!INCLUDE [claude-mythos-preview-restriction](../includes/claude-mythos-preview-restriction.md)]


## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

To deploy Cohere models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Offer availability region |
| ------ | ---- | ------------ | ------------------------- |
| `Cohere-embed-v3-english` | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Japan <br> Qatar |
| `Cohere-embed-v3-multilingual` | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Japan <br> Qatar |

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

To deploy Meta Llama models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Offer availability region |
| ------ | ---- | ------------ | ------------------------- |
| `Llama-4-Scout-17B-16E-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) |

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more.

To deploy Microsoft models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Offer availability region |
| ------ | ---- | ------------ | ------------------------- |
| `Phi-4-mini-instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Not applicable |
| `Phi-4-multimodal-instruct` | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Not applicable |
| `Phi-4` | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Not applicable |
| `Phi-4-reasoning` | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Not applicable |
| `Phi-4-mini-reasoning` | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Not applicable |



## Mistral AI

Mistral AI offers models for code generation, general-purpose chat, and multimodal tasks, including Codestral, Ministral, Mistral Small, and Mistral Medium.

To deploy Mistral AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Offer availability region |
| ----- | ---- | ------------ | ------------------------- |
| `Codestral-2501` | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Brazil <br> Hong Kong SAR <br> Israel |
| `Ministral-3B` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Brazil <br> Hong Kong SAR <br> Israel |
| `Mistral-small-2503` | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Brazil <br> Hong Kong SAR <br> Israel |
| `Mistral-medium-2505` | chat-completion | - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) <br> Brazil <br> Hong Kong SAR <br> Israel |
| `mistralai-Mistral-7B-Instruct-v01`<sup>1</sup> | chat-completion | - **Input:** text  <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Response formats:** Text | - |
| `mistralai-Mistral-7B-Instruct-v0-2`<sup>1</sup> | chat-completion | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | - |
| `mistralai-Mixtral-8x7B-Instruct-v01`<sup>1</sup> | chat-completion | - **Input:** text  <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | - |
| `mistralai-Mixtral-8x22B-Instruct-v0-1`<sup>1</sup> | chat-completion | - **Input:** text (64,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, it, de, es, en <br /> - **Response formats:** Text | - |

<sup>1</sup> These models require a hub-based project for deployment. Selecting them in the model catalog opens them up in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

## NTT Data

**tsuzumi** is an autoregressive language-optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

To deploy tsuzumi-7b in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Offer availability region |
| ------ | ---- | ------------ | ------------------------- |
| `tsuzumi-7b`<sup>1</sup> | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | [Microsoft Managed Countries/Regions](/partner-center/marketplace/tax-details-marketplace#microsoft-managed-countriesregions) |

<sup>1</sup> This model requires a hub-based project for deployment. Selecting the model in the model catalog opens it in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

See [NTT Data models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=NTT+Data/?cid=learnDocs).

## Region availability by deployment type

Microsoft Foundry provides customers with choices on the hosting structure that fits their business and usage patterns. This section lists the regional availability for Foundry Models from partners and community, across all regions, for the Global Standard and Data Zone standard deployment types. To deploy your model in any of the Azure regions listed in the following tables, you must have a project or hub in that region.

For billing-account country/region eligibility, see [Country/region availability](#countryregion-availability). To learn about all available model deployment types, see [Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md).

[!INCLUDE [marketplace-deployments-standard](model-matrix/marketplace-deployments-standard.md)]

## Alternatives to region availability

If most of your infrastructure is in a particular region and you want to take advantage of models available only as serverless APIs, you can create a hub or project in a supported region and then consume the endpoint from another region.

To learn how to configure an existing serverless API deployment in a different hub or project than the one where it was deployed, see [Consume serverless APIs from a different hub or project](../../../foundry-classic/how-to/deploy-models-serverless-connect.md).


## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in Foundry Models:

| Error | Description |
| ----- | ----------- |
| Offer not available in your country/region | The model provider didn't make the specific model SKU available in the country/region where you registered your subscription. Each model provider decides which countries/regions are available, and availability can vary by model SKU. Deploy the model to a subscription with billing in a supported country/region. See [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md). |
| Marketplace purchase eligibility check failed | The model provider didn't make the specific model SKU available in your country/region, or the model isn't available in the region where you deployed the Foundry resource. See [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment | Azure Marketplace rejected the request to create a model subscription. This rejection can happen for multiple reasons, including subscribing to the model offering too often or from multiple subscriptions at the same time. Contact [support](https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409) and include your subscription ID. |
| CSP subscription not supported | Cloud Solution Provider (CSP) subscriptions can't purchase third-party model offerings. Consider using models offered as a first-party consumption service. |

## Related content

- [Deployment overview for Foundry Models](../../../foundry-classic/concepts/deployments-overview.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md)
- [Region availability for Foundry Models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md)
- [Explore Foundry Models](../../../foundry-classic/concepts/foundry-models-overview.md)
