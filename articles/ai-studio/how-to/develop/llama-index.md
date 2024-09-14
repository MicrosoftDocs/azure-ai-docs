---
title: Develop application with LlamaIndex and Azure AI studio
titleSuffix: Azure AI Studio
description: This article explains how to use LlamaIndex with models deployed in Azure AI studio to build advance intelligent applications
manager: nitinme
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 9/14/2024
ms.reviewer: fasantia
ms.author: eur
author: eric-urban
---

# Develop application with LlamaIndex and Azure AI studio

In this article, you learn how to use [`llama-index`](https://github.com/run-llama/llama_index) with models deployed from the Azure AI model catalog deployed to Azure AI studio.

## Prerequisites

To run this tutorial you need:

1. An [Azure subscription](https://azure.microsoft.com).
2. An Azure AI hub resource as explained at [How to create and manage an Azure AI Studio hub](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/create-azure-ai-resource).
3. A model supporting the [Azure AI model inference API](https://aka.ms/azureai/modelinference) deployed. In this example we use a `Mistral-Large` deployment, but use any model of your preference. For using embeddings capabilities in LlamaIndex, you need an embedding model like Cohere Embed V3. 

    * You can follow the instructions at [Deploy models as serverless APIs](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless).

4. A Python environment.


## Install dependencies

Ensure you have `llama-index` installed:

```bash
pip install llama-index
```

Models deployed to Azure AI studio or Azure Machine Learning can be used with LlamaIndex in two ways:

- **Using the Azure AI model inference API:** All models deployed to Azure AI studio and Azure Machine Learning support the Azure AI model inference API, which offers a common set of functionalities that can be used for most of the models in the catalog. The benefit of this API is that, since it's the same for all the models, changing from one to another is as simple as changing the model deployment being use. No further changes are required in the code. When working with `llama-index`, install the extensions `llama-index-llms-azure-inference` and `llama-index-embeddings-azure-inference`.

- **Using the model's provider specific API:** Some models, like OpenAI, Cohere, or Mistral, offer their own set of APIs and extensions for `llama-index`. Those extensions may include specific functionalities that the model support and hence are suitable if you want to exploit them. When working with `llama-index`, install the extension specific for the model you want to use, like `llama-index-llms-openai` or `llama-index-llms-cohere`.


In this example, we are working with the Azure AI model inference API, hence we install the following packages:

```bash
pip install -U llama-index-llms-azure-inference
pip install -U llama-index-embeddings-azure-inference
```

## Configure the environment

To use LLMs deployed in Azure AI studio you need the endpoint and credentials to connect to it. The parameter `model_name` is not required for endpoints serving a single model, like Managed Online Endpoints. Follow this steps to get the information you need from the model you want to use:

1. Go to the [Azure AI studio](https://ai.azure.com/).
2. Go to deployments and select the model you have deployed as indicated in the prerequisites.
3. Copy the endpoint URL and the key.
    
> [!TIP]
> If your model was deployed with Microsoft Entra ID support, you don't need a key.

In this scenario, we have placed both the endpoint URL and key in the following environment variables:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Once configured, create a client to connect to the endpoint:

```python
import os
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

Alternatively, if you endpoint support Microsoft Entra ID, you can use the following code to create the client:

```python
from azure.identity import DefaultAzureCredential

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> [!NOTE]
> > Note: When using Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

If you are planning to use asynchronous calling, it's a best practice to use the asynchronous version for the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
)
```

### Inference parameters

You can configure how inference in performed for all the operations that are using this client by setting extra parameters. This helps avoid indicating them on each call you make to the model.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"top_p": 1.0},
)
```

For parameters extra parameters that are not supported by the Azure AI model inference API but that are available in the underlying model, you can use the `model_extras` argument. In the following example, the parameter `safe_prompt`, only available for Mistral models, is being passed.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"model_extras": {"safe_prompt": True}},
)
```

## Use LLMs models

Use the `chat` endpoint for chat instruction models. The `complete` method is still available for model of type `chat-completions`. On those cases, your input text is converted to a message with `role="user"`.

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="You are a pirate with colorful personality."
    ),
    ChatMessage(role="user", content="Hello"),
]

response = llm.chat(messages)
print(response)
```

You can stream the outputs also:

```python
response = llm.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

## Use embeddings models

In the same way you create an LLM client, you can connect to an embedding model. In the following example, we are setting again the environment variable to now point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Then create the client:

```python
from llama_index.embeddings.azure_inference import AzureAIEmbeddingsModel

embed_model = AzureAIEmbeddingsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ['AZURE_INFERENCE_CREDENTIAL'],
)
```

## Configure the models used by your code

You can use the LLM or embeddings model client individually in the code you develop with LlamaIndex or you can configure the entire session using the `Settings` options. Configuring the session has the advantage that then all your code will use the same models for all the operations.

```python
from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
```

However, there are scenarios where you want to use a general model for most of the operations but an specific one for a given task. On those cases, it's useful to set the LLM or embedding model your are using for each LlamaIndex construct. In the following example, we set an specific model:

```python
from llama_index.core.evaluation import RelevancyEvaluator

relevancy_evaluator = RelevancyEvaluator(llm=llm)
```

In general, you will use a combination of both strategies.

## Related content

* [How to get started with Azure AI SDKs](sdk-overview.md)
