---
title: Models available in Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Explore the models available via Azure AI Foundry Models and their capabilities.
author: msakande
ms.author: mopeakande
manager: scottpolly
reviewer: santiagxf
ms.reviewer: fasantia
ms.date: 07/03/2025
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.custom:
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
---

# Models and capabilities

Azure AI Foundry Models gives you access to flagship models in Azure AI Foundry to consume them as APIs with flexible deployment options.

This article lists the current model offerings and their capabilities, excluding [deprecated and legacy models](../../concepts/model-lifecycle-retirement.md#deprecated)

## Azure OpenAI

Azure OpenAI in Azure AI Foundry Models offers a diverse set of models with different capabilities and price points. Learn more details at [Azure OpenAI Model availability](../../../ai-services/openai/concepts/models.md). These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

| Models | Description | Serverless API Availability |
|--|--|--|
| [GPT-4.1 series](../../../ai-services/openai/concepts/models.md#gpt-41-series) | Latest model release from Azure OpenAI | Yes |
| [model-router](../../../ai-services/openai/concepts/models.md#model-router) | A model that intelligently selects from a set of underlying chat models to respond to a given prompt. | Yes |
| [computer-use-preview](../../../ai-services/openai/concepts/models.md#computer-use-preview) | An experimental model trained for use with the Responses API computer use tool. | Yes |
| [GPT-4.5 Preview](../../../ai-services/openai/concepts/models.md#gpt-45-preview) |The latest GPT model that excels at diverse text and image tasks.  | Yes |
| [o-series models](../../../ai-services/openai/concepts/models.md#o-series-models) |[Reasoning models](../../../ai-services/openai/how-to/reasoning.md) with advanced problem-solving and increased focus and capability.  | Yes |
| [GPT-4o & GPT-4o mini & GPT-4 Turbo](../../../ai-services/openai/concepts/models.md#gpt-4o-and-gpt-4-turbo) | The latest most capable Azure OpenAI models with multimodal versions, which can accept both text and images as input. | Yes |
| [GPT-4](../../../ai-services/openai/concepts/models.md#gpt-4) | A set of models that improve on GPT-3.5 and can understand and generate natural language and code. | Yes |
| [GPT-3.5](../../../ai-services/openai/concepts/models.md#gpt-35) | A set of models that improve on GPT-3 and can understand and generate natural language and code. | Yes |
| [Embeddings](../../../ai-services/openai/concepts/models.md#embeddings-models) | A set of models that can convert text into numerical vector form to facilitate text similarity. | Yes |
| [Image generation](../../../ai-services/openai/concepts/models.md#image-generation-models) | A series of models that can generate original images from natural language. | Yes |
| [Audio](../../../ai-services/openai/concepts/models.md#audio-models) | A series of models for speech to text, translation, and text to speech. GPT-4o audio models support either low-latency, "speech in, speech out" conversational interactions or audio generation. | Yes |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=aoai).

## AI21 Labs

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which uses AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-ai21) | chat-completion | Partners and Community | - **Input:** text (262,144 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `pt`, `de`, `ar`, and `he` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs | No |
| [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) | chat-completion | Partners and Community | - **Input:** text (262,144 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `pt`, `de`, `ar`, and `he` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs | No |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=ai21).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------- | --------------------------- |
| [Cohere-command-a](https://ai.azure.com/explore/models/Cohere-command-a/version/1/registry/azureml-cohere) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,182 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [embed-v-4-0](https://ai.azure.com/explore/models/embed-v-4-0/version/4/registry/azureml-cohere) | embeddings | Partners and Community | - **Input:** text (512 tokens) and images (2MM pixels) <br /> - **Output:** Vector (256, 512, 1024, 1536 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | No |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere) | embeddings | Partners and Community | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` | No |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere) | embeddings | Partners and Community | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | No |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=cohere).

## Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42) | chat-completion | Partners and Community | - **Input:** text (8,192 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** en and ar <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=core42).

## DeepSeek

DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | ---- | ------------ | --------------------------- |
| [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Models sold directly by Azure | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | Yes |
| [DeepSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek) | chat-completion | Models sold directly by Azure | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | Yes |
| [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Models sold directly by Azure | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | Yes |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=deepseek).

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text and image (128,000 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No* <br /> - **Response formats:** Text | No |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=meta). There are also several Meta models available as [Models Sold Directly by Azure](../../concepts/foundry-models-overview.md#models-sold-directly-by-azure). 

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) |  chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | Partners and Community | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | No |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml) | chat-completion | Partners and Community | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (16,384 tokens) <br /> - **Output:**  (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3.5-mini-instruct](https://ai.azure.com/explore/models/Phi-3.5-mini-instruct/version/6/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en`, `ar`, `zh`, `cs`, `da`, `nl`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3.5-vision-instruct](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/2/registry/azureml) | chat-completion | Partners and Community | - **Input:** text and image (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3.5-MoE-instruct](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/5/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `ar`, `zh`, `cs`, `da`, `nl`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-mini-128k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-128k-instruct/version/12/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-mini-4k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-4k-instruct/version/14/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (4,096 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-small-8k-instruct](https://ai.azure.com/explore/models/Phi-3-small-8k-instruct/version/5/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-medium-128k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-128k-instruct/version/6/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-medium-4k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-4k-instruct/version/5/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (4,096 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Phi-3-small-128k-instruct](https://ai.azure.com/explore/models/Phi-3-small-128k-instruct/version/4/registry/azureml) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |

See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

## Mistral AI

Mistral AI offers two categories of models: premium models including Mistral Large and Mistral Small and open models including Mistral Nemo.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral) | chat-completion | Partners and Community | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |
| [Mistral-small-2503](https://ai.azure.com/explore/models/Mistral-small-2503/version/1/registry/azureml-mistral) | chat-completion | Partners and Community | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral) | chat-completion | Partners and Community | - **Input:** text (128,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral) | chat-completion | Partners and Community | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `zh`, `ja`, `ko`, `pt`, `nl`, and `pl` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | No |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=mistral).

## NTT Data

**tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata) | chat-completion | Partners and Community | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` and `jp` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | No |

## xAI

xAI's Grok 3 and Grok 3 Mini models are designed to excel in various enterprise domains. Grok 3, a non-reasoning model pre-trained by the Colossus datacenter, is tailored for business use cases such as data extraction, coding, and text summarization, with exceptional instruction-following capabilities. It supports a 131,072 token context window, allowing it to handle extensive inputs while maintaining coherence and depth, and is particularly adept at drawing connections across domains and languages. On the other hand, Grok 3 Mini is a lightweight reasoning model trained to tackle agentic, coding, mathematical, and deep science problems with test-time compute. It also supports a 131,072 token context window for understanding codebases and enterprise documents, and excels at using tools to solve complex logical problems in novel environments, offering raw reasoning traces for user inspection with adjustable thinking budgets.

| Model  | Type | Offering | Capabilities | Serverless API Availability |
| ------ | ---- | --- | ------------ | --------------------------- |
| [grok-3](https://ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai) | chat-completion | Models sold directly by Azure | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | Yes |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai) | chat-completion | Models sold directly by Azure | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | Yes |

## Open and custom models

The model catalog offers a larger selection of models, from a bigger range of providers. For these models, you cannot use the option for [standard deployment in Azure AI Foundry resources](../../concepts/deployments-overview.md#standard-deployment-in-azure-ai-foundry-resources), where models are provided as APIs; rather, to deploy these models, you might be required to host them on your infrastructure, create an AI hub, and provide the underlying compute quota to host the models.

Furthermore, these models can be open-access or IP protected. In both cases, you have to deploy them in Managed Compute offerings in Azure AI Foundry. To get started, see [How-to: Deploy to Managed compute](../../how-to/deploy-models-managed.md).

## Related content

- Get started today and [deploy your first model in Azure AI Foundry Models](../../model-inference/how-to/create-model-deployments.md)
