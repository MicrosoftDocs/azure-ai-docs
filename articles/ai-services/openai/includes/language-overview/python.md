---
title: Azure OpenAI Python support
titleSuffix: Azure OpenAI Service
description: Azure OpenAI Python support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/18/2024
---

[Library source code](https://github.com/openai/openai-python?azure-portal=true) | [Package (PyPi)](https://pypi.org/project/openai?azure-portal=true) | [Reference](../../reference.md) |

> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

## Azure OpenAI API version support

Feature availability in Azure OpenAI is dependent on what version of the REST API you target. For the newest features, target the latest preview API.

| Latest GA API | Latest Preview API|
|:-----|:------|
|`2024-10-21` |`2024-10-01-preview`|

## Installation

```cmd
pip install openai
```

For the latest version:

```cmd
pip install openai --upgrade
```

## Authentication

# [Microsoft Entra ID](#tab/python-secure)

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-10-21"
)
```

# [API Key](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-10-21",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

```

---

## Audio

### audio.speech.create()

This function currently requires a preview API version. 

Set `api_version="2024-10-01-preview"` to use this function. 

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

from pathlib import Path
import os

speech_file_path = Path("speech.mp3")

response = client.audio.speech.create(
  model="tts-hd", #Replace with model deployment name
  voice="alloy",
  input="Testing, testing, 1,2,3."
)
response.write_to_file(speech_file_path)
```

### audio.transcriptions.create()


# [Python](#tab/command)

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

audio_file = open("speech1.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper", # Replace with model deployment name
  file=audio_file
)

print(transcript)
```
# [Response](#tab/response)

```text
Transcription(text='Testing, testing, one, two, three.')
```

---

## Chat

### chat.completions.create()

# [Python](#tab/command)

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model dpeloyment name.
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
# from openai import AzureOpenAI
# client = AzureOpenAI()

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model dpeloyment name.
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
                        "url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png",
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
# from openai import AzureOpenAI
# client = AzureOpenAI()

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

## Batch

[Batch with Python how-to article](../../how-to/batch.md)

## Images

### images.generate()


# [Python](#tab/command)

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

generate_image = client.images.generate(
  model="dall-e-3", #replace with your model deployment name
  prompt="A rabbit eating pancakes",
  n=1,
  size="1024x1024",
  quality = "hd",
  response_format = "url",
  style = "vivid"
)

print(generate_image.model_dump_json(indent=2))
```

# [Response](#tab/response)

```json
{
  "created": 1731894125,
  "data": [
    {
      "b64_json": null,
      "revised_prompt": "A fluffy rabbit contentedly munching on a stack of miniature pancakes laid out on a small plate just its size, set against the backdrop of a sunny meadow.",
      "url": "{Secure path to generated image's Azure Blob storage image url}",
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
      },
      "prompt_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "profanity": {
          "detected": false,
          "filtered": false
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

## Completions (legacy)

### completions.create()

# [Python](#tab/command)

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

legacy_completion = client.completions.create(
  model="gpt-35-turbo-instruct", # Replace with model deployment name
  prompt="Hello World!",
  max_tokens=100,
  temperature=0
)

print(legacy_completion.model_dump_json(indent=2))
```


# [Response](#tab/response)

```
{
  "id": "cmpl-AUlF8xymP0ngMlIgIEYlT7C3Igi2H",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\n\nHello World!\n\nHello World!",
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
  "created": 1731894806,
  "model": "gpt-35-turbo-instruct",
  "object": "text_completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 8,
    "prompt_tokens": 3,
    "total_tokens": 11,
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

## Error handling

```python
# from openai import AzureOpenAI
# client = AzureOpenAI()

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

To retrieve the ID of your request you can use the `_request_id` property which corresponds to the `x-request-id` responde header.

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

from openai import AzureOpenAI
client = AzureOpenAI(
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