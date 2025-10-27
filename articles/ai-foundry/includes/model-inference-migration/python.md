## Benefits of migrating

Migrating to the OpenAI v1 SDK provides several advantages:

- **Unified API**: Use the same SDK for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **No API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters
- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok

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

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

# [OpenAI v1 SDK](#tab/openai)

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://<resource>.openai.azure.com/openai/v1/",
)
```

---

With Microsoft Entra ID:

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

# [OpenAI v1 SDK](#tab/openai)

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

---

## Responses API

For Azure OpenAI models, use the Responses API for chat completions:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support the Responses API. Use chat completions instead.

# [OpenAI v1 SDK](#tab/openai)

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

# [OpenAI v1 SDK](#tab/openai)

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

# [OpenAI v1 SDK](#tab/openai)

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

# [OpenAI v1 SDK](#tab/openai)

```python
response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"  # Your deployment name
)

embedding = response.data[0].embedding
```

---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation. Use OpenAI SDK instead.

# [OpenAI v1 SDK](#tab/openai)

```python
response = client.images.generate(
    model="dall-e-3",  # Your deployment name
    prompt="a happy monkey eating a banana, in watercolor",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
print(f"Generated image available at: {image_url}")
```

---

## Error handling

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.core.exceptions import HttpResponseError

try:
    response = client.complete(
        messages=[{"role": "user", "content": "Hello"}],
        model="gpt-4o-mini"
    )
except HttpResponseError as error:
    print(f"Request failed: {error.status_code}")
    print(f"Error message: {error.message}")
```

# [OpenAI v1 SDK](#tab/openai)

```python
from openai import OpenAIError, RateLimitError, APIError

try:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    print(f"API error: {e}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

---
