---
title: Develop Applications with Semantic Kernel and Microsoft Foundry
titleSuffix: Microsoft Foundry
ai-usage: ai-assisted
description: Learn how to Develop applications with Semantic Kernel and Microsoft Foundry with models deployed from the Foundry model catalog.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: taochen
ms.date: 01/30/2026
ms.topic: how-to
ms.service: azure-ai-foundry
---

# Develop applications with Semantic Kernel and Microsoft Foundry

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, you learn how to use [Semantic Kernel](/semantic-kernel/overview/) with models deployed from the Foundry model catalog in Microsoft Foundry portal.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

- A Foundry project as explained at [Create a project in Foundry portal](../create-projects.md).

- A deployed model that supports the [Azure AI Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md?tabs=python). This article uses a `Mistral-Large` deployment. You can use any model. To use embeddings capabilities in LlamaIndex, you need an embedding model like `cohere-embed-v3-multilingual`.

  - Follow the instructions at [Deploy models as serverless API deployments](../deploy-models-serverless.md).

- Python **3.10** or later installed, including pip.
- Semantic Kernel installed. You can use the following command:

    ```bash
    pip install semantic-kernel
    ```

- This article uses the Model Inference API, so install the relevant Azure dependencies. You can use the following command:

    ```bash
    pip install semantic-kernel[azure]
    ```

## Configure the environment

To use language models deployed in Foundry portal, you need the endpoint and credentials to connect to your project. Follow these steps to get the information you need from the model:

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

1. Sign in to [!INCLUDE [classic-link](../../includes/classic-link.md)].
1. Open the project where the model is deployed, if it isn't already open.
1. Go to **Models + endpoints** and select the model you deployed as indicated in the prerequisites.
1. Copy the endpoint URL and the key.

    > [!TIP]
    > If you deployed your model with Microsoft Entra ID support, you don't need a key.

This example uses environment variables for both the endpoint URL and key:

```bash
export AZURE_AI_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_AI_INFERENCE_API_KEY="<your-key-goes-here>"
```

After you configure the endpoint and key, create a client to connect to the endpoint:

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

chat_completion_service = AzureAIInferenceChatCompletion(ai_model_id="<deployment-name>")
```

> [!TIP]
> The client automatically reads the environment variables `AZURE_AI_INFERENCE_ENDPOINT` and `AZURE_AI_INFERENCE_API_KEY` to connect to the model. You can instead pass the endpoint and key directly to the client by using the `endpoint` and `api_key` parameters on the constructor.

Alternatively, if your endpoint supports Microsoft Entra ID, you can use the following code to create the client:

```bash
export AZURE_AI_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
```

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

chat_completion_service = AzureAIInferenceChatCompletion(ai_model_id="<deployment-name>")
```

> [!NOTE]
> If you use Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

### Azure OpenAI models

If you're using an Azure OpenAI model, use the following code to create the client:

```python
from azure.ai.inference.aio import ChatCompletionsClient
from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

chat_completion_service = AzureAIInferenceChatCompletion(
    ai_model_id="<deployment-name>",
    client=ChatCompletionsClient(
        endpoint=f"{str(<your-azure-open-ai-endpoint>).strip('/')}/openai/deployments/{<deployment_name>}",
        credential=DefaultAzureCredential(),
        credential_scopes=["https://cognitiveservices.azure.com/.default"],
    ),
)
```

## Inference parameters

You can configure how to perform inference by using the `AzureAIInferenceChatPromptExecutionSettings` class:

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatPromptExecutionSettings

execution_settings = AzureAIInferenceChatPromptExecutionSettings(
    max_tokens=100,
    temperature=0.5,
    top_p=0.9,
    # extra_parameters={...},    # model-specific parameters
)
```

## Calling the service

First, call the chat completion service with a simple chat history:

> [!TIP]
> Semantic Kernel is an asynchronous library, so you need to use the asyncio library to run the code.
>
> ```python
> import asyncio
> 
> async def main():
>     ...
>
> if __name__ == "__main__":
>     asyncio.run(main())
> ```

```python
from semantic_kernel.contents.chat_history import ChatHistory

chat_history = ChatHistory()
chat_history.add_user_message("Hello, how are you?")

response = await chat_completion_service.get_chat_message_content(
    chat_history=chat_history,
    settings=execution_settings,
)
print(response)
```

Alternatively, you can stream the response from the service:

```python
chat_history = ChatHistory()
chat_history.add_user_message("Hello, how are you?")

response = chat_completion_service.get_streaming_chat_message_content(
    chat_history=chat_history,
    settings=execution_settings,
)

chunks = []
async for chunk in response:
    chunks.append(chunk)
    print(chunk, end="")

full_response = sum(chunks[1:], chunks[0])
```

### Create a long-running conversation

You can create a long-running conversation by using a loop:

```python
while True:
    response = await chat_completion_service.get_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )
    print(response)
    chat_history.add_message(response)
    chat_history.add_user_message(user_input = input("User:> "))
```

If you're streaming the response, you can use the following code:

```python
while True:
    response = chat_completion_service.get_streaming_chat_message_content(
        chat_history=chat_history,
        settings=execution_settings,
    )

    chunks = []
    async for chunk in response:
        chunks.append(chunk)
        print(chunk, end="")

    full_response = sum(chunks[1:], chunks[0])
    chat_history.add_message(full_response)
    chat_history.add_user_message(user_input = input("User:> "))
```

## Use embeddings models

Configure your environment similarly to the previous steps, but use the `AzureAIInferenceEmbeddings` class:

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceTextEmbedding

embedding_generation_service = AzureAIInferenceTextEmbedding(ai_model_id="<deployment-name>")
```

The following code shows how to get embeddings from the service:

```python
embeddings = await embedding_generation_service.generate_embeddings(
    texts=["My favorite color is blue.", "I love to eat pizza."],
)

for embedding in embeddings:
    print(embedding)
```

## Related content

- [How to get started with Azure AI SDKs](sdk-overview.md)
- [Reference for Semantic Kernel model integration](/semantic-kernel/concepts/ai-services/)
