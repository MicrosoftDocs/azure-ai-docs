---
title: "Foundry Models from partners and community (classic)"
description: "Learn about Microsoft Foundry Models from partners and community, including their capabilities, supported input and output types, and language support for AI applications. (classic)"
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 04/06/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: partner-tools
ms.custom:
  - classic-and-new
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
  - pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: azure-ai-model-categories

#CustomerIntent: As a developer or AI practitioner, I want to explore and understand the available Microsoft Foundry Models from partners and community, including their specific capabilities, supported input and output types, and language support, so that I can select the most appropriate model for my AI application requirements.
ROBOTS: NOINDEX, NOFOLLOW
---

# Foundry Models from partners and community (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/concepts/models-from-partners.md)

This article lists capabilities for a selection of Microsoft Foundry Models from partners and community.
Most Foundry Model providers are trusted third-party organizations, partners, research labs, and community contributors. 
The selection of models that you see in Foundry depends on the [kind of project](../../what-is-foundry.md#types-of-projects) you use.
To learn more about attributes of Foundry Models from partners and community, see [Explore Foundry Models](../../concepts/foundry-models-overview.md#models-from-partners-and-community).

> [!NOTE]
> For a list of models sold directly by Azure, see [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md).
>
> For a list of Azure OpenAI models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../../foundry/agents/concepts/limits-quotas-regions.md).

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

    > [!IMPORTANT]
    > The following Azure subscriptions can't be used to purchase software as a service (SaaS) offers in Marketplace: Student, Visual Studio Enterprise, or Free credit. For more information on purchasing SaaS offers, see [The SaaS purchase experience](/marketplace/purchase-saas-offer-in-azure-portal#the-saas-purchase-experience).

- A [Microsoft Foundry project](../../how-to/create-projects.md).

[!INCLUDE [marketplace-rbac](../../../foundry/foundry-models/includes/configure-marketplace/rbac.md)]

## Country/region availability

Users can access models from partners and community with pay-as-you-go billing only if their Azure subscription belongs to a billing account in a country/region or region where the model offer is available. Availability varies per model provider and model SKU. For more information, see [Region availability for models](../../how-to/deploy-models-serverless-availability.md).

## Anthropic

Anthropic's flagship product is Claude, a frontier AI model trusted by leading enterprises and millions of users worldwide for complex tasks including coding, agents, financial analysis, research, and office tasks. Claude delivers exceptional performance while maintaining high safety standards.

To work with Claude models in Foundry, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md)

> [!NOTE]
> Claude Mythos Preview is only available as a *gated research preview*. Access to the model is prioritized by Anthropic for defensive cybersecurity use cases. See the [Claude Mythos Preview system card](https://www.anthropic.com/claude-mythos-preview-system-card) for responsible use guidance.

#### Subscription type and region support

[!INCLUDE [claude-usage-restriction](../../../foundry/foundry-models/includes/claude-usage-restriction.md)]

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| `claude-mythos-preview` <br><br> **(Gated research preview)** | Messages | - **Input:** text, image, and code <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000 <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br /> - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:** Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) <br /> - **Key parameters:** `top_p` must be at least 0.99. Requests with `top_p` below this threshold are rejected with a 400 error. When `top_p` is omitted, the default (0.99) is used. | Foundry, Hub-based |
| [claude-opus-4-6](https://aka.ms/claude-opus-4-6) <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |
| [claude-opus-4-5](https://aka.ms/claude-opus-4-5) <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |
| [claude-opus-4-1](https://aka.ms/claude-opus-4-1) <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (32,000 max tokens) <br /> - **Context window:** 200,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |
| [claude-sonnet-4-6](https://aka.ms/claude-sonnet-4-6) <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |
| [claude-sonnet-4-5](https://aka.ms/claude-sonnet-4-5) <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |
| [claude-haiku-4-5](https://aka.ms/claude-haiku-4-5) <br><br> **(Preview)** | Messages | - **Input:**  text and image  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)| Foundry, Hub-based |

See [Anthropic models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=anthropic/?cid=learnDocs).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

To deploy Cohere models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere/?cid=learnDocs) | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` | Foundry, Hub-based |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere/?cid=learnDocs) | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | Foundry, Hub-based |

### Cohere rerank

| Model | Type | Capabilities | API Reference | Project type |
| ----- | ---- | ------------ | ------------- | ------------ |
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere/?cid=learnDocs) | rerank <br> text classification | - **Input:** text <br /> - **Output:** text  <br /> - **Languages:** English, Chinese, French, German, Indonesian, Italian, Portuguese, Russian, Spanish, Arabic, Dutch, Hindi, Japanese, Vietnamese | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) | Hub-based |

For more details on pricing for Cohere rerank models, see [Pricing for Cohere rerank models](../../concepts/models-inference-examples.md#pricing-for-cohere-rerank-models).

See [Cohere models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Cohere/?cid=learnDocs).

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

To deploy Meta Llama models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-4-Scout-17B-16E-Instruct](https://aka.ms/aifoundry/landing/llama-4-scout-17b-16e-instruct) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [Meta models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta/?cid=learnDocs). You can also find several Meta models available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more.

To deploy Microsoft models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-reasoning](https://ai.azure.com/explore/models/Phi-4-reasoning/version/1/registry/azureml/?cid=learnDocs) | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-mini-reasoning](https://ai.azure.com/explore/models/Phi-4-mini-reasoning/version/1/registry/azureml/?cid=learnDocs) | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [Microsoft models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs). Microsoft models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Mistral AI

Mistral AI offers models for code generation, general-purpose chat, and multimodal tasks, including Codestral, Ministral, Mistral Small, and Mistral Medium.

To deploy Mistral AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities | Project type |
| ----- | ---- | ------------ | ------------ |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-small-2503](https://ai.azure.com/explore/models/Mistral-small-2503/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-medium-2505](https://aka.ms/aistudio/landing/mistral-medium-2505?cid=learnDocs) | chat-completion |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | Foundry, Hub-based|
| [mistralai-Mistral-7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v01/version/11/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text  <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Response formats:** Text | Hub-based |
| [mistralai-Mistral-7B-Instruct-v0-2](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v0-2/version/6/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mixtral-8x7B-Instruct-v01/version/10/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text  <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x22B-Instruct-v0-1](https://ai.azure.com/explore/models/mistralai-Mixtral-8x22B-Instruct-v0-1/version/5/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (64,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, it, de, es, en <br /> - **Response formats:** Text | Hub-based |

See [Mistral AI models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI/?cid=learnDocs). Mistral models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Nixtla

Nixtla's TimeGEN-1 is a generative pretrained forecasting and anomaly detection model for time series data. TimeGEN-1 produces accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

To deploy TimeGEN-1 in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.

| Model  | Type | Capabilities | Inference API | Project type |
| ------ | ---- | ------------ | ------------- | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla/?cid=learnDocs) | Forecasting  | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/neuralforecast/docs/capabilities/overview.html) | Hub-based |

For more details on pricing for Nixtla models, see [Nixtla](../../concepts/models-inference-examples.md#nixtla).

See [Nixtla models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=nixtla/?cid=learnDocs).

## NTT Data

**tsuzumi** is an autoregressive language-optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

To deploy tsuzumi-7b in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata/?cid=learnDocs) | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Hub-based |

See [NTT Data models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=NTT+Data/?cid=learnDocs).

## Stability AI

The Stability AI collection of image generation models includes Stable Image Core, Stable Image Ultra, and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large accepts both image and text input. 

To deploy Stability AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text and image (1,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) | Foundry, Hub-based |
| [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Foundry, Hub-based |
| [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Foundry, Hub-based |

See [Stability AI models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Stability+AI/?cid=learnDocs).

[!INCLUDE [models-open-and-custom](../includes/models-open-custom.md)]

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in Foundry Models:

| Error | Description |
|-------|-------------|
| Offer not available in your country/region | The model provider didn't make the specific model SKU available in the country/region where you registered your subscription. Each model provider decides which countries/regions are available, and availability can vary by model SKU. Deploy the model to a subscription with billing in a supported country/region. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Marketplace purchase eligibility check failed | The model provider didn't make the specific model SKU available in your country/region, or the model isn't available in the region where you deployed the Foundry resource. See [Region availability for models](../../how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment | Azure Marketplace rejected the request to create a model subscription. This rejection can happen for multiple reasons, including subscribing to the model offering too often or from multiple subscriptions at the same time. Contact [support](https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409) and include your subscription ID. |
| CSP subscription not supported | Cloud Solution Provider (CSP) subscriptions can't purchase third-party model offerings. Consider using models offered as a first-party consumption service. |

## Related content

- [Deployment overview for Foundry Models](../../concepts/deployments-overview.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Deployment types in Foundry Models](deployment-types.md)
- [Region availability for Foundry Models](../../how-to/deploy-models-serverless-availability.md)
- [Explore Foundry Models](../../concepts/foundry-models-overview.md)

- [Serverless API inference examples for Foundry Models](../../concepts/models-inference-examples.md)
