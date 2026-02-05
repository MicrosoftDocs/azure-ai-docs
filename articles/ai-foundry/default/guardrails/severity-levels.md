---
title: 'Harm categories and severity levels in Microsoft Foundry'
titleSuffix: Microsoft Foundry
description: Learn about the harm categories and severity levels used by the content safety system in Microsoft Foundry to detect and filter harmful content.
manager: nitinme
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 10/30/2025
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: azure-ai-content-safety
# customer intent: As a developer, I want to understand the harm categories and severity levels in Microsoft Foundry so that I can properly handle content filtering in my applications.
---

# Harm categories and severity levels in Microsoft Foundry

Content filtering in Microsoft Foundry ensures that AI-generated outputs align with ethical guidelines and safety standards. Azure OpenAI provides content filtering capabilities to help identify and mitigate risks associated with various categories of harmful or inappropriate content.

The content safety system contains neural multiclass classification models aimed at detecting and filtering harmful content. The models cover four categories (hate, sexual, violence, and self-harm) across four severity levels (safe, low, medium, and high) for both text and image content. Content detected at the 'safe' severity level is labeled in annotations but isn't subject to filtering and isn't configurable.


> [!NOTE]
> The text content safety models for the hate, sexual, violence, and self-harm categories are specifically trained and tested on the following languages: English, German, Japanese, Spanish, French, Italian, Portuguese, and Chinese. However, the service can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.

## Harm category descriptions

The following table summarizes the harm categories supported by Foundry guardrails:

| Category | Description |
|----------|-------------|
| **Hate and Fairness** | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or identity group based on certain differentiating attributes of these groups.<br><br>This includes, but is not limited to:<br>• Race, ethnicity, nationality<br>• Gender identity groups and expression<br>• Sexual orientation<br>• Religion<br>• Personal appearance and body size<br>• Disability status<br>• Harassment and bullying |
| **Sexual** | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one's will.<br><br>This includes but is not limited to:<br>• Vulgar content<br>• Prostitution<br>• Nudity and pornography<br>• Abuse<br>• Child exploitation, child abuse, child grooming |
| **Violence** | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns and related entities.<br><br>This includes, but isn't limited to:<br>• Weapons<br>• Bullying and intimidation<br>• Terrorist and violent extremism<br>• Stalking |
| **Self-Harm** | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one's body or kill oneself.<br><br>This includes, but isn't limited to:<br>• Eating disorders<br>• Bullying and intimidation |

## Severity levels

[!INCLUDE [severity-levels-text-four](../../../ai-services/content-safety/includes/severity-levels-text-four.md)]

[!INCLUDE [severity-levels-image](../../../ai-services/content-safety/includes/severity-levels-image.md)]

## Content filtering scenarios

When the content safety system detects harmful content, you receive either an error on the API call if the prompt was deemed inappropriate, or the `finish_reason` on the response will be `content_filter` to signify that some of the completion was filtered. When building your application or system, you'll want to account for these scenarios where the content returned by the Completions API is filtered, which might result in content that is incomplete.

The behavior can be summarized in the following points:

- Prompts that are classified at a filtered category and severity level return an HTTP 400 error.
- Non-streaming completions calls don't return any content when the content is filtered. The `finish_reason` value is set to `content_filter`. In rare cases with longer responses, a partial result can be returned. In these cases, the `finish_reason` is updated.
- For streaming completions calls, segments are returned to the user as they're completed. The service continues streaming until either reaching a stop token, length, or when content that is classified at a filtered category and severity level is detected.

### Scenario 1: Non-streaming call with no filtered content

When all generations pass the filters as configured, the response doesn't include content moderation details. The `finish_reason` for each generation is either `stop` or `length`.

**HTTP Response Code:** 200

**Example request payload:**

```json
{
    "prompt": "Text example", 
    "n": 3,
    "stream": false
}
```

**Example response:**

```json
{
    "id": "example-id",
    "object": "text_completion",
    "created": 1653666286,
    "model": "davinci",
    "choices": [
        {
            "text": "Response generated text",
            "index": 0,
            "finish_reason": "stop",
            "logprobs": null
        }
    ]
}
```

### Scenario 2: Multiple responses with at least one filtered

When your API call asks for multiple responses (N>1) and at least one of the responses is filtered, the generations that are filtered have a `finish_reason` value of `content_filter`.

**HTTP Response Code:** 200

**Example request payload:**

```json
{
    "prompt": "Text example",
    "n": 3,
    "stream": false
}
```

**Example response:**

```json
{
    "id": "example",
    "object": "text_completion",
    "created": 1653666831,
    "model": "ada",
    "choices": [
        {
            "text": "returned text 1",
            "index": 0,
            "finish_reason": "length",
            "logprobs": null
        },
        {
            "text": "returned text 2",
            "index": 1,
            "finish_reason": "content_filter",
            "logprobs": null
        }
    ]
}
```

### Scenario 3: Inappropriate input prompt

The API call fails when the prompt triggers a content filter as configured. Modify the prompt and try again.

**HTTP Response Code:** 400

**Example request payload:**

```json
{
    "prompt": "Content that triggered the filtering model"
}
```

**Example response:**

```json
{
    "error": {
        "message": "The response was filtered",
        "type": null,
        "param": "prompt",
        "code": "content_filter",
        "status": 400
    }
}
```

### Scenario 4: Streaming call with no filtered content

In this case, the call streams back with the full generation and `finish_reason` is either `length` or `stop` for each generated response.

**HTTP Response Code:** 200

**Example request payload:**

```json
{
    "prompt": "Text example",
    "n": 3,
    "stream": true
}
```

**Example response:**

```json
{
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1653670914,
    "model": "ada",
    "choices": [
        {
            "text": "last part of generation",
            "index": 2,
            "finish_reason": "stop",
            "logprobs": null
        }
    ]
}
```

### Scenario 5: Streaming call with filtered content

For a given generation index, the last chunk of the generation includes a non-null `finish_reason` value. The value is `content_filter` when the generation is filtered.

**HTTP Response Code:** 200

**Example request payload:**

```json
{
    "prompt": "Text example",
    "n": 3,
    "stream": true
}
```

**Example response:**

```json
{
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1653670515,
    "model": "ada",
    "choices": [
        {
            "text": "Last part of generated text streamed back",
            "index": 2,
            "finish_reason": "content_filter",
            "logprobs": null
        }
    ]
}
```

### Scenario 6: Content filtering system unavailable

If the content filtering system is down or otherwise unable to complete the operation in time, your request still completes without content filtering. You can determine that the filtering wasn't applied by looking for an error message in the `content_filter_results` object.

**HTTP Response Code:** 200

**Example request payload:**

```json
{
    "prompt": "Text example",
    "n": 1,
    "stream": false
}
```

**Example response:**

```json
{
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1652294703,
    "model": "ada",
    "choices": [
        {
            "text": "generated text",
            "index": 0,
            "finish_reason": "length",
            "logprobs": null,
            "content_filter_results": {
                "error": {
                    "code": "content_filter_error",
                    "message": "The contents are not filtered"
                }
            }
        }
    ]
}
```

## Best practices

As part of your application design, consider the following best practices to deliver a positive experience with your application while minimizing potential harms:

- **Handle filtered content appropriately**: Decide how you want to handle scenarios where your users send prompts containing content that is classified at a filtered category and severity level or otherwise misuse your application.
- **Check finish_reason**: Always check the `finish_reason` to see if a completion is filtered.
- **Verify content filter execution**: Check that there's no error object in the `content_filter_results` (indicating that content filters didn't run).
- **Display citations for protected material**: If you're using the protected material code model in annotate mode, display the citation URL when you're displaying the code in your application.

## Severity levels

Guardrails ensure that AI-generated outputs align with ethical guidelines and safety standards. The content safety system uses four severity levels to classify harmful content:

- **Safe**: Content that doesn't contain harmful material
- **Low**: Content that contains mild harmful material
- **Medium**: Content that contains moderate harmful material  
- **High**: Content that contains severe harmful material

> [!NOTE]
> Content detected at the 'safe' severity level is labeled in annotations but isn't subject to filtering and isn't configurable.

## Next steps

- [Guardrails and controls overview](how-to-create-guardrails.md)
- [Understanding guardrail annotations](../../openai/concepts/content-filter-annotations.md)
- [Learn about content filtering in Azure OpenAI](../../openai/concepts/content-filter.md)
