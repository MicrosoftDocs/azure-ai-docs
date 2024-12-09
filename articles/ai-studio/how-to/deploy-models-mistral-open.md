---
title: How to use Mistral-7B and Mixtral chat models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use Mistral-7B and Mixtral chat models with Azure AI Foundry.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 09/13/2024
ms.reviewer: kritifaujdar
reviewer: fkriti
ms.author: mopeakande
author: msakande
ms.custom: references_regions, generated
zone_pivot_groups: azure-ai-model-catalog-samples-chat
---

# How to use Mistral-7B and Mixtral chat models

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn about Mistral-7B and Mixtral chat models and how to use them.
Mistral AI offers two categories of models. Premium models including [Mistral Large and Mistral Small](deploy-models-mistral.md), available as serverless APIs with pay-as-you-go token-based billing. Open models including [Mistral Nemo](deploy-models-mistral-nemo.md), [Mixtral-8x7B-Instruct-v01, Mixtral-8x7B-v01, Mistral-7B-Instruct-v01, and Mistral-7B-v01](deploy-models-mistral-open.md); available to also download and run on self-hosted managed endpoints.

[!INCLUDE [models-preview](../includes/models-preview.md)]

::: zone pivot="programming-language-python"

## Mistral-7B and Mixtral chat models

The Mistral-7B and Mixtral chat models include the following models:

# [Mistral-7B-Instruct](#tab/mistral-7b-instruct)

The Mistral-7B-Instruct Large Language Model (LLM) is an instruct, fine-tuned version of the Mistral-7B, a transformer model with the following architecture choices:

* Grouped-Query Attention
* Sliding-Window Attention
* Byte-fallback BPE tokenizer


The following models are available:

* [mistralai-Mistral-7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v01)
* [mistralai-Mistral-7B-Instruct-v02](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v02)


# [Mixtral-8x7B-Instruct](#tab/mistral-8x7B-instruct)

The Mixtral-8x7B Large Language Model (LLM) is a pretrained generative Sparse Mixture of Experts. The Mixtral-8x7B outperforms Llama 2 70B on most benchmarks with 6x faster inference.

Mixtral-8x7B-v0.1 is a decoder-only model with eight distinct groups or the "experts". At every layer, for every token, a router network chooses two of these experts to process the token and combine their output additively. Mixtral has 46.7B total parameters but only uses 12.9B parameters per token with this technique; therefore, the model can perform with the same speed and cost as a 12.9B model.


The following models are available:

* [mistralai-Mixtral-8x7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mixtral-8x7B-Instruct-v01)


# [Mixtral-8x22B-Instruct](#tab/mistral-8x22b-instruct)

The Mixtral-8x22B-Instruct-v0.1 Large Language Model (LLM) is an instruct, fine-tuned version of the Mixtral-8x22B-v0.1. The model is a sparse Mixture-of-Experts (SMoE) model that uses only 39B active parameters out of 141B, offering unparalleled cost efficiency for its size.

Mixtral 8x22B comes with the following strengths:

* Fluent in English, French, Italian, German, and Spanish
* Strong mathematics and coding capabilities
* Natively capable of function calling, enabling application development and tech stack modernization at scale
* Precise information recall from large documents, due to its 64K tokens context window


The following models are available:

* [mistralai-Mixtral-8x22B-Instruct-v0-1](https://aka.ms/azureai/landing/mistralai-Mixtral-8x22B-Instruct-v0-1)


---

> [!TIP]
> Additionally, MistralAI supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [MistralAI documentation](https://docs.mistral.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Mistral-7B and Mixtral chat models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

Mistral-7B and Mixtral chat models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../concepts/deployments-overview.md)

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Mistral-7B and Mixtral chat models.

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

When you deploy the model to a self-hosted online endpoint with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
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
Model name: mistralai-Mistral-7B-Instruct-v01
Model type: chat-completions
Model provider name: MistralAI
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

> [!NOTE]
> mistralai-Mistral-7B-Instruct-v01, mistralai-Mistral-7B-Instruct-v02 and mistralai-Mixtral-8x22B-Instruct-v0-1 don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

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
Model: mistralai-Mistral-7B-Instruct-v01
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

> [!WARNING]
> Mistral models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

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

The following extra parameters can be passed to Mistral-7B and Mixtral chat models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `logit_bias` | Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token. | `float` |
| `logprobs` | Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`. | `int` |
| `top_logprobs` | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used. | `float` |
| `n` | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. | `int` |


::: zone-end


::: zone pivot="programming-language-javascript"

## Mistral-7B and Mixtral chat models

The Mistral-7B and Mixtral chat models include the following models:

# [Mistral-7B-Instruct](#tab/mistral-7b-instruct)

The Mistral-7B-Instruct Large Language Model (LLM) is an instruct, fine-tuned version of the Mistral-7B, a transformer model with the following architecture choices:

* Grouped-Query Attention
* Sliding-Window Attention
* Byte-fallback BPE tokenizer


The following models are available:

* [mistralai-Mistral-7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v01)
* [mistralai-Mistral-7B-Instruct-v02](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v02)


# [Mixtral-8x7B-Instruct](#tab/mistral-8x7B-instruct)

The Mixtral-8x7B Large Language Model (LLM) is a pretrained generative Sparse Mixture of Experts. The Mixtral-8x7B outperforms Llama 2 70B on most benchmarks with 6x faster inference.

Mixtral-8x7B-v0.1 is a decoder-only model with eight distinct groups or the "experts". At every layer, for every token, a router network chooses two of these experts to process the token and combine their output additively. Mixtral has 46.7B total parameters but only uses 12.9B parameters per token with this technique; therefore, the model can perform with the same speed and cost as a 12.9B model.


The following models are available:

* [mistralai-Mixtral-8x7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mixtral-8x7B-Instruct-v01)


# [Mixtral-8x22B-Instruct](#tab/mistral-8x22b-instruct)

The Mixtral-8x22B-Instruct-v0.1 Large Language Model (LLM) is an instruct, fine-tuned version of the Mixtral-8x22B-v0.1. The model is a sparse Mixture-of-Experts (SMoE) model that uses only 39B active parameters out of 141B, offering unparalleled cost efficiency for its size.

Mixtral 8x22B comes with the following strengths:

* Fluent in English, French, Italian, German, and Spanish
* Strong mathematics and coding capabilities
* Natively capable of function calling, enabling application development and tech stack modernization at scale
* Precise information recall from large documents, due to its 64K tokens context window


The following models are available:

* [mistralai-Mixtral-8x22B-Instruct-v0-1](https://aka.ms/azureai/landing/mistralai-Mixtral-8x22B-Instruct-v0-1)


---

> [!TIP]
> Additionally, MistralAI supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [MistralAI documentation](https://docs.mistral.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Mistral-7B and Mixtral chat models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

Mistral-7B and Mixtral chat models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../concepts/deployments-overview.md)

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Mistral-7B and Mixtral chat models.

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

When you deploy the model to a self-hosted online endpoint with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```javascript
import ModelClient from "@azure-rest/ai-inference";
import { isUnexpected } from "@azure-rest/ai-inference";
import { DefaultAzureCredential }  from "@azure/identity";

const client = new ModelClient(
    process.env.AZURE_INFERENCE_ENDPOINT, 
    new DefaultAzureCredential()
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
Model name: mistralai-Mistral-7B-Instruct-v01
Model type: chat-completions
Model provider name: MistralAI
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

> [!NOTE]
> mistralai-Mistral-7B-Instruct-v01, mistralai-Mistral-7B-Instruct-v02 and mistralai-Mixtral-8x22B-Instruct-v0-1 don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

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
Model: mistralai-Mistral-7B-Instruct-v01
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

> [!WARNING]
> Mistral models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

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

The following extra parameters can be passed to Mistral-7B and Mixtral chat models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `logit_bias` | Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token. | `float` |
| `logprobs` | Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`. | `int` |
| `top_logprobs` | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used. | `float` |
| `n` | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. | `int` |


::: zone-end


::: zone pivot="programming-language-csharp"

## Mistral-7B and Mixtral chat models

The Mistral-7B and Mixtral chat models include the following models:

# [Mistral-7B-Instruct](#tab/mistral-7b-instruct)

The Mistral-7B-Instruct Large Language Model (LLM) is an instruct, fine-tuned version of the Mistral-7B, a transformer model with the following architecture choices:

* Grouped-Query Attention
* Sliding-Window Attention
* Byte-fallback BPE tokenizer


The following models are available:

* [mistralai-Mistral-7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v01)
* [mistralai-Mistral-7B-Instruct-v02](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v02)


# [Mixtral-8x7B-Instruct](#tab/mistral-8x7B-instruct)

The Mixtral-8x7B Large Language Model (LLM) is a pretrained generative Sparse Mixture of Experts. The Mixtral-8x7B outperforms Llama 2 70B on most benchmarks with 6x faster inference.

Mixtral-8x7B-v0.1 is a decoder-only model with eight distinct groups or the "experts". At every layer, for every token, a router network chooses two of these experts to process the token and combine their output additively. Mixtral has 46.7B total parameters but only uses 12.9B parameters per token with this technique; therefore, the model can perform with the same speed and cost as a 12.9B model.


The following models are available:

* [mistralai-Mixtral-8x7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mixtral-8x7B-Instruct-v01)


# [Mixtral-8x22B-Instruct](#tab/mistral-8x22b-instruct)

The Mixtral-8x22B-Instruct-v0.1 Large Language Model (LLM) is an instruct, fine-tuned version of the Mixtral-8x22B-v0.1. The model is a sparse Mixture-of-Experts (SMoE) model that uses only 39B active parameters out of 141B, offering unparalleled cost efficiency for its size.

Mixtral 8x22B comes with the following strengths:

* Fluent in English, French, Italian, German, and Spanish
* Strong mathematics and coding capabilities
* Natively capable of function calling, enabling application development and tech stack modernization at scale
* Precise information recall from large documents, due to its 64K tokens context window


The following models are available:

* [mistralai-Mixtral-8x22B-Instruct-v0-1](https://aka.ms/azureai/landing/mistralai-Mixtral-8x22B-Instruct-v0-1)


---

> [!TIP]
> Additionally, MistralAI supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [MistralAI documentation](https://docs.mistral.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Mistral-7B and Mixtral chat models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

Mistral-7B and Mixtral chat models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../concepts/deployments-overview.md)

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Mistral-7B and Mixtral chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL"))
);
```

When you deploy the model to a self-hosted online endpoint with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```csharp
client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new DefaultAzureCredential(includeInteractiveCredentials: true)
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
Model name: mistralai-Mistral-7B-Instruct-v01
Model type: chat-completions
Model provider name: MistralAI
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

> [!NOTE]
> mistralai-Mistral-7B-Instruct-v01, mistralai-Mistral-7B-Instruct-v02 and mistralai-Mixtral-8x22B-Instruct-v0-1 don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

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
Model: mistralai-Mistral-7B-Instruct-v01
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

> [!WARNING]
> Mistral models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

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

The following extra parameters can be passed to Mistral-7B and Mixtral chat models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `logit_bias` | Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token. | `float` |
| `logprobs` | Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`. | `int` |
| `top_logprobs` | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used. | `float` |
| `n` | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. | `int` |


::: zone-end


::: zone pivot="programming-language-rest"

## Mistral-7B and Mixtral chat models

The Mistral-7B and Mixtral chat models include the following models:

# [Mistral-7B-Instruct](#tab/mistral-7b-instruct)

The Mistral-7B-Instruct Large Language Model (LLM) is an instruct, fine-tuned version of the Mistral-7B, a transformer model with the following architecture choices:

* Grouped-Query Attention
* Sliding-Window Attention
* Byte-fallback BPE tokenizer


The following models are available:

* [mistralai-Mistral-7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v01)
* [mistralai-Mistral-7B-Instruct-v02](https://aka.ms/azureai/landing/mistralai-Mistral-7B-Instruct-v02)


# [Mixtral-8x7B-Instruct](#tab/mistral-8x7B-instruct)

The Mixtral-8x7B Large Language Model (LLM) is a pretrained generative Sparse Mixture of Experts. The Mixtral-8x7B outperforms Llama 2 70B on most benchmarks with 6x faster inference.

Mixtral-8x7B-v0.1 is a decoder-only model with eight distinct groups or the "experts". At every layer, for every token, a router network chooses two of these experts to process the token and combine their output additively. Mixtral has 46.7B total parameters but only uses 12.9B parameters per token with this technique; therefore, the model can perform with the same speed and cost as a 12.9B model.


The following models are available:

* [mistralai-Mixtral-8x7B-Instruct-v01](https://aka.ms/azureai/landing/mistralai-Mixtral-8x7B-Instruct-v01)


# [Mixtral-8x22B-Instruct](#tab/mistral-8x22b-instruct)

The Mixtral-8x22B-Instruct-v0.1 Large Language Model (LLM) is an instruct, fine-tuned version of the Mixtral-8x22B-v0.1. The model is a sparse Mixture-of-Experts (SMoE) model that uses only 39B active parameters out of 141B, offering unparalleled cost efficiency for its size.

Mixtral 8x22B comes with the following strengths:

* Fluent in English, French, Italian, German, and Spanish
* Strong mathematics and coding capabilities
* Natively capable of function calling, enabling application development and tech stack modernization at scale
* Precise information recall from large documents, due to its 64K tokens context window


The following models are available:

* [mistralai-Mixtral-8x22B-Instruct-v0-1](https://aka.ms/azureai/landing/mistralai-Mixtral-8x22B-Instruct-v0-1)


---

> [!TIP]
> Additionally, MistralAI supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [MistralAI documentation](https://docs.mistral.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Mistral-7B and Mixtral chat models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

Mistral-7B and Mixtral chat models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../concepts/deployments-overview.md)

### A REST client

Models deployed with the [Azure AI model inference API](https://aka.ms/azureai/modelinference) can be consumed using any REST client. To use the REST client, you need the following prerequisites:

* To construct the requests, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name`` is your unique model deployment host name and `your-azure-region`` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

## Work with chat completions

In this section, you use the [Azure AI model inference API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Mistral-7B and Mixtral chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

When you deploy the model to a self-hosted online endpoint with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

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
    "model_name": "mistralai-Mistral-7B-Instruct-v01",
    "model_type": "chat-completions",
    "model_provider_name": "MistralAI"
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

> [!NOTE]
> mistralai-Mistral-7B-Instruct-v01, mistralai-Mistral-7B-Instruct-v02 and mistralai-Mixtral-8x22B-Instruct-v0-1 don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

The response is as follows, where you can see the model's usage statistics:


```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "mistralai-Mistral-7B-Instruct-v01",
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
    "model": "mistralai-Mistral-7B-Instruct-v01",
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
    "model": "mistralai-Mistral-7B-Instruct-v01",
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
    "model": "mistralai-Mistral-7B-Instruct-v01",
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

> [!WARNING]
> Mistral models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

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

The following extra parameters can be passed to Mistral-7B and Mixtral chat models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `logit_bias` | Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token. | `float` |
| `logprobs` | Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the `content` of `message`. | `int` |
| `top_logprobs` | An integer between 0 and 20 specifying the number of most likely tokens to return at each token position, each with an associated log probability. `logprobs` must be set to `true` if this parameter is used. | `float` |
| `n` | How many chat completion choices to generate for each input message. Note that you will be charged based on the number of generated tokens across all of the choices. | `int` |


::: zone-end

## More inference examples

For more examples of how to use Mistral models, see the following examples and tutorials:

| Description                               | Language          | Sample                                                          |
|-------------------------------------------|-------------------|-----------------------------------------------------------------|
| CURL request                              | Bash              | [Link](https://aka.ms/mistral-large/webrequests-sample)         |
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://aka.ms/azsdk/azure-ai-inference/javascript/samples)  |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  |
| Python web requests                       | Python            | [Link](https://aka.ms/mistral-large/webrequests-sample)         |
| OpenAI SDK (experimental)                 | Python            | [Link](https://aka.ms/mistral-large/openaisdk)                  |
| LangChain                                 | Python            | [Link](https://aka.ms/mistral-large/langchain-sample)           |
| Mistral AI                                | Python            | [Link](https://aka.ms/mistral-large/mistralai-sample)           |
| LiteLLM                                   | Python            | [Link](https://aka.ms/mistral-large/litellm-sample)             | 


## Cost and quota considerations for Mistral models deployed to managed compute

Mistral models deployed to managed compute are billed based on core hours of the associated compute instance. The cost of the compute instance is determined by the size of the instance, the number of instances running, and the run duration.

It is a good practice to start with a low number of instances and scale up as needed. You can monitor the cost of the compute instance in the Azure portal.

## Related content


* [Azure AI Model Inference API](../reference/reference-model-inference-api.md)
* [Deploy models as serverless APIs](deploy-models-serverless.md)
* [Consume serverless API endpoints from a different Azure AI Foundry project or hub](deploy-models-serverless-connect.md)
* [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md)
* [Plan and manage costs (marketplace)](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace)
