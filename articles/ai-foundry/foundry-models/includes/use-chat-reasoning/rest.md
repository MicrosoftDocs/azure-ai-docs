---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use the reasoning capabilities of chat completions models deployed in Microsoft Foundry Models.

[!INCLUDE [about-reasoning](about-reasoning.md)]

## Prerequisites

To complete this tutorial, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A model with reasoning capabilities model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a reasoning model. 

  * This example uses `DeepSeek-R1`.

## Use reasoning capabilities with chat

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

# [OpenAI API](#tab/openai)

```http
POST https://<resource>.services.ai.azure.com/openai/deployments/deepseek-r1/chat/completions?api-version=2024-10-21
Content-Type: application/json
api-key: <key>
```

# [Model Inference API (preview)](#tab/inference)

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
api-key: <key>
```
---

If you have configured the resource with **Microsoft Entra ID** support, pass you token in the `Authorization` header with the format `Bearer <token>`. Use scope `https://cognitiveservices.azure.com/.default`. 

# [OpenAI API](#tab/openai)

```http
POST https://<resource>.services.ai.azure.com/openai/deployments/deepseek-r1/chat/completions?api-version=2024-10-21
Content-Type: application/json
Authorization: Bearer <token>
```

# [Model Inference API (preview)](#tab/inference)

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
Authorization: Bearer <token>
```
---

Using Microsoft Entra ID may require additional configuration in your resource to grant access. Learn how to [configure key-less authentication with Microsoft Entra ID](../../how-to/configure-entra-id.md).

[!INCLUDE [best-practices](best-practices.md)]

### Create a chat completion request

The following example shows how you can create a basic chat request to the model.

```json
{
    "model": "deepseek-r1",
    "messages": [
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ]
}
```

The response is as follows, where you can see the model's usage statistics:

# [OpenAI API](#tab/openai)

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "reasoning_content": "Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start by recalling the general consensus from linguistic sources. I remember that the number often cited is around 7,000, but maybe I should check some reputable organizations.\n\nEthnologue is a well-known resource for language data, and I think they list about 7,000 languages. But wait, do they update their numbers? It might be around 7,100 or so. Also, the exact count can vary because some sources might categorize dialects differently or have more recent data. \n\nAnother thing to consider is language endangerment. Many languages are endangered, with some having only a few speakers left. Organizations like UNESCO track endangered languages, so mentioning that adds context. Also, the distribution isn't even. Some countries have hundreds of languages, like Papua New Guinea with over 800, while others have just a few. \n\nA user might also wonder why the exact number is hard to pin down. It's because the distinction between a language and a dialect can be political or cultural. For example, Mandarin and Cantonese are considered dialects of Chinese by some, but they're mutually unintelligible, so others classify them as separate languages. Also, some regions are under-researched, making it hard to document all languages. \n\nI should also touch on language families. The 7,000 languages are grouped into families like Indo-European, Sino-Tibetan, Niger-Congo, etc. Maybe mention a few of the largest families. But wait, the question is just about the count, not the families. Still, it's good to provide a bit more context. \n\nI need to make sure the information is up-to-date. Let me think – recent estimates still hover around 7,000. However, languages are dying out rapidly, so the number decreases over time. Including that note about endangerment and language extinction rates could be helpful. For instance, it's often stated that a language dies every few weeks. \n\nAnother point is sign languages. Does the count include them? Ethnologue includes some, but not all sources might. If the user is including sign languages, that adds more to the count, but I think the 7,000 figure typically refers to spoken languages. For thoroughness, maybe mention that there are also over 300 sign languages. \n\nSummarizing, the answer should state around 7,000, mention Ethnologue's figure, explain why the exact number varies, touch on endangerment, and possibly note sign languages as a separate category. Also, a brief mention of Papua New Guinea as the most linguistically diverse country. \n\nWait, let me verify Ethnologue's current number. As of their latest edition (25th, 2022), they list 7,168 living languages. But I should check if that's the case. Some sources might round to 7,000. Also, SIL International publishes Ethnologue, so citing them as reference makes sense. \n\nOther sources, like Glottolog, might have a different count because they use different criteria. Glottolog might list around 7,000 as well, but exact numbers vary. It's important to highlight that the count isn't exact because of differing definitions and ongoing research. \n\nIn conclusion, the approximate number is 7,000, with Ethnologue being a key source, considerations of endangerment, and the challenges in counting due to dialect vs. language distinctions. I should make sure the answer is clear, acknowledges the variability, and provides key points succinctly.\n",
                "content": "The exact number of languages in the world is challenging to determine due to differences in definitions (e.g., distinguishing languages from dialects) and ongoing documentation efforts. However, widely cited estimates suggest there are approximately **7,000 languages** globally.",
                "tool_calls": null
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 11,
        "total_tokens": 897,
        "completion_tokens": 886
    }
}
```

# [Model Inference API (preview)](#tab/inference)

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "<think>\nOkay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start by recalling the general consensus from linguistic sources. I remember that the number often cited is around 7,000, but maybe I should check some reputable organizations.\n\nEthnologue is a well-known resource for language data, and I think they list about 7,000 languages. But wait, do they update their numbers? It might be around 7,100 or so. Also, the exact count can vary because some sources might categorize dialects differently or have more recent data. \n\nAnother thing to consider is language endangerment. Many languages are endangered, with some having only a few speakers left. Organizations like UNESCO track endangered languages, so mentioning that adds context. Also, the distribution isn't even. Some countries have hundreds of languages, like Papua New Guinea with over 800, while others have just a few. \n\nA user might also wonder why the exact number is hard to pin down. It's because the distinction between a language and a dialect can be political or cultural. For example, Mandarin and Cantonese are considered dialects of Chinese by some, but they're mutually unintelligible, so others classify them as separate languages. Also, some regions are under-researched, making it hard to document all languages. \n\nI should also touch on language families. The 7,000 languages are grouped into families like Indo-European, Sino-Tibetan, Niger-Congo, etc. Maybe mention a few of the largest families. But wait, the question is just about the count, not the families. Still, it's good to provide a bit more context. \n\nI need to make sure the information is up-to-date. Let me think – recent estimates still hover around 7,000. However, languages are dying out rapidly, so the number decreases over time. Including that note about endangerment and language extinction rates could be helpful. For instance, it's often stated that a language dies every few weeks. \n\nAnother point is sign languages. Does the count include them? Ethnologue includes some, but not all sources might. If the user is including sign languages, that adds more to the count, but I think the 7,000 figure typically refers to spoken languages. For thoroughness, maybe mention that there are also over 300 sign languages. \n\nSummarizing, the answer should state around 7,000, mention Ethnologue's figure, explain why the exact number varies, touch on endangerment, and possibly note sign languages as a separate category. Also, a brief mention of Papua New Guinea as the most linguistically diverse country. \n\nWait, let me verify Ethnologue's current number. As of their latest edition (25th, 2022), they list 7,168 living languages. But I should check if that's the case. Some sources might round to 7,000. Also, SIL International publishes Ethnologue, so citing them as reference makes sense. \n\nOther sources, like Glottolog, might have a different count because they use different criteria. Glottolog might list around 7,000 as well, but exact numbers vary. It's important to highlight that the count isn't exact because of differing definitions and ongoing research. \n\nIn conclusion, the approximate number is 7,000, with Ethnologue being a key source, considerations of endangerment, and the challenges in counting due to dialect vs. language distinctions. I should make sure the answer is clear, acknowledges the variability, and provides key points succinctly.\n</think>\n\nThe exact number of languages in the world is challenging to determine due to differences in definitions (e.g., distinguishing languages from dialects) and ongoing documentation efforts. However, widely cited estimates suggest there are approximately **7,000 languages** globally.",
                "tool_calls": null
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 11,
        "total_tokens": 897,
        "completion_tokens": 886
    }
}
```
---

### Reasoning content

> [!NOTE]
> This information on reasoning content does not apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind it. 

# [OpenAI API](#tab/openai)

The reasoning associated with the completion is included in the field `reasoning_content`. The model may select on which scenarios to generate reasoning content. 

# [Model Inference API (preview)](#tab/inference)

The reasoning associated with the completion is included in the response's content within the tags `<think>` and `</think>`. The model may select on which scenarios to generate reasoning content. 

---

When making multi-turn conversations, it's useful to avoid sending the reasoning content in the chat history as reasoning tends to generate long explanations.

### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.

To stream completions, set `"stream": true` when you call the model.


```json
{
    "model": "DeepSeek-R1",
    "messages": [
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "stream": true,
    "max_tokens": 2048
}
```

To visualize the output, define a helper function to print the stream. The following example implements a routing that stream only the answer without the reasoning content:

# [OpenAI API](#tab/openai)

```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "reasoning_content": "Okay,",
                "content": ""
            },
            "finish_reason": null,
            "logprobs": null
        }
    ]
}
```

# [Model Inference API (preview)](#tab/inference)

```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": "<think>Okay,"
            },
            "finish_reason": null,
            "logprobs": null
        }
    ]
}
```
---

The last message in the stream has `finish_reason` set, indicating the reason for the generation process to stop.

# [OpenAI API](#tab/openai)

```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "delta": {
                "reasoning_content": "",
                "content": ""
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 11,
        "total_tokens": 897,
        "completion_tokens": 886
    }
}
```

# [Model Inference API (preview)](#tab/inference)

```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "DeepSeek-R1",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": ""
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 11,
        "total_tokens": 897,
        "completion_tokens": 886
    }
}
```
---

### Parameters

In general, reasoning models don't support the following parameters you can find in chat completion models:

* Temperature
* Presence penalty
* Repetition penalty
* Parameter `top_p`

Some models support the use of tools or structured outputs (including JSON-schemas). Read the [Models](../../concepts/models-sold-directly-by-azure.md) details page to understand each model's support.

### Apply Guardrails and controls

The Azure AI Model Inference API supports [Azure AI Content Safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI Content Safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt.


```json
{
    "model": "DeepSeek-R1",
    "messages": [
        {
            "role": "user",
            "content": "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
        }
    ]
}
```

```json
{
    "error": {
        "message": "The response was filtered due to the prompt triggering Microsoft's content management policy. Please modify your prompt and retry.",
        "type": null,
        "param": "prompt",
        "code": "content_filter",
        "status": 400
    }
}
```


> [!TIP]
> To learn more about how you can configure and control Azure AI Content Safety settings, check the [Azure AI Content Safety documentation](https://aka.ms/azureaicontentsafety).
