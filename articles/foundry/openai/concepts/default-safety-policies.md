---
title: "Default Guardrail policies for Azure OpenAI"
description: "Learn about the default Guardrail policies that Azure OpenAI uses to flag content and ensure responsible use of the service."
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 05/31/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: concept-article
ms.custom:
  - classic-and-new
  - build-2025
  - doc-kit-assisted
  - dev-focus
ai-usage: ai-assisted
---

# Default Guardrail policies for Azure OpenAI

Azure OpenAI in Microsoft Foundry Models includes default safety policies applied to all models (excluding Whisper models). These configurations provide you with a responsible experience by default, including [content filtering models](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new), blocklists, prompt transformation, [content credentials](/azure/ai-foundry/openai/concepts/content-credentials), and other features.

Guardrails and controls ensure that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides Guardrail capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content. Default safety aims to mitigate risks in different categories such as hate and fairness, sexual, violence, self-harm, protected material content, and user prompt injection attacks. To learn more, see [categories and severity levels](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new).

All safety policies are configurable. To learn more about configurability, see [configuring Guardrails](/azure/ai-foundry/openai/how-to/content-filters).

When content is detected that exceeds the severity threshold for a risk category, the API request is blocked and returns an error response indicating which category triggered the filter. This applies to both user prompts (input) and model completions (output).

## Prerequisites

- An Azure subscription with access to Azure OpenAI Service
- Deployed Azure OpenAI models (excluding Whisper, which uses different safety configurations)

## Text models

Text models in Azure OpenAI can take in and generate both text and code. These models leverage Azure's text content filters to detect and prevent harmful content. This system works on both prompts and completions.

| Risk category     | Prompt or completion | Severity threshold |
|-------------------------------------------|------------------------|---------------------|
| Hate and fairness | Prompts and completions| Medium    |
| Violence     | Prompts and completions| Medium    |
| Sexual  | Prompts and completions| Medium    |
| Self-harm    | Prompts and completions| Medium    |
| User prompt injection attack (jailbreak)  | Prompts | N/A  |
| Protected material – text  | Completions  | N/A  |
| Protected material – code  | Completions  | N/A  |

## Vision models

### Vision-enabled chat models

| Risk category  | Prompt or completion | Severity threshold |
|------------------------------------------------------|------------------------|---------------------|
| Hate and fairness  | Prompts and completions| Medium    |
| Violence  | Prompts and completions| Medium    |
| Sexual    | Prompts and completions| Medium    |
| Self-harm | Prompts and completions| Medium    |
| Identification of individuals and inference of sensitive attributes | Prompts | N/A  |
| User prompt injection attack (jailbreak)   | Prompts | N/A  |

### Image generation models

| Risk category   | Prompt or completion | Severity threshold |
|---------------------------------------------------|------------------------|---------------------|
| Hate and fairness    | Prompts and completions| Medium  |
| Violence    | Prompts and completions| Medium  |
| Sexual | Prompts and completions| Medium  |
| Self-harm   | Prompts and completions| Medium  |
| Content credentials  | Completions  | N/A  |
| Deceptive generation of political candidates | Prompts | N/A  |
| Depictions of public figures   | Prompts | N/A  |
| User prompt injection attack (jailbreak)     | Prompts | N/A  |
| Protected material – art and studio characters    | Prompts | N/A  |
| Profanity   | Prompts | N/A  |

## Audio models

| Risk category                          | Prompt or completion | Severity threshold |
|----------------------------------------|--------------------|---------------------|
| Hate and fairness                      | Prompts and completions | Medium |
| Violence                               | Prompts and completions | Medium |
| Sexual                                 | Prompts and completions | Medium |
| Self-harm                              | Prompts and completions | Medium |
| User prompt injection attack (jailbreak) | Prompts           | N/A   |
| Protected material - text              | Completions        | N/A    |
| Protected material - code              | Completions        | N/A    |

## Severity levels

> [!NOTE]
> The text content filtering models for the hate, sexual, violence, and self-harm categories are specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

[!INCLUDE [severity-levels text, four-level](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels image](../../../ai-services/content-safety/includes/severity-levels-image.md)]

## Testing safety policies

To verify that default safety policies are active, send a test prompt that should trigger content filtering. The following example uses the Azure OpenAI Python SDK with key-based authentication:

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],  # your deployment name
    messages=[{"role": "user", "content": "[test prompt]"}],
)

print(response.choices[0].finish_reason)
```

Replace `[test prompt]` with content that exceeds one of the configured severity thresholds. If safety policies are active and the content is filtered, the request returns an HTTP 400 error with a `content_filter` code, or the response's `finish_reason` is `content_filter` with details indicating which category was triggered.

References: [`AzureOpenAI` client](/python/api/openai/openai.azureopenai), [`chat.completions.create`](/azure/ai-foundry/openai/reference#chat-completions), [content filter response schema](/azure/ai-foundry/openai/concepts/content-filter#annotations-preview).

## Next steps

- [Configure custom safety policies](../../../foundry-classic/openai/how-to/content-filters.md)
- [Content filtering concepts](../../../foundry-classic/foundry-models/concepts/content-filter.md)
- [Content credentials](../../../foundry-classic/openai/concepts/content-credentials.md)
- [Prompt transformation for image generation](prompt-transformation.md)

