---
title: Featured models of Foundry model catalog
titleSuffix: Azure Machine Learning
description: Explore various models available within the Foundry model catalog.
author: s-polly
reviewer: santiagxf
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: concept-article
ms.date: 07/29/2025
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: references_regions, tool_generated
ms.collection: ce-skilling-ai-copilot 

---

# Featured models of Foundry model catalog

The Foundry model catalog offers a large selection of models from a wide range of providers. You have various options for deploying models from the model catalog. This article lists featured models in the model catalog that can be deployed and hosted on Microsoft's servers via standard deployments. For some of these models, you can also host them on your infrastructure for deployment via managed compute. See [Available models for supported deployment options](concept-model-catalog.md#deployment-options) to find models in the catalog that are available for deployment via managed compute or standard deployment.


To perform inferencing with the models, some models such as [Nixtla's TimeGEN-1](#nixtla) and [Cohere rerank](#cohere-rerank) require you to use custom APIs from the model providers. Others support inferencing using the [Azure AI model inference](../ai-foundry/model-inference/overview.md). You can find more details about individual models by reviewing their model cards in the [model catalog](https://ai.azure.com/explore/models).

:::image type="content" source="../ai-foundry/media/models-featured/models-catalog.gif" alt-text="An animation showing Foundry model catalog section and the models available." lightbox="../ai-foundry/media/models-featured/models-catalog.gif":::



## AI21 Labs

The Jamba family models are AI21's production-grade Mamba-based large language model (LLM) which uses AI21's hybrid Mamba-Transformer architecture. It's an instruction-tuned version of AI21's hybrid structured state space model (SSM) transformer Jamba model. The Jamba family models are built for reliable commercial use with respect to quality and performance.

| Model  | Type | Capabilities |
| ------ | ---- | --- |
| [AI21-Jamba-1.5-Mini](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Mini/version/1/registry/azureml-ai21) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (262,144 tokens) <br /> - **Output:**  text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [AI21-Jamba-1.5-Large](https://ai.azure.com/explore/models/AI21-Jamba-1.5-Large/version/1/registry/azureml-ai21) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (262,144 tokens) <br /> - **Output:**  text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |


See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=ai21).

## Azure OpenAI

Azure OpenAI in Microsoft Foundry Models offers a diverse set of models with different capabilities and price points. These models include:

- State-of-the-art models designed to tackle reasoning and problem-solving tasks with increased focus and capability
- Models that can understand and generate natural language and code
- Models that can transcribe and translate speech to text

| Model  | Type | Capabilities | 
| ------ | ---- | --- | 
| [o3-mini](https://ai.azure.com/explore/models/o3-mini/version/2025-01-31/registry/azure-openai) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text and image (200,000 tokens) <br /> - **Output:** text (100,000 tokens) <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs  |
| [o1](https://ai.azure.com/explore/models/o1/version/2024-12-17/registry/azure-openai) | [chat-completion (with images)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (200,000 tokens) <br /> - **Output:** text (100,000 tokens) <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs|
| [o1-preview](https://ai.azure.com/explore/models/o1-preview/version/1/registry/azure-openai) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (128,000 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [o1-mini](https://ai.azure.com/explore/models/o1-mini/version/1/registry/azure-openai) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |   - **Input:** text (128,000 tokens) <br /> - **Output:** text (65,536 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [gpt-4o-realtime-preview](https://ai.azure.com/explore/models/gpt-4o-realtime-preview/version/2024-10-01/registry/azure-openai) | real-time |   - **Input:** control, text, and audio (131,072 tokens) <br /> - **Output:** text and audio (16,384 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON  |
| [gpt-4o](https://ai.azure.com/explore/models/gpt-4o/version/2024-11-20/registry/azure-openai) | [chat-completion (with image and audio content)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) |   - **Input:** text, image, and audio (131,072 tokens) <br /> - **Output:** text (16,384 tokens) <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs  |
| [gpt-4o-mini](https://ai.azure.com/explore/models/gpt-4o-mini/version/2024-07-18/registry/azure-openai) | [chat-completion (with image and audio content)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) |  - **Input:** text, image, and audio (131,072 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON, structured outputs |
| [text-embedding-3-large](https://ai.azure.com/explore/models/text-embedding-3-large/version/1/registry/azure-openai) | [embeddings](../ai-foundry/model-inference/how-to/use-embeddings.md?context=/azure/machine-learning/context/context) |  - **Input:** text (8,191 tokens) <br /> - **Output:** Vector (3,072 dim.) |
| [text-embedding-3-small](https://ai.azure.com/explore/models/text-embedding-3-small/version/1/registry/azure-openai) | [embeddings](../ai-foundry/model-inference/how-to/use-embeddings.md?context=/azure/machine-learning/context/context) |   - **Input:** text (8,191 tokens) <br /> - **Output:** Vector (1,536 dim.) |


See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=aoai).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including rerank, chat completions, and embeddings models.

### Cohere command and embed

The following table lists the Cohere models that you can inference via the  Azure AI model Inference.

| Model  | Type | Capabilities | 
| ------ | ---- | --- | 
| [Cohere-command-A](https://aka.ms/aistudio/landing/cohere-command-a) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (256,000 tokens) <br /> - **Output:** text (8,000 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text |
| [Cohere-command-r-plus-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-plus-08-2024/version/1/registry/azureml-cohere) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r-08-2024](https://ai.azure.com/explore/models/Cohere-command-r-08-2024/version/1/registry/azureml-cohere) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r-plus](https://ai.azure.com/explore/models/Cohere-command-r-plus/version/1/registry/azureml-cohere) <br> (deprecated) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-command-r](https://ai.azure.com/explore/models/Cohere-command-r/version/1/registry/azureml-cohere) <br> (deprecated)| [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Cohere-embed-4](https://aka.ms/aistudio/landing/cohere-embed-4) | [embeddings](../ai-foundry/model-inference/how-to/use-embeddings.md?context=/azure/machine-learning/context/context) <br /> [image-embeddings](../ai-foundry/model-inference/how-to/use-image-embeddings.md?context=/azure/machine-learning/context/context) | - **Input:** image, text <br /> - **Output:** image, text (128,000 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** image, text  |
| [Cohere-embed-v3-english](https://ai.azure.com/explore/models/Cohere-embed-v3-english/version/1/registry/azureml-cohere) | [embeddings](../ai-foundry/model-inference/how-to/use-embeddings.md?context=/azure/machine-learning/context/context) <br /> [image-embeddings](../ai-foundry/model-inference/how-to/use-image-embeddings.md?context=/azure/machine-learning/context/context) | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1,024 dim.) |
| [Cohere-embed-v3-multilingual](https://ai.azure.com/explore/models/Cohere-embed-v3-multilingual/version/1/registry/azureml-cohere) | [embeddings](../ai-foundry/model-inference/how-to/use-embeddings.md?context=/azure/machine-learning/context/context) <br /> [image-embeddings](../ai-foundry/model-inference/how-to/use-image-embeddings.md?context=/azure/machine-learning/context/context) | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1,024 dim.) |

#### Inference examples: Cohere command and embed

For more examples of how to use Cohere models, see the following examples:

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

The following table lists the Cohere rerank models. To perform inferencing with these rerank models, you're required to use Cohere's custom rerank APIs that are listed in the table.

| Model  | Type | Inference API | 
| ------ | ---- | --- | 
| [Cohere-rerank-v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/1/registry/azureml-cohere) | rerank <br> text classification | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) |
| [Cohere-rerank-v3-english](https://ai.azure.com/explore/models/Cohere-rerank-v3-english/version/1/registry/azureml-cohere) <br> (deprecated) | rerank <br> text classification  | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |
| [Cohere-rerank-v3-multilingual](https://ai.azure.com/explore/models/Cohere-rerank-v3-multilingual/version/1/registry/azureml-cohere) <br> (deprecated) | rerank <br> text classification | [Cohere's v2/rerank API](https://docs.cohere.com/v2/reference/rerank) <br> [Cohere's v1/rerank API](https://docs.cohere.com/v1/reference/rerank) |


#### Pricing for Cohere rerank models

*Queries*, not to be confused with a user's query, is a pricing meter that refers to the cost associated with the tokens used as input for inference of a Cohere Rerank model. Cohere counts a single search unit as a query with up to 100 documents to be ranked. Documents longer than 500 tokens (for Cohere-rerank-v3.5) or longer than 4096 tokens (for Cohere-rerank-v3-English and Cohere-rerank-v3-multilingual) when including the length of the search query are split up into multiple chunks, where each chunk counts as a single document.

See the [Cohere model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=cohere).

## Core42

Core42 includes autoregressive bi-lingual LLMs for Arabic & English with state-of-the-art capabilities in Arabic.

| Model  | Type | Capabilities | 
| ------ | ---- | --- | 
| [jais-30b-chat](https://ai.azure.com/explore/models/jais-30b-chat/version/1/registry/azureml-core42) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (8,192 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | 

See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=core42).

#### Inference examples: Core42

For more examples of how to use Jais models, see the following examples:    

| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)   |      
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples)  |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |


## DeepSeek

DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks using a step-by-step training process, such as language, scientific reasoning, and coding tasks, DeepSeek-V3-0324, a Mixture-of-Experts (MoE) language model, and more. 

| Model  | Type | Capabilities | 
| ------ | ---- | --- | 
| [DeekSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** (131,072 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text, JSON |
| [DeepSeek-V3](https://ai.azure.com/explore/models/deepseek-v3/version/1/registry/azureml-deepseek) <br />(Legacy) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON |
| [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | [chat-completion with reasoning content](../ai-foundry/model-inference/how-to/use-chat-reasoning.md?context=/azure/machine-learning/context/context) | - **Input:** text (163,840 tokens) <br /> - **Output:** text (163,840 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |

For a tutorial on DeepSeek-R1, see [Tutorial: Get started with DeepSeek-R1 reasoning model in Azure AI model inference](../ai-foundry/model-inference/tutorials/get-started-deepseek-r1.md).

See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=deepseek).

#### Inference examples: DeepSeek

For more examples of how to use DeepSeek models, see the following examples:    

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

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| [Llama-4-Scout-17B-16E-Instruct](https://aka.ms/aifoundry/landing/llama-4-scout-17b-16e-instruct) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text |
| [Llama 4-Maverick-17B-128E-Instruct-FP8](https://aka.ms/aifoundry/landing/llama-4-maverick-17b-128e-instruct-fp8) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Llama-3.2-90B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-90B-Vision-Instruct/version/1/registry/azureml-meta) | [chat-completion (with images)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Llama-3.2-11B-Vision-Instruct](https://ai.azure.com/explore/models/Llama-3.2-11B-Vision-Instruct/version/1/registry/azureml-meta) | [chat-completion (with images)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/4/registry/azureml-meta) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-405B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-405B-Instruct/version/1/registry/azureml-meta) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/4/registry/azureml-meta) (deprecated)| [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/9/registry/azureml-meta) (deprecated)| [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/9/registry/azureml-meta) (deprecated)| [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |


See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=meta).

#### Inference examples: Meta Llama

For more examples of how to use Meta Llama models, see the following examples:  
  
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

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).


| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) | [chat-completion with reasoning content](../ai-foundry/model-inference/how-to/use-chat-reasoning.md?context=/azure/machine-learning/context/context) | - **Input:** text (163,840 tokens) <br /> - **Output:** text (163,840 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text. |
| [Phi-4-reasoning](https://aka.ms/azureai/landing/Phi-4-reasoning) | [chat-completion with reasoning content](../ai-foundry/model-inference/how-to/use-chat-reasoning.md?context=/azure/machine-learning/context/context) | - **Input:** text (32768 tokens) <br /> - **Output:** text (32768 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4-mini-reasoning](https://aka.ms/azureai/landing/Phi-4-mini-reasoning) | [chat-completion with reasoning content](../ai-foundry/model-inference/how-to/use-chat-reasoning.md?context=/azure/machine-learning/context/context) | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4-multimodal-instruct](https://ai.azure.com/explore/models/Phi-4-multimodal-instruct/version/1/registry/azureml) | [chat-completion (with image and audio content)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4-mini-instruct](https://ai.azure.com/explore/models/Phi-4-mini-instruct/version/1/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-4](https://ai.azure.com/explore/models/Phi-4/version/2/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (16,384 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-mini-instruct](https://ai.azure.com/explore/models/Phi-3.5-mini-instruct/version/6/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-MoE-instruct](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/5/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3.5-vision-instruct](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/2/registry/azureml) | [chat-completion (with images)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) | - **Input:** text and image (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-mini-128k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-128k-instruct/version/12/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-mini-4k-instruct](https://ai.azure.com/explore/models/Phi-3-mini-4k-instruct/version/14/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (4,096 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-small-128k-instruct](https://ai.azure.com/explore/models/Phi-3-small-128k-instruct/version/4/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-small-8k-instruct](https://ai.azure.com/explore/models/Phi-3-small-8k-instruct/version/5/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-medium-128k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-128k-instruct/version/6/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| [Phi-3-medium-4k-instruct](https://ai.azure.com/explore/models/Phi-3-medium-4k-instruct/version/5/registry/azureml) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (4,096 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |


#### Inference examples: Microsoft models

For more examples of how to use Microsoft models, see the following examples:   

| Description                               | Language          | Sample                                                          |    
|-------------------------------------------|-------------------|-----------------------------------------------------------------|    
| Azure AI Inference package for C#         | C#                | [Link](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Inference/samples)                  |    
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-inference-rest/samples) |    
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |    
| LangChain                                 | Python            | [Link](https://aka.ms/azureai/langchain)           |    
| Llama-Index                               | Python            | [Link](https://aka.ms/azureai/llamaindex)             |  


See [the Microsoft model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=phi).


## Mistral AI

Mistral AI offers two categories of models, namely: 

- _Premium models_: These include Mistral Large, Mistral Small, Mistral-OCR-2503, Mistral Medium 3 (25.05), and Ministral 3B models, and are available as serverless APIs with pay-as-you-go token-based billing.  
- _Open models_: These include Mistral-small-2503, Codestral, and Mistral Nemo (that are available as serverless APIs with pay-as-you-go token-based billing), and [Mixtral-8x7B-Instruct-v01, Mixtral-8x7B-v01, Mistral-7B-Instruct-v01, and Mistral-7B-v01](../ai-foundry/concepts/models-inference-examples.md#mistral-ai)(that are available to download and run on self-hosted managed endpoints).

| Model  | Type | Capabilities |
| ------ | ---- | --- | 
| [Codestral-2501](https://ai.azure.com/explore/models/Codestral-2501/version/2/registry/azureml-mistral) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| [Ministral-3B](https://ai.azure.com/explore/models/Ministral-3B/version/1/registry/azureml-mistral) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-Nemo](https://ai.azure.com/explore/models/Mistral-Nemo/version/1/registry/azureml-mistral) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-Large-2411](https://ai.azure.com/explore/models/Mistral-Large-2411/version/2/registry/azureml-mistral) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (128,000 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-large-2407](https://ai.azure.com/explore/models/Mistral-large-2407/version/1/registry/azureml-mistral) <br /> (deprecated) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON  |
| [Mistral-large](https://ai.azure.com/explore/models/Mistral-large/version/1/registry/azureml-mistral) <br /> (deprecated) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-medium-2505](https://aka.ms/aistudio/landing/mistral-medium-2505) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON |
| [Mistral-OCR-2503](https://aka.ms/aistudio/landing/mistral-ocr-2503) | [image to text](../ai-foundry/how-to/use-image-models.md?context=/azure/machine-learning/context/context) |  - **Input:** image or PDF pages (1,000 pages, max 50MB PDF file) <br> - **Output:** text <br /> - **Tool calling:** No <br /> - **Response formats:** Text, JSON, Markdown |
| [Mistral-small-2503](https://aka.ms/aistudio/landing/mistral-small-2503) | [chat-completion (with images)](../ai-foundry/model-inference/how-to/use-chat-multi-modal.md?context=/azure/machine-learning/context/context) |  - **Input:** text and images (131,072 tokens), <br> image-based tokens are 16px x 16px <br> blocks of the original images <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| [Mistral-small](https://ai.azure.com/explore/models/Mistral-small/version/1/registry/azureml-mistral) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) |  - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |

See [this model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=mistral).

#### Inference examples: Mistral

For more examples of how to use Mistral models, see the following examples and tutorials:    

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

To perform inferencing, TimeGEN-1 requires you to use Nixtla's custom inference API.

| Model  | Type | Capabilities | Inference API|
| ------ | ---- | --- | ------------ |
| [TimeGEN-1](https://ai.azure.com/explore/models/TimeGEN-1/version/1/registry/azureml-nixtla) | Forecasting  | - **Input:** Time series data as JSON or dataframes (with support for multivariate input)  <br /> - **Output:**  Time series data as JSON <br /> - **Tool calling:** No <br /> - **Response formats:** JSON  | [Forecast client to interact with Nixtla's API](https://nixtlaverse.nixtla.io/nixtla/docs/reference/nixtla_client.html#nixtlaclient-forecast) |

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

See the [Nixtla model collection in the model catalog](https://ai.azure.com/explore/models?&selectedCollection=nixtla).

## NTT DATA

**tsuzumi** is an autoregressive language optimized transformer. The tuned versions use supervised fine-tuning (SFT). tsuzumi handles both Japanese and English language with high efficiency.

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| [tsuzumi-7b](https://ai.azure.com/explore/models/Tsuzumi-7b/version/1/registry/azureml-nttdata) | [chat-completion](../ai-foundry/model-inference/how-to/use-chat-completions.md?context=/azure/machine-learning/context/context) | - **Input:** text (8,192 tokens) <br /> - **Output:** text (8,192 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text |

## Stability AI

The Stability AI collection of image generation models include Stable Image Core, Stable Image Ultra and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large allows for an image and text input. 

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| [Stable Diffusion 3.5 Large](https://ai.azure.com/explore/models/Stable-Diffusion-3.5-Large/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text and image (1000 tokens and 1 image)  <br /> - **Output:** 1 Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) |
| [Stable Image Core](https://ai.azure.com/explore/models/Stable-Image-Core/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text (1000 tokens)  <br /> - **Output:** 1 Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |
| [Stable Image Ultra](https://ai.azure.com/explore/models/Stable-Image-Ultra/version/1/registry/azureml-stabilityai) | Image generation | - **Input:** text (1000 tokens)  <br /> - **Output:** 1 Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |

#### Inference examples: Stability AI

Stability AI models deployed to standard deployments implement the Azure AI model inference API on the route `/image/generations`.
For examples of how to use Stability AI models, see the following examples:

- [Use OpenAI SDK with Stability AI models for text to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Text_to_Image_openai_library.ipynb)
- [Use Requests library with Stability AI models for text to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Text_to_Image_requests_library.ipynb)
- [Use Requests library with Stable Diffusion 3.5 Large for image to image requests](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Image_to_Image.ipynb)
- [Example of a fully encoded image generation response](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/stabilityai/Sample_image_generation_response.txt)


## Related content

- [Deploy models as standard deployment](how-to-deploy-models-serverless.md)
- [Model catalog and collections](concept-model-catalog.md)
- [Region availability for models in standard deployment](concept-endpoint-serverless-availability.md)
- [Content safety for Models Sold Directly by Azure](../ai-foundry/concepts/model-catalog-content-safety.md)
