---
title: Content Safety in Microsoft Foundry portal overview
titleSuffix: Microsoft Foundry
description: Learn how to use Azure AI Content Safety in Microsoft Foundry portal to detect harmful user-generated and AI-generated content in applications and services.
manager: nitinme
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: overview
ms.date: 12/30/2025
ms.author: pafarley
author: PatrickFarley
---

# Content Safety in the Microsoft Foundry portal

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Azure AI Content Safety is an AI service that detects harmful user-generated and AI-generated content in applications and services. Azure AI Content Safety includes APIs that help you detect and prevent the output of harmful content. The interactive Content Safety **try it out** page in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) lets you view, explore, and try out sample code for detecting harmful content across different modalities. 

## Features

Use Azure AI Content Safety for the following scenarios: 

### Text content
- **Moderate text content**: Scans and moderates text content. It identifies and categorizes text based on different levels of severity to ensure appropriate responses. 
- **Groundedness detection**: Determines if the AI's responses are based on trusted, user-provided sources. This feature ensures that the answers are "grounded" in the intended material. Groundedness detection helps improve the reliability and factual accuracy of responses. 
- **Protected material detection for text**: Identifies protected text material, such as known song lyrics, articles, or other content. This feature ensures that the AI doesn't output this content without permission. 
- **Protected material detection for code**: Detects code segments in the model's output that match known code from public repositories. This feature helps prevent uncredited or unauthorized reproduction of source code. 
- **Prompt shields**: Provides a unified API to address "Jailbreak" and "Indirect Attacks": 
    - Jailbreak Attacks: Attempts by users to manipulate the AI into bypassing its safety protocols or ethical guidelines. Examples include prompts designed to trick the AI into giving inappropriate responses or performing tasks it was programmed to avoid. 
    - Indirect Attacks: Also known as Cross-Domain Prompt Injection Attacks. Indirect attacks involve embedding malicious prompts within documents that the AI might process. For example, if a document contains hidden instructions, the AI might inadvertently follow them, leading to unintended or unsafe outputs. 

### Image content
- **Moderate image content**: Similar to text moderation, this feature filters and assesses image content to detect inappropriate or harmful visuals. 
- **Moderate multimodal content**: Designed to handle a combination of text and images. It assesses the overall context and any potential risks across multiple types of content. 

### Custom filtering
- **Custom categories**: Allows users to define specific categories for moderating and filtering content. Tailors safety protocols to unique needs. 
- **Safety system message**: Provides a method for setting up a "System Message" to instruct the AI on desired behavior and limitations. It reinforces safety boundaries and helps prevent unwanted outputs. 

[!INCLUDE [content-safety-harm-categories](../includes/content-safety-harm-categories.md)]

## Limitations

For supported regions, rate limits, and input requirements for all features, see the [Content Safety service overview](/azure/ai-services/content-safety/overview). For supported languages, see the [Language support](/azure/ai-services/content-safety/language-support) page.


## Next step

Get started using Azure AI Content Safety in Foundry portal by following the [How-to guide](/azure/ai-services/content-safety/how-to/foundry).