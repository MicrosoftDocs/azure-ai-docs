---
title: Azure OpenAI reasoning models - o3-mini, o1, o1-mini
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's advanced o3-mini, o1, & o1-mini reasoning models 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/07/2025
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
| `o3-mini` | [Model availability](../concepts/models.md#global-standard-model-availability).  | Access is no longer restricted for this model.   |
|`o1` | [Model availability](../concepts/models.md#global-standard-model-availability).  | Access is no longer restricted for this model.  |
| `o1-preview` | [Model availability](../concepts/models.md#global-standard-model-availability). |This model is only available for customers who were granted access as part of the original limited access release. We're currently not expanding access to `o1-preview`. |
| `o1-mini` | [Model availability](../concepts/models.md#global-standard-model-availability). | No access request needed for Global Standard deployments.<br><br>Standard (regional) deployments are currently only available to select customers who were previously granted access as part of the `o1-preview` release.|

## API & feature support

| **Feature**     | **o3-mini**, **2025-01-31**  |**o1**, **2024-12-17**   | **o1-preview**, **2024-09-12**   | **o1-mini**, **2024-09-12**   |
|:-------------------|:--------------------------:|:--------------------------:|:-------------------------------:|:---:|
| **API Version**    | `2024-12-01-preview` or later <br> `2025-03-01-preview` (Recommended)   | `2024-12-01-preview` or later <br> `2025-03-01-preview` (Recommended) | `2024-09-01-preview` or later <br> `2025-03-01-preview` (Recommended)    | `2024-09-01-preview` or later <br> `2025-03-01-preview` (Recommended)    |
| **[Developer Messages](#developer-messages)** | ✅ | ✅ | - | - |
| **[Structured Outputs](./structured-outputs.md)** | ✅ | ✅ | - | - |
| **[Context Window](../concepts/models.md#o-series-models)** | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 128,000  <br> Output: 32,768 | Input: 128,000  <br> Output: 65,536 |
| **[Reasoning effort](#reasoning-effort)** | ✅ | ✅ | - | - |
| **[Vision Support](./gpt-with-vision.md)** | - | ✅ | - | - |
| Functions/Tools | ✅  | ✅  |  - | - |
| `max_completion_tokens`<sup>*</sup> |✅ |✅ |✅ | ✅ |
| System Messages<sup>**</sup> | ✅ | ✅ | - | - |
| Streaming | ✅ | - | - | - |

<sup>*</sup> Reasoning models will only work with the `max_completion_tokens` parameter. <br><br>

<sup>**</sup>The latest o<sup>&#42;</sup> series model support system messages to make migration easier. When you use a system message with `o3-mini` and `o1` it will be treated as a developer message. You should not use both a developer message and a system message in the same API request.



### Not Supported

The following are currently unsupported with reasoning models:

- Parallel tool calling
- `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, `logit_bias`, `max_tokens`

## Usage

These models [don't currently support the same set of parameters](#api--feature-support) as other models that use the chat completions API. 

# [Python (Microsoft Entra ID)](#tab/python-secure)

You'll need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI Service with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-12-01-preview"
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
  api_version="2024-12-01-preview"
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

# [C#](tab/#csharp)

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

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI Service with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-12-01-preview"
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
  api_version="2024-12-01-preview"
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

## Markdown output

By default the `o3-mini` and `o1` models will not attempt to produce output that includes markdown formatting. A common use case where this behavior is undesirable is when you want the model to output code contained within a markdown code block. When the model generates output without markdown formatting you lose features like syntax highlighting, and copyable code blocks in interactive playground experiences. To override this new default behavior and encourage markdown inclusion in model responses, add the string `Formatting re-enabled` to the beginning of your developer message.

Adding `Formatting re-enabled` to the beginning of your developer message does not guarantee that the model will include markdown formatting in its response, it only increases the likelihood. We have found from internal testing that `Formatting re-enabled` is less effective by itself with the `o1` model than with `o3-mini`.

To improve the performance of `Formatting re-enabled` you can further augment the beginning of the developer message which will often result in the desired output. Rather than just adding `Formatting re-enabled` to the beginning of your developer message, you can experiment with adding a more descriptive initial instruction like one of the examples below:

- `Formatting re-enabled - please enclose code blocks with appropriate markdown tags.`
- `Formatting re-enabled - code output should be wrapped in markdown.`

Depending on your expected output you may need to customize your initial developer message further to target your specific use case.
