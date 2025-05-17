---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/31/2025
ms.author: fasantia
author: santiagxf
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use the reasoning capabilities of chat completions models deployed in Azure AI Foundry Models.

[!INCLUDE [about-reasoning](about-reasoning.md)]

## Prerequisites

To complete this tutorial, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-python](../how-to-prerequisites-python.md)]

* A model with reasoning capabilities model deployment. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md) to add a reasoning model. 

  * This example uses `DeepSeek-R1`.

## Use reasoning capabilities with chat

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

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

> [!TIP]
> Verify that you have deployed the model to Azure AI Services resource with the Foundry Models API. `Deepseek-R1` is also available as standard deployments. However, those endpoints don't take the parameter `model` as explained in this tutorial. You can verify that by going to [Azure AI Foundry portal]() > Models + endpoints, and verify that the model is listed under the section **Azure AI Services**.

If you have configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

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

[!INCLUDE [best-practices](best-practices.md)]

### Create a chat completion request

The following example shows how you can create a basic chat request to the model.

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        UserMessage(content="How many languages are in the world?"),
    ],
)
```

[!INCLUDE [best-practices](best-practices.md)]

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
Response: <think>Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...</think>As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: deepseek-r1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```


### Reasoning content

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind it. The reasoning associated with the completion is included in the response's content within the tags `<think>` and `</think>`. The model may select on which scenarios to generate reasoning content. You can extract the reasoning content from the response to understand the model's thought process as follows:

```python
import re

match = re.match(r"<think>(.*?)</think>(.*)", response.choices[0].message.content, re.DOTALL)

print("Response:", )
if match:
    print("\tThinking:", match.group(1))
    print("\tAnswer:", match.group(2))
else:
    print("\tAnswer:", response.choices[0].message.content)
print("Model:", response.model)
print("Usage:")
print("\tPrompt tokens:", response.usage.prompt_tokens)
print("\tTotal tokens:", response.usage.total_tokens)
print("\tCompletion tokens:", response.usage.completion_tokens)
```

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer. Let's start by recalling the general consensus from linguistic sources. I remember that the number often cited is around 7,000, but maybe I should check some reputable organizations.\n\nEthnologue is a well-known resource for language data, and I think they list about 7,000 languages. But wait, do they update their numbers? It might be around 7,100 or so. Also, the exact count can vary because some sources might categorize dialects differently or have more recent data. \n\nAnother thing to consider is language endangerment. Many languages are endangered, with some having only a few speakers left. Organizations like UNESCO track endangered languages, so mentioning that adds context. Also, the distribution isn't even. Some countries have hundreds of languages, like Papua New Guinea with over 800, while others have just a few. \n\nA user might also wonder why the exact number is hard to pin down. It's because the distinction between a language and a dialect can be political or cultural. For example, Mandarin and Cantonese are considered dialects of Chinese by some, but they're mutually unintelligible, so others classify them as separate languages. Also, some regions are under-researched, making it hard to document all languages. \n\nI should also touch on language families. The 7,000 languages are grouped into families like Indo-European, Sino-Tibetan, Niger-Congo, etc. Maybe mention a few of the largest families. But wait, the question is just about the count, not the families. Still, it's good to provide a bit more context. \n\nI need to make sure the information is up-to-date. Let me think – recent estimates still hover around 7,000. However, languages are dying out rapidly, so the number decreases over time. Including that note about endangerment and language extinction rates could be helpful. For instance, it's often stated that a language dies every few weeks. \n\nAnother point is sign languages. Does the count include them? Ethnologue includes some, but not all sources might. If the user is including sign languages, that adds more to the count, but I think the 7,000 figure typically refers to spoken languages. For thoroughness, maybe mention that there are also over 300 sign languages. \n\nSummarizing, the answer should state around 7,000, mention Ethnologue's figure, explain why the exact number varies, touch on endangerment, and possibly note sign languages as a separate category. Also, a brief mention of Papua New Guinea as the most linguistically diverse country. \n\nWait, let me verify Ethnologue's current number. As of their latest edition (25th, 2022), they list 7,168 living languages. But I should check if that's the case. Some sources might round to 7,000. Also, SIL International publishes Ethnologue, so citing them as reference makes sense. \n\nOther sources, like Glottolog, might have a different count because they use different criteria. Glottolog might list around 7,000 as well, but exact numbers vary. It's important to highlight that the count isn't exact because of differing definitions and ongoing research. \n\nIn conclusion, the approximate number is 7,000, with Ethnologue being a key source, considerations of endangerment, and the challenges in counting due to dialect vs. language distinctions. I should make sure the answer is clear, acknowledges the variability, and provides key points succinctly.

Answer: The exact number of languages in the world is challenging to determine due to differences in definitions (e.g., distinguishing languages from dialects) and ongoing documentation efforts. However, widely cited estimates suggest there are approximately **7,000 languages** globally.
Model: DeepSeek-R1
Usage: 
  Prompt tokens: 11
  Total tokens: 897
  Completion tokens: 886
```

When making multi-turn conversations, it's useful to avoid sending the reasoning content in the chat history as reasoning tends to generate long explanations.

### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.

To stream completions, set `stream=True` when you call the model.


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

To visualize the output, define a helper function to print the stream. The following example implements a routing that stream only the answer without the reasoning content:

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

You can visualize how streaming generates content:


```python
print_stream(result)
```

### Parameters

In general, reasoning models don't support the following parameters you can find in chat completion models:

* Temperature
* Presence penalty
* Repetition penalty
* Parameter `top_p`

Some models support the use of tools or structured outputs (including JSON-schemas). Read the [Models](../../concepts/models.md) details page to understand each model's support.

### Apply Guardrails and controls

The Foundry Models API supports [Azure AI Content Safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI Content Safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt.

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

> [!TIP]
> To learn more about how you can configure and control Azure AI Content Safety settings, check the [Azure AI Content Safety documentation](https://aka.ms/azureaicontentsafety).
