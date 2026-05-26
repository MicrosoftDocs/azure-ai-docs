---
title: "Retrieval augmented generation (RAG) and indexes in Microsoft Foundry"
description: "Learn how retrieval augmented generation (RAG) uses indexes and grounding data to improve response accuracy in generative AI apps."
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - pilot-ai-workflow-jan-2026
  - doc-kit-assisted
ms.topic: concept-article
ms.date: 05/20/2026
ms.reviewer: sgilley
ms.author: sgilley
ai-usage: ai-assisted
author: sdgilley
---

# Retrieval augmented generation (RAG) and indexes

[!INCLUDE [retrieval-augmented-generation 1](../includes/concepts-retrieval-augmented-generation-1.md)]

## Choose an approach in Foundry

Foundry supports multiple patterns for working with private data. Choose based on your use case complexity and how much control you need:

- **Use RAG** when you need answers grounded in private or frequently changing data.
- **Use fine-tuning** when you need to change model behavior, style, or task performance, rather than add fresh knowledge.
- **Use agent tools** when you're building an agent that needs retrieval as a tool. For example, see [File search tool for agents](../agents/how-to/tools/file-search.md).

## Getting started with RAG in Foundry

Implementing RAG in Foundry typically follows this workflow:

1. **Prepare your data**: Organize and chunk your private documents or knowledge base into searchable content
2. **Set up an index**: Create an Azure AI Search index or use another retrieval service to organize your content for efficient searching
3. **Connect to Foundry**: Create a connection from your Foundry project to your index or retrieval service
4. **Build your RAG application**: Integrate retrieval with your LLM calls using the Foundry SDK or REST APIs
5. **Test and evaluate**: Verify that retrieval quality is good and responses are accurate and properly cited

To get started, choose one of these paths based on your needs:

- **Agent with retrieval**: If you're building an agent, use retrieval as a tool. See [File search tool for agents](../agents/how-to/tools/file-search.md).
- **Custom RAG application**: Build a full RAG app with the Foundry SDK for complete control.

[!INCLUDE [retrieval-augmented-generation 2](../includes/concepts-retrieval-augmented-generation-2.md)]

## Related content

- [File search tool for agents](../agents/how-to/tools/file-search.md)
- [Quickstart: Agentic retrieval](../../search/search-get-started-agentic-retrieval.md)
