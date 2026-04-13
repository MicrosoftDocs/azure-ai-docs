---
title: "Retrieval augmented generation (RAG) and indexes in Microsoft Foundry (classic)"
description: "Learn how retrieval augmented generation (RAG) uses indexes and grounding data to improve response accuracy in generative AI apps. (classic)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - pilot-ai-workflow-jan-2026
ms.topic: concept-article
ms.date: 02/04/2026
ms.reviewer: sgilley
ms.author: sgilley
ai-usage: ai-assisted
author: sdgilley
ROBOTS: NOINDEX, NOFOLLOW
---

# Retrieval augmented generation (RAG) and indexes (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/retrieval-augmented-generation.md)

[!INCLUDE [retrieval-augmented-generation 1](../../foundry/includes/concepts-retrieval-augmented-generation-1.md)]

## Choose an approach in Foundry

Foundry supports multiple patterns for working with private data. Choose based on your use case complexity and how much control you need:

- **Use RAG** when you need answers grounded in private or frequently changing data.
- **Use fine-tuning** when you need to change model behavior, style, or task performance, rather than add fresh knowledge.
- **Use a managed “use your data” experience** if you want a more guided way to connect, ingest, and chat over your data. See [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md) and [Quickstart: Chat with Azure OpenAI models using your own data](../quickstarts/get-started-code.md).

## Getting started with RAG in Foundry

Implementing RAG in Foundry typically follows this workflow:

1. **Prepare your data**: Organize and chunk your private documents or knowledge base into searchable content
2. **Set up an index**: Create an Azure AI Search index or use another retrieval service to organize your content for efficient searching
3. **Connect to Foundry**: Create a connection from your Foundry project to your index or retrieval service
4. **Build your RAG application**: Integrate retrieval with your LLM calls using the Foundry SDK or REST APIs
5. **Test and evaluate**: Verify that retrieval quality is good and responses are accurate and properly cited

To get started, follow these tutorials:

- [Tutorial: Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-create-resources.md)
- [Tutorial: Part 2 - Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-build-rag.md)

[!INCLUDE [retrieval-augmented-generation 2](../../foundry/includes/concepts-retrieval-augmented-generation-2.md)]

## Related content

- [Tutorial: Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-create-resources.md)
- [Tutorial: Part 2 - Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-build-rag.md)
- [Quickstart: Chat with Azure OpenAI models using your own data](../quickstarts/get-started-code.md)
- [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md)
