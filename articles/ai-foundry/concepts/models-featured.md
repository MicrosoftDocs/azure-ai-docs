---
title: Featured models of Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Explore a variety of models available within AI Foundry
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: conceptual
ms.date: 03/06/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
---

# Featured models of Azure AI Foundry

The Azure AI model catalog offers a large selection of models, from a wide range of providers. This article lists featured models available in AI Foundry. 

[!INCLUDE [models-preview](../includes/models-preview.md)]

You have various options for deploying these models. For some models, you need to host them on your infrastructure, as in the case of deployment via managed compute, while for others, you can host them on Microsoft's servers, as in the case of deployment via serverless APIs. See [Available models for supported deployment options](../how-to/model-catalog-overview.md#available-models-for-supported-deployment-options) for a list of models in the catalog that are available for deployment via managed compute or serverless API.

When it comes to performing inferencing with the models, some of these models are supported for inferencing using the [Azure AI model inference](../model-inference/overview.md), while others require you to use custom APIs from the model providers. You can find more details about individual models by reviewing their model cards in the [model catalog for Azure AI Foundry portal](https://ai.azure.com/explore/models).


:::image type="content" source="../media/models-featured/models-catalog.gif" alt-text="An animation showing Azure AI studio model catalog section and the models available." lightbox="../media/models-featured/models-catalog.gif":::

### AI21 Labs

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which uses AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-ai21) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description | 
| [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |



See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=ai21).

### Azure OpenAI

Azure OpenAI Service offers a diverse set of models with different capabilities and price points. These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [o3-mini](https://ai.azure.com/explore/models/o3-mini/version/2025-01-31/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [o1](https://ai.azure.com/explore/models/o1/version/2024-12-17/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description|
| [o1-preview](https://ai.azure.com/explore/models/o1-preview/version/1/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [o1-mini](https://ai.azure.com/explore/models/o1-mini/version/1/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [gpt-4o-realtime-preview](https://ai.azure.com/explore/models/gpt-4o-realtime-preview/version/2024-10-01/registry/azure-openai) | real-time |  short description |
| [gpt-4o](https://ai.azure.com/explore/models/gpt-4o/version/2024-11-20/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [gpt-4o-mini](https://ai.azure.com/explore/models/gpt-4o-mini/version/2024-07-18/registry/azure-openai) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [text-embedding-3-large](https://ai.azure.com/explore/models/text-embedding-3-large/version/1/registry/azure-openai) | [embeddings](../model-inference/how-to/use-embeddings.md?context=/azure/ai-foundry/context/context) |  short description |
| [text-embedding-3-small](https://ai.azure.com/explore/models/text-embedding-3-small/version/1/registry/azure-openai) | [embeddings](../model-inference/how-to/use-embeddings.md?context=/azure/ai-foundry/context/context) |  short description |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=aoai).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including rerank, chat completions, and embeddings. The following table lists the available Cohere rerank models. that can be accessed for inferencing, by using Cohere's rerank API. For other Cohere models that you can inference via the  Azure AI model Inference, see [Cohere models](https://learn.microsoft.com/azure/ai-foundry/model-inference/concepts/models?context=%2Fazure%2Fai-studio%2Fcontext%2Fcontext#cohere).

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere) | embeddings <br /> [image-embeddings](../model-inference/how-to/use-image-embeddings.md) | short description |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere) | embeddings <br /> [image-embeddings](../model-inference/how-to/use-image-embeddings.md) | short description |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Cohere-command-r-plus](https://ai.azure.com/explore/models/Cohere-command-r-plus/version/1/registry/azureml-cohere) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Cohere-command-r](https://ai.azure.com/explore/models/Cohere-command-r/version/1/registry/azureml-cohere) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |

### Cohere rerank

| Model  | Type | Description | Inference API | 
| ------ | ---- | --- | --- | 
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) | rerank <br> text classification  | short description | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) |
| [Cohere-rerank-v3-english](https://ai.azure.com/explore/models/Cohere-rerank-v3-english/version/1/registry/azureml-cohere) | rerank <br> text classification  | short description | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |
| [Cohere-rerank-v3-multilingual](https://ai.azure.com/explore/models/Cohere-rerank-v3-multilingual/version/1/registry/azureml-cohere) | rerank <br> text classification  | short description | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |


#### Pricing for Cohere Rerank models

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 500 tokens (for Cohere-rerank-v3.5) or longer than 4096 tokens (for Cohere-rerank-v3-English and Cohere-rerank-v3-multilingual) when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

See the [Cohere model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=cohere).

### Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=core42).

### DeepSeek

DeepSeek family of models include DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [DeekSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) |Short description |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=deepseek).

### Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/9/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/4/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 
| [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/9/registry/azureml-meta) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | Short description | 

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=meta).

### Microsoft

Phi is a family of lightweight, state-of-the-art open models. These models were trained with Phi-3 datasets. The datasets include both synthetic data and the filtered, publicly available websites data, with a focus on high quality and reasoning-dense properties. The models underwent a rigorous enhancement process, incorporating both supervised fine-tuning, proximal policy optimization, and direct preference optimization to ensure precise instruction adherence and robust safety measures.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [Phi-3-mini-128k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-128k-instruct/version/12/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |   short description |
| [Phi-3-mini-4k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-4k-instruct/version/14/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Phi-3-small-8k-instruct](https://ai.azure.com/explore/models/Phi-3-small-8k-instruct/version/5/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |   short description |
| [Phi-3-medium-128k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-128k-instruct/version/6/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |   short description |
| [Phi-3-medium-4k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-4k-instruct/version/5/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Phi-3.5-vision-instruct](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/2/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Phi-3.5-MoE-instruct](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/5/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Phi-3-small-128k-instruct](https://ai.azure.com/explore/models/Phi-3-small-128k-instruct/version/4/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Phi-3.5-mini-instruct](https://ai.azure.com/explore/models/Phi-3.5-mini-instruct/version/6/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

### Mistral AI

Mistral AI offers two categories of models: premium models including Mistral Large and Mistral Small and open models including Mistral Nemo.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Mistral-large](https://ai.azure.com/explore/models/Mistral-large/version/1/registry/azureml-mistral) <br /> (deprecated) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Mistral-small](https://ai.azure.com/explore/models/Mistral-small/version/1/registry/azureml-mistral) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Mistral-large-2407](https://ai.azure.com/explore/models/Mistral-large-2407/version/1/registry/azureml-mistral) <br /> (legacy) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) |  short description |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=mistral).

## Nixtla

Nixtla's TimeGEN-1 is a generative pre-trained forecasting and anomaly detection model for time series data. TimeGEN-1 can produce accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

| Model  | Type | Inference API |
| ------ | ---- | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla) | Forecasting | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/nixtla/docs/reference/nixtla_client.html#nixtlaclient-forecast) |

#### Estimate the number of tokens needed

Before you create a TimeGEN-1 deployment, it's useful to estimate the number of tokens that you plan to consume and be billed for.
One token corresponds to one data point in your input dataset or output dataset.

Suppose you have the following input time series dataset:

| Unique_id | Timestamp           | Target Variable | Exogenous Variable 1 | Exogenous Variable 2 |
|:---------:|:-------------------:|:---------------:|:--------------------:|:--------------------:|
| BE        | 2016-10-22 00:00:00 | 70.00           | 49593.0              | 57253.0              |
| BE        | 2016-10-22 01:00:00 | 37.10           | 46073.0              | 51887.0              |

To determine the number of tokens, multiply the number of rows (in this example, two) and the number of columns used for forecasting—not counting the unique_id and timestamp columns (in this example, three) to get a total of six tokens.

Given the following output dataset:

| Unique_id | Timestamp           | Forecasted Target Variable |
|:---------:|:-------------------:|:--------------------------:|
| BE        | 2016-10-22 02:00:00 | 46.57                      |
| BE        | 2016-10-22 03:00:00 | 48.57                      |

You can also determine the number of tokens by counting the number of data points returned after data forecasting. In this example, the number of tokens is two.

#### Estimate pricing based on tokens

There are four pricing meters that determine the price you pay. These meters are as follows:

| Pricing Meter | Description |
| -- | -- |
| paygo-inference-input-tokens | Costs associated with the tokens used as input for inference when *finetune_steps* = 0 |
| paygo-inference-output-tokens | Costs associated with the tokens used as output for inference when *finetune_steps* = 0 |
| paygo-finetuned-model-inference-input-tokens | Costs associated with the tokens used as input for inference when *finetune_steps* > 0 |
| paygo-finetuned-model-inference-output-tokens | Costs associated with the tokens used as output for inference when *finetune_steps* > 0 |

See the [Nixtla model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=nixtla).

### NTT Data

**Tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). Tsuzumi is handles both Japanese and English language with high efficiency.

| Model  | Type | Description | 
| ------ | ---- | --- | 
| [Tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata) | [chat-completion](../model-inference/how-to/use-chat-completions.md?context=/azure/ai-foundry/context/context) | short description |

## Related content

- [Region availability for models in serverless API endpoints](../how-to/deploy-models-serverless-availability.md)

