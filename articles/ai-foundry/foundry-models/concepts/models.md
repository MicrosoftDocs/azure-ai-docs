---
title: Models available in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Explore the available Azure AI Foundry Models and their capabilities.
author: msakande
ms.author: mopeakande
reviewer: santiagxf
ms.reviewer: fasantia
ms.date: 08/08/2025
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
---

# Foundry Models and capabilities

Azure AI Foundry Models gives you access to flagship models in Azure AI Foundry to consume them as APIs with flexible deployment options.
This article lists a selection of model offerings and their capabilities, excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated). 

Depending on what [kind of project](../../what-is-azure-ai-foundry.md#work-in-an-azure-ai-foundry-project) you're using in Azure AI Foundry, you might see a different selection of these models. Specifically, if you're using a Foundry project, built on an Azure AI Foundry resource, you see the models that are available for standard deployment to a Foundry resource. Alternatively, if you're using a hub-based project, hosted by an Azure AI Foundry hub, you see models that are available for deployment to managed compute and serverless APIs. These model selections do overlap in many cases, since many models support the multiple [deployment options](../../concepts/deployments-overview.md). 

Foundry Models in the model catalog belong to two main categories:

* [Models sold directly by Azure](#models-sold-directly-by-azure)
* [Models from partners and community](#models-from-partners-and-community)


## Models sold directly by Azure

Models sold directly by Azure include all Azure OpenAI models and specific, selected models from top providers. To learn more about these models, see [Models Sold Directly by Azure](../../concepts/foundry-models-overview.md#models-sold-directly-by-azure).

### Azure OpenAI

Azure OpenAI in Azure AI Foundry Models offers a diverse set of models with different capabilities and price points. Learn more details at [Azure OpenAI Model availability](../../openai/concepts/models.md). These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

| Models | Description |
|--|--|
| [`GPT-5 series`](../../openai/concepts/models.md#gpt-5) | **NEW** `gpt-5`, `gpt-5-mini`, `gpt-5-nano`, `gpt-5-chat` |
| [gpt-oss](../../openai/concepts/models.md#gpt-oss) | Open-weight reasoning models |
| [codex-mini](../../openai/concepts/models.md#o-series-models) | Fine-tuned version of o4-mini. |  
| [GPT-4.1 series](../../openai/concepts/models.md#gpt-41-series) | `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano` |
| [model-router](../../openai/concepts/models.md#model-router) | A model that intelligently selects from a set of underlying chat models to respond to a given prompt. |
| [computer-use-preview](../../openai/concepts/models.md#computer-use-preview) | An experimental model trained for use with the Responses API computer use tool. |
| [o-series models](../../openai/concepts/models.md#o-series-models) |[Reasoning models](../../openai/how-to/reasoning.md) with advanced problem solving and increased focus and capability. |
| [GPT-4o, GPT-4o mini, and GPT-4 Turbo](../../openai/concepts/models.md#gpt-4o-and-gpt-4-turbo) | Capable Azure OpenAI models with multimodal versions, which can accept both text and images as input. |
| [GPT-4](../../openai/concepts/models.md#gpt-4) | A set of models that improve on GPT-3.5 and can understand and generate natural language and code. |
| [GPT-3.5](../../openai/concepts/models.md#gpt-35) | A set of models that improve on GPT-3 and can understand and generate natural language and code. |
| [Embeddings](../../openai/concepts/models.md#embeddings) | A set of models that can convert text into numerical vector form to facilitate text similarity. |
| [Image generation](../../openai/concepts/models.md#image-generation-models) | A series of models that can generate original images from natural language. |
| [Audio](../../openai/concepts/models.md#audio-models) | A series of models for speech to text, translation, and text to speech. GPT-4o audio models support either low latency *speech in, speech out* conversational interactions or audio generation. |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?selectedCollection=OpenAI).

### Black Forest Labs models sold directly by Azure

The Black Forest Labs collection of image generation models include FLUX.1 Kontext [pro] for in-context generation and editing and FLUX1.1 [pro] for text-to-image generation. 

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [FLUX.1-Kontext-pro](https://ai.azure.com/explore/models/FLUX.1-Kontext-pro/version/1/registry/azureml-blackforestlabs) | Image generation | - **Input:** text and image (5000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) | Foundry, Hub-based |
| [FLUX-1.1-pro](https://ai.azure.com/explore/models/FLUX-1.1-pro/version/1/registry/azureml-blackforestlabs) | Image generation | - **Input:** text (5000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Hub-based |


See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=black+forest+labs).

### DeepSeek models sold directly by Azure

DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | Foundry, Hub-based |
| [DeepSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=DeepSeek).

### Meta models sold directly by Azure

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta) | chat-completion | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta). There are also several Meta models available [from partners and community](#meta).

### Microsoft models sold directly by Azure

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | Foundry, Hub-based |

See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft). There are also several Microsoft models available [from partners and community](#microsoft).

### Mistral models sold directly by Azure

| Model | Type | Capabilities | Project type 
| ------ | ---- | ------------ | ------------ |
| [mistral-document-ai-2505](https://ai.azure.com/explore/models/mistral-document-ai-2505/version/1/registry/azureml-mistral) | Image-to-Text | - **Input:** image or PDF pages ( 30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  | Foundry |

See [the Mistral model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI).  There are also several Mistral models available [from partners and community](#mistral-ai).


### xAI models sold directly by Azure

xAI's Grok 3 and Grok 3 Mini models are designed to excel in various enterprise domains. Grok 3, a non-reasoning model pretrained by the Colossus datacenter, is tailored for business use cases such as data extraction, coding, and text summarization, with exceptional instruction-following capabilities. It supports a 131,072 token context window, allowing it to handle extensive inputs while maintaining coherence and depth, and is adept at drawing connections across domains and languages. On the other hand, Grok 3 Mini is a lightweight reasoning model trained to tackle agentic, coding, mathematical, and deep science problems with test-time compute. It also supports a 131,072 token context window for understanding codebases and enterprise documents, and excels at using tools to solve complex logical problems in novel environments, offering raw reasoning traces for user inspection with adjustable thinking budgets.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [grok-3](https://ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai)<sup>1</sup> | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | Foundry, Hub-based |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai)<sup>1</sup> | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | Foundry, Hub-based |

See [the xAI model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=xAI).


## Models from partners and community

Models from partners and community constitute the majority of the Azure AI Foundry Models and are provided by trusted third-party organizations, partners, research labs, and community contributors. To learn more about these models, see [Models from Partners and Community](../../concepts/foundry-models-overview.md#models-from-partners-and-community).


### Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------- | ------------ |
| [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,182 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [embed-v-4-0](https://ai.azure.com/explore/models/embed-v-4-0/version/4/registry/azureml-cohere) | embeddings | - **Input:** text (512 tokens) and images (2MM pixels) <br /> - **Output:** Vector (256, 512, 1024, 1536 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | Foundry, Hub-based |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere) | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` | Foundry, Hub-based |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere) | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | Foundry, Hub-based |

#### Cohere rerank

| Model | Type | Capabilities | API Reference | Project type |
| ------ | ---- | ------------ | ------------- | ------------ |
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) | rerank <br> text classification | - **Input:** text <br /> - **Output:** text  <br /> - **Languages:** English, Chinese, French, German, Indonesian, Italian, Portuguese, Russian, Spanish, Arabic, Dutch, Hindi, Japanese, Vietnamese | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) | Hub-based |

For more details on pricing for Cohere rerank models, see [Pricing for Cohere rerank models](../../concepts/models-inference-examples.md#pricing-for-cohere-rerank-models).

See [the Cohere model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Cohere).

### Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42) | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** en and ar <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Core42).

### Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Llama-4-Scout-17B-16E-Instruct](https://aka.ms/aifoundry/landing/llama-4-scout-17b-16e-instruct) | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta). There are also several Meta models available as [models sold directly by Azure](#meta-models-sold-directly-by-azure).

### Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml) | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml) | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:**  (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-reasoning](https://aka.ms/azureai/landing/Phi-4-reasoning) | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Phi-4-mini-reasoning](https://aka.ms/azureai/landing/Phi-4-mini-reasoning) | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |

See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft).  There are also Microsoft models available as [models sold directly by Azure](#microsoft-models-sold-directly-by-azure).

### Mistral AI

Mistral AI offers two categories of models: premium models such as Mistral Large 2411 and Ministral 3B, and open models such as Mistral Nemo.

| Model | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral) | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Foundry, Hub-based |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-small-2503](https://ai.azure.com/explore/models/Mistral-small-2503/version/1/registry/azureml-mistral) | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-medium-2505](https://aka.ms/aistudio/landing/mistral-medium-2505) | chat-completion |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | Foundry, Hub-based|
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral) | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Foundry, Hub-based |
| [Mistral-OCR-2503](https://aka.ms/aistudio/landing/mistral-ocr-2503) | image to text |  - **Input:** image or PDF pages (1,000 pages, max 50MB PDF file) <br> - **Output:** text <br /> - **Tool calling:** No <br /> - **Response formats:** Text, JSON, Markdown | Hub-based|
| [mistralai-Mistral-7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v01/version/11/registry/azureml) | chat-completion | - **Input:** text  <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Response formats:** Text | Hub-based |
| [mistralai-Mistral-7B-Instruct-v0-2](https://ai.azure.com/explore/models/mistralai-Mistral-7B-Instruct-v0-2/version/6/registry/azureml) | chat-completion | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x7B-Instruct-v01](https://ai.azure.com/explore/models/mistralai-Mixtral-8x7B-Instruct-v01/version/10/registry/azureml) | chat-completion | - **Input:** text  <br /> - **Output:** text <br /> - **Languages:** en <br /> - **Response formats:** Text | Hub-based |
| [mistralai-Mixtral-8x22B-Instruct-v0-1](https://ai.azure.com/explore/models/mistralai-Mixtral-8x22B-Instruct-v0-1/version/5/registry/azureml) | chat-completion | - **Input:** text (64,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, it, de, es, en <br /> - **Response formats:** Text | Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI).


### Nixtla

Nixtla's TimeGEN-1 is a generative pretrained forecasting and anomaly detection model for time series data. TimeGEN-1 can produce accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.

| Model  | Type | Capabilities | Inference API | Project type |
| ------ | ---- | --- | ------------ | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla) | Forecasting  | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/nixtla/docs/reference/nixtla_client.html#nixtlaclient-forecast) | Hub-based |

For more details on pricing for Nixtla models, see [Nixtla](../../concepts/models-inference-examples.md#Nixtla).


### NTT Data

**tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata) | chat-completion | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=NTT+Data).

### Stability AI

The Stability AI collection of image generation models include Stable Image Core, Stable Image Ultra, and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large allows for an image and text input. 

| Model  | Type | Capabilities | Project type |
| ------ | ---- | ------------ | ------------ |
| [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text and image (1,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) | Hub-based |
| [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Hub-based |
| [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) | Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Stability+AI).


## Open and custom models

The model catalog offers a larger selection of models, from a bigger range of providers. For these models, you can't use the option for [standard deployment in Azure AI Foundry resources](../../concepts/deployments-overview.md#standard-deployment-in-azure-ai-foundry-resources), where models are provided as APIs; rather, to deploy these models, you might be required to host them on your infrastructure, create an AI hub, and provide the underlying compute quota to host the models.

Furthermore, these models can be open-access or IP protected. In both cases, you have to deploy them in managed compute offerings in Azure AI Foundry. To get started, see [How-to: Deploy to Managed compute](../../how-to/deploy-models-managed.md).


## Related content

- [Deployment overview for Azure AI Foundry Models](../../concepts/deployments-overview.md)
- [Add and configure models to Azure AI Foundry Models](../how-to/create-model-deployments.md)
- [How to generate chat completions with Azure AI Foundry Models](../how-to/use-chat-completions.md)
- [Serverless API inference examples for Foundry Models](../../concepts/models-inference-examples.md)
