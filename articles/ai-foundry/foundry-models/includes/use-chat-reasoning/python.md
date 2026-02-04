---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/27/2025
ms.author: mopeakande
author: msakande
ms.reviewer: balapv
reviewer: balapv
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use the reasoning capabilities of chat completions models deployed in Microsoft Foundry Models.

[!INCLUDE [about-reasoning](about-reasoning.md)]

## Prerequisites

To complete this tutorial, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-openai-python](../how-to-prerequisites-openai-python.md)]

* A model with reasoning capabilities model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a reasoning model. 

  * This example uses `DeepSeek-R1`.

## Use reasoning capabilities with chat

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

# [OpenAI API](#tab/openai)

```python
import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    azure_endpoint = "https://<resource>.services.ai.azure.com",
    api_key=os.getenv("AZURE_INFERENCE_CREDENTIAL"),  
    api_version="2024-10-21",
)
```

# [Model Inference API (preview)](#tab/inference)

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    model="deepseek-r1"
)
```
---

If you have configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

# [OpenAI API](#tab/openai)

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint = "https://<resource>.services.ai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
)
```

# [Model Inference API (preview)](#tab/inference)

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=DefaultAzureCredential(),
    credential_scopes=["https://cognitiveservices.azure.com/.default"],
    model="deepseek-r1"
)
```
---

[!INCLUDE [best-practices](best-practices.md)]

### Create a chat completion request

The following example shows how you can create a basic chat request to the model.

# [OpenAI API](#tab/openai)

```python
response = client.chat.completions.create(
    model="deepseek-r1",
    messages=[
        {"role": "user", "content": "How many languages are in the world?"}
    ]
)
```

# [Model Inference API (preview)](#tab/inference)

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        UserMessage(content="How many languages are in the world?"),
    ],
)
```
---

The response is as follows, where you can see the model's usage statistics:

# [OpenAI API](#tab/openai)

```python
print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
```

```console
Response: As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: deepseek-r1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```

# [Model Inference API (preview)](#tab/inference)

```python
print("Response:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
```

```console
Response: <think>Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...</think>As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: deepseek-r1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```
---

### Reasoning content

> [!NOTE]
> This information on reasoning content does not apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind it. 

# [OpenAI API](#tab/openai)

The reasoning associated with the completion is included in the field `reasoning_content`. The model may select on which scenarios to generate reasoning content. 

```python
print("Thinking:", response.choices[0].message.reasoning_content)
```

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
```

# [Model Inference API (preview)](#tab/inference)

The reasoning associated with the completion is included in the response's content within the tags `<think>` and `</think>`. The model may select on which scenarios to generate reasoning content. You can extract the reasoning content from the response to understand the model's thought process as follows:

```python
import re

match = re.match(r"<think>(.*?)</think>(.*)", response.choices[0].message.content, re.DOTALL)

if match:
    print("\tThinking:", match.group(1))
else:
    print("\tAnswer:", response.choices[0].message.content)
```

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start...
```
---

When making multi-turn conversations, it's useful to avoid sending the reasoning content in the chat history as reasoning tends to generate long explanations.

### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.

To stream completions, set `stream=True` when you call the model.

# [OpenAI API](#tab/openai)

```python
response = client.chat.completions.create(
    model="deepseek-r1",
    messages=[
        {"role": "user", "content": "How many languages are in the world?"}
    ],
    stream=True
)
```

# [Model Inference API (preview)](#tab/inference)

```python
response = client.complete(
    model="deepseek-r1",
    messages=[
        UserMessage(content="How many languages are in the world?"),
    ],
    max_tokens=2048,
    stream=True,
)
```
---

To visualize the output, define a helper function to print the stream. The following example implements a routing that stream only the answer without the reasoning content:

# [OpenAI API](#tab/openai)

Reasoning content is also included inside of the delta pieces of the response, in the key `reasoning_content`.

```python
def print_stream(completion):
    """
    Prints the chat completion with streaming.
    """
    is_thinking = False
    for event in completion:
        if event.choices:
            content = event.choices[0].delta.content
            reasoning_content = event.choices[0].delta.reasoning_content if hasattr(event.choices[0].delta, "reasoning_content") else None
            if reasoning_content and not is_thinking:
                is_thinking = True
                print("🧠 Thinking...", end="", flush=True)
            elif content:
                if is_thinking:
                    is_thinking = False
                    print("🛑\n\n")
            print(content or reasoning_content, end="", flush=True)

print_stream(response)
```

# [Model Inference API (preview)](#tab/inference)

When streaming, pay closer attention to the `<think>` tag that may be included inside of the `content` field.

```python
def print_stream(completion):
    """
    Prints the chat completion with streaming.
    """
    is_thinking = False
    for event in completion:
        if event.choices:
            content = event.choices[0].delta.content
            if content == "<think>":
                is_thinking = True
                print("🧠 Thinking...", end="", flush=True)
            elif content == "</think>":
                is_thinking = False
                print("🛑\n\n")
            elif content:
                print(content, end="", flush=True)
```
---

You can visualize how streaming generates content:


```python
print_stream(response)
```

### Parameters

In general, reasoning models don't support the following parameters you can find in chat completion models:

* Temperature
* Presence penalty
* Repetition penalty
* Parameter `top_p`

Some models support the use of tools or structured outputs (including JSON-schemas). Read the [Models](../../concepts/models-sold-directly-by-azure.md) details page to understand each model's support.

### Apply Guardrails and controls

The Azure AI Model Inference API supports [Azure AI Content Safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI Content Safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt.

# [OpenAI API](#tab/openai)

```python
try:
    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "user", "content": "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."}
        ],
    )

    print(response.choices[0].message.content)

except HttpResponseError as ex:
    if ex.status_code == 400:
        response = ex.response.json()
        if isinstance(response, dict) and "error" in response:
            print(f"Your request triggered an {response['error']['code']} error:\n\t {response['error']['message']}")
        else:
            raise
    raise
```

# [Model Inference API (preview)](#tab/inference)

```python
from azure.ai.inference.models import AssistantMessage, UserMessage

try:
    response = client.complete(
        model="deepseek-r1",
        messages=[
            UserMessage(content="Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."),
        ],
    )

    print(response.choices[0].message.content)

except HttpResponseError as ex:
    if ex.status_code == 400:
        response = ex.response.json()
        if isinstance(response, dict) and "error" in response:
            print(f"Your request triggered an {response['error']['code']} error:\n\t {response['error']['message']}")
        else:
            raise
    raise
```
---

> [!TIP]
> To learn more about how you can configure and control Azure AI Content Safety settings, check the [Azure AI Content Safety documentation](https://aka.ms/azureaicontentsafety).
