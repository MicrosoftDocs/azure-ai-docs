---
title: Develop application with LlamaIndex and Microsoft Foundry
titleSuffix: Microsoft Foundry
description: This article explains how to use LlamaIndex with models deployed in Microsoft Foundry portal to build advance intelligent applications.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - dev-focus
ms.topic: how-to
ai-usage: ai-assisted
ms.date: 12/30/2025
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
---

# Develop applications with LlamaIndex and Microsoft Foundry

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, you learn how to use [LlamaIndex](https://github.com/run-llama/llama_index) with models deployed from the model catalog in Microsoft Foundry.

<!-- ::: moniker range="foundry-classic" -->
You can use models deployed to [!INCLUDE [classic-link](../../includes/classic-link.md)] with LlamaIndex in two ways:
<!-- ::: moniker-end

::: moniker range="foundry"
You can use models deployed to [!INCLUDE [foundry-link](../../default/includes/foundry-link.md)] with LlamaIndex in two ways:
::: moniker-end -->

- **Using the model's provider specific API:** Some models, like OpenAI, Cohere, or Mistral, offer their own set of APIs and extensions for LlamaIndex. Those extensions might include specific functionalities that the model support and hence are suitable if you want to exploit them. When working with `llama-index`, install the extension specific for the model you want to use, like `llama-index-llms-openai` or `llama-index-llms-cohere`.

- **Using the Azure AI Model Inference API:** All models deployed to Foundry support the [Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md), which offers a common set of functionalities that most models in the catalog can use. The benefit of this API is that, since it's the same for all the models, changing from one to another is as simple as changing the model deployment being use. No further changes are required in the code. When working with LlamaIndex, install the extensions `llama-index-llms-azure-inference` and `llama-index-embeddings-azure-inference`.

In this example, you work with the **Model Inference API**.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Prerequisites

To run this tutorial, you need:

* [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
* A [Foundry project](../create-projects.md).

<!-- :::moniker range="foundry-classic" -->
* Required role: 
    * **Owner** or **Contributor** on the Foundry resource or AI Hub to deploy models
    * **Azure AI User** to use the model in a Foundry project
    * **Azure AI Developer** to use the model in a hub-based project
<!-- :::moniker-end

:::moniker range="foundry"
* Required role: 
    * **Owner** or **Contributor** on the Foundry resource to deploy models
    * **Azure AI User** to use the model in a Foundry project
:::moniker-end -->

* A model deployment that supports the [Model Inference API](https://aka.ms/azureai/modelinference). This article uses `Mistral-Large-3` in code examples; you can substitute your own deployed model name.
* To use embeddings capabilities in LlamaIndex, you need an embedding model like `cohere-embed-v3-multilingual`. 

    * You can follow the instructions at [Deploy models as serverless API deployments](../deploy-models-serverless.md).

* Python 3.8 or later installed, including pip.
* LlamaIndex installed. You can install it by using the following command:

    ```bash
    pip install llama-index
    ```

* In this example, you're working with the Model Inference API, so you install the following packages:

    ```bash
    pip install -U llama-index-llms-azure-inference
    pip install -U llama-index-embeddings-azure-inference
    ```

    > [!IMPORTANT]
    > Using the [Foundry Models service](https://aka.ms/aiservices/inference) requires version `0.2.4` for `llama-index-llms-azure-inference` or `llama-index-embeddings-azure-inference`.

## Configure the environment


<!-- ::: moniker range="foundry-classic" -->
[!INCLUDE [set-endpoint](../../includes/set-endpoint.md)]
<!-- ::: moniker-end

::: moniker range="foundry"
[!INCLUDE [set-endpoint](../../default/includes/set-endpoint.md)]
::: moniker-end -->

After you configure the environment, create a client to connect to the endpoint.

```python
import os
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

> [!TIP]
> If your model deployment is hosted in Azure OpenAI in Foundry Models or Foundry Tools resource, configure the client as indicated at [Azure OpenAI models and Foundry Models service](#azure-openai-models-and-foundry-models-service).


If your endpoint serves more than one model, like with the [Foundry Models service](../../foundry-models/concepts/models-sold-directly-by-azure.md) or [GitHub Models](https://github.com/marketplace/models), you need to specify the `model_name` parameter:

```python
import os
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="Mistral-Large-3",
)
```

**What this does:** Creates an LLM client with explicit model name specification for multi-model endpoints. The `model_name` parameter tells the service which model to use for chat completions.

**References:**
- [LlamaIndex Azure Inference Integration](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/)
- [AzureAICompletionsModel Parameters](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/llms/llama-index-llms-azure-inference/llama_index/llms/azure_inference/base.py)

Alternatively, if your endpoint supports Microsoft Entra ID, you can use the following code to create the client:

```python
import os
from azure.identity import DefaultAzureCredential
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

**What this does:** Creates an LLM client using Microsoft Entra ID (Azure AD) authentication, which is more secure for production environments than API keys.

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint is deployed with that authentication method and that you have the required permissions to invoke it.

### Verify your setup

Test your client connection with a simple invocation:

```python
from llama_index.core.llms import ChatMessage

messages = [ChatMessage(role="user", content="Hello")]
response = llm.chat(messages)
print(response)
```

**What this does:** Calls the model with a simple message to verify authentication and connectivity. Expected output: A response object containing the model's greeting message.

**References:**
- [LlamaIndex ChatMessage](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/)
- [LlamaIndex LLM Chat Method](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/)

If you plan to use asynchronous calling, use the asynchronous version for the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
)
```

### Azure OpenAI models and Foundry Models service

If you're using Azure OpenAI or [Foundry Models service](../../foundry-models/concepts/models-sold-directly-by-azure.md), make sure you have at least version `0.2.4` of the LlamaIndex integration. Use the `api_version` parameter if you need to select a specific `api_version`. 

For the [Foundry Models service](../../foundry-models/concepts/models-sold-directly-by-azure.md), you need to pass the `model_name` parameter:

```python
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="Mistral-Large-3",
)
```

For Azure OpenAI in Foundry Models:

```python
from llama_index.llms.azure_inference import AzureAICompletionsModel

llm = AzureAICompletionsModel(
    endpoint="https://<resource>.openai.azure.com/openai/deployments/<deployment-name>",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    api_version="2024-05-01-preview",
)
```

> [!TIP]
> Check which API version your deployment is using. Using a wrong `api_version` or one not supported by the model results in a `ResourceNotFound` exception.

### Inference parameters

You can configure how inference is performed for all the operations that use this client by setting extra parameters. This approach helps you avoid specifying them on each call you make to the model.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"top_p": 1.0},
)
```

**What this does:** Sets default inference parameters (`temperature` and `top_p`) that apply to all chat and completion calls made with this client. Lower temperature (0.0) produces more deterministic outputs; `top_p` controls diversity in sampling.

**References:**
- [Model Inference API Parameters](../../../ai-foundry/model-inference/reference/reference-model-inference-chat-completions.md)

For parameters not supported in the Model Inference API ([reference](../../../ai-foundry/model-inference/reference/reference-model-inference-chat-completions.md)) but available in the underlying model, use the `model_extras` argument. In the following example, the parameter `safe_prompt`, which is only available for Mistral models, is passed.

```python
llm = AzureAICompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    temperature=0.0,
    model_kwargs={"model_extras": {"safe_prompt": True}},
)
```

## Use LLM models

You can use the client directly or [configure the models used by your code](#configure-the-models-your-code-uses) in LlamaIndex. To use the model directly, use the `chat` method for chat instruction models:

```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(
        role="system", content="You are a pirate with colorful personality."
    ),
    ChatMessage(role="user", content="Hello"),
]

response = llm.chat(messages)
print(response)
```

You can stream the outputs, too:

```python
response = llm.stream_chat(messages)
for r in response:
    print(r.delta, end="")
```

The `complete` method is still available for models of type `chat-completions`. In those cases, your input text is converted to a message by using `role="user"`.

## Use embeddings models

Just like you create an LLM client, you can connect to an embeddings model. In the following example, set the environment variable to point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Then create the client:

```python
from llama_index.embeddings.azure_inference import AzureAIEmbeddingsModel

embed_model = AzureAIEmbeddingsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ['AZURE_INFERENCE_CREDENTIAL'],
    model="<your-model-name>",
)
```

**What this does:** Instantiates an embeddings client to convert text into vector embeddings. Embeddings are numerical representations of text used for semantic similarity searches and retrieval-augmented generation (RAG).

**References:**
- [LlamaIndex Embeddings Integration](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/)
- [AzureAIEmbeddingsModel](https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/embeddings/llama-index-embeddings-azure-inference/llama_index/embeddings/azure_inference/base.py)

The following example shows a simple test to verify it works:

```python
from llama_index.core.schema import TextNode

nodes = [
    TextNode(
        text="Before college the two main things I worked on, "
        "outside of school, were writing and programming."
    )
]
response = embed_model(nodes=nodes)
print(response[0].embedding)
```

**What this does:** Converts a text node into embeddings and prints the numerical vector representation. Expected output: A list of floating-point numbers representing the semantic meaning of the text (typical length: 384–1024 dimensions depending on the model).

**References:**
- [TextNode](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/)

## Configure the models your code uses

In your code, you can use the LLM or embeddings model client individually when working with LlamaIndex, or you can configure the entire session by using the `Settings` options. When you configure the session, all your code uses the same models for all operations.

```python
from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model
```

**What this does:** Registers the LLM and embeddings clients globally so all LlamaIndex operations automatically use these models without needing to pass them as parameters to each function.

**References:**
- [LlamaIndex Settings](https://docs.llamaindex.ai/en/stable/module_guides/models/llms/)

However, some scenarios require a general model for most operations and a specific model for a given task. In these cases, set the LLM or embedding model for each LlamaIndex construct. The following example shows how to set a specific model:

```python
from llama_index.core.evaluation import RelevancyEvaluator

relevancy_evaluator = RelevancyEvaluator(llm=llm)
```

**What this does:** Creates a relevancy evaluator that uses your custom LLM client for evaluating retrieval results. This allows you to use different models for different tasks (e.g., a specific model for evaluation vs. general chat).

**References:**
- [LlamaIndex Evaluators](https://docs.llamaindex.ai/en/stable/module_guides/)

Generally, use a combination of both strategies.

## Related content

* [How to get started with Azure AI SDKs](sdk-overview.md)
* [Reference for LlamaIndex Embeddings Integration](https://llamahub.ai/l/embeddings/llama-index-embeddings-azure-inference)
* [Reference for LlamaIndex LLMs Integration](https://llamahub.ai/l/llms/llama-index-llms-azure-inference)
