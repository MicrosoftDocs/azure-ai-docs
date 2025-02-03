---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/31/2025
ms.author: fasantia
author: santiagxf
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use the reasoning capabilities of chat completions models deployed to Azure AI model inference in Azure AI services.

## Prerequisites

To complete this tutorial, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A model with reasoning capabilities model deployment. If you don't have one read [Add and configure models to Azure AI services](../../how-to/create-model-deployments.md) to add a reasoning model. 

  * This examples uses `DeepSeek-R1`.

* Install the Azure AI inference package with the following command:

  ```bash
  pip install -U azure-ai-inference
  ```
  
  > [!TIP]
  > Read more about the [Azure AI inference package and reference](https://aka.ms/azsdk/azure-ai-inference/python/reference).

## Use reasoning capabilities with chat

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    model="deepseek-r1"
)
```

> [!TIP]
> Verify that you have deployed the model to Azure AI Services resource with the Azure AI model inference API. `Deepseek-R1` is also available as Serverless API Endpoints. However, those endpoints doesn't take the parameter `model` as explained in this tutorial. You can verify that by going to [Azure AI Foundry portal]() > Models + endpoints, and verify that the model is listed under the section **Azure AI Services**.

If you have configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="mistral-large-2407"
)
```

### Create a chat completion request

The following example shows how you can create a basic reasoning capabilities with chat request to the model.

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
)
```

> [!NOTE]
> Some models don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

The response is as follows, where you can see the model's usage statistics:


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
Model: mistral-large-2407
Usage: 
  Prompt tokens: 19
  Total tokens: 91
  Completion tokens: 72
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.

To stream completions, set `stream=True` when you call the model.


```python
result = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
    temperature=0,
    top_p=1,
    max_tokens=2048,
    stream=True,
)
```

To visualize the output, define a helper function to print the stream.

```python
def print_stream(result):
    """
    Prints the chat completion with streaming.
    """
    import time
    for update in result:
        if update.choices:
            print(update.choices[0].delta.content, end="")
```

You can visualize how streaming generates content:


```python
print_stream(result)
```

### Considerations when working with reasoning models

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and content safety is enabled.


```python
from azure.ai.inference.models import AssistantMessage, UserMessage, SystemMessage

try:
    response = client.complete(
        messages=[
            SystemMessage(content="You are an AI assistant that helps people find information."),
            UserMessage(content="Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."),
        ]
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

> [!TIP]
> To learn more about how you can configure and control Azure AI content safety settings, check the [Azure AI content safety documentation](https://aka.ms/azureaicontentsafety).
