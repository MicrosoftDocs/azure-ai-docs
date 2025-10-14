---
title: How to use chat completions with Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to generate chat completions with Azure AI Foundry Models
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use the chat completions API with models deployed in Azure AI Foundry Models.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A chat completions model deployment. If you don't have one, see [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.


## Use chat completions

For Azure OpenAI in Foundry Models, we recommend using the [Responses API](../../../openai/supported-languages.md), however, the v1 API also allows you to make chat completions calls with models from other Models sold directly by Azure, such as DeepSeek and Grok models, which support the OpenAI v1 chat completions syntax.

In the following examples, you first create the client to consume the model. Then, create a basic request to the model. When you're creating the client, `base_url` will accept both `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/` and `https://YOUR-RESOURCE-NAME.services.ai.azure.com/openai/v1/` formats.

### Use the chat completions API

The following code uses an endpoint URL and **API Key** that are stored in environment variables to create the client.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
)

completion = client.chat.completions.create(
  model="grok-3-mini", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about the attention is all you need paper"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```

- `OpenAI()` client is used instead of `AzureOpenAI()`.
- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `api-version` is no longer a required parameter with the v1 GA API.

**API Key** with environment variables set for `OPENAI_BASE_URL` and `OPENAI_API_KEY`:

```python
client = OpenAI()
```


The following code uses **Microsoft Entra ID** to create the client.

> [!IMPORTANT]
> Handling automatic token refresh was previously handled through use of the `AzureOpenAI()` client. The v1 API removes this dependency, by adding automatic token refresh support to the `OpenAI()` client.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key = token_provider  
)

completion = client.chat.completions.create(
  model="grok-3-mini", # Replace with your model deployment name.
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me about the attention is all you need paper"}
  ]
)

#print(completion.choices[0].message)
print(completion.model_dump_json(indent=2))
```

- `base_url` passes the Azure OpenAI endpoint and `/openai/v1` is appended to the endpoint address.
- `api_key` parameter is set to `token_provider`, enabling automatic retrieval and refresh of an authentication token instead of using a static API key.

### Using the responses API

This code shows how to ese an Azure OpenAI model with the recommended [Responses API](../../../openai/supported-languages.md).

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key = token_provider  
)

response = client.responses.create(
    model="gpt-4.1-nano",
    input= "This is a test" 
)

print(response.model_dump_json(indent=2)) 
```


To see more details about how to use chat completions, see [Work with chat completions models](../../../openai/how-to/chatgpt.md).


