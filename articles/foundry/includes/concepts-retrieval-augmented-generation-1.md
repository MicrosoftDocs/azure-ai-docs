---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Retrieval augmented generation (RAG) is a pattern that combines search with large language models (LLMs) so responses are grounded in your data. This article explains how RAG works in Microsoft Foundry, what role indexes play, and how agentic retrieval changes classic RAG patterns.

LLMs are trained on public data available at training time. If you need answers based on your private data, or on frequently changing information, RAG helps you:

- Retrieve relevant information from your data (often through an index).
- Provide that information to the model as grounding data.
- Generate a response that can include citations back to source content.

## What is RAG?

Large language models (LLMs) like ChatGPT are trained on public internet data that was available when the model was trained. The public data might not be sufficient for your needs. For example, you might want answers based on private documents, or you might need up-to-date information.

RAG addresses this by retrieving relevant content from your data and including it in the model input. The model can then generate responses grounded in the retrieved content.

Key concepts for RAG:

- **Grounding data**: Retrieved content you provide to the model to reduce guessing.
- **Index**: A data structure optimized for retrieval (keyword, semantic, vector, or hybrid search).
- **Embeddings**: Numeric representations of content used for vector similarity search. See [Understand embeddings](../../foundry-classic/openai/concepts/understand-embeddings.md).
- **System message and prompts**: Instructions that guide how the model uses retrieved content. See [Prompt engineering](../openai/concepts/prompt-engineering.md) and [Safety system messages](../openai/concepts/system-message.md).

## How does RAG work?

RAG follows a three-step flow:

1. **Retrieve**: When a user asks a question, your application queries an index or data store to find relevant content.
2. **Augment**: The app combines the user's question and the retrieved content (grounding data) into a prompt.
3. **Generate**: The model receives the augmented prompt and generates a response grounded in the retrieved content, reducing inaccuracies and enabling accurate citations.

:::image type="content" source="../media/index-retrieve/rag-pattern.png" alt-text="Diagram that shows a user query, retrieval from a data store, and a grounded model response." lightbox="../media/index-retrieve/rag-pattern.png":::

## What is an index and why do I need it?

RAG works best when you can retrieve relevant content quickly and consistently. An index helps by organizing your content for efficient retrieval.

Many RAG solutions use an index that supports one or more of these retrieval modes:

- **Keyword search**
- **Semantic search**
- **Vector search**
- **Hybrid search** (keyword + vector, sometimes with semantic ranking)

An index can also store fields that improve citation quality (for example, document titles, URLs, or file names).

:::image type="content" source="../media/index-retrieve/rag-pattern-with-index.png" alt-text="Diagram that shows retrieval from an index and how the retrieved passages are added to the model prompt." lightbox="../media/index-retrieve/rag-pattern-with-index.png":::

Foundry can connect your project to an Azure AI Search service and index for retrieval. Depending on the feature and API surface you're using, this connection information might be represented as a project connection or an *index asset ID*.

For example, the Foundry Project REST API preview includes an `index_asset_id` field for Azure AI Search index resources. See [Foundry Project REST API preview](../reference/foundry-project-rest-preview.md).

Azure AI Search is a recommended index store for RAG scenarios. Azure AI Search supports retrieval over vector and textual data stored in search indexes, and it can also query other targets if you use agentic retrieval. See [What is Azure AI Search?](/azure/search/search-what-is-azure-search).

## Agentic RAG: modern approach to retrieval

Traditional RAG patterns often use a single query to retrieve information from your data. *Agentic retrieval*, also known as agentic RAG, is an evolution in retrieval architecture that uses a model to break down complex inputs into multiple focused subqueries, run them in parallel, and return structured grounding data that works well with chat completion models.

Agentic retrieval provides several advantages over classic RAG:

* **Context-aware query planning** - Uses conversation history to understand context and intent. Follow-up questions retain the context of earlier exchanges, making multi-turn conversations more natural.
* **Parallel execution** - Runs multiple focused subqueries simultaneously for better coverage. Instead of retrieving from a single query sequentially, parallel execution reduces latency and retrieves more diverse relevant results.
* **Structured responses** - Returns grounding data, citations, and execution metadata along with results. This structured output makes it easier for your application to cite sources accurately and trace the reasoning behind answers.
* **Built-in semantic ranking** - Ensures optimal relevance of results. Semantic ranking filters noise and prioritizes truly relevant passages, which is especially important with large datasets.
* **Optional answer synthesis** - Can include LLM-formulated answers directly in the query response. Alternatively, you can choose to return raw, verbatim passages for your application to process.

If you're using Azure AI Search as your retrieval engine, see [Agentic retrieval](/azure/search/agentic-retrieval-overview) and [Quickstart: Agentic retrieval](../../search/search-get-started-agentic-retrieval.md).
