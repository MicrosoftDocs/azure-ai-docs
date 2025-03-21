---
title: Content Safety in Azure AI Foundry portal overview
titleSuffix: Azure AI Foundry
description: Learn how to use Azure AI Content Safety in Azure AI Foundry portal to detect harmful user-generated and AI-generated content in applications and services.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: overview
ms.date: 02/20/2025
ms.author: pafarley
author: PatrickFarley
---

# Content Safety in the Azure AI Foundry portal

Azure AI Content Safety is an AI service that detects harmful user-generated and AI-generated content in applications and services. Azure AI Content Safety includes various APIs that allow you to detect and prevent the output of harmful content. The interactive Content Safety **try out** page in [Azure AI Foundry portal](https://ai.azure.com) allows you to view, explore, and try out sample code for detecting harmful content across different modalities. 

## Features

You can use Azure AI Content Safety for many scenarios: 

**Text content**: 
- Moderate text content: This feature scans and moderates text content, identifying and categorizing it based on different levels of severity to ensure appropriate responses. 
- Groundedness detection: This filter determines if the AI's responses are based on trusted, user-provided sources, ensuring that the answers are "grounded" in the intended material. Groundedness detection is helpful for improving the reliability and factual accuracy of responses. 
- Protected material detection for text: This feature identifies protected text material, such as known song lyrics, articles, or other content, ensuring that the AI doesn't output this content without permission. 
- Protected material detection for code: Detects code segments in the model's output that match known code from public repositories, helping to prevent uncredited or unauthorized reproduction of source code. 
- Prompt shields: This feature provides a unified API to address "Jailbreak" and "Indirect Attacks": 
    - Jailbreak Attacks: Attempts by users to manipulate the AI into bypassing its safety protocols or ethical guidelines. Examples include prompts designed to trick the AI into giving inappropriate responses or performing tasks it was programmed to avoid. 
    - Indirect Attacks: Also known as Cross-Domain Prompt Injection Attacks, indirect attacks involve embedding malicious prompts within documents that the AI might process. For example, if a document contains hidden instructions, the AI might inadvertently follow them, leading to unintended or unsafe outputs. 

**Image content**: 
- Moderate image content: Similar to text moderation, this feature filters and assesses image content to detect inappropriate or harmful visuals. 
- Moderate multimodal content: This is designed to handle a combination of text and images, assessing the overall context and any potential risks across multiple types of content. 

**Customize your own categories**: 
- Custom categories: Allows users to define specific categories for moderating and filtering content, tailoring safety protocols to unique needs. 
- Safety system message: Provides a method for setting up a "System Message" to instruct the AI on desired behavior and limitations, reinforcing safety boundaries and helping prevent unwanted outputs. 

[!INCLUDE [content-safety-harm-categories](../includes/content-safety-harm-categories.md)]

## Limitations

Refer to the [Content Safety overview](/azure/ai-services/content-safety/overview) for supported regions, rate limits, and input requirements for all features. Refer to the [Language support](/azure/ai-services/content-safety/language-support) page for supported languages. 


## Next step

Get started using Azure AI Content Safety in [Azure AI Foundry portal](https://ai.azure.com) by following the [How-to guide](/azure/ai-services/content-safety/how-to/foundry).