---
title: Content Filter Streaming in Azure OpenAI
description: Learn about content filter streaming options in Azure OpenAI, including default and asynchronous filtering modes, and their impact on latency and content safety.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.topic: conceptual
ms.date: 05/07/2025
ms.author: pafarley
---


# Content filter streaming

This section describes the Azure OpenAI content streaming experience and options. Customers can receive content from the API as it's generated, instead of waiting for chunks of content that have been verified to pass your content filters.

## Default

The content filtering system is integrated and enabled by default for all customers. In the default streaming scenario, completion content is buffered, the content filtering system runs on the buffered content, and – depending on the content filtering configuration – content is either returned to the user if it doesn't violate the content filtering policy (Microsoft's default or a custom user configuration), or it’s immediately blocked and returns a content filtering error, without returning the harmful completion content. This process is repeated until the end of the stream. Content is fully vetted according to the content filtering policy before it's returned to the user. Content isn't returned token-by-token in this case, but in “content chunks” of the respective buffer size.

## Asynchronous Filter

Customers can choose the Asynchronous Filter as an extra option, providing a new streaming experience. In this case, content filters are run asynchronously, and completion content is returned immediately with a smooth token-by-token streaming experience. No content is buffered, which allows for a fast streaming experience with zero latency associated with content safety.

Customers must understand that while the feature improves latency, it's a trade-off against the safety and real-time vetting of smaller sections of model output. Because content filters are run asynchronously, content moderation messages and policy violation signals are delayed, which means some sections of harmful content that would otherwise have been filtered immediately could be displayed to the user.
 
**Annotations**: Annotations and content moderation messages are continuously returned during the stream. We strongly recommend you consume annotations in your app and implement other AI content safety mechanisms, such as redacting content or returning other safety information to the user.

**Content filtering signal**: The content filtering error signal is delayed. If there is a policy violation, it’s returned as soon as it’s available, and the stream is stopped. The content filtering signal is guaranteed within a ~1,000-character window of the policy-violating content. 

**Customer Copyright Commitment**: Content that is retroactively flagged as protected material may not be eligible for Customer Copyright Commitment coverage. 

To enable Asynchronous Filter in [Azure AI Foundry portal](https://ai.azure.com/), follow the [Content filter how-to guide](/azure/ai-services/openai/how-to/content-filters) to create a new content filtering configuration, and select **Asynchronous Filter** in the Streaming section.

## Comparison of content filtering modes

| Compare | Streaming - Default | Streaming - Asynchronous Filter |
|---|---|---|
|Status |GA |Public Preview |
| Eligibility |All customers |Customers approved for modified content filtering |
| How to enable | Enabled by default, no action needed |Customers approved for modified content filtering can configure it directly in [Azure AI Foundry portal](https://ai.azure.com/) (as part of a content filtering configuration, applied at the deployment level) |
|Modality and availability |Text; all GPT models |Text; all GPT models |
|Streaming experience |Content is buffered and returned in chunks |Zero latency (no buffering, filters run asynchronously) |
|Content filtering signal |Immediate filtering signal |Delayed filtering signal (in up to ~1,000-character increments) |
|Content filtering configurations |Supports default and any customer-defined filter setting (including optional models) |Supports default and any customer-defined filter setting (including optional models) |

## Annotations and sample responses

### Prompt annotation message

This is the same as default annotations.

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

Completion messages are forwarded immediately. No moderation is performed first, and no annotations are provided initially. 

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

The text field will always be an empty string, indicating no new tokens. Annotations will only be relevant to already-sent tokens. There may be multiple annotation messages referring to the same tokens.  

`"start_offset"` and `"end_offset"` are low-granularity offsets in text (with 0 at beginning of prompt) to mark which text the annotation is relevant to. 

`"check_offset"` represents how much text has been fully moderated. It's an exclusive lower bound on the `"end_offset"` values of future annotations. It's non-decreasing.

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

Below is a real chat completion response using Asynchronous Filter. Note how the prompt annotations aren't changed, completion tokens are sent without annotations, and new annotation messages are sent without tokens&mdash;they're instead associated with certain content filter offsets. 

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
> When content filtering is triggered for a prompt and a `"status": 400` is received as part of the response there will be a charge for this request as the prompt was evaluated by the service. Due to the asynchronous nature of the content filtering system, a charge for both the prompt and completion tokens will occur. [Charges will also occur](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) when a `"status":200` is received with `"finish_reason": "content_filter"`. In this case the prompt did not have any issues, but the completion generated by the model was detected to violate the content filtering rules which results in the completion being filtered.
