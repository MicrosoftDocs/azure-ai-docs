---
title: 'Prompt caching with Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to use prompt caching with Azure OpenAI
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 09/15/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Prompt caching

Prompt caching allows you to reduce overall request latency and cost for longer prompts that have identical content at the beginning of the prompt. *"Prompt"* in this context is referring to the input you send to the model as part of your chat completions request. Rather than reprocess the same input tokens over and over again, the service is able to retain a temporary cache of processed input token computations to improve overall performance. Prompt caching has no impact on the output content returned in the model response beyond a reduction in latency and cost. For supported models, cached tokens are billed at a [discount on input token pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for Standard deployment types and up to [100% discount on input tokens](/azure/ai-foundry/openai/concepts/provisioned-throughput) for Provisioned deployment types. 

Caches are typically cleared within 5-10 minutes of inactivity and are always removed within one hour of the cache's last use. Prompt caches aren't shared between Azure subscriptions.

## Supported models

- Prompt caching is supported with all Azure OpenAI models GPT-4o or newer.
- Prompt caching applies to models that have chat-completion, completion, responses, or real-time operations. For models which don't have these operations, this feature isn't available.

## Getting started

For a request to take advantage of prompt caching the request must be both:

- A minimum of 1,024 tokens in length.
- The first 1,024 tokens in the prompt must be identical.

Requests are routed based on a hash of the initial prefix of a prompt.

When a match is found between the token computations in a prompt and the current content of the prompt cache, it's referred to as a cache hit. Cache hits will show up as [`cached_tokens`](/azure/ai-foundry/openai/reference-preview#cached_tokens) under [`prompt_tokens_details`](/azure/ai-foundry/openai/reference-preview#properties-for-prompt_tokens_details) in the chat completions response.

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

If you provide the [`user`](/azure/ai-foundry/openai/reference-preview-latest#request-body-2) parameter, it's combined with the prefix hash, allowing you to influence routing and improve cache hit rates. This is especially beneficial when many requests share long, common prefixes.

## What is cached?

o1-series models feature support varies by model. For more information, see our dedicated [reasoning models guide](./reasoning.md). 

Prompt caching is supported for:

|**Caching supported**|**Description**|**Supported models**|
|--------|--------|--------|
| **Messages** | The complete messages array: system, developer, user, and assistant content | `gpt-4o`<br/>`gpt-4o-mini`<br/>`gpt-4o-realtime-preview` (version 2024-12-17)<br/>`gpt-4o-mini-realtime-preview` (version 2024-12-17)<br>`gpt-realtime` (version 2025-08-28)<br> `gpt-realtime-mini` (version 2025-10-06)<br>`o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |
| **Images** | Images included in user messages, both as links or as base64-encoded data. The detail parameter must be set the same across requests. | `gpt-4o`<br/>`gpt-4o-mini` <br> `o1` (version 2024-12-17)  |
| **Tool use** | Both the messages array and tool definitions. | `gpt-4o`<br/>`gpt-4o-mini`<br/>`gpt-4o-realtime-preview` (version 2024-12-17)<br/>`gpt-4o-mini-realtime-preview` (version 2024-12-17)<br>`gpt-realtime` (version 2025-08-28)<br>`gpt-realtime-mini` (version 2025-10-06)<br> `o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |
| **Structured outputs** | Structured output schema is appended as a prefix to the system message. | `gpt-4o`<br/>`gpt-4o-mini` <br> `o1` (version 2024-12-17) <br> `o3-mini` (version 2025-01-31) |

To improve the likelihood of cache hits occurring, you should structure your requests such that repetitive content occurs at the beginning of the messages array.

## Can I disable prompt caching?

Prompt caching is enabled by default for all supported models. There's no opt-out support for prompt caching.
