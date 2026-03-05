---
title: Get started with LangChain and LangGraph with Foundry
description: Learn how to use langchain-azure-ai as an entry point for LangChain and LangGraph apps with Microsoft Foundry capabilities.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/05/2026
ms.author: fasanti
author: santiagxf
ms.reviewer: sgilley
ms.custom:
  - classic-and-new
  - dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want an overview of langchain-azure-ai so I can choose the right integration pattern for my LangChain or LangGraph solution.
---

# Get started with LangChain and LangGraph with Foundry

Use `langchain-azure-ai` as the entry point for building LangChain and
LangGraph applications with Microsoft Foundry capabilities. This article gives
you a high-level map of the package so you can start quickly, then move to the
right deep-dive documentation for each capability.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../create-projects.md).
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate.

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

- Use `[tools]` if your app uses integrations such as Document Intelligence.
- Use `[opentelemetry]` if you want tracing integration.

## Choose integration building blocks

Use this map to pick the right namespace for your solution:

| Capability | Namespace | Typical use |
|---|---|---|
| Foundry Agent Service | `langchain_azure_ai.agents` | Build managed agent nodes and flows for LangGraph and LangChain. |
| Chat models | `langchain_azure_ai.chat_models` | Call Azure OpenAI and model catalog chat deployments. |
| Embeddings | `langchain_azure_ai.embeddings` | Generate vectors for search, retrieval, and ranking workflows. |
| Vector stores | `langchain_azure_ai.vectorstores` | Use Azure AI Search and Cosmos DB vector integrations. |
| Retrievers | `langchain_azure_ai.retrievers` | Run retrieval over Azure-backed indexes and stores. |
| Chat history stores | `langchain_azure_ai.chat_message_histories` | Persist and replay chat history across sessions. |
| Tools | `langchain_azure_ai.tools` | Add tools such as Document Intelligence, Vision, health text analytics, and Logic Apps. |
| Callbacks and tracing | `langchain_azure_ai.callbacks` | Capture run events and emit OpenTelemetry traces. |
| Query constructors | `langchain_azure_ai.query_constructors` | Build backend-specific query filters for retrieval scenarios. |

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
