---
title: How to use image and audio in chat completions with Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to process audio and images with chat completions models with Azure AI Foundry Models
manager: scottpolly
author: mopeakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 03/20/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

This article explains how to use chat completions API with _multimodal_ models deployed in Azure AI Foundry Models. Apart from text input, multimodal models can accept other input types, such as images or audio input.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-java](../how-to-prerequisites-java.md)]

* A chat completions model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

    * This example uses `phi-4-multimodal-instruct`.

## Use chat completions

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

```java
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

If you've configured the resource with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

```java
TokenCredential defaultCredential = new DefaultAzureCredentialBuilder().build();
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(defaultCredential)
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```


## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of Some models for vision in a chat fashion:

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):

```java
Path testFilePath = Paths.get("small-language-models-chart-example.jpg");
String imageFormat = "jpg";
```

Visualize the image:

:::image type="content" source="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-foundry/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:

```java
List<ChatMessageContentItem> contentItems = new ArrayList<>();
contentItems.add(new ChatMessageTextContentItem("Which conclusion can be extracted from the following chart?"));
contentItems.add(new ChatMessageImageContentItem(testFilePath, imageFormat));

List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are an AI assistant that helps people find information."));
chatMessages.add(ChatRequestUserMessage.fromContentItems(contentItems));

ChatCompletionsOptions options = new ChatCompletionsOptions(chatMessages);
options.setModel("phi-4-multimodal-instruct")

ChatCompletions response = client.complete(options);
```

The response is as follows, where you can see the model's usage statistics:

```java
System.out.println("Response: " + response.getValue().getChoices().get(0).getMessage().getContent());
System.out.println("Model: " + response.getValue().getModel());
System.out.println("Usage:");
System.out.println("\tPrompt tokens: " + response.getValue().getUsage().getPromptTokens());
System.out.println("\tTotal tokens: " + response.getValue().getUsage().getTotalTokens());
System.out.println("\tCompletion tokens: " + response.getValue().getUsage().getCompletionTokens());
```

Images are broken into tokens and submitted to the model for processing. When referring to images, each of those tokens is typically referred as *patches*. Each model might break down a given image on a different number of patches. Read the model card to learn the details.

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

The service can read the content from an **accessible cloud location** by passing the URL as an input.

```java
Path testFilePath = Paths.get("https://.../small-language-models-chart-example.jpg");

List<ChatMessageContentItem> contentItems = new ArrayList<>();
contentItems.add(new ChatMessageTextContentItem("Which conclusion can be extracted from the following chart?"));
contentItems.add(new ChatMessageImageContentItem(
    new ChatMessageImageUrl(testFilePath)));

List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are an AI assistant that helps people find information."));
chatMessages.add(ChatRequestUserMessage.fromContentItems(contentItems));

ChatCompletionsOptions options = new ChatCompletionsOptions(chatMessages);
options.setModel("phi-4-multimodal-instruct")

ChatCompletions response = client.complete(options);
```

## Use chat completions with audio

Some models can reason across text and audio inputs. This capability isn't available in the Azure AI Inference package for Java.
