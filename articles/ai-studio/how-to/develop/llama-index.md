---
title: Develop application with LlamaIndex and Azure AI studio
titleSuffix: Azure AI Studio
description: This article explains how to use LlamaIndex with models deployed in Azure AI studio to build advance intelligent applications.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 9/14/2024
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
---

# Develop applications with LlamaIndex and Azure AI studio

In this article, you learn how to use [LlamaIndex](https://github.com/run-llama/llama_index) with models deployed from the Azure AI model catalog in Azure AI studio.

Models deployed to Azure AI studio can be used with LlamaIndex in two ways:

- **Using the Azure AI model inference API:** All models deployed to Azure AI studio support the [Azure AI model inference API](../../reference/reference-model-inference-api.md), which offers a common set of functionalities that can be used for most of the models in the catalog. The benefit of this API is that, since it's the same for all the models, changing from one to another is as simple as changing the model deployment being use. No further changes are required in the code. When working with LlamaIndex, install the extensions `llama-index-llms-azure-inference` and `llama-index-embeddings-azure-inference`.

- **Using the model's provider specific API:** Some models, like OpenAI, Cohere, or Mistral, offer their own set of APIs and extensions for LlamaIndex. Those extensions may include specific functionalities that the model support and hence are suitable if you want to exploit them. When working with `llama-index`, install the extension specific for the model you want to use, like `llama-index-llms-openai` or `llama-index-llms-cohere`.

In this example, we are working with the **Azure AI model inference API**.

## Prerequisites

To run this tutorial, you need:

1. An [Azure subscription](https://azure.microsoft.com).
2. An Azure AI hub resource as explained at [How to create and manage an Azure AI Studio hub](../create-azure-ai-resource.md).
3. A model supporting the [Azure AI model inference API](https://aka.ms/azureai/modelinference) deployed. In this example, we use a `Mistral-Large` deployment, but use any model of your preference. For using embeddings capabilities in LlamaIndex, you need an embedding model like `cohere-embed-v3-multilingual`. 

    * You can follow the instructions at [Deploy models as serverless APIs](../deploy-models-serverless.md).

4. Python 3.8 or later installed, including pip.
5. LlamaIndex installed. You can do it with:

    ```bash
    pip install llama-index
    ```

6. In this example, we are working with the Azure AI model inference API, hence we install the following packages:

    ```bash
    pip install -U llama-index-llms-azure-inference
    pip install -U llama-index-embeddings-azure-inference
    ```

    > [!IMPORTANT]
    > Using the [Azure AI model inference service](https://aka.ms/aiservices/inference) requires version `0.2.4` for `llama-index-llms-azure-inference` or `llama-index-embeddings-azure-inference`.

## Configure the environment

To use LLMs deployed in Azure AI studio, you need the endpoint and credentials to connect to it. Follow these steps to get the information you need from the model you want to use:

1. Go to the [Azure AI studio](https://ai.azure.com/).
2. Go to deployments and select the model you deployed as indicated in the prerequisites.
3. Copy the endpoint URL and the key.

    :::image type="content" source="../../media/how-to/inference/serverless-endpoint-url-keys.png" alt-text="Screenshot of the option to copy endpoint URI and keys from an endpoint." lightbox="../../media/how-to/inference/serverless-endpoint-url-keys.png":::
    
    > [!TIP]
    > If your model was deployed with Microsoft Entra ID support, you don't need a key.

In this scenario, we placed both the endpoint URL and key in the following environment variables:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Once configured, create a client to connect to the endpoint.

```python
import os
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

> [!TIP]
> If your model is an OpenAI model deployed to Azure OpenAI service or AI services resource, configure the client as indicated at [Azure OpenAI models and Azure AI model inference service](#azure-openai-models-and-azure-ai-model-infernece-service).

If your endpoint is serving more than one model, like with the [Azure AI model inference service](../../ai-services/model-endpoint.md) or [GitHub Models](https://github.com/marketplace/models), you have to indicate `model_name` parameter:

```python
import os
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="mistral-large-2407",
)
```

Alternatively, if your endpoint support Microsoft Entra ID, you can use the following code to create the client:

```python
import os
from azure.identity import DefaultAzureCredential
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

If you are planning to use asynchronous calling, it's a best practice to use the asynchronous version for the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
)
```

### Azure OpenAI models and Azure AI model infernece service

If you are using Azure OpenAI models or [Azure AI model inference service](../../ai-services/model-endpoint.md), ensure you have at least version `0.2.4` of the LlamaIndex integration. Use `api_version` parameter in case you need to select a specific `api_version`. For the [Azure AI model inference service](../../ai-services/model-endpoint.md), you need to pass `model_name` parameter:

```python
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="gpt-4o",
    api_version="2024-05-01-preview",
)
```

> [!TIP]
> Using a wrong `api_version` or one not supported by the model results in a `ResourceNotFound` exception.

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

Parameters not supported in the Azure AI model inference API ([reference](../../reference/reference-model-inference-chat-completions.md)) but available in the underlying model, you can use the `model_extras` argument. In the following example, the parameter `safe_prompt`, only available for Mistral models, is being passed.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"model_extras": {"safe_prompt": True}},
)
```

## Use LLMs models

You can use the client directly or [Configure the models used by your code](#configure-the-models-used-by-your-code) in LlamaIndex. To use the model directly, use the `chat` method for chat instruction models:

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

The `complete` method is still available for model of type `chat-completions`. On those cases, your input text is converted to a message with `role="user"`.

## Use embeddings models

In the same way you create an LLM client, you can connect to an embeddings model. In the following example, we are setting the environment variable to now point to an embeddings model:

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

The following example shows a simple test to verify it works:

```python
from llama_index.core.schema import TextNode

nodes = [
    TextNode(
        text="Before college the two main things I worked on, "
        "outside of school, were writing and programming."
    )
]
response = embed_model(nodes=nodes)
print(response[0].embedding)
```

## Configure the models used by your code

You can use the LLM or embeddings model client individually in the code you develop with LlamaIndex or you can configure the entire session using the `Settings` options. Configuring the session has the advantage of all your code using the same models for all the operations.

```python
from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
```

However, there are scenarios where you want to use a general model for most of the operations but a specific one for a given task. On those cases, it's useful to set the LLM or embedding model you are using for each LlamaIndex construct. In the following example, we set a specific model:

```python
from llama_index.core.evaluation import RelevancyEvaluator

relevancy_evaluator = RelevancyEvaluator(llm=llm)
```

In general, you use a combination of both strategies.

## Related content

* [How to get started with Azure AI SDKs](sdk-overview.md)
* [Reference for LlamaIndex Embeddings Integration](https://llamahub.ai/l/embeddings/llama-index-embeddings-azure-inference)
* [Reference for LlamaIndex LLMs Integration](https://llamahub.ai/l/llms/llama-index-llms-azure-inference)
