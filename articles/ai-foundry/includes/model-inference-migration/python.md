---
title: Include file
description: Include file
author: msakande
ms.reviewer: mopeakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 10/28/2025
ms.custom: include
---

## Setup

Install the OpenAI SDK:

```bash
pip install openai
```

For Microsoft Entra ID authentication, also install:

```bash
pip install azure-identity
```

## Client configuration

# [Azure AI Inference SDK](#tab/azure-ai-inference)

With API key authentication:

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

# [OpenAI SDK](#tab/openai)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://<resource>.openai.azure.com/openai/v1/",
)
```

---

With Microsoft Entra ID authentication:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
)
```

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
```

---

## Responses API

Responses API supports only Azure OpenAI in Foundry Models. For Azure OpenAI models, use the Responses API for chat completions:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support the Responses API.  Use chat completions instead.

# [OpenAI SDK](#tab/openai)

```python
response = client.responses.create(   
    model="gpt-4o-mini", # Your deployment name
    input="This is a test.",
)

print(response.model_dump_json(indent=2))
```

---

## Chat completions

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is Azure AI?"),
    ],
    model="gpt-4o-mini"  # Optional for single-model endpoints
)

print(response.choices[0].message.content)
```

# [OpenAI SDK](#tab/openai)

```python
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # Required: your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure AI?"}
    ]
)

print(completion.choices[0].message.content)
```

---

### Streaming

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Write a poem about Azure."),
    ],
    model="gpt-4o-mini"
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")
```

# [OpenAI SDK](#tab/openai)

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a poem about Azure."}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## Embeddings

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

client = EmbeddingsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)

response = client.embed(
    input=["Your text string goes here"],
    model="text-embedding-3-small"
)

embedding = response.data[0].embedding
```

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

client = OpenAI(
    base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key = token_provider,
)

response = client.embeddings.create(
    input = "How do I use Python in VS Code?",
    model = "text-embedding-3-large" // Use the name of your deployment
)
print(response.data[0].embedding)
```


---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation models.

# [OpenAI SDK](#tab/openai)

OpenAI SDK doesn't support image generation models.

---
