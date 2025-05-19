---
title: Models available in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Explore the models available via the Azure AI Foundry Models and their capabilities.
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
---

# Models available in Azure AI Foundry Models

Azure AI Foundry Models gives you access to flagship models in Azure AI Foundry to consume them as APIs without hosting them on your infrastructure.

A selection of models is offered directly by Microsoft under [Models Sold Directly by Azure](#models-sold-directly-by-azure) which brings the most powerful options to developers to build AI applications. We also enable the breath of models by partnering with key players in the industry and bringing [Models from Partners and Community](#models-from-partners-and-community).


:::image type="content" source="../media/models/models-catalog.gif" alt-text="An animation showing Azure AI Foundry portal model catalog section and the models available." lightbox="../media/models/models-catalog.gif":::


## Models Sold Directly by Azure 

Models Sold Directly by Azure  is a selection of flagship models offered directly by Microsoft. These models don't require integration with Azure Marketplace. 

### Azure OpenAI

Azure OpenAI in Azure AI Foundry Models offers a diverse set of models with different capabilities and price points. Learn more details at [Azure OpenAI Model availability](../../../ai-services/openai/concepts/models.md). These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

| Model  | Type | Tier | Capabilities |
| ------ | ---- | ---- | ------------ |
| [o3-mini](https://ai.azure.com/explore/models/o3-mini/version/2025-01-31/registry/azure-openai) | chat-completion | Global standard | - **Input:** text and image (200,000 tokens) <br /> - **Output:** text (100,000 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [o1](https://ai.azure.com/explore/models/o1/version/2024-12-17/registry/azure-openai) | chat-completion | Global standard | - **Input:** text and image (200,000 tokens) <br /> - **Output:** text (100,000 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [o1-preview](https://ai.azure.com/explore/models/o1-preview/version/1/registry/azure-openai) | chat-completion | Global standard <br />Standard<br /> | - **Input:** text (128,000 tokens) <br /> - **Output:**  (32,768 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [o1-mini](https://ai.azure.com/explore/models/o1-mini/version/1/registry/azure-openai) | chat-completion | Global standard <br />Standard | - **Input:** text (128,000 tokens) <br /> - **Output:**  (65,536 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [gpt-4o-realtime-preview](https://ai.azure.com/explore/models/gpt-4o-realtime-preview/version/2024-10-01/registry/azure-openai) | real-time | Global standard | - **Input:** control, text, and audio (131,072 tokens) <br /> - **Output:** text and audio (16,384 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [gpt-4o](https://ai.azure.com/explore/models/gpt-4o/version/2024-11-20/registry/azure-openai) | chat-completion | Global standard <br />Standard<br />Batch<br />Provisioned<br />Global provisioned<br />Data Zone | - **Input:** text and image (131,072 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [gpt-4o-mini](https://ai.azure.com/explore/models/gpt-4o-mini/version/2024-07-18/registry/azure-openai) | chat-completion | Global standard <br />Standard<br />Batch<br />Provisioned<br />Global provisioned<br />Data Zone | - **Input:** text, image, and audio (131,072 tokens) <br /> - **Output:**  (16,384 tokens) <br /> - **Languages:** `en`, `it`, `af`, `es`, `de`, `fr`, `id`, `ru`, `pl`, `uk`, `el`, `lv`, `zh`, `ar`, `tr`, `ja`, `sw`, `cy`, `ko`, `is`, `bn`, `ur`, `ne`, `th`, `pa`, `mr`, and `te`. <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [text-embedding-3-large](https://ai.azure.com/explore/models/text-embedding-3-large/version/1/registry/azure-openai) | embeddings | Global standard <br />Standard<br />Provisioned<br />Global provisioned | - **Input:** text (8,191 tokens) <br /> - **Output:** Vector (3,072 dim.) <br /> - **Languages:** `en` |
| [text-embedding-3-small](https://ai.azure.com/explore/models/text-embedding-3-small/version/1/registry/azure-openai) | embeddings | Global standard <br />Standard<br />Provisioned<br />Global provisioned | - **Input:** text (8,191 tokens) <br /> - **Output:** Vector (1,536 dim.) <br /> - **Languages:** `en` |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=aoai).

### DeepSeek

DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | ---- | ------------ |
| [DeekSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [DeekSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Global standard | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |
| [DeekSeek-V3](https://ai.azure.com/explore/models/deepseek-v3/version/1/registry/azureml-deepseek) <br />(Legacy) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON |

For a tutorial on DeepSeek-R1, see [Tutorial: Get started with DeepSeek-R1 reasoning model in Azure AI Foundry Models](../tutorials/get-started-deepseek-r1.md).

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=deepseek).

### Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. Some Microsoft models are offered as [Models from Partners and Community](#models-from-partners-and-community). To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).


| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) |  chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Global standard | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |

### Mistral AI

Mistral AI offers two categories of models: premium models including Mistral Large and Mistral Small and open models including Mistral Nemo. Some Mistral models are offered as [Models from Partners and Community](#models-from-partners-and-community).

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral) | chat-completion | Global standard | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=mistral).

### Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta Llama 4 is part of Models Sold Directly by Azure, while the rest of the Llama family is offered as [Models from Partners and Community](#models-from-partners-and-community).

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=meta).

## Models from Partners and Community

Models from Partners and Community available for deployment with pay-as-you-go billing (for example, Cohere models) are offered by the model provider but hosted in Microsoft-managed Azure infrastructure and accessed via API in the Azure AI Foundry. Model providers define the license terms and set the price for use of their models, while Azure AI Foundry manages the hosting infrastructure.

Models from Partners and Community are offered through Azure Marketplace and [requires additional configuration for enabling](../how-to/configure-marketplace.md). 

### AI21 Labs

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which uses AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-ai21) | chat-completion | Global standard | - **Input:** text (262,144 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `pt`, `de`, `ar`, and `he` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) | chat-completion | Global standard | - **Input:** text (262,144 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `pt`, `de`, `ar`, and `he` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=ai21).

### Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r-plus](https://ai.azure.com/explore/models/Cohere-command-r-plus/version/1/registry/azureml-cohere) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r](https://ai.azure.com/explore/models/Cohere-command-r/version/1/registry/azureml-cohere) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere) | embeddings <br /> image-embeddings | Global standard | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1,024 dim.) <br /> - **Languages:** en |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere) | embeddings <br /> image-embeddings | Global standard | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1,024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` |


See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=cohere).

### Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42) | chat-completion | Global standard | - **Input:** text (8,192 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** en and ar <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |


See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=core42).

### Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/4/registry/azureml-meta) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/9/registry/azureml-meta) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (8,192 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |
| [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/9/registry/azureml-meta) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (8,192 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text |


See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=meta).

### Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).


| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) |  chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Global standard | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml) | chat-completion | Global standard | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml) | chat-completion | Global standard | - **Input:** text (16,384 tokens) <br /> - **Output:**  (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-mini-instruct](https://ai.azure.com/explore/models/Phi-3.5-mini-instruct/version/6/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `ar`, `zh`, `cs`, `da`, `nl`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-vision-instruct](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/2/registry/azureml) | chat-completion | Global standard | - **Input:** text and image (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-MoE-instruct](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/5/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `ar`, `zh`, `cs`, `da`, `nl`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-mini-128k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-128k-instruct/version/12/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-mini-4k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-4k-instruct/version/14/registry/azureml) | chat-completion | Global standard | - **Input:** text (4,096 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-small-8k-instruct](https://ai.azure.com/explore/models/Phi-3-small-8k-instruct/version/5/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-medium-128k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-128k-instruct/version/6/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-medium-4k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-4k-instruct/version/5/registry/azureml) | chat-completion | Global standard | - **Input:** text (4,096 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-small-128k-instruct](https://ai.azure.com/explore/models/Phi-3-small-128k-instruct/version/4/registry/azureml) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |


See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

### Mistral AI

Mistral AI offers two categories of models: premium models including Mistral Large and Mistral Small and open models including Mistral Nemo.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [Mistral-small-2503](https://ai.azure.com/explore/models/Mistral-small-2503/version/1/registry/azureml-mistral) | chat-completion | Global standard | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral) | chat-completion | Global standard | - **Input:** text (128,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-large-2407](https://ai.azure.com/explore/models/Mistral-large-2407/version/1/registry/azureml-mistral) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-small](https://ai.azure.com/explore/models/Mistral-small/version/1/registry/azureml-mistral) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-large](https://ai.azure.com/explore/models/Mistral-large/version/1/registry/azureml-mistral) <br> (deprecated) | chat-completion | Global standard | - **Input:** text (32,768 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=mistral).

### NTT Data

**tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata) | chat-completion | Global standard | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |

### xAI

xAI's Grok 3 and Grok 3 Mini models are designed to excel in various enterprise domains. Grok 3, a non-reasoning model pre-trained by the Colossus datacenter, is tailored for business use cases such as data extraction, coding, and text summarization, with exceptional instruction-following capabilities. It supports a 131,072 token context window, allowing it to handle extensive inputs while maintaining coherence and depth, and is particularly adept at drawing connections across domains and languages. On the other hand, Grok 3 Mini is a lightweight reasoning model trained to tackle agentic, coding, mathematical, and deep science problems with test-time compute. It also supports a 131,072 token context window for understanding codebases and enterprise documents, and excels at using tools to solve complex logical problems in novel environments, offering raw reasoning traces for user inspection with adjustable thinking budgets.

| Model  | Type | Tier | Capabilities |
| ------ | ---- | --- | ------------ |
| [grok-3](https://int.ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai) | chat-completion | Global standard | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |

## Open and protected models

The [Azure AI model catalog](../../../ai-studio/how-to/model-catalog-overview.md) offers a larger selection of models, from a bigger range of providers. As opposite to Azure AI Foundry Models where models are provided as APIs, these models might require you to host them on your infrastructure, including the creation of an AI hub and project, and providing the underlying compute quota to host the models. 

Those models can be of open access or IP protected. In both cases, you have to deploy them in Managed Compute offerings in Azure AI Foundry.

## Next steps

- Get started today and [deploy your fist model in Azure AI Foundry Models](../how-to/create-model-deployments.md)
