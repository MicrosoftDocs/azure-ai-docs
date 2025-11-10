---
title: Foundry Models from partners and community
titleSuffix: Azure AI Foundry
description: Learn about Azure AI Foundry Models from partners and community, their capabilities, deployment types, and regional availability for AI applications.
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 09/05/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: conceptual
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
zone_pivot_groups: azure-ai-model-categories

#CustomerIntent: As a developer or AI practitioner, I want to explore and understand the available Azure AI Foundry Models from partners and community, including their specific capabilities, deployment types, and regional availability, so that I can select the most appropriate model for my AI application requirements.
---

# Foundry Models from partners and community

This article lists a selection of Azure AI Foundry Models from partners and community along with their capabilities, [deployment types, and regions of availability](deployment-types.md), excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). 
Most Foundry Models come from partners and community. Trusted third-party organizations, partners, research labs, and community contributors provide these models. 

[!INCLUDE [models-list-introduction](../includes/models-list-introduction.md)]

To learn more about attributes of Foundry Models from partners and community, see [Explore Azure AI Foundry Models](../../concepts/foundry-models-overview.md#models-from-partners-and-community).

> [!NOTE]
> For a list of models sold directly by Azure, see [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md).
>
> For a list of Azure OpenAI models that are supported by the Azure AI Foundry Agent Service, see [Models supported by Azure AI Foundry Agent Service](../../agents/concepts/model-region-support.md).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,182 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [embed-v-4-0](https://ai.azure.com/explore/models/embed-v-4-0/version/4/registry/azureml-cohere/?cid=learnDocs) | embeddings | - **Input:** text (512 tokens) and images (2MM pixels) <br /> - **Output:** Vector (256, 512, 1024, 1536 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | Foundry, Hub-based |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere/?cid=learnDocs) | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` | Foundry, Hub-based |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere/?cid=learnDocs) | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | Foundry, Hub-based |

### Cohere rerank

| Model | Type | Capabilities | API Reference | Project type |
| ----- | ---- | ------------ | ------------- | ------------ |
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere/?cid=learnDocs) | rerank <br> text classification | - **Input:** text <br /> - **Output:** text  <br /> - **Languages:** English, Chinese, French, German, Indonesian, Italian, Portuguese, Russian, Spanish, Arabic, Dutch, Hindi, Japanese, Vietnamese | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) | Hub-based |

For more details on pricing for Cohere rerank models, see [Pricing for Cohere rerank models](../../concepts/models-inference-examples.md#pricing-for-cohere-rerank-models).

See [the Cohere model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Cohere/?cid=learnDocs).

## Core42

Core42 includes autoregressive bilingual LLMs for Arabic and English with state-of-the-art capabilities in Arabic.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42/?cid=learnDocs) | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** en and ar <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Core42/?cid=learnDocs).

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-4-Scout-17B-16E-Instruct](https://aka.ms/aifoundry/landing/llama-4-scout-17b-16e-instruct) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta/?cid=learnDocs). You can also find several Meta models available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:**  (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-reasoning](https://aka.ms/azureai/landing/Phi-4-reasoning) | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-mini-reasoning](https://aka.ms/azureai/landing/Phi-4-mini-reasoning) | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs). Microsoft models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Mistral AI

Mistral AI offers two categories of models: premium models such as Mistral Large 2411 and Ministral 3B, and open models such as Mistral Nemo.

| Model | Type | Capabilities | Project type |
| ----- | ---- | ------------ | ------------ |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-small-2503](https://ai.azure.com/explore/models/Mistral-small-2503/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-medium-2505](https://aka.ms/aistudio/landing/mistral-medium-2505?cid=learnDocs) | chat-completion |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | Foundry, Hub-based|
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-OCR-2503](https://aka.ms/aistudio/landing/mistral-ocr-2503?cid=learnDocs) | image to text |  - **Input:** image or PDF pages (1,000 pages, max 50MB PDF file) <br> - **Output:** text <br /> - **Tool calling:** No <br /> - **Response formats:** Text, JSON, Markdown | Hub-based|
| [mistralai-Mistral-7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v01/version/11/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text  <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Response formats:** Text | Hub-based |
| [mistralai-Mistral-7B-Instruct-v0-2](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v0-2/version/6/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mixtral-8x7B-Instruct-v01/version/10/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text  <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x22B-Instruct-v0-1](https://ai.azure.com/explore/models/mistralai-Mixtral-8x22B-Instruct-v0-1/version/5/registry/azureml/?cid=learnDocs) | chat-completion | - **Input:** text (64,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, it, de, es, en <br /> - **Response formats:** Text | Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI/?cid=learnDocs). Mistral models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).


## Nixtla

Nixtla's TimeGEN-1 is a generative pretrained forecasting and anomaly detection model for time series data. TimeGEN-1 produces accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.

| Model  | Type | Capabilities | Inference API | Project type |
| ------ | ---- | ------------ | ------------- | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla/?cid=learnDocs) | Forecasting  | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/nixtla/docs/reference/nixtla_client.html#nixtlaclient-forecast) | Hub-based |

For more details on pricing for Nixtla models, see [Nixtla](../../concepts/models-inference-examples.md#nixtla).


## NTT Data

**tsuzumi** is an autoregressive language-optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata/?cid=learnDocs) | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=NTT+Data/?cid=learnDocs).

## Stability AI

The Stability AI collection of image generation models includes Stable Image Core, Stable Image Ultra, and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large accepts both image and text input. 

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text and image (1,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) | Foundry, Hub-based |
| [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Foundry, Hub-based |
| [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai/?cid=learnDocs) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Stability+AI/?cid=learnDocs).


[!INCLUDE [models-open-and-custom](../includes/models-open-custom.md)]


## Related content

- [Deployment overview for Azure AI Foundry Models](../../concepts/deployments-overview.md)
- [Add and configure models to Azure AI Foundry Models](../how-to/create-model-deployments.md)
- [Deployment types in Azure AI Foundry Models](deployment-types.md)
- [Serverless API inference examples for Foundry Models](../../concepts/models-inference-examples.md)
