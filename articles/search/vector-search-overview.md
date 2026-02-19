---
title: Vector Search
titleSuffix: Azure AI Search
description: Describes concepts, scenarios, and availability of vector capabilities in Azure AI Search.
author: robertklee
ms.author: robertlee
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 01/15/2026
ai-usage: ai-assisted
---

# Vector search in Azure AI Search

Vector search is an information retrieval approach that supports indexing and querying over numeric representations of content. Because the content is numeric rather than plain text, matching is based on vectors that are most similar to the query vector. This approach enables matching across:

+ Semantic or conceptual likeness. For example, "dog" and "canine" are conceptually similar but linguistically distinct.
+ Multilingual content, such as "dog" in English and "hund" in German.
+ Multiple content types, such as "dog" in plain text and an image of a dog.

This article provides an overview of vector search in Azure AI Search, including supported scenarios, availability, and integration with other Azure services.

> [!TIP]
> Want to get started right away? Follow these steps:
>
> 1. [Provide embeddings](vector-search-how-to-generate-embeddings.md) for your index or [generate embeddings](vector-search-integrated-vectorization.md) in an indexer pipeline.
> 1. [Create a vector index](vector-search-how-to-create-index.md).
> 1. [Run vector queries](vector-search-how-to-query.md).

## What scenarios can vector search support?

Vector search supports the following scenarios:

+ **Similarity search**. Encode text using embedding models or open-source models, such as OpenAI embeddings or SBERT, respectively. You then retrieve documents using queries that are also encoded as vectors.

+ **[Hybrid search](hybrid-search-overview.md)**. Azure AI Search defines hybrid search as the execution of vector search and [keyword search](search-lucene-query-architecture.md) in the same request. Vector support is implemented at the field level. If an index contains vector and nonvector fields, you can write a query that targets both. The queries execute in parallel, and the results are merged into a single response and ranked accordingly.

+ **[Multimodal search](multimodal-search-overview.md)**. Encode text and images using multimodal embeddings, such as [OpenAI CLIP](https://github.com/openai/CLIP) or [GPT-4 Turbo with Vision](/azure/ai-services/openai/whats-new#gpt-4-turbo-with-vision-now-available) in Azure OpenAI, and then query an embedding space composed of vectors from both content types.

+ **Multilingual search**. Azure AI Search is designed for extensibility. If you have embedding models and chat models trained in multiple languages, you can call them through custom or built-in skills on the indexing side or vectorizers on the query side. For more control over text translation, use the [multi-language capabilities](search-language-support.md) supported by Azure AI Search for nonvector content in hybrid search scenarios.

+ **Filtered vector search**. A query request can include a vector query and a [filter expression](search-filters.md). Filters apply to text and numeric fields. They're useful for metadata filters and for including or excluding search results based on filter criteria. Although a vector field isn't filterable, you can set up a filterable text or numeric field. The search engine can process the filter before or after executing the vector query.

+ **Vector database**. Azure AI Search stores the data that you query over. Use it as a [pure vector index](vector-store.md) when you need long-term memory or a knowledge base, grounding data for the [retrieval-augmented generation (RAG)](retrieval-augmented-generation-overview.md) architecture, or an app that uses vectors.

## How does vector search work?

Azure AI Search supports indexing, storing, and querying vector embeddings from a search index. The following diagram shows the indexing and query workflows for vector search.

:::image type="content" source="media/vector-search-overview/vector-search-architecture-diagram-3.svg" alt-text="Architecture of vector search workflow." border="false" lightbox="media/vector-search-overview/vector-search-architecture-diagram-3-high-res.png":::

On the indexing side, Azure AI Search uses a [nearest neighbors algorithm](vector-search-ranking.md) to place similar vectors close together in an index. Internally, it creates [vector indexes](vector-store.md) for each vector field.

How you get embeddings from your source content into Azure AI Search depends on your processing approach:

+ For internal processing, Azure AI Search offers [integrated data chunking and vectorization](vector-search-integrated-vectorization.md) in an indexer pipeline. You provide the necessary resources, such as endpoints and connection information for Azure OpenAI. Azure AI Search then makes the calls and handles the transitions. This approach requires an indexer, a supported data source, and a skillset that drives chunking and embedding.

+ For external processing, you can [generate embeddings](vector-search-how-to-generate-embeddings.md) outside of Azure AI Search and push the prevectorized content directly into [vector fields](vector-search-how-to-create-index.md) in your search index.

On the query side, your client app collects user input, typically through a prompt. You can add an encoding step to vectorize the input and then send the vector query to your Azure AI Search index for similarity search. As with indexing, you can use [integrated vectorization](vector-search-integrated-vectorization.md) to encode the query. For either approach, Azure AI Search returns documents with the requested `k` nearest neighbors (kNN) in the results.

Azure AI Search supports [hybrid scenarios](hybrid-search-overview.md) that run vector and keyword search in parallel and return a unified result set, which often provides better results than vector or keyword search alone. For hybrid search, both vector and nonvector content are ingested into the same index for queries that run simultaneously.

## Availability and pricing

Vector search is available in [all regions](search-region-support.md) and on [all tiers](search-sku-tier.md) at no extra charge. However, generating embeddings or using AI enrichment for vectorization might incur charges from the model provider.

For portal and programmatic access to vector search, you can use:

+ The [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) in the Azure portal.
+ The [Search Service REST APIs](/rest/api/searchservice).
+ The Azure SDKs for [.NET](https://www.nuget.org/packages/Azure.Search.Documents), [Python](https://pypi.org/project/azure-search-documents), and [JavaScript](https://www.npmjs.com/package/@azure/search-documents).
+ [Other Azure offerings](#azure-integration-and-related-services), such as Microsoft Foundry.

> [!NOTE]
> + Some search services created before January 1, 2019 don't support vector workloads. If you try to add a vector field to a schema and get an error, it's a result of outdated services. In this situation, you must create a new search service to try out the vector feature.
>
> + Search services created after April 3, 2024 offer [higher quotas for vector indexes](vector-search-index-size.md). If you have an older service, you might be able to [upgrade your service](search-how-to-upgrade.md) for higher vector quotas.

## Azure integration and related services

Azure AI Search is deeply integrated across the Azure AI platform. The following table lists products that are useful in vector workloads.

| Product | Integration |
|---------|-------------|
| Azure OpenAI | Azure OpenAI provides embedding models and chat models. Demos and samples target the [text-embedding-ada-002](/azure/ai-services/openai/concepts/models#embeddings-models) model. We recommend Azure OpenAI for generating embeddings for text. |
| Foundry Tools | [Image Retrieval Vectorize Image API](/azure/ai-services/computer-vision/how-to/image-retrieval#call-the-vectorize-image-api) supports vectorization of image content. We recommend this API for generating embeddings for images. |
| Foundry Agent Service | In Azure AI Search, you can create an *indexed [knowledge source](agentic-knowledge-source-overview.md)* that points to a search index containing vector fields and a vectorizer. You can then parent the knowledge source to a *[knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)* and [connect the knowledge base to Foundry Agent Service](/azure/ai-foundry/agents/how-to/foundry-iq-connect), providing your agents with vector search results for enhanced knowledge retrieval. |
| Azure data platforms: Azure Blob Storage, Azure Cosmos DB, Azure SQL, Microsoft OneLake | You can use [indexers](search-indexer-overview.md) to automate data ingestion, and then use [integrated vectorization](vector-search-integrated-vectorization.md) to generate embeddings. Azure AI Search can automatically index vector data from [Azure blob indexers](search-how-to-index-azure-blob-storage.md), [Azure Cosmos DB for NoSQL indexers](search-how-to-index-cosmosdb-sql.md), [Azure Data Lake Storage Gen2](search-how-to-index-azure-data-lake-storage.md), [Azure Table Storage](search-how-to-index-azure-tables.md), and [Microsoft OneLake](search-how-to-index-onelake-files.md). For more information, see [Add vector fields to a search index](vector-search-how-to-create-index.md). |

It's also commonly used in open-source frameworks like [LangChain](https://js.langchain.com/docs/integrations/vectorstores/azure_aisearch).

## Related content

+ [Quickstart: Vector search using REST](search-get-started-vector.md)
+ [Create a vector index](vector-search-how-to-create-index.md)
+ [Create a vector query](vector-search-how-to-query.md)
+ [azure-vector-search-samples](https://github.com/Azure-Samples/azure-vector-search-samples)
+ [Azure Cognitive Search and LangChain: A Seamless Integration for Enhanced Vector Search Capabilities](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-and-langchain-a-seamless-integration-for/ba-p/3901448)
