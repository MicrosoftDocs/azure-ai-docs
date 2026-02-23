---
title: Retrieval augmented generation (RAG) and indexes in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how retrieval augmented generation (RAG) uses indexes and grounding data to improve response accuracy in generative AI apps.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - pilot-ai-workflow-jan-2026
ms.topic: concept-article
ms.date: 02/04/2026
ms.reviewer: sgilley
ms.author: sgilley
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: sdgilley
---

# Retrieval augmented generation (RAG) and indexes

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
- **Embeddings**: Numeric representations of content used for vector similarity search. See [Understand embeddings](../openai/concepts/understand-embeddings.md).
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

## Choose an approach in Foundry

Foundry supports multiple patterns for working with private data. Choose based on your use case complexity and how much control you need:

- **Use RAG** when you need answers grounded in private or frequently changing data.
- **Use fine-tuning** when you need to change model behavior, style, or task performance, rather than add fresh knowledge.
- **Use a managed “use your data” experience** if you want a more guided way to connect, ingest, and chat over your data. See [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md) and [Quickstart: Chat with Azure OpenAI models using your own data](../openai/use-your-data-quickstart.md).
:::moniker range="foundry"
- **Use agent tools** when you're building an agent that needs retrieval as a tool. For example, see [File search tool for agents](../default/agents/how-to/tools/file-search.md).
:::moniker-end

## Getting started with RAG in Foundry

Implementing RAG in Foundry typically follows this workflow:

1. **Prepare your data**: Organize and chunk your private documents or knowledge base into searchable content
2. **Set up an index**: Create an Azure AI Search index or use another retrieval service to organize your content for efficient searching
3. **Connect to Foundry**: Create a connection from your Foundry project to your index or retrieval service
4. **Build your RAG application**: Integrate retrieval with your LLM calls using the Foundry SDK or REST APIs
5. **Test and evaluate**: Verify that retrieval quality is good and responses are accurate and properly cited

::: moniker range="foundry"

To get started, choose one of these paths based on your needs:

- **Guided experience**: Start with [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md), which provides a managed setup for connecting data and chatting over it. See [Quickstart: Chat with Azure OpenAI models using your own data](../openai/use-your-data-quickstart.md).
- **Agent with retrieval**: If you're building an agent, use retrieval as a tool. See [File search tool for agents](../default/agents/how-to/tools/file-search.md).
- **Custom RAG application**: Build a full RAG app with the Foundry SDK for complete control.

::: moniker-end

::: moniker range="foundry-classic"

To get started, follow these tutorials:

- [Tutorial: Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-create-resources.md)
- [Tutorial: Part 2 - Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-build-rag.md)

::: moniker-end

## Security and privacy considerations

RAG systems can expose sensitive content if you don't design access and prompting carefully.

- **Apply access control at retrieval time**. If you're using Azure AI Search as a data source, you can use document-level access control with security filters. See the [document-level access control](../openai/concepts/use-your-data.md#document-level-access-control) section.
- **Prefer Microsoft Entra ID over API keys for production**. API keys are convenient for development but aren't recommended for production scenarios. For Azure AI Search RBAC guidance, see [Connect to Azure AI Search using roles](../../search/search-security-rbac.md).
- **Treat retrieved content as untrusted input**. Your system message and application logic should reduce the risk of prompt injection from documents and retrieved passages. See [Safety system messages](../openai/concepts/system-message.md).

## Cost and latency considerations

RAG adds extra work compared to a model-only request:

- **Retrieval costs and latency**: Querying an index adds round trips and compute.
- **Embedding costs and latency**: Vector search requires embeddings at indexing time, and often at query time.
- **Token usage**: Retrieved passages increase input tokens, which can increase cost.

If you're using Azure AI Search, confirm service tier and pricing before production rollout. If you're using semantic or hybrid retrieval, review Azure AI Search pricing and limits in the Azure AI Search documentation.

## Limitations and troubleshooting

### Known limitations

- RAG quality depends on content preparation, retrieval configuration, and prompt design. Poor data preparation or indexing strategy directly impacts response quality.
- If retrieval returns irrelevant or incomplete passages, the model can still produce incomplete or inaccurate answers despite grounding.
- If you don't control access to source content, grounded responses can leak sensitive information from your index.

### Common challenges and mitigation

- **Poor retrieval quality**: If your index isn't returning relevant passages, review your data chunking strategy, embedding model quality, and search configuration (keyword vs. semantic vs. hybrid).
- **Hallucination despite grounding**: Even with retrieved content, models can still generate inaccurate responses. Enable citations and use clear system messages and prompts to instruct the model to stick to retrieved content.
- **Latency issues**: Large indexes can slow retrieval. Consider indexing strategy, filtering, and re-ranking to reduce the volume of passages processed.
- **Token budget exceeded**: Retrieved passages can quickly consume token limits. Implement passage filtering, ranking, or summarization to stay within budget.

For guidance on evaluating RAG effectiveness, see the tutorials and quickstarts in the related content section below.

## Related content

::: moniker range="foundry"

- [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md)
- [File search tool for agents](../default/agents/how-to/tools/file-search.md)
- [Quickstart: Agentic retrieval](../../search/search-get-started-agentic-retrieval.md)
- [File search tool for agents](../default/agents/how-to/tools/file-search.md)

::: moniker-end

::: moniker range="foundry-classic"

- [Tutorial: Part 1 - Set up project and development environment to build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-create-resources.md)
- [Tutorial: Part 2 - Build a custom knowledge retrieval (RAG) app with the Microsoft Foundry SDK](../tutorials/copilot-sdk-build-rag.md)
- [Quickstart: Chat with Azure OpenAI models using your own data](../openai/use-your-data-quickstart.md)
- [Azure OpenAI On Your Data](../openai/concepts/use-your-data.md)


::: moniker-end
