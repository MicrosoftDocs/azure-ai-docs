---
title: Azure OpenAI o1 series reasoning models
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's advanced o1 series reasoning models
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 12/17/2024
author: mrbullwinkle    
ms.author: mbullwin
---


# Azure OpenAI reasoning models

Azure OpenAI `o1` and `o1-mini` models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

**Key capabilities of the o1 series:**

- Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
- Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
- Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
- Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.

## Availability

The **o1 series** models are now available for API access and model deployment. **Registration is required, and access will be granted based on Microsoft's eligibility criteria**. Customers who previously applied and received access to `o1-preview`, don't need to reapply as they are automatically on the wait-list for the latest model.

Request access: [limited access model application](https://aka.ms/OAI/o1access)

Once access has been granted, you'll need to create a deployment for each model. If you have an existing `o1-preview` deployment, in-place upgrade is currently not supported, you'll need to create a new deployment.

### Region availability

| Model | Region |
|---|---|
|`o1` | East US2 (Global Standard) <br> Sweden Central (Global Standard) |
| `o1-preview` | See [models page](../concepts/models.md#global-standard-model-availability). |
| `o1-mini` | See [models page](../concepts/models.md#global-standard-model-availability). |

## API support

Initial support for the **o1-preview** and **o1-mini** preview models was added in API version `2024-09-01-preview`. 

As part of this release, the `max_tokens` parameter was deprecated and replaced with the new `max_completion_tokens` parameter. **o1 series** models will only work with the `max_completion_tokens` parameter.

The latest most capable **o1 series** model is `o1` **Version: 2024-12-17**. This  general availability (GA) model should be used with API version `2024-12-01-preview`.

### 2024-12-01-preview

`2024-12-01-preview` adds support for the new `reasoning_effort` parameter, [structured outputs](./structured-outputs.md), and developer messages. The older preview reasoning models do not currently support these features. For reasoning models, these features are currently only available with `o1` **Version: 2024-12-17**.

## Usage

These models do not currently support the same set of parameters as other models that use the chat completions API. Only a limited subset is currently supported. Using standard parameters like `temperature` and `top_p` will result in errors.

# [Python (Microsoft Entra ID)](#tab/python-secure)

You will need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

If you are new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI Service with Microsoft Entra ID authentication](../how-to/managed-identity.md).

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

---

**Output:**

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



> [!NOTE]
> Reasoning models have `reasoning_tokens` as part of `completion_tokens_details` in the model response. These are hidden tokens that are not returned as part of the message response content but are used by the model to help generate a final answer to your request. `2024-12-01-preview` adds an additional new parameter `reasoning_effort` which can be set to `low`, `medium`, or `high` with the latest `o1` model. The higher the effort setting, the longer the model will spend processing the request, which will generally result in a larger number of `reasoning_tokens`.

## Developer messages

Functionally developer messages ` "role": "developer"` are the same as system messages.

- **System messages are not supported** with the **o1 series** reasoning models. 
- `o1-2024-12-17` with API version: `2024-12-01-preview` and later adds support for developer messages. 

Adding a developer message to the previous code example would look as follows:

# [Python (Microsoft Entra ID)](#tab/python-secure)

You will need to upgrade your OpenAI client library for access to the latest parameters.

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
        {"role": "developer","content": "You are a helpful assistant."}, # optional equivalent to a system message for reasoning models 
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000
)

print(response.model_dump_json(indent=2))
```

---

