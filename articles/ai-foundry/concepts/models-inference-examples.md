---
title: Serverless API inference examples for Foundry Models
titleSuffix: Microsoft Foundry
description: Inference examples for Foundry Models that support deployment to serverless APIs in Microsoft Foundry.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
reviewer: santiagxf
ms.reviewer: fasantia
ms.date: 12/09/2025
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.custom:
  - references_regions
  - build-aifnd
  - build-2025
---

# Serverless API inference examples for Foundry Models

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The Foundry model catalog offers a large selection of Microsoft Foundry Models from a wide range of providers. You have various options for deploying models from the model catalog. This article lists inference examples for serverless API deployments.

[!INCLUDE [models-preview](../includes/models-preview.md)]

To perform inferencing with the models, some models such as [Nixtla's TimeGEN-1](#nixtla) and [Cohere rerank](#cohere-rerank) require you to use custom APIs from the model providers. Others support inferencing using the [Model Inference API](../foundry-models/concepts/models-sold-directly-by-azure.md). You can find more details about individual models by reviewing their model cards in the [model catalog for Foundry portal](https://ai.azure.com/explore/models).


## Cohere

The Cohere family of models includes various models optimized for different use cases, including rerank, chat completions, and embeddings models.

#### Inference examples: Cohere command and embed

The following table provides links to examples of how to use Cohere models.

| Description                               | Language          | Sample                                                          |
|-------------------------------------------|-------------------|-----------------------------------------------------------------|
| Web requests                              | Bash              | [Command-R](https://aka.ms/samples/cohere-command-r/webrequests)  [Command-R+](https://aka.ms/samples/cohere-command-r-plus/webrequests) <br> [cohere-embed.ipynb](https://aka.ms/samples/embed-v3/webrequests) |
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)   |  
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples)  |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)      |
| OpenAI SDK (experimental)                 | Python            | [Link](https://aka.ms/samples/cohere-command/openaisdk)             |
| LangChain                                 | Python            | [Link](https://aka.ms/samples/cohere/langchain)                     |
| Cohere SDK                                | Python            | [Command](https://aka.ms/samples/cohere-python-sdk)  <br> [Embed](https://aka.ms/samples/cohere-embed/cohere-python-sdk)                  |
| LiteLLM SDK                               | Python            | [Link](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/litellm.ipynb) |

#### Retrieval Augmented Generation (RAG) and tool use samples: Cohere command and embed

| Description | Packages   | Sample          |
|-------------|------------|-----------------|
| Create a local Facebook AI similarity search (FAISS) vector index, using Cohere embeddings - Langchain | `langchain`, `langchain_cohere` | [cohere_faiss_langchain_embed.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere_faiss_langchain_embed.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in local FAISS vector index - Langchain |`langchain`, `langchain_cohere` | [command_faiss_langchain.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/command_faiss_langchain.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in AI search vector index - Langchain | `langchain`, `langchain_cohere` | [cohere-aisearch-langchain-rag.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere-aisearch-langchain-rag.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in AI search vector index - Cohere SDK | `cohere`, `azure_search_documents` | [cohere-aisearch-rag.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere-aisearch-rag.ipynb) |
| Command R+ tool/function calling, using LangChain | `cohere`, `langchain`, `langchain_cohere` | [command_tools-langchain.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/command_tools-langchain.ipynb) |


### Cohere rerank

To perform inferencing with Cohere rerank models, you're required to use Cohere's custom rerank APIs. For more information on the Cohere rerank model and its capabilities, see [Cohere rerank](../foundry-models/concepts/models.md#cohere-rerank).


#### Pricing for Cohere rerank models

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 500 tokens (for Cohere-rerank-v3.5) or longer than 4096 tokens (for Cohere-rerank-v3-English and Cohere-rerank-v3-multilingual) when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

See the [Cohere model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Cohere).

## Core42

The following table provides links to examples of how to use Jais models.


| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)   |      
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples)  |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |


## DeepSeek

DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks, DeepSeek-V3-0324, a Mixture-of-Experts (MoE) language model, and more. 

The following table provides links to examples of how to use DeepSeek models.
  

| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |    
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://aka.ms/azsdk/azure-ai-inference/javascript/samples)  |    
| Azure AI Inference package for C#         | C#                | [Link](https://aka.ms/azsdk/azure-ai-inference/csharp/samples)  |    
| Azure AI Inference package for Java       | Java              | [Link](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-inference/src/samples)  |


## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range is scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performant models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.
- High-performant natively multimodal models, Llama 4 Scout and Llama 4 Maverick, leverage a mixture-of-experts architecture to offer industry-leading performance in text and image understanding.


The following table provides links to examples of how to use Meta Llama models.

  
| Description                               | Language          | Sample                                                             |    
|-------------------------------------------|-------------------|------------------------------------------------------------------- |    
| CURL request                              | Bash              | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-webrequests)    |    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)   |      
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azureml-examples/blob/main/sdk/typescript/README.md) |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)     |    
| Python web requests                       | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-webrequests)    |    
| OpenAI SDK (experimental)                 | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-openai)         |    
| LangChain                                 | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-langchain)      |    
| LiteLLM                                   | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-litellm)        | 

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft).

The following table provides links to examples of how to use Microsoft models.
 

| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)                  |    
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |    
| LangChain                                 | Python            | [Link](https://aka.ms/azureai/langchain)           |    
| Llama-Index                               | Python            | [Link](https://aka.ms/azureai/llamaindex)             |  


See [the Microsoft model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft).


## Mistral AI

Mistral AI offers two categories of models, namely: 

- _Premium models_: These include Mistral Large, Mistral Small, Mistral-OCR-2503, Mistral Medium 3 (25.05), and Ministral 3B models, and are available as serverless APIs with pay-as-you-go token-based billing.  
- _Open models_: These include Mistral-small-2503, Codestral, and Mistral Nemo (that are available as serverless APIs with pay-as-you-go token-based billing), and Mixtral-8x7B-Instruct-v01, Mixtral-8x7B-v01, Mistral-7B-Instruct-v01, and Mistral-7B-v01(that are available to download and run on self-hosted managed endpoints).


The following table provides links to examples of how to use Mistral models.
   

| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| CURL request                              | Bash              | [Link](https://aka.ms/mistral-large/webrequests-sample)         |    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)   |      
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples)  |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |    
| Python web requests                       | Python            | [Link](https://aka.ms/mistral-large/webrequests-sample)         |    
| OpenAI SDK (experimental)                 | Python            | [Mistral - OpenAI SDK sample](https://aka.ms/mistral-large/openaisdk)                  |    
| LangChain                                 | Python            | [Mistral - LangChain sample](https://aka.ms/mistral-large/langchain-sample)           |    
| Mistral AI                                | Python            | [Mistral - Mistral AI sample](https://aka.ms/mistral-large/mistralai-sample)           |    
| LiteLLM                                   | Python            | [Mistral - LiteLLM sample](https://aka.ms/mistral-large/litellm-sample)             | 

## Nixtla

Nixtla's TimeGEN-1 is a generative pre-trained forecasting and anomaly detection model for time series data. TimeGEN-1 can produce accurate forecasts for new time series without training, using only historical values and exogenous covariates as inputs.

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.  For more information on the TimeGEN-1 model and its capabilities, see [Nixtla](../foundry-models/concepts/models.md#nixtla).

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

See the [Nixtla model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Nixtla).

## Stability AI

Stability AI models deployed via serverless API deployment implement the Model Inference API on the route `/image/generations`.
For examples of how to use Stability AI models, see the following examples:

- [Use OpenAI SDK with Stability AI models for text to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Text_to_Image_openai_library.ipynb)
- [Use Requests library with Stability AI models for text to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Text_to_Image_requests_library.ipynb)
- [Use Requests library with Stable Diffusion 3.5 Large for image to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Image_to_Image.ipynb)
- [Example of a fully encoded image generation response](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Sample_image_generation_response.txt)

## Gretel Navigator

Gretel Navigator employs a compound AI architecture specifically engineered for synthetic data, by combining top open-source small language models (SLMs) fine-tuned across more than 10 industry domains. This purpose-built system creates diverse, domain-specific datasets at scales of hundreds to millions of examples. The system also preserves complex statistical relationships and offers increased speed and accuracy compared to manual data creation.

| Description                               | Language          | Sample                                                          |
|-------------------------------------------|-------------------|-----------------------------------------------------------------|
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://aka.ms/azsdk/azure-ai-inference/javascript/samples)  |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  | 


## Related content

- [Deploy models as serverless API deployments](../how-to/deploy-models-serverless.md)
- [Explore Foundry Models](foundry-models-overview.md)
- [Foundry Models and their capabilities](../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Region availability for models in serverless API deployments](../how-to/deploy-models-serverless-availability.md)
- [Content safety for  Models Sold Directly by Azure ](model-catalog-content-safety.md)

