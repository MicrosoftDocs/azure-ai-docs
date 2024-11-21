---
title: Develop application with LangChain and Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article explains how to use LangChain with models deployed in Azure AI Foundry portal to build advance intelligent applications.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 11/04/2024
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
---

# Develop applications with LangChain and Azure AI Foundry

LangChain is a development ecosystem that makes as easy possible for developers to build applications that reason. The ecosystem is composed by multiple components. Most of the them can be used by themselves, allowing you to pick and choose whichever components you like best.

Models deployed to Azure AI Foundry can be used with LangChain in two ways:

- **Using the Azure AI model inference API:** All models deployed to Azure AI Foundry support the [Azure AI model inference API](../../reference/reference-model-inference-api.md), which offers a common set of functionalities that can be used for most of the models in the catalog. The benefit of this API is that, since it's the same for all the models, changing from one to another is as simple as changing the model deployment being use. No further changes are required in the code. When working with LangChain, install the extensions `langchain-azure-ai`.

- **Using the model's provider specific API:** Some models, like OpenAI, Cohere, or Mistral, offer their own set of APIs and extensions for LlamaIndex. Those extensions may include specific functionalities that the model support and hence are suitable if you want to exploit them. When working with LangChain, install the extension specific for the model you want to use, like `langchain-openai` or `langchain-cohere`.

In this tutorial, you learn how to use the packages `langchain-azure-ai` to build applications with LangChain.

## Prerequisites

To run this tutorial, you need:

* An [Azure subscription](https://azure.microsoft.com).
* An Azure AI project as explained at [Create a project in Azure AI Foundry portal](../create-projects.md).
* A model supporting the [Azure AI model inference API](https://aka.ms/azureai/modelinference) deployed. In this example, we use a `Mistral-Large` deployment, but use any model of your preference. 

    * You can follow the instructions at [Deploy models as serverless APIs](../deploy-models-serverless.md).

* Python 3.8 or later installed, including pip.
* LangChain installed. You can do it with:

    ```bash
    pip install langchain-core
    ```

* In this example, we are working with the Azure AI model inference API, hence we install the following packages:

    ```bash
    pip install -U langchain-azure-ai
    ```

## Configure the environment

To use LLMs deployed in Azure AI Foundry portal, you need the endpoint and credentials to connect to it. Follow these steps to get the information you need from the model you want to use:

1. Go to the [Azure AI Foundry](https://ai.azure.com/).
1. Open the project where the model is deployed, if it isn't already open.
1. Go to **Models + endpoints** and select the model you deployed as indicated in the prerequisites.
1. Copy the endpoint URL and the key.

    :::image type="content" source="../../media/how-to/inference/serverless-endpoint-url-keys.png" alt-text="Screenshot of the option to copy endpoint URI and keys from an endpoint." lightbox="../../media/how-to/inference/serverless-endpoint-url-keys.png":::
    
    > [!TIP]
    > If your model was deployed with Microsoft Entra ID support, you don't need a key.

In this scenario, we placed both the endpoint URL and key in the following environment variables:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Once configured, create a client to connect to the endpoint. In this case, we are working with a chat completions model hence we import the class `AzureAIChatCompletionsModel`.

```python
import os
from langchain_azure_ai import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

> [!TIP]
> For Azure OpenAI models, configure the client as indicated at [Using Azure OpenAI models](#using-azure-openai-models).

If your endpoint is serving more than one model, like with the [Azure AI model inference service](../../ai-services/model-inference.md) or [GitHub Models](https://github.com/marketplace/models), you have to indicate `model_name` parameter:

```python
import os
from langchain_azure_ai import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="mistral-large-2407",
)
```

Alternatively, if your endpoint support Microsoft Entra ID, you can use the following code to create the client:

```python
import os
from azure.identity import DefaultAzureCredential
from langchain_azure_ai import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

If you are planning to use asynchronous calling, it's a best practice to use the asynchronous version for the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)
from langchain_azure_ai import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
)
```

## Use chat completions models

Let's first use the model directly. `ChatModels` are instances of LangChain `Runnable`, which means they expose a standard interface for interacting with them. To simply call the model, we can pass in a list of messages to the `invoke` method.

```python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

model.invoke(messages)
```

You can also compose operations as needed in what's called **chains**. Let's now use a prompt template to translate sentences:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
```

As you can see from the prompt template, this chain has a `language` and `text` input. Now, let's create an output parser:

```python
parser = StrOutputParser()
```

We can now combine the template, model, and the output parser from above using the pipe (`|`) operator:

```python
chain = prompt_template | model | parser
```

To invoke the chain, identify the inputs required and provide values using the `invoke` method:

```python
chain.invoke({"language": "italian", "text": "hi"})
```

```output
'ciao'
```

### Chaining multiple LLMs together

Models deployed to Azure AI Foundry support the Azure AI model inference API, which is standard across all the models. Chain multiple LLM operations based on the capabilities of each model so you can optimize for the right model based on capabilities. 

In the following example, we create 2 model clients, one is a producer and another one is a verifier. To make the distinction clear, we are using a multi-model endpoint like the [Azure AI model inference service](../../ai-services/model-inference.md) and hence we are passing the parameter `model_name` to use a `Mistral-Large` and a `Mistral-Small` model, quoting the fact that **producing content is more complex than verifying it**.

```python
producer = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="mistral-large-2407",
)

verifier = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="mistral-small",
)
```

The following example generates a poem written by an urban poet:

```python
producer_template = PromptTemplate(
    template="You are an urban poet, your job is to come up \
             verses based on a given topic.\n\
             Here is the topic you have been asked to generate a verse on:\n\
             {topic}",
    input_variables=["topic"]
)

verifier_template = PromptTemplate(
    template="You are a verifier of poems, you are tasked\
              to inspect the verses of poem. If they consist of violence and abusive language\
              report it. Your response should be only one word either True or False.\n \
              Here is the lyrics submitted to you:\n\
              {input}",
    input_variables=["input"]
)
```

Now let's chain the pieces:

```python
chain = producer_template | producer | parser | verifier_template | verifier
```

To invoke the chain, identify the inputs required and provide values using the `invoke` method:

```python
chain.invoke({"topic": "living in a foreign country"})
```

> [!TIP]
> Explore the model card of each of the models to understand the best use cases for each model.


## Use embeddings models

In the same way, you create an LLM client, you can connect to an embeddings model. In the following example, we are setting the environment variable to now point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Then create the client:

```python
from langchain_azure_ai.embeddings import AzureAIEmbeddingsModel

embed_model = AzureAIEmbeddingsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ['AZURE_INFERENCE_CREDENTIAL'],
)
```

The following example shows a simple example using a vector store in memory:

```python
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embed_model)
```

Let's add some documents:

```python
from langchain_core.documents import Document

document_1 = Document(id="1", page_content="foo", metadata={"baz": "bar"})
document_2 = Document(id="2", page_content="thud", metadata={"bar": "baz"})

documents = [document_1, document_2]
vector_store.add_documents(documents=documents)
```

Let's search by similarity:

```python
results = vector_store.similarity_search(query="thud",k=1)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
```

## Using Azure OpenAI models

If you are using Azure OpenAI service or Azure AI model inference service with OpenAI models with `langchain-azure-ai` package, you may need to use `api_version` parameter to select a specific API version. The following example shows how to connect to an Azure OpenAI model deployment in Azure OpenAI service:

```python
from langchain_azure_ai import AzureAIChatCompletionsModel

llm = AzureAIChatCompletionsModel(
    endpoint="https://<resource>.openai.azure.com/openai/deployments/<deployment-name>",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    api_version="2024-05-01-preview",
)
```

> [!IMPORTANT]
> Check which is the API version that your deployment is using. Using a wrong `api_version` or one not supported by the model results in a `ResourceNotFound` exception.

If the deployment is hosted in Azure AI Services, you can use the Azure AI model inference service:

```python
from langchain_azure_ai import AzureAIChatCompletionsModel

llm = AzureAIChatCompletionsModel(
    endpoint="https://<resource>.services.ai.azure.com/models",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model_name="<model-name>",
    api_version="2024-05-01-preview",
)
```

## Next steps

* [Develop applications with LlamaIndex](llama-index.md)
* [Use the Azure AI model inference service](../../ai-services/model-inference.md)
* [Reference: Azure AI model inference API](../../reference/reference-model-inference-api.md)












