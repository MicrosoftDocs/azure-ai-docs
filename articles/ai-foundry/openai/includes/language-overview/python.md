---
title: Azure OpenAI Python support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI Python support
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 08/29/2024
ai-usage: ai-assisted
---

[Library source code](https://github.com/openai/openai-python?azure-portal=true) | [Package (PyPi)](https://pypi.org/project/openai?azure-portal=true) | [Reference](../../latest.md) |

> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-python/releases) to track the latest updates to the library.

## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

```cmd
pip install openai
```

For the latest version:

```cmd
pip install openai --upgrade
```

## Authentication

::: moniker range="foundry-classic"

Endpoints and API keys for your resources can be retrieved from the [Azure portal](https://portal.azure.com) or the [Foundry portal](https://ai.azure.com/?cid=learnDocs):

- Sign in to [Azure portal](https://portal.azure.com) > select your resource > **Resource Management** > **Keys and Endpoint**.
- Sign in to [Foundry portal](https://ai.azure.com/?cid=learnDocs) > select your resource.

::: moniker-end

::: moniker range="foundry"

Endpoints and API keys for your resources can be retrieved from the [Azure portal](https://portal.azure.com) or the [!INCLUDE [foundry-link](../../../default/includes/foundry-link.md)] portal:

- Sign in to [Azure portal](https://portal.azure.com) > select your resource > **Resource Management** > **Keys and Endpoint**.
- Sign in to [!INCLUDE [foundry-link](../../../default/includes/foundry-link.md)] portal > select your resource.

::: moniker-end


# [Microsoft Entra ID](#tab/python-entra)

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
```

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

# [Environment Variables](#tab/python-env)

If you use the default environment variables of `OPENAI_BASE_URL` and `OPENAI_API_KEY` they're automatically used by the client with no further configuration required.

| Environment Variable | Value |
|----------------|-------------|
| `OPENAI_BASE_URL`    | `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`|
| `OPENAI_API_KEY`     | Azure OpenAI or Foundry API key. |

```python
from openai import OpenAI

client = OpenAI()   
```

# [Response](#tab/python-output)

There's no output for client instantiation.

---

## Responses API

### responses.create()

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="gpt-4.1-nano",
    input= "This is a test" 
)

print(response.model_dump_json(indent=2)) 
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your model deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [Environment Variables](#tab/python-env)

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your model deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [Response](#tab/python-output)

```json
{
  "id": "resp_088ffc6b5f37c64d0068e187d0ceac819499c9331c2a02e92e",
  "created_at": 1759610832.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4.1-nano",
  "object": "response",
  "output": [
    {
      "id": "msg_088ffc6b5f37c64d0068e187d15f8c819495f84e214435175d",
      "content": [
        {
          "annotations": [],
          "text": "Hello! I see you've sent a message saying \"This is a test.\" How can I assist you today?",
          "type": "output_text",
          "logprobs": []
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
  "background": false,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": null,
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "top_logprobs": 0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 11,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 23,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 34
  },
  "user": null,
  "content_filters": null,
  "store": true
}
```

---

### responses.create() with MCP server tool

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

resp = client.responses.create(
    model="gpt-5",
    tools=[
        {
            "type": "mcp",
            "server_label": "microsoft_learn",
            "server_description": "Microsoft Learn MCP server for searching and fetching Microsoft documentation.",
            "server_url": "https://learn.microsoft.com/api/mcp",
            "require_approval": "never",
        },
    ],
    input="Search for information about Azure Functions",
)

print(resp.output_text)
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

resp = client.responses.create(
    model="gpt-5",
    tools=[
        {
            "type": "mcp",
            "server_label": "microsoft_learn",
            "server_description": "Microsoft Learn MCP server for searching and fetching Microsoft documentation.",
            "server_url": "https://learn.microsoft.com/api/mcp",
            "require_approval": "never",
        },
    ],
    input="Search for information about Azure Functions",
)

print(resp.output_text)
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [Environment Variables](#tab/python-env)

```python
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-5",
    tools=[
        {
            "type": "mcp",
            "server_label": "microsoft_learn",
            "server_description": "Microsoft Learn MCP server for searching and fetching Microsoft documentation.",
            "server_url": "https://learn.microsoft.com/api/mcp",
            "require_approval": "never",
        },
    ],
    input="Search for information about Azure Functions",
)

print(resp.output_text)
```

For more examples, see the [Responses API](../../how-to/responses.md) documentation.

# [Response](#tab/python-output)

```markdown
Here is a summary of Azure Functions based on official Microsoft documentation:

## What is Azure Functions?
Azure Functions is a serverless compute service that enables you to run event-driven code without managing infrastructure. You write code in your preferred language—such as C#, Java, JavaScript, PowerShell, or Python—and Azure Functions handles the hosting, scaling, and maintenance for you. You pay only for the compute time you consume, making it cost-effective for many use cases.

- **Official overview:** [What is Azure Functions?](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)

## Key Scenarios for Azure Functions
Azure Functions supports a wide range of cloud application scenarios, including:

- Processing file uploads from blob storage.
- Real-time stream and event processing (IoT, analytics).
- Executing AI and machine learning inference.
- Running scheduled tasks or background jobs.
- Building scalable web APIs with HTTP endpoints.
- Orchestrating serverless workflows (using Durable Functions).
- Responding to data or database changes.
- Creating reliable message processing systems (with queues, Service Bus, Event Hubs).

Read more about scenarios here: [Azure Functions scenarios](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scenarios).

## How It Works
- **Triggers and Bindings:** Functions are executed by triggers (events like HTTP requests, file uploads, timers, etc.) and can use bindings to automatically interact with other Azure services.
- **Coding:** Write only the code you need for business logic; Azure Functions integrates with IDEs like Visual Studio and VS Code for development and debugging.
- **Monitoring:** Built-in integration with Azure Monitor and Application Insights.
- **Hosting plans:** Choose serverless (Consumption plan), Premium, Dedicated, or deploy in custom containers.

## Getting Started
You can create your first Azure Function quickly using:

- [Azure CLI or Developer CLI](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-azure-developer-cli)
- [Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-functions/how-to-create-function-vs-code)
- [Visual Studio](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-your-first-function-visual-studio)

See quickstarts for all languages: [Getting started with Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-get-started)

## Supported Languages
- Native: C#, Java, JavaScript, PowerShell, Python
- With custom handlers: Go, Rust, and more

## Learn More
- [Overview of Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)
- [Supported languages](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages)
- [Triggers and bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)

Let me know if you're looking for step-by-step tutorials, specific language samples, or deeper technical details!
```

---


## Chat

### chat.completions.create()

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```


# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```

# [Environment Variables](#tab/python-env)

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "When was Microsoft founded?"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```

# [Response](#tab/python-output)

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

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

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

# [API Key](#tab/python-key)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

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

# [Environment Variables](#tab/python-env)

```python
from openai import OpenAI

client = OpenAI()

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

# [Response](#tab/python-output)

```text
Microsoft was founded on April 4, 1975, by Bill Gates and Paul Allen.
```

---

### chat.completions.create() - image input

# [Microsoft Entra ID](#tab/python-entra)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

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

# [API Key](#tab/python-key)


```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

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

# [Environment Variables](#tab/python-env)

```python
from openai import OpenAI

client = OpenAI()

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

# [Response](#tab/python-output)

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

# [Microsoft Entra ID](#tab/python-entra)

Embeddings currently don't support Microsoft Entra ID with Azure OpenAI and the v1 API.

# [API Key](#tab/python-key)

```python
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

embedding = client.embeddings.create(
  model="text-embedding-3-large", # Replace with your model deployment name
  input="Attenion is all you need",
  encoding_format="float" 
)

print(embedding)
```

# [Environment Variables](#tab/python-env)

```python
client = OpenAI()

embedding = client.embeddings.create(
  model="text-embedding-3-large", # Replace with your model deployment name
  input="Attenion is all you need",
  encoding_format="float" 
)

print(embedding)
```

# [Response](#tab/python-output)

The response has been truncated for brevity.

```
CreateEmbeddingResponse(data=[Embedding(embedding=[0.009098228, -0.010369237, -0.00048062875, -0.014328566, 0.019677775, 0.010049199, -0.005600668, 0.003858746, -0.007818076, 0.012554641, 0.005134327, 0.004514824, -0.020262988, -0.0039181816, 0.025475038, 0.016733425, 0.002136255, 0.0155172795, 0.0058978465, 0.012911255, -0.014273703, -0.016806576, 0.0265906, 0.037673064, 0.003909038, 0.0265906, -0.001935088, -0.014913779, 0.01781241, -0.017821554, 0.0016596265, -0.002987785, -0.014346854, -0.000962972, 0.0068671047, 0.004405097, -0.015764166, -0.007539185, -0.030394483, -0.01586475, 0.0074706054, -0.013761641, 0.010186358, 0.008805621, -0.009939471, 0.013944521, -0.010113207, -0.015745878, -0.021927187, 0.03231471, 0.0026951786, 0.004759425, 0.0065196347, 0.010927018, 0.017263774, 0.0055229445, 0.009381691, -0.042903405], index=0, object='embedding')], model='text-embedding-3-large', object='list', usage=Usage(prompt_tokens=7, total_tokens=7))
```

---

## Fine-tuning

[Fine-tuning with Python how-to article](../../how-to/fine-tuning.md)

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

To retrieve the ID of your request, you can use the `_request_id` property, which corresponds to the `x-request-id` response header.

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