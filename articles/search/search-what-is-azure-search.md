---
title: Introduction to Azure AI Search
titleSuffix: Azure AI Search
description: Azure AI Search is an AI-powered information retrieval platform that helps developers build rich search experiences and generative AI apps that combine large language models (LLMs) with enterprise or web data.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: overview
ms.date: 12/02/2025
---

# What is Azure AI Search?

Azure AI Search is a fully managed, cloud-hosted service that provides APIs for indexing, enriching, and retrieving heterogeneous content. Use it to create rich search experiences at production scale while offloading operational overhead to the Azure platform.

Common use cases include traditional search and modern retrieval-augmented generation (RAG) for conversational AI. This makes Azure AI Search suitable for both enterprise and consumer scenarios, whether you're adding search functionality to a website, app, agent, or chatbot.

When you create a search service, you unlock the following capabilities:

+ A search engine for [agentic search](agentic-retrieval-overview.md), [full-text search](search-lucene-query-architecture.md), [vector search](vector-search-overview.md), [hybrid search](hybrid-search-overview.md), and [multimodal search](multimodal-search-overview.md).
+ AI enrichment during indexing to process and transform content that's otherwise unsearchable.
+ Extensive query syntax and smart results through semantic ranking and scoring profiles.
+ Azure scale, security, monitoring, and compliance.
+ Azure integrations with supported data platforms, Azure OpenAI, and Microsoft Foundry.

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)

<!-- Azure AI Search ([formerly known as "Azure Cognitive Search"](whats-new.md#new-service-name)) is an enterprise-ready information retrieval system for your heterogeneous content that you ingest into a search index, and surface to users through queries and apps. It comes with a comprehensive set of advanced search technologies, built for high-performance applications at any scale.

Azure AI Search is the recommended retrieval system for building agent-to-agent (A2A) and RAG-based applications on Azure, with native LLM integrations between Azure OpenAI in Foundry Models and Azure Machine Learning, with mechanisms for integrating third-party and open-source models and processes.

Azure AI Search can be used for both traditional search as well as modern information retrieval. Common use cases include catalog or document search, information discovery (data exploration), and  retrieval-augmented generation (RAG) for conversational search.  
 -->

<!-- Azure AI Search is a knowledge retrieval platform that consolidates and organizes information across different types of content. You add your content to a search index. Users, agents, and bots retrieve your content through queries and apps.
Indexing and query workloads support native integration with AI models from Azure OpenAI, Microsoft Foundry, and Azure Machine Learning. By leveraging an extensibility layer, you can connect workloads to third-party and open-source AI models and tools.

You can use Azure AI Search for regular search needs (like searching through catalogs or documents) or for AI-powered search that can have conversations with users and generate answers based on your content. -->

## Why use Azure AI Search?

+ Ground agents and chatbots in proprietary, enterprise, or web data for accurate, context-aware responses.

+ Ingest data from Azure Blob Storage, Azure Cosmos DB, Microsoft OneLake, and other supported data sources. You control the index schema and what's searchable.

+ Enrich and structure content during indexing with skillsets, which offer chunking, optical character recognition (OCR), translation, summarization, metadata extraction, vector generation, and more.

+ Use integrated vectorization to streamline the process of converting text into embeddings for similarity search.

+ Combine traditional full-text search with next-generation vector search (known as hybrid search) to balance precision and semantic recall for both classic and agentic search.

+ Tune relevance with semantic ranking, scoring profiles, synonyms, faceting, autocomplete, fuzzy matching, and filters (including geo-spatial).

+ Provide enterprise security, access control, and compliance through Microsoft Entra, Azure Private Link, document-level access control, and role-based access control (RBAC).

+ Scale and operate in production with Azure reliability, autoscaling, monitoring and diagnostics (logs, metrics, and alerts), and REST API or SDK tooling for automation.

For more information about specific functionality, see [Features of Azure AI Search](search-features-list.md).

## How it works

Architecturally, a search service sits between raw, unprocessed content and a downstream client app that consumes and outputs search results.

The following diagram illustrates how your content, search service, and client app interact for classic search. In Azure AI Search, the indexing and query engines are the same component operating in both read-write and read-only modes. However, our diagram separates the engines to indicate the type of work being performed.

:::image type="content" source="media/search-what-is-azure-search/azure-search.svg" alt-text="Diagram of Azure AI Search architecture." lightbox="media/search-what-is-azure-search/azure-search.svg" :::

<!--
On the indexing side, your content can be ingested into a *search index* through an indexer, push API, or logic app workflow. For remote *knowledge sources* that provide real-time data to knowledge bases, the search service can bypass indexing and directly query the source at runtime.

On the retrieval side, your client can be an agent, tool, or any app that sends requests to a search index or knowledge base and receives ranked, post-processed results.
-->

### Primary workflows

Azure AI Search supports two primary workflows: classic search and agentic search.

Classic search queries an index using keyword, vector, hybrid, or multimodal techniques. Agentic search builds on those capabilities for RAG: it orchestrates retrieval across indexed and remote knowledge sources, plans and executes subqueries, and produces grounded answers. The output is intended for consumption by your agent.

#### [**Classic search**](#tab/classic)

If you're building a traditional search experience, you might follow these steps:

1. **Define goals and requirements:** Inventory your content types and expected query patterns, such as [keyword](search-lucene-query-architecture.md), [vector](vector-search-overview.md), [hybrid](hybrid-search-overview.md), [multimodal](multimodal-search-overview.md), [fuzzy](search-query-fuzzy.md), autocomplete, and geo-search. Decide on freshness, SLAs, and document‑level access needs to guide indexing and authorization choices.

1. **Create an index:** Map your content model to JSON fields within a [search index](search-what-is-an-index.md). Set data types and attributes (searchable, sortable, filterable, facetable, retrievable) to control field behavior. If needed, include vector fields for embeddings.

1. **Import content:** Choose the [push method](search-what-is-data-import.md#pushing-data-to-an-index) (upload JSON documents directly) or [pull method](search-what-is-data-import.md#pulling-data-into-an-index) (use an indexer or logic app workflow to extract data from external sources) to populate the index.

1. **Add AI enrichment:** Use a [skillset](cognitive-search-working-with-skillsets.md) to chunk text, perform OCR on images, generate embeddings, extract metadata, summarize content, detect layout, translate text, and more. Store enriched outputs in appropriate index fields.

1. **Add relevance and ranking:** Create [scoring profiles](index-add-scoring-profiles.md), [synonyms](search-synonyms.md), and [analyzers](search-analyzers.md) to influence lexical ranking. Use [semantic ranking](semantic-search-overview.md) to promote relevant results that match user intent.

1. **Implement client-side query handling:** Expose API endpoints or SDK client methods that construct and submit queries to the search service.

1. **Enforce security:** Encrypt data [in transit](search-security-overview.md#data-in-transit), [in use](search-security-overview.md#data-in-use), and [at rest](search-security-overview.md#data-at-rest). Use [RBAC](search-security-rbac.md) to avoid key leakage from client apps. Apply [document-level access control](search-document-level-access-overview.md).

1. **Monitor and operate:** Analyze [query and indexing performance](search-performance-analysis.md) to identify bottlenecks and optimize resource usage. Configure [diagnostic logs](search-monitor-enable-logging.md) for auditing and troubleshooting.

#### [**Agentic search**](#tab/agentic)

If you're building a modern RAG experience, you might follow these steps:

1. **Define goals and requirements:** Identify your goal for [agentic retrieval](agentic-retrieval-overview.md), such as document retrieval or multi-turn conversational support. Determine which of your content can be indexed versus accessed remotely to meet performance, freshness, and security requirements.

1. **Create knowledge sources:** Create one or more [knowledge sources](agentic-knowledge-source-overview.md) that represent searchable content. Use indexed sources for low‑latency queries, document‑level permissions, and ingestion-time enrichment and scheduling. Use remote sources for freshness or data volume constraints.

1. **Create a knowledge base:** Create a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that links your knowledge sources and an optional LLM to drive query planning, query execution, and result synthesis. Choose whether the system returns [raw grounding data](agentic-retrieval-how-to-retrieve.md#review-the-extracted-response) or [synthesized answers](agentic-retrieval-how-to-answer-synthesis.md) that cite retrieved content.

1. **Implement client-side query handling:** [Retrieve data](agentic-retrieval-how-to-retrieve.md) from the knowledge base by passing user queries and context. Your agent is responsible for routing requests, maintaining the conversation state, rendering or synthesizing results, and enforcing client-side access control.

1. **Enforce security:** Use [RBAC](search-security-rbac.md) to avoid key leakage from client apps. Apply [document-level access control](search-document-level-access-overview.md) to indexed knowledge sources.

1. **Monitor and operate:** Review the [activity array](agentic-retrieval-how-to-retrieve.md#review-the-activity-array) and [references array](agentic-retrieval-how-to-retrieve.md#review-the-references-array) for visibility into billing and grounding quality. Adjust the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) to control LLM invocations. For indexed sources, iterate on chunking, embedding model parameters, and field selection to improve precision.

---

<!--
### Indexing and querying

On the search service itself, there are two primary workloads:

#### [Indexing](#tab/indexing)

[Indexing](search-what-is-an-index.md) loads content into your search service and makes it searchable. Internally, inbound text is tokenized and stored in inverted indexes, while inbound vectors are stored in vector indexes. Azure AI Search can only index JSON documents. You can use the push API to upload JSON documents directly, or you can use an indexer or logic app workflow to retrieve and serialize your data into JSON.

For [agentic retrieval](agentic-retrieval-overview.md), Azure AI Search can ingest external data into a search index or query remote sources at runtime. Indexed sources are best when you need predictable, low‑latency responses, relevance tuning, or document‑level access control. Remote sources are best when freshness, policy, or data volume prevents indexing. Many agentic retrieval solutions use both: index core content or embeddings for speed and fall back to remote sources for real-time data.

[AI enrichment](cognitive-search-concept-intro.md) extends indexing by using language and vision models to transform raw content. Enrichment is configured through a *skillset* that outputs text or vectors, which are serialized into JSON and ingested into a search index. Common enrichment tasks include:

+ Chunk large unstructured text and generate embeddings for vector indexing.
+ Extract text from images via OCR, summarize or describe images with LLMs, and infer structure or metadata.
+ Translate text and extract entities, key phrases, and sentiment.

### [Querying](#tab/querying)

[Querying](search-query-overview.md) targets an index populated with searchable content or a knowledge base that points to configured knowledge sources. This step occurs when your client app sends query requests to the search service and handles responses. In your code, set up a search client to handle requests for [agentic queries](agentic-retrieval-how-to-retrieve.md), [vector queries](vector-search-how-to-query.md), [full-text queries](search-query-create.md), [hybrid queries](hybrid-search-how-to-query.md), fuzzy search, autocomplete, geo-search, and other query types.

---
-->

## How to get started

You can access Azure AI Search through the Azure portal, [REST APIs](search-api-versions.md#rest-apis), and Azure SDKs for [.NET](search-api-versions.md#azure-sdk-for-net), [Java](search-api-versions.md#azure-sdk-for-java), [JavaScript](search-api-versions.md#azure-sdk-for-javascript), and [Python](search-api-versions.md#azure-sdk-for-python).

The portal is useful for service administration and content management, with tools for prototyping your knowledge bases, knowledge sources, indexes, indexers, skillsets, and data sources. REST APIs and SDKs are useful for production automation.

### [**Quickstarts**](#tab/quickstarts)

We maintain quickstarts that span various scenarios to help you get started with Azure AI Search:

+ Quickstart: Agentic search ([portal](get-started-portal-agentic-retrieval.md) or [programmatic](search-get-started-agentic-retrieval.md))
+ Quickstart: Full-text search ([portal](search-get-started-portal.md) or [programmatic](search-get-started-text.md))
+ Quickstart: Vector search ([portal](search-get-started-portal-import-vectors.md) or [programmatic](search-get-started-vector.md))

### [**Samples**](#tab/samples)

We maintain samples that use REST APIs and supported SDK programming languages:

+ [REST samples](/azure/search/samples-rest)
+ [Python samples](/azure/search/samples-python)
+ [C# samples](/azure/search/samples-dotnet)
+ [Java samples](/azure/search/samples-java)
+ [JavaScript/TypeScript samples](/azure/search/samples-javascript)
+ [Vector samples](https://github.com/Azure/azure-search-vector-samples)

### [**Accelerators**](#tab/accelerators)

Try solution accelerators for common RAG and conversational scenarios:

+ [Chat with your data solution accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator) helps you create a custom RAG solution over your content.

+ [Conversational Knowledge Mining solution accelerator](https://github.com/microsoft/Customer-Service-Conversational-Insights-with-Azure-OpenAI-Services) helps you create an interactive solution to extract actionable insights from post-contact center transcripts.

+ [Document Knowledge Mining accelerator](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator) helps you process and extract summaries, entities, and metadata from unstructured, multimodal documents.

+ [Build your own copilot solution accelerator](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) uses Azure OpenAI, Azure AI Search, and Microsoft Fabric to create custom copilot solutions.

---

> [!TIP]
> For help with complex or custom solutions, [contact a partner](https://partner.microsoft.com/partnership/find-a-partner) with deep expertise in Azure AI Search.

<!--
### [**Azure portal**](#tab/portal)

For end-to-end exploration of core features:

1. [**Choose a pricing tier**](search-sku-tier.md) and region. One free search service is allowed per subscription, and most quickstarts support the free tier. For more capacity and capabilities, you need a [billable tier](https://azure.microsoft.com/pricing/details/search/).

1. [**Create a search service**](search-create-service-portal.md) in the Azure portal.

1. [**Start with the Import data wizard**](search-get-started-portal.md). Choose a built-in sample or a supported data source to create, load, and query an index in minutes.

1. [**Finish with Search Explorer**](search-explorer.md). Use a portal client to query the search index you just created.

### [**REST APIs and SDKs**](#tab/rest-apis-sdks)

To create, load, and query a search index programmatically:

1. [**Create a search index**](search-what-is-an-index.md) using the Azure portal, [REST API](/rest/api/searchservice/indexes/create), [.NET SDK](search-howto-dotnet-sdk.md), or another SDK. The index schema defines the structure of searchable content.

1. [**Upload content**](search-what-is-data-import.md) using the [push model](tutorial-optimize-indexing-push-api.md) to push JSON documents from any source or the [pull model (indexers)](search-indexer-overview.md) if your source data is a [supported type](search-indexer-overview.md#supported-data-sources).

1. [**Query an index**](search-query-overview.md) using [Search explorer](search-explorer.md) in the Azure portal, [REST API](search-get-started-text.md), [.NET SDK](/dotnet/api/azure.search.documents.searchclient.search), or another SDK.
-->

<!--   + [Generic copilot](https://github.com/microsoft/Generic-Build-your-own-copilot-Solution-Accelerator) helps you build your own copilot to identify relevant documents, summarize unstructured information, and generate Word document templates using your own data.

  + [Client Advisor](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) all-in-one custom copilot empowers Client Advisor to harness the power of generative AI across both structured and unstructured data. Help our customers to optimize daily tasks and foster better interactions with more clients

  + [Research Assistant](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) helps build your own AI Assistant to identify relevant documents, summarize and categorize vast amounts of unstructured information, and accelerate the overall document review and content generation.
 -->

<!-- ## Compare search options

Customers often ask how Azure AI Search compares with other search-related solutions. The following table summarizes key differences.

| Compared to | Key differences |
|-------------|-----------------|
| Microsoft Search | [Microsoft Search](/microsoftsearch/overview-microsoft-search) is for Microsoft 365 authenticated users who need to query over content in SharePoint. Azure AI Search pulls in content across Azure and any JSON dataset. |
|Bing | [Bing APIs](/bing/search-apis/bing-web-search/bing-api-comparison) query the indexes on Bing.com for matching terms. Azure AI Search searches over indexes populated with your content. You control data ingestion and the schema. |
|Database search | Azure SQL has [full text search](/sql/relational-databases/search/full-text-search) and [vector search](/samples/azure-samples/azure-sql-db-openai/azure-sql-db-openai/). Azure Cosmos DB also has [text search](/azure/cosmos-db/nosql/query/) and [vector search](/azure/cosmos-db/vector-database). Azure AI Search becomes an attractive alternative when you need features like relevance tuning, or content from heterogeneous sources. Resource utilization is another inflection point. Indexing and queries are computationally intensive. Offloading search from the DBMS preserves system resources for transaction processing. |
|Dedicated search solution | Assuming you've decided on dedicated search with full spectrum functionality, a final categorical comparison is between search technologies. Among cloud providers, Azure AI Search is strongest for vector, keyword, and hybrid workloads over content on Azure, for apps that rely primarily on search for both information retrieval and content navigation. |

Key strengths include:

+ Support for vector and nonvector (text) indexing and queries. With vector similarity search, you can find information that’s semantically similar to search queries, even if the search terms aren’t exact matches. Use hybrid search to combine the strengths of keyword and vector search.
+ Ranking and relevance tuning through semantic ranking and scoring profiles. You can also leverage query syntax that supports term boosting and field prioritization.
+ Azure data integration (crawlers) at the indexing layer.
+ Azure AI integration for transformations that make content text and vector searchable.
+ Microsoft Entra security for trusted connections, and Azure Private Link for private connections in no-internet scenarios.
+ [Full search experience](search-features-list.md): Linguistic and custom text analysis in 56 languages. Faceting, autocomplete queries and suggested results, and synonyms.
+ Azure scale, reliability, and global reach. -->
