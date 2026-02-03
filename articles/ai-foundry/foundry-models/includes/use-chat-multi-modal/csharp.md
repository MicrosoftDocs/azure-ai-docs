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

[!INCLUDE [how-to-prerequisites-csharp](../how-to-prerequisites-csharp.md)]

* A chat completions model deployment. If you don't have one, read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

    * This example uses `phi-4-multimodal-instruct`.

## Use chat completions

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/api/models"),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL")),
);
```

If you've configured the resource with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```csharp
client = new ChatCompletionsClient(
    new Uri("https://<resource>.services.ai.azure.com/api/models"),
    new DefaultAzureCredential(),
);
```

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of Some models for vision in a chat fashion:

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):


```csharp
string imageUrl = "https://news.microsoft.com/source/wp-content/uploads/2024/04/The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg";
string imageFormat = "jpeg";
HttpClient httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");
byte[] imageBytes = httpClient.GetByteArrayAsync(imageUrl).Result;
string imageBase64 = Convert.ToBase64String(imageBytes);
string dataUrl = $"data:image/{imageFormat};base64,{imageBase64}";
```

Visualize the image:

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:


```csharp
ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are an AI assistant that helps people find information."),
        new ChatRequestUserMessage([
            new ChatMessageTextContentItem("Which conclusion can be extracted from the following chart?"),
            new ChatMessageImageContentItem(new Uri(dataUrl))
        ]),
    },
    MaxTokens=2048,
    Model = "Phi-4-multimodal-instruct",
};

var response = client.Complete(requestOptions);
Console.WriteLine(response.Value.Content);
```

The response is as follows, where you can see the model's usage statistics:


```csharp
Console.WriteLine($"{response.Value.Role}: {response.Value.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
```

```console
ASSISTANT: The chart illustrates that larger models tend to perform better in quality, as indicated by their size in billions of parameters. However, there are exceptions to this trend, such as Phi-3-medium and Phi-3-small, which outperform smaller models in quality. This suggests that while larger models generally have an advantage, there might be other factors at play that influence a model's performance.
Model: Phi-4-multimodal-instruct
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

## Use chat completions with audio

Some models can reason across text and audio inputs. The following example shows how you can send audio context to chat completions models that also supports audio. Use `InputAudio` to load the content of the audio file into the payload. The content is encoded in `base64` data and sent over the payload.

```csharp
var requestOptions = new ChatCompletionsOptions()
{
    Messages =
    {
        new ChatRequestSystemMessage("You are an AI assistant for translating and transcribing audio clips."),
        new ChatRequestUserMessage(
            new ChatMessageTextContentItem("Please translate this audio snippet to spanish."),
            new ChatMessageAudioContentItem("hello_how_are_you.mp3", AudioContentFormat.Mp3),
    },
};

Response<ChatCompletions> response = client.Complete(requestOptions);
```

The response is as follows, where you can see the model's usage statistics:

```csharp
Console.WriteLine($"{response.Value.Role}: {response.Value.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
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

```csharp
var requestOptions = new ChatCompletionsOptions()
{
    Messages =
    {
        new ChatRequestSystemMessage("You are an AI assistant for translating and transcribing audio clips."),
        new ChatRequestUserMessage(
            new ChatMessageTextContentItem("Please translate this audio snippet to spanish."),
            new ChatMessageAudioContentItem(new Uri("https://.../hello_how_are_you.mp3"))),
    },
};

Response<ChatCompletions> response = client.Complete(requestOptions);
```

The response is as follows, where you can see the model's usage statistics:

```csharp
Console.WriteLine($"{response.Value.Role}: {response.Value.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
```

```console
ASSISTANT: Hola. ¿Cómo estás?
Model: speech
Usage:
    Prompt tokens: 77
    Completion tokens: 7
    Total tokens: 84
```

### Usage

Audio is broken into tokens and submitted to the model for processing. Some models might operate directly over audio tokens while other might use internal modules to perform speech-to-text, resulting in different strategies to compute tokens. Read the model card for details about how each model operates.