---
title: 'Prompt caching with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use prompt caching with Azure OpenAI
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 04/14/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Prompt caching

Prompt caching allows you to reduce overall request latency and cost for longer prompts that have identical content at the beginning of the prompt. *"Prompt"* in this context is referring to the input you send to the model as part of your chat completions request. Rather than reprocess the same input tokens over and over again, the service is able to retain a temporary cache of processed input token computations to improve overall performance. Prompt caching has no impact on the output content returned in the model response beyond a reduction in latency and cost. For supported models, cached tokens are billed at a [discount on input token pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for Standard deployment types and up to [100% discount on input tokens](/azure/ai-services/openai/concepts/provisioned-throughput) for Provisioned deployment types.

Caches are typically cleared within 5-10 minutes of inactivity and are always removed within one hour of the cache's last use. Prompt caches are not shared between Azure subscriptions. 

## Supported models

Currently only the following models support prompt caching with Azure OpenAI:

- `o3-mini-2025-01-31`
- `o1-2024-12-17`
- `o1-preview-2024-09-12`
- `o1-mini-2024-09-12`
- `gpt-4o-2024-11-20`
- `gpt-4o-2024-08-06`
- `gpt-4o-mini-2024-07-18`
- `gpt-4o-realtime-preview` (version 2024-12-17)
- `gpt-4o-mini-realtime-preview` (version 2024-12-17)
- `gpt-4.1-2025-04-14`
- `gpt-4.1-nano-2025-04-14`

> [!NOTE]
> Prompt caching is now also available as part of model fine-tuning for `gpt-4o` and `gpt-4o-mini`. Refer to the fine-tuning section of the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for details.

## API support

Official support for prompt caching was first added in API version `2024-10-01-preview`. At this time, only the o-series model family supports the `cached_tokens` API response parameter.

## Getting started

For a request to take advantage of prompt caching the request must be both:

- A minimum of 1,024 tokens in length.
- The first 1,024 tokens in the prompt must be identical.

When a match is found between the token computations in a prompt and the current content of the prompt cache, it's referred to as a cache hit. Cache hits will show up as [`cached_tokens`](/azure/ai-services/openai/reference-preview#cached_tokens) under [`prompt_tokens_details`](/azure/ai-services/openai/reference-preview#properties-for-prompt_tokens_details) in the chat completions response.

```json
{
  "created": 1729227448,
  "model": "o1-2024-12-17",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_50cdd5dc04",
  "usage": {
    "completion_tokens": 1518,
    "prompt_tokens": 1566,
    "total_tokens": 3084,
    "completion_tokens_details": {
      "audio_tokens": null,
      "reasoning_tokens": 576
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 1408
    }
  }
}
```

After the first 1,024 tokens cache hits will occur for every 128 additional identical tokens.

A single character difference in the first 1,024 tokens will result in a cache miss which is characterized by a `cached_tokens` value of 0. Prompt caching is enabled by default with no additional configuration needed for supported models.

## What is cached?

o1-series models feature support varies by model. For more details, see our dedicated [reasoning models guide](./reasoning.md). 

Prompt caching is supported for:

|**Caching supported**|**Description**|**Supported models**|
|--------|--------|--------|
| **Messages** | The complete messages array: system, developer, user, and assistant content | `gpt-4o`<br/>`gpt-4o-mini`<br/>`gpt-4o-realtime-preview` (version 2024-12-17)<br/>`gpt-4o-mini-realtime-preview` (version 2024-12-17)<br> `o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |
| **Images** | Images included in user messages, both as links or as base64-encoded data. The detail parameter must be set the same across requests. | `gpt-4o`<br/>`gpt-4o-mini` <br> `o1` (version 2024-12-17)  |
| **Tool use** | Both the messages array and tool definitions. | `gpt-4o`<br/>`gpt-4o-mini`<br/>`gpt-4o-realtime-preview` (version 2024-12-17)<br/>`gpt-4o-mini-realtime-preview` (version 2024-12-17)<br> `o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |
| **Structured outputs** | Structured output schema is appended as a prefix to the system message. | `gpt-4o`<br/>`gpt-4o-mini` <br> `o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |

To improve the likelihood of cache hits occurring, you should structure your requests such that repetitive content occurs at the beginning of the messages array.

## Can I disable prompt caching?

Prompt caching is enabled by default for all supported models. There is no opt-out support for prompt caching.
