---
title: Develop applications with LangChain and models in Microsoft Foundry
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
ai-usage: ai-assisted
# customer intent: As a developer, I want to use OpenAI-compatible LangChain classes with Foundry models so I can build chat, embedding, and chained workflows.
---

# Develop applications with LangChain and models in Microsoft Foundry

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

## Configure the environment

Set one of the following connection patterns:

1. Project endpoint with Microsoft Entra ID (recommended).
1. Direct endpoint with an API key.

```python
import os

# Option 1: Project endpoint (recommended)
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)

# Option 2: Direct OpenAI-compatible endpoint + API key
os.environ["AZURE_OPENAI_ENDPOINT"] = (
	"https://<resource>.services.ai.azure.com/openai/v1"
)
os.environ["AZURE_OPENAI_API_KEY"] = "<your-api-key>"
```

**What this snippet does:** Defines environment variables used by the
`langchain-azure-ai` model classes for project-based or direct endpoint access.

You can configure the following environment variables. Those values can also be configured when constructing the objects:

| Variable | Role | Example | Parameter in constructor |
|----------|------|---------|--------------------------|
| `AZURE_AI_PROJECT_ENDPOINT` | Foundry project endpoint. Use of the project endpoint requires Microsoft Entra ID authentication (recommended). | `https://contoso.services.ai.azure.com/api/projects/my-project` | `project_endpoint` |
| `AZURE_AI_OPENAI_ENDPOINT` | Direct OpenAI-compatible endpoint used for model calls. | `https://contoso.services.ai.azure.com/openai/v1` | `endpoint` |
| `AZURE_OPENAI_ENDPOINT` | Root for OpenAI resources.  | `https://contoso.openai.azure.com` | None. |
| `AZURE_OPENAI_API_KEY` | API key used with `AZURE_OPENAI_ENDPOINT` for key-based authentication. | `<your-api-key>` | `credential` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Deployment name in the Foundry or OpenAI resource. Any model supporting OpenAI-compatible APIs can be used, however, not all the parameters may be supported. | `Mistral-Large-3` | `model` |
| `AZURE_OPENAI_API_VERSION` | The API version to use. When an `api_version` is available we construct the OpenAI clients and inject the `api-version` query parameter via `default_query`. | `v1` or `preview` | `api_version` |

> [!IMPORTANT]
> Environment variables `AZURE_AI_INFERENCE_ENDPOINT` and `AZURE_AI_CREDENTIALS` used for `AzureAIChatCompletionsModel` or `AzureAIEmbeddingsModel` (legacy) are not longer used.

**References:**
- [AzureAIOpenAIApiChatModel](https://python.langchain.com/api_reference/azure_ai/chat_models/langchain_azure_ai.chat_models.AzureAIOpenAIApiChatModel.html)
- [AzureAIOpenAIApiEmbeddingsModel](https://python.langchain.com/api_reference/azure_ai/embeddings/langchain_azure_ai.embeddings.AzureAIOpenAIApiEmbeddingsModel.html)

## Use chat models

Create a chat model client by using `AzureAIOpenAIApiChatModel`. All Foundry Models supporting OpenAI-compatible APIs can be used with the client:

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

# Project endpoint + Microsoft Entra ID
model = AzureAIOpenAIApiChatModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(),
	model="gpt-4.1", # Or any model like "Mistral-Large-3"
)
```

Using `project_endpoint` requires Microsoft Entra ID for authentication and the role **Azure AI User**. For direct endpoint and API key authentication:

```python
import os

from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

model = AzureAIOpenAIApiChatModel(
	endpoint=os.environ["AZURE_AI_OPENAI_ENDPOINT"],
	credential=os.environ["AZURE_OPENAI_API_KEY"],
	model="Mistral-Large-3",
)
```

**What this snippet does:** Creates a chat model client by using either a
Foundry project endpoint with Microsoft Entra ID or a direct endpoint with API
key authentication.

### Verify your setup

Run a simple model invocation:

```python
response = model.invoke("Say hello")
print(response.content)
```

```output
[{'type': 'text', 'text': 'Hello! 👋 How can I help you today?', 'annotations': [], 'id': 'msg_a0b1c2d3e5...'}]
```

**What this snippet does:** Sends a basic prompt to verify endpoint,
authentication, and model routing.

**References:**
- [LangChain runnable interface](https://python.langchain.com/docs/concepts/runnables/)

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
	print(response.content)


await main()
```

```output
Hello! How can I help you today?
```

**What this snippet does:** Creates an async client and runs a non-blocking
request with `ainvoke`.

**References:**
- [Async credentials in Azure Identity](/python/api/overview/azure/identity-readme)
- [LangChain runnable interface](https://python.langchain.com/docs/concepts/runnables/)

## Use chat models

`AzureAIOpenAIApiChatModel` implements LangChain's runnable interface, so you
can invoke it with message lists.

```python
from langchain_core.messages import HumanMessage

messages = [
	{
		"role": "developer",
		"content": "Translate the following from English into Italian",
	},
	HumanMessage(content="hi!"),
]

model.invoke(messages).pretty_print()
```

```output
================================== Ai Message ==================================
Ciao! Come posso aiutarti oggi?
```

**What this snippet does:** Sends structured chat messages to the model and
prints the assistant response.

**References:**
- [LangChain messages](https://python.langchain.com/docs/concepts/messages/)

### Build prompt chains

Compose prompts, model calls, and output parsing by using the pipe operator.

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
	[("system", system_template), ("user", "{text}")]
)
parser = StrOutputParser()

chain = prompt_template | model | parser
result = chain.invoke({"language": "italian", "text": "hi"})
print(result)
```

```output
ciao
```

**What this snippet does:** Builds and invokes a simple translation chain with
templating and string output parsing.

**References:**
- [ChatPromptTemplate](https://python.langchain.com/docs/concepts/prompt_templates/)
- [Output parsers](https://python.langchain.com/docs/concepts/output_parsers/)

### Chain multiple models

Use one model to generate content and another model to verify it.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIOpenAIApiChatModel

producer = AzureAIOpenAIApiChatModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(),
	model="gpt-4.1",
)

verifier = AzureAIOpenAIApiChatModel(
	project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
	credential=DefaultAzureCredential(),
	model="Mistral-Large-3",
)
```

```python
from pprint import pprint

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

producer_template = PromptTemplate(
	template=(
		"You are an urban poet. Write verses about this topic:\n"
		"{topic}"
	),
	input_variables=["topic"],
)

verifier_template = PromptTemplate(
	template=(
		"You are a poem verifier. Reply with one word, True or False, based "
		"on whether the poem includes abusive language.\n"
		"Poem:\n"
		"{input}"
	),
	input_variables=["input"],
)

parser = StrOutputParser()
generate_poem = producer_template | producer | parser
verify_poem = verifier_template | verifier | parser

chain = generate_poem | RunnableParallel(
	poem=RunnablePassthrough(),
	verification=RunnablePassthrough() | verify_poem,
)

output = chain.invoke({"topic": "living in a foreign country"})
pprint(output)
```

```output
{'poem': '...generated poem text...', 'verification': 'False'}
```

**What this snippet does:** Builds a producer-verifier workflow that returns
both generated content and a safety-style verification result.

**References:**
- [LangChain runnables](https://python.langchain.com/docs/concepts/runnables/)
- [PromptTemplate](https://python.langchain.com/docs/concepts/prompt_templates/)

## Use embedding models

Create an embeddings client with
`AzureAIOpenAIApiEmbeddingsModel`.

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
	endpoint=os.environ["AZURE_AI_OPENAI_ENDPOINT"],
	credential=os.environ["AZURE_OPENAI_API_KEY"],
	model="text-embedding-3-large",
)
```

**What this snippet does:** Configures embeddings generation for vector search,
retrieval, and ranking workflows.


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

## Next step

> [!div class="nextstepaction"]
> [Use Foundry Agent Service with LangGraph](langchain-agents.md)
