---
title: Python file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 11/05/2025
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

# [OpenAI SDK](#tab/openai)

With API key authentication:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://<resource>.openai.azure.com/openai/v1/",
)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

---

With Microsoft Entra ID authentication:

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=token_provider,
)
```

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

---

## Chat completions

# [OpenAI SDK](#tab/openai)

```python
completion = client.chat.completions.create(
    model="DeepSeek-V3.1",  # Required: your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Azure AI?"}
    ]
)

print(completion.choices[0].message.content)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="What is Azure AI?"),
    ],
    model="DeepSeek-V3.1"  # Optional for single-model endpoints
)

print(response.choices[0].message.content)
```

---

### Streaming

# [OpenAI SDK](#tab/openai)

```python
stream = client.chat.completions.create(
    model="DeepSeek-V3.1",
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

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    stream=True,
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Write a poem about Azure."),
    ],
    model="DeepSeek-V3.1"
)

for update in response:
    if update.choices:
        print(update.choices[0].delta.content or "", end="")
```

---

## Embeddings

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), 
"https://cognitiveservices.azure.com/.default")

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

---
