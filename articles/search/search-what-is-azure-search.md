---
title: Introduction to Azure AI Search
description: Learn how Azure AI Search helps you build rich search experiences and generative AI apps. Combine LLMs with enterprise data using classic search and agentic retrieval.
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: overview
ms.date: 06/02/2026
---

# What is Azure AI Search?

Azure AI Search is a fully managed, cloud-hosted service that connects your data to AI. The service unifies access to enterprise and web content so agents and LLMs can use context, chat history, and multi-source signals to produce reliable, grounded answers.

Azure AI Search is available in two pricing models:

- **Dedicated**: Provisioned capacity with fixed pricing. You select a service tier and you're billed per hour based on Search Units (SUs). Best for steady, predictable, high-utilization workloads.

- **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. Best for infrequent, bursty, or highly variable workloads.

[!INCLUDE [Serverless preview](./includes/previews/preview-serverless.md)]

Common use cases include *classic search* and retrieval-augmented generation (RAG) using *agentic retrieval*, where the service orchestrates query planning, retrieval, and response construction. These capabilities support scenarios ranging from traditional search experiences to AI-powered agents and chat applications suitable for both enterprise and consumer scenarios.

When you create a search service, the following capabilities are included:

+ Two engines: [classic search](#what-is-classic-search) for single requests and [agentic retrieval](#what-is-agentic-retrieval) for parallel, iterative, LLM-assisted search.
+ [Full-text](search-lucene-query-architecture.md), [vector](vector-search-overview.md), [hybrid](hybrid-search-overview.md), and [multimodal](multimodal-search-overview.md) queries over local (indexed) and remote content.
+ AI enrichment to chunk, vectorize, and otherwise make raw content searchable.
+ Relevance tuning to improve intent matching and result quality.
+ Azure scale, security, monitoring, and compliance.
+ Azure integrations with supported data platforms, Azure OpenAI, and Microsoft Foundry.

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)

## Why use Azure AI Search?

+ Ground agents and chatbots in proprietary, enterprise, or web data for accurate, context-aware responses.

+ Access data from Azure Blob Storage, Azure Cosmos DB, Microsoft SharePoint, Microsoft OneLake, and other supported data sources. Choose indexed or remote access based on your freshness, latency, and compliance needs.

+ Enrich and structure content at indexing or query time with skills that perform chunking, embedding, and LLM-assisted transformations.

+ Combine full-text search with vector search (hybrid search) to balance precision and recall.

+ Query content containing both text and images in a single multimodal pipeline.

+ Easily implement search-related features: relevance tuning, faceted navigation, filters (including geo-spatial search), synonym mapping, and autocomplete.

+ Provide enterprise security, access control, and compliance through Microsoft Entra, Azure Private Link, document-level access control, and role-based access.

+ Scale and operate in production with Azure reliability, monitoring and diagnostics (logs, metrics, and alerts), and REST API or SDK tooling for automation.

> [!NOTE]
> In the Serverless pricing model, scaling is handled automatically by the service. Unlike Dedicated models where you configure replicas and partitions, Serverless uses consumption-based scaling and service-level limits to manage capacity. For more information, see [Optimize costs with the Serverless pricing model](./serverless-cost-optimization.md).

For more information about specific functionality, see [Features of Azure AI Search](search-features-list.md).

## What is classic search?

Classic search is an index-first retrieval model for predictable, low-latency queries. Each query targets a single, predefined search index and returns ranked documents in one request–response cycle. No LLM-assisted planning, iteration, or synthesis occurs during retrieval.

In this architecture, your search service sits between the data stores that contain your unprocessed content and your client app. The app is responsible for sending query requests to your search service and handling the response.

This architecture has two primary workloads:

### [Indexing](#tab/indexing)

[Indexing](search-what-is-an-index.md) loads content into an index and makes it searchable. Internally, inbound text is tokenized and stored in inverted indexes, while inbound vectors are stored in vector indexes. Azure AI Search can only index JSON documents. You can use the [push method](search-what-is-data-import.md#pushing-data-to-an-index) to upload JSON documents directly or the [pull method](search-what-is-data-import.md#pulling-data-into-an-index) (indexer or logic app workflow) to retrieve and serialize data into JSON.

During indexing, you can use [AI enrichment](cognitive-search-concept-intro.md) to chunk text, generate vectors, and apply other transformations that create structure and content. Azure AI Search then serializes the enriched output into JSON documents and ingests them into the index.

### [Querying](#tab/querying)

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
| Status | Generally available | Generally available, with some capabilities in preview |
| Dedicated pricing model support | Yes | Yes |
| Serverless pricing model support | Yes | Yes |

## How to get started

You can access Azure AI Search through the Azure portal, [REST APIs](search-api-versions.md#rest-apis), and Azure SDKs for [.NET](search-api-versions.md#azure-sdk-for-net), [Java](search-api-versions.md#azure-sdk-for-java), [JavaScript](search-api-versions.md#azure-sdk-for-javascript), and [Python](search-api-versions.md#azure-sdk-for-python).

The portal is useful for service administration and content management, with tools for prototyping your knowledge bases, knowledge sources, indexes, indexers, skillsets, and data sources. REST APIs and SDKs are useful for production automation.

### Choose your path

Before you get started, use this checklist to make key decisions:

+ **Choose a pricing model**: Select between the **Dedicated** or **Serverless** pricing model. See [Choose a pricing model and service tier](./search-sku-tier.md) for help with choosing the model that best fits your needs.

+ **Choose how you want to retrieve data:** You can query directly from a search index for predictable, low-latency results, or use agentic retrieval to query across multiple indexes through a knowledge base. If you’re building a traditional app without an agent or chatbot, direct index queries can meet most needs with lower cost and complexity. If you want to work across multiple knowledge sources or support more advanced scenarios, consider agentic retrieval with minimal [reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

+ **Choose a region:** If you're using agentic retrieval, choose a [supported region](search-region-support.md). For classic search, choose a region that offers the features and capacity you need.

+ **Choose an ingestion method for index-bound content:** If your content is in a [supported data source](search-indexer-overview.md#supported-data-sources), use the [pull method](search-what-is-data-import.md#pulling-data-into-an-index) to retrieve and serialize data into JSON. If you don't have a supported data source, or if your content and index must be synchronized in real time, the [push method](search-what-is-data-import.md#pushing-data-to-an-index) is your only option.

+ **Do you need vectors?** LLMs and agents don't require vectors. Only use them if you need similarity search or if you have content that can be homogenized into vectors. Azure AI Search offers [integrated vectorization](vector-search-integrated-vectorization.md) for this task.

+ **Do you need user-based permission inheritance?** Remote SharePoint is designed for this scenario, but you can also inherit user permissions attached to content in Azure Blob Storage or ADLS Gen2. For all other scenarios, you can use the [security filter](search-security-trimming-for-azure-search.md) workaround.

### Choose your learning resources

These quickstarts and samples are available to help you get started.

### [Quickstarts](#tab/quickstarts)

+ Quickstart: Agentic retrieval ([portal](get-started-portal-agentic-retrieval.md) or [programmatic](search-get-started-agentic-retrieval.md))
+ Quickstart: Full-text search ([portal](search-get-started-portal.md) or [programmatic](search-get-started-text.md))
+ Quickstart: Vector search ([portal](search-get-started-portal-import-vectors.md) or [programmatic](search-get-started-vector.md))

### [Samples](#tab/samples)

Microsoft maintains samples that use REST APIs and supported SDK programming languages:

+ [REST samples](/azure/search/samples-rest)
+ [Python samples](/azure/search/samples-python)
+ [C# samples](/azure/search/samples-dotnet)
+ [Java samples](/azure/search/samples-java)
+ [JavaScript/TypeScript samples](/azure/search/samples-javascript)
+ [Vector samples](https://github.com/Azure/azure-search-vector-samples)

---

> [!TIP]
> For help with complex or custom solutions, [contact a partner](https://partner.microsoft.com/partnership/find-a-partner) with deep expertise in Azure AI Search.
