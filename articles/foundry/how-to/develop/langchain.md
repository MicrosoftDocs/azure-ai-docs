---
title: Get started with LangChain and LangGraph with Foundry
description: Learn how to use langchain-azure-ai as an entry point for LangChain and LangGraph apps with Microsoft Foundry capabilities.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/05/2026
ms.author: fasantia
author: santiagxf
ms.reviewer: sgilley
ms.custom:
  - classic-and-new
  - dev-focus
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
# customer intent: As a developer, I want an overview of langchain-azure-ai so I can choose the right integration pattern for my LangChain or LangGraph solution.
---

# Get started with LangChain and LangGraph with Foundry

Use the `langchain-azure-ai` package as the entry point for building LangChain and
LangGraph applications with Microsoft Foundry capabilities. This article gives
you a high-level map of the package so you can start quickly, then move to the
right deep-dive documentation for each capability.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../create-projects.md).
- The **Azure AI User** role on the Foundry project (least-privilege role for
  development). If you also create or manage resources, use **Contributor** or
  **Owner** as needed. For details, see [Role-based access control for
  Microsoft Foundry](../../concepts/rbac-foundry.md).
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate.

> [!TIP]
> This article mentions support for **Microsoft Foundry (new)**, which uses version `azure-ai-projects>=2.0`.
> If you are using Foundry classic, use `langchain-azure-ai[v1]` instead.

## Install the package

Install the base package:

```bash
pip install -U langchain-azure-ai azure-identity
```

Install optional extras based on your scenario:

```bash
pip install -U "langchain-azure-ai[tools]"
pip install -U "langchain-azure-ai[opentelemetry]"
```

- Use `[tools]` if your app uses tools from the namespace `langchain_azure_ai.tools.*`, like Document Intelligence.
- Use `[opentelemetry]` if you want tracing integration via OpenTelemetry.

## Choose integration building blocks

Use this map to pick the right namespace for your solution:

| Capability | Namespace | Typical use |
|---|---|---|
| Foundry Agent Service | `langchain_azure_ai.agents` | Build managed agent nodes to build complex graph and flows for LangGraph and LangChain. |
| Chat models | `langchain_azure_ai.chat_models` | Call Azure OpenAI and model catalog chat models. |
| Embeddings | `langchain_azure_ai.embeddings` | Call embedding models from the catalog and generate vectors for search, retrieval, and ranking workflows. |
| Vector stores | `langchain_azure_ai.vectorstores` | Use Azure AI Search and Cosmos DB vector integrations. |
| Retrievers | `langchain_azure_ai.retrievers` | Run retrieval over Azure-backed indexes and stores. |
| Chat history stores | `langchain_azure_ai.chat_message_histories` | Persist and replay chat history across sessions. Use memory-powered histories to retrieve consolidated pass chat history. |
| Tools | `langchain_azure_ai.tools` | Add tools such as Document Intelligence, Vision, health text analytics, and Logic Apps. |
| Callbacks and tracing | `langchain_azure_ai.callbacks` | Capture run events and emit OpenTelemetry traces. |
| Query constructors | `langchain_azure_ai.query_constructors` | Build backend-specific query filters for retrieval scenarios. |

See the section [Learn each capability in detail](#learn-each-capability-in-detail) for specific walkthroughs. 

## Connect with project endpoints and credentials

Many `langchain-azure-ai` classes support connecting through a Foundry project
endpoint. Set `AZURE_AI_PROJECT_ENDPOINT` once, then reuse it across supported
classes.

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/openai/v1"
```

When you use `project_endpoint`, authentication uses Microsoft Entra ID and
Azure RBAC on the project. API keys are for direct service endpoints, such as
`/openai/v1`.

### Example: use `project_endpoint` or `endpoint`

Use `AzureAIChatCompletionsModel` as a representative pattern:

```python
import os

from azure.identity import AzureCliCredential, DefaultAzureCredential
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

# Option A: Use a Foundry project endpoint (Microsoft Entra ID required).
model_from_project = AzureAIChatCompletionsModel(
  project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
  credential=DefaultAzureCredential(),
  model="gpt-4.1",
)

# Option B: Use a service endpoint directly.
model_from_endpoint = AzureAIChatCompletionsModel(
  endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  credential=DefaultAzureCredential(),
  model="gpt-4.1",
)

# Option C: Use a different credential strategy.
model_with_cli_credential = AzureAIChatCompletionsModel(
  endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
  credential="super-secret",
  model="gpt-4.1",
)
```

**What this snippet does:** Shows the same model initialized from a Foundry
project endpoint or from a direct service endpoint, and shows how to swap
credentials.

You can apply the same pattern to tools. For example,
`AzureAIDocumentIntelligenceTool` can use the project endpoint and
`DefaultAzureCredential` without extra configuration when
`AZURE_AI_PROJECT_ENDPOINT` is set:

```python
from langchain_azure_ai.tools import AzureAIDocumentIntelligenceTool

document_tool = AzureAIDocumentIntelligenceTool()
```

### How `DefaultAzureCredential` works

`DefaultAzureCredential` tries several Microsoft Entra ID credential sources in
order and uses the first one that works. Common sources are environment
variables, managed identity, developer tools, and Azure CLI.

Use `DefaultAzureCredential` as the default for local development and deployed
workloads. If you need stricter control, replace it with a specific credential
such as `AzureCliCredential` for local-only development or
`ManagedIdentityCredential` for production workloads in Azure.

The same project-endpoint pattern is also used by other classes.

## Learn each capability in detail

Start with these guides in this documentation set:

- [Use LangGraph with the Agent Service](langchain-agents.md)
- [Use Foundry Memory with LangChain and LangGraph](langchain-memory.md)
- [Trace LangChain and LangGraph apps with Foundry](langchain-traces.md)

Use these package resources for module-level details and updates:

- [Package overview](https://github.com/langchain-ai/langchain-azure/tree/main/libs/azure-ai) and [README](https://github.com/langchain-ai/langchain-azure/blob/main/libs/azure-ai/README.md).
- [LangChain documentation for `langchain-azure-ai`](https://python.langchain.com/api_reference/azure_ai).

## Next step

> [!div class="nextstepaction"]
> [Use LangGraph with the Agent Service](langchain-agents.md)
