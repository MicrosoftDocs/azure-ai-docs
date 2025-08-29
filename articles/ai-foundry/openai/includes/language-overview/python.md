---
title: Azure OpenAI Python support
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI Python support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 08/29/2024
---

[Library source code](https://github.com/openai/openai-python?azure-portal=true) | [Package (PyPi)](https://pypi.org/project/openai?azure-portal=true) | [Reference](../../latest.md) |

> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to be both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

```cmd
pip install openai
```

For the latest version:

```cmd
pip install openai --upgrade
```

## Authentication

# [API Key](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import OpenAI
    
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
    )

```


# [Microsoft Entra ID](#tab/python-secure)

v1 support for Entra ID authentication is coming soon. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

---

## Chat

### chat.completions.create()

# [Python](#tab/command)

```python
# from openai import OpenAI
# client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2)
```

# [Response](#tab/response)

```json
{
  "id": "chatcmpl-AUhZ11g6aNb1Nnxjp4hFUNcszw3uf",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Microsoft was founded on April 4, 1975, by Bill Gates and Paul Allen in Albuquerque, New Mexico.",
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
  "created": 1731880663,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_04751d0b65",
  "usage": {
    "completion_tokens": 24,
    "prompt_tokens": 22,
    "total_tokens": 46,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
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

---

### chat.completions.create() - streaming

# [Python](#tab/command)

```python
# from openai import OpenAI
# client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ],
  stream=True
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='',)
```

# [Response](#tab/response)

```text
Microsoft was founded on April 4, 1975, by Bill Gates and Paul Allen.
```

---

### chat.completions.create() - image input

# [Python](#tab/command)


```python
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-foundry/openai/media/how-to/generated-seattle.png",
                    }
                },
            ],
        }
    ],
    max_tokens=300,
)

print(completion.model_dump_json(indent=2))
```

# [Response](#tab/response)

```json
{
  "id": "chatcmpl-AUisNBsjzPisMbx3k5Uz5SOKN63KN",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "This image is a watercolor painting of a city skyline, featuring a prominent tower that resembles the Space Needle, which is located in Seattle. The painting uses a blend of colors to depict the cityscape and sky.",
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
  "created": 1731885707,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_04751d0b65",
  "usage": {
    "completion_tokens": 42,
    "prompt_tokens": 639,
    "total_tokens": 681,
    "completion_tokens_details": null,
    "prompt_tokens_details": null
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "jailbreak": {
          "filtered": false,
          "detected": false
        }
      }
    },
    {
      "prompt_index": 1,
      "content_filter_results": {
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

---

## Embeddings

### embeddings.create()

# [Python](#tab/command)

```python
# from openai import OpenAI
# client = OpenAI()

embedding = client.embeddings.create(
  model="text-embedding-3-large", # Replace with your model deployment name
  input="Attenion is all you need",
  encoding_format="float" 
)

print(embedding)
```

# [Response](#tab/response)

The response has been truncated for brevity.

```
CreateEmbeddingResponse(data=[Embedding(embedding=[0.009098228, -0.010369237, -0.00048062875, -0.014328566, 0.019677775, 0.010049199, -0.005600668, 0.003858746, -0.007818076, 0.012554641, 0.005134327, 0.004514824, -0.020262988, -0.0039181816, 0.025475038, 0.016733425, 0.002136255, 0.0155172795, 0.0058978465, 0.012911255, -0.014273703, -0.016806576, 0.0265906, 0.037673064, 0.003909038, 0.0265906, -0.001935088, -0.014913779, 0.01781241, -0.017821554, 0.0016596265, -0.002987785, -0.014346854, -0.000962972, 0.0068671047, 0.004405097, -0.015764166, -0.007539185, -0.030394483, -0.01586475, 0.0074706054, -0.013761641, 0.010186358, 0.008805621, -0.009939471, 0.013944521, -0.010113207, -0.015745878, -0.021927187, 0.03231471, 0.0026951786, 0.004759425, 0.0065196347, 0.010927018, 0.017263774, 0.0055229445, 0.009381691, -0.042903405], index=0, object='embedding')], model='text-embedding-3-large', object='list', usage=Usage(prompt_tokens=7, total_tokens=7))
```

---

## Fine-tuning

[Fine-tuning with Python how-to article](../../how-to/fine-tuning.md)

## Responses API

See the [Responses API](../../how-to/responses.md) documentation.

## Error handling

```python
# from openai import OpenAI
# client = OpenAI()

import openai

try:
    client.fine_tuning.jobs.create(
        model="gpt-4o",
        training_file="file-test",
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

### Error codes

| Status Code | Error Type |
|----|---|
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |

### Request IDs

To retrieve the ID of your request you can use the `_request_id` property which corresponds to the `x-request-id` response header.

```python
print(completion._request_id) 
print(legacy_completion._request_id)
```

### Retries

The following errors are automatically retired twice by default with a brief exponential backoff:

- Connection Errors
- 408 Request Timeout
- 429 Rate Limit
- `>=`500 Internal Errors

Use `max_retries` to set/disable the retry behavior:

```python
# For all requests

from openai import OpenAI
client = OpenAI(
      max_retries=0
)
```

```python
# max retires for specific requests

client.with_options(max_retries=5).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "When was Microsoft founded?",
        }
    ],
    model="gpt-4o",
)
```