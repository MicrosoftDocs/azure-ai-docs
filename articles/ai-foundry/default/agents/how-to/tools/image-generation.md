---
title: 'How to use Azure AI Foundry Agent Service with image generation'
titleSuffix: Azure AI Foundry
description: Learn how to use Azure AI Agents with image generation.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 10/29/2025
author: aahill
ms.author: aahi
---


# Image generation tool (preview) 

>[!IMPORTANT] 
> The Image Generation tool is powered by the `gpt-image-1` model.  Learn more about intended uses, capabilities, limitations, risks, and considerations when choosing a use case model in the [Azure OpenAI transparency note](/azure/ai-foundry/responsible-ai/openai/transparency-note?tabs=image). 

The Azure AI Foundry Agent Service enables image generation as part of conversations and multi-step workflows. It supports image inputs and outputs within context and includes built-in tools for generating and editing images. 

## When to use the image generation tool

Compared to Azure OpenAI's Image API, the image generation tool in Azure AI Foundry Agent Service offers several advantages: 

**Streaming**: Display partial image outputs during generation to improve perceived latency. 

**Flexible inputs**: Accept image file IDs as inputs, in addition to raw image bytes. 

> [!NOTE]
> * The image generation tool only supported by the `gpt-image-1` model. You can however call this model from the following supported models: gpt-4o, gpt-4o-mini, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, o3. 
> * The Image Generation tool can be used with the following tools: [function calling](./function-calling.md), [code interpreter](./code-interpreter.md), [file search](./file-search.md), computer use, and [MCP server](./model-context-protocol.md).

Use the Responses API if you want to: 

* Build conversational image experiences with GPT Image. 
* Stream partial image results during generation for a smoother user experience. 

## Best practices for writing text-to-image prompts  

Your prompts should describe the content you want to see in the image, and the visual style of image. You can use terms like "draw" or "edit" in your prompt. 

When you write prompts, consider that the Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filter](../../../openai/concepts/content-filter.md). 

> [!TIP] 
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see [Image prompt engineering techniques](../../../../openai/concepts/gpt-4-v-prompt-engineering.md). 
