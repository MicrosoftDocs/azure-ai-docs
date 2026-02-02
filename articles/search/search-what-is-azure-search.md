---
title: Introduction to Azure AI Search
titleSuffix: Azure AI Search
description: Azure AI Search is an AI-powered information retrieval platform, helps developers build rich search experiences and generative AI apps that combine large language models with enterprise data.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: overview
ms.date: 07/18/2025
---

# What's Azure AI Search?

Azure AI Search is a scalable search infrastructure that indexes heterogeneous content and enables retrieval through APIs, applications, and AI agents. The platform provides native integrations with Azure's AI stack (OpenAI, AI Foundry, Machine Learning) and supports extensible architectures for third-party and open-source model integration.

The service handles both traditional search workloads and modern RAG (retrieval-augmented generation) patterns for conversational AI applications. This makes it suitable for enterprise search scenarios as well as AI-powered customer experiences that require dynamic content generation through chat completion models.

<!-- Azure AI Search ([formerly known as "Azure Cognitive Search"](whats-new.md#new-service-name)) is an enterprise-ready information retrieval system for your heterogeneous content that you ingest into a search index, and surface to users through queries and apps. It comes with a comprehensive set of advanced search technologies, built for high-performance applications at any scale.

Azure AI Search is the recommended retrieval system for building agent-to-agent (A2A) and RAG-based applications on Azure, with native LLM integrations between Azure OpenAI in Azure AI Foundry Models and Azure Machine Learning, with mechanisms for integrating third-party and open-source models and processes.

Azure AI Search can be used for both traditional search as well as modern information retrieval. Common use cases include catalog or document search, information discovery (data exploration), and  retrieval-augmented generation (RAG) for conversational search.  
 -->

<!-- Azure AI Search is a knowledge retrieval platform that consolidates and organizes information across different types of content. You add your content to a search index. Users, agents, and bots retrieve your content through queries and apps.
Indexing and query workloads support native integration with AI models from Azure OpenAI, Azure AI Foundry, and Azure Machine Learning. By leveraging an extensibility layer, you can connect workloads to third-party and open-source AI models and tools.

You can use Azure AI Search for regular search needs (like searching through catalogs or documents) or for AI-powered search that can have conversations with users and generate answers based on your content. -->

When you create a search service, you work with the following capabilities:

+ A search engine for [agentic search](agentic-retrieval-overview.md), [vector search](vector-search-overview.md), [full text](search-lucene-query-architecture.md), [multimodal search](multimodal-search-overview.md), or [hybrid search](hybrid-search-overview.md).
+ Content processing during indexing that can add structure and transformations.
+ Extensive query syntax for agents, vectors, text, hybrid, and multimodal queries.
+ Smart results through semantic ranking, scoring profiles, and parameterized queries.
+ Azure scale, security, and reach.
+ Azure integration at the data layer, machine learning layer, Azure AI services, and Azure OpenAI.

> [!div class="nextstepaction"]
> [Create a search service](search-create-service-portal.md)

Architecturally, a search service sits between the external data stores that contain your un-indexed data, and your client app that sends query requests to a search index and handles the response.

![Azure AI Search architecture](media/search-what-is-azure-search/azure-search.svg "Azure AI Search architecture")

On the indexing side, if your content is on Azure, you can use indexers and skillsets for automated and AI-enriched indexing. Or, create a logic app workflow for equivalent automation over an even broader set of supported data sources. 

On the retrieval side, your app can be an agent or tool, a bot, or any client that sends requests to a search index or knowledge agent.

Within Azure AI Search, the indexing and query engine is the same component operating in read-write and read-only modes, but we split it up in this diagram to indicate the type of work being performed.

## Inside a search service

On the search service itself, the two primary workloads are *indexing* and *querying*. 

+ [**Indexing**](search-what-is-an-index.md) is an intake process that loads content into your search service and makes it searchable. Internally, inbound text is processed into tokens and stored in inverted indexes, and inbound vectors are stored in vector indexes. The document format that Azure AI Search can index is JSON. You can upload JSON documents, or use an indexer or a logic app workflow to retrieve and serialize your data into JSON. 

  [AI enrichment](cognitive-search-concept-intro.md) is through a [skillset](cognitive-search-working-with-skillsets.md) that extends indexing with image and language models. If you have images or large unstructured text in source document, you can attach skills that chunk and vectorize content. If you have image content, you can use LLMs to summarize content, generate descriptions, or perform OCR and image analysis. Skills can also infer structure, translate text, and more. Output is text or vectors that can be serialized into JSON and ingested into a search index.

+ [**Querying**](search-query-overview.md) can happen once an index is populated with searchable content, when your client app sends query requests to a search service and handles responses. All query execution is over a search index that you control. In your code, set up a search client to handle query requests for [agentic queries](agentic-retrieval-how-to-retrieve.md), [vector queries](vector-search-how-to-query.md), [text search](search-query-create.md), [hybrid queries](hybrid-search-how-to-query.md), fuzzy search, autocomplete, geo-search, and others.

## Why use Azure AI Search?

Azure AI Search offloads indexing and query workloads onto a dedicated search service. It's well suited for the following application scenarios:

+ Use it for empowering agents and bots with grounding data based on your content.

+ Use it for traditional full text search and next-generation vector similarity search. Back your generative AI apps with information retrieval that leverages the strengths of both keyword and similarity search. Use both modalities to retrieve the most relevant results.

+ Consolidate heterogeneous content into a user-defined and populated search index composed of vectors and text. You maintain ownership and control over what's searchable.

+ Transform large undifferentiated text or image files, or application files stored in Azure Blob Storage or Azure Cosmos DB, into searchable chunks. This is achieved during indexing through [AI skills](cognitive-search-concept-intro.md) that add external processing from Azure AI.

+ [Integrate data chunking and vectorization](vector-search-integrated-vectorization.md) for generative AI and RAG apps.

+ Add linguistic or custom text analysis for keyword search. If you have non-English content, Azure AI Search supports both Lucene analyzers and Microsoft's natural language processors. You can also configure analyzers to achieve specialized processing of raw content, such as filtering out diacritics, or recognizing and preserving patterns in strings.

+ Easily implement search-related features: relevance tuning, faceted navigation, filters (including geo-spatial search), synonym mapping, and autocomplete.

+ [Apply granular access control](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/access-control-in-generative-ai-applications-with-azure/ba-p/3956408) at the document level.

For more information about specific functionality, see [Features of Azure AI Search](search-features-list.md)

## How to get started

Functionality is exposed through the Azure portal, simple [REST APIs](/rest/api/searchservice/), or Azure SDKs like the [Azure SDK for .NET](search-howto-dotnet-sdk.md). The Azure portal supports service administration and content management, with tools for prototyping and querying your indexes and skillsets. 

### Use the Azure portal

An end-to-end exploration of core search features can be accomplished in four steps:

1. [**Decide on a tier**](search-sku-tier.md) and region. One free search service is allowed per subscription. Most quickstarts can be completed on the free tier. For more capacity and capabilities, you need a [billable tier](https://azure.microsoft.com/pricing/details/search/).

1. [**Create a search service**](search-create-service-portal.md) in the Azure portal.

1. [**Start with Import data wizard**](search-get-started-portal.md). Choose a built-in sample or a supported data source to create, load, and query an index in minutes. 

1. [**Finish with Search Explorer**](search-explorer.md), using a portal client to query the search index you just created.

### Check out samples

We maintain an inventory of samples that use the REST APIs and the Azure SDK programming languages supported by Azure AI Search:

+ [REST samples](/azure/search/samples-rest)
+ [Python samples](/azure/search/samples-python)
+ [C# samples](/azure/search/samples-dotnet)
+ [Java samples](/azure/search/samples-java)
+ [JavaScript/TypeScript samples](/azure/search/samples-javascript)
+ [Vector samples](https://github.com/Azure/azure-search-vector-samples)

### Use APIs

Alternatively, you can create, load, and query a search index in atomic steps:

1. [**Create a search index**](search-what-is-an-index.md) using the Azure portal, [REST API](/rest/api/searchservice/indexes/create), [.NET SDK](search-howto-dotnet-sdk.md), or another SDK. The index schema defines the structure of searchable content.

1. [**Upload content**](search-what-is-data-import.md) using the ["push" model](tutorial-optimize-indexing-push-api.md) to push JSON documents from any source, or use the ["pull" model (indexers)](search-indexer-overview.md) if your source data is of a [supported type](search-indexer-overview.md#supported-data-sources).

1. [**Query an index**](search-query-overview.md) using [Search explorer](search-explorer.md) in the Azure portal, [REST API](search-get-started-text.md), [.NET SDK](/dotnet/api/azure.search.documents.searchclient.search), or another SDK.

### Use accelerators

Or, try solution accelerators:

+ [**Chat with your data solution accelerator**](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator) helps you create a custom RAG solution over your content.

+ [**Conversational Knowledge Mining solution accelerator**](https://github.com/microsoft/Customer-Service-Conversational-Insights-with-Azure-OpenAI-Services) helps you create an interactive solution to extract actionable insights from post-contact center transcripts.

+ [**Document Knowledge Mining accelerator**](https://github.com/microsoft/Document-Knowledge-Mining-Solution-Accelerator) helps you process and extract summaries, entities, and metadata from unstructured, multimodal documents.

+ [**Build your own copilot solution accelerator**](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator), leverages Azure OpenAI, Azure AI Search and Microsoft Fabric, to create custom copilot solutions.

<!--   + [Generic copilot](https://github.com/microsoft/Generic-Build-your-own-copilot-Solution-Accelerator) helps you build your own copilot to identify relevant documents, summarize unstructured information, and generate Word document templates using your own data.

  + [Client Advisor](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) all-in-one custom copilot empowers Client Advisor to harness the power of generative AI across both structured and unstructured data. Help our customers to optimize daily tasks and foster better interactions with more clients

  + [Research Assistant](https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator) helps build your own AI Assistant to identify relevant documents, summarize and categorize vast amounts of unstructured information, and accelerate the overall document review and content generation.
 -->
> [!TIP]
> For help with complex or custom solutions, [**contact a partner**](https://partner.microsoft.com/partnership/find-a-partner) with deep expertise in Azure AI Search technology.

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
