---
title: How to use the Meta Llama family of models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use the Meta Llama family of models with Azure AI Foundry.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 08/08/2024
ms.reviewer: shubhiraj
reviewer: shubhirajMsft
ms.author: ssalgado
author: ssalgadodev
ms.custom: references_regions, generated, ai-learning-hub
zone_pivot_groups: azure-ai-model-catalog-samples-chat
---

# How to use the Meta Llama family of models

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn about the Meta Llama family of models and how to use them. Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models - ranging in scale from SLMs (1B, 3B Base and Instruct models) for on-device and edge inferencing - to mid-size LLMs (7B, 8B and 70B Base and Instruct models) and high performant models like Meta Llama 3.1 405B Instruct for synthetic data generation and distillation use cases.

See our announcements of Meta's Llama 3.2 family models available now on Azure AI Model Catalog through [Meta's blog](https://aka.ms/llama-3.2-meta-announcement) and [Microsoft Tech Community Blog](https://aka.ms/llama-3.2-microsoft-announcement).

[!INCLUDE [models-preview](../includes/models-preview.md)]

::: zone pivot="programming-language-python"

## Meta Llama family of models

The Meta Llama family of models include the following models:

# [Llama-3.2](#tab/python-llama-3-2)

The Llama 3.2 collection of SLMs and image reasoning models are now available. Coming soon, Llama 3.2 11B Vision Instruct and Llama 3.2 90B Vision Instruct will be available as a serverless API endpoint via Models-as-a-Service. Starting today, the following models will be available for deployment via managed compute:
* Llama 3.2 1B
* Llama 3.2 3B
* Llama 3.2 1B Instruct
* Llama 3.2 3B Instruct
* Llama Guard 3 1B
* Llama Guard 11B Vision
* Llama 3.2 11B Vision Instruct
* Llama 3.2 90B Vision Instruct are available for managed compute deployment.

# [Meta Llama-3.1](#tab/python-meta-llama-3-1)

The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models (8B, 70B, 405B) are optimized for multilingual dialogue use cases and outperform many of the available open-source and closed models on common industry benchmarks.


The following models are available:

* [Meta-Llama-3.1-405B-Instruct](https://aka.ms/azureai/landing/Meta-Llama-3.1-405B-Instruct)
* [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/1/registry/azureml-meta)
* [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/1/registry/azureml-meta)


# [Meta Llama-3](#tab/python-meta-llama-3)

Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, and 70B sizes. The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open-source models on common industry benchmarks. Further, in developing these models, we took great care to optimize helpfulness and safety.


The following models are available:

* [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/6/registry/azureml-meta)
* [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/6/registry/azureml-meta)


# [Meta Llama-2](#tab/python-meta-llama-2)

Meta has developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM. We provide a detailed description of our approach to fine-tuning and safety improvements of Llama-2-Chat in order to enable the community to build on our work and contribute to the responsible development of LLMs.


The following models are available:

* [Llama-2-70b-chat](https://ai.azure.com/explore/models/Llama-2-70b-chat/version/20/registry/azureml-meta)
* [Llama-2-13b-chat](https://ai.azure.com/explore/models/Llama-2-13b-chat/version/20/registry/azureml-meta)
* [Llama-2-7b-chat](https://ai.azure.com/explore/models/Llama-2-7b-chat/version/24/registry/azureml-meta)


---

## Prerequisites

To use Meta Llama models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Meta Llama models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](deploy-models-serverless.md)

**Deployment to a self-hosted managed compute**

Meta Llama models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Meta Llama Instruct models - text-only or image reasoning models.

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

> [!NOTE]
> Currently, serverless API endpoints do not support using Microsoft Entra ID for authentication.

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
Model name: Meta-Llama-3.1-405B-Instruct
Model type: chat-completions
Model provider name: Meta
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
Model: Meta-Llama-3.1-405B-Instruct
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
> Meta Llama models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

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

The following extra parameters can be passed to Meta Llama models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `n` | How many completions to generate for each prompt. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `best_of` | Generates best_of completions server-side and returns the *best* (the one with the lowest log probability per token). Results can't be streamed. When used with `n`, best_of controls the number of candidate completions and n specifies how many to return—best_of must be greater than `n`. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `logprobs` | A number indicating to include the log probabilities on the logprobs most likely tokens and the chosen tokens. For example, if logprobs is 10, the API returns a list of the 10 most likely tokens. the API will always return the logprob of the sampled token, so there might be up to logprobs+1 elements in the response. | `integer` |
| `ignore_eos` | Whether to ignore the `EOS` token and continue generating tokens after the `EOS` token is generated. | `boolean` |
| `use_beam_search` | Whether to use beam search instead of sampling. In such case, `best_of` must be greater than 1 and temperature must be 0. | `boolean` |
| `stop_token_ids` | List of IDs for tokens that, when generated, stop further token generation. The returned output contains the stop tokens unless the stop tokens are special tokens. | `array` |
| `skip_special_tokens` | Whether to skip special tokens in the output. | `boolean` |


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

> [!NOTE]
> Azure AI content safety is only available for models deployed as serverless API endpoints.

::: zone-end


::: zone pivot="programming-language-javascript"

## Meta Llama models

The Meta Llama models include the following models:

# [Meta Llama-3.1](#tab/meta-llama-3-1)

The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models (8B, 70B, 405B) are optimized for multilingual dialogue use cases and outperform many of the available open-source and closed chat models on common industry benchmarks.


The following models are available:

* [Meta-Llama-3.1-405B-Instruct](https://aka.ms/azureai/landing/Meta-Llama-3.1-405B-Instruct)
* [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/1/registry/azureml-meta)
* [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/1/registry/azureml-meta)


# [Meta Llama-3](#tab/meta-llama-3)

Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B, and 405B sizes. The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open-source chat models on common industry benchmarks. Further, in developing these models, we took great care to optimize helpfulness and safety.


The following models are available:

* [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/6/registry/azureml-meta)
* [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/6/registry/azureml-meta)


# [Meta Llama-2](#tab/meta-llama-2)

Meta has developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM. We provide a detailed description of our approach to fine-tuning and safety improvements of Llama-2-Chat in order to enable the community to build on our work and contribute to the responsible development of LLMs.


The following models are available:

* [Llama-2-70b-chat](https://ai.azure.com/explore/models/Llama-2-70b-chat/version/20/registry/azureml-meta)
* [Llama-2-13b-chat](https://ai.azure.com/explore/models/Llama-2-13b-chat/version/20/registry/azureml-meta)
* [Llama-2-7b-chat](https://ai.azure.com/explore/models/Llama-2-7b-chat/version/24/registry/azureml-meta)


---

## Prerequisites

To use Meta Llama models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Meta Llama models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](deploy-models-serverless.md)

**Deployment to a self-hosted managed compute**

Meta Llama models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Meta Llama models.

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

> [!NOTE]
> Currently, serverless API endpoints do not support using Microsoft Entra ID for authentication.

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
Model name: Meta-Llama-3.1-405B-Instruct
Model type: chat-completions
Model provider name: Meta
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
Model: Meta-Llama-3.1-405B-Instruct
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
> Meta Llama models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

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

The following extra parameters can be passed to Meta Llama models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `n` | How many completions to generate for each prompt. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `best_of` | Generates best_of completions server-side and returns the *best* (the one with the lowest log probability per token). Results can't be streamed. When used with `n`, best_of controls the number of candidate completions and n specifies how many to return—best_of must be greater than `n`. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `logprobs` | A number indicating to include the log probabilities on the logprobs most likely tokens and the chosen tokens. For example, if logprobs is 10, the API returns a list of the 10 most likely tokens. the API will always return the logprob of the sampled token, so there might be up to logprobs+1 elements in the response. | `integer` |
| `ignore_eos` | Whether to ignore the `EOS` token and continue generating tokens after the `EOS` token is generated. | `boolean` |
| `use_beam_search` | Whether to use beam search instead of sampling. In such case, `best_of` must be greater than 1 and temperature must be 0. | `boolean` |
| `stop_token_ids` | List of IDs for tokens that, when generated, stop further token generation. The returned output contains the stop tokens unless the stop tokens are special tokens. | `array` |
| `skip_special_tokens` | Whether to skip special tokens in the output. | `boolean` |


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

> [!NOTE]
> Azure AI content safety is only available for models deployed as serverless API endpoints.

::: zone-end


::: zone pivot="programming-language-csharp"

## Meta Llama models

The Meta Llama models include the following models:

# [Meta Llama-3.1](#tab/meta-llama-3-1)

The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models (8B, 70B, 405B) are optimized for multilingual dialogue use cases and outperform many of the available open-source and closed models on common industry benchmarks.


The following models are available:

* [Meta-Llama-3.1-405B-Instruct](https://aka.ms/azureai/landing/Meta-Llama-3.1-405B-Instruct)
* [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/1/registry/azureml-meta)
* [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/1/registry/azureml-meta)


# [Meta Llama-3](#tab/meta-llama-3)

Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B, and 405B sizes. The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open-source models on common industry benchmarks. Further, in developing these models, we took great care to optimize helpfulness and safety.


The following models are available:

* [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/6/registry/azureml-meta)
* [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/6/registry/azureml-meta)


# [Meta Llama-2](#tab/meta-llama-2)

Meta has developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM. We provide a detailed description of our approach to fine-tuning and safety improvements of Llama-2-Chat in order to enable the community to build on our work and contribute to the responsible development of LLMs.


The following models are available:

* [Llama-2-70b-chat](https://ai.azure.com/explore/models/Llama-2-70b-chat/version/20/registry/azureml-meta)
* [Llama-2-13b-chat](https://ai.azure.com/explore/models/Llama-2-13b-chat/version/20/registry/azureml-meta)
* [Llama-2-7b-chat](https://ai.azure.com/explore/models/Llama-2-7b-chat/version/24/registry/azureml-meta)


---

## Prerequisites

To use Meta Llama models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Meta Llama models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](deploy-models-serverless.md)

**Deployment to a self-hosted managed compute**

Meta Llama models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Meta Llama chat models.

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

> [!NOTE]
> Currently, serverless API endpoints do not support using Microsoft Entra ID for authentication.

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
Model name: Meta-Llama-3.1-405B-Instruct
Model type: chat-completions
Model provider name: Meta
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
Model: Meta-Llama-3.1-405B-Instruct
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
> Meta Llama models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

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

The following extra parameters can be passed to Meta Llama models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `n` | How many completions to generate for each prompt. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `best_of` | Generates best_of completions server-side and returns the *best* (the one with the lowest log probability per token). Results can't be streamed. When used with `n`, best_of controls the number of candidate completions and n specifies how many to return—best_of must be greater than `n`. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `logprobs` | A number indicating to include the log probabilities on the logprobs most likely tokens and the chosen tokens. For example, if logprobs is 10, the API returns a list of the 10 most likely tokens. the API will always return the logprob of the sampled token, so there might be up to logprobs+1 elements in the response. | `integer` |
| `ignore_eos` | Whether to ignore the `EOS` token and continue generating tokens after the `EOS` token is generated. | `boolean` |
| `use_beam_search` | Whether to use beam search instead of sampling. In such case, `best_of` must be greater than 1 and temperature must be 0. | `boolean` |
| `stop_token_ids` | List of IDs for tokens that, when generated, stop further token generation. The returned output contains the stop tokens unless the stop tokens are special tokens. | `array` |
| `skip_special_tokens` | Whether to skip special tokens in the output. | `boolean` |


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

> [!NOTE]
> Azure AI content safety is only available for models deployed as serverless API endpoints.

::: zone-end


::: zone pivot="programming-language-rest"

## Meta Llama chat models

The Meta Llama chat models include the following models:

# [Meta Llama-3.1](#tab/meta-llama-3-1)

The Meta Llama 3.1 collection of multilingual large language models (LLMs) is a collection of pretrained and instruction tuned generative models in 8B, 70B and 405B sizes (text in/text out). The Llama 3.1 instruction tuned text only models (8B, 70B, 405B) are optimized for multilingual dialogue use cases and outperform many of the available open-source and closed chat models on common industry benchmarks.


The following models are available:

* [Meta-Llama-3.1-405B-Instruct](https://aka.ms/azureai/landing/Meta-Llama-3.1-405B-Instruct)
* [Meta-Llama-3.1-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-70B-Instruct/version/1/registry/azureml-meta)
* [Meta-Llama-3.1-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3.1-8B-Instruct/version/1/registry/azureml-meta)


# [Meta Llama-3](#tab/meta-llama-3)

Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8B, 70B, and 405B sizes. The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open-source chat models on common industry benchmarks. Further, in developing these models, we took great care to optimize helpfulness and safety.


The following models are available:

* [Meta-Llama-3-70B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-70B-Instruct/version/6/registry/azureml-meta)
* [Meta-Llama-3-8B-Instruct](https://ai.azure.com/explore/models/Meta-Llama-3-8B-Instruct/version/6/registry/azureml-meta)


# [Meta Llama-2](#tab/meta-llama-2)

Meta has developed and publicly released the Llama 2 family of large language models (LLMs), a collection of pretrained and fine-tuned generative text models ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama-2-Chat, are optimized for dialogue use cases. Llama-2-Chat models outperform open-source chat models on most benchmarks we tested, and in our human evaluations for helpfulness and safety, are on par with some popular closed-source models like ChatGPT and PaLM. We provide a detailed description of our approach to fine-tuning and safety improvements of Llama-2-Chat in order to enable the community to build on our work and contribute to the responsible development of LLMs.


The following models are available:

* [Llama-2-70b-chat](https://ai.azure.com/explore/models/Llama-2-70b-chat/version/20/registry/azureml-meta)
* [Llama-2-13b-chat](https://ai.azure.com/explore/models/Llama-2-13b-chat/version/20/registry/azureml-meta)
* [Llama-2-7b-chat](https://ai.azure.com/explore/models/Llama-2-7b-chat/version/24/registry/azureml-meta)


---

## Prerequisites

To use Meta Llama models with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to serverless APIs**

Meta Llama chat models can be deployed to serverless API endpoints with pay-as-you-go billing. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a serverless API endpoint doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a serverless API](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to serverless API endpoints](deploy-models-serverless.md)

**Deployment to a self-hosted managed compute**

Meta Llama models can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

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
> The [Azure AI model inference API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Meta Llama chat models.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.

When you deploy the model to a self-hosted online endpoint with **Microsoft Entra ID** support, you can use the following code snippet to create a client.

> [!NOTE]
> Currently, serverless API endpoints do not support using Microsoft Entra ID for authentication.

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
    "model_name": "Meta-Llama-3.1-405B-Instruct",
    "model_type": "chat-completions",
    "model_provider_name": "Meta"
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
    "model": "Meta-Llama-3.1-405B-Instruct",
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
    "model": "Meta-Llama-3.1-405B-Instruct",
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
    "model": "Meta-Llama-3.1-405B-Instruct",
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
    "model": "Meta-Llama-3.1-405B-Instruct",
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
> Meta Llama models don't support JSON output formatting (`response_format = { "type": "json_object" }`). You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

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

The following extra parameters can be passed to Meta Llama chat models:

| Name           | Description           | Type            |
| -------------- | --------------------- | --------------- |
| `n` | How many completions to generate for each prompt. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `best_of` | Generates best_of completions server-side and returns the *best* (the one with the lowest log probability per token). Results can't be streamed. When used with `n`, best_of controls the number of candidate completions and n specifies how many to return—best_of must be greater than `n`. Note: Because this parameter generates many completions, it can quickly consume your token quota. | `integer` |
| `logprobs` | A number indicating to include the log probabilities on the logprobs most likely tokens and the chosen tokens. For example, if logprobs is 10, the API returns a list of the 10 most likely tokens. the API will always return the logprob of the sampled token, so there might be up to logprobs+1 elements in the response. | `integer` |
| `ignore_eos` | Whether to ignore the `EOS` token and continue generating tokens after the `EOS` token is generated. | `boolean` |
| `use_beam_search` | Whether to use beam search instead of sampling. In such case, `best_of` must be greater than 1 and temperature must be 0. | `boolean` |
| `stop_token_ids` | List of IDs for tokens that, when generated, stop further token generation. The returned output contains the stop tokens unless the stop tokens are special tokens. | `array` |
| `skip_special_tokens` | Whether to skip special tokens in the output. | `boolean` |


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

> [!NOTE]
> Azure AI content safety is only available for models deployed as serverless API endpoints.

::: zone-end

## More inference examples

For more examples of how to use Meta Llama models, see the following examples and tutorials:

| Description                               | Language          | Sample                                                             |
|-------------------------------------------|-------------------|------------------------------------------------------------------- |
| CURL request                              | Bash              | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-webrequests)    |
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://github.com/Azure/azureml-examples/blob/main/sdk/typescript/README.md) |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)     |
| Python web requests                       | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-webrequests)    |
| OpenAI SDK (experimental)                 | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-openai)         |
| LangChain                                 | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-langchain)      |
| LiteLLM                                   | Python            | [Link](https://aka.ms/meta-llama-3.1-405B-instruct-litellm)        | 

## Cost and quota considerations for Meta Llama models deployed as serverless API endpoints

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

Meta Llama models deployed as a serverless API are offered by Meta through the Azure Marketplace and integrated with Azure AI Foundry for use. You can find the Azure Marketplace pricing when deploying the model.

Each time a project subscribes to a given offer from the Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through the Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

## Cost and quota considerations for Meta Llama models deployed to managed compute

Meta Llama models deployed to managed compute are billed based on core hours of the associated compute instance. The cost of the compute instance is determined by the size of the instance, the number of instances running, and the run duration.

It is a good practice to start with a low number of instances and scale up as needed. You can monitor the cost of the compute instance in the Azure portal.

## Related content


* [Azure AI Model Inference API](../reference/reference-model-inference-api.md)
* [Deploy models as serverless APIs](deploy-models-serverless.md)
* [Consume serverless API endpoints from a different Azure AI Foundry project or hub](deploy-models-serverless-connect.md)
* [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md)
* [Plan and manage costs (marketplace)](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace)
