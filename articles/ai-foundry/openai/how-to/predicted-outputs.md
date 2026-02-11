---
title: 'How to use predicted outputs with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to improve your model response latency with predicted outputs
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/11/2026
author: mrbullwinkle
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
recommendations: false
ai-usage: ai-assisted
---

# Predicted outputs (preview)

Predicted outputs can improve model response latency for chat completions calls where minimal changes are needed to a larger body of text. If you're asking the model to provide a response where a large portion of the expected response is already known, predicted outputs can significantly reduce the latency of this request. This capability is particularly well-suited for coding scenarios, including autocomplete, error detection, and real-time editing, where speed and responsiveness are critical for developers and end-users. Rather than have the model regenerate all the text from scratch, you can indicate to the model that most of the response is already known by passing the known text to the `prediction` parameter.

## Prerequisites

- An Azure OpenAI model deployed
- Upgrade the OpenAI Python library:

  ```cmd
  pip install --upgrade openai
  ```

- If you use Microsoft Entra ID, also install `azure-identity`:

  ```cmd
  pip install --upgrade azure-identity
  ```


## Model support

- `gpt-4o-mini` version: `2024-07-18`
- `gpt-4o` version: `2024-08-06`
- `gpt-4o` version: `2024-11-20`
- `gpt-4.1` version: `2025-04-14`
- `gpt-4.1-nano` version: `2025-04-14`
- `gpt-4.1-mini` version: `2025-04-14`

## API support

First introduced in `2025-01-01-preview`. Supported in all subsequent releases.

## Unsupported features

Predicted outputs is currently text-only. These features can't be used in conjunction with the `prediction` parameter and predicted outputs.

- Tools/Function calling
- audio models/inputs and outputs
- `n` values higher than `1`
- `logprobs`
- `presence_penalty` values greater than `0`
- `frequency_penalty` values greater than `0`
- `max_completion_tokens`

> [!NOTE]
> The predicted outputs feature is currently unavailable for models in the South East Asia region.

## Getting started

To demonstrate the basics of predicted outputs, we'll start by asking a model to refactor the code from the common programming `FizzBuzz` problem to replace the instance of `FizzBuzz` with `MSFTBuzz`. We'll pass our example code to the model in two places. First as part of a user message in the `messages` array/list, and a second time as part of the content of the new `prediction` parameter.

# [Microsoft Entra ID](#tab/python-secure)

You might need to upgrade your OpenAI client library to access the `prediction` parameter.

# [Microsoft Entra ID](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

code = """
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
"""

instructions = """
Replace string `FizzBuzz` with `MSFTBuzz`. Respond only 
with code, and with no markdown formatting.
"""


completion = client.chat.completions.create(
    model="YOUR-DEPLOYMENT-NAME",
    messages=[
        {
            "role": "user",
            "content": instructions
        },
        {
            "role": "user",
            "content": code
        }
    ],
    prediction={
        "type": "content",
        "content": code
    },
)

print(completion.model_dump_json(indent=2))
```

# [API key](#tab/python)

```python
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

code = """
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
"""

instructions = """
Replace string `FizzBuzz` with `MSFTBuzz`. Respond only 
with code, and with no markdown formatting.
"""


completion = client.chat.completions.create(
  model="YOUR-DEPLOYMENT-NAME",
  messages=[
    {
      "role": "user",
      "content": instructions
    },
    {
      "role": "user",
      "content": code
    }
  ],
    prediction={
        "type": "content",
        "content": code
  },
)

print(completion.model_dump_json(indent=2))
```

---

### Output

```json
{
  "id": "chatcmpl-AskZk3P5QGmefqobDw4Ougo6jLxSP",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "for number in range(1, 101):\n    if number % 3 == 0 and number % 5 == 0:\n        print(\"MSFTBuzz\")\n    elif number % 3 == 0:\n        print(\"Fizz\")\n    elif number % 5 == 0:\n        print(\"Buzz\")\n    else:\n        print(number)",
        "refusal": null,
        "role": "assistant",
        "audio": null,
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
  "created": 1737612112,
  "model": "gpt-4o-mini-2024-07-18",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_5154047bf2",
  "usage": {
    "completion_tokens": 77,
    "prompt_tokens": 124,
    "total_tokens": 201,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 6,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 4
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
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

Notice in the output the new response parameters for `accepted_prediction_tokens` and `rejected_prediction_tokens`:

```json
  "usage": {
    "completion_tokens": 77,
    "prompt_tokens": 124,
    "total_tokens": 201,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 6,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 4
    }
```

The `accepted_prediction_tokens` help reduce model response latency, but any `rejected_prediction_tokens` have the same cost implication as additional output tokens generated by the model. For this reason, while predicted outputs can improve model response times, it can result in greater costs. You'll need to evaluate and balance the increased model performance against the potential increases in cost.

It's also important to understand, that using predictive outputs doesn't guarantee a reduction in latency. A large request with a greater percentage of rejected prediction tokens than accepted prediction tokens could result in an increase in model response latency, rather than a decrease.  

> [!NOTE]
> Unlike [prompt caching](./prompt-caching.md) which only works when a set minimum number of initial tokens at the beginning of a request are identical, predicted outputs isn't constrained by token location. Even if your response text contains new output that will be returned prior to the predicted output, `accepted_prediction_tokens` can still occur.

## Streaming

Predicted outputs performance boost is often most obvious if you're returning your responses with streaming enabled.

# [Microsoft Entra ID](#tab/python-secure)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

code = """
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
"""

instructions = """
Replace string `FizzBuzz` with `MSFTBuzz`. Respond only 
with code, and with no markdown formatting.
"""


completion = client.chat.completions.create(
    model="YOUR-DEPLOYMENT-NAME",
    messages=[
        {
            "role": "user",
            "content": instructions
        },
        {
            "role": "user",
            "content": code
        }
    ],
    prediction={
        "type": "content",
        "content": code
    },
    stream=True
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='',)

```

# [API key](#tab/python)

```python
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

code = """
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
"""

instructions = """
Replace string `FizzBuzz` with `MSFTBuzz`. Respond only 
with code, and with no markdown formatting.
"""


completion = client.chat.completions.create(
    model="YOUR-DEPLOYMENT-NAME",
    messages=[
        {
            "role": "user",
            "content": instructions
        },
        {
            "role": "user",
            "content": code
        }
    ],
    prediction={
        "type": "content",
        "content": code
    },
    stream=True
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='',)
```

---

## Troubleshooting

- **401/403**: If you use Microsoft Entra ID, confirm your identity has access to the Azure OpenAI resource. If you use `get_bearer_token_provider`, request a token for `https://cognitiveservices.azure.com/.default`.
- **404**: Confirm `base_url` uses your Azure OpenAI resource name, and `model` uses your deployment name.
- **400**: Remove optional parameters and features listed in [Unsupported features](#unsupported-features), and try again.
