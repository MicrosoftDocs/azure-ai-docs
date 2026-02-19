---
title: Default Guardrails & controls policies for Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Learn how Microsoft Foundry Models applies default safety policies and content filtering to help ensure responsible AI usage.
author: ssalgadodev
ms.author: ssalgado
ms.reviewer: yinchang
reviewer: ychang-msft
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 12/03/2025
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to understand the default safety policies and content filtering configurations applied to Microsoft Foundry Models so that I can ensure my AI applications comply with responsible AI practices and understand what safety measures are in place by default.
---

# Default Guardrails and controls policies for Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Microsoft Foundry Models applies default safety to all models, excluding audio models such as Whisper in Azure OpenAI in Foundry Models. These configurations provide you with a responsible experience by default.

Default safety aims to mitigate risks such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more about content filtering, read about [risk categories and severity levels](content-filter.md).

This article describes the default safety configuration.

> [!TIP]
> The default configuration applies to all models. However, you can configure content filtering per model deployment as explained in [How to configure content filters](../how-to/configure-content-filters.md).

## Text models

Text models in Foundry Models can take in and generate both text and code. These models apply Azure's text content filtering models to detect and prevent harmful content. This system works on both prompt and completion. 

| Risk Category                             | Prompt/Completion      | Severity Threshold  |
|-------------------------------------------|------------------------|---------------------|
| Hate and Fairness                         | Prompts and Completions| Medium              |
| Violence                                  | Prompts and Completions| Medium              |
| Sexual                                    | Prompts and Completions| Medium              |
| Self-Harm                                 | Prompts and Completions| Medium              |
| User prompt injection attack (Jailbreak)  | Prompts                | N/A                 |
| Protected Material – Text                 | Completions            | N/A                 |
| Protected Material – Code                 | Completions            | N/A                 |

## Vision and chat with vision models

Vision models can take both text and images at the same time as part of the input. Default content filtering capabilities vary per model and provider.

### Azure OpenAI: GPT-4o and GPT-4 Turbo

| Risk Category                                                       | Prompt/Completion      | Severity Threshold |
|---------------------------------------------------------------------|------------------------|---------------------|
| Hate and Fairness                                                   | Prompts and Completions| Medium              |
| Violence                                                            | Prompts and Completions| Medium              |
| Sexual                                                              | Prompts and Completions| Medium              |
| Self-Harm                                                           | Prompts and Completions| Medium              |
| Identification of Individuals and Inference of Sensitive Attributes | Prompts                | N/A                 |
| User prompt injection attack (Jailbreak)                            | Prompts                | N/A                 |

### Azure OpenAI: DALL-E 3 and DALL-E 2

| Risk Category                                     | Prompt/Completion      | Severity Threshold |
|---------------------------------------------------|------------------------|---------------------|
| Hate and Fairness                                 | Prompts and Completions| Low                 |
| Violence                                          | Prompts and Completions| Low                 |
| Sexual                                            | Prompts and Completions| Low                 |
| Self-Harm                                         | Prompts and Completions| Low                 |
| Content Credentials                               | Completions            | N/A                 |
| Deceptive Generation of Political Candidates      | Prompts                | N/A                 |
| Depictions of Public Figures                      | Prompts                | N/A                 |
| User prompt injection attack (Jailbreak)          | Prompts                | N/A                 |
| Protected Material – Art and Studio Characters    | Prompts                | N/A                 |
| Profanity                                         | Prompts                | N/A                 |


In addition to the previous safety configurations, Azure OpenAI DALL-E also comes with [prompt transformation](../../openai/concepts/prompt-transformation.md) by default. This transformation occurs on all prompts to enhance the safety of your original prompt, specifically in the risk categories of diversity, deceptive generation of political candidates, depictions of public figures, protected material, and others. 

### Meta: Llama-3.2-11B-Vision-Instruct and Llama-3.2-90B-Vision-Instruct

Content filters apply only to text prompts and completions. Content moderation doesn't apply to images.

## Next step

* [Configure content filters in Foundry Models](../how-to/configure-content-filters.md)
