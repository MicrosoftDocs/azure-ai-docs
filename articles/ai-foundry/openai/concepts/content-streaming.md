---
title: Content Streaming in Azure OpenAI
description: Learn about content streaming options in Azure OpenAI, including default and asynchronous filtering modes, and their impact on latency and performance.
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/15/2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---


# Content streaming


This guide describes the Azure OpenAI content streaming experience and options. Customers can receive content from the API when it's generated, instead of waiting for chunks of content that have been verified to pass the content filters.


> [!NOTE]
> Asynchronous Filter configuration requires permission to modify content filtering policies in Foundry portal.

## Choose the right streaming mode

**Use Default streaming when:**
- Maximum safety and compliance are required
- You need immediate filtering before any content is displayed
- Your application cannot handle retroactive content removal
- Example: Customer-facing chatbots in regulated industries

**Use Asynchronous Filter when:**
- Low latency is critical to user experience
- You can implement client-side content redaction
- Your application has additional safety controls
- You're willing to handle delayed filtering signals
- Example: Internal development tools, creative writing assistants

## Default filtering behavior

::: moniker range="foundry"

The content guardrails system is integrated and enabled by default for all customers. In the default streaming scenario, completion content buffers, the content guardrail system runs on the buffered content, and – depending on the guardrail configuration – content is returned to the user if it doesn't violate the guardrail policy (Microsoft's default or a custom user configuration), or it is immediately blocked and a guardrail error is returned instead. This process repeats until the end of the stream. Content is fully vetted according to the guardrail policy before it's returned to the user. Content isn't returned token-by-token in this case, but in "content chunks" of the respective buffer size.

::: moniker-end

::: moniker range="foundry-classic"

The content filtering system is integrated and enabled by default for all customers. In the default streaming scenario, completion content buffers, the content filtering system runs on the buffered content, and – depending on the content filtering configuration – content is returned to the user if it doesn't violate the content filtering policy (Microsoft's default or a custom user configuration), or it is immediately blocked and a content filtering error is returned instead. This process repeats until the end of the stream. Content is fully vetted according to the content filtering policy before it's returned to the user. Content isn't returned token-by-token in this case, but in "content chunks" of the respective buffer size.

::: moniker-end

## Asynchronous filtering

Customers can choose the Asynchronous Filter as an extra option, providing a new streaming experience. In this case, content filters run asynchronously, and completion content returns immediately with a smooth token-by-token streaming experience. No content is buffered, which allows for a fast streaming experience with zero latency associated with content filtering.

Customers must understand that while the feature improves latency, it's a trade-off against the safety and real-time vetting of smaller sections of model output. Because content filters are run asynchronously, content moderation messages and policy violation signals are delayed, which means some sections of harmful content that would otherwise have been filtered immediately could be displayed to the user.
 
**Annotations**: Annotations and content moderation messages are continuously returned during the stream. We strongly recommend you consume annotations in your app and implement other AI Guidelines & control mechanisms, such as redacting content or returning other safety information to the user.

**Content filtering signal**: The content filtering error signal is delayed. If there is a policy violation, it’s returned as soon as it’s available, and the stream stops. The content filtering signal is guaranteed within a ~1,000-character window of the policy-violating content. 

**Customer Copyright Commitment**: Content that is retroactively flagged as protected material might not be eligible for Customer Copyright Commitment coverage. 

### Cost considerations

> [!IMPORTANT]
> **Billing for content filtering in streaming**
> 
> When content filtering is triggered during streaming, charges apply for both prompt and completion tokens:
> - **Status 400 (prompt filtered)**: Charged for prompt evaluation
> - **Status 200 with finish_reason: "content_filter"**: Charged for both prompt and completion tokens generated before filtering
> 
> This applies to both Default and Asynchronous Filter modes. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for details.

To enable Asynchronous Filter in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), follow the [Content filter how-to guide](../how-to/content-filters.md) to create a new content filtering configuration, and select **Asynchronous Filter** in the Streaming section.

> [!NOTE]
> Asynchronous Filter is available in API version **2024-02-01 and later**. Use the OpenAI Python SDK v1.0+ or Azure OpenAI SDK with compatible API versions.

## Comparison of content filtering modes

| Compare | Streaming - Default | Streaming - Asynchronous Filter |
|---|---|---|
|Status |GA | GA |
| Eligibility |All customers |All customers |
| How to enable | Enabled by default, no action needed |Customers can configure it directly in [Foundry portal](https://ai.azure.com/?cid=learnDocs) (as part of a content filtering configuration, applied at the deployment level) |
|Modality and availability |Text; all GPT models |Text; all GPT models |
|Streaming experience |Content is buffered and returned in chunks |Zero latency (no buffering, filters run asynchronously) |
|Content filtering signal |Immediate filtering signal |Delayed filtering signal (in up to ~1,000-character increments) |
|Content filtering configurations |Supports default and any customer-defined filter setting (including optional models) |Supports default and any customer-defined filter setting (including optional models) |

## Annotations and sample responses

### Prompt annotation message

This message is the same as default annotations.

```json
data: { 
    "id": "", 
    "object": "", 
    "created": 0, 
    "model": "", 
    "prompt_filter_results": [ 
        { 
            "prompt_index": 0, 
            "content_filter_results": { ... } 
        } 
    ], 
    "choices": [], 
    "usage": null 
} 
```

### Completion token message

Completion messages are forwarded immediately. The service doesn't perform moderation or provide annotations initially. 

```json
data: { 
    "id": "chatcmpl-7rAJvsS1QQCDuZYDDdQuMJVMV3x3N", 
    "object": "chat.completion.chunk", 
    "created": 1692905411, 
    "model": "gpt-35-turbo", 
    "choices": [ 
        { 
            "index": 0, 
            "finish_reason": null, 
            "delta": { 
                "content": "Color" 
            } 
        } 
    ], 
    "usage": null 
} 
```

### Annotation message

The text field is always an empty string, indicating no new tokens. Annotations only apply to tokens that are already sent. Multiple annotation messages can refer to the same tokens.  

`"start_offset"` and `"end_offset"` are low-granularity offsets in text (with 0 at the beginning of the prompt) that mark which text the annotation applies to. 

`"check_offset"` shows how much text is fully moderated. It's an exclusive lower bound on the `"end_offset"` values of future annotations. It never decreases.

```json
data: { 
    "id": "", 
    "object": "", 
    "created": 0, 
    "model": "", 
    "choices": [ 
        { 
            "index": 0, 
            "finish_reason": null, 
            "content_filter_results": { ... }, 
            "content_filter_raw": [ ... ], 
            "content_filter_offsets": { 
                "check_offset": 44, 
                "start_offset": 44, 
                "end_offset": 198 
            } 
        } 
    ], 
    "usage": null 
} 
```

**Key fields explained:**

- `check_offset`: Character position up to which content has been fully moderated (never decreases)
- `start_offset`: Beginning character position where this annotation batch starts
- `end_offset`: Ending character position where this annotation batch ends

All offsets count from 0 at the beginning of the original prompt text.

### Sample response stream (passes filters)

The following example shows a real chat completion response that uses Asynchronous Filter. The prompt annotations don't change, completion tokens are sent without annotations, and new annotation messages are sent without tokens. Instead, these new annotation messages link to certain content filter offsets. 

`{"temperature": 0, "frequency_penalty": 0, "presence_penalty": 1.0, "top_p": 1.0, "max_tokens": 800, "messages": [{"role": "user", "content": "What is color?"}], "stream": true}`

```
data: {"id":"","object":"","created":0,"model":"","prompt_annotations":[{"prompt_index":0,"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}}}],"choices":[],"usage":null} 

data: {"id":"chatcmpl-7rCNsVeZy0PGnX3H6jK8STps5nZUY","object":"chat.completion.chunk","created":1692913344,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"role":"assistant"}}],"usage":null} 

data: {"id":"chatcmpl-7rCNsVeZy0PGnX3H6jK8STps5nZUY","object":"chat.completion.chunk","created":1692913344,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":"Color"}}],"usage":null} 

data: {"id":"chatcmpl-7rCNsVeZy0PGnX3H6jK8STps5nZUY","object":"chat.completion.chunk","created":1692913344,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":" is"}}],"usage":null} 

data: {"id":"chatcmpl-7rCNsVeZy0PGnX3H6jK8STps5nZUY","object":"chat.completion.chunk","created":1692913344,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":" a"}}],"usage":null} 

... 

data: {"id":"","object":"","created":0,"model":"","choices":[{"index":0,"finish_reason":null,"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"content_filter_offsets":{"check_offset":44,"start_offset":44,"end_offset":198}}],"usage":null} 

... 

data: {"id":"chatcmpl-7rCNsVeZy0PGnX3H6jK8STps5nZUY","object":"chat.completion.chunk","created":1692913344,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":"stop","delta":{}}],"usage":null} 

data: {"id":"","object":"","created":0,"model":"","choices":[{"index":0,"finish_reason":null,"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"content_filter_offsets":{"check_offset":506,"start_offset":44,"end_offset":571}}],"usage":null} 

data: [DONE] 
```

### Sample response stream (blocked by filters)

`{"temperature": 0, "frequency_penalty": 0, "presence_penalty": 1.0, "top_p": 1.0, "max_tokens": 800, "messages": [{"role": "user", "content": "Tell me the lyrics to \"Hey Jude\"."}], "stream": true}`

```
data: {"id":"","object":"","created":0,"model":"","prompt_filter_results":[{"prompt_index":0,"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}}}],"choices":[],"usage":null} 

data: {"id":"chatcmpl-8JCbt5d4luUIhYCI7YH4dQK7hnHx2","object":"chat.completion.chunk","created":1699587397,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"role":"assistant"}}],"usage":null} 

data: {"id":"chatcmpl-8JCbt5d4luUIhYCI7YH4dQK7hnHx2","object":"chat.completion.chunk","created":1699587397,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":"Hey"}}],"usage":null} 

data: {"id":"chatcmpl-8JCbt5d4luUIhYCI7YH4dQK7hnHx2","object":"chat.completion.chunk","created":1699587397,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":" Jude"}}],"usage":null} 

data: {"id":"chatcmpl-8JCbt5d4luUIhYCI7YH4dQK7hnHx2","object":"chat.completion.chunk","created":1699587397,"model":"gpt-35-turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":","}}],"usage":null} 

... 

data: {"id":"chatcmpl-8JCbt5d4luUIhYCI7YH4dQK7hnHx2","object":"chat.completion.chunk","created":1699587397,"model":"gpt-35- 

turbo","choices":[{"index":0,"finish_reason":null,"delta":{"content":" better"}}],"usage":null} 

data: {"id":"","object":"","created":0,"model":"","choices":[{"index":0,"finish_reason":null,"content_filter_results":{"hate":{"filtered":false,"severity":"safe"},"self_harm":{"filtered":false,"severity":"safe"},"sexual":{"filtered":false,"severity":"safe"},"violence":{"filtered":false,"severity":"safe"}},"content_filter_offsets":{"check_offset":65,"start_offset":65,"end_offset":1056}}],"usage":null} 

data: {"id":"","object":"","created":0,"model":"","choices":[{"index":0,"finish_reason":"content_filter","content_filter_results":{"protected_material_text":{"detected":true,"filtered":true}},"content_filter_offsets":{"check_offset":65,"start_offset":65,"end_offset":1056}}],"usage":null} 

data: [DONE] 
```

## Troubleshooting

### Stream stops with content_filter finish reason

**Symptom**: The stream ends unexpectedly with `finish_reason: "content_filter"`.

**Cause**: The content generated by the model violated the content filtering policy. In Asynchronous Filter mode, this signal may arrive after some content has already been displayed.

**Resolution**:
1. Check the `content_filter_results` in the last chunk to identify which category triggered filtering (hate, violence, sexual, self_harm, protected_material_text)
2. If using Asynchronous Filter, implement content redaction in your application to remove already-displayed content
3. Review your content filtering configuration in Foundry portal to adjust severity thresholds if appropriate
4. Consider rephrasing the prompt to avoid triggering filters

### Annotations not appearing in stream

**Symptom**: The stream completes successfully but `content_filter_results` is always empty or null.

**Cause**: Content filtering annotations may not be enabled for your deployment, or you're using an API version that doesn't support annotations.

**Resolution**:
1. Verify you're using API version 2024-02-01 or later
2. Check your content filtering configuration in Foundry portal
3. Ensure annotations are enabled for your selected filters
4. Review [Guardrail annotations documentation](content-filter-annotations.md) for configuration steps

### Delayed filtering signals in Asynchronous Filter mode

**Symptom**: Content that should be filtered appears briefly before being retroactively flagged.

**Cause**: This is expected behavior in Asynchronous Filter mode. Filtering runs asynchronously with a guaranteed signal within ~1,000 characters.

**Resolution**:
1. This is working as designed for Asynchronous Filter mode
2. Implement client-side content redaction when you receive delayed filter signals
3. Monitor `check_offset` values to track moderation progress
4. Consider using Default streaming mode if immediate filtering is required for your use case

### Understanding content_filter_offsets

**Symptom**: Unclear how to interpret `check_offset`, `start_offset`, and `end_offset` values.

**Explanation**:
- `check_offset`: Character position up to which content has been fully moderated (never decreases)
- `start_offset`: Beginning of the text range this annotation applies to
- `end_offset`: End of the text range this annotation applies to

All offsets are character positions with 0 at the beginning of the prompt.

## Next steps

- [Configure content filters](../how-to/content-filters.md) - Set up Asynchronous Filter in Foundry portal
- [Guardrail annotations reference](content-filter-annotations.md) - Detailed annotation schemas and severity levels
- [Content filtering](../../foundry-models/concepts/content-filter.md) - Understanding content safety features
