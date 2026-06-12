---
title: Python file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 06/10/2026
ms.custom: include
ai-usage: ai-assisted
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
    "https://ai.azure.com/.default"
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
response = client.chat.completions.create(
    model="DeepSeek-V3.1",  # Required: your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How many languages are in the world?"}
    ]
)

print(response.choices[0].message.content)
```

**Output is as follows:**

```console
Response: As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.

```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
    model="DeepSeek-V3.1"  # Optional for single-model endpoints
)

print(response.choices[0].message.content)
```

**Output is as follows:**

```console
Response: <think>Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...</think>As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
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

## Responses

The Responses API is OpenAI's stateful interface that returns a structured `output` array containing message, tool call, and reasoning items.

# [OpenAI SDK](#tab/openai)

```python
response = client.responses.create(
    model="DeepSeek-V3.1",  # Required: your deployment name
    input="How many languages are in the world?",
    max_output_tokens=2000,
)

print(response.output_text)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To call it, use the OpenAI SDK.

---

### Reasoning

> [!NOTE]
> This information on reasoning content doesn't apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The Responses API surfaces this as a structured `reasoning` output item whose `summary[].text` contains the model's thinking, alongside the final answer.

# [OpenAI SDK](#tab/openai)

```python
response = client.responses.create(
    model="DeepSeek-R1-0528",  # Required: your deployment name
    input="How many languages are in the world?",
    max_output_tokens=2000,
)

# Walk response.output for items of type "reasoning" and join summary[].text.
parts = []
for item in getattr(response, "output", None) or []:
    if getattr(item, "type", None) != "reasoning":
        continue
    for s in getattr(item, "summary", None) or []:
        text = getattr(s, "text", None)
        if text:
            parts.append(text)
reasoning_summary = "\n".join(parts).strip()

print("Thinking:", reasoning_summary)
print("Answer:", response.output_text)
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer: There are approximately 7,000 languages spoken around the world today.
```

[!INCLUDE [reasoning-tokens-known-issue](reasoning-tokens-known-issue.md)]

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To get reasoning content, call the chat completions API instead. The reasoning is included in the message content wrapped in `<think>` and `</think>` tags, which you can extract with a regex match.

```python
import re
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
    model="DeepSeek-R1-0528"  # Optional for single-model endpoints
)

content = response.choices[0].message.content
match = re.match(r"<think>(.*?)</think>(.*)", content, re.DOTALL)
if match:
    print("Thinking:", match.group(1).strip())
    print("Answer: ", match.group(2).strip())
else:
    print("Response:", content)
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:  There are approximately 7,000 languages spoken around the world today.
```

---

When you make multi-turn conversations, avoid sending the reasoning content in the chat history because reasoning tends to generate long explanations.

## Embeddings

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), 
"https://ai.azure.com/.default")

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
