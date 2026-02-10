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

To enable Asynchronous Filter in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs), follow the [Content filter how-to guide](/azure/ai-foundry/openai/how-to/content-filters) to create a new content filtering configuration, and select **Asynchronous Filter** in the Streaming section.

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

> [!IMPORTANT]
> When content filtering is triggered for a prompt and a `"status": 400` is received as part of the response there is a charge for this request as the prompt was evaluated by the service. Due to the asynchronous nature of the content filtering system, a charge for both the prompt and completion tokens occurs. [Charges will also occur](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) when a `"status":200` is received with `"finish_reason": "content_filter"`. In this case, the prompt didn't have any issues, but the completion generated by the model was detected to violate the content filtering rules, which results in the completion being filtered.
