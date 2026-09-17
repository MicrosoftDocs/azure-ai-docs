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
ms.date: 08/21/2026
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
- **Use agent tools** when you're building an agent that needs retrieval as a tool. For example, see [File search tool for agents](../agents/how-to/tools/file-search.md). To build a full RAG app with complete control instead, use the Foundry SDK.

## RAG workflow in Foundry

A RAG implementation in Foundry typically covers these stages:

- **Prepare your data**: Organize and chunk your private documents or knowledge base into searchable content.
- **Set up an index**: Create an Azure AI Search index or use another retrieval service to organize your content for efficient searching.
- **Connect to Foundry**: Create a connection from your Foundry project to your index or retrieval service.
- **Build your RAG application**: Integrate retrieval with your model calls by using the Foundry SDK or REST APIs.
- **Test and evaluate**: Verify that retrieval quality is good and that responses are accurate and properly cited.

[!INCLUDE [retrieval-augmented-generation 2](../includes/concepts-retrieval-augmented-generation-2.md)]

## Related content

- [File search tool for agents](../agents/how-to/tools/file-search.md)
- [Quickstart: Agentic retrieval](../../search/search-get-started-agentic-retrieval.md)
