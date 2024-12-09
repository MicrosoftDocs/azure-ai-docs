---
title: How to use Cohere Command chat models with Azure Machine Learning studio
titleSuffix: Azure Machine Learning
description: Learn how to use Cohere Command chat models with Azure Machine Learning studio.
manager: scottpolly
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
ms.date: 09/24/2024
ms.reviewer: shubhiraj
reviewer: shubhirajMsft
ms.author: mopeakande
author: msakande
ms.custom: references_regions, generated
zone_pivot_groups: azure-ai-model-catalog-samples-chat
ms.collection: ce-skilling-ai-copilot
---

# How to use Cohere Command chat models with Azure Machine Learning studio


In this article, you learn about Cohere Command chat models and how to use them.
The Cohere family of models includes various models optimized for different use cases, including chat completions, embeddings, and rerank. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]


::: zone pivot="programming-language-python"

## Cohere Command chat models

The Cohere Command chat models include the following models:

# [Cohere Command R+ 08-2024](#tab/cohere-command-r-plus-08-2024)

Command R+ 08-2024 is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The mode is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ 08-2024 for those workflows that lean on complex retrieval augmented generation (RAG) functionality, multi-step tool use (agents), and structured outputs.


The following models are available:

* [Cohere-command-r-plus-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024)


# [Cohere Command R 08-2024](#tab/cohere-command-r-08-2024)

Command R 08-2024 is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.


The following models are available:

* [Cohere-command-r-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024)


# [Cohere Command R+](#tab/cohere-command-r-plus)

Command R+ is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ for those workflows that lean on complex retrieval augmented generation (RAG) functionality and multi-step tool use (agents).


The following models are available:

* [Cohere-command-r-plus](https://aka.ms/azureai/landing/Cohere-command-r-plus)


# [Cohere Command R](#tab/cohere-command-r)

Command R is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R supports a context length of 128 K.

Command R is great for simpler retrieval augmented generation (RAG) and single-step tool use tasks. It's also great for use in applications where price is a major consideration.


The following models are available:

* [Cohere-command-r](https://aka.ms/azureai/landing/Cohere-command-r)


---

> [!TIP]
> Additionally, Cohere supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Cohere documentation](https://docs.cohere.com/reference/about) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Cohere Command chat models with Azure Machine Learning, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Cohere Command chat models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure Machine Learning studio, Azure Machine Learning studio, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](how-to-deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](how-to-deploy-models-serverless.md)

### The inference package installed

You can consume predictions from this model by using the `azure-ai-inference` package with Python. To install this package, you need the following prerequisites:

* Python 3.8 or later installed, including pip.
* The endpoint URL. To construct the client library, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name` is your unique model deployment host name and `your-azure-region` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.
  
Once you have these prerequisites, install the Azure AI inference package with the following command:

```bash
pip install azure-ai-inference
```

Read more about the [Azure AI inference package and reference](https://aka.ms/azsdk/azure-ai-inference/python/reference).

## Work with chat completions

In this section, you use the [Azure AI model inference API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure Machine Learning with the same code and structure, including Cohere Command chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

### Get the model's capabilities

The `/info` route returns information about the model that is deployed to the endpoint. Return the model's information by calling the following method:


```python
model_info = client.get_model_info()
```

The response is as follows:


```python
print("Model name:", model_info.model_name)
print("Model type:", model_info.model_type)
print("Model provider name:", model_info.model_provider_name)
```

```console
Model name: Cohere-command-r-plus-08-2024
Model type: chat-completions
Model provider name: Cohere
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
)
```

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
Model: Cohere-command-r-plus-08-2024
Usage: 
  Prompt tokens: 19
  Total tokens: 91
  Completion tokens: 72
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.


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

To stream completions, set `stream=True` when you call the model.

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

#### Explore more parameters supported by the inference client

Explore other parameters that you can specify in the inference client. For a full list of all the supported parameters and their corresponding documentation, see [Azure AI Model Inference API reference](https://aka.ms/azureai/modelinference).

```python
from azure.ai.inference.models import ChatCompletionsResponseFormatText

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
    presence_penalty=0.1,
    frequency_penalty=0.8,
    max_tokens=2048,
    stop=["<|endoftext|>"],
    temperature=0,
    top_p=1,
    response_format={ "type": ChatCompletionsResponseFormatText() },
)
```

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

#### Create JSON outputs

Cohere Command chat models can create JSON outputs. Set `response_format` to `json_object` to enable JSON mode and guarantee that the message the model generates is valid JSON. You must also instruct the model to produce JSON yourself via a system or user message. Also, the message content might be partially cut off if `finish_reason="length"`, which indicates that the generation exceeded `max_tokens` or that the conversation exceeded the max context length.


```python
from azure.ai.inference.models import ChatCompletionsResponseFormatJSON

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant that always generate responses in JSON format, using."
                      " the following format: { ""answer"": ""response"" }."),
        UserMessage(content="How many languages are in the world?"),
    ],
    response_format={ "type": ChatCompletionsResponseFormatJSON() }
)
```

### Pass extra parameters to the model

The Azure AI Model Inference API allows you to pass extra parameters to the model. The following code example shows how to pass the extra parameter `logprobs` to the model. 

Before you pass extra parameters to the Azure AI model inference API, make sure your model supports those extra parameters. When the request is made to the underlying model, the header `extra-parameters` is passed to the model with the value `pass-through`. This value tells the endpoint to pass the extra parameters to the model. Use of extra parameters with the model doesn't guarantee that the model can actually handle them. Read the model's documentation to understand which extra parameters are supported.


```python
response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="How many languages are in the world?"),
    ],
    model_extras={
        "logprobs": True
    }
)
```

### Use tools

Cohere Command chat models support the use of tools, which can be an extraordinary resource when you need to offload specific tasks from the language model and instead rely on a more deterministic system or even a different language model. The Azure AI Model Inference API allows you to define tools in the following way.

The following code example creates a tool definition that is able to look from flight information from two different cities.


```python
from azure.ai.inference.models import FunctionDefinition, ChatCompletionsFunctionToolDefinition

flight_info = ChatCompletionsFunctionToolDefinition(
    function=FunctionDefinition(
        name="get_flight_info",
        description="Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
        parameters={
            "type": "object",
            "properties": {
                "origin_city": {
                    "type": "string",
                    "description": "The name of the city where the flight originates",
                },
                "destination_city": {
                    "type": "string",
                    "description": "The flight destination city",
                },
            },
            "required": ["origin_city", "destination_city"],
        },
    )
)

tools = [flight_info]
```

In this example, the function's output is that there are no flights available for the selected route, but the user should consider taking a train.


```python
def get_flight_info(loc_origin: str, loc_destination: str):
    return { 
        "info": f"There are no flights available from {loc_origin} to {loc_destination}. You should take a train, specially if it helps to reduce CO2 emissions."
    }
```

> [!NOTE]
> Cohere-command-r-plus-08-2024, Cohere-command-r-08-2024, Cohere-command-r-plus, and Cohere-command-r require a tool's responses to be a valid JSON content formatted as a string. When constructing messages of type *Tool*, ensure the response is a valid JSON string.

Prompt the model to book flights with the help of this function:


```python
messages = [
    SystemMessage(
        content="You are a helpful assistant that help users to find information about traveling, how to get"
                " to places and the different transportations options. You care about the environment and you"
                " always have that in mind when answering inqueries.",
    ),
    UserMessage(
        content="When is the next flight from Miami to Seattle?",
    ),
]

response = client.complete(
    messages=messages, tools=tools, tool_choice="auto"
)
```

You can inspect the response to find out if a tool needs to be called. Inspect the finish reason to determine if the tool should be called. Remember that multiple tool types can be indicated. This example demonstrates a tool of type `function`.


```python
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

print("Finish reason:", response.choices[0].finish_reason)
print("Tool call:", tool_calls)
```

To continue, append this message to the chat history:


```python
messages.append(
    response_message
)
```

Now, it's time to call the appropriate function to handle the tool call. The following code snippet iterates over all the tool calls indicated in the response and calls the corresponding function with the appropriate parameters. The response is also appended to the chat history.


```python
import json
from azure.ai.inference.models import ToolMessage

for tool_call in tool_calls:

    # Get the tool details:

    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments.replace("\'", "\""))
    tool_call_id = tool_call.id

    print(f"Calling function `{function_name}` with arguments {function_args}")

    # Call the function defined above using `locals()`, which returns the list of all functions 
    # available in the scope as a dictionary. Notice that this is just done as a simple way to get
    # the function callable from its string name. Then we can call it with the corresponding
    # arguments.

    callable_func = locals()[function_name]
    function_response = callable_func(**function_args)

    print("->", function_response)

    # Once we have a response from the function and its arguments, we can append a new message to the chat 
    # history. Notice how we are telling to the model that this chat message came from a tool:

    messages.append(
        ToolMessage(
            tool_call_id=tool_call_id,
            content=json.dumps(function_response)
        )
    )
```

View the response from the model:


```python
response = client.complete(
    messages=messages,
    tools=tools,
)
```

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

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

::: zone-end


::: zone pivot="programming-language-javascript"

## Cohere Command chat models

The Cohere Command chat models include the following models:

# [Cohere Command R+ 08-2024](#tab/cohere-command-r-plus-08-2024)

Command R+ 08-2024 is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The mode is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ 08-2024 for those workflows that lean on complex retrieval augmented generation (RAG) functionality, multi-step tool use (agents), and structured outputs.


The following models are available:

* [Cohere-command-r-plus-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024)


# [Cohere Command R 08-2024](#tab/cohere-command-r-08-2024)

Command R 08-2024 is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.


The following models are available:

* [Cohere-command-r-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024)


# [Cohere Command R+](#tab/cohere-command-r-plus)

Command R+ is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ for those workflows that lean on complex retrieval augmented generation (RAG) functionality and multi-step tool use (agents).


The following models are available:

* [Cohere-command-r-plus](https://aka.ms/azureai/landing/Cohere-command-r-plus)


# [Cohere Command R](#tab/cohere-command-r)

Command R is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R supports a context length of 128 K.

Command R is great for simpler retrieval augmented generation (RAG) and single-step tool use tasks. It's also great for use in applications where price is a major consideration.


The following models are available:

* [Cohere-command-r](https://aka.ms/azureai/landing/Cohere-command-r)


---

> [!TIP]
> Additionally, Cohere supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Cohere documentation](https://docs.cohere.com/reference/about) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Cohere Command chat models with Azure Machine Learning, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Cohere Command chat models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure Machine Learning studio, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](how-to-deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](how-to-deploy-models-serverless.md)

### The inference package installed

You can consume predictions from this model by using the `@azure-rest/ai-inference` package from `npm`. To install this package, you need the following prerequisites:

* LTS versions of `Node.js` with `npm`.
* The endpoint URL. To construct the client library, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name` is your unique model deployment host name and `your-azure-region` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

Once you have these prerequisites, install the Azure Inference library for JavaScript with the following command:

```bash
npm install @azure-rest/ai-inference
```

## Work with chat completions

In this section, you use the [Azure AI model inference API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure Machine Learning with the same code and structure, including Cohere Command chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { AzureKeyCredential } from "@azure/core-auth";

const client = new ModelClient(
    process.env.AZURE_INFERENCE_ENDPOINT, 
    new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
);
```

### Get the model's capabilities

The `/info` route returns information about the model that is deployed to the endpoint. Return the model's information by calling the following method:


```javascript
var model_info = await client.path("/info").get()
```

The response is as follows:


```javascript
console.log("Model name: ", model_info.body.model_name)
console.log("Model type: ", model_info.body.model_type)
console.log("Model provider name: ", model_info.body.model_provider_name)
```

```console
Model name: Cohere-command-r-plus-08-2024
Model type: chat-completions
Model provider name: Cohere
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
    }
});
```

The response is as follows, where you can see the model's usage statistics:


```javascript
if (isUnexpected(response)) {
    throw response.body.error;
}

console.log("Response: ", response.body.choices[0].message.content);
console.log("Model: ", response.body.model);
console.log("Usage:");
console.log("\tPrompt tokens:", response.body.usage.prompt_tokens);
console.log("\tTotal tokens:", response.body.usage.total_tokens);
console.log("\tCompletion tokens:", response.body.usage.completion_tokens);
```

```console
Response: As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: Cohere-command-r-plus-08-2024
Usage: 
  Prompt tokens: 19
  Total tokens: 91
  Completion tokens: 72
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.


```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
    }
}).asNodeStream();
```

To stream completions, use `.asNodeStream()` when you call the model.

You can visualize how streaming generates content:


```javascript
var stream = response.body;
if (!stream) {
    stream.destroy();
    throw new Error(`Failed to get chat completions with status: ${response.status}`);
}

if (response.status !== "200") {
    throw new Error(`Failed to get chat completions: ${response.body.error}`);
}

var sses = createSseStream(stream);

for await (const event of sses) {
    if (event.data === "[DONE]") {
        return;
    }
    for (const choice of (JSON.parse(event.data)).choices) {
        console.log(choice.delta?.content ?? "");
    }
}
```

#### Explore more parameters supported by the inference client

Explore other parameters that you can specify in the inference client. For a full list of all the supported parameters and their corresponding documentation, see [Azure AI Model Inference API reference](https://aka.ms/azureai/modelinference).

```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        presence_penalty: "0.1",
        frequency_penalty: "0.8",
        max_tokens: 2048,
        stop: ["<|endoftext|>"],
        temperature: 0,
        top_p: 1,
        response_format: { type: "text" },
    }
});
```

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

#### Create JSON outputs

Cohere Command chat models can create JSON outputs. Set `response_format` to `json_object` to enable JSON mode and guarantee that the message the model generates is valid JSON. You must also instruct the model to produce JSON yourself via a system or user message. Also, the message content might be partially cut off if `finish_reason="length"`, which indicates that the generation exceeded `max_tokens` or that the conversation exceeded the max context length.


```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant that always generate responses in JSON format, using."
        + " the following format: { \"answer\": \"response\" }." },
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        response_format: { type: "json_object" }
    }
});
```

### Pass extra parameters to the model

The Azure AI Model Inference API allows you to pass extra parameters to the model. The following code example shows how to pass the extra parameter `logprobs` to the model. 

Before you pass extra parameters to the Azure AI model inference API, make sure your model supports those extra parameters. When the request is made to the underlying model, the header `extra-parameters` is passed to the model with the value `pass-through`. This value tells the endpoint to pass the extra parameters to the model. Use of extra parameters with the model doesn't guarantee that the model can actually handle them. Read the model's documentation to understand which extra parameters are supported.


```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "How many languages are in the world?" },
];

var response = await client.path("/chat/completions").post({
    headers: {
        "extra-params": "pass-through"
    },
    body: {
        messages: messages,
        logprobs: true
    }
});
```

### Use tools

Cohere Command chat models support the use of tools, which can be an extraordinary resource when you need to offload specific tasks from the language model and instead rely on a more deterministic system or even a different language model. The Azure AI Model Inference API allows you to define tools in the following way.

The following code example creates a tool definition that is able to look from flight information from two different cities.


```javascript
const flight_info = {
    name: "get_flight_info",
    description: "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
    parameters: {
        type: "object",
        properties: {
            origin_city: {
                type: "string",
                description: "The name of the city where the flight originates",
            },
            destination_city: {
                type: "string",
                description: "The flight destination city",
            },
        },
        required: ["origin_city", "destination_city"],
    },
}

const tools = [
    {
        type: "function",
        function: flight_info,
    },
];
```

In this example, the function's output is that there are no flights available for the selected route, but the user should consider taking a train.


```javascript
function get_flight_info(loc_origin, loc_destination) {
    return {
        info: "There are no flights available from " + loc_origin + " to " + loc_destination + ". You should take a train, specially if it helps to reduce CO2 emissions."
    }
}
```

> [!NOTE]
> Cohere-command-r-plus-08-2024, Cohere-command-r-08-2024, Cohere-command-r-plus, and Cohere-command-r require a tool's responses to be a valid JSON content formatted as a string. When constructing messages of type *Tool*, ensure the response is a valid JSON string.

Prompt the model to book flights with the help of this function:


```javascript
var result = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        tools: tools,
        tool_choice: "auto"
    }
});
```

You can inspect the response to find out if a tool needs to be called. Inspect the finish reason to determine if the tool should be called. Remember that multiple tool types can be indicated. This example demonstrates a tool of type `function`.


```javascript
const response_message = response.body.choices[0].message;
const tool_calls = response_message.tool_calls;

console.log("Finish reason: " + response.body.choices[0].finish_reason);
console.log("Tool call: " + tool_calls);
```

To continue, append this message to the chat history:


```javascript
messages.push(response_message);
```

Now, it's time to call the appropriate function to handle the tool call. The following code snippet iterates over all the tool calls indicated in the response and calls the corresponding function with the appropriate parameters. The response is also appended to the chat history.


```javascript
function applyToolCall({ function: call, id }) {
    // Get the tool details:
    const tool_params = JSON.parse(call.arguments);
    console.log("Calling function " + call.name + " with arguments " + tool_params);

    // Call the function defined above using `window`, which returns the list of all functions 
    // available in the scope as a dictionary. Notice that this is just done as a simple way to get
    // the function callable from its string name. Then we can call it with the corresponding
    // arguments.
    const function_response = tool_params.map(window[call.name]);
    console.log("-> " + function_response);

    return function_response
}

for (const tool_call of tool_calls) {
    var tool_response = tool_call.apply(applyToolCall);

    messages.push(
        {
            role: "tool",
            tool_call_id: tool_call.id,
            content: tool_response
        }
    );
}
```

View the response from the model:


```javascript
var result = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        tools: tools,
    }
});
```

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and content safety is enabled.


```javascript
try {
    var messages = [
        { role: "system", content: "You are an AI assistant that helps people find information." },
        { role: "user", content: "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills." },
    ];

    var response = await client.path("/chat/completions").post({
        body: {
            messages: messages,
        }
    });

    console.log(response.body.choices[0].message.content);
}
catch (error) {
    if (error.status_code == 400) {
        var response = JSON.parse(error.response._content);
        if (response.error) {
            console.log(`Your request triggered an ${response.error.code} error:\n\t ${response.error.message}`);
        }
        else
        {
            throw error;
        }
    }
}
```

> [!TIP]
> To learn more about how you can configure and control Azure AI content safety settings, check the [Azure AI content safety documentation](https://aka.ms/azureaicontentsafety).

::: zone-end


::: zone pivot="programming-language-csharp"

## Cohere Command chat models

The Cohere Command chat models include the following models:

# [Cohere Command R+ 08-2024](#tab/cohere-command-r-plus-08-2024)

Command R+ 08-2024 is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The mode is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ 08-2024 for those workflows that lean on complex retrieval augmented generation (RAG) functionality, multi-step tool use (agents), and structured outputs.


The following models are available:

* [Cohere-command-r-plus-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024)


# [Cohere Command R 08-2024](#tab/cohere-command-r-08-2024)

Command R 08-2024 is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.


The following models are available:

* [Cohere-command-r-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024)


# [Cohere Command R+](#tab/cohere-command-r-plus)

Command R+ is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ for those workflows that lean on complex retrieval augmented generation (RAG) functionality and multi-step tool use (agents).


The following models are available:

* [Cohere-command-r-plus](https://aka.ms/azureai/landing/Cohere-command-r-plus)


# [Cohere Command R](#tab/cohere-command-r)

Command R is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R supports a context length of 128 K.

Command R is great for simpler retrieval augmented generation (RAG) and single-step tool use tasks. It's also great for use in applications where price is a major consideration.


The following models are available:

* [Cohere-command-r](https://aka.ms/azureai/landing/Cohere-command-r)


---

> [!TIP]
> Additionally, Cohere supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Cohere documentation](https://docs.cohere.com/reference/about) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Cohere Command chat models with Azure Machine Learning, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Cohere Command chat models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure Machine Learning studio, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](how-to-deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](how-to-deploy-models-serverless.md)

### The inference package installed

You can consume predictions from this model by using the `Azure.AI.Inference` package from [NuGet](https://www.nuget.org/). To install this package, you need the following prerequisites:

* The endpoint URL. To construct the client library, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name` is your unique model deployment host name and `your-azure-region` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

Once you have these prerequisites, install the Azure AI inference library with the following command:

```dotnetcli
dotnet add package Azure.AI.Inference --prerelease
```

You can also authenticate with Microsoft Entra ID (formerly Azure Active Directory). To use credential providers provided with the Azure SDK, install the `Azure.Identity` package:

```dotnetcli
dotnet add package Azure.Identity
```

Import the following namespaces:


```csharp
using Azure;
using Azure.Identity;
using Azure.AI.Inference;
```

This example also uses the following namespaces but you may not always need them:


```csharp
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Reflection;
```

## Work with chat completions

In this section, you use the [Azure AI model inference API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure Machine Learning with the same code and structure, including Cohere Command chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

### Get the model's capabilities

The `/info` route returns information about the model that is deployed to the endpoint. Return the model's information by calling the following method:


```csharp
Response<ModelInfo> modelInfo = client.GetModelInfo();
```

The response is as follows:


```csharp
Console.WriteLine($"Model name: {modelInfo.Value.ModelName}");
Console.WriteLine($"Model type: {modelInfo.Value.ModelType}");
Console.WriteLine($"Model provider name: {modelInfo.Value.ModelProviderName}");
```

```console
Model name: Cohere-command-r-plus-08-2024
Model type: chat-completions
Model provider name: Cohere
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

```csharp
ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
};

Response<ChatCompletions> response = client.Complete(requestOptions);
```

The response is as follows, where you can see the model's usage statistics:


```csharp
Console.WriteLine($"Response: {response.Value.Choices[0].Message.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
```

```console
Response: As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: Cohere-command-r-plus-08-2024
Usage: 
  Prompt tokens: 19
  Total tokens: 91
  Completion tokens: 72
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.


```csharp
static async Task StreamMessageAsync(ChatCompletionsClient client)
{
    ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
    {
        Messages = {
            new ChatRequestSystemMessage("You are a helpful assistant."),
            new ChatRequestUserMessage("How many languages are in the world? Write an essay about it.")
        },
        MaxTokens=4096
    };

    StreamingResponse<StreamingChatCompletionsUpdate> streamResponse = await client.CompleteStreamingAsync(requestOptions);

    await PrintStream(streamResponse);
}
```

To stream completions, use `CompleteStreamingAsync` method when you call the model. Notice that in this example we the call is wrapped in an asynchronous method.

To visualize the output, define an asynchronous method to print the stream in the console.

```csharp
static async Task PrintStream(StreamingResponse<StreamingChatCompletionsUpdate> response)
{
    await foreach (StreamingChatCompletionsUpdate chatUpdate in response)
    {
        if (chatUpdate.Role.HasValue)
        {
            Console.Write($"{chatUpdate.Role.Value.ToString().ToUpperInvariant()}: ");
        }
        if (!string.IsNullOrEmpty(chatUpdate.ContentUpdate))
        {
            Console.Write(chatUpdate.ContentUpdate);
        }
    }
}
```

You can visualize how streaming generates content:


```csharp
StreamMessageAsync(client).GetAwaiter().GetResult();
```

#### Explore more parameters supported by the inference client

Explore other parameters that you can specify in the inference client. For a full list of all the supported parameters and their corresponding documentation, see [Azure AI Model Inference API reference](https://aka.ms/azureai/modelinference).

```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    PresencePenalty = 0.1f,
    FrequencyPenalty = 0.8f,
    MaxTokens = 2048,
    StopSequences = { "<|endoftext|>" },
    Temperature = 0,
    NucleusSamplingFactor = 1,
    ResponseFormat = new ChatCompletionsResponseFormatText()
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Choices[0].Message.Content}");
```

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

#### Create JSON outputs

Cohere Command chat models can create JSON outputs. Set `response_format` to `json_object` to enable JSON mode and guarantee that the message the model generates is valid JSON. You must also instruct the model to produce JSON yourself via a system or user message. Also, the message content might be partially cut off if `finish_reason="length"`, which indicates that the generation exceeded `max_tokens` or that the conversation exceeded the max context length.


```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage(
            "You are a helpful assistant that always generate responses in JSON format, " +
            "using. the following format: { \"answer\": \"response\" }."
        ),
        new ChatRequestUserMessage(
            "How many languages are in the world?"
        )
    },
    ResponseFormat = new ChatCompletionsResponseFormatJSON()
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Choices[0].Message.Content}");
```

### Pass extra parameters to the model

The Azure AI Model Inference API allows you to pass extra parameters to the model. The following code example shows how to pass the extra parameter `logprobs` to the model. 

Before you pass extra parameters to the Azure AI model inference API, make sure your model supports those extra parameters. When the request is made to the underlying model, the header `extra-parameters` is passed to the model with the value `pass-through`. This value tells the endpoint to pass the extra parameters to the model. Use of extra parameters with the model doesn't guarantee that the model can actually handle them. Read the model's documentation to understand which extra parameters are supported.


```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    AdditionalProperties = { { "logprobs", BinaryData.FromString("true") } },
};

response = client.Complete(requestOptions, extraParams: ExtraParameters.PassThrough);
Console.WriteLine($"Response: {response.Value.Choices[0].Message.Content}");
```

### Use tools

Cohere Command chat models support the use of tools, which can be an extraordinary resource when you need to offload specific tasks from the language model and instead rely on a more deterministic system or even a different language model. The Azure AI Model Inference API allows you to define tools in the following way.

The following code example creates a tool definition that is able to look from flight information from two different cities.


```csharp
FunctionDefinition flightInfoFunction = new FunctionDefinition("getFlightInfo")
{
    Description = "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
    Parameters = BinaryData.FromObjectAsJson(new
    {
        Type = "object",
        Properties = new
        {
            origin_city = new
            {
                Type = "string",
                Description = "The name of the city where the flight originates"
            },
            destination_city = new
            {
                Type = "string",
                Description = "The flight destination city"
            }
        }
    },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    )
};

ChatCompletionsFunctionToolDefinition getFlightTool = new ChatCompletionsFunctionToolDefinition(flightInfoFunction);
```

In this example, the function's output is that there are no flights available for the selected route, but the user should consider taking a train.


```csharp
static string getFlightInfo(string loc_origin, string loc_destination)
{
    return JsonSerializer.Serialize(new
    {
        info = $"There are no flights available from {loc_origin} to {loc_destination}. You " +
        "should take a train, specially if it helps to reduce CO2 emissions."
    });
}
```

> [!NOTE]
> Cohere-command-r-plus-08-2024, Cohere-command-r-08-2024, Cohere-command-r-plus, and Cohere-command-r require a tool's responses to be a valid JSON content formatted as a string. When constructing messages of type *Tool*, ensure the response is a valid JSON string.

Prompt the model to book flights with the help of this function:


```csharp
var chatHistory = new List<ChatRequestMessage>(){
        new ChatRequestSystemMessage(
            "You are a helpful assistant that help users to find information about traveling, " +
            "how to get to places and the different transportations options. You care about the" +
            "environment and you always have that in mind when answering inqueries."
        ),
        new ChatRequestUserMessage("When is the next flight from Miami to Seattle?")
    };

requestOptions = new ChatCompletionsOptions(chatHistory);
requestOptions.Tools.Add(getFlightTool);
requestOptions.ToolChoice = ChatCompletionsToolChoice.Auto;

response = client.Complete(requestOptions);
```

You can inspect the response to find out if a tool needs to be called. Inspect the finish reason to determine if the tool should be called. Remember that multiple tool types can be indicated. This example demonstrates a tool of type `function`.


```csharp
var responseMenssage = response.Value.Choices[0].Message;
var toolsCall = responseMenssage.ToolCalls;

Console.WriteLine($"Finish reason: {response.Value.Choices[0].FinishReason}");
Console.WriteLine($"Tool call: {toolsCall[0].Id}");
```

To continue, append this message to the chat history:


```csharp
requestOptions.Messages.Add(new ChatRequestAssistantMessage(response.Value.Choices[0].Message));
```

Now, it's time to call the appropriate function to handle the tool call. The following code snippet iterates over all the tool calls indicated in the response and calls the corresponding function with the appropriate parameters. The response is also appended to the chat history.


```csharp
foreach (ChatCompletionsToolCall tool in toolsCall)
{
    if (tool is ChatCompletionsFunctionToolCall functionTool)
    {
        // Get the tool details:
        string callId = functionTool.Id;
        string toolName = functionTool.Name;
        string toolArgumentsString = functionTool.Arguments;
        Dictionary<string, object> toolArguments = JsonSerializer.Deserialize<Dictionary<string, object>>(toolArgumentsString);

        // Here you have to call the function defined. In this particular example we use 
        // reflection to find the method we definied before in an static class called 
        // `ChatCompletionsExamples`. Using reflection allows us to call a function 
        // by string name. Notice that this is just done for demonstration purposes as a 
        // simple way to get the function callable from its string name. Then we can call 
        // it with the corresponding arguments.

        var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static;
        string toolResponse = (string)typeof(ChatCompletionsExamples).GetMethod(toolName, flags).Invoke(null, toolArguments.Values.Cast<object>().ToArray());

        Console.WriteLine("->", toolResponse);
        requestOptions.Messages.Add(new ChatRequestToolMessage(toolResponse, callId));
    }
    else
        throw new Exception("Unsupported tool type");
}
```

View the response from the model:


```csharp
response = client.Complete(requestOptions);
```

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and content safety is enabled.


```csharp
try
{
    requestOptions = new ChatCompletionsOptions()
    {
        Messages = {
            new ChatRequestSystemMessage("You are an AI assistant that helps people find information."),
            new ChatRequestUserMessage(
                "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
            ),
        },
    };

    response = client.Complete(requestOptions);
    Console.WriteLine(response.Value.Choices[0].Message.Content);
}
catch (RequestFailedException ex)
{
    if (ex.ErrorCode == "content_filter")
    {
        Console.WriteLine($"Your query has trigger Azure Content Safety: {ex.Message}");
    }
    else
    {
        throw;
    }
}
```

> [!TIP]
> To learn more about how you can configure and control Azure AI content safety settings, check the [Azure AI content safety documentation](https://aka.ms/azureaicontentsafety).

::: zone-end


::: zone pivot="programming-language-rest"

## Cohere Command chat models

The Cohere Command chat models include the following models:

# [Cohere Command R+ 08-2024](#tab/cohere-command-r-plus-08-2024)

Command R+ 08-2024 is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The mode is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ 08-2024 for those workflows that lean on complex retrieval augmented generation (RAG) functionality, multi-step tool use (agents), and structured outputs.


The following models are available:

* [Cohere-command-r-plus-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-plus-08-2024)


# [Cohere Command R 08-2024](#tab/cohere-command-r-08-2024)

Command R 08-2024 is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R 08-2024 is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R 08-2024 supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.


The following models are available:

* [Cohere-command-r-08-2024](https://aka.ms/azureai/landing/Cohere-command-r-08-2024)


# [Cohere Command R+](#tab/cohere-command-r-plus)

Command R+ is a generative large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R+ is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R+ supports a context length of 128 K.
* **Input:** Text only.
* **Output:** Text only.

We recommend using Command R+ for those workflows that lean on complex retrieval augmented generation (RAG) functionality and multi-step tool use (agents).


The following models are available:

* [Cohere-command-r-plus](https://aka.ms/azureai/landing/Cohere-command-r-plus)


# [Cohere Command R](#tab/cohere-command-r)

Command R is a large language model optimized for various use cases, including reasoning, summarization, and question answering.

* **Model Architecture**: Command R is an autoregressive language model that uses an optimized transformer architecture. After pre-training, the model uses supervised fine-tuning (SFT) and preference training to align model behavior to human preferences for helpfulness and safety.
* **Languages covered**: The model is optimized to perform well in the following languages: English, French, Spanish, Italian, German, Brazilian Portuguese, Japanese, Korean, simplified Chinese, and Arabic.
* **Pre-training data also included the following 13 languages:** Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, and Persian.
* **Context length:** Command R supports a context length of 128 K.

Command R is great for simpler retrieval augmented generation (RAG) and single-step tool use tasks. It's also great for use in applications where price is a major consideration.


The following models are available:

* [Cohere-command-r](https://aka.ms/azureai/landing/Cohere-command-r)


---

> [!TIP]
> Additionally, Cohere supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Cohere documentation](https://docs.cohere.com/reference/about) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Cohere Command chat models with Azure Machine Learning, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Cohere Command chat models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure Machine Learning studio, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](how-to-deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](how-to-deploy-models-serverless.md)

### A REST client

Models deployed with the [Azure AI model inference API](https://aka.ms/azureai/modelinference) can be consumed using any REST client. To use the REST client, you need the following prerequisites:

* To construct the requests, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name`` is your unique model deployment host name and `your-azure-region`` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

## Work with chat completions

In this section, you use the [Azure AI model inference API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure Machine Learning with the same code and structure, including Cohere Command chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

### Get the model's capabilities

The `/info` route returns information about the model that is deployed to the endpoint. Return the model's information by calling the following method:

```http
GET /info HTTP/1.1
Host: <ENDPOINT_URI>
Authorization: Bearer <TOKEN>
Content-Type: application/json
```

The response is as follows:


```json
{
    "model_name": "Cohere-command-r-plus-08-2024",
    "model_type": "chat-completions",
    "model_provider_name": "Cohere"
}
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ]
}
```

The response is as follows, where you can see the model's usage statistics:


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 19,
        "total_tokens": 91,
        "completion_tokens": 72
    }
}
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "stream": true,
    "temperature": 0,
    "top_p": 1,
    "max_tokens": 2048
}
```

You can visualize how streaming generates content:


```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "delta": {
                "role": "assistant",
                "content": ""
            },
            "finish_reason": null,
            "logprobs": null
        }
    ]
}
```

The last message in the stream has `finish_reason` set, indicating the reason for the generation process to stop.


```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "delta": {
                "content": ""
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 19,
        "total_tokens": 91,
        "completion_tokens": 72
    }
}
```

#### Explore more parameters supported by the inference client

Explore other parameters that you can specify in the inference client. For a full list of all the supported parameters and their corresponding documentation, see [Azure AI Model Inference API reference](https://aka.ms/azureai/modelinference).

```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "presence_penalty": 0.1,
    "frequency_penalty": 0.8,
    "max_tokens": 2048,
    "stop": ["<|endoftext|>"],
    "temperature" :0,
    "top_p": 1,
    "response_format": { "type": "text" }
}
```


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 19,
        "total_tokens": 91,
        "completion_tokens": 72
    }
}
```

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

#### Create JSON outputs

Cohere Command chat models can create JSON outputs. Set `response_format` to `json_object` to enable JSON mode and guarantee that the message the model generates is valid JSON. You must also instruct the model to produce JSON yourself via a system or user message. Also, the message content might be partially cut off if `finish_reason="length"`, which indicates that the generation exceeded `max_tokens` or that the conversation exceeded the max context length.


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that always generate responses in JSON format, using the following format: { \"answer\": \"response\" }"
        },
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "response_format": { "type": "json_object" }
}
```


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718727522,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "{\"answer\": \"There are approximately 7,117 living languages in the world today, according to the latest estimates. However, this number can vary as some languages become extinct and others are newly discovered or classified.\"}",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 39,
        "total_tokens": 87,
        "completion_tokens": 48
    }
}
```

### Pass extra parameters to the model

The Azure AI Model Inference API allows you to pass extra parameters to the model. The following code example shows how to pass the extra parameter `logprobs` to the model. 

Before you pass extra parameters to the Azure AI model inference API, make sure your model supports those extra parameters. When the request is made to the underlying model, the header `extra-parameters` is passed to the model with the value `pass-through`. This value tells the endpoint to pass the extra parameters to the model. Use of extra parameters with the model doesn't guarantee that the model can actually handle them. Read the model's documentation to understand which extra parameters are supported.

```http
POST /chat/completions HTTP/1.1
Host: <ENDPOINT_URI>
Authorization: Bearer <TOKEN>
Content-Type: application/json
extra-parameters: pass-through
```


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "How many languages are in the world?"
        }
    ],
    "logprobs": true
}
```

### Use tools

Cohere Command chat models support the use of tools, which can be an extraordinary resource when you need to offload specific tasks from the language model and instead rely on a more deterministic system or even a different language model. The Azure AI Model Inference API allows you to define tools in the following way.

The following code example creates a tool definition that is able to look for flight information from two different cities.


```json
{
    "type": "function",
    "function": {
        "name": "get_flight_info",
        "description": "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
        "parameters": {
            "type": "object",
            "properties": {
                "origin_city": {
                    "type": "string",
                    "description": "The name of the city where the flight originates"
                },
                "destination_city": {
                    "type": "string",
                    "description": "The flight destination city"
                }
            },
            "required": [
                "origin_city",
                "destination_city"
            ]
        }
    }
}
```

In this example, the function's output is that there are no flights available for the selected route, but the user should consider taking a train.

> [!NOTE]
> Cohere-command-r-plus-08-2024, Cohere-command-r-08-2024, Cohere-command-r-plus, and Cohere-command-r require a tool's responses to be a valid JSON content formatted as a string. When constructing messages of type *Tool*, ensure the response is a valid JSON string.

Prompt the model to book flights with the help of this function:


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that help users to find information about traveling, how to get to places and the different transportations options. You care about the environment and you always have that in mind when answering inqueries"
        },
        {
            "role": "user",
            "content": "When is the next flight from Miami to Seattle?"
        }
    ],
    "tool_choice": "auto",
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_flight_info",
                "description": "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin_city": {
                            "type": "string",
                            "description": "The name of the city where the flight originates"
                        },
                        "destination_city": {
                            "type": "string",
                            "description": "The flight destination city"
                        }
                    },
                    "required": [
                        "origin_city",
                        "destination_city"
                    ]
                }
            }
        }
    ]
}
```

You can inspect the response to find out if a tool needs to be called. Inspect the finish reason to determine if the tool should be called. Remember that multiple tool types can be indicated. This example demonstrates a tool of type `function`.


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726007,
    "model": "Cohere-command-r-plus-08-2024",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "id": "abc0dF1gh",
                        "type": "function",
                        "function": {
                            "name": "get_flight_info",
                            "arguments": "{\"origin_city\": \"Miami\", \"destination_city\": \"Seattle\"}",
                            "call_id": null
                        }
                    }
                ]
            },
            "finish_reason": "tool_calls",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 190,
        "total_tokens": 226,
        "completion_tokens": 36
    }
}
```

To continue, append this message to the chat history:

Now, it's time to call the appropriate function to handle the tool call. The following code snippet iterates over all the tool calls indicated in the response and calls the corresponding function with the appropriate parameters. The response is also appended to the chat history.

View the response from the model:


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that help users to find information about traveling, how to get to places and the different transportations options. You care about the environment and you always have that in mind when answering inqueries"
        },
        {
            "role": "user",
            "content": "When is the next flight from Miami to Seattle?"
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": "abc0DeFgH",
                    "type": "function",
                    "function": {
                        "name": "get_flight_info",
                        "arguments": "{\"origin_city\": \"Miami\", \"destination_city\": \"Seattle\"}",
                        "call_id": null
                    }
                }
            ]
        },
        {
            "role": "tool",
            "content": "{ \"info\": \"There are no flights available from Miami to Seattle. You should take a train, specially if it helps to reduce CO2 emissions.\" }",
            "tool_call_id": "abc0DeFgH" 
        }
    ],
    "tool_choice": "auto",
    "tools": [
        {
            "type": "function",
            "function": {
            "name": "get_flight_info",
            "description": "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
            "parameters":{
                "type": "object",
                "properties": {
                    "origin_city": {
                        "type": "string",
                        "description": "The name of the city where the flight originates"
                    },
                    "destination_city": {
                        "type": "string",
                        "description": "The flight destination city"
                    }
                },
                "required": ["origin_city", "destination_city"]
            }
            }
        }
    ]
}
```

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering (preview) system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and content safety is enabled.


```json
{
    "messages": [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        },
                {
            "role": "user",
            "content": "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
        }
    ]
}
```


```json
{
    "error": {
        "message": "The response was filtered due to the prompt triggering Microsoft's content management policy. Please modify your prompt and retry.",
        "type": null,
        "param": "prompt",
        "code": "content_filter",
        "status": 400
    }
}
```

> [!TIP]
> To learn more about how you can configure and control Azure AI content safety settings, check the [Azure AI content safety documentation](https://aka.ms/azureaicontentsafety).

::: zone-end

## More inference examples

For more examples of how to use Cohere models, see the following examples and tutorials:

| Description                               | Language          | Sample                                                          |
|-------------------------------------------|-------------------|-----------------------------------------------------------------|
| Web requests                              | Bash              | [Command-R](https://aka.ms/samples/cohere-command-r/webrequests) - [Command-R+](https://aka.ms/samples/cohere-command-r-plus/webrequests) |
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://aka.ms/azsdk/azure-ai-inference/javascript/samples)  |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)      |
| OpenAI SDK (experimental)                 | Python            | [Link](https://aka.ms/samples/cohere-command/openaisdk)             |
| LangChain                                 | Python            | [Link](https://aka.ms/samples/cohere/langchain)                     |
| Cohere SDK                                | Python            | [Link](https://aka.ms/samples/cohere-python-sdk)                    |
| LiteLLM SDK                               | Python            | [Link](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/litellm.ipynb) |

#### Retrieval Augmented Generation (RAG) and tool use samples

| Description | Packages   | Sample          |
|-------------|------------|-----------------|
| Create a local Facebook AI similarity search (FAISS) vector index, using Cohere embeddings - Langchain | `langchain`, `langchain_cohere` | [cohere_faiss_langchain_embed.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere_faiss_langchain_embed.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in local FAISS vector index - Langchain |`langchain`, `langchain_cohere` | [command_faiss_langchain.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/command_faiss_langchain.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in AI search vector index - Langchain | `langchain`, `langchain_cohere` | [cohere-aisearch-langchain-rag.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere-aisearch-langchain-rag.ipynb) |
| Use Cohere Command R/R+ to answer questions from data in AI search vector index - Cohere SDK | `cohere`, `azure_search_documents` | [cohere-aisearch-rag.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/cohere-aisearch-rag.ipynb) |
| Command R+ tool/function calling, using LangChain | `cohere`, `langchain`, `langchain_cohere` | [command_tools-langchain.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/cohere/command_tools-langchain.ipynb) |


## Cost and quota considerations for Cohere models deployed as serverless API endpoints

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

Cohere models deployed as a serverless API are offered by Cohere through the Azure Marketplace and integrated with Azure Machine Learning studio for use. You can find the Azure Marketplace pricing when deploying the model.

Each time a project subscribes to a given offer from the Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](/azure/ai-studio/how-to/costs-plan-manage#monitor-costs-for-models-offered-through-the-azure-marketplace).

## Related content


* [Azure AI Model Inference API](reference-model-inference-api.md)
* [Deploy models as serverless APIs](how-to-deploy-models-serverless.md)
* [Region availability for models in serverless API endpoints](concept-endpoint-serverless-availability.md)
* [Plan and manage costs for Azure AI Foundry](/azure/ai-studio/how-to/costs-plan-manage)