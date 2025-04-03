---
title: Develop applications with Semantic Kernel and Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Develop applications with Semantic Kernel and Azure AI Foundry.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: taochen
ms.date: 02/27/2025
ms.topic: how-to
ms.service: azure-ai-foundry
manager: scottpolly
---

# Develop applications with Semantic Kernel and Azure AI Foundry

In this article, you learn how to use [Semantic Kernel](/semantic-kernel/overview/) with models deployed from the Azure AI model catalog in Azure AI Foundry portal.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com).
- An Azure AI project as explained at [Create a project in Azure AI Foundry portal](../create-projects.md).
- A model supporting the [Azure AI model inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md?tabs=python) deployed. In this example, we use a `Mistral-Large` deployment, but use any model of your preference. For using embeddings capabilities in LlamaIndex, you need an embedding model like `cohere-embed-v3-multilingual`.

  - You can follow the instructions at [Deploy models as serverless APIs](../deploy-models-serverless.md).

- Python **3.10** or later installed, including pip.
- Semantic Kernel installed. You can do it with:

    ```bash
    pip install semantic-kernel
    ```

- In this example, we're working with the Azure AI model inference API, so we need to install the relevant Azure dependencies. You can do it with:

    ```bash
    pip install semantic-kernel[azure]
    ```

## Configure the environment

To use LLMs deployed in Azure AI Foundry portal, you need the endpoint and credentials to connect to it. Follow these steps to get the information you need from the model you want to use:

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/).
1. Open the project where the model is deployed, if it isn't already open.
1. Go to **Models + endpoints** and select the model you deployed as indicated in the prerequisites.
1. Copy the endpoint URL and the key.

    :::image type="content" source="../../media/how-to/inference/serverless-endpoint-url-keys.png" alt-text="Screenshot of the option to copy endpoint URI and keys from an endpoint." lightbox="../../media/how-to/inference/serverless-endpoint-url-keys.png":::

    > [!TIP]
    > If your model was deployed with Microsoft Entra ID support, you don't need a key.

In this scenario, we placed both the endpoint URL and key in the following environment variables:

```bash
export AZURE_AI_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_AI_INFERENCE_API_KEY="<your-key-goes-here>"
```

Once configured, create a client to connect to the endpoint:

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

chat_completion_service = AzureAIInferenceChatCompletion(ai_model_id="<deployment-name>")
```

> [!TIP]
> The client automatically reads the environment variables `AZURE_AI_INFERENCE_ENDPOINT` and `AZURE_AI_INFERENCE_API_KEY` to connect to the model. However, you can also pass the endpoint and key directly to the client via the `endpoint` and `api_key` parameters on the constructor.

Alternatively, if your endpoint support Microsoft Entra ID, you can use the following code to create the client:

```bash
export AZURE_AI_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
```

```python
from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion

chat_completion_service = AzureAIInferenceChatCompletion(ai_model_id="<deployment-name>")
```

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

### Azure OpenAI models

If you're using an Azure OpenAI model, you can use the following code to create the client:

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

You can configure how inference is performed by using the `AzureAIInferenceChatPromptExecutionSettings` class:

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

Let's first call the chat completion service with a simple chat history:

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