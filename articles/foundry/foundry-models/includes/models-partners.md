---
title: Models from partners
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 04/17/2026
ms.service: microsoft-foundry
ms.topic: include
ms.custom: pilot-ai-workflow-jan-2026, classic-and-new
---

Microsoft Foundry Models in the model catalog comprise two main categories, namely *Foundry Models sold directly by Azure* and *Foundry Models from partners and community*.
This article lists a selection of Foundry Models from partners and community, along with their capabilities, deployment types, and regions of availability, excluding deprecated and retired models.
Most Foundry Model providers are trusted third-party organizations, partners, research labs, and community contributors. 

> [!NOTE]
> Note that Models from partners and community that are not sold directly by Azure are Non-Microsoft Products under the Product Terms.

For a list of Foundry Models sold directly by Azure, see [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md), and for a list of Foundry Models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/limits-quotas-regions.md).

Foundry Models support several [deployment types](../../foundry-models/concepts/deployment-types.md) to a Foundry resource. Some models in the model catalog require a hub-based project hosted by a Foundry hub for deployment. Selecting those models in the catalog opens them up in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

    > [!IMPORTANT]
    > The following Azure subscriptions can't be used to purchase software as a service (SaaS) offers in Marketplace: Student, Visual Studio Enterprise, or Free credit. For more information on purchasing SaaS offers, see [The SaaS purchase experience](/marketplace/purchase-saas-offer-in-azure-portal#the-saas-purchase-experience).

- A [Microsoft Foundry project](../../how-to/create-projects.md).

[!INCLUDE [marketplace-rbac](../includes/configure-marketplace/rbac.md)]

## Country/region availability

You can access models from partners and community with pay-as-you-go billing only if your Azure subscription belongs to a billing account in a country/region where the model offer is available. Availability varies per model provider and model SKU. For more information, see [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md).


## Anthropic

Anthropic's flagship product is Claude, a frontier AI model trusted by leading enterprises and millions of users worldwide for complex tasks including coding, agents, financial analysis, research, and office tasks. Claude delivers exceptional performance while maintaining high safety standards.

To work with Claude models in Foundry, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md). 

> [!NOTE]
> [!INCLUDE [claude-mythos-preview-restriction](../includes/claude-mythos-preview-restriction.md)]

#### Subscription type and region support

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]


| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `claude-mythos-preview` <br> **Gated research preview** | Messages | - **Input:** text, image, and code <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000 <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br /> - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:** Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:** `top_p` must be at least 0.99. Requests with `top_p` below this threshold are rejected with a 400 error. When `top_p` is omitted, the default (0.99) is used. |
| `claude-opus-4-7` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:**<br> `top_k`, `temperature`, and `thinking={"type":"enabled"}` are **not supported**.<br> `top_p` must be 0.99. When omitted, the default (0.99) is used. |
| `claude-opus-4-6` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-opus-4-5` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-opus-4-1` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (32,000 max tokens) <br /> - **Context window:** 200,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |
| `claude-sonnet-4-6` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-sonnet-4-5` <br> **Preview** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |
| `claude-haiku-4-5` <br> **Preview** | Messages | - **Input:**  text and image  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |


## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

To deploy Cohere models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Cohere-command-r-plus-08-2024` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Cohere-command-r-08-2024` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Cohere-embed-v3-english` | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` |
| `Cohere-embed-v3-multilingual` | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` |

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

To deploy Meta Llama models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Llama-3.2-11B-Vision-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Llama-3.2-90B-Vision-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Meta-Llama-3.1-405B-Instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Meta-Llama-3.1-8B-Instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Llama-4-Scout-17B-16E-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |



## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more.

To deploy Microsoft models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Phi-4-mini-instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-multimodal-instruct` | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4` | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-reasoning` | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-mini-reasoning` | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |



## Mistral AI

Mistral AI offers models for code generation, general-purpose chat, and multimodal tasks, including Codestral, Ministral, Mistral Small, and Mistral Medium.

To deploy Mistral AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities |
| ----- | ---- | ------------ |
| `Codestral-2501` | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Ministral-3B` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Mistral-small-2503` | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Mistral-medium-2505` | chat-completion |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON |
| `mistralai-Mistral-7B-Instruct-v01`<sup>1</sup> | chat-completion | - **Input:** text  <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Response formats:** Text |
| `mistralai-Mistral-7B-Instruct-v0-2`<sup>1</sup> | chat-completion | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text |
| `mistralai-Mixtral-8x7B-Instruct-v01`<sup>1</sup> | chat-completion | - **Input:** text  <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text |
| `mistralai-Mixtral-8x22B-Instruct-v0-1`<sup>1</sup> | chat-completion | - **Input:** text (64,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, it, de, es, en <br /> - **Response formats:** Text |

<sup>1</sup> These models require a hub-based project for deployment. Selecting them in the model catalog opens them up in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).


## Nixtla

Nixtla's TimeGEN-1 is a generative pretrained forecasting and anomaly detection model for time series data. TimeGEN-1 produces accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

To deploy TimeGEN-1 in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.

| Model  | Type | Capabilities | Inference API |
| ------ | ---- | ------------ | ------------- |
| `TimeGEN-1`<sup>1</sup> | Forecasting  | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/overview.html) |

<sup>1</sup> This model requires a hub-based project for deployment. Selecting the model in the model catalog opens it in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

For more details on pricing for Nixtla models, see [Nixtla](../../../foundry-classic/concepts/models-inference-examples.md#nixtla).

See [Nixtla models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=nixtla/?cid=learnDocs).

## NTT Data

**tsuzumi** is an autoregressive language-optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

To deploy tsuzumi-7b in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `tsuzumi-7b`<sup>1</sup> | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |

<sup>1</sup> This model requires a hub-based project for deployment. Selecting the model in the model catalog opens it in the [Foundry (classic) portal experience](../../../foundry-classic/what-is-foundry.md).

See [NTT Data models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=NTT+Data/?cid=learnDocs).

## Stability AI

The Stability AI collection of image generation models includes Stable Image Core, Stable Image Ultra, and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large accepts both image and text input. 

To deploy Stability AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Stable Diffusion 3.5 Large` | Image generation | - **Input:** text and image (1,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) |
| `Stable Image Core` | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |
| `Stable Image Ultra` | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in Foundry Models:

| Error | Description |
|-------|-------------|
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

