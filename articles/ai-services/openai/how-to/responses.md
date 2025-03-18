---
title: Azure OpenAI Responses API
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's new stateful Responses API.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/07/2025
author: mrbullwinkle    
ms.author: mbullwin
ms.custom: references_regions
---

# Azure OpenAI Responses API (Preview)

The Responses API is a new stateful API from Azure OpenAI. It brings together the best capabilities from the chat completions and assistants API in one unified experience. The Responses API also adds support for the new `computer-use-preview` model which powers the [Computer Use](./computer-use.md) tool.

## Responses API

### API support

`2025-03-01-preview` or later

### Region Availability

The responses API is currently available in the following regions:

- australiaeast
- eastus
- eastus2
- francecentral
- japaneast
- norwayeast
- southindia
- swedencentral
- uaenorth
- uksouth
- westus
- westus3

### Model support

- `o1`
- `o1-preview`
- `o1-mini`
- `o3-mini`
- `gpt-4o`
- `gpt-4o-mini`
- `computer-use-preview`

## Getting started with the responses API

To access the responses API commands you may need to upgrade your version of the OpenAI library.

```cmd
pip install --upgrade openai
```

## Generate a text response

# [Python (Microsoft Entra ID)](#tab/python-secure)

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

response = client.responses.create(
    model="gpt-4o", # replace with your model deployment name 
    input="This is a test."

)
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-03-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

response = client.responses.create(
    model="gpt-4o", # replace with your model deployment name 
    input="This is a test."

)
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-03-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

### API Key

```bash
curl -X https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses?api-version=2025-03-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

# [Output](#tab/output)

**Output:**

```json
{
  "id": "resp_67cb32528d6881909eb2859a55e18a85",
  "created_at": 1741369938.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cb3252cfac8190865744873aada798",
      "content": [
        {
          "annotations": [],
          "text": "Great! How can I help you today?",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "output_text": "Great! How can I help you today?",
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 20,
    "output_tokens": 11,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 31
  },
  "user": null,
  "reasoning_effort": null
}
```

---

## Retrieve a response

To retrieve a response from a previous call to the responses API.

# [Python (Microsoft Entra ID)](#tab/python-secure)

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

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2025-03-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X GET "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/{response_id}?api-version=2025-03-01-preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" 
```

### API Key

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/responses/{response_id}?api-version=2025-03-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" 
```

# [Output](#tab/output)

```json
{
  "id": "resp_67cb61fa3a448190bcf2c42d96f0d1a8",
  "created_at": 1741382138.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cb61fa95588190baf22ffbdbbaaa9d",
      "content": [
        {
          "annotations": [],
          "text": "Hello! How can I assist you today?",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": null,
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 20,
    "output_tokens": 11,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 31
  },
  "user": null,
  "reasoning_effort": null
}
```

---

## Delete response

By default response data is retained for 30 days. To delete a response you can use `response.del("{response_id})`

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

response = client.responses.del("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response.model_dump_json(indent=2))
```

## Chaining responses together

You can chain responses together by passing the `response.id` from the previous response to the `previous_response_id` parameter.

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

response = client.responses.create(
    model="gpt-4o",  # replace with your model deployment name
    input="Define and explain the concept of catastrophic forgetting?"
)

second_response = client.responses.create(
    model="gpt-4o",  # replace with your model deployment name
    previous_response_id=response.id,
    input=[{"role": "user", "content": "Explain this at a level that could be understood by a college freshman"}]
)
print(second_response.model_dump_json(indent=2)) 
```

Note from the output that even though we never shared the first input question with the `second_response` API call, by passing the `previous_response_id` the model has full context of previous question and response to answer the new question.

**Output:**

```json
{
  "id": "resp_67cbc9705fc08190bbe455c5ba3d6daf",
  "created_at": 1741408624.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-4o-2024-08-06",
  "object": "response",
  "output": [
    {
      "id": "msg_67cbc970fd0881908353a4298996b3f6",
      "content": [
        {
          "annotations": [],
          "text": "Sure! Imagine you are studying for exams in different subjects like math, history, and biology. You spend a lot of time studying math first and get really good at it. But then, you switch to studying history. If you spend all your time and focus on history, you might forget some of the math concepts you learned earlier because your brain fills up with all the new history facts. \n\nIn the world of artificial intelligence (AI) and machine learning, a similar thing can happen with computers. We use special programs called neural networks to help computers learn things, sort of like how our brain works. But when a neural network learns a new task, it can forget what it learned before. This is what we call \"catastrophic forgetting.\"\n\nSo, if a neural network learned how to recognize cats in pictures, and then you teach it how to recognize dogs, it might get really good at recognizing dogs but suddenly become worse at recognizing cats. This happens because the process of learning new information can overwrite or mess with the old information in its \"memory.\"\n\nScientists and engineers are working on ways to help computers remember everything they learn, even as they keep learning new things, just like students have to remember math, history, and biology all at the same time for their exams. They use different techniques to make sure the neural network doesn’t forget the important stuff it learned before, even when it gets new information.",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": null,
      "type": "message"
    }
  ],
  "parallel_tool_calls": null,
  "temperature": 1.0,
  "tool_choice": null,
  "tools": [],
  "top_p": 1.0,
  "max_output_tokens": null,
  "previous_response_id": "resp_67cbc96babbc8190b0f69aedc655f173",
  "reasoning": null,
  "status": "completed",
  "text": null,
  "truncation": null,
  "usage": {
    "input_tokens": 405,
    "output_tokens": 285,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 690
  },
  "user": null,
  "reasoning_effort": null
}
```

### Chaining responses manually

Alternatively you can manually chain responses together using the method below:

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


inputs = [{"type": "message", "role": "user", "content": "Define and explain the concept of catastrophic forgetting?"}] 
  
response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    input="inputs"  
)  
  
inputs += response.output

inputs.append({"role": "user", "type": "message", "content": "Explain this at a level that could be understood by a college freshman"}) 
               

second_response = client.responses.create(  
    model="gpt-4o",  
    previous_response_id=response.id,  
    input=inputs
)  
      
print(second_response.model_dump_json(indent=2))  
```

## Function calling

The responses API supports function calling.

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

response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    tools=[  
        {  
            "type": "function",  
            "name": "get_weather",  
            "description": "Get the weather for a location",  
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "location": {"type": "string"},  
                },  
                "required": ["location"],  
            },  
        }  
    ],  
    input=[{"role": "user", "content": "What's the weather in San Francisco?"}],  
)  

print(response.model_dump_json(indent=2))  
  
# To provide output to tools, add a response for each tool call to an array passed  
# to the next response as `input`  
input = []  
for output in response.output:  
    if output.type == "function_call":  
        match output.name:  
            case "get_weather":  
                input.append(  
                    {  
                        "type": "function_call_output",  
                        "call_id": output.id,  
                        "output": '{"temperature": "70 degrees"}',  
                    }  
                )  
            case _:  
                raise ValueError(f"Unknown function call: {output.name}")  
  
second_response = client.responses.create(  
    model="gpt-4o",  
    previous_response_id=response.id,  
    input=input  
)  

print(second_response.model_dump_json(indent=2)) 

```
