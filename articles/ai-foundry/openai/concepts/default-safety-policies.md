---
title: Default guardrail policies for Azure OpenAI
titleSuffix: Azure OpenAI
description: Learn about the default guardrail policies that Azure OpenAI uses to flag content and ensure responsible use of the service.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 11/06/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.custom:
  - build-2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Default guardrail policies for Azure OpenAI

[!INCLUDE [version-banner](../../includes/version-banner.md)]

::: moniker range="foundry"

Azure OpenAI in Microsoft Foundry Models includes default safety policies applied to all models (excluding Azure OpenAI Whisper). These configurations provide you with a responsible experience by default, including [content filtering models](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new), blocklists, prompt transformation, [content credentials](/azure/ai-foundry/openai/concepts/content-credentials), and other features.

Default safety aims to mitigate risks in different categories such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more about guardrail and controls, visit our documentation describing [categories and severity levels](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new).

All safety policies are configurable. To learn more about configurability, see the documentation on [configuring guardrails](/azure/ai-foundry/openai/how-to/content-filters).

When content is detected that exceeds the severity threshold for a risk category, the API request is blocked and returns an error response indicating which category triggered the filter. This applies to both user prompts (input) and model completions (output).

## Prerequisites

- An Azure subscription with access to Azure OpenAI Service
- Deployed Azure OpenAI models (excluding Whisper, which uses different safety configurations)

::: moniker-end

::: moniker range="foundry-classic"

Azure OpenAI in Foundry Models includes default safety policies applied to all models (excluding Azure OpenAI Whisper). These configurations provide you with a responsible experience by default, including [content filtering models](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new), blocklists, prompt transformation, [content credentials](/azure/ai-foundry/openai/concepts/content-credentials), and other features.

Default safety aims to mitigate risks in different categories such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more about content filtering, visit our documentation describing [categories and severity levels](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new).

All safety policies are configurable. To learn more about configurability, see the documentation on [configuring content filtering](/azure/ai-foundry/openai/how-to/content-filters).

::: moniker-end

## Text models

Text models in the Azure OpenAI can take in and generate both text and code. These models leverage Azure’s text content filters to detect and prevent harmful content. This system works on both prompts and completions. 

| Risk Category     | Prompt/Completion | Severity Threshold |
|-------------------------------------------|------------------------|---------------------|
| Hate and Fairness | Prompts and Completions| Medium    |
| Violence     | Prompts and Completions| Medium    |
| Sexual  | Prompts and Completions| Medium    |
| Self-Harm    | Prompts and Completions| Medium    |
| User prompt injection attack (Jailbreak)  | Prompts | N/A  |
| Protected Material – Text  | Completions  | N/A  |
| Protected Material – Code  | Completions  | N/A  |



## Vision models

### Vision-enabled chat models

| Risk Category  | Prompt/Completion | Severity Threshold |
|------------------------------------------------------|------------------------|---------------------|
| Hate and Fairness  | Prompts and Completions| Medium    |
| Violence  | Prompts and Completions| Medium    |
| Sexual    | Prompts and Completions| Medium    |
| Self-Harm | Prompts and Completions| Medium    |
| Identification of Individuals and Inference of Sensitive Attributes | Prompts | N/A  |
| User prompt injection attack (Jailbreak)   | Prompts | N/A  |

### Image generation models

#### [GPT-image-1 series](#tab/gpt-image-1)

| Risk Category   | Prompt/Completion | Severity Threshold |
|---------------------------------------------------|------------------------|---------------------|
| Hate and Fairness    | Prompts and Completions| Medium  |
| Violence    | Prompts and Completions| Medium  |
| Sexual | Prompts and Completions| Medium  |
| Self-Harm   | Prompts and Completions| Medium  |
| Content Credentials  | Completions  | N/A  |
| Deceptive Generation of Political Candidates | Prompts | N/A  |
| Depictions of Public Figures   | Prompts | N/A  |
| User prompt injection attack (Jailbreak)     | Prompts | N/A  |
| Protected Material – Art and Studio Characters    | Prompts | N/A  |
| Profanity   | Prompts | N/A  |

#### [DALL-E](#tab/dalle)

| Risk Category   | Prompt/Completion | Severity Threshold |
|---------------------------------------------------|------------------------|---------------------|
| Hate and Fairness    | Prompts and Completions| Low  |
| Violence    | Prompts and Completions| Low  |
| Sexual | Prompts and Completions| Low  |
| Self-Harm   | Prompts and Completions| Low  |
| Content Credentials  | Completions  | N/A  |
| Deceptive Generation of Political Candidates | Prompts | N/A  |
| Depictions of Public Figures   | Prompts | N/A  |
| User prompt injection attack (Jailbreak)     | Prompts | N/A  |
| Protected Material – Art and Studio Characters    | Prompts | N/A  |
| Profanity   | Prompts | N/A  |

In addition to the above safety configurations, DALL-E 3 also comes with [prompt transformation](./prompt-transformation.md) by default. This transformation occurs on all prompts to enhance the safety of your original prompt, specifically in the risk categories of diversity, deceptive generation of political candidates, depictions of public figures, protected material, and others. 

---


## Audio Models

| Risk Category                          | Prompt/Completion | Severity Threshold |
|----------------------------------------|--------------------|---------------------|
| Hate and Fairness                      | Prompts and Completions | Medium |
| Violence                               | Prompts and Completions | Medium |
| Sexual                                 | Prompts and Completions | Medium |
| Self-Harm                              | Prompts and Completions | Medium |
| User prompt injection attack (Jailbreak) | Prompts           | N/A   |
| Protected Material - Text              | Completions        | N/A    |
| Protected Material - Code              | Completions        | N/A    |

::: moniker range="foundry"

## Severity levels


<!--
Text and image models support Drugs as an additional classification. This category covers advice related to Drugs and depictions of recreational and non-recreational drugs.
-->

Guardrails and controls ensure that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides guardrail capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content. This article outlines the key risk categories and their descriptions to help you better understand the built-in guardrail system.


> [!NOTE]
> The text content filtering models for the hate, sexual, violence, and self-harm categories are specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.


[!INCLUDE [severity-levels text, four-level](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels image](../../../ai-services/content-safety/includes/severity-levels-image.md)]

## Testing safety policies

To verify that default safety policies are active, send a test prompt that should trigger content filtering. For example:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "[test prompt]"}]
)
```

If safety policies are active, you'll receive a content filtering response indicating which category was triggered.

## Next steps

- [Configure custom safety policies](../how-to/content-filters.md)
- [Content filtering concepts](content-filter.md)
- [Content credentials](content-credentials.md)
- [Prompt transformation for image generation](prompt-transformation.md)

::: moniker-end

