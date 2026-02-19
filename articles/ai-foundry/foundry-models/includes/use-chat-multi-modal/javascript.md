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

[!INCLUDE [how-to-prerequisites-javascript](../how-to-prerequisites-javascript.md)]

* A chat completions model deployment with support for **audio and images**. If you don't have one, see [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

  * This article uses `Phi-4-multimodal-instruct`.

## Use chat completions

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

```javascript
const client = ModelClient(
    "https://<resource>.services.ai.azure.com/api/models", 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

If you've configured the resource with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

```javascript
const clientOptions = { credentials: { "https://cognitiveservices.azure.com" } };

const client = ModelClient(
    "https://<resource>.services.ai.azure.com/api/models", 
    new DefaultAzureCredential()
    clientOptions,
);
```

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of some models for vision in a chat fashion. 

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):

```javascript
const image_url = "https://news.microsoft.com/source/wp-content/uploads/2024/04/The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg";
const image_format = "jpeg";

const response = await fetch(image_url, { headers: { "User-Agent": "Mozilla/5.0" } });
const image_data = await response.arrayBuffer();
const image_data_base64 = Buffer.from(image_data).toString("base64");
const data_url = `data:image/${image_format};base64,${image_data_base64}`;
```

Visualize the image:


```javascript
const img = document.createElement("img");
img.src = data_url;
document.body.appendChild(img);
```

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:


```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant that can generate responses based on images." },
    { role: "user", content: 
        [
            { type: "text", text: "Which conclusion can be extracted from the following chart?" },
            { type: "image_url", image:
                {
                    url: data_url
                }
            } 
        ] 
    }
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        model: "Phi-4-multimodal-instruct",
    }
});
```

The response is as follows, where you can see the model's usage statistics:


```javascript
console.log(response.body.choices[0].message.role + ": " + response.body.choices[0].message.content);
console.log("Model:", response.body.model);
console.log("Usage:");
console.log("\tPrompt tokens:", response.body.usage.prompt_tokens);
console.log("\tCompletion tokens:", response.body.usage.completion_tokens);
console.log("\tTotal tokens:", response.body.usage.total_tokens);
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

Some models can reason across text and audio inputs. The following example shows how you can send audio context to chat completions models that also supports audio.

In this example, we create a function `getAudioData` to load the content of the audio file encoded in `base64` data as the model expects it.

```javascript
import fs from "node:fs";

/**
 * Get the Base 64 data of an audio file.
 * @param {string} audioFile - The path to the image file.
 * @returns {string} Base64 data of the audio.
 */
function getAudioData(audioFile: string): string {
  try {
    const audioBuffer = fs.readFileSync(audioFile);
    return audioBuffer.toString("base64");
  } catch (error) {
    console.error(`Could not read '${audioFile}'.`);
    console.error("Set the correct path to the audio file before running this sample.");
    process.exit(1);
  }
}
```

Let's now use this function to load the content of an audio file stored on disk. We send the content of the audio file in a user message. Notice that in the request we also indicate the format of the audio content:

```javascript
const audioFilePath = "hello_how_are_you.mp3"
const audioFormat = "mp3"
const audioData = getAudioData(audioFilePath);

const systemMessage = { role: "system", content: "You are an AI assistant for translating and transcribing audio clips." };
const audioMessage = { 
role: "user",
content: [
    { type: "text", text: "Translate this audio snippet to spanish."},
    { type: "input_audio",
    input_audio: {
        audioData,
        audioFormat,
    },
    },
] 
};

const response = await client.path("/chat/completions").post({
    body: {
      messages: [
        systemMessage,
        audioMessage
      ],
      model: "Phi-4-multimodal-instruct",
    },
  });
```

The response is as follows, where you can see the model's usage statistics:

```javascript
if (isUnexpected(response)) {
    throw response.body.error;
}

console.log("Response: ", response.body.choices[0].message.content);
console.log("Model: ", response.body.model);
console.log("Usage:");
console.log("\tPrompt tokens:", response.body.usage.prompt_tokens);
console.log("\tTotal tokens:", response.body.usage.total_tokens);
console.log("\tCompletion tokens:", response.body.usage.completion_tokens);
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

```javascript
const systemMessage = { role: "system", content: "You are a helpful assistant." };
const audioMessage = { 
    role: "user",
    content: [
        { type: "text", text: "Transcribe this audio."},
        { type: "audio_url",
        audio_url: {
            url: "https://example.com/audio.mp3", 
        },
        },
    ] 
};

const response = await client.path("/chat/completions").post({
    body: {
      messages: [
        systemMessage,
        audioMessage
      ],
      model: "Phi-4-multimodal-instruct",
    },
  });
```

### Usage

Audio is broken into tokens and submitted to the model for processing. Some models might operate directly over audio tokens while other might use internal modules to perform speech-to-text, resulting in different strategies to compute tokens. Read the model card for details about how each model operates.