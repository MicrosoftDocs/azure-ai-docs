---
title: Develop applications with LangChain and Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to use LangChain with models deployed in Microsoft Foundry to build advanced, intelligent applications.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - update-code
ms.topic: how-to
ms.date: 09/09/2025
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
monikerRange: foundry-classic || foundry
ai-usage: ai-assisted
---

# Develop applications with LangChain and Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

LangChain is a developer ecosystem that makes it easier to build reasoning applications. It includes multiple components, and most of them can be used independently, allowing you to pick and choose the pieces you need.

::: moniker range="foundry-classic"
Models deployed to [!INCLUDE [classic-link](../../includes/classic-link.md)] can be used with LangChain in two ways:
::: moniker-end

::: moniker range="foundry"
Models deployed to [!INCLUDE [foundry-link](../../default/includes/foundry-link.md)] can be used with LangChain in two ways:
::: moniker-end

- **Use the Azure AI Model Inference API:** All models deployed in Microsoft Foundry support the [Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md), which offers a common set of capabilities across most models in the catalog. Because the API is consistent, switching models is as simple as changing the deployment; no code changes are required. With LangChain, install the `langchain-azure-ai` integration.

- **Use the model provider’s API:** Some models, such as OpenAI, Cohere, or Mistral, offer their own APIs and LangChain extensions. These extensions might include model-specific capabilities and are suitable if you need to use them. Install the extension for your chosen model, such as `langchain-openai` or `langchain-cohere`.

This tutorial shows how to use the `langchain-azure-ai` package with LangChain.

## Prerequisites

To run this tutorial, you need:

* [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

* A model deployment that supports the [Model Inference API](https://aka.ms/azureai/modelinference). This article uses a `Mistral-Large-2411` deployment available in the [Foundry model catalog](../../../ai-foundry/model-inference/overview.md).
* Python 3.9 or later installed, including pip.
* LangChain installed. You can install it with:

    ```bash
    pip install langchain
    ```

* Install the Foundry integration:

    ```bash
    pip install -U langchain-azure-ai
    ```

## Configure the environment

::: moniker range="foundry-classic"
[!INCLUDE [set-endpoint](../../includes/set-endpoint.md)]
::: moniker-end

::: moniker range="foundry"
[!INCLUDE [set-endpoint](../../default/includes/set-endpoint.md)]
::: moniker-end

After configuration, create a client to connect to the chat model using `init_chat_model`. For Azure OpenAI models, see [Use Azure OpenAI models](#use-azure-openai-models).

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

If you plan to use asynchronous calls, use the asynchronous version of the credentials:

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

If your endpoint serves a single model (for example, serverless API deployments), omit the `model` parameter:

```python
import os
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

## Use chat completion models

Use the model directly. `ChatModels` are instances of the LangChain `Runnable` interface, which provides a standard way to interact with them. To call the model, pass a list of messages to the `invoke` method.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=human_message)] 

Compose operations as needed in chains. Use a prompt template to translate sentences:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
```

This chain takes `language` and `text` inputs. Now, create an output parser:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_output_parser)]

Combine the template, model, and output parser using the pipe (`|`) operator:

```python
chain = prompt_template | model | parser
```

Invoke the chain by providing `language` and `text` values using the `invoke` method:

```python
chain.invoke({"language": "italian", "text": "hi"})
```

### Chain multiple LLMs together

Because models in Foundry expose a common Model Inference API, you can chain multiple LLM operations and choose the model best suited to each step.

In the following example, we create two model clients: one producer and one verifier. To make the distinction clear, we use a multi-model endpoint such as the [Model Inference API](../../model-inference/overview.md) and pass the `model` parameter to use `Mistral-Large` for generation and `Mistral-Small` for verification. Producing content generally requires a larger model, while verification can use a smaller one.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_producer_verifier)]


> [!TIP]
> Review the model card for each model to understand the best use cases.

The following example generates a poem written by an urban poet:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=generate_poem)]

Chain the pieces:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_chain)]

The previous chain returns only the output of the `verifier` step. To access the intermediate result generated by the `producer`, use a `RunnablePassthrough` to output that intermediate step.

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

generate_poem = producer_template | producer | parser
verify_poem = verifier_template | verifier | parser

chain = generate_poem | RunnableParallel(poem=RunnablePassthrough(), verification=RunnablePassthrough() | verify_poem)
```

Invoke the chain using the `invoke` method:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=invoke_chain)]


## Use embedding models

Create an embeddings client similarly. Set the environment variables to point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Create the client:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_embed_model_client)]

Use an in-memory vector store:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_vector_store)]


Add documents:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=add_documents)]


Search by similarity:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=search_similarity)]

## Use Azure OpenAI models

When using Azure OpenAI models with the `langchain-azure-ai` package, use the following endpoint format:

```python
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

llm = AzureAIChatCompletionsModel(
    endpoint="https://<resource>.openai.azure.com/openai/v1",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model="gpt-4o"
)
```

## Debugging and troubleshooting

If you need to debug your application and understand the requests sent to models in Foundry, use the integration’s debug capabilities:

First, configure logging to the desired level:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=configure_logging)]


To see request payloads, pass `logging_enable=True` in `client_kwargs` when instantiating the client:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_client_with_logging)]


Use the client as usual in your code.

## Tracing

Use tracing in Foundry by creating a tracer. Logs are stored in Azure Application Insights and can be queried at any time using Azure Monitor or the Foundry portal. Each AI hub has an associated Azure Application Insights instance.


### Get your instrumentation connection string

::: moniker range="foundry-classic"

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

You can configure your application to send telemetry to Azure Application Insights either by:

1. Using the connection string to Azure Application Insights directly:

    1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs) and select **Tracing**.

    2. Select **Manage data source**. In this screen you can see the instance that is associated with the project.

    3. Copy the value at **Connection string** and set it to the following variable:

        ```python
        import os
      
        application_insights_connection_string = "instrumentation...."
        ```

2. Using the Microsoft Foundry SDK and the Foundry Project endpoint:

    1. Ensure you have the package `azure-ai-projects` installed in your environment.

    2. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs).
    
    3. Copy your Foundry project endpoint URL and set it in the following code:

        ```python
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
        
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint="<your-foundry-project-endpoint-url>",
        )
        
        application_insights_connection_string = project_client.telemetry.get_application_insights_connection_string()
        ```
::: moniker-end
::: moniker range="foundry"

::: moniker-end

### Configure tracing for Foundry

The following code creates a tracer connected to the Azure Application Insights behind a Foundry project. The `enable_content_recording` parameter is set to `True`, which captures inputs and outputs across the application, including intermediate steps. This is helpful when debugging and building applications, but you might want to disable it in production environments. You can also control this via the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable:

```python
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

azure_tracer = AzureAIOpenTelemetryTracer(
    connection_string=application_insights_connection_string,
    enable_content_recording=True,
)
```

Pass the tracer via `config` in the `invoke` operation:

```python
chain.invoke({"topic": "living in a foreign country/region"}, config={"callbacks": [azure_tracer]})
```

To configure the chain itself for tracing, use the `.with_config()` method:

```python
chain = chain.with_config({"callbacks": [azure_tracer]})
```

Then use the `invoke()` method as usual:

```python
chain.invoke({"topic": "living in a foreign country"})
```

### View traces

To see traces:

::: moniker range="foundry-classic"
1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. Navigate to **Tracing** section.

3. Identify the trace you created. It may take a few seconds to appear.

    :::image type="content" source="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png" alt-text="A screenshot showing the trace of a chain." lightbox="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png":::

::: moniker-end

::: moniker range="foundry"
1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. Navigate to **Tracing** section.

1. Identify the trace you have created. It may take a couple of seconds for the trace to show.
::: moniker-end





Learn more about [how to visualize and manage traces](visualize-traces.md).

## Next steps

* [Develop applications with LlamaIndex](llama-index.md)
* [Visualize and manage traces in Foundry](visualize-traces.md)
* [Use Foundry Models](../../model-inference/overview.md)
* [Reference: Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md)
