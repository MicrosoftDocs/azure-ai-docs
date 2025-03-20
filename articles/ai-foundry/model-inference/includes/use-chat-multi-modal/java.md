---
title: How to use image and audio in chat completions with Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to process audio and images with chat completions models with Azure AI model inference
manager: scottpolly
author: mopeakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

> [!NOTE]
> Using audio inputs is only supported using Python, JavaScript, C#, or REST requests.

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of Some models for vision in a chat fashion:

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):

Visualize the image:

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:

The response is as follows, where you can see the model's usage statistics:

```console
ASSISTANT: The chart illustrates that larger models tend to perform better in quality, as indicated by their size in billions of parameters. However, there are exceptions to this trend, such as Phi-3-medium and Phi-3-small, which outperform smaller models in quality. This suggests that while larger models generally have an advantage, there might be other factors at play that influence a model's performance.
Model: mistral-large-2407
Usage: 
  Prompt tokens: 2380
  Completion tokens: 126
  Total tokens: 2506
```