---
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: structured-outputs
ai-usage: ai-assisted
---

## Getting started

# [Python (Microsoft Entra ID)](#tab/python-secure)

You can use [`Pydantic`](https://docs.pydantic.dev/latest/) to define object schemas in Python. Depending on what version of the [OpenAI](https://pypi.org/project/openai/) and [`Pydantic` libraries](https://pypi.org/project/pydantic/) you're running you might need to upgrade to a newer version. These examples were tested against `openai 1.42.0` and `pydantic 2.8.2`.

```cmd
pip install openai pydantic azure-identity --upgrade
```

If you are new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from pydantic import BaseModel
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

print(event)
print(completion.model_dump_json(indent=2))
```

### Output

```json
name='Science Fair' date='Friday' participants=['Alice', 'Bob']
{
  "id": "chatcmpl-A1EUP2fAmL4SeB1lVMinwM7I2vcqG",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "{\n  \"name\": \"Science Fair\",\n  \"date\": \"Friday\",\n  \"participants\": [\"Alice\", \"Bob\"]\n}",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": [],
        "parsed": {
          "name": "Science Fair",
          "date": "Friday",
          "participants": [
            "Alice",
            "Bob"
          ]
        }
      }
    }
  ],
  "created": 1724857389,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_1c2eaec9fe",
  "usage": {
    "completion_tokens": 27,
    "prompt_tokens": 32,
    "total_tokens": 59
  }
}
```

# [Python (key-based auth)](#tab/python)

You can use [`Pydantic`](https://docs.pydantic.dev/latest/) to define object schemas in Python. Depending on what version of the [OpenAI](https://pypi.org/project/openai/) and [`Pydantic` libraries](https://pypi.org/project/pydantic/) you're running you might need to upgrade to a newer version. These examples were tested against `openai 1.42.0` and `pydantic 2.8.2`.

```cmd
pip install openai pydantic --upgrade
```

```python
import os
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

print(event)
print(completion.model_dump_json(indent=2))
```

### Output

```json
name='Science Fair' date='Friday' participants=['Alice', 'Bob']
{
  "id": "chatcmpl-A1EUP2fAmL4SeB1lVMinwM7I2vcqG",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "{\n  \"name\": \"Science Fair\",\n  \"date\": \"Friday\",\n  \"participants\": [\"Alice\", \"Bob\"]\n}",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": [],
        "parsed": {
          "name": "Science Fair",
          "date": "Friday",
          "participants": [
            "Alice",
            "Bob"
          ]
        }
      }
    }
  ],
  "created": 1724857389,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_1c2eaec9fe",
  "usage": {
    "completion_tokens": 27,
    "prompt_tokens": 32,
    "total_tokens": 59
  }
}
```

---

## Function calling with structured outputs

Structured Outputs for function calling can be enabled with a single parameter, by supplying `strict: true`. 

> [!NOTE]
> Structured outputs are not supported with parallel function calls. When using structured outputs set `parallel_tool_calls` to `false`.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
import openai
from pydantic import BaseModel
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

class GetDeliveryDate(BaseModel):
    order_id: str

tools = [openai.pydantic_function_tool(GetDeliveryDate)]

messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order #12345?"}) 

response = client.chat.completions.create(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=messages,
    tools=tools
)

print(response.choices[0].message.tool_calls[0].function)
print(response.model_dump_json(indent=2))
```

# [Python (key-based auth)](#tab/python)

```python
import os
from pydantic import BaseModel
import openai
from openai import OpenAI

client = OpenAI(
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)


class GetDeliveryDate(BaseModel):
    order_id: str

tools = [openai.pydantic_function_tool(GetDeliveryDate)]

messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order #12345?"}) 

response = client.chat.completions.create(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=messages,
    tools=tools
)

print(response.choices[0].message.tool_calls[0].function)
print(response.model_dump_json(indent=2))
```
