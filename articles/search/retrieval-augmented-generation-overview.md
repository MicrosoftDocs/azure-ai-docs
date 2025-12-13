---
title: RAG and generative AI
titleSuffix: Azure AI Search
description: Learn how generative AI and retrieval augmented generation (RAG) patterns are used in Azure AI Search solutions.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 12/12/2025
ms.service: azure-ai-search
ms.topic: article
ms.custom:
  - ignite-2023
  - ignite-2024
  - build-2025
---

# Retrieval-augmented Generation (RAG) in Azure AI Search

Retrieval-augmented Generation (RAG) is a design pattern that augments the capabilities of a pretrained large language model (LLM) by adding newer, specialized, or proprietary content to help answer questions. 

RAG implementations typically include an information retrieval component. The decision about which information retrieval system to use is critical because LLMs are constrained by the number of token inputs they can accept, so you want the grounding data to be as relevant as possible. Criteria to consider include:

+ Ability to pull from a broad range of data sources and platforms.

+ Query capabilities that can target all of your data and return synthesized and highly relevant results, in the short-form formats necessary for meeting the token length requirements of LLM inputs.

+ Ease of integration with agents and chat apps, and other models and processes that are part of your application.

+ Built-in content preparation (chunking, vectorization, image verbalization). It's common to consolidate searchable data into separate physical data structures that are optimized for search. You can verbalize, recognize, or analyze images to get text-equivalent information into your index. More likely, you might want to chunk verbose source content so that it can be easily consumed, and vectorize that content if you want similarity search.

Azure AI Search is a [proven solution for RAG workloads](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md). It provides indexing and query capabilities that meet common criteria, with the infrastructure and security of the Azure cloud. Through code and other components, you can design a full stack RAG architecture that includes all of the elements for generative AI over your proprietary content.

You can choose between two approaches for RAG workloads: new **agentic retrieval** for modern RAG (currently in preview), or the original query architecture for **classic RAG**. If you're required to use only generally available features, you should consider classic RAG.

## Modern RAG with agentic retrieval

Azure AI Search now provides agentic retrieval, a specialized pipeline designed specifically for RAG patterns. This approach uses LLMs to intelligently break down complex user queries into focused subqueries, executes them in parallel, and returns structured responses optimized for chat completion models.

Agentic retrieval represents the evolution from traditional single-query RAG patterns to multi-query intelligent retrieval, providing:

+ Context-aware query planning using conversation history
+ Parallel execution of multiple focused subqueries  
+ Structured responses with grounding data, citations, and execution metadata
+ Built-in semantic ranking for optimal relevance
+ Optional answer synthesis that uses an LLM-formulated answer in the query response.

You need new objects for this pipeline: one or more knowledge sources, a knowledge base, and the retrieve action that you call from application code, such as a tool that works with your AI agent.

For new RAG implementations, we recommend starting with [agentic retrieval](agentic-retrieval-overview.md). For existing solutions, consider migrating to take advantage of improved accuracy and context understanding.

## Classic RAG pattern for Azure AI Search

Classic RAG uses the original query execution architecture where your application sends a single query to Azure AI Search and orchestrates the handoff to an LLM separately. This approach is simpler with fewer components, and faster because there's no LLM involvement in query planning.

For detailed information about implementing classic RAG, see the [azure-search-classic-rag repository](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md).

## Comparison of agentic retrieval and classic RAG

You can choose between two approaches for RAG workloads: new **agentic retrieval** for modern RAG (currently in preview), or the original query architecture for **classic RAG**. The following table highlights the key differences to help you choose.

| Characteristic | Agentic retrieval | Classic RAG |
|----------------|-------------------|-------------|
| Search corpus  | [A knowledge base](/rest/api/searchservice/knowledge-bases/create-or-update) that defines an entire search domain. It can include one or more search indexes (indexed content) and remote content from Bing and SharePoint.| [A single search index](/rest/api/searchservice/indexes/create-or-update). |
| Query mechanism  | [Retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve) | [Search Documents](/rest/api/searchservice/documents/search-post) |
| Query composition | Multiple subqueries, as many as needed, composed by an LLM. | A single-shot query. |
| Query execution | Keyword, vector, hybrid in subqueries. <br>Optionally, call an LLM to return a formulated answer in the response. | Keyword, vector, hybrid in a single shot. |
| Query response | A long unified string in a multi-part format, consisting of a query activity plan, results, citations, source data. | Flattened rowset based on fields in the index. |
| LLM integration at query time | Query planning, embedded answer synthesis. | None. Application code sends results to an LLM. |

## Searchable content in Azure AI Search

Azure AI Search indexes support multiple content types optimized for RAG:

| Content type | How it's indexed | Key features |
|--------------|------------------|--------------|
| Plain text | Tokens, raw text | [Indexers](search-indexer-overview.md) and [knowledge sources](agentic-knowledge-source-overview.md). Also, [analyzers](search-analyzers.md) and [normalizers](search-normalizers.md) to modify text in flight. [Synonym maps](search-synonyms.md) for query expansion. |
| Vectorized text <sup>1</sup> | [Embeddings](vector-search-how-to-create-index.md) | [Chunking and vectorization](vector-search-integrated-vectorization.md) via indexers  or external tools |
| Images<sup>2</sup | Tokens via OCR and AI | OCR and Image Analysis [skills](cognitive-search-working-with-skillsets.md) (indexer required) |
| Multimodal | Unified embeddings | [Azure Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) or [OpenAI CLIP](https://github.com/openai/CLIP/blob/main/README.md) for unified embedding space. |

For agentic retrieval, you can also access remote sources (Bing, SharePoint) without indexing.

Vectors provide the best accommodation for dissimilar content (multiple file formats and languages) because content is expressed universally in mathematical representations. Vectors also support similarity search: matching on the coordinates that are most similar to the vector query. Compared to keyword search (or term search) that matches on tokenized terms, similarity search is more nuanced. It's a better choice if there's ambiguity or interpretation requirements in the content or in queries.

For implementation details, see [integrated vectorization](vector-search-integrated-vectorization.md) and [skillsets](cognitive-search-working-with-skillsets.md).

## Maximize relevance and recall

To ensure the best results for your RAG implementation:

+ [Use hybrid queries](hybrid-search-overview.md) that combine keyword (nonvector) and vector search for maximum recall. In a hybrid query, if you double down on the same input, a text string and its vector equivalent generate parallel queries for keywords and similarity search, returning the most relevant matches from each query type in a unified result set.

+ [Use semantic ranking](semantic-ranking.md), built into agentic retrieval, optional for classic RAG.

+ [Apply scoring profiles](index-add-scoring-profiles.md) to boost specific fields or criteria.

+ Fine-tune with vector query parameters for [vector weighting](vector-search-how-to-query.md#vector-weighting) and [minimum thresholds](vector-search-how-to-query.md#set-thresholds-to-exclude-low-scoring-results-preview).

Learn more about [hybrid search](hybrid-search-overview.md) and [semantic ranking](semantic-ranking.md).

## Choosing between agentic retrieval and classic RAG

**Use agentic retrieval when:**

+ You need the highest possible relevance and accuracy
+ Your queries are complex or conversational
+ You want structured responses with citations and query details
+ You're building new RAG implementations

**Use classic RAG when:**

+ You need generally available (GA) features only
+ Simplicity and speed are priorities over advanced relevance
+ You have existing orchestration code you want to preserve
+ You need fine-grained control over the query pipeline

A RAG solution that includes agents and Azure AI Search can benefit from [Foundry IQ](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-unlocking-ubiquitous-knowledge-for-agents/4470812), as an agent's single endpoint to a knowledge layer that provides grounding data.

Review the resources in the next section for more options and next steps.

## How to get started

There are many ways to get started, including code-first solutions and demos.

### [**Videos**](#tab/videos)

+ [Build agents with knowledge, agentic RAG and Azure AI Search](https://www.youtube.com/watch?v=lW47o2ss3Yg) 

+ [Foundry IQ: the future of RAG with knowledge retrieval and AI Search](https://www.youtube.com/watch?v=slDdNIQCJBQ)

+ [(Classic RAG) Vector search and state of the art retrieval for Generative AI apps](https://www.youtube.com/watch?v=lSzc1MJktAo)

### [**Docs**](#tab/docs)

+ [Retrieval augmented generation and indexes (Foundry)](/azure/ai-foundry/concepts/retrieval-augmented-generation)

+ [Try this agentic retrieval quickstart](search-get-started-agentic-retrieval.md) to walk through the new and recommended approach for RAG.

+ [Try this agentic retrieval tutorial](agentic-retrieval-how-to-create-pipeline.md) for a more comprehensive approach that includes an agent.

+ Interested in classic RAG? The [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md) repository has quickstarts and a tutorial.

+ [Review indexing concepts and strategies](search-what-is-an-index.md) to determine how you want to ingest and refresh data. Decide whether to use vector search, keyword search, or hybrid search. The kind of content you need to search over, and the type of queries you want to run, determines index design.

+ [Review creating queries](search-query-create.md) to learn more about search request syntax and requirements.

> [!NOTE]
> Some Azure AI Search features are intended for human interaction and aren't useful in a RAG pattern. Specifically, you can skip features like autocomplete and suggestions. Other features like facets and orderby might be useful, but would be uncommon in a RAG scenario.

### [**Code**](#tab/demos)

+ [RAG chat app with Azure OpenAI and Azure AI Search (Python)](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md), updated for agentic retrieval.

+ [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md) in REST, Python, Java, .NET, JavaScript, and TypeScript.

+ [Classic RAG Time Journeys](https://github.com/microsoft/rag-time)

+ [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples)

### [**Templates**](#tab/templates)

[Use enterprise chat app templates](https://aka.ms/azai) deploy Azure resources, code, and sample grounding data using fictitious health plan documents for Contoso and Northwind. This end-to-end solution gives you an operational chat app in as little as 15 minutes. Code for these templates is the **azure-search-openai-demo** featured in several presentations. The following links provide language-specific versions:

+ [.NET](https://aka.ms/azai/net)
+ [Python](https://aka.ms/azai/py)
+ [JavaScript](https://aka.ms/azai/js)
+ [Java](https://aka.ms/azai/javat)

---