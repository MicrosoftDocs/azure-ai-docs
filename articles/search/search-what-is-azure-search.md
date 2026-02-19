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
ms.date: 12/10/2025
---

# What is Azure AI Search?

Azure AI Search is a fully managed, cloud-hosted service that connects your data to AI. The service unifies access to enterprise and web content so agents and LLMs can use context, chat history, and multi-source signals to produce reliable, grounded answers.

Common use cases include *classic search* and modern retrieval-augmented generation (RAG) via *agentic retrieval*. This makes Azure AI Search suitable for both enterprise and consumer scenarios, whether you're adding search functionality to a website, app, agent, or chatbot.

When you create a search service, you unlock the following capabilities:

+ Two engines: [classic search](#what-is-classic-search) for single requests and [agentic retrieval](#what-is-agentic-retrieval) for parallel, iterative, LLM-assisted search.
+ [Full-text](search-lucene-query-architecture.md), [vector](vector-search-overview.md), [hybrid](hybrid-search-overview.md), and [multimodal](multimodal-search-overview.md) queries over local (indexed) and remote content.
+ AI enrichment to chunk, vectorize, and otherwise make raw content searchable.
+ Relevance tuning to improve intent matching and result quality.
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

+ Access data from Azure Blob Storage, Azure Cosmos DB, Microsoft SharePoint, Microsoft OneLake, and other supported data sources. Choose indexed or remote access based on your freshness, latency, and compliance needs.

+ Enrich and structure content at indexing or query time with skills that perform chunking, embedding, and LLM-assisted transformations.

+ Combine full-text search with vector search (hybrid search) to balance precision and recall.

+ Query content containing both text and images in a single multimodal pipeline.

+ Easily implement search-related features: relevance tuning, faceted navigation, filters (including geo-spatial search), synonym mapping, and autocomplete.

+ Provide enterprise security, access control, and compliance through Microsoft Entra, Azure Private Link, document-level access control, and role-based access.

+ Scale and operate in production with Azure reliability, monitoring and diagnostics (logs, metrics, and alerts), and REST API or SDK tooling for automation.

For more information about specific functionality, see [Features of Azure AI Search](search-features-list.md).

## What is classic search?

Classic search is an index-first retrieval model for predictable, low-latency queries. Each query targets a single, predefined search index and returns ranked documents in one request–response cycle. No LLM-assisted planning, iteration, or synthesis occurs during retrieval.

In this architecture, your search service sits between the data stores that contain your unprocessed content and your client app. The app is responsible for sending query requests to your search service and handling the response.

This architecture has two primary workloads:

#### [Indexing](#tab/indexing)

[Indexing](search-what-is-an-index.md) loads content into an index and makes it searchable. Internally, inbound text is tokenized and stored in inverted indexes, while inbound vectors are stored in vector indexes. Azure AI Search can only index JSON documents. You can use the [push method](search-what-is-data-import.md#pushing-data-to-an-index) to upload JSON documents directly or the [pull method](search-what-is-data-import.md#pulling-data-into-an-index) (indexer or logic app workflow) to retrieve and serialize data into JSON.

During indexing, you can use [AI enrichment](cognitive-search-concept-intro.md) to chunk text, generate vectors, and apply other transformations that create structure and content. Azure AI Search then serializes the enriched output into JSON documents and ingests them into the index.

#### [Querying](#tab/querying)

[Querying](search-query-overview.md) targets an index populated with searchable content. This step occurs when your client app sends a query request to your search service. In your code, set up a search client to handle requests for [full-text queries](search-query-create.md), [vector queries](vector-search-how-to-query.md), [hybrid queries](hybrid-search-how-to-query.md), [multimodal queries](multimodal-search-overview.md), fuzzy search, autocomplete, geo-search, and other query types.

---

:::image type="content" source="media/search-what-is-azure-search/classic-search-architecture.png" alt-text="Diagram of the Azure AI Search architecture for classic search." lightbox="media/search-what-is-azure-search/classic-search-architecture.png" :::

> [!NOTE]
> This diagram separates the indexing and query engines for clarity, but in Azure AI Search, they're the same component operating in read-write and read-only modes.

## What is agentic retrieval?

[Agentic retrieval](agentic-retrieval-overview.md) is a multi-query pipeline designed for complex agent-to-agent workflows. Each query targets a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that represents a complete domain of knowledge. Your agent references the knowledge base for *what* to ground on, while the knowledge base handles *how* to perform grounding.

A knowledge base consists of one or more [knowledge sources](agentic-knowledge-source-overview.md), an optional LLM for query planning and answer synthesis, and parameters that govern retrieval behavior. Each query undergoes planning, decomposition into focused subqueries, parallel retrieval from knowledge sources, semantic reranking, and results merging. The three-pronged response is optimized for agent consumption.

Under the hood, agentic retrieval builds on the classic search architecture by adding a context layer (knowledge base) that orchestrates multi-source retrieval. Knowledge sources can be indexed or remote: indexed sources use the same indexing and query engines as classic search, while remote sources bypass indexing and are queried live.

:::image type="content" source="media/search-what-is-azure-search/agentic-retrieval-architecture.png" alt-text="Diagram of the Azure AI Search architecture for agentic retrieval." lightbox="media/search-what-is-azure-search/agentic-retrieval-architecture.png" :::

## How they compare

Classic search and agentic retrieval are complementary modes of information retrieval. Both support [full-text](search-lucene-query-architecture.md), [vector](vector-search-overview.md), [hybrid](hybrid-search-overview.md), and [multimodal](multimodal-search-overview.md) search. However, they differ in how content is ingested and queried. The following table summarizes their key differences.

| Aspect | Classic search | Agentic retrieval |
|---|---|---|
| Search corpus | [Search index](search-what-is-an-index.md) | [Knowledge source](agentic-knowledge-source-overview.md) |
| Search target | One index defined by a schema | A knowledge base pointing to one or more knowledge sources |
| Query plan | No plan, just a request | LLM-assisted or user-provided plan |
| Query request | Search documents in an index | Retrieve from knowledge sources |
| Response | Flattened search results based on schema | LLM-formulated answer or raw source data, activity log, references |
| Region restrictions | No | Yes |
| Status | Generally available | Public preview|

## How to get started

You can access Azure AI Search through the Azure portal, [REST APIs](search-api-versions.md#rest-apis), and Azure SDKs for [.NET](search-api-versions.md#azure-sdk-for-net), [Java](search-api-versions.md#azure-sdk-for-java), [JavaScript](search-api-versions.md#azure-sdk-for-javascript), and [Python](search-api-versions.md#azure-sdk-for-python).

The portal is useful for service administration and content management, with tools for prototyping your knowledge bases, knowledge sources, indexes, indexers, skillsets, and data sources. REST APIs and SDKs are useful for production automation.

### Choose your path

Before you get started, use this checklist to make key decisions:

+ **Choose a search engine:** If you're not using an agent or chatbot, classic search can meet most app needs, with lower costs and complexity than LLM integration. If you want the benefits of a knowledge base and multiple knowledge sources without full LLM orchestration, consider agentic retrieval with the minimal [reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

+ **Choose a region:** If you're using agentic retrieval, choose a [supported region](search-region-support.md). For classic search, choose a region that offers the features and capacity you need.

+ **Choose an ingestion method for index-bound content:** If your content is in a [supported data source](search-indexer-overview.md#supported-data-sources), use the [pull method](search-what-is-data-import.md#pulling-data-into-an-index) to retrieve and serialize data into JSON. If you don't have a supported data source, or if your content and index must be synchronized in real time, the [push method](search-what-is-data-import.md#pushing-data-to-an-index) is your only option.

+ **Do you need vectors?** LLMs and agents don't require vectors. Only use them if you need similarity search or if you have content that can be homogenized into vectors. Azure AI Search offers [integrated vectorization](vector-search-integrated-vectorization.md) for this task.

+ **Do you need user-based permission inheritance?** Remote SharePoint is designed for this scenario, but you can also inherit user permissions attached to content in Azure Blob Storage or ADLS Gen2. For all other scenarios, you can use the [security filter](search-security-trimming-for-azure-search.md) workaround.

### Choose your learning resources

### [Quickstarts](#tab/quickstarts)

We maintain quickstarts that span various end-to-end search scenarios:

+ Quickstart: Agentic retrieval ([portal](get-started-portal-agentic-retrieval.md) or [programmatic](search-get-started-agentic-retrieval.md))
+ Quickstart: Full-text search ([portal](search-get-started-portal.md) or [programmatic](search-get-started-text.md))
+ Quickstart: Vector search ([portal](search-get-started-portal-import-vectors.md) or [programmatic](search-get-started-vector.md))

### [Samples](#tab/samples)

We maintain samples that use REST APIs and supported SDK programming languages:

+ [REST samples](/azure/search/samples-rest)
+ [Python samples](/azure/search/samples-python)
+ [C# samples](/azure/search/samples-dotnet)
+ [Java samples](/azure/search/samples-java)
+ [JavaScript/TypeScript samples](/azure/search/samples-javascript)
+ [Vector samples](https://github.com/Azure/azure-search-vector-samples)

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
