---
title: include file
description: include file
author: mrbullwinkle
ms.author: mbullwin
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/16/2026
ms.custom: include, classic-and-new
---

Prompt caching allows you to reduce overall request latency and cost for longer prompts that have identical content at the beginning of the prompt. *"Prompt"* in this context is referring to the input you send to the model as part of your chat completions request. Rather than reprocess the same input tokens over and over again, the service is able to retain a temporary cache of processed input token computations to improve overall performance. Prompt caching has no impact on the output content returned in the model response beyond a reduction in latency and cost. For supported models, cached tokens are billed at a [discount on input token pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for Standard deployment types and up to [100% discount on input tokens](/azure/ai-foundry/openai/concepts/provisioned-throughput) for Provisioned deployment types. 

## Prompt cache retention

Caches are typically cleared within 5-10 minutes of inactivity and are always removed within one hour of the cache's last use. Prompt caches aren't shared between Azure subscriptions.

## Supported models

- Prompt caching is supported with all Azure OpenAI models GPT-4o or newer.
- Prompt caching applies to models that have chat-completion, completion, responses, or real-time operations. For models that don't have these operations, this feature isn't available.

## Extended prompt cache retention

Extended prompt cache retention is available for the following models:

- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.2`
- `gp5-5.1-codex-max`
- `gpt-5.1`
- `gpt-5.1-codex`
- `gpt-5.1-codex-mini`
- `gpt-5.1-chat`
- `gpt-5`
- `gpt-5-codex`
- `gpt-4.1`

Extended prompt cache retention keeps cached prefixes active for longer, up to a maximum of 24 hours. Extended Prompt Caching works by offloading the key/value tensors to GPU-local storage when memory is full, significantly increasing the storage capacity available for caching.

### Configure per request

If you don’t specify a retention policy, for most models the default is `in_memory`. For gpt-5.5, gpt-5.5-pro, and all future models, the default is `24h` and `in_memory` is not supported. Allowed values are `in_memory` and `24h`.

```json
{
  "model": "gpt-5.5",
  "input": "Your prompt goes here...",
  "prompt_cache_retention": "24h"
}
```

## Getting started

To take advantage of prompt caching, a request must meet both of these requirements:

- A minimum of 1,024 tokens in length.
- The first 1,024 tokens in the prompt must be identical.

Requests are routed based on a hash of the initial prefix of a prompt. The hash typically uses the first 256 tokens, though the exact length varies depending on the model.

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

If you provide the `prompt_cache_key` parameter, it's combined with the prefix hash, allowing you to influence routing and improve cache hit rates. This is especially beneficial when many requests share long, common prefixes.

If requests for the same prefix and `prompt_cache_key` combination exceed a certain rate (approximately 15 requests per minute), some may overflow and get routed to additional machines, reducing cache effectiveness.

## What is cached?

Feature support of o1-series models varies by model. For more information, see our dedicated [reasoning models guide](../how-to/reasoning.md).

Prompt caching is supported for:

| **Caching supported** | **Description** |
| --- | --- |
| **Messages** | The complete messages array: system, developer, user, and assistant content |
| **Images** | Images included in user messages, both as links or as base64-encoded data. The detail parameter must be set the same across requests. |
| **Tool use** | Both the messages array and tool definitions. |
| **Structured outputs** | Structured output schema is appended as a prefix to the system message. |

To improve the likelihood of cache hits occurring, you should structure your requests such that repetitive content occurs at the beginning of the messages array.

## Can I disable prompt caching?

Prompt caching is enabled by default for all supported models. There's no opt-out support for prompt caching.
