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

RAG implementations typically include an information retrieval component. The decision about which information retrieval system to use is critical because LLMs are constrained by the amount of token inputs they can accept, so you want the grounding data to be as relevant as possible. Criteria to consider include:

+ Ability to pull from a broad range of data sources and platforms.

+ Query capabilities that can target all of your data and return synthesized and highly relevant results, in the short-form formats necessary for meeting the token length requirements of LLM inputs.

+ Ease of integration with agents and chat apps, and other models and processes that are part of your application.

+ It's common to consolidate searchable data into separate physical data structures that are optimized for search. The search indexes on Azure AI Search are an example. If you're using indexes, you might want to verbalize, recognize or analyze images to get text-equivalent information in your index. More likely, you might want to chunk verbose source content so that it can be easily consumed, and vectorize that content if you want similarity search.

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

A RAG solution can be implemented on Azure AI Search using the original query execution architecture. With this approach, your application sends a single query request to Azure AI Search, the search engine processes the request, and returns search results to the caller. There's no side trip to an LLM for query planning or answer formulation. There's no query execution details in the response, and citations are built into the response only if you have fields in your index that provide a parent document name or page. This approach is faster and simpler with fewer components. Depending on your application requirements, it could be the best choice. 

A high-level summary of classic RAG pattern built on Azure AI Search looks like this:

+ Start with a user question or request (prompt).
+ Send it as a query request to Azure AI Search to find relevant information.
+ Return the top-ranked search results to an LLM.
+ Use the natural language understanding and reasoning capabilities of the LLM to generate a response to the initial prompt.

Azure AI Search provides inputs to the LLM prompt, but doesn't train the model. In a traditional RAG pattern, there's no extra training. The LLM is pretrained using public data, but it generates responses that are augmented by information from the retriever, in this case, Azure AI Search.

RAG patterns that include Azure AI Search have the elements indicated in the following illustration.

:::image type="content" source="media/retrieval-augmented-generation-overview/architecture-diagram.png" alt-text="Architecture diagram of information retrieval with search and ChatGPT." border="true" lightbox="media/retrieval-augmented-generation-overview/architecture-diagram.png":::

+ App UX (web app) for the user experience
+ App server or orchestrator (integration and coordination layer)
+ Azure AI Search (information retrieval system)
+ Azure OpenAI (LLM for generative AI)

The web app provides the user experience, providing the presentation, context, and user interaction. Questions or prompts from a user start here. Inputs pass through the integration layer, going first to information retrieval to get the search results, but also go to the LLM to set the context and intent. 

The app server or orchestrator is the integration code that coordinates the handoffs between information retrieval and the LLM. Common solutions include [Azure Semantic Kernel](/semantic-kernel/get-started/quick-start-guide) or [LangChain](https://python.langchain.com/docs/introduction/) to coordinate the workflow. [LangChain integrates with Azure AI Search](https://python.langchain.com/docs/integrations/retrievers/azure_ai_search/), making it easier to include Azure AI Search as a [retriever](https://python.langchain.com/docs/how_to/#retrievers) in your workflow. [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/vector_stores/llama-index-vector-stores-azureaisearch) and [Semantic Kernel](https://devblogs.microsoft.com/semantic-kernel/announcing-semantic-kernel-integration-with-azure-cognitive-search/) are other options.

The information retrieval system provides the searchable index, query logic, and the payload (query response). The search index can contain vectors or nonvector content. Although most samples and demos include vector fields, it's not a requirement. The query is executed using the existing search engine in Azure AI Search, which can handle keyword (or term) and vector queries. The index is created in advance, based on a schema you define, and loaded with your content that's sourced from files, databases, or storage.

The LLM receives the original prompt, plus the results from Azure AI Search. The LLM analyzes the results and formulates a response. If the LLM is ChatGPT, the user interaction might consist of multiple conversation turns. An Azure solution most likely uses Azure OpenAI, but there's no hard dependency on this specific service.

## Comparison of agentic retrieval and classic RAG

You can choose between two approaches for RAG workloads: new **agentic retrieval** for modern RAG (currently in preview), or the original query architecture for **classic RAG**. The following table highlights the key differences to help you choose.

| Characteristic | Agentic retrieval | Classic RAG |
|----------------|-------------------|-------------|
| Search corpus  | [A knowledge base](/rest/api/searchservice/knowledge-bases/create-or-update) that defines an entire search domain. It can include one or more search indexes (indexed content) and remote content from Bing and SharePoint.| [A search index](/rest/api/searchservice/indexes/create-or-update). |
| Query mechanism  | [Retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve) | [Search Documents](/rest/api/searchservice/documents/search-post) |
| Query composition | Multiple subqueries, as many as needed, composed by an LLM. | A single-shot query. |
| Query execution | Keyword, vector, hybrid in subqueries. <br>Optionally, call an LLM to return a formulated answer in the response. | Keyword, vector, hybrid in a single shot. |
| Query response | A long unified string in a multi-part format, consisting of a query activity plan, results, citations, source data. | Flattened rowset based on fields in the index. |
| LLM integration at query time | Query planning, embedded answer synthesis. | None. Application code sends results to an LLM. |

How queries execute is a primary differentiator between agentic retrieval and classic RAG. 

+ In a non-RAG pattern for regular search, queries make a round trip from a search client. The query is submitted, it executes on a search engine, and the response returned to the client application. The response, or search results, consist exclusively of the verbatim content found in your index. 

+ In a classic RAG pattern, queries and responses are coordinated between the search engine and the LLM. A user's question or query is forwarded to both the search engine and to the LLM as a prompt. The search results come back from the search engine and are redirected to an LLM. The response that makes it back to the user is generative AI, either a summation or answer from the LLM.

+ In a modern agentic retrieval RAG pattern, queries and responses integrate with LLMs for help with query planning and optional answer formulation. Query inputs can be richer, with chat history as well as the user's question. The LLM determines how to set up subqueries for the best coverage over your indexed content and it follows any retrieval instructions you've provided that guide which knowledge sources to use. The response includes not just search results, but the query execution details and source documents. You can optionally include answer formulation, which in other patterns occurs outside of the query pipeline.

## Searchable content in Azure AI Search

With agentic retrieval, you're not strictly limited to searching indexed content. Remote knowledge sources for Bing and SharePoint are accessed through direct queries against that content using APIs that are native to the technology. Otherwise, all searchable content is stored in a search index that's hosted on your search service. 

A search index is designed for fast queries with millisecond response times, so its internal data structures exist to support that objective. To that end, a search index stores *indexed content*, and not whole content files like entire PDFs or images. Internally, the data structures include inverted indexes of [tokenized text](https://lucene.apache.org/core/7_5_0/test-framework/org/apache/lucene/analysis/Token.html), vector indexes for embeddings, and unaltered plain text for cases where verbatim matching is required (for example, in filters, fuzzy search, regular expression queries).

When you set up the data for your RAG solution, you use the features that create and load an index in Azure AI Search. For agentic retrieval, a [knowledge source](agentic-knowledge-source-overview.md) provides this capability. 

An index includes fields that duplicate or represent your external source content. An index field might be simple transference (a title or description in a source document becomes a title or description in a search index), or a field might contain the output of an external process, such as vectorization or skill processing that generates a representation or text description of an image.

Since you probably know what kind of content you want to search over, consider the indexing features that are applicable to each content type:

| Content type | Indexed as | Features |
|--------------|------------|----------|
| Plain text | Tokens, raw text | [Indexers](search-indexer-overview.md) and [knowledge sources](agentic-knowledge-source-overview.md). Also, [analyzers](search-analyzers.md) and [normalizers](search-normalizers.md) to modify text in flight. [Synonym maps](search-synonyms.md) for query expansion. |
| Text (vectorized)<sup>1</sup> | [Vectors](vector-search-how-to-create-index.md) | Chunking and vectorization via indexers  or external tools |
| Images<sup>2</sup | Tokens, raw text | OCR and Image Analysis [skills](cognitive-search-working-with-skillsets.md) (indexer required) |
| Multimodal | Vectors | [Azure Vision multimodal](/azure/ai-services/computer-vision/how-to/image-retrieval) or [OpenAI CLIP](https://github.com/openai/CLIP/blob/main/README.md) for unified embedding space. |

 <sup>1</sup> Azure AI Search provides [integrated data chunking and vectorization](vector-search-integrated-vectorization.md), but you must take a dependency on indexers and skillsets. For code samples, see [azure-search-vectors-sample repo](https://github.com/Azure/azure-search-vector-samples).

<sup>2</sup> Through skills, image descriptions are converted to searchable text and added to the index. The images themselves are not stored in the index. Skills are also used for integrated data chunking and embedding. 

Vectors provide the best accommodation for dissimilar content (multiple file formats and languages) because content is expressed universally in mathematic representations. Vectors also support similarity search: matching on the coordinates that are most similar to the vector query. Compared to keyword search (or term search) that matches on tokenized terms, similarity search is more nuanced. It's a better choice if there's ambiguity or interpretation requirements in the content or in queries.

## Maximize relevance and recall

When you're working with complex processes, a large amount of data, and expectations for millisecond responses, it's critical that each step adds value and improves the quality of the end result. On the information retrieval side, *relevance tuning* is an activity that improves the quality of the results sent to the LLM. Only the most relevant or the most similar matching documents should be included in results.

Whether you use agentic retrieval or classic RAG, here's how you maximize relevance and recall:

+ [Hybrid queries](hybrid-search-overview.md) that combine keyword (nonvector) search and vector search give you maximum recall when the inputs are the same. In a hybrid query, if you double down on the same input, a text string and its vector equivalent generate parallel queries for keywords and similarity search, returning the most relevant matches from each query type in a unified result set.

+ Hybrid queries are expansive. You can run similarity search over chunked vector content, and keyword search over names, all in the same request.

+ Extra relevance tuning is enabled by:

  + [Scoring profiles](index-add-scoring-profiles.md) that boost the search score if matches are found in a specific search field or on other criteria.

  + [Semantic ranker](semantic-ranking.md) that re-ranks an initial results set, using semantic models from Bing to reorder results for a better semantic fit to the original query. Semantic ranker is integrated into agentic retrieval and recommended for classic RAG.

  + Query parameters for fine-tuning. You can [boost the importance of vector queries](vector-search-how-to-query.md#vector-weighting) or [adjust the amount of BM25-ranked results](hybrid-search-how-to-query.md#set-maxtextrecallsize-and-countandfacetmode) in a hybrid query response. You can also [set minimum thresholds to exclude low scoring results](vector-search-how-to-query.md#set-thresholds-to-exclude-low-scoring-results-preview) from a vector query.

In comparison and benchmark testing, hybrid queries with text and vector fields, supplemented with semantic ranking, produce the most relevant results.

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

### [**Accelerators**](#tab/accelerators)

+ [Chat with your data solution accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator)

+ [Conversational Knowledge Mining solution accelerator](https://github.com/microsoft/Customer-Service-Conversational-Insights-with-Azure-OpenAI-Services)

+ [Document Knowledge Mining accelerator](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator)

+ [Build your own copilot solution accelerator](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator)

  + [Client Advisor](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator)

  + [Research Assistant](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator)

  + [Generic copilot](https://github.com/microsoft/Generic-Build-your-own-copilot-Solution-Accelerator)

---