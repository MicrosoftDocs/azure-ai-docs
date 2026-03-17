---
title: Use LangChain with models in Microsoft Foundry
description: Learn how to use OpenAI-compatible LangChain classes with models deployed in Microsoft Foundry.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/09/2026
ms.author: fasantia
author: santiagxf
ms.reviewer: sgilley
ms.custom:
  - dev-focus
  - classic-and-new
  - update-code-2
  - doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to use OpenAI-compatible LangChain classes with Foundry models so I can build chat, embedding, and chained workflows.
---

# Use LangChain with models in Microsoft Foundry

Use `langchain-azure-ai` to build LangChain apps that call models deployed
in Microsoft Foundry. Models with **OpenAI-compatible APIs** can be directly
used. In this article, you create
chat and embeddings clients, run prompt chains, and combine generation plus
verification patterns.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../create-projects.md).
- The **Azure AI User** role on the Foundry project.
- A deployed chat model that supports OpenAI-compatible APIs, such as
  `gpt-4.1` or `Mistral-Large-3`.
- A deployed embeddings model, such as `text-embedding-3-large`.
- Python 3.9 or later.

Install the required packages:

```bash
pip install -U langchain langchain-azure-ai azure-identity
```

> [!IMPORTANT]
> `langchain-azure-ai` uses the new Microsoft Foundry SDK (v2). If you are using Foundry classic or Foundry Hubs, use `langchain-azure-ai[v1]`,
> which uses Azure AI Inference SDK (legacy). [Learn more](../../../foundry-classic/how-to/develop/langchain.md).

## Configure the environment

Set one of the following connection patterns:

- Project endpoint with Microsoft Entra ID (recommended).
- Direct endpoint with an API key.

```python
import os

# Option 1: Project endpoint (recommended)
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)

# Option 2: Direct OpenAI-compatible endpoint + API key
os.environ["OPENAI_BASE_URL"] = (
	"https://<resource>.services.ai.azure.com/openai/v1"
)
os.environ["OPENAI_API_KEY"] = "<your-api-key>"
```

**What this snippet does:** Defines environment variables used by the
`langchain-azure-ai` model classes for project-based or direct endpoint access.


## Use chat models

You can easily instantiate a model by using `init_chat_model`:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("azure_ai:gpt-4.1")
```

All Foundry models supporting OpenAI-compatible APIs can be used with the client, but they need to be deployed to your Foundry resource first. Using `project_endpoint` (environment variable `AZURE_AI_PROJECT_ENDPOINT`) requires Microsoft Entra ID for authentication and the role **Azure AI User**.

**What this snippet does:** Creates a chat model client by using the
`init_chat_model` convenience method. The client routes to the specified model
through the Foundry project endpoint or direct endpoint configured in the environment.

**References:**
- [AzureAIOpenAIApiChatModel](https://python.langchain.com/api_reference/azure_ai/chat_models/langchain_azure_ai.chat_models.AzureAIOpenAIApiChatModel.html)

### Verify your setup

Run a simple model invocation:

```python
response = model.invoke("Say hello")
response.pretty_print()
```

```output
================================== Ai Message ==================================
Hello! 👋 How can I help you today?
```

**What this snippet does:** Sends a basic prompt to verify endpoint,
authentication, and model routing.

**References:**
- [LangChain runnable interface](https://python.langchain.com/docs/concepts/runnables/)


### Configurable models

You can also create a runtime-configurable model by specifying `configurable_fields`. If you don't specify a `model` value, then `model` will be configurable by default.

```python
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(
    model_provider="azure_ai", 
    temperature=0,
)


configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-nano
)
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "Mistral-Large-3"}}, # Run with Mistral Large
)
```

```output
================================== Ai Message ==================================

Hi! I'm ChatGPT, an AI assistant built by OpenAI. You can call me ChatGPT or just Assistant. How can I help you today?
================================== Ai Message ==================================

I don't have a name, but you can call me **Assistant** or anything you like! 😊 What can I help you with today?
```

**What this snippet does:** Creates a configurable model instance allowing to switch
models easily at invocation time. Because `model` parameter is missing in `init_chat_model`,
it's by default a *configurable field* and can be passed with `invoke()`. You can add other
fields to be configurable by configuring `configurable_fields`.

### Configure clients directly

You can also create a chat model client by using `AzureAIOpenAIApiChatModel` class.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

model = AzureAIOpenAIApiChatModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(), # pass your API key here
	model="Mistral-Large-3",
)
```

By default `AzureAIOpenAIApiChatModel` uses OpenAI Responses API. You can change this behavior by passing `use_responses_api=False`:

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

model = AzureAIOpenAIApiChatModel(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
    model="Mistral-Large-3",
    use_responses_api=False
)
```

### Run asynchronous calls

Use asynchronous credentials if your app calls models with `ainvoke`. When using Microsoft Entra ID for authentication, use 
the corresponding asynchronous implementation for credentials:

```python
import os

from azure.identity.aio import DefaultAzureCredential as DefaultAzureCredentialAsync
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

model = AzureAIOpenAIApiChatModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredentialAsync(),
	model="gpt-4.1",
)


async def main():
	response = await model.ainvoke("Say hello asynchronously")
	response.pretty_print()


import asyncio
asyncio.run(main())
```

> [!TIP]
> If you run this code in a Jupyter notebook, you can use `await main()` directly instead of `asyncio.run(main())`.

```output
================================== Ai Message ==================================
Hello! 👋 How can I help you today?
```

**What this snippet does:** Creates an async client and runs a non-blocking
request with `ainvoke`.

**References:**
- [Async credentials in Azure Identity](/python/api/overview/azure/identity-readme)
- [LangChain runnable interface](https://python.langchain.com/docs/concepts/runnables/)

## Reasoning 

Many models can perform multi-step reasoning to arrive at a conclusion. This involves breaking down complex problems into smaller, more manageable steps.

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("azure_ai:DeepSeek-R1-0528")

for chunk in model.stream("Why do parrots have colorful feathers?"):
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    print(reasoning_steps if reasoning_steps else chunk.text, end="")

print("\n")
```

```output
Parrots have colorful feathers primarily due to a combination of evolutionary ...
```

**References:**
- [LangChain streaming](https://python.langchain.com/docs/concepts/streaming/)

## Use Foundry models in agents

Use `create_agent` with models connected to Foundry to create React-like agent loops:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="azure_ai:gpt-5.2", 
    system_prompt="You're an informational agent. Answer questions cheerfully.", 
    tools=[]
)

response = agent.invoke({"messages": "what's your name?"})
response["messages"][-1].pretty_print()
```

```output
================================== Ai Message ==================================

I’m ChatGPT, your AI assistant.
```


## Use embedding models

You can easily instantiate a model by using `init_embeddings`:

```python
from langchain.embeddings import init_embeddings

embed_model = init_embeddings("azure_ai:text-embedding-3-small")
```

**What this snippet does:** Creates an embeddings model client by using the
`init_embeddings` convenience method.

All Foundry models supporting OpenAI-compatible APIs can be used with the client, but they need to be deployed to your Foundry resource first. Using `project_endpoint` (environment variable `AZURE_AI_PROJECT_ENDPOINT`) requires Microsoft Entra ID for authentication and the role **Azure AI User**.

Or create the embeddings client with `AzureAIOpenAIApiEmbeddingsModel`.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.embeddings import AzureAIOpenAIApiEmbeddingsModel

embed_model = AzureAIOpenAIApiEmbeddingsModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(),
	model="text-embedding-3-large",
)
```

For direct endpoint and API key authentication:

```python
import os

from langchain_azure_ai.embeddings import AzureAIOpenAIApiEmbeddingsModel

embed_model = AzureAIOpenAIApiEmbeddingsModel(
	endpoint=os.environ["OPENAI_BASE_URL"],
	credential=os.environ["OPENAI_API_KEY"],
	model="text-embedding-3-large",
)
```

**What this snippet does:** Configures embeddings generation for vector search,
retrieval, and ranking workflows.

**References:**
- [AzureAIOpenAIApiEmbeddingsModel](https://python.langchain.com/api_reference/azure_ai/embeddings/langchain_azure_ai.embeddings.AzureAIOpenAIApiEmbeddingsModel.html)


### Example: Run similarity search with a vector store

Use an in-memory vector store for local experimentation.

```python
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embed_model)

documents = [
	Document(id="1", page_content="foo", metadata={"baz": "bar"}),
	Document(id="2", page_content="thud", metadata={"bar": "baz"}),
]

vector_store.add_documents(documents=documents)

results = vector_store.similarity_search(query="thud", k=1)
for doc in results:
	print(f"* {doc.page_content} [{doc.metadata}]")
```

```output
* thud [{'bar': 'baz'}]
```

**What this snippet does:** Adds sample documents to a vector store and returns
the most similar document for a query.

**References:**
- [LangChain vector stores](https://python.langchain.com/docs/concepts/vectorstores/)

## Debug requests with logging

Enable `langchain_azure_ai` debug logging to inspect request flow.

```python
import logging
import sys

logger = logging.getLogger("langchain_azure_ai")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
	"%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

**What this snippet does:** Configures Python logging to emit detailed SDK logs
that help troubleshoot endpoint or payload issues.

**References:**
- [Python logging](https://docs.python.org/3/library/logging.html)

## Environment variables reference

You can configure the following environment variables. Those values can also be configured when constructing the objects:

| Variable | Role | Example | Parameter in constructor |
|----------|------|---------|--------------------------|
| `AZURE_AI_PROJECT_ENDPOINT` | Foundry project endpoint. Use of the project endpoint requires Microsoft Entra ID authentication (recommended). | `https://contoso.services.ai.azure.com/api/projects/my-project` | `project_endpoint` |
| `AZURE_OPENAI_ENDPOINT` | Root for OpenAI resources.  | `https://contoso.openai.azure.com` | None. |
| `OPENAI_BASE_URL` | Direct OpenAI-compatible endpoint used for model calls. | `https://contoso.services.ai.azure.com/openai/v1` | `endpoint` |
| `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY` | API key used with `OPENAI_BASE_URL` or `AZURE_OPENAI_ENDPOINT` for key-based authentication. | `<your-api-key>` | `credential` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model's deployment name in the Foundry or OpenAI resource. Check the name in the Foundry portal as deployment names can be different from the underlying model used. Any model supporting OpenAI-compatible APIs can be used, however, not all the parameters may be supported. | `Mistral-Large-3` | `model` |
| `AZURE_OPENAI_API_VERSION` | The API version to use. When an `api_version` is available we construct the OpenAI clients and inject the `api-version` query parameter via `default_query`. | `v1` or `preview` | `api_version` |

> [!IMPORTANT]
> Environment variables `AZURE_AI_INFERENCE_ENDPOINT` and `AZURE_AI_CREDENTIALS` used for `AzureAIChatCompletionsModel` or `AzureAIEmbeddingsModel` (legacy) are no longer used.

## Next step

> [!div class="nextstepaction"]
> [Use Foundry Agent Service with LangGraph](langchain-agents.md)

## Related content

- [Foundry models overview](../../concepts/foundry-models-overview.md)
- [Microsoft Foundry SDK overview](sdk-overview.md)
- [Use LangChain with memory in Foundry](langchain-memory.md)
- [Use LangChain with Foundry Agent Service](langchain-agents.md)
