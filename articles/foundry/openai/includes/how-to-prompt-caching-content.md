---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/04/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

Prompt caching reduces overall request latency and cost for longer prompts that have identical content at the beginning of the prompt. In this context, *"prompt"* refers to the input you send to the model as part of your chat completions or response creation requests. Rather than reprocessing the same input tokens over and over again, the service retains a temporary cache of processed input token computations to improve overall performance. Prompt caching has no impact on the output content returned in the model response beyond a reduction in latency and cost.

For supported models, cache reads are billed at a [discount on input token pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for Standard deployment types and up to [100% discount on input tokens](/azure/ai-foundry/openai/concepts/provisioned-throughput) for Provisioned deployment types. Prompt cache pricing is the same for both retention policies.

> [!IMPORTANT]
> Models before the GPT-5.6 family don't charge extra to write to the cache. On GPT-5.6 models and later model families, cache writes can incur charges in addition to discounted cache reads. To keep costs predictable, structure your prompts so that reused content stays identical across requests, which favors cache reads over cache writes. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Improve cache hit rates with a prompt cache key

On GPT-5.6 models and later model families, set the `prompt_cache_key` parameter and reuse the same key for requests that share long, common prompt prefixes. This parameter improves cache matching for related requests. You don't need a specific API version to use `prompt_cache_key`. For new integrations, use the [v1 API](../api-version-lifecycle.md).

If requests for the same prefix and `prompt_cache_key` combination exceed approximately 15 requests per minute, some requests might miss the cache. For higher-volume workloads, distribute requests across multiple keys while keeping a stable mapping between each key and its shared prompt prefixes.

## Configure prompt cache breakpoints

On GPT-5.6 models and later model families, use explicit cache breakpoints to mark the end of a reusable prompt prefix. Both the Responses API and Chat Completions API support breakpoints. Content after the breakpoint can change without invalidating the cached prefix.

Standard pay-as-you-go deployments support prompt cache breakpoints. [Provisioned Throughput managed (PTU-M)](../concepts/provisioned-throughput.md) deployments don't support prompt cache breakpoints.

Set the request-wide cache policy by using `prompt_cache_options.mode`:

| **Mode** | **Behavior** |
| --- | --- |
| `implicit` | The default. Azure OpenAI places a breakpoint on the latest message and also uses any explicit breakpoints that you provide. |
| `explicit` | Azure OpenAI uses only explicit breakpoints for cache reads and writes. If the request contains no explicit breakpoints, it doesn't use prompt caching or incur cache-write charges. |

Set `prompt_cache_options.ttl` to `30m` to configure the minimum cache lifetime for all breakpoints in the request. The `30m` value is the default and the only supported value. This setting doesn't select the in-memory or extended retention policy.

Add `prompt_cache_breakpoint: { "mode": "explicit" }` to a supported prompt content block. The breakpoint includes the block and all prompt content before it in the reusable prefix.

- The Responses API supports breakpoints on `input_text`, `input_image`, and `input_file` blocks.
- The Chat Completions API supports breakpoints on `text`, `image_url`, `input_audio`, and `file` blocks.

### Breakpoint limits

- Each request can create up to four new cache writes.
- In `implicit` mode, the breakpoint on the latest message uses one write slot, so the request can write up to the latest three explicit breakpoints.
- In `explicit` mode, the request can write up to the latest four explicit breakpoints.
- Breakpoints from earlier conversation turns are read-only. They can match the cache, but the request doesn't write them again.
- For cache reads, Azure OpenAI considers up to the latest 50 breakpoints in the conversation.

The following Responses API request marks the end of reusable developer instructions:

```json
{
  "model": "<your-gpt-5.6-deployment>",
  "prompt_cache_key": "support-assistant-v1",
  "prompt_cache_options": { "mode": "explicit", "ttl": "30m" },
  "input": [
    {
      "type": "message",
      "role": "developer",
      "content": [{
        "type": "input_text",
        "text": "<at least 1,024 tokens of reusable instructions>",
        "prompt_cache_breakpoint": { "mode": "explicit" }
      }]
    },
    {
      "type": "message",
      "role": "user",
      "content": "<variable user input>"
    }
  ]
}
```

The following Chat Completions API request marks the end of a reusable system message:

```json
{
  "model": "<your-gpt-5.6-deployment>",
  "prompt_cache_key": "support-assistant-v1",
  "prompt_cache_options": { "mode": "explicit", "ttl": "30m" },
  "messages": [
    {
      "role": "system",
      "content": [{
        "type": "text",
        "text": "<at least 1,024 tokens of reusable instructions>",
        "prompt_cache_breakpoint": { "mode": "explicit" }
      }]
    },
    {
      "role": "user",
      "content": "<variable user input>"
    }
  ]
}
```

> [!NOTE]
> Models before the GPT-5.6 family don't support `prompt_cache_options` or `prompt_cache_breakpoint`. Requests that include these parameters return a `400` error. Continue to use automatic prompt caching with these models.

## Prompt cache retention

Prompt caching has two controls with different semantics:

- On GPT-5.6 models and later model families, `prompt_cache_options.ttl` sets a minimum cache lifetime. It doesn't select a storage policy or maximum retention period.
- For earlier models, `prompt_cache_retention` selects a maximum-retention policy. On GPT-5.6 models and later model families, this field doesn't apply and is deprecated.

On GPT-5.6 models and later model families, use `prompt_cache_options.ttl` to set the minimum lifetime of all breakpoints written by the request. The only supported value is `30m`, which is also the default. A cached prefix remains eligible for reuse for at least 30 minutes, but the service might retain it longer.

For models before the GPT-5.6 family, set `prompt_cache_retention` on your Responses or Chat Completions request. Prompt caching can use either in-memory or extended retention policies. When available, extended prompt caching aims to retain the cache for longer, so that subsequent requests are more likely to match the cache. Prompt cache pricing is the same for both policies.

### In-memory prompt cache retention

The system typically clears caches within 5 to 10 minutes of inactivity and always removes them within one hour of the cache's last use. The system doesn't share prompt caches between Azure subscriptions.

All Azure OpenAI models GPT-4o or newer support in-memory prompt cache retention. It applies to models that have chat-completion, completion, responses, or real-time operations. For models that don't have these operations, this feature isn't available.

### Extended prompt cache retention

Extended prompt cache retention keeps cached prefixes active for longer, up to a maximum of 24 hours. Extended prompt caching works by offloading the key/value tensors to GPU-local storage when memory is full, which significantly increases the storage capacity available for caching.

Extended prompt cache retention is available for the following models:

- `gpt-5.5`
- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.2`
- `gpt-5.1-codex-max`
- `gpt-5.1`
- `gpt-5.1-codex`
- `gpt-5.1-codex-mini`
- `gpt-5.1-chat`
- `gpt-5`
- `gpt-5-codex`
- `gpt-4.1`

### Configure per request

For `gpt-5.4` and older models, if you don't specify a retention policy, the default is `in_memory`. Allowed values are `in_memory` and `24h`. For `gpt-5.5`, extended retention is enabled by default.

```json
{
  "model": "gpt-5.4",
  "input": "Your prompt goes here...",
  "prompt_cache_retention": "24h"
}
```

## Getting started

To take advantage of prompt caching, a request must meet both of these requirements:

- A minimum of 1,024 tokens in length.
- The first 1,024 tokens in the prompt must be identical.

When a match is found between the token computations in a prompt and the current content of the prompt cache, it's referred to as a cache hit. Cache hits show up as [`cached_tokens`](/rest/api/microsoft-foundry/azureopenai/chat?view=rest-microsoft-foundry-2025-04-01-preview&preserve-view=true) under [`prompt_tokens_details`](/rest/api/microsoft-foundry/azureopenai/chat?view=rest-microsoft-foundry-2025-04-01-preview&preserve-view=true) in the chat completions response.

On GPT-5.6 models and later model families, Standard pay-as-you-go deployments report cache reads in `cached_tokens` and cache writes in `cache_write_tokens`.

```json
{
  "created": 1729227448,
  "model": "<your-gpt-5.6-deployment>",
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
      "cached_tokens": 1408,
      "cache_write_tokens": 0
    }
  }
}
```

After the first 1,024 tokens, cache hits occur for every 128 additional identical tokens.

A single character difference in the first 1,024 tokens results in a cache miss, which is characterized by a `cached_tokens` value of 0. Prompt caching is enabled by default for supported models.

## Best practices

- Place stable or repeated content at the beginning of the prompt and dynamic content at the end. Keep conversation context append-only.
- Reuse a consistent `prompt_cache_key` for requests that share a prefix. For high-volume workloads, partition traffic across keys while keeping a stable mapping between each key and its prefixes.
- On Standard pay-as-you-go deployments with GPT-5.6 models and later model families, place explicit breakpoints after stable content. Use `explicit` mode when you want only the breakpoints you provide to be eligible for cache reads and writes.
- Monitor cache reads with `cached_tokens`. On Standard pay-as-you-go deployments with GPT-5.6 models and later model families, also monitor cache writes with `cache_write_tokens` and compare write volume with later cache reads.
- Maintain a steady stream of requests with identical prefixes to improve cache reuse.

## Frequently asked questions

The following answers clarify supported cache content, costs, deployment types, and data residency.

### What is cached?

Feature support for o1-series models varies by model. For more information, see the dedicated [reasoning models guide](../how-to/reasoning.md).

Prompt caching supports:

| **Caching supported** | **Description** |
| --- | --- |
| **Messages** | The complete messages array: system, developer, user, and assistant content |
| **Images** | Images included in user messages, both as links or as base64-encoded data. The detail parameter must be set the same across requests. |
| **Tool use** | Both the messages array and tool definitions. |
| **Structured outputs** | Structured output schema is appended as a prefix to the system message. |

To improve the likelihood of cache hits, structure your requests so that repetitive content occurs at the beginning of the messages array.

### Can I disable prompt caching?

On Standard pay-as-you-go deployments with GPT-5.6 models and later model families, set `prompt_cache_options.mode` to `explicit` and don't add any explicit breakpoints. The request doesn't use prompt caching or incur cache-write charges. Earlier models and PTU-M deployments don't support this option; prompt caching remains enabled by default.

### Do I pay extra to write to the cache?

On models before the GPT-5.6 family, there's no extra charge to write to the cache. On GPT-5.6 models and later model families, cache writes can incur charges in addition to discounted cache reads. To see current rates, go to the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

### Do prompt cache breakpoints work with PTU-M?

On GPT-5.6 models and later model families, Standard pay-as-you-go deployments support prompt cache breakpoints and expose `cache_write_tokens`. [Provisioned Throughput managed (PTU-M)](../concepts/provisioned-throughput.md) deployments continue to support prompt caching, but they don't support prompt cache breakpoints or expose `cache_write_tokens`.

### Does prompt caching work with data residency?

In-memory prompt caching is compatible with all data residency regions. Extended prompt caching temporarily stores data on GPU machines. Data stays within the data zone boundary for Data Zone Standard and Data Zone Provisioned deployment types, and within the regional boundary for Regional Standard and Regional Provisioned deployment types.

## Related content

- [Azure OpenAI Responses API reference](/rest/api/microsoft-foundry/azureopenai/responses?view=rest-microsoft-foundry-v1&preserve-view=true#create-response)
- [Azure OpenAI Chat Completions API reference](/rest/api/microsoft-foundry/azureopenai/chat?view=rest-microsoft-foundry-v1&preserve-view=true#create-chat-completion)

