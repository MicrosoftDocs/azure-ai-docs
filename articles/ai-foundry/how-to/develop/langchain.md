---
title: Develop applications with LangChain and Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to use LangChain with models deployed in Microsoft Foundry to build advanced, intelligent applications.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - update-code-2
  - dev-focus
ms.topic: how-to
ms.date: 12/29/2025
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
---

# Develop applications with LangChain and Microsoft Foundry

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

LangChain is a developer ecosystem that makes it easier to build reasoning applications. It includes multiple components, and most of them can be used independently, so you can pick and choose the pieces you need.

<!-- ::: moniker range="foundry-classic" -->
You can use models deployed to [!INCLUDE [classic-link](../../includes/classic-link.md)] with LangChain in two ways:
<!-- ::: moniker-end

::: moniker range="foundry"
You can use models deployed to [!INCLUDE [foundry-link](../../default/includes/foundry-link.md)] with LangChain in two ways:
::: moniker-end -->

- **Use the model provider's API:** Some models, such as OpenAI, Cohere, or Mistral, offer their own APIs and LangChain extensions. These extensions might include model-specific capabilities and are suitable if you need to use them. Install the extension for your chosen model, such as `langchain-openai` or `langchain-cohere`.

- **Use the Azure AI Model Inference API:** All models deployed in Microsoft Foundry support the [Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md), which offers a common set of capabilities across most models in the catalog. Because the API is consistent, switching models is as simple as changing the deployment; no code changes are required. For LangChain, also install the `langchain-azure-ai` integration.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]


This tutorial shows how to use the `langchain-azure-ai` package with LangChain.

## Prerequisites

To run this tutorial, you need:

* [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]

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

* A model deployment that supports the [Model Inference API](https://aka.ms/azureai/modelinference). This article uses `Mistral-Large-3`.

* Python 3.9 or later installed, including pip.
* LangChain installed. You can install it by using the following command:

    ```bash
    pip install langchain
    ```

* Install the Foundry integration:

    ```bash
    pip install -U langchain-azure-ai
    ```



## Configure the environment

<!-- ::: moniker range="foundry-classic" -->
[!INCLUDE [set-endpoint](../../includes/set-endpoint.md)]
<!-- ::: moniker-end -->

<!-- ::: moniker range="foundry"
[!INCLUDE [set-endpoint](../../default/includes/set-endpoint.md)]
::: moniker-end -->


Create a client to connect to the chat model by using the `AzureAIChatCompletionsModel` class.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_client)]

**What this snippet does:** Instantiates an `AzureAIChatCompletionsModel` client configured to connect to your deployed model using an API key for authentication. This client acts as an interface to the Model Inference API.

**References:**
- [LangChain Azure AI integration](https://python.langchain.com/docs/integrations/chat/azure_ai)
- [Model Inference API overview](../../../ai-foundry/model-inference/overview.md)


> [!CAUTION]
> **Breaking change:** The `model_name` parameter is renamed to `model` in version `0.1.3`.

If your endpoint supports Microsoft Entra ID, use the following code to create the client:

```python
import os
from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="Mistral-Large-3",
)
```

> [!NOTE]
> When using Microsoft Entra ID, make sure that the endpoint is deployed with that authentication method and that you have the required permissions to invoke it.

If you plan to use asynchronous calls, use the asynchronous version of the credentials:

```python
from azure.identity.aio import (
    DefaultAzureCredential as DefaultAzureCredentialAsync,
)
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=DefaultAzureCredentialAsync(),
    model="Mistral-Large-3",
)
```

If your endpoint serves a single model (for example, serverless API deployments), don't include the `model` parameter:

```python
import os
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)
```

### Verify your setup

Test your client connection with a simple invocation:

```python
response = model.invoke("Say hello")
print(response.content)
```

**What this does:** Calls the model with a simple prompt to verify authentication and connectivity. Expected output: A greeting message from the model (for example, "Hello! How can I assist you today?").

**References:**
- [LangChain Runnable interface](https://python.langchain.com/docs/concepts/runnable)

## Use chat completion models

Use the model directly. `ChatModels` are instances of the LangChain `Runnable` interface, which provides a standard way to interact with them. To call the model, pass a list of messages to the `invoke` method.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=human_message)]

**What this snippet does:** Demonstrates how to pass a list of `HumanMessage` and `SystemMessage` objects to the model's `invoke()` method to generate a response.

**References:**
- [LangChain Messages](https://python.langchain.com/docs/concepts/messages)
- [LangChain Runnable interface](https://python.langchain.com/docs/concepts/runnable)

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

**What this snippet does:** Creates a `StrOutputParser` that converts the model's output into a string format, stripping any extra metadata.

**References:**
- [LangChain Output Parsers](https://python.langchain.com/docs/concepts/output_parsers)

Combine the template, model, and output parser by using the pipe (`|`) operator:

```python
chain = prompt_template | model | parser
```

Invoke the chain by providing `language` and `text` values by using the `invoke` method:

```python
chain.invoke({"language": "italian", "text": "hi"})
```

### Chain multiple LLMs together

Because models in Foundry expose a common Model Inference API, you can chain multiple LLM operations and choose the model best suited to each step.

In the following example, you create two model clients: one producer and one verifier. To make the distinction clear, use a multi-model endpoint such as the [Model Inference API](../../foundry-models/concepts/models-sold-directly-by-azure.md) and pass the `model` parameter to a large model for generation and a small model for verification. Producing content generally requires a larger model, while verification can use a smaller one.

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_producer_verifier)]

**What this snippet does:** Instantiates two separate `AzureAIChatCompletionsModel` clients: one using `Mistral-Large-3` for content generation and another using `Mistral-Small` for verification, demonstrating how to choose different models for different tasks.

**References:**
- [LangChain Azure AI integration](https://python.langchain.com/docs/integrations/chat/azure_ai)


> [!TIP]
> Review the model card for each model to understand the best use cases.

The following example generates a poem written by an urban poet:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=generate_poem)]

**What this snippet does:** Creates a prompt template and chains it with the `producer` model client to generate creative content (a poem in this case).

Chain the pieces:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_chain)]

**What this snippet does:** Chains the generated poem through the `verifier` model to validate or review the generated content, demonstrating a producer-verifier workflow.

The previous chain returns only the output of the `verifier` step. To access the intermediate result generated by the `producer`, use a `RunnablePassthrough` to output that intermediate step.

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

generate_poem = producer_template | producer | parser
verify_poem = verifier_template | verifier | parser

chain = generate_poem | RunnableParallel(poem=RunnablePassthrough(), verification=RunnablePassthrough() | verify_poem)
```

Invoke the chain by using the `invoke` method:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=invoke_chain)]

**What this snippet does:** Calls the complete producer-verifier chain with a topic input, returning both the generated content and the verification result. Expected output: A JSON object containing `poem` and `verification` keys with the generated poem and verification response.

**References:**
- [LangChain Runnables](https://python.langchain.com/docs/concepts/runnable)


## Use embedding models

Create an embeddings client in a similar way. Set the environment variables to point to an embeddings model:

```bash
export AZURE_INFERENCE_ENDPOINT="<your-model-endpoint-goes-here>"
export AZURE_INFERENCE_CREDENTIAL="<your-key-goes-here>"
```

Create the client:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_embed_model_client)]

**What this snippet does:** Instantiates an embeddings client using `AzureAIEmbeddingsModel` to convert text into vector embeddings, which can be used for semantic search and similarity comparisons.

**References:**
- [LangChain Embeddings](https://python.langchain.com/docs/integrations/text_embedding/azure_ai)

Use an in-memory vector store:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=create_vector_store)]

**What this snippet does:** Creates an in-memory vector store (InMemoryVectorStore) that stores embeddings for fast similarity search operations.

**References:**
- [LangChain Vector Stores](https://python.langchain.com/docs/concepts/vectorstores)


Add documents:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=add_documents)]

**What this snippet does:** Converts documents into embeddings using the embeddings client and adds them to the vector store for later retrieval.

**References:**
- [LangChain Vector Stores](https://python.langchain.com/docs/concepts/vectorstores)


Search by similarity:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-embeddings.ipynb?name=search_similarity)]

**What this snippet does:** Performs a semantic search against the vector store, returning documents most similar to the query based on embedding similarity. Expected output: List of relevant documents ranked by similarity score.

## Use Azure OpenAI models

When you use Azure OpenAI models with the `langchain-azure-ai` package, use the following endpoint format:

```python
import os
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

llm = AzureAIChatCompletionsModel(
    endpoint="https://<resource>.openai.azure.com/openai/v1",
    credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
    model="gpt-4o"
)
```

**What this snippet does:** Instantiates a client configured specifically for Azure OpenAI models using the Azure OpenAI endpoint format. The `endpoint` parameter points to your Azure OpenAI resource, and the `credential` uses the API key stored in the environment variable.

**References:**
- [LangChain Azure AI integration](https://python.langchain.com/docs/integrations/chat/azure_ai)

## Debugging and troubleshooting

If you need to debug your application and understand the requests sent to models in Foundry, use the integration's debug capabilities:

First, configure logging to the desired level:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=configure_logging)]

**What this snippet does:** Sets up Python logging at the DEBUG level to capture detailed information about HTTP requests and responses between LangChain and the Model Inference API.

**References:**
- [Python logging module](https://docs.python.org/3/library/logging.html)


To see request payloads, pass `logging_enable=True` in `client_kwargs` when instantiating the client:

[!notebook-python[](~/azureai-samples-main/scenarios/langchain/getting-started-with-langchain-chat-models.ipynb?name=create_client_with_logging)]

**What this snippet does:** Creates a client with logging enabled to capture and display detailed request/response payloads, helpful for debugging API interactions.


Use the client as usual in your code.

## Tracing

Use tracing in Foundry by creating a tracer. Logs are stored in Azure Application Insights and can be queried at any time using Azure Monitor or the Foundry portal. Each AI hub has an associated Azure Application Insights instance.


### Get your instrumentation connection string

<!-- ::: moniker range="foundry-classic" -->

[!INCLUDE [tip-left-pane](../../includes/tip-left-pane.md)]

You can configure your application to send telemetry to Azure Application Insights by using either of the following methods:

1. Use the connection string to Azure Application Insights directly:

    1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs) and select **Tracing**.

    1. Select **Manage data source**. In this screen, you can see the instance that is associated with the project.

    1. Copy the value at **Connection string** and set it to the following variable:

        ```python
        import os
      
        application_insights_connection_string = "instrumentation...."
        ```

1. Use the Microsoft Foundry SDK and the Foundry Project endpoint:

    1. Ensure you have the package `azure-ai-projects` installed in your environment.

    1. Go to [Foundry portal](https://ai.azure.com/?cid=learnDocs).
    
    1. Copy your Foundry project endpoint URL and set it in the following code:

        ```python
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
        
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint="<your-foundry-project-endpoint-url>",
        )
        
        application_insights_connection_string = project_client.telemetry.get_application_insights_connection_string()
        ```
<!-- ::: moniker-end
::: moniker range="foundry"

::: moniker-end -->

### Configure tracing for Foundry

The following code creates a tracer connected to the Azure Application Insights behind a Foundry project. The `enable_content_recording` parameter is set to `True`, which captures inputs and outputs across the application, including intermediate steps. This feature is helpful when debugging and building applications, but you might want to disable it in production environments. You can also control this feature by using the `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED` environment variable:

```python
from langchain_azure_ai.callbacks.tracers import AzureAIOpenTelemetryTracer

azure_tracer = AzureAIOpenTelemetryTracer(
    connection_string=application_insights_connection_string,
    enable_content_recording=True,
)
```

Pass the tracer through `config` in the `invoke` operation:

```python
chain.invoke({"topic": "living in a foreign country/region"}, config={"callbacks": [azure_tracer]})
```

To configure the chain itself for tracing, use the `.with_config()` method:

```python
chain = chain.with_config({"callbacks": [azure_tracer]})
```

Then use the `invoke()` method as usual:

```python
chain.invoke({"topic": "living in a foreign country/region"})
```

### View traces

To see traces:

<!-- ::: moniker range="foundry-classic" -->
1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]

1. Go to the **Tracing** section.

1. Find the trace you created. It might take a few seconds to appear.

    :::image type="content" source="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png" alt-text="A screenshot showing the trace of a chain." lightbox="../../media/how-to/develop-langchain/langchain-portal-tracing-example.png":::

<!-- ::: moniker-end

::: moniker range="foundry"
1. [!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

1. Go to the **Tracing** section.

1. Find the trace you created. It might take a couple of seconds for the trace to show.
::: moniker-end -->





Learn more about [how to visualize and manage traces](./trace-application.md).

## Next steps

* [Develop applications with LlamaIndex](llama-index.md)
* [Visualize and manage traces in Foundry](./trace-application.md)
* [Use Foundry Models](../../foundry-models/concepts/models-sold-directly-by-azure.md)
* [Reference: Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md)
