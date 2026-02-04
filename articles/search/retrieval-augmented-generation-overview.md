---
title: RAG and generative AI
titleSuffix: Azure AI Search
description: Learn how generative AI and retrieval augmented generation (RAG) patterns are used in Azure AI Search solutions.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 01/15/2026
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - ignite-2023
  - ignite-2024
  - build-2025
---

# Retrieval-augmented Generation (RAG) in Azure AI Search

Retrieval-augmented Generation (RAG) is a pattern that extends LLM capabilities by grounding responses in your proprietary content. While conceptually simple, RAG implementations face significant challenges.

## The challenges of RAG

| Challenge | Description |
|-----------|-------------|
| **Query&nbsp;understanding** | Modern users ask complex, conversational, or vague questions with assumed context. Traditional keyword search fails when queries don't match document terminology. For RAG, an information retrieval system must understand intent, not just match words. |
| **Multi-source&nbsp;data&nbsp;access** | Enterprise content spans SharePoint, databases, blob storage, and other platforms. Creating a unified search corpus without disrupting data operations is essential. |
| **Token&nbsp;constraints** | LLMs accept limited token inputs. Your retrieval system must return highly relevant, concise results - not exhaustive document dumps. |
| **Response&nbsp;time&nbsp;expectations** | Users expect AI-powered answers in seconds, not minutes. The retrieval system must balance thoroughness with speed.
| **Security&nbsp;and&nbsp;governance** | Opening private content to LLMs requires granular access control. Users and agents must only retrieve authorized content. |

## How Azure AI Search meets RAG challenges

Azure AI Search provides two approaches designed specifically for these RAG challenges:

+ **[Agentic retrieval](#modern-rag-with-agentic-retrieval) (preview)**: A complete RAG pipeline with LLM-assisted query planning, multi-source access, and structured responses optimized for agent consumption.

+ **[Classic RAG pattern](#classic-rag-pattern-for-azure-ai-search)**: The proven approach using hybrid search and semantic ranking, ideal for simpler requirements or when generally available (GA) features are required.

The following sections explain how each approach solves specific RAG challenges.

### Solving query understanding challenges

**The problem:** Users ask "What's our PTO policy for remote workers hired after 2023?" but documents say "time off," "telecommute," and "recent hires."

**Agentic retrieval solution:**

+ LLM analyzes the question and generates multiple targeted subqueries.
+ Decomposes complex questions into focused searches.
+ Uses conversation history to understand context.
+ Parallel execution across knowledge sources.

**Classic RAG solution:**

+ Hybrid queries combine keyword and vector search for better recall.
+ Semantic ranking re-scores results based on meaning, not just keywords.
+ Vector similarity search matches concepts, not exact terms.

[Learn more about query planning](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

### Solving multisource data challenges

**The problem:** HR policies in SharePoint, benefits in databases, company news on web pages - creating copies disrupts governance and routine data operations.

**Agentic retrieval solution:**

+ Knowledge bases unify multiple knowledge sources.
+ Direct query against remote SharePoint and Bing (no indexing needed) to supplement index content.
+ Retrieval instructions guide the LLM to appropriate data sources.
+ Automatic indexing pipeline generation for Azure Blob, OneLake, ingested SharePoint content, ingested other external content.
+ Single query interface and query plan across all sources.

**Classic RAG solution:**

+ Indexers pull from more than 10 Azure data sources.
+ Skills pipeline for chunking, vectorization, image verbalization, and analysis.
+ Incremental indexing keeps content fresh.
+ You control what's indexed and how.

[Learn more about knowledge sources](agentic-knowledge-source-overview.md).

### Solving token constraint challenges

**The problem:** GPT-4 accepts about 128k tokens, but you have 10,000 pages of documentation. Sending everything wastes tokens and degrades quality.

**Agentic retrieval solution:**

+ Returns a structured response with only the most relevant chunks
+ Built-in citation tracking shows provenance
+ Query activity log explains what was searched
+ Optional answer synthesis reduces token usage further

**Classic RAG solution:**

+ Semantic ranking identifies the top 50 most relevant results
+ Configurable result limits (top-k for vectors, top-n for text) and minimum thresholds
+ Scoring profiles boost critical content
+ Select statement controls which fields are returned

[Learn more about relevance tuning](#maximize-relevance-and-recall).

### Solving response time challenges

**The problem:** Users expect answers in 3-5 seconds, but you're querying multiple sources with complex processing.

**Agentic retrieval solution:**

+ Parallel subquery execution (not sequential)
+ Adjustable reasoning effort (minimal/low/medium)
+ Pre-built semantic ranking (no extra orchestration)

**Classic RAG solution:**

+ Millisecond query response times
+ Single-shot queries reduce complexity
+ You control timeout and retry logic
+ Simpler architecture with fewer failure points

### Solving security challenges

**The problem:** Finance data should only be accessible to finance team, even when an executive asks the chatbot.

**Agentic retrieval solution:**

+ Knowledge source-level access control
+ Inherits SharePoint permissions for queries against remote SharePoint
+ Inherits Microsoft Entra ID permission metadata for indexed content from Azure Storage
+ Filter-based security at query time for other data sources
+ Network isolation via private endpoints

**Classic RAG solution:**

+ Document-level security trimming
+ Inherits Microsoft Entra ID permission metadata for indexed content from Azure Storage
+ Filter-based security at query time for other data sources
+ Network isolation via private endpoints

[Learn more about security](search-security-overview.md).

<!-- OLD INTRO
Retrieval-augmented Generation (RAG) is a design pattern in AI that augments the capabilities of a pretrained large language model (LLM) by adding newer, specialized, or proprietary content to help answer questions. To get that content, you typically need an information retrieval component. Azure AI Search is an information retrieval solution that's designed to solve the challenges of RAG implementations.

+ The first challenge: rising expectations for reasonable answers regardless of the quality of the question. The modern query consists of complex or convoluted questions, possibly vague or incomplete, with the assumption of context from the current chat. These become the inputs to the information retrieval system, against which the system must understand so that it can find relevant matches for LLM answer formulation.

+ The second challenge: The search domain consists of multiple data sources and platforms. Content might be in various locations and in heterogenous content types. Solving for data extraction and access across disparate systems is a key objective for RAG workloads. You need to be able to either access each data source directly, or easily consolidate content into a search corpus without disrupting data operations.

+ The third challenge: LLMs are constrained by the number of token inputs they can accept. The information retrieval system must be efficient in how it provides inputs to the LLM. The response must be designed for the constraints under which LLMs operate.

+ The fourth challenge: Turnaround should be fast. Users expect reasoning efforts to take longer than traditional web searches, but they still want answers in seconds. 

+ The fifth challenge: Data security and governance. When you open up private content to information retrieval workloads, users and LLMs must only have access to authorized content.

Azure AI Search can meet *all* of these challenges with the new agentic retrieval pipeline currently in preview. It's designed for the entire problem space, connecting your agent and application code to the right data at the right time, and returning the most useful content to the LLM.

It can meet *most* of these challenges with the classic search engine that accepts single-shot queries against a single search index. Classic search is generally available, and it supports a hybrid search capability with semantic ranking that produces high quality responses that help LLMs deliver their best answers using your content.

This article explores modern RAG and classic RAG experiences that you can get with Azure AI Search. It speaks to the challenges of RAG implementations and how Azure AI Search solves for specific problems with each RAG pattern. 
 -->

### Modern RAG with agentic retrieval

Azure AI Search is a [proven solution for RAG workloads](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md). It now provides [agentic retrieval](search-what-is-azure-search.md#what-is-agentic-retrieval), a specialized pipeline designed specifically for RAG patterns. This approach uses LLMs to intelligently break down complex user queries into focused subqueries, executes them in parallel, and returns structured responses optimized for chat completion models.

Agentic retrieval represents the evolution from traditional single-query RAG patterns to multi-query intelligent retrieval, providing:

+ Context-aware query planning using conversation history
+ Parallel execution of multiple focused subqueries  
+ Structured responses with grounding data, citations, and execution metadata
+ Built-in semantic ranking for optimal relevance
+ Optional answer synthesis that uses an LLM-formulated answer in the query response

You need new objects for this pipeline: one or more knowledge sources, a knowledge base, and the retrieve action that you call from application code, such as a tool that works with your AI agent.

For new RAG implementations, start with [agentic retrieval](agentic-retrieval-overview.md). For existing solutions, consider migrating to take advantage of improved accuracy and context understanding.

### Classic RAG pattern for Azure AI Search

Classic RAG uses the [original query execution architecture](search-what-is-azure-search.md#what-is-classic-search) where your application sends a single query to Azure AI Search and orchestrates the handoff to an LLM separately. Your deployed LLM formulates an answer using the flattened result set from the query. This approach is simpler with fewer components, and faster because there's no LLM involvement in query planning.

For detailed information about implementing classic RAG, see the [azure-search-classic-rag repository](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md).

## Content preparation for RAG

RAG quality depends on how you prepare content for retrieval. Azure AI Search supports:

| Content challenge | How Azure AI Search helps |
|-------------------|---------------------------|
| **Large documents** | Automatic chunking (built-in or via skills) |
| **Multiple languages** | More than 50 language analyzers for text, multilingual vectors |
| **Images and PDFs** | OCR, image analysis, image verbalization, document extraction skills |
| **Need for similarity search** | Integrated vectorization (Azure OpenAI, Azure Vision in Foundry Tools, custom) |
| **Terminology mismatches** | Synonym maps, semantic ranking |

**For agentic retrieval:** Use [knowledge sources](agentic-knowledge-source-overview.md) that auto-generate chunking and vectorization pipelines.

**For classic RAG:** Use [indexers and skillsets](search-indexer-overview.md) to build custom pipelines, or push pre-processed content via the [push API](search-what-is-data-import.md).

### Maximize relevance and recall

How do you provide the best grounding data for LLM answer formulation? It's a combination of having appropriate content, smart queries, and query logic that can identify the best chunks for answering a question.

During indexing, use chunking to subdivide large documents so that portions can be matched on independently. Include a vectorization step to create embeddings used for vector queries.

On the query side, to ensure the most relevant results for your RAG implementation:

+ [Use hybrid queries](hybrid-search-overview.md) that combine keyword (nonvector) and vector search for maximum recall. In a hybrid query, if you double down on the same input, a text string and its vector equivalent generate parallel queries for keywords and similarity search, returning the most relevant matches from each query type in a unified result set.

+ [Use semantic ranking](semantic-ranking.md), built into agentic retrieval, optional for classic RAG.

+ [Apply scoring profiles](index-add-scoring-profiles.md) to boost specific fields or criteria.

+ Fine-tune with vector query parameters for [vector weighting](vector-search-how-to-query.md#vector-weighting) and [minimum thresholds](vector-search-how-to-query.md#set-thresholds-to-exclude-low-scoring-results-preview).

For more information, see [hybrid search](hybrid-search-overview.md) and [semantic ranking](semantic-ranking.md).

## Choose between agentic retrieval and classic RAG

**Use agentic retrieval when:**

+ Your client is an agent or chatbot.
+ You need the highest possible relevance and accuracy.
+ Your queries are complex or conversational.
+ You want structured responses with citations and query details.
+ You're building new RAG implementations.

**Use classic RAG when:**

+ You need generally available (GA) features only.
+ Simplicity and speed are priorities over advanced relevance.
+ You have existing orchestration code you want to preserve.
+ You need fine-grained control over the query pipeline.

A RAG solution that includes agents and Azure AI Search can benefit from [Foundry IQ](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-unlocking-ubiquitous-knowledge-for-agents/4470812), as an agent's single endpoint to a knowledge layer that provides grounding data. Foundry IQ uses agentic retrieval.

Learn more about [classic search](search-what-is-azure-search.md#what-is-classic-search), [agentic retrieval](search-what-is-azure-search.md#what-is-agentic-retrieval), and [how they compare](search-what-is-azure-search.md#how-they-compare).

## How to get started

There are many ways to get started, including code-first solutions and demos.

### [**Videos**](#tab/videos)

+ [Foundry IQ: The future of RAG with knowledge retrieval and Azure AI Search](https://www.youtube.com/watch?v=slDdNIQCJBQ)

+ [Build agents with knowledge, agentic RAG, and Azure AI Search](https://www.youtube.com/watch?v=lW47o2ss3Yg) 

+ [(Classic RAG) Vector search and state of the art retrieval for Generative AI apps](https://www.youtube.com/watch?v=lSzc1MJktAo)

### [**Docs**](#tab/docs)

+ [Retrieval augmented generation and indexes (Foundry)](/azure/ai-foundry/concepts/retrieval-augmented-generation)

+ [Try this agentic retrieval quickstart](search-get-started-agentic-retrieval.md) to walk through the new and recommended approach for RAG.

+ [Try this agentic retrieval tutorial](agentic-retrieval-how-to-create-pipeline.md) for a more comprehensive approach that includes an agent.

+ Interested in classic RAG? The [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md) repository has quickstarts and a tutorial.

+ [Review indexing concepts and strategies](search-what-is-an-index.md) to determine how you want to ingest and refresh data. Decide whether to use vector search, keyword search, or hybrid search. The kind of content you need to search over, and the type of queries you want to run, determines index design.

+ [Review creating queries](search-query-create.md) to learn more about search request syntax and requirements.

> [!NOTE]
> Some Azure AI Search features are intended for human interaction and aren't useful in a RAG pattern. Specifically, you can skip features like autocomplete and suggestions. Other features like facets and orderby might be useful, but are uncommon in a RAG scenario.

### [**Code**](#tab/demos)

+ [RAG chat app with Azure OpenAI and Azure AI Search (Python)](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md), updated for agentic retrieval.

+ [azure-search-classic-rag](https://github.com/Azure-Samples/azure-search-classic-rag/blob/main/README.md) in REST, Python, Java, .NET, JavaScript, and TypeScript.

+ [Classic RAG Time Journeys](https://github.com/microsoft/rag-time)

+ [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples)

### [**Templates**](#tab/templates)

[Use enterprise chat app templates](https://aka.ms/azai) to deploy Azure resources, code, and sample grounding data using fictitious health plan documents for Contoso and Northwind. This end-to-end solution gives you an operational chat app in as little as 15 minutes. Code for these templates is the **azure-search-openai-demo** featured in several presentations. The following links provide language-specific versions:

+ [.NET](https://aka.ms/azai/net)
+ [Python](https://aka.ms/azai/py)
+ [JavaScript](https://aka.ms/azai/js)
+ [Java](https://aka.ms/azai/javat)

---