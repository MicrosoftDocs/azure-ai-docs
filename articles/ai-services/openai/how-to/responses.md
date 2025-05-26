---
title: Azure OpenAI Responses API
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's new stateful Responses API.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 05/25/2025
author: mrbullwinkle    
ms.author: mbullwin
ms.custom: references_regions
---

# Azure OpenAI Responses API (Preview)

The Responses API is a new stateful API from Azure OpenAI. It brings together the best capabilities from the chat completions and assistants API in one unified experience. The Responses API also adds support for the new `computer-use-preview` model which powers the [Computer use](../how-to/computer-use.md) capability.

## Responses API

### API support

- [v1 preview API is required for access to the latest features](../api-version-lifecycle.md#api-evolution)

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

- `gpt-4o` (Versions: `2024-11-20`, `2024-08-06`, `2024-05-13`)
- `gpt-4o-mini` (Version: `2024-07-18`)
- `computer-use-preview`
- `gpt-4.1` (Version: `2025-04-14`)
- `gpt-4.1-nano` (Version: `2025-04-14`)
- `gpt-4.1-mini` (Version: `2025-04-14`)
- `gpt-image-1` (Version: `2025-04-15`)
- `o3` (Version: `2025-04-16`)
- `o4-mini` (Version: `2025-04-16`)

Not every model is available in the regions supported by the responses API. Check the [models page](../concepts/models.md) for model region availability.

> [!NOTE]
> Not currently supported:
> - The web search tool
> - Fine-tuned models
>

### Reference documentation

- [Responses API reference documentation](/azure/ai-services/openai/reference-preview-latest?#responses-api---create)

## Getting started with the responses API

To access the responses API commands, you need to upgrade your version of the OpenAI library.

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
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)

response = client.responses.create(
    model="gpt-4.1-nano",
    input= "This is a test" 
)

print(response.model_dump_json(indent=2)) 
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    default_query={"api-version": "preview"}, 
)

response = client.responses.create(   
  model="gpt-4.1-nano", # Replace with your model deployment name 
  input="This is a test.",
)

print(response.model_dump_json(indent=2)) 
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
     "model": "gpt-4o",
     "input": "This is a test"
    }'
```

### API Key

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
     "model": "gpt-4.1-nano",
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
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response.model_dump_json(indent=2))
```

# [Python (API Key)](#tab/python-key)

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    default_query={"api-version": "preview"}, 
)

response = client.responses.retrieve("resp_67cb61fa3a448190bcf2c42d96f0d1a8")
```

# [REST API](#tab/rest-api)

### Microsoft Entra ID

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/{response_id}?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" 
```

### API Key

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/{response_id}?api-version=preview \
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

By default response data is retained for 30 days. To delete a response, you can use `response.delete"("{response_id})`

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

response = client.responses.delete("resp_67cb61fa3a448190bcf2c42d96f0d1a8")

print(response)
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
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
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
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)


inputs = [{"type": "message", "role": "user", "content": "Define and explain the concept of catastrophic forgetting?"}] 
  
response = client.responses.create(  
    model="gpt-4o",  # replace with your model deployment name  
    input=inputs  
)  
  
inputs += response.output

inputs.append({"role": "user", "type": "message", "content": "Explain this at a level that could be understood by a college freshman"}) 
               

second_response = client.responses.create(  
    model="gpt-4o",  
    input=inputs
)  
      
print(second_response.model_dump_json(indent=2))  
```

## Streaming

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
    input = "This is a test",
    model = "o4-mini", # replace with model deployment name
    stream = True
)

for event in response:
    if event.type == 'response.output_text.delta':
        print(event.delta, end='')

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
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
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
                        "call_id": output.call_id,  
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

## List input items

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

response = client.responses.input_items.list("resp_67d856fcfba0819081fd3cffee2aa1c0")

print(response.model_dump_json(indent=2))
```

**Output:**

```json
{
  "data": [
    {
      "id": "msg_67d856fcfc1c8190ad3102fc01994c5f",
      "content": [
        {
          "text": "This is a test.",
          "type": "input_text"
        }
      ],
      "role": "user",
      "status": "completed",
      "type": "message"
    }
  ],
  "has_more": false,
  "object": "list",
  "first_id": "msg_67d856fcfc1c8190ad3102fc01994c5f",
  "last_id": "msg_67d856fcfc1c8190ad3102fc01994c5f"
}
```

## Image input

### Image url

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
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what is in this image?" },
                {
                    "type": "input_image",
                    "image_url": "<image_URL>"
                }
            ]
        }
    ]
)

print(response)

```

### Base64 encoded image

```python
import base64
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

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "path_to_your_image.jpg"

# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what is in this image?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]
)

print(response)
```

## Using remote MCP servers

You can extend the capabilities of your model by connecting it to tools hosted on remote Model Context Protocol (MCP) servers. These servers are maintained by developers and organizations and expose tools that can be accessed by MCP-compatible clients, such as the Responses API.

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open standard that defines how applications provide tools and contextual data to large language models (LLMs). It enables consistent, scalable integration of external tools into model workflows.

The following example demonstrates how to use the fictitious MCP server to query information about the Azure REST API. This allows the model to retrieve and reason over repository content in real time.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
  "model": "gpt-4.1",
  "tools": [
    {
      "type": "mcp",
      "server_label": "github",
      "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
      "require_approval": "never"
    }
  ],
  "input": "What is this repo in 100 words?"
}'
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
    model="gpt-4.1", # replace with your model deployment name 
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
            "require_approval": "never"
        },
    ],
    input="What transport protocols are supported in the 2025-03-26 version of the MCP spec?",
)

print(response.output_text)
```

The MCP tool works only in the Responses API, and is available across all newer models (gpt-4o, gpt-4.1, and our reasoning models). When you're using the MCP tool, you only pay for tokens used when importing tool definitions or making tool calls—there are no additional fees involved.

### Approvals

By default, the Responses API requires explicit approval before any data is shared with a remote MCP server. This approval step helps ensure transparency and gives you control over what information is sent externally.

We recommend reviewing all data being shared with remote MCP servers and optionally logging it for auditing purposes.

When an approval is required, the model returns a `mcp_approval_request` item in the response output. This object contains the details of the pending request and allows you to inspect or modify the data before proceeding.

```json
{
  "id": "mcpr_682bd9cd428c8198b170dc6b549d66fc016e86a03f4cc828",
  "type": "mcp_approval_request",
  "arguments": {},
  "name": "fetch_azure_rest_api_docs",
  "server_label": "github"
}
```

To proceed with the remote MCP call, you must respond to the approval request by creating a new response object that includes an mcp_approval_response item. This object confirms your intent to allow the model to send the specified data to the remote MCP server.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
  "model": "gpt-4.1",
  "tools": [
    {
      "type": "mcp",
      "server_label": "github",
      "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
      "require_approval": "never"
    }
  ],
  "previous_response_id": "resp_682f750c5f9c8198aee5b480980b5cf60351aee697a7cd77",
  "input": [{
    "type": "mcp_approval_response",
    "approve": true,
    "approval_request_id": "mcpr_682bd9cd428c8198b170dc6b549d66fc016e86a03f4cc828"
  }]
}'
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
    model="gpt-4.1", # replace with your model deployment name 
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
            "require_approval": "never"
        },
    ],
    previous_response_id="resp_682f750c5f9c8198aee5b480980b5cf60351aee697a7cd77",
    input=[{
        "type": "mcp_approval_response",
        "approve": True,
        "approval_request_id": "mcpr_682bd9cd428c8198b170dc6b549d66fc016e86a03f4cc828"
    }],
)
```

### Authentication

Unlike the GitHub MCP server, most remote MCP servers require authentication. The MCP tool in the Responses API supports custom headers, allowing you to securely connect to these servers using the authentication scheme they require.

You can specify headers such as API keys, OAuth access tokens, or other credentials directly in your request. The most commonly used header is the `Authorization` header.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "gpt-4.1",
        "input": "What is this repo in 100 words?"
        "tools": [
            {
                "type": "mcp",
                "server_label": "github",
                "server_url": "https://contoso.com/Azure/azure-rest-api-specs",
                "headers": {
                    "Authorization": "Bearer $YOUR_API_KEY"
            }
        ]
    }'
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
    model="gpt-4.1",
    input="What is this repo in 100 words?",
    tools=[
        {
            "type": "mcp",
            "server_label": "github",
            "server_url": "https://gitmcp.io/Azure/azure-rest-api-specs",
            "headers": {
                "Authorization": "Bearer $YOUR_API_KEY"
        }
    ]
)

print(response.output_text)
```

## Background tasks

Background mode allows you to run long-running tasks asynchronously using models like o3 and o1-pro. This is especially useful for complex reasoning tasks that may take several minutes to complete, such as those handled by agents like Codex or Deep Research.

By enabling background mode, you can avoid timeouts and maintain reliability during extended operations. When a request is sent with `"background": true`, the task is processed asynchronously, and you can poll for its status over time.

To start a background task, set the background parameter to true in your request:

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "o3",
    "input": "Write me a very long story",
    "background": true
  }'
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
    model = "o3",
    input = "Write me a very long story",
    background = True
)

print(response.status)
```

Use the `GET` endpoint to check the status of a background response. Continue polling while the status is queued or in_progress. Once the response reaches a final (terminal) state, it will be available for retrieval.

```bash
curl GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/resp_1234567890?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
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
    model = "o3",
    input = "Write me a very long story",
    background = True
)

while response.status in {"queued", "in_progress"}:
    print(f"Current status: {resp.status}")
    sleep(2)
    response = client.responses.retrieve(response.id)

print(f"Final status: {response.status}\nOutput:\n{response.output_text}")
```

You can cancel an in-progress background task using the cancel endpoint. Canceling is idempotent—subsequent calls will return the final response object.

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/resp_1234567890/cancel?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
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

response = client.responses.cancel("resp_1234567890")

print(response.status)
```

### Stream a background response

To stream a background response, set both `background` and `stream` to true. This is useful if you want to resume streaming later in case of a dropped connection. Use the sequence_number from each event to track your position.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "o3",
    "input": "Write me a very long story",
    "background": true,
    "stream": true
  }'

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

# Fire off an async response but also start streaming immediately
stream = client.responses.create(
    model="o3",
    input="Write me a very long story",
    background=True,
    stream=True,
)

cursor = None
for event in stream:
    print(event)
    cursor = event["sequence_number"]
```

> [!NOTE] 
> Background responses currently have a higher time-to-first-token latency than synchronous responses. Improvements are underway to reduce this gap.

### Limitations

* Background mode requires `store=true`. Stateless requests are not supported.
* You can only resume streaming if the original request included `stream=true`.
* To cancel a synchronous response, terminate the connection directly.

### Resume streaming from a specific point

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/resp_1234567890?stream=true&starting_after=42&api-version=2025-04-01-preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```

## Encrypted Reasoning Items

When using the Responses API in stateless mode — either by setting `store` to false or when your organization is enrolled in zero data retention — you must still preserve reasoning context across conversation turns. To do this, include encrypted reasoning items in your API requests.

To retain reasoning items across turns, add `reasoning.encrypted_content` to the `include` parameter in your request. This ensures that the response includes an encrypted version of the reasoning trace, which can be passed along in future requests.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "o4-mini",
    "reasoning": {"effort": "medium"},
    "input": "What is the weather like today?",
    "tools": [<YOUR_FUNCTION GOES HERE>],
    "include": ["reasoning.encrypted_content"]
  }'
```

## Image Generation

The Responses API enables image generation as part of conversations and multi-step workflows. It supports image inputs and outputs within context and includes built-in tools for generating and editing images.

Compared to the standalone Image API, the Responses API offers several advantages:

* **Multi-turn editing**: Iteratively refine and edit images using natural language prompts.
* **Streaming**: Display partial image outputs during generation to improve perceived latency.
* **Flexible inputs**: Accept image File IDs as inputs, in addition to raw image bytes.

> [!NOTE]
> The image generation tool in the Responses API is only supported by the `gpt-image-1` model. You can however call this model from this list of supported models - `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`.

Use the Responses API if you want to:

* Build conversational image experiences with GPT Image.
* Enable iterative image editing through multi-turn prompts.
* Stream partial image results during generation for a smoother user experience.

Generate an image


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
    model="o3",
    input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
    tools=[{"type": "image_generation"}],
)

# Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]
    
if image_data:
    image_base64 = image_data[0]
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
```

You can perform multi-turn image generation by using the output of image generation in subsequent calls or just using the `1previous_response_id`.

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

image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]

    with open("cat_and_otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))


# Follow up

response_followup = client.responses.create(
    model="gpt-4.1-mini",
    previous_response_id=response.id,
    input="Now make it look realistic",
    tools=[{"type": "image_generation"}],
)

image_data_followup = [
    output.result
    for output in response_followup.output
    if output.type == "image_generation_call"
]

if image_data_followup:
    image_base64 = image_data_followup[0]
    with open("cat_and_otter_realistic.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
```

### Streaming

You can stream partial images using Responses API. The `partial_images` can be used to receive 1-3 partial images

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

stream = client.responses.create(
    model="gpt-4.1",
    input="Draw a gorgeous image of a river made of white owl feathers, snaking its way through a serene winter landscape",
    stream=True,
    tools=[{"type": "image_generation", "partial_images": 2}],
)

for event in stream:
    if event.type == "response.image_generation_call.partial_image":
        idx = event.partial_image_index
        image_base64 = event.partial_image_b64
        image_bytes = base64.b64decode(image_base64)
        with open(f"river{idx}.png", "wb") as f:
            f.write(image_bytes)
```


### Edit images

```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import base64

client = AzureOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  azure_ad_token_provider=token_provider,
  api_version="preview"
)

def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

def encode_image(file_path):
    with open(file_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    return base64_image

prompt = """Generate a photorealistic image of a gift basket on a white background 
labeled 'Relax & Unwind' with a ribbon and handwriting-like font, 
containing all the items in the reference pictures."""

base64_image1 = encode_image("image1.png")
base64_image2 = encode_image("image2.png")
file_id1 = create_file("image3.png")
file_id2 = create_file("image4.png")

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image1}",
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image2}",
                },
                {
                    "type": "input_image",
                    "file_id": file_id1,
                },
                {
                    "type": "input_image",
                    "file_id": file_id2,
                }
            ],
        }
    ],
    tools=[{"type": "image_generation"}],
)

image_generation_calls = [
    output
    for output in response.output
    if output.type == "image_generation_call"
]

image_data = [output.result for output in image_generation_calls]

if image_data:
    image_base64 = image_data[0]
    with open("gift-basket.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
else:
    print(response.output.content)
```


## Reasoning models

For examples of how to use reasoning models with the responses API see the [reasoning models guide](./reasoning.md#reasoning-summary).

## Computer use

Computer use with Playwright has moved to the [dedicated computer use model guide](./computer-use.md#playwright-integration)