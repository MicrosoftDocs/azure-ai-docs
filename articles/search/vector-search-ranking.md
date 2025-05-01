---
title: Vector relevance and ranking
titleSuffix: Azure AI Search
description: Explains the concepts behind vector relevance, scoring, including how matches are found in vector space and ranked in search results.

author: yahnoosh
ms.author: jlembicz
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 12/05/2024
---

# Relevance in vector search

During vector query execution, the search engine looks for similar vectors to find the best candidates to return in search results. Depending on how you indexed the vector content, the search for relevant matches is either exhaustive, or constrained to nearest neighbors for faster processing. Once candidates are found, similarity metrics are used to score each result based on the strength of the match. 

This article explains the algorithms used to find relevant matches and the similarity metrics used for scoring. It also offers tips for improving relevance if search results don't meet expectations.

## Algorithms used in vector search

Vector search algorithms include exhaustive k-nearest neighbors (KNN) and Hierarchical Navigable Small World (HNSW). 

+ Exhaustive KNN performs a brute-force search that scans the entire vector space.

+ HNSW performs an [approximate nearest neighbor (ANN)](vector-search-overview.md#approximate-nearest-neighbors) search. 

Only vector fields marked as `searchable` in the index, or as `searchFields` in the query, are used for searching and scoring. 

### When to use exhaustive KNN

Exhaustive KNN calculates the distances between all pairs of data points and finds the exact `k` nearest neighbors for a query point. It's intended for scenarios where high recall is of utmost importance, and users are willing to accept the trade-offs in query latency. Because it's computationally intensive, use exhaustive KNN for small to medium datasets, or when precision requirements outweigh query performance considerations. 

A secondary use case is to build a dataset to evaluate approximate nearest neighbor algorithm recall. Exhaustive KNN can be used to build the ground truth set of nearest neighbors.

### When to use HNSW

During indexing, HNSW creates extra data structures for faster search, organizing data points into a hierarchical graph structure. HNSW has several configuration parameters that can be tuned to achieve the throughput, latency, and recall objectives for your search application. For example, at query time, you can specify options for exhaustive search, even if the vector field is indexed for HNSW.

During query execution, HNSW enables fast neighbor queries by navigating through the graph. This approach strikes a balance between search accuracy and computational efficiency. HNSW is recommended for most scenarios due to its efficiency when searching over larger data sets. 

## How nearest neighbor search works

Vector queries execute against an embedding space consisting of vectors generated from the same embedding model. Generally, the input value within a query request is fed into the same machine learning model that generated embeddings in the vector index. The output is a vector in the same embedding space. Since similar vectors are clustered close together, finding matches is equivalent to finding the vectors that are closest to the query vector, and returning the associated documents as the search result.

For example, if a query request is about hotels, the model maps the query into a vector that exists somewhere in the cluster of vectors representing documents about hotels. Identifying which vectors are the most similar to the query, based on a similarity metric, determines which documents are the most relevant.

When vector fields are indexed for exhaustive KNN, the query executes against "all neighbors". For fields indexed for HNSW, the search engine uses an HNSW graph to search over a subset of nodes within the vector index.

### Creating the HNSW graph

During indexing, the search service constructs the HNSW graph. The goal of indexing a new vector into an HNSW graph is to add it to the graph structure in a manner that allows for efficient nearest neighbor search. The following steps summarize the process:

1. Initialization: Start with an empty HNSW graph, or the existing HNSW graph if it's not a new index.

1. Entry point: This is the top-level of the hierarchical graph and serves as the starting point for indexing.

1. Adding to the graph: Different hierarchical levels represent different granularities of the graph, with higher levels being more global, and lower levels being more granular. Each node in the graph represents a vector point. 

   - Each node is connected to up to `m` neighbors that are nearby. This is the `m` parameter.

   - The number of data points considered as candidate connections is governed by the `efConstruction` parameter. This dynamic list forms the set of closest points in the existing graph for the algorithm to consider. Higher `efConstruction` values result in more nodes being considered, which often leads to denser local neighborhoods for each vector.

   - These connections use the configured similarity `metric` to determine distance. Some connections are "long-distance" connections that connect across different hierarchical levels, creating shortcuts in the graph that enhance search efficiency.

1. Graph pruning and optimization: This can happen after indexing all vectors, and it improves navigability and efficiency of the HNSW graph. 

### Navigating the HNSW graph at query time

A vector query navigates the hierarchical graph structure to scan for matches. The following summarize the steps in the process:

1. Initialization: The algorithm initiates the search at the top-level of the hierarchical graph. This entry point contains the set of vectors that serve as starting points for search.

1. Traversal: Next, it traverses the graph level by level, navigating from the top-level to lower levels, selecting candidate nodes that are closer to the query vector based on the configured distance metric, such as cosine similarity.

1. Pruning: To improve efficiency, the algorithm prunes the search space by only considering nodes that are likely to contain nearest neighbors. This is achieved by maintaining a priority queue of potential candidates and updating it as the search progresses. The length of this queue is configured by the parameter `efSearch`.

1. Refinement: As the algorithm moves to lower, more granular levels, HNSW considers more neighbors near the query, which allows the candidate set of vectors to be refined, improving accuracy.

1. Completion: The search completes when the desired number of nearest neighbors have been identified, or when other stopping criteria are met. This desired number of nearest neighbors is governed by the query-time parameter `k`.

## Similarity metrics used to measure nearness

The algorithm finds candidate vectors to evaluate similarity. To perform this task, a similarity metric calculation compares the candidate vector to the query vector and measures the similarity. The algorithm keeps track of the ordered set of most similar vectors that its found, which forms the ranked result set when the algorithm has reached completion.

| Metric | Description |
|--------|-------------|
| `cosine` | This metric measures the angle between two vectors, and isn't affected by differing vector lengths. Mathematically, it calculates the angle between two vectors. Cosine is the similarity metric used by [Azure OpenAI embedding models](/azure/ai-services/openai/concepts/understand-embeddings#cosine-similarity), so if you're using Azure OpenAI, specify `cosine` in the vector configuration.|
| `dotProduct` | This metric measures both the length of each pair of two vectors, and the angle between them. Mathematically, it calculates the products of vectors' magnitudes and the angle between them. For normalized vectors, this is identical to `cosine` similarity, but slightly more performant. |
| `euclidean` | (also known as `l2 norm`) This metric measures the length of the vector difference between two vectors. Mathematically, it calculates the Euclidean distance between two vectors, which is the l2-norm of the difference of the two vectors. |

> [!NOTE]
> If you run two or more vector queries in parallel, or if you do a hybrid search that combines vector and text queries in the same request, [Reciprocal Rank Fusion (RRF)](hybrid-search-ranking.md) is used for scoring the final search results.

## Scores in a vector search results

Scores are calculated and assigned to each match, with the highest matches returned as `k` results. The **`@search.score`** property contains the score. The following table shows the range within which a score will fall.

| Search method | Parameter | Scoring metric | Range |
|---------------|-----------|-------------------|-------|
| vector search | `@search.score` | Cosine | 0.333 - 1.00 | 

For`cosine` metric, it's important to note that the calculated `@search.score` isn't the cosine value between the query vector and the document vectors. Instead, Azure AI Search applies transformations such that the score function is monotonically decreasing, meaning score values will always decrease in value as the similarity becomes worse. This transformation ensures that search scores are usable for ranking purposes.

There are some nuances with similarity scores: 

- Cosine similarity is defined as the cosine of the angle between two vectors.
- Cosine distance is defined as `1 - cosine_similarity`.

To create a monotonically decreasing function, the `@search.score` is defined as `1 / (1 + cosine_distance)`.

Developers who need a cosine value instead of the synthetic value can use a formula to convert the search score back to cosine distance:

```csharp
double ScoreToSimilarity(double score)
{
    double cosineDistance = (1 - score) / score;
    return  -cosineDistance + 1;
}
```

Having the original cosine value can be useful in custom solutions that set up thresholds to trim results of low quality results.

## Tips for relevance tuning

If you aren't getting relevant results, experiment with changes to [query configuration](vector-search-how-to-query.md). There are no specific tuning features, such as a scoring profile or field or term boosting, for vector queries:

+ Experiment with [chunk size and overlap](vector-search-how-to-chunk-documents.md). Try increasing the chunk size and ensuring there's sufficient overlap to preserve context or continuity between chunks.

+ For HNSW, try different levels of `efConstruction` to change the internal composition of the proximity graph. The default is 400. The range is 100 to 1,000.

+ Increase `k` results to feed more search results into a chat model, if you're using one.

+ Try [hybrid queries](hybrid-search-how-to-query.md) with semantic ranking. In benchmark testing, this combination consistently produced the most relevant results.

## Next steps

+ [Try the quickstart](search-get-started-vector.md)
+ [Create and configure a vector index](vector-search-how-to-create-index.md)
+ [Learn more about embeddings](vector-search-how-to-generate-embeddings.md)
+ [Learn more about data chunking](vector-search-how-to-chunk-documents.md)
