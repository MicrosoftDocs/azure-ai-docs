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

* A chat completions model deployment. If you don't have one, see [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

  * This article uses `Phi-4-multimodal-instruct`.


## Use chat completions

To use chat completions API, use the route `/chat/completions` appended to the base URL along with your credential indicated in `api-key`. `Authorization` header is also supported with the format `Bearer <key>`.

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
api-key: <key>
```

If you've configured the resource with **Microsoft Entra ID** support, pass your token in the `Authorization` header with the format `Bearer <token>`. Use scope `https://cognitiveservices.azure.com/.default`. 

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
Authorization: Bearer <token>
```

Using Microsoft Entra ID might require extra configuration in your resource to grant access. Learn how to [configure key-less authentication with Microsoft Entra ID](../../how-to/configure-entra-id.md).

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of Some models for vision in a chat fashion:

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):

> [!TIP]
> You'll need to construct the data URL using a scripting or programming language. This article uses [this sample image](../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg) in JPEG format. A data URL has a format as follows: `data:image/jpg;base64,0xABCDFGHIJKLMNOPQRSTUVWXYZ...`.

Visualize the image:

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:


```json
{
    "model": "Phi-4-multimodal-instruct",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Which peculiar conclusion about LLMs and SLMs can be extracted from the following chart?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpg;base64,0xABCDFGHIJKLMNOPQRSTUVWXYZ..."
                    }
                }
            ]
        }
    ],
    "temperature": 0,
    "top_p": 1,
    "max_tokens": 2048
}
```

The response is as follows, where you can see the model's usage statistics:


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "Phi-4-multimodal-instruct",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The chart illustrates that larger models tend to perform better in quality, as indicated by their size in billions of parameters. However, there are exceptions to this trend, such as Phi-3-medium and Phi-3-small, which outperform smaller models in quality. This suggests that while larger models generally have an advantage, there might be other factors at play that influence a model's performance.",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 2380,
        "completion_tokens": 126,
        "total_tokens": 2506
    }
}
```

Images are broken into tokens and submitted to the model for processing. When referring to images, each of those tokens is typically referred as *patches*. Each model might break down a given image on a different number of patches. Read the model card to learn the details.

## Use chat completions with audio

Some models can reason across text and audio inputs. The following example shows how you can send audio context to chat completions models that also supports audio. 

The following example sends audio content encoded in `base64` data in the chat history:

```json
{
    "model": "Phi-4-multimodal-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are an AI assistant for translating and transcribing audio clips."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Please translate this audio snippet to spanish."
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "0xABCDFGHIJKLMNOPQRSTUVWXYZ...",
                        "format": "mp3"
                    }
                }
            ]
        }
    ],
}
```

The response is as follows, where you can see the model's usage statistics:

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "Phi-4-multimodal-instruct",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hola. ¿Cómo estás?",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 77,
        "completion_tokens": 7,
        "total_tokens": 84
    }
}
```

The model can read the content from an **accessible cloud location** by passing the URL as an input. You can indicate the payload as follows:

```json
{
    "model": "Phi-4-multimodal-instruct",
    "messages": [
        {
            "role": "system",
            "content": "You are an AI assistant for translating and transcribing audio clips."
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
                        "url": "https://.../hello_how_are_you.mp3",
                    }
                }
            ]
        }
    ],
}
```

The response is as follows, where you can see the model's usage statistics:

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "Phi-4-multimodal-instruct",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hola. ¿Cómo estás?",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 77,
        "completion_tokens": 7,
        "total_tokens": 84
    }
}
```

Audio is broken into tokens and submitted to the model for processing. Some models might operate directly over audio tokens while others might use internal modules to perform speech-to-text, resulting in different strategies to compute tokens. Read the model card for details about how each model operates.