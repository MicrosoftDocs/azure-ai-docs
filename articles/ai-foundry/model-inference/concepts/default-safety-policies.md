---
title: Default Guardrails & controls policies for Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about the default Guardrails & controls policies that Azure AI Foundry Models uses to flag content.
author: PatrickFarley
ms.author: fasantia
ms.service: azure-ai-model-inference
ms.topic: conceptual 
ms.date: 1/21/2025
manager: nitinme
---

# Default Guardrails & controls policies for Azure AI Foundry Models

Azure AI Foundry Models includes default safety applied to all models, excluding Azure OpenAI Whisper. These configurations provide you with a responsible experience by default.

Default safety aims to mitigate risks such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more about content filtering, read [our documentation describing categories and severity levels](content-filter.md).

This document describes the default configuration.

> [!TIP]
> By default, all model deployments use the default configuration. However, you can configure content filtering per model deployment as explained at [Configuring content filtering](../how-to/configure-content-filters.md).

## Text models

Text models in Azure AI Foundry Models can take in and generate both text and code. These models apply Azure's text content filtering models to detect and prevent harmful content. This system works on both prompt and completion. 

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


In addition to the previous safety configurations, Azure OpenAI DALL-E also comes with [prompt transformation](../../../ai-services/openai/concepts/prompt-transformation.md) by default. This transformation occurs on all prompts to enhance the safety of your original prompt, specifically in the risk categories of diversity, deceptive generation of political candidates, depictions of public figures, protected material, and others. 

### Meta: Llama-3.2-11B-Vision-Instruct and Llama-3.2-90B-Vision-Instruct

Content filters apply only to text prompts and completions. Images aren't subject to content moderation.

### Microsoft: Phi-3.5-vision-instruct

Content filters apply only to text prompts and completions. Images aren't subject to content moderation.

## Next steps

* [Configure content filters in Azure AI Foundry Models](../how-to/configure-content-filters.md)