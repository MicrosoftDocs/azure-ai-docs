---
title: Featured models of AI Foundry
titleSuffix: Azure AI Foundry
description: Explore a variety of models available within AI Foundry
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: conceptual
ms.date: 02/26/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
---

# Featured models of AI Foundry

The Azure AI model catalog offers a large selection of models, from a wide range of providers. This article lists featured models available in AI Foundry. Some of these models might require you to host them on your infrastructure, as in the case of deployment via managed compute, or host them on Microsoft's servers, as in the case of deployment via serverless APIs. See [Available models for supported deployment options](../how-to/model-catalog-overview.md#available-models-for-supported-deployment-options) for a list of models in the catalog that are available for deployment via managed compute or serverless API.

For some of these models, you can access them for inferencing only by using custom APIs from the model providers. For these type of models, this article lists the featured partner models and the APIs to use for inferencing. You can find more details about individual models by reviewing their model cards in the [model catalog for Azure AI Foundry portal](https://ai.azure.com/explore/models).

:::image type="content" source="../media/concepts/models-catalog.gif" alt-text="An animation showing Azure AI studio model catalog section and the models available." lightbox="../media/concepts/models-catalog.gif":::

### AI21 Labs

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which uses AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=ai21).

### Azure OpenAI

Azure OpenAI Service offers a diverse set of models with different capabilities and price points. These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=aoai).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including rerank, chat completions, and embeddings. The following table lists the available Cohere rerank models. that can be accessed for inferencing, by using Cohere's rerank API. For other Cohere models that you can inference via the  Azure AI model Inference, see [Cohere models](https://learn.microsoft.com/azure/ai-foundry/model-inference/concepts/models?context=%2Fazure%2Fai-studio%2Fcontext%2Fcontext#cohere).

| Model  | Type | Tier | Capabilities | Inference API|
| ------ | ---- | --- | ------------ |
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) | rerank <br> text classification  | Standard | - **Input:** text (--- tokens) <br /> - **Output:**  text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:**  <br /> - **Response formats:** Text, JSON  | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) |
| [Cohere-rerank-v3-english](https://ai.azure.com/explore/models/Cohere-rerank-v3-english/version/1/registry/azureml-cohere) | rerank <br> text classification  | Standard | - **Input:** text (--- tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:**  <br /> - **Response formats:** Text, JSON  | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |
| [Cohere-rerank-v3-multilingual](https://ai.azure.com/explore/models/Cohere-rerank-v3-multilingual/version/1/registry/azureml-cohere) | rerank <br> text classification  | Standard | - **Input:** text (--- tokens) <br /> - **Output:**  (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:**  <br /> - **Response formats:** Text, JSON  | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |

#### Pricing for Cohere Rerank models

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 500 tokens (for Cohere-rerank-v3.5) or longer than 4096 tokens (for Cohere-rerank-v3-English and Cohere-rerank-v3-multilingual) when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

See the [Cohere model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=cohere).

### Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=core42).

### DeepSeek

DeepSeek family of models include DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=deepseek).

### Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=meta).

### Microsoft

Phi is a family of lightweight, state-of-the-art open models. These models were trained with Phi-3 datasets. The datasets include both synthetic data and the filtered, publicly available websites data, with a focus on high quality and reasoning-dense properties. The models underwent a rigorous enhancement process, incorporating both supervised fine-tuning, proximal policy optimization, and direct preference optimization to ensure precise instruction adherence and robust safety measures.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

### Mistral AI

Mistral AI offers two categories of models: premium models including Mistral Large and Mistral Small and open models including Mistral Nemo.

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=mistral).

## Nixtla

Nixtla's TimeGEN-1 is a generative pre-trained forecasting and anomaly detection model for time series data. TimeGEN-1 can produce accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

| Model  | Type | Tier | Capabilities | Inference API|
| ------ | ---- | --- | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla) | Forecasting  | Standard | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/nixtla/docs/reference/nixtla_client.html#nixtlaclient-forecast) |

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
|--|--|
| paygo-inference-input-tokens | Costs associated with the tokens used as input for inference when *finetune_steps* = 0 |
| paygo-inference-output-tokens | Costs associated with the tokens used as output for inference when *finetune_steps* = 0 |
| paygo-finetuned-model-inference-input-tokens | Costs associated with the tokens used as input for inference when *finetune_steps* > 0 |
| paygo-finetuned-model-inference-output-tokens | Costs associated with the tokens used as output for inference when *finetune_steps* > 0 |

See the [Nixtla model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=nixtla).

### NTT Data

**Tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). Tsuzumi is handles both Japanese and English language with high efficiency.

## Next steps

- Get started today and [deploy your fist model in Azure AI services](../how-to/create-model-deployments.md)

