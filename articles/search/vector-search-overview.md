---
title: Vector search
titleSuffix: Azure AI Search
description: Describes concepts, scenarios, and availability of vector capabilities in Azure AI Search.

author: robertklee
ms.author: robertlee
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 06/20/2025
---

# Vector search in Azure AI Search

Vector search is an information retrieval approach that supports indexing and querying over numeric representations of content. Because the content is numeric rather than plain text, matching is based on vectors that are most similar to the query vector, which enables matching across:

+ Semantic or conceptual likeness. For example, "dog" and "canine" are conceptually similar but linguistically distinct.
+ Multilingual content, such as "dog" in English and "hund" in German.
+ Multiple content types, such as "dog" in plain text and an image of a dog.

This article covers vector support in Azure AI Search, including its integration with other Azure services. It also introduces concepts and terminology related to vector search development.

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

## How vector search works in Azure AI Search

Azure AI Search supports indexing, storing, and querying vector embeddings from a search index. The following diagram shows the indexing and query workflows for vector search.

:::image type="content" source="media/vector-search-overview/vector-search-architecture-diagram-3.svg" alt-text="Architecture of vector search workflow." border="false" lightbox="media/vector-search-overview/vector-search-architecture-diagram-3-high-res.png":::

On the indexing side, Azure AI Search uses a [nearest neighbors algorithm](vector-search-ranking.md) to place similar vectors close together in an index. Internally, it creates [vector indexes](vector-store.md) for each vector field.

How you get embeddings from your source content into Azure AI Search depends on your processing approach:

+ For internal processing, Azure AI Search offers [integrated data chunking and vectorization](vector-search-integrated-vectorization.md) in an indexer pipeline. You provide the necessary resources, such as endpoints and connection information for Azure OpenAI. Azure AI Search then makes the calls and handles the transitions. This approach requires an indexer, a supported data source, and a skillset that drives chunking and embedding.

+ For external processing, you can [generate embeddings](vector-search-how-to-generate-embeddings.md) outside of Azure AI Search and push the prevectorized content directly into [vector fields](vector-search-how-to-create-index.md) in your search index.

On the query side, your client app collects user input, typically through a prompt. You can add an encoding step to vectorize the input and then send the vector query to your Azure AI Search index for similarity search. As with indexing, you can use [integrated vectorization](vector-search-integrated-vectorization.md) to encode the query. For either approach, Azure AI Search returns documents with the requested `k` nearest neighbors (kNN) in the results.

Azure AI Search supports [hybrid scenarios](hybrid-search-overview.md) that run vector and keyword search in parallel and return a unified result set, which often provides better results than vector or keyword search alone. For hybrid search, both vector and nonvector content are ingested into the same index for queries that run simultaneously.

## Availability and pricing

Vector search is available in [all regions](search-region-support.md) and on [all tiers](search-sku-tier.md) at no extra charge.

For portal and programmatic access to vector search, you can use:

+ The [Import and vectorize data wizard](search-get-started-portal-import-vectors.md) in the Azure portal.
+ The [Search Service REST APIs](/rest/api/searchservice).
+ The Azure SDKs for [.NET](https://www.nuget.org/packages/Azure.Search.Documents), [Python](https://pypi.org/project/azure-search-documents), and [JavaScript](https://www.npmjs.com/package/@azure/search-documents).
+ [Other Azure offerings](#azure-integration-and-related-services), such as Azure AI Foundry.

> [!NOTE]
> + Some search services created before January 1, 2019 don't support vector workloads. If you try to add a vector field to a schema and get an error, it's a result of outdated services. In this situation, you must create a new search service to try out the vector feature.
>
> + Search services created after April 3, 2024 offer [higher quotas for vector indexes](vector-search-index-size.md). If you have an older service, you might be able to [upgrade your service](search-how-to-upgrade.md) for higher vector quotas.

## Azure integration and related services

Azure AI Search is deeply integrated across the Azure AI platform. The following table lists products that are useful in vector workloads.

| Product | Integration |
|---------|-------------|
| Azure AI Foundry | In the chat playground, **Add your own data** uses Azure AI Search for grounding data and conversational search. The playground is the easiest and fastest way to [chat with your data](/azure/ai-services/openai/use-your-data-quickstart). |
| Azure OpenAI | Azure OpenAI provides embedding models and chat models. Demos and samples target the [text-embedding-ada-002](/azure/ai-services/openai/concepts/models#embeddings-models) model. We recommend Azure OpenAI for generating embeddings for text. |
| Azure AI Services | [Image Retrieval Vectorize Image API (preview)](/azure/ai-services/computer-vision/how-to/image-retrieval#call-the-vectorize-image-api) supports vectorization of image content. We recommend this API for generating embeddings for images. |
| Azure data platforms: Azure Blob Storage, Azure Cosmos DB, Azure SQL, OneLake | You can use [indexers](search-indexer-overview.md) to automate data ingestion, and then use [integrated vectorization](vector-search-integrated-vectorization.md) to generate embeddings. Azure AI Search can automatically index vector data from [Azure blob indexers](search-howto-indexing-azure-blob-storage.md), [Azure Cosmos DB for NoSQL indexers](search-howto-index-cosmosdb.md), [Azure Data Lake Storage Gen2](search-howto-index-azure-data-lake-storage.md), [Azure Table Storage](search-howto-indexing-azure-tables.md), and [Fabric OneLake](search-how-to-index-onelake-files.md). For more information, see [Add vector fields to a search index.](vector-search-how-to-create-index.md). |

It's also commonly used in open-source frameworks like [LangChain](https://js.langchain.com/docs/integrations/vectorstores/azure_aisearch).

## Vector search concepts

If you're new to vectors, this section explains some core concepts.

### About vector search

Vector search is a method of information retrieval where documents and queries are represented as vectors instead of plain text. In vector search, machine learning models generate the vector representations of source inputs, which can be text, images, or other content.

Having a mathematic representation of content provides a common language for comparing disparate content. If everything is a vector, a query can find a match in vector space, even if the associated original content is in different media or language than the query.

### Why use vector search?

When searchable content is represented as vectors, a query can find close matches in similar content. The embedding model used for vector generation knows which words and concepts are similar and places the resulting vectors close together in the embedding space.

For example, vectorized source documents about "clouds" and "fog" are more likely to show up in a query about "mist" because they're semantically similar, even if they aren't a lexical match.

### Embeddings and vectorization

Machine learning models create *embeddings*, a specific type of vector representation of content or queries. These models capture the semantic meaning of text or representations of other content, such as images.

Natural-language machine learning models are trained on large amounts of data to identify patterns and relationships between words. During training, the models learn to represent any input as a vector of real numbers in an intermediary step called the *encoder*. After training, the models can be modified so that the intermediary vector representation becomes their output. The resulting embeddings are high-dimensional vectors, where words with similar meanings are closer together in the vector space. For more information about embeddings, see [Understand embeddings in Azure OpenAI in Azure AI Foundry Models](/azure/ai-services/openai/concepts/understand-embeddings).

The effectiveness of vector search in retrieving relevant information depends on how effectively the embedding model distills the meaning of documents and queries into the resulting vector. The best models are well-trained on the types of data they represent. You can evaluate existing models, such as Azure OpenAI text-embedding-ada-002; bring your own model that's trained directly on the problem space; or fine-tune a general-purpose model. Azure AI Search doesn't impose constraints on which model you choose, so pick the best one for your data.

To create effective embeddings for vector search, it's important to consider input size limitations. We recommend following the [guidelines for chunking data](vector-search-how-to-chunk-documents.md) before generating embeddings. This best practice ensures that the embeddings accurately capture the relevant information and enable more efficient vector search.

### What is an embedding space?

An *embedding space* is the corpus for vector queries. Within a [search index](search-what-is-an-index.md), the embedding space is all of the vector fields populated with embeddings from the same embedding model. Machine learning models create the embedding space by mapping individual words, phrases, documents (for natural-language processing), images, or other data into representations comprised of vectors of real numbers that act as coordinates in a high-dimensional space.

In the embedding space, similar items are located close together, while dissimilar items are located farther apart. For example, documents about different species of dogs would be clustered close together. Documents about cats would be close together but farther from the dogs cluster, while still being in the neighborhood for animals. Dissimilar concepts, such as cloud computing, would be much farther away.

In practice, embedding spaces are abstract and don't have well-defined, human-interpretable meanings, but the core idea stays the same.

<a name="eknn"></a>

### Nearest neighbors search

In vector search, the search engine scans vectors within the embedding space to identify vectors that are closest to the query vector. This technique is called [*nearest neighbor search*](https://en.wikipedia.org/wiki/Nearest_neighbor_search).

Nearest neighbors quantify the similarity between items. A high degree of vector similarity indicates that the original data is also similar. To expedite nearest neighbor search and reduce the search space, the search engine uses data structures and data partitioning. Each vector search algorithm solves the nearest neighbor problems differently, optimizing for minimum latency, maximum throughput, recall, and memory. To compute similarity, similarity metrics provide the mechanism for computing distance.

Azure AI Search supports the following algorithms:

+ **Hierarchical navigable small world (HNSW)**. HNSW is a leading ANN algorithm optimized for high-recall, low-latency applications with unknown or volatile data distribution. It organizes high-dimensional data points into a hierarchical graph structure that enables fast, scalable similarity search and allows a tunable trade-off between search accuracy and computational cost. Because the algorithm requires all data points to reside in memory for fast random access, HNSW consumes [vector index size](vector-search-index-size.md) quota.

+ **Exhaustive k-nearest neighbors (KNN)**. KNN calculates the distances between the query vector and all data points. It's computationally intensive and works best for smaller datasets. Because the algorithm doesn't require fast random access of data points, KNN doesn't consume vector index size quota. However, it provides the global set of nearest neighbors.

To learn how to specify the algorithm, vector profile, and profile assignment for HNSW or KNN, see [Create a vector field](vector-search-how-to-create-index.md).

Algorithm parameters that are used to initialize the index during index creation are immutable and can't be changed after the index is built. However, parameters that affect the query-time characteristics (`efSearch`) can be modified.

Fields that specify the HNSW algorithm also support exhaustive KNN search using the [query request](vector-search-how-to-query.md) parameter `"exhaustive": true`. However, the opposite isn't true. If a field is indexed for `exhaustiveKnn`, you can't use HNSW in the query because the extra data structures that enable efficient search don't exist.

### Approximate nearest neighbors

Approximate nearest neighbor (ANN) is a class of algorithms for finding matches in vector space. This class of algorithms uses different data structures or data partitioning methods to significantly reduce the search space and accelerate query processing.

ANN algorithms sacrifice some accuracy but offer scalable and faster retrieval of approximate nearest neighbors, which makes them ideal for balancing accuracy and efficiency in modern information retrieval applications. You can adjust the parameters of your algorithm to fine-tune the recall, latency, memory, and disk footprint requirements of your search application.

Azure AI Search uses HNSW for its ANN algorithm.

<!-- > [!NOTE]
> Finding the true set of [nearest neighbors](https://en.wikipedia.org/wiki/Nearest_neighbor_search) requires comparing the input vector exhaustively against all vectors in the dataset. While each vector similarity calculation is relatively fast, performing these exhaustive comparisons across large datasets is computationally expensive and slow due to the sheer number of comparisons. For example, if a dataset contains 10 million 1,000-dimensional vectors, computing the distance between the query vector and all vectors in the dataset would require scanning 37 GB of data (assuming single-precision floating point vectors) and a high number of similarity calculations.
> 
> To address this challenge, approximate nearest neighbor (ANN) search methods are used to trade off recall for speed. These methods can efficiently find a small set of candidate vectors that are similar to the query vector and have high likelihood to be in the globally most similar neighbors. Each algorithm has a different approach to reducing the total number of vectors comparisons, but they all share the ability to balance accuracy and efficiency by tweaking the algorithm configuration parameters. -->

## Related content

+ [Quickstart: Vector search using REST](search-get-started-vector.md)
+ [Create a vector index](vector-search-how-to-create-index.md)
+ [Create a vector query](vector-search-how-to-query.md)
+ [azure-vector-search-samples](https://github.com/Azure-Samples/azure-vector-search-samples)
+ [Azure Cognitive Search and LangChain: A Seamless Integration for Enhanced Vector Search Capabilities](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-and-langchain-a-seamless-integration-for/ba-p/3901448)
