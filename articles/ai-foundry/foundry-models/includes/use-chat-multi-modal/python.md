---
title: How to use image and audio in chat completions with Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how to process audio and images with chat completions models with Microsoft Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use chat completions API with _multimodal_ models deployed in Microsoft Foundry Models. Apart from text input, multimodal models can accept other input types, such as images or audio input.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-python](../how-to-prerequisites-python.md)]

* A chat completions model deployment with support for **audio and images**. If you don't have one, see [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

  * This article uses `Phi-4-multimodal-instruct`.

## Use chat completions

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    model="Phi-4-multimodal-instruct"
)
```

If you've configured the resource with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    model="Phi-4-multimodal-instruct"
)
```

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of some models for vision in a chat fashion. 

Images can be passed to models using URLs and including them inside of messages with the role **user**. You can also use [data URLs](https://developer.mozilla.org/docs/Web/URI/Reference/Schemes/data) which allow you to embed the actual content of the file inside of a URL encoded in `base64` strings.

Let's consider the following image which can be download [from this source](https://news.microsoft.com/source/wp-content/uploads/2024/04/The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg):

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

You can load the image into a *data URL* as follows:

```python
from azure.ai.inference.models import ImageContentItem, ImageUrl

data_url = ImageUrl.load(
    image_file="The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg",
    image_format="jpeg"
)
```

Data URLs are of the form `data:image/{image_format};base64,{image_data_base64}`.

Now, create a chat completion request with the image:

```python
from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem, ImageContentItem, ImageUrl
response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant that can generate responses based on images."),
        UserMessage(content=[
            TextContentItem(text="Which conclusion can be extracted from the following chart?"),
            ImageContentItem(image_url=data_url)
        ]),
    ],
    temperature=1,
    max_tokens=2048,
)
```

The response is as follows, where you can see the model's usage statistics:

```python
print(f"{response.choices[0].message.role}: {response.choices[0].message.content}")
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
```

```console
ASSISTANT: The chart illustrates that larger models tend to perform better in quality, as indicated by their size in billions of parameters. However, there are exceptions to this trend, such as Phi-3-medium and Phi-3-small, which outperform smaller models in quality. This suggests that while larger models generally have an advantage, there might be other factors at play that influence a model's performance.
Model: phi-4-omni
Usage: 
  Prompt tokens: 2380
  Completion tokens: 126
  Total tokens: 2506
```

### Usage

Images are broken into tokens and submitted to the model for processing. When referring to images, each of those tokens is typically referred as *patches*. Each model might break down a given image on a different number of patches. Read the model card to learn the details.

### Multi-turn conversations

Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error. Read the model card to understand the case of each model.

### Image URLs

The model can read the content from an **accessible cloud location** by passing the URL as an input. This approach requires the URL to be public and do not require specific handling.

```python
from azure.ai.inference.models import SystemMessage, UserMessage, TextContentItem, ImageContentItem, ImageUrl

image_url = "https://news.microsoft.com/source/wp-content/uploads/2024/04/The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg"

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant that can generate responses based on images."),
        UserMessage(content=[
            TextContentItem(text="Which conclusion can be extracted from the following chart?"),
            ImageContentItem(image_url=ImageUrl(image_url))
        ]),
    ],
    temperature=1,
    max_tokens=2048,
)
```

## Use chat completions with audio

Some models can reason across text and audio inputs. The following example shows how you can send audio context to chat completions models that also supports audio. Use `InputAudio` to load the content of the audio file into the payload. The content is encoded in `base64` data and sent over the payload.

```python
from azure.ai.inference.models import (
    TextContentItem,
    AudioContentItem,
    InputAudio,
    AudioContentFormat,
    SystemMessage,
    UserMessage
)

response = client.complete(
    messages=[
        SystemMessage("You are an AI assistant for translating and transcribing audio clips."),
        UserMessage(
            [
                TextContentItem(text="Please translate this audio snippet to spanish."),
                AudioContentItem(
                    input_audio=InputAudio.load(
                        audio_file="hello_how_are_you.mp3", audio_format=AudioContentFormat.MP3
                    )
                ),
            ],
        ),
    ],
)
```

The response is as follows, where you can see the model's usage statistics:

```python
print(f"{response.choices[0].message.role}: {response.choices[0].message.content}")
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
```

```console
ASSISTANT: Hola. ¿Cómo estás?
Model: speech
Usage:
    Prompt tokens: 77
    Completion tokens: 7
    Total tokens: 84
```

The model can read the content from an **accessible cloud location** by passing the URL as an input. The Python SDK doesn't provide a direct way to do it, but you can indicate the payload as follows:

```python
response = client.complete(
    {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant for translating and transcribing audio clips.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please translate this audio snippet to spanish."
                    },
                    {
                        "type": "audio_url",
                        "audio_url": {
                            "url": "https://.../hello_how_are_you.mp3"
                        }
                    }
                ]
            },
        ],
    }
)
```
### Usage

Audio is broken into tokens and submitted to the model for processing. Some models might operate directly over audio tokens while other might use internal modules to perform speech-to-text, resulting in different strategies to compute tokens. Read the model card for details about how each model operates.