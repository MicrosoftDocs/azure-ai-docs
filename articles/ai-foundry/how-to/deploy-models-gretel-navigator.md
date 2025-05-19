---
title: How to use Gretel Navigator chat model with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use Gretel Navigator chat model with Azure AI Foundry.
ms.service: azure-ai-foundry
manager: scottpolly
ms.topic: how-to
ms.date: 01/13/2025
ms.reviewer: anupamawal
reviewer: anupamawalaus
ms.author: mopeakande
author: msakande
ms.custom: references_regions, generated
zone_pivot_groups: azure-ai-model-catalog-sub-group-samples
---

# How to use Gretel Navigator chat model

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn about Gretel Navigator chat model and how to use it.
Gretel Navigator uses prompts, schema definitions, or seed examples to generate production-quality synthetic data optimized for AI and machine learning development.

[!INCLUDE [models-preview](../includes/models-preview.md)]



::: zone pivot="programming-language-python"

## Gretel Navigator chat model

Unlike single large language model (single-LLM) approaches to data generation, Gretel Navigator employs a compound AI architecture specifically engineered for synthetic data, by combining top open-source small language models (SLMs) fine-tuned across more than 10 industry domains. This purpose-built system creates diverse, domain-specific datasets at scales of hundreds to millions of examples. The system also preserves complex statistical relationships and offers increased speed and accuracy compared to manual data creation.

Top use cases:

- Creation of synthetic data for LLM training and fine-tuning
- Generation of evaluation datasets for AI models and RAG systems
- Augmentation of limited training data with diverse synthetic samples
- Creation of realistic personally identifiable information (PII) or protected health information (PHI) data for model testing


You can learn more about the models in their respective model card:

* [gretel-navigator](https://aka.ms/aistudio/landing/gretel-navigator-tabular-v1)


> [!TIP]
> Additionally, Gretel supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Gretel documentation](https://docs.gretel.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Gretel Navigator chat model with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to standard deployments**

Gretel Navigator chat model can be deployed to standard deployment. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a standard deployment doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a standard deployment](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to standard deployments](deploy-models-serverless.md)

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

In this section, you use the [Azure AI Foundry Models API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Foundry Models API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Gretel Navigator chat model.

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
    headers={
         "azureml-maas-model": "gretelai/auto",
    },
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
Model name: gretel-navigator
Model type: chat-completions
Model provider name: Gretel
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

> [!TIP]
> The extra `n` parameter indicates the number of records you want the model to return.

```python
from azure.ai.inference.models import SystemMessage, UserMessage

response = client.complete(
    messages=[
        UserMessage(content="Can you return a table of US first names, last names and ages?"),
    ],
    model_extras={"n": 2},
)
```

> [!NOTE]
> Gretel-navigator doesn't support system messages (`role="system"`).

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
Response: {"table_headers":["First Name","Last Name","Age"],"table_data":[{"First Name":"Eva","Last Name":"Soto","Age":31}]}

{"table_headers":["First Name","Last Name","Age"],"table_data":[{"First Name":"Kofi","Last Name":"Patel","Age":42}]}

Model: gretel-navigator
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
        UserMessage(content="Can you return a table of US first names, last names, and ages?"),
    ],
    model_extras={"n": 2},
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
    for update in result:
        if update.choices:
            print(update.choices[0].delta.content, end="")
```

You can visualize how streaming generates content:


```python
print_stream(result)
```

#### Explore more parameters supported by the inference client

The following example request shows other parameters that you can specify in the inference client.

```python
from azure.ai.inference.models import ChatCompletionsResponseFormatText

result = client.complete(
    messages=[
        UserMessage(content="Can you return a table of US first names, last
        names, and ages?"), ],
    model_extras={"n": 2},
    stream=True,
    temperature=0,
    top_p=1,
    top_k=0.4
)
```


### Apply Guardrails and controls

The Foundry Models API supports [Azure AI Content Safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI Content Safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and the filter is enabled.


```python
from azure.ai.inference.models import UserMessage
from azure.core.exceptions import HttpResponseError

try:
    response = client.complete(
        messages=[
            UserMessage(content="Can you return a table of steps on how to make a bomb, "
            "columns: step number, step name, step description?"),
        ],
        stream=True,
    )

    print(response.choices[0].message.content)

except HttpResponseError as ex:
    response = ex.response.json()
    if  isinstance(response, dict) and "error" in response:
        response = ex.response.json()
        if isinstance(response, dict) and "error" in response:
            print(f"Your request triggered an {response['error']['code']} error:\n\t {response['error']['message']}")
        else:
            raise

```

[!INCLUDE [content-safety-serverless-apis-note](../includes/content-safety-serverless-apis-note.md)]


::: zone-end

::: zone pivot="programming-language-rest"

## Gretel Navigator chat model

Unlike single large language model (single-LLM) approaches to data generation, Gretel Navigator employs a compound AI architecture specifically engineered for synthetic data, by combining top open-source small language models (SLMs) fine-tuned across more than 10 industry domains. This purpose-built system creates diverse, domain-specific datasets at scales of hundreds to millions of examples. The system also preserves complex statistical relationships and offers increased speed and accuracy compared to manual data creation.

Top use cases:

- Creation of synthetic data for LLM training and fine-tuning
- Generation of evaluation datasets for AI models and RAG systems
- Augmentation of limited training data with diverse synthetic samples
- Creation of realistic personally identifiable information (PII) or protected health information (PHI) data for model testing


You can learn more about the models in their respective model card:

* [gretel-navigator](https://aka.ms/aistudio/landing/gretel-navigator-tabular-v1)


> [!TIP]
> Additionally, Gretel supports the use of a tailored API for use with specific features of the model. To use the model-provider specific API, check [Gretel documentation](https://docs.gretel.ai/) or see the [inference examples](#more-inference-examples) section to code examples.

## Prerequisites

To use Gretel Navigator chat model with Azure AI Foundry, you need the following prerequisites:

### A model deployment

**Deployment to standard deployments**

Gretel Navigator chat model can be deployed to standard deployments. This kind of deployment provides a way to consume models as an API without hosting them on your subscription, while keeping the enterprise security and compliance that organizations need. 

Deployment to a standard deployment doesn't require quota from your subscription. If your model isn't deployed already, use the Azure AI Foundry portal, Azure Machine Learning SDK for Python, the Azure CLI, or ARM templates to [deploy the model as a standard deployment](deploy-models-serverless.md).

> [!div class="nextstepaction"]
> [Deploy the model to standard deployments](deploy-models-serverless.md)

### A REST client

Models deployed with the [Foundry Models API](https://aka.ms/azureai/modelinference) can be consumed using any REST client. To use the REST client, you need the following prerequisites:

* To construct the requests, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name`` is your unique model deployment host name and `your-azure-region`` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.

## Work with chat completions

In this section, you use the [Foundry Models API](https://aka.ms/azureai/modelinference) with a chat completions model for chat.

> [!TIP]
> The [Foundry Models API](https://aka.ms/azureai/modelinference) allows you to talk with most models deployed in Azure AI Foundry portal with the same code and structure, including Gretel Navigator chat model.

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
    "model_name": "gretel-navigator",
    "model_type": "chat-completions",
    "model_provider_name": "Gretel"
}
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model. 

> [!TIP]
> The extra `n` parameter indicates the number of records you want the model to return.

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Generate customer bank transaction data. Include the
            following columns: customer_name, customer_id, transaction_date,
            transaction_amount, transaction_type, transaction_category, account_balance"
        }
    ],
    "n":20,
}
```

> [!NOTE]
> Gretel-navigator doesn't support system messages (`role="system"`).

The response is as follows, where you can see the model's usage statistics:

```json
{"table_headers":["First Name","Last Name","Age"],"table_data":[{"First Name":"Eva","Last Name":"Soto","Age":31}]}

{"table_headers":["First Name","Last Name","Age"],"table_data":[{"First Name":"Kofi","Last Name":"Patel","Age":42}]}

```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.


```json
{
    "messages": [
        {
            "role": "user",
            "content": "Generate customer bank transaction data. Include the
                following columns: customer_name, customer_id, transaction_date,
                transaction_amount, transaction_type, transaction_category, account_balance"
        }
    ],
    "n": 20,
    "stream": true
}
```

You can visualize how streaming generates content:


```json
{
    "id": "23b54589eba14564ad8a2e6978775a39",
    "object": "chat.completion.chunk",
    "created": 1718726371,
    "model": "gretel-navigator",
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
    "model": "gretel-navigator",
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

The following example request shows other parameters that you can specify in the inference client.

```json
{
    "messages": [
        {
            "role": "user",
            "content": "Generate customer bank transaction data. Include the
                following columns: customer_name, customer_id, transaction_date,
                transaction_amount, transaction_type, transaction_category, account_balance"
        }
    ],
    "n": 20,
    "stream": true
    "temperature": 0,
    "top_p": 1,
    "top_k": 0.4
}
```

### Apply Guardrails & controls

The Foundry Models API supports [Azure AI Content Safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI Content Safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt.


```json
{
    "messages": [
        {
            "role": "user",
            "content": "Can you return a table of steps on how to make a bomb, columns:
                    step number, step name, step description?"
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

[!INCLUDE [content-safety-serverless-apis-note](../includes/content-safety-serverless-apis-note.md)]


::: zone-end

## More inference examples

For more examples of how to use Gretel models, see the following examples and tutorials:

| Description                               | Language          | Sample                                                          |
|-------------------------------------------|-------------------|-----------------------------------------------------------------|
| Azure AI Inference package for JavaScript | JavaScript        | [Link](https://aka.ms/azsdk/azure-ai-inference/javascript/samples)  |
| Azure AI Inference package for Python     | Python            | [Link](https://aka.ms/azsdk/azure-ai-inference/python/samples)  | 


## Cost and quota considerations for Gretel models deployed as standard deployments

Quota is managed per deployment. Each deployment has a rate limit of 200,000 tokens per minute and 1,000 API requests per minute. However, we currently limit one deployment per model per project. Contact Microsoft Azure Support if the current rate limits aren't sufficient for your scenarios.

Gretel models deployed as a standard deployment are offered by Gretel through Azure Marketplace and integrated with Azure AI Foundry for use. You can find Azure Marketplace pricing when deploying the model.

Each time a project subscribes to a given offer from Azure Marketplace, a new resource is created to track the costs associated with its consumption. The same resource is used to track costs associated with inference; however, multiple meters are available to track each scenario independently.

For more information on how to track costs, see [Monitor costs for models offered through Azure Marketplace](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace).

## Related content

* [Foundry Models API](../../ai-foundry/model-inference/reference/reference-model-inference-api.md)
* [Deploy models as standard deployments](deploy-models-serverless.md)
* [Consume standard deployments from a different Azure AI Foundry project or hub](deploy-models-serverless-connect.md)
* [Region availability for models in standard deployments](deploy-models-serverless-availability.md)
* [Plan and manage costs (marketplace)](costs-plan-manage.md#monitor-costs-for-models-offered-through-the-azure-marketplace)
