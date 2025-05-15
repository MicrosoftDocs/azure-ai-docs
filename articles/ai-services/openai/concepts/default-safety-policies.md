---
title: Azure OpenAI default Guidelines & controls policies
titleSuffix: Azure OpenAI
description: Learn about the default Guidelines & controls policies that Azure OpenAI uses to flag content and ensure responsible use of the service.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 02/20/2025
manager: nitinme
---

# Default Guidelines & controls policies


Azure OpenAI Service includes default safety policies applied to all models, excluding Azure OpenAI Whisper. These configurations provide you with a responsible experience by default, including [content filtering models](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cpython-new), blocklists, prompt transformation, [content credentials](/azure/ai-services/openai/concepts/content-credentials), and others.

Default safety aims to mitigate risks in different categories such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more about content filtering, visit our documentation describing [categories and severity levels](/azure/ai-services/openai/concepts/content-filter?tabs=warning%2Cpython-new).

All safety policies are configurable. To learn more about configurability, see the documentation on [configuring content filtering](/azure/ai-services/openai/how-to/content-filters).

## Text models

Text models in the Azure OpenAI Service can take in and generate both text and code. These models leverage Azure’s text content filters to detect and prevent harmful content. This system works on both prompts and completions. 

| Risk Category                             | Prompt/Completion      | Severity Threshold |
|-------------------------------------------|------------------------|---------------------|
| Hate and Fairness                         | Prompts and Completions| Medium              |
| Violence                                  | Prompts and Completions| Medium              |
| Sexual                                    | Prompts and Completions| Medium              |
| Self-Harm                                 | Prompts and Completions| Medium              |
| User prompt injection attack (Jailbreak)  | Prompts                | N/A                 |
| Protected Material – Text                 | Completions            | N/A                 |
| Protected Material – Code                 | Completions            | N/A                 |



## Vision models

### Vision-enabled chat models

| Risk Category                                        | Prompt/Completion      | Severity Threshold |
|------------------------------------------------------|------------------------|---------------------|
| Hate and Fairness                                    | Prompts and Completions| Medium              |
| Violence                                             | Prompts and Completions| Medium              |
| Sexual                                               | Prompts and Completions| Medium              |
| Self-Harm                                            | Prompts and Completions| Medium              |
| Identification of Individuals and Inference of Sensitive Attributes | Prompts                | N/A                 |
| User prompt injection attack (Jailbreak)             | Prompts                | N/A                 |

### Image generation models


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


In addition to the above safety configurations, the latest image generation models also come with [prompt transformation](./prompt-transformation.md) by default. This transformation occurs on all prompts to enhance the safety of your original prompt, specifically in the risk categories of diversity, deceptive generation of political candidates, depictions of public figures, protected material, and others. 