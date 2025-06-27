---
title: Develop application with LangChain and Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article explains how to use LangChain with models deployed in Azure AI Foundry portal to build advance intelligent applications.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 06/26/2025
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
---

# Develop applications with LangChain and Azure AI Foundry

LangChain is a development ecosystem that makes as easy possible for developers to build applications that reason. The ecosystem is composed by multiple components. Most of the them can be used by themselves, allowing you to pick and choose whichever components you like best.

Models deployed to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) can be used with LangChain in two ways:

- **Using the Azure AI Model Inference API:** All models deployed to Azure AI Foundry support the [Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md), which offers a common set of functionalities that can be used for most of the models in the catalog. The benefit of this API is that, since it's the same for all the models, changing from one to another is as simple as changing the model deployment being use. No further changes are required in the code. When working with LangChain, install the extensions `langchain-azure-ai`.

- **Using the model's provider specific API:** Some models, like OpenAI, Cohere, or Mistral, offer their own set of APIs and extensions for LangChain. Those extensions might include specific functionalities that the model support and hence are suitable if you want to exploit them. When working with LangChain, install the extension specific for the model you want to use, like `langchain-openai` or `langchain-cohere`.

In this tutorial, you learn how to use the packages `langchain-azure-ai` to build applications with LangChain.

## Prerequisites

To run this tutorial, you need:

* An [Azure subscription](https://azure.microsoft.com).

* A model deployment supporting the [Model Inference API](https://aka.ms/azureai/modelinference) deployed. In this example, we use a `Mistral-Large-2411` deployment in the [Foundry Models](../../../ai-foundry/model-inference/overview.md).
* Python 3.9 or later installed, including pip.
* LangChain installed. You can do it with:

    ```bash
    pip install langchain
    ```

* In this example, we're working with the Model Inference API, hence we install the following packages:

    ```bash
    pip install -U langchain-azure-ai
    ```

## Configure the environment

[!INCLUDE [set-endpoint](../../includes/set-endpoint.md)]

Once configured, create a client to connect with the chat model by using the `init_chat_model`. For Azure OpenAI models, configure the client as indicated at [Using Azure OpenAI models](#using-azure-openai-models).

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(model="Mistral-Large-2411", model_provider="azure_ai")
```

You can also use the class `AzureAIChatCompletionsModel` directly.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_client)]


> [!CAUTION]
> **Breaking change:** Parameter `model_name` was renamed `model` in version `0.1.3`.

You can use the following code to create the client if your endpoint supports Microsoft Entra ID:

```python
import os
from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="Mistral-Large-2411",
)
```

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint was deployed with that authentication method and that you have the required permissions to invoke it.

If you're planning to use asynchronous calling, it's a best practice to use the asynchronous version for the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
    model="Mistral-Large-2411",
)
```

If your endpoint is serving one model, like with the serverless API deployment, you don't have to indicate `model` parameter:

```python
import os
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

## Use chat completions models

Let's first use the model directly. `ChatModels` are instances of LangChain `Runnable`, which means they expose a standard interface for interacting with them. To call the model, we can pass in a list of messages to the `invoke` method.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=human_message)] 

You can also compose operations as needed in **chains**. Let's now use a prompt template to translate sentences:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
```

As you can see from the prompt template, this chain has a `language` and `text` input. Now, let's create an output parser:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_output_parser)]

We can now combine the template, model, and the output parser from above using the pipe (`|`) operator:

```python
chain = prompt_template | model | parser
```

To invoke the chain, identify the inputs required and provide values using the `invoke` method:

```python
chain.invoke({"language": "italian", "text": "hi"})
```

### Chaining multiple LLMs together

Models deployed to Azure AI Foundry support the Model Inference API, which is standard across all the models. Chain multiple LLM operations based on the capabilities of each model so you can optimize for the right model based on capabilities. 

In the following example, we create two model clients. One is a producer and another one is a verifier. To make the distinction clear, we're using a multi-model endpoint like the [Foundry Models API](../../model-inference/overview.md) and hence we're passing the parameter `model` to use a `Mistral-Large` and a `Mistral-Small` model, quoting the fact that **producing content is more complex than verifying it**.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_producer_verifier)]


> [!TIP]
> Explore the model card of each of the models to understand the best use cases for each model.

The following example generates a poem written by an urban poet:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=generate_poem)]

Now let's chain the pieces:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_chain)]

The previous chain returns the output of the step `verifier` only. Since we want to access the intermediate result generated by the `producer`, in LangChain you need to use a `RunnablePassthrough` object to also output that intermediate step. 

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

generate_poem = producer_template | producer | parser
verify_poem = verifier_template | verifier | parser

chain = generate_poem | RunnableParallel(poem=RunnablePassthrough(), verification=RunnablePassthrough() | verify_poem)
```

To invoke the chain, identify the inputs required and provide values using the `invoke` method:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=invoke_chain)]


## Use embeddings models

In the same way, you create an LLM client, you can connect to an embeddings model. In the following example, we're setting the environment variable to now point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Then create the client:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_embed_model_client)]

The following example shows a simple example using a vector store in memory:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_vector_store)]


Let's add some documents:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=add_documents)]


Let's search by similarity:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=search_similarity)]

## Using Azure OpenAI models

If you're using Azure OpenAI models with `langchain-azure-ai` package, use the following URL:

```python
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

llm = AzureAIChatCompletionsModel(
    endpoint="https://<resource>.openai.azure.com/openai/v1",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model="gpt-4o"
)
```

## Debugging and troubleshooting

If you need to debug your application and understand the requests sent to the models in Azure AI Foundry, you can use the debug capabilities of the integration as follows:

First, configure logging to the level you are interested in:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=configure_logging)]


To see the payloads of the requests, when instantiating the client, pass the argument `logging_enable`=`True` to the `client_kwargs`:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_client_with_logging)]


Use the client as usual in your code.

## Tracing

You can use the tracing capabilities in Azure AI Foundry by creating a tracer. Logs are stored in Azure Application Insights and can be queried at any time using Azure Monitor or Azure AI Foundry portal. Each AI Hub has an Azure Application Insights associated with it.

### Get your instrumentation connection string

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

You can configure your application to send telemetry to Azure Application Insights either by:

1. Using the connection string to Azure Application Insights directly:

    1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and select **Tracing**.

    2. Select **Manage data source**. In this screen you can see the instance that is associated with the project.

    3. Copy the value at **Connection string** and set it to the following variable:

        ```python
        import os
      
        application_insights_connection_string = "instrumentation...."
        ```

2. Using the Azure AI Foundry SDK and the project connection string (**[!INCLUDE [hub-project-name](../../includes/hub-project-name.md)]s only**).

    1. Ensure you have the package `azure-ai-projects` installed in your environment.

    2. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).
    
    3. Copy your project's connection string and set it the following code:

        ```python
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
        
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str="<your-project-connection-string>",
        )
        
        application_insights_connection_string = project_client.telemetry.get_connection_string()
        ```

### Configure tracing for Azure AI Foundry

The following code creates a tracer connected to the Azure Application Insights behind a project in Azure AI Foundry. Notice that the parameter `enable_content_recording` is set to `True`. This enables the capture of the inputs and outputs of the entire application as well as the intermediate steps. Such is helpful when debugging and building applications, but you might want to disable it on production environments. It defaults to the environment variable `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED`:

```python
from langchain_azure_ai.callbacks.tracers import AzureAIInferenceTracer

tracer = AzureAIInferenceTracer(
    connection_string=application_insights_connection_string,
    enable_content_recording=True,
)
```

To configure tracing with your chain, indicate the value config in the `invoke` operation as a callback:

```python
chain.invoke({"topic": "living in a foreign country"}, config={"callbacks": [tracer]})
```

To configure the chain itself for tracing, use the `.with_config()` method:

```python
chain = chain.with_config({"callbacks": [tracer]})
```

Then use the `invoke()` method as usual:

```python
chain.invoke({"topic": "living in a foreign country"})
```

### View traces

To see traces:

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

2. Navigate to **Tracing** section.

3. Identify the trace you have created. It may take a couple of seconds for the trace to show.

    :::image type="content" source="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png" alt-text="A screenshot showing the trace of a chain." lightbox="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png":::

Learn more about [how to visualize and manage traces](visualize-traces.md).

## Next steps

* [Develop applications with LlamaIndex](llama-index.md)
* [Visualize and manage traces in Azure AI Foundry](visualize-traces.md)
* [Use Azure AI Foundry Models](../../model-inference/overview.md)
* [Reference: Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md)
