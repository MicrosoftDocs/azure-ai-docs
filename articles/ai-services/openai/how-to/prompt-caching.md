---
title: 'Prompt caching with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use prompt caching with Azure OpenAI
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 10/18/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Prompt caching

Prompt caching allows you to reduce overall request latency and cost for longer prompts that have identical content at the beginning of the prompt. *"Prompt"* in this context is referring to the input you send to the model as part of your chat completions request. Rather than reprocess the same input tokens over and over again, the model is able to retain a temporary cache of processed input data to improve overall performance. Prompt caching has no impact on the output content returned in the model response beyond a reduction in latency and cost.  

## Supported models

Currently only the following models support prompt caching with Azure OpenAI:

- `o1-preview-2024-09-12`
- `o1-mini-2024-09-12`
- `gpt-4o-2024-05-13`
- `gpt-4o-2024-08-06`
- `gpt-4o-mini-2024-07-18`

## API support

Official support for prompt caching was first added in API version `2024-10-01-preview`. At this time, only `o1-preview-2024-09-12` and `o1-mini-2024-09-12` models support the `cached_tokens` API response parameter.

## Getting started

For a request to take advantage of prompt caching the request must be both:

- A minimum of 1,024 tokens in length.
- The first 1,024 tokens in the prompt must be identical.

When a match is found between a prompt and the current content of the prompt cache, it's referred to as a cache hit. Cache hits will show up as [`cached_tokens`](/azure/ai-services/openai/reference-preview#cached_tokens) under [`prompt_token_details`](/azure/ai-services/openai/reference-preview#properties-for-prompt_tokens_details) in the chat completions response.

```json
{
  "created": 1729227448,
  "model": "o1-preview-2024-09-12",
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

The o1-series models are text only and don't support system messages, images, tool use/function calling, or structured outputs. This limits the efficacy of prompt caching for these models to the user/assistant portions of the messages array which are less likely to have an identical 1024 token prefix.

For `gpt-4o` and `gpt-4o-mini` models, prompt caching is supported for:  

| **Caching Supported** | **Description** |
|--------|--------|
|**Messages** | The complete messages array: system, user, and assistant content |
|**Images** | Images included in user messages, both as links or as base64-encoded data. The detail parameter must be set the same across requests.
|**Tool use**| Both the messages array and tool definitions |
|**Structured outputs** | Structured output schema is appended as a prefix to the system message|

To improve the likelihood of cache hits occurring, you should structure your requests such that repetitive content occurs at the beginning of the messages array.

## Can I disable prompt caching?

Prompt caching is enabled by default. There is no opt-out option.