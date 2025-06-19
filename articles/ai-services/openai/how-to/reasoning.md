---
title: Azure OpenAI reasoning models - o3-mini, o1, o1-mini
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's advanced o3-mini, o1, & o1-mini reasoning models 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 06/17/2025
author: mrbullwinkle    
ms.author: mbullwin
---


# Azure OpenAI reasoning models

Azure OpenAI `o-series` models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

**Key capabilities of the o-series models:**

- Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
- Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
- Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
- Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.

## Availability

### Region availability

| Model | Region | Limited access |
|---|---|---|
| `o3-pro`  | East US2 & Sweden Central (Global Standard)    |  Request access: [o3 limited access model application](https://aka.ms/oai/o3access). If you already have `o3 access` no request is required for `o3-pro`.    |
| `codex-mini`  | East US2 & Sweden Central (Global Standard)    | No access request needed.    |
| `o4-mini`  | [Model availability](../concepts/models.md#global-standard-model-availability)   | No access request needed to use the core capabilities of this model.<br><br> Request access: [o4-mini reasoning summary feature](https://aka.ms/oai/o3access)     |
| `o3` |  [Model availability](../concepts/models.md#global-standard-model-availability)  | Request access: [o3 limited access model application](https://aka.ms/oai/o3access)     |
| `o3-mini` | [Model availability](../concepts/models.md#global-standard-model-availability).  | Access is no longer restricted for this model.   |
|`o1` | [Model availability](../concepts/models.md#global-standard-model-availability).  | Access is no longer restricted for this model.  |
| `o1-preview` | [Model availability](../concepts/models.md#global-standard-model-availability). |This model is only available for customers who were granted access as part of the original limited access release. We're currently not expanding access to `o1-preview`. |
| `o1-mini` | [Model availability](../concepts/models.md#global-standard-model-availability). | No access request needed for Global Standard deployments.<br><br>Standard (regional) deployments are currently only available to select customers who were previously granted access as part of the `o1-preview` release.|

## API & feature support

| **Feature**  | **codex-mini**, **2025-05-16**  | **o3-pro**, **2025-06-10**   | **o4-mini**, **2025-04-16**  | **o3**, **2025-04-16** | **o3-mini**, **2025-01-31**  |**o1**, **2024-12-17**   | **o1-preview**, **2024-09-12**   | **o1-mini**, **2024-09-12**   |
|:-------------------|:--------------------------:|:------:|:--------|:-----:|:-------:|:--------------------------:|:-------------------------------:|:---:|
| **API Version** | `2025-04-01-preview` & [v1 preview](../api-version-lifecycle.md#api-evolution)   | `2025-04-01-preview`  & [v1 preview](../api-version-lifecycle.md#api-evolution)  | `2025-04-01-preview`   | `2025-04-01-preview`   | `2024-12-01-preview` or later <br> `2025-03-01-preview` (Recommended)   | `2024-12-01-preview` or later <br> `2025-03-01-preview` (Recommended) | `2024-09-01-preview` or later <br> `2025-03-01-preview` (Recommended)    | `2024-09-01-preview` or later <br> `2025-03-01-preview` (Recommended)    |
| **[Developer Messages](#developer-messages)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| **[Structured Outputs](./structured-outputs.md)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| **[Context Window](../concepts/models.md#o-series-models)** |  Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 128,000  <br> Output: 32,768 | Input: 128,000  <br> Output: 65,536 |
| **[Reasoning effort](#reasoning-effort)** | ✅| ✅| ✅| ✅ |✅ | ✅ | - | - |
| **[Vision Support](./gpt-with-vision.md)** | ✅ | ✅ | ✅ | ✅ | - | ✅ | - | - |
| Chat Completions API | - | - | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Responses API | ✅  | ✅  | ✅ | ✅  | - | - | - | - |
| Functions/Tools | ✅ | ✅ |✅ | ✅ | ✅  | ✅  |  - | - |
| Parallel Tool Calls | - | - | - | - | -  | -  |  - | - |
| `max_completion_tokens` <sup>1</sup> |  ✅ | ✅ | ✅ | ✅ |✅ |✅ |✅ | ✅ |
| System Messages <sup>2</sup>  ✅ | ✅| ✅ | ✅ | ✅ | ✅ | - | - |
| [Reasoning summary](#reasoning-summary) <sup>3</sup> |  ✅ | ✅ | ✅ | ✅ | -  | -  |  - | - |
| Streaming <sup>4</sup>  | ✅ | - | ✅ | ✅| ✅ | - | - | - |

<sup>1</sup> Reasoning models will only work with the `max_completion_tokens` parameter. <br><br>
<sup>2</sup> The latest o<sup>&#42;</sup> series model support system messages to make migration easier. When you use a system message with `o4-mini`, `o3`, `o3-mini`, and `o1` it will be treated as a developer message. You should not use both a developer message and a system message in the same API request.
<sup>3</sup> Access to the chain-of-thought reasoning summary is limited access only for `o3` & `o4-mini`.
<sup>4</sup> Streaming for `o3` is limited access only.

> [!NOTE]
> To avoid timeouts [background mode](./responses.md#background-tasks) is recommended for `o3-pro`.

### Not Supported

The following are currently unsupported with reasoning models:

- `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, `logit_bias`, `max_tokens`

## Usage

These models [don't currently support the same set of parameters](#api--feature-support) as other models that use the chat completions API. 

# [Python (Microsoft Entra ID)](#tab/python-secure)

You'll need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Azure AI Foundry Models with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.chat.completions.create(
    model="o1-new", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

# [Python (key-based auth)](#tab/python)

You might need to upgrade your version of the OpenAI Python library to take advantage of the new parameters like `max_completion_tokens`.

```cmd
pip install openai --upgrade
```

```python

from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2025-03-01-preview"
)

response = client.chat.completions.create(
    model="o1-new", # replace with the model deployment name of your o1 deployment.
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

# [C#](#tab/csharp)

```c#
using Azure.AI.OpenAI;
using Azure.AI.OpenAI.Chat;
using Azure.Identity;
using OpenAI.Chat;

AzureOpenAIClient openAIClient = new(
    new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("o3-mini"); //model deployment name

ChatCompletionOptions options = new ChatCompletionOptions
{
    MaxOutputTokenCount = 100000
};

#pragma warning disable AOAI001 //currently required to use MaxOutputTokenCount

options.SetNewMaxCompletionTokensPropertyEnabled(true);

ChatCompletion completion = chatClient.CompleteChat(
    [

        new UserChatMessage("Testing 1,2,3")
    ],
    options); // Pass the options to the CompleteChat method

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

---

**Python Output:**

```json
{
  "id": "chatcmpl-AEj7pKFoiTqDPHuxOcirA9KIvf3yz",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Writing your first Python API is an exciting step in developing software that can communicate with other applications. An API (Application Programming Interface) allows different software systems to interact with each other, enabling data exchange and functionality sharing. Here are the steps you should consider when creating your first Python API...truncated for brevity.",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1728073417,
  "model": "o1-2024-12-17",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_503a95a7d8",
  "usage": {
    "completion_tokens": 1843,
    "prompt_tokens": 20,
    "total_tokens": 1863,
    "completion_tokens_details": {
      "audio_tokens": null,
      "reasoning_tokens": 448
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "custom_blocklists": {
          "filtered": false
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

## Reasoning effort

> [!NOTE]
> Reasoning models have `reasoning_tokens` as part of `completion_tokens_details` in the model response. These are hidden tokens that aren't returned as part of the message response content but are used by the model to help generate a final answer to your request. `2024-12-01-preview` adds an additional new parameter `reasoning_effort` which can be set to `low`, `medium`, or `high` with the latest `o1` model. The higher the effort setting, the longer the model will spend processing the request, which will generally result in a larger number of `reasoning_tokens`.

## Developer messages

Functionally developer messages ` "role": "developer"` are the same as system messages. 

Adding a developer message to the previous code example would look as follows:

# [Python (Microsoft Entra ID)](#tab/python-secure)

You'll need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2025-03-01-preview"
)

response = client.chat.completions.create(
    model="o1-new", # replace with the model deployment name of your o1-preview, or o1-mini model
    messages=[
        {"role": "developer","content": "You are a helpful assistant."}, # optional equivalent to a system message for reasoning models 
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000,
    reasoning_effort = "medium" # low, medium, or high

)

print(response.model_dump_json(indent=2))
```

# [Python (key-based auth)](#tab/python)

You might need to upgrade your version of the OpenAI Python library to take advantage of the new parameters like `max_completion_tokens`.

```cmd
pip install openai --upgrade
```

```python

from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2025-03-01-preview"
)

response = client.chat.completions.create(
    model="o1-new", # replace with the model deployment name of your o1 deployment.
    messages=[
        {"role": "developer","content": "You are a helpful assistant."}, # optional equivalent to a system message for reasoning models 
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000,
    reasoning_effort = "medium" # low, medium, or high
)

print(response.model_dump_json(indent=2))
```

# [C#](#tab/csharp)

```csharp
using Azure.AI.OpenAI;
using Azure.AI.OpenAI.Chat;
using Azure.Identity;
using OpenAI.Chat;

AzureOpenAIClient openAIClient = new(
    new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/"),
    new DefaultAzureCredential());
ChatClient chatClient = openAIClient.GetChatClient("o3-mini"); //model deployment name

ChatCompletionOptions options = new ChatCompletionOptions
{
    ReasoningEffortLevel = ChatReasoningEffortLevel.Low,
    MaxOutputTokenCount = 100000
};

#pragma warning disable AOAI001 //currently required to use MaxOutputTokenCount

options.SetNewMaxCompletionTokensPropertyEnabled(true);

ChatCompletion completion = chatClient.CompleteChat(
    [
        new DeveloperChatMessage("You are a helpful assistant."),
        new UserChatMessage("Testing 1,2,3")
    ],
    options); // Pass the options to the CompleteChat method

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

---

## Reasoning summary

When using the latest `o3` and `o4-mini` models with the [Responses API](./responses.md) you can use the reasoning summary parameter to receive summaries of the model's chain of thought reasoning. This parameter can be set to `auto`, `concise`, or `detailed`. Access to this feature requires you to [Request Access](https://aka.ms/oai/o3access).

> [!NOTE]
> Even when enabled, reasoning summaries are not generated for every step/request. This is expected behavior.

# [Python](#tab/py)

You'll need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)

response = client.responses.create(
    input="Tell me about the curious case of neural text degeneration",
    model="o4-mini", # replace with model deployment name
    reasoning={
        "effort": "medium",
        "summary": "detailed" # auto, concise, or detailed (currently only supported with o4-mini and o3)
    }
)

print(response.model_dump_json(indent=2))
```

# [REST](#tab/REST)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
 -d '{
     "model": "o4-mini",
     "input": "Tell me about the curious case of neural text degeneration",
     "reasoning": {"summary": "detailed"}
    }'
```

---

```output
{
  "id": "resp_68007e26b2cc8190b83361014f3a78c50ae9b88522c3ad24",
  "created_at": 1744862758.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "o4-mini",
  "object": "response",
  "output": [
    {
      "id": "rs_68007e2773bc8190b5b8089949bfe13a0ae9b88522c3ad24",
      "summary": [
        {
          "text": "**Summarizing neural text degeneration**\n\nThe user's asking about \"The Curious Case of Neural Text Degeneration,\" a paper by Ari Holtzman et al. from 2020. It explains how certain decoding strategies produce repetitive and dull text. In contrast, methods like nucleus sampling yield more coherent and diverse outputs. The authors introduce metrics like surprisal and distinct-n for evaluation and suggest that maximum likelihood decoding often favors generic continuations, leading to loops and repetitive patterns in longer texts. They promote sampling from truncated distributions for improved text quality.",
          "type": "summary_text"
        },
        {
          "text": "**Explaining nucleus sampling**\n\nThe authors propose nucleus sampling, which captures a specified mass of the predictive distribution, improving metrics such as coherence and diversity. They identify a \"sudden drop\" phenomenon in token probabilities, where a few tokens dominate, leading to a long tail. By truncating this at a cumulative probability threshold, they aim to enhance text quality compared to top-k sampling. Their evaluations include human assessments, showing better results in terms of BLEU scores and distinct-n measures. Overall, they highlight how decoding strategies influence quality and recommend adaptive techniques for improved outcomes.",
          "type": "summary_text"
        }
      ],
      "type": "reasoning",
      "status": null
    },
    {
      "id": "msg_68007e35c44881908cb4651b8e9972300ae9b88522c3ad24",
      "content": [
        {
          "annotations": [],
          "text": "Researchers first became aware that neural language models, when used to generate long stretches of text with standard “maximum‐likelihood” decoding (greedy search, beam search, etc.), often produce bland, repetitive or looping output. The 2020 paper “The Curious Case of Neural Text Degeneration” (Holtzman et al.) analyzes this failure mode and proposes a simple fix—nucleus (top‑p) sampling—that dramatically improves output quality.\n\n1. The Problem: Degeneration  \n   • With greedy or beam search, models tend to pick very high‑probability tokens over and over, leading to loops (“the the the…”) or generic, dull continuations.  \n   • Even sampling with a fixed top‑k (e.g. always sample from the 40 most likely tokens) can be suboptimal: if the model’s probability mass is skewed, k may be too small (overly repetitive) or too large (introducing incoherence).\n\n2. Why It Happens: Distributional Peakedness  \n   • At each time step the model’s predicted next‐token distribution often has one or two very high‑probability tokens, then a long tail of low‑probability tokens.  \n   • Maximum‐likelihood decoding zeroes in on the peak, collapsing diversity.  \n   • Uniform sampling over a large k allows low‑probability “wild” tokens, harming coherence.\n\n3. The Fix: Nucleus (Top‑p) Sampling  \n   • Rather than fixing k, dynamically truncate the distribution to the smallest set of tokens whose cumulative probability ≥ p (e.g. p=0.9).  \n   • Then renormalize and sample from that “nucleus.”  \n   • This keeps only the “plausible” mass and discards the improbable tail, adapting to each context.\n\n4. Empirical Findings  \n   • Automatic metrics (distinct‑n, repetition rates) and human evaluations show nucleus sampling yields more diverse, coherent, on‑topic text than greedy/beam or fixed top‑k.  \n   • It also outperforms simple temperature scaling (raising logits to 1/T) because it adapts to changes in the distribution’s shape.\n\n5. Takeaways for Practitioners  \n   • Don’t default to beam search for open-ended generation—its high likelihood doesn’t mean high quality.  \n   • Use nucleus sampling (p between 0.8 and 0.95) for a balance of diversity and coherence.  \n   • Monitor repetition and distinct‑n scores if you need automatic sanity checks.\n\nIn short, “neural text degeneration” is the tendency of likelihood‐maximizing decoders to produce dull or looping text. By recognizing that the shape of the model’s probability distribution varies wildly from step to step, nucleus sampling provides an elegant, adaptive way to maintain both coherence and diversity in generated text.",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": {
    "effort": "medium",
    "generate_summary": null,
    "summary": "detailed"
  },
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    }
  },
  "truncation": "disabled",
  "usage": {
    "input_tokens": 16,
    "output_tokens": 974,
    "output_tokens_details": {
      "reasoning_tokens": 384
    },
    "total_tokens": 990,
    "input_tokens_details": {
      "cached_tokens": 0
    }
  },
  "user": null,
  "store": true
}
```

## Markdown output

By default the `o3-mini` and `o1` models will not attempt to produce output that includes markdown formatting. A common use case where this behavior is undesirable is when you want the model to output code contained within a markdown code block. When the model generates output without markdown formatting you lose features like syntax highlighting, and copyable code blocks in interactive playground experiences. To override this new default behavior and encourage markdown inclusion in model responses, add the string `Formatting re-enabled` to the beginning of your developer message.

Adding `Formatting re-enabled` to the beginning of your developer message does not guarantee that the model will include markdown formatting in its response, it only increases the likelihood. We have found from internal testing that `Formatting re-enabled` is less effective by itself with the `o1` model than with `o3-mini`.

To improve the performance of `Formatting re-enabled` you can further augment the beginning of the developer message which will often result in the desired output. Rather than just adding `Formatting re-enabled` to the beginning of your developer message, you can experiment with adding a more descriptive initial instruction like one of the examples below:

- `Formatting re-enabled - please enclose code blocks with appropriate markdown tags.`
- `Formatting re-enabled - code output should be wrapped in markdown.`

Depending on your expected output you may need to customize your initial developer message further to target your specific use case.
