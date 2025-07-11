---
title: Create a vector index
titleSuffix: Azure AI Search
description: Create or update a search index to include vector fields.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 07/07/2025
---

# Create a vector index

In Azure AI Search, you can use [Create or Update Index (REST API)](/rest/api/searchservice/indexes/create-or-update) to store vectors in a search index. A vector index is defined by an index schema that has vector fields, nonvector fields, and a vector configuration section.

When you create a vector index, you implicitly create an *embedding space* that serves as the corpus for vector queries. The embedding space consists of all vector fields populated with embeddings from the same embedding model. At query time, the system compares the vector query to the indexed vectors, returning results based on semantic similarity.

To index vectors in Azure AI Search, follow these steps:

> [!div class="checklist"]
> + Start with a basic schema definition.
> + Add vector algorithms and optional compression.
> + Add vector field definitions.
> + Load prevectorized data as a [separate step](#load-vector-data-for-indexing) or use [integrated vectorization](vector-search-integrated-vectorization.md) for data chunking and embedding during indexing.

This article uses REST for illustration. After you understand the basic workflow, continue with the Azure SDK code samples in the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo, which provides guidance on using vectors in test and production code.

> [!TIP]
> You can also use the Azure portal to [create a vector index](search-get-started-portal-import-vectors.md) and try out integrated data chunking and vectorization.

## Prerequisites

+ An [Azure AI Search service](search-create-service-portal.md) in any region and on any tier. If you plan to use [integrated vectorization](vector-search-integrated-vectorization.md) with Azure AI skills and vectorizers, Azure AI Search must be in the same region as the embedding models hosted on Azure AI Vision.

+ Your source documents must have [vector embeddings](vector-search-how-to-generate-embeddings.md) to upload to the index. You can also use [integrated vectorization](vector-search-integrated-vectorization.md) for this step.

+ You should know the dimensions limit of the model that creates the embeddings so that you can assign that limit to the vector field. For **text-embedding-ada-002**, dimensions are fixed at 1536. For **text-embedding-3-small** or **text-embedding-3-large**, dimensions range from 1 to 1536 and from 1 to 3072, respectively.

+ You should know what similarity metric to use. For embedding models on Azure OpenAI, similarity is computed using [`cosine`](/azure/ai-services/openai/concepts/understand-embeddings#cosine-similarity).

+ You should know how to [create an index](search-how-to-create-search-index.md). A schema always includes a field for the document key, fields for search or filters, and other configurations for behaviors needed during indexing and queries.

## Limitations

Some search services created before January 2019 can't create a vector index. If this applies to you, create a new service to use vectors.

## Prepare documents for indexing

Before indexing, assemble a document payload that includes fields of vector and nonvector data. The document structure must conform to the fields collection of index schema.

Make sure your source documents provide the following content:

| Content | Description |
|---------|-------------|
| Unique identifier | A field or a metadata property that uniquely identifies each document. All search indexes require a document key. To satisfy document key requirements, a source document must have one field or property uniquely identifies it in the index. If you're indexing blobs, it might be the metadata_storage_path that uniquely identifies each blob. If you're indexing from a database, it might be primary key. This source field must be mapped to an index field of type `Edm.String` and `key=true` in the search index.|
| Non-vector content | Provide other fields with human-readable content. Human-readable content is useful for the query response and for [hybrid queries](hybrid-search-overview.md) that include full-text search or semantic ranking in the same request. If you're using a chat completion model, most models like ChatGPT expect human-readable text and don't accept raw vectors as input. |
| Vector content | A vectorized representation of your nonvector content for use at query time. A vector is an array of single-precision floating point numbers generated by an embedding model. Each vector field contains a model-generated array. There's one embedding per field, where the field is a top-level field (not part of a nested or complex type). For simple integration, we recommend embedding models in [Azure OpenAI](https://aka.ms/oai/access), such as **text-embedding-3** for text documents or the [Image Retrieval REST API](/rest/api/computervision/image-retrieval) for images and multimodal embeddings.<br><br>If you can use indexers and skillsets, consider [integrated vectorization](vector-search-integrated-vectorization.md), which encodes images and text during indexing. Your field definitions are for vector fields, but incoming source data can be text or images, which are converted to vector arrays during indexing. |

Your search index should include fields and content for all of the query scenarios you want to support. Suppose you want to search or filter over product names, versions, metadata, or addresses. In this case, vector similarity search isn't especially helpful. Keyword search, geo-search, or filters that iterate over verbatim content would be a better choice. A search index that's inclusive of both vector and nonvector fields provides maximum flexibility for query construction and response composition.

For a short example of a documents payload that includes vector and nonvector fields, see the [load vector data](#load-vector-data-for-indexing) section of this article.

## Start with a basic index

Start with a minimum schema so that you have a definition to work with before adding a vector configuration and vector fields. A simple index might look the following example. For more information about an index schema, see [Create a search index](search-how-to-create-search-index.md).

Notice that the index has a required name, a required document key (`"key": true`), and fields for human-readable content in plain text. It's common to have a human-readable version of whatever content you intend to vectorize. For example, if you have a chunk of text from a PDF file, your index schema should have a field for plain-text chunks and a second field for vectorized chunks.

Here's a basic index with a `"name"`, a `"fields"` collection, and some other constructs for extra configuration:

```http
POST https://[servicename].search.windows.net/indexes?api-version=[api-version] 
{
  "name": "example-index",
  "fields": [
    { "name": "documentId", "type": "Edm.String", "key": true, "retrievable": true, "searchable": true, "filterable": true },
    { "name": "myHumanReadableNameField", "type": "Edm.String", "retrievable": true, "searchable": true, "filterable": false, "sortable": true, "facetable": false },
    { "name": "myHumanReadableContentField", "type": "Edm.String", "retrievable": true, "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
  ],
  "analyzers": [ ],
  "scoringProfiles": [ ],
  "suggesters": [ ],
  "vectorSearch": [ ]
}
```

## Add a vector search configuration

Next, add a `"vectorSearch"` configuration to your schema. It's useful to specify a configuration before field definitions, because the profiles you define here become part of the vector field's definition. In the schema, vector configuration is typically inserted after the fields collection, perhaps after `"analyzers"`, `"scoringProfiles"`, and `"suggesters"`. However, order doesn't matter.

A vector configuration includes:

+ `vectorSearch.algorithms` used during indexing to create "nearest neighbor" information among the vector nodes.
+ `vectorSearch.compressions` for scalar or binary quantization, oversampling, and reranking with original vectors.
+ `vectorSearch.profiles` for specifying multiple combinations of algorithm and compression configurations.

### [**2024-07-01**](#tab/config-2024-07-01)

[**2024-07-01**](/rest/api/searchservice/search-service-api-versions#2024-07-01) is generally available. It supports a vector configuration that has:

+ Hierarchical Navigable Small World (HNSW) algorithm.
+ Exhaustive K-Nearest Neighbor (KNN) algorithm.
+ Scalar compression.
+ Binary compression, which is available in 2024-07-01 only and in newer Azure SDK packages.
+ Oversampling.
+ Reranking with original vectors.

If you choose HNSW on a field, you can opt for exhaustive KNN at query time. However, the opposite doesn’t work. If you choose exhaustive for indexing, you can’t later request HNSW search because the extra data structures that enable approximate search don’t exist.

Be sure to have a strategy for [vectorizing your content](vector-search-how-to-generate-embeddings.md). We recommend [integrated vectorization](vector-search-integrated-vectorization.md) and [query-time vectorizers](vector-search-how-to-configure-vectorizer.md) for built-in encoding.

1. Use the [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) REST API to create the index.

1. Add a `vectorSearch` section in the index that specifies the search algorithms used to create the embedding space.

   ```json
    "vectorSearch": {
        "compressions": [
            {
                "name": "scalar-quantization",
                "kind": "scalarQuantization",
                "rerankWithOriginalVectors": true,
                "defaultOversampling": 10.0,
                    "scalarQuantizationParameters": {
                        "quantizedDataType": "int8"
                    }
            },
            {
                "name": "binary-quantization",
                "kind": "binaryQuantization",
                "rerankWithOriginalVectors": true,
                "defaultOversampling": 10.0
            }
        ],
        "algorithms": [
            {
                "name": "hnsw-1",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            },
            {
                "name": "hnsw-2",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 8,
                    "efConstruction": 800,
                    "efSearch": 800,
                    "metric": "hamming"
                }
            },
            {
                "name": "eknn",
                "kind": "exhaustiveKnn",
                "exhaustiveKnnParameters": {
                    "metric": "euclidean"
                }
            }

        ],
        "profiles": [
          {
            "name": "vector-profile-hnsw-scalar",
            "compression": "scalar-quantization",
            "algorithm": "hnsw-1"
          }
        ]
    }
   ```

   **Key points**:

   + Names for each configuration of compression, algorithm, and profile must be unique for its type within the index.

   + `vectorSearch.compressions` can be `scalarQuantization` or `binaryQuantization`. Scalar quantization compresses float values into narrower data types. Binary quantization converts floats into binary 1-bit values.

   + `vectorSearch.compressions.rerankWithOriginalVectors` uses the original, uncompressed vectors to recalculate similarity and rerank the top results returned by the initial search query. The uncompressed vectors exist in the search index even if `stored` is false. This property is optional. Default is true.

   + `vectorSearch.compressions.defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

   + `vectorSearch.compressions.scalarQuantizationParameters.quantizedDataType` must be set to `int8`. This is the only primitive data type supported at this time. This property is optional. Default is `int8`.

   + `vectorSearch.algorithms` is either `hnsw` or `exhaustiveKnn`. These are the Approximate Nearest Neighbors (ANN) algorithms used to organize vector content during indexing.

   + `vectorSearch.algorithms.m` is the bi-directional link count. Default is 4. The range is 4 to 10. Lower values should return less noise in the results.

   + `vectorSearch.algorithms.efConstruction` is the number of nearest neighbors used during indexing. Default is 400. The range is 100 to 1,000.

   + `"vectorSearch.algorithms.efSearch` is the number of nearest neighbors used during search. Default is 500. The range is 100 to 1,000.

   + `vectorSearch.algorithms.metric` should be `cosine` if you're using Azure OpenAI, otherwise use the similarity metric associated with the embedding model you're using. Supported values are `cosine`, `dotProduct`, `euclidean`, and `hamming` (used for [indexing binary data](vector-search-how-to-index-binary-data.md)).

   + `vectorSearch.profiles` add a layer of abstraction for accommodating richer definitions. A profile is defined in `vectorSearch` and referenced by name in each vector field. It's a combination of compression and algorithm configurations. You assign this property to a vector field, and it determines the fields' algorithm and compression.

### [**2024-05-01-preview**](#tab/config-2024-05-01-Preview)

[**2024-05-01-preview**](/rest/api/searchservice/search-service-api-versions#2024-05-01-preview) is the most recent preview version. It's inclusive of previous preview versions.

Preview and stable API versions support the same `vectorSearch` configurations. You would choose the preview over the stable version for other reasons, such as [more compression options](vector-search-how-to-quantization.md) or [newer vectorizers](vector-search-how-to-configure-vectorizer.md) invoked at query time.

1. Use the [Create or Update Index Preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) to create the index.

1. Add a `vectorSearch` section in the index that specifies compression settings and the search algorithms used to create the embedding space. For more information, see [Configure vector quantization](vector-search-how-to-quantization.md).

   ```json
    "vectorSearch": {
        "compressions": [
            {
                "name": "my-scalar-quantization",
                "kind": "scalarQuantization",
                "rerankWithOriginalVectors": true,
                "defaultOversampling": 10.0,
                    "scalarQuantizationParameters": {
                        "quantizedDataType": "int8"
                    }
            }
        ],
        "algorithms": [
            {
                "name": "hnsw-1",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            },
            {
                "name": "hnsw-2",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 8,
                    "efConstruction": 800,
                    "efSearch": 800,
                    "metric": "hamming"
                }
            },
            {
                "name": "eknn",
                "kind": "exhaustiveKnn",
                "exhaustiveKnnParameters": {
                    "metric": "euclidean"
                }
            }

        ],
        "profiles": [
          {
            "name": "vector-profile-hnsw-1",
            "algorithm": "hnsw-1"
          }
        ]
    }
   ```

   **Key points**:

   + `vectorSearch.compressions.kind` must be `scalarQuantization`.

   + `vectorSearch.compressions.rerankWithOriginalVectors` uses the original, uncompressed vectors to recalculate similarity and rerank the top results returned by the initial search query. The uncompressed vectors exist in the search index even if `stored` is false. This property is optional. Default is true.

   + `vectorSearch.compressions.defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

   + `vectorSearch.compressions.scalarQuantizationParameters.quantizedDataType` must be set to `int8`. This is the only primitive data type supported at this time. This property is optional. Default is `int8`.

   + `vectorSearch.algorithms.kind` is either `hnsw` or `exhaustiveKnn`. These are the Approximate Nearest Neighbors (ANN) algorithms used to organize vector content during indexing.

   + `vectorSearch.algorithms.m` is the bi-directional link count. Default is 4. The range is 4 to 10. Lower values should return less noise in the results.

   + `vectorSearch.algorithms.efConstruction` is the number of nearest neighbors used during indexing. Default is 400. The range is 100 to 1,000.

   + `vectorSearch.algorithms.efSearch` is the number of nearest neighbors used during search. Default is 500. The range is 100 to 1,000.

   + `vectorSearch.algorithms.metric` should be `cosine` if you're using Azure OpenAI, otherwise use the similarity metric associated with the embedding model you're using. Supported values are `cosine`, `dotProduct`, `euclidean`, and `hamming` (used for [indexing binary data](vector-search-how-to-index-binary-data.md)).

   + `vectorSearch.profiles` add a layer of abstraction for accommodating richer definitions. A profile is defined in `vectorSearch` and referenced by name in each vector field. It's a combination of compression and algorithm configurations. You assign this property to a vector field, and it determines the fields' algorithm and compression.

For more information about new preview features, see [What's new in Azure AI Search](whats-new.md).

---

## Add a vector field to the fields collection

Once you have a vector configuration, you can add a vector field to the fields collection. Recall that the fields collection must include a field for the document key, vector fields, and any other nonvector fields you need for [hybrid search scenarios](hybrid-search-overview.md) or chat model completion in [RAG workloads](retrieval-augmented-generation-overview.md).

Vector fields are characterized by [their data type](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields), a `dimensions` property based on the embedding model used to output the vectors, and a vector profile that you created in a previous step.

### [**2024-07-01**](#tab/rest-2024-07-01)

[**2024-07-01**](/rest/api/searchservice/search-service-api-versions#2024-07-01) is generally available.

1. Use the [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) REST API to create the index and add a vector field to the fields collection.

    ```json
    {
      "name": "example-index",
      "fields": [
        {
            "name": "contentVector",
            "type": "Collection(Edm.Single)",
            "searchable": true,
            "retrievable": false,
            "stored": false,
            "dimensions": 1536,
            "vectorSearchProfile": "vector-profile-1"
        }
      ]
    }
    ```

1. Specify a vector field with the following attributes. You can store one generated embedding per field. For each vector field:

   + `type` must be a [vector data type](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields). `Collection(Edm.Single)` is the most common for embedding models.
   + `dimensions` is the number of dimensions generated by the embedding model. For text-embedding-ada-002, it's fixed at 1536. For the text-embedding-3 model series, there's a range of values. If you're using integrated vectorization and an embedding skill to generate vectors, make sure this property is set to the [same dimensions value](cognitive-search-skill-azure-openai-embedding.md#supported-dimensions-by-modelname) used by the embedding skill.
   + `vectorSearchProfile` is the name of a profile defined elsewhere in the index.
   + `searchable` must be true.
   + `retrievable` can be true or false. True returns the raw vectors (1,536 of them) as plain text and consumes storage space. Set to true if you're passing a vector result to a downstream app.
   + `stored` can be true or false. It determines whether an extra copy of vectors is stored for retrieval. For more information, see [Reduce vector size](vector-search-how-to-storage-options.md).
   + `filterable`, `facetable`, and `sortable` must be false.

1. Add filterable nonvector fields to the collection, such as `title` with `filterable` set to true, if you want to invoke [prefiltering or postfiltering](vector-search-filters.md) on the [vector query](vector-search-how-to-query.md).

1. Add other fields that define the substance and structure of the textual content you're indexing. At a minimum, you need a document key.

   You should also add fields that are useful in the query or in its response. The following example shows vector fields for title and content (`titleVector` and `contentVector`) that are equivalent to vectors. It also provides fields for equivalent textual content (`title` and `content`) that are useful for sorting, filtering, and reading in a search result.

   The following example shows the fields collection:

    ```http
    PUT https://my-search-service.search.windows.net/indexes/my-index?api-version=2024-07-01&allowIndexDowntime=true
    Content-Type: application/json
    api-key: {{admin-api-key}}
    {
        "name": "{{index-name}}",
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "key": true,
                "filterable": true
            },
            {
                "name": "title",
                "type": "Edm.String",
                "searchable": true,
                "filterable": true,
                "sortable": true,
                "retrievable": true
            },
            {
                "name": "titleVector",
                "type": "Collection(Edm.Single)",
                "searchable": true,
                "retrievable": true,
                "stored": true,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            },
            {
                "name": "content",
                "type": "Edm.String",
                "searchable": true,
                "retrievable": true
            },
            {
                "name": "contentVector",
                "type": "Collection(Edm.Single)",
                "searchable": true,
                "retrievable": false,
                "stored": false,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            }
        ],
        "vectorSearch": {
            "algorithms": [
                {
                    "name": "hnsw-1",
                    "kind": "hnsw",
                    "hnswParameters": {
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500,
                        "metric": "cosine"
                    }
                }
            ],
            "profiles": [
                {
                    "name": "vector-profile-1",
                    "algorithm": "hnsw-1"
                }
            ]
        }
    }
    ```

### [**2024-05-01-preview**](#tab/rest-2024-05-01-Preview)

[**2024-05-01-preview**](/rest/api/searchservice/search-service-api-versions#2024-05-01-preview) is the most recent preview version. It supports the same vector field definitions as the stable version, including support for all [vector data types](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields).

1. Use the [Create or Update Index Preview REST API](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-05-01-preview&preserve-view=true) to create the index and add a vector field to the fields collection.

    ```json
    {
      "name": "example-index",
      "fields": [
        {
            "name": "contentVector",
            "type": "Collection(Edm.Single)",
            "searchable": true,
            "retrievable": false,
            "stored": false,
            "dimensions": 1536,
            "vectorSearchProfile": "vector-profile-1"
        }
      ]
    }
    ```

1. Specify a vector field with the following attributes. You can store one generated embedding per document field. For each vector field:

   + `type` can be `Collection(Edm.Single)`, `Collection(Edm.Half)`, `Collection(Edm.Int16)`, or `Collection(Edm.SByte)`.
   + `dimensions` is the number of dimensions generated by the embedding model. For text-embedding-ada-002, it's 1536.
   + `vectorSearchProfile` is the name of a profile defined elsewhere in the index.
   + `searchable` must be true.
   + `retrievable` can be true or false. True returns the raw vectors (1,536 of them) as plain text and consumes storage space. Set to true if you're passing a vector result to a downstream app. False is required if `stored` is false.
   + `stored` is a new boolean property that applies to vector fields only. True stores a copy of vectors returned in search results. False discards that copy during indexing. You can search on vectors, but you can't return vectors in results.
   + `filterable`, `facetable`, and `sortable` must be false.

1. Add filterable nonvector fields to the collection, such as "title" with `filterable` set to true, if you want to invoke [prefiltering or postfiltering](vector-search-filters.md) on the [vector query](vector-search-how-to-query.md).

1. Add other fields that define the substance and structure of the textual content you're indexing. At a minimum, you need a document key.

   You should also add fields that are useful in the query or in its response. The following example shows vector fields for title and content (`titleVector` and `contentVector`) that are equivalent to vectors. It also provides fields for equivalent textual content (`title` and `content`) that are useful for sorting, filtering, and reading in a search result.

   The following example shows the fields collection:

    ```http
    PUT https://my-search-service.search.windows.net/indexes/my-index?api-version=2024-05-01-preview&allowIndexDowntime=true
    Content-Type: application/json
    api-key: {{admin-api-key}}
    {
        "name": "{{index-name}}",
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "key": true,
                "filterable": true
            },
            {
                "name": "firstVectorfield-float32-embeddings",
                "type": "Collection(Edm.Single)",
                "searchable": true,
                "retrievable": false,
                "stored": false,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            },
            {
                "name": "secondVectorfield-float16-embeddings",
                "type": "Collection(Edm.Half)",
                "searchable": true,
                "retrievable": false,
                "stored": false,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            },
            {
                "name": "thirdVectorfield-int8-embeddings-for-my-custom-quantization-output",
                "type": "Collection(Edm.SByte)",
                "searchable": true,
                "retrievable": false,
                "stored": false,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            },
            {
                "name": "fourthVectorfield-for-binary-data",
                "type": "Collection(Edm.Byte)",
                "searchable": true,
                "retrievable": false,
                "stored": false,
                "dimensions": 1536,
                "vectorSearchProfile": "vector-profile-1"
            }
        ],
        "vectorSearch": {
            "algorithms": [
                {
                    "name": "hnsw-1",
                    "kind": "hnsw",
                    "hnswParameters": {
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500,
                        "metric": "cosine"
                    }
                }
            ],
            "profiles": [
                {
                    "name": "vector-profile-1",
                    "algorithm": "hnsw-1"
                }
            ]
        }
    }
   ```

---

## Load vector data for indexing

Content that you provide for indexing must conform to the index schema and include a unique string value for the document key. Prevectorized data is loaded into one or more vector fields, which can coexist with other fields containing nonvector content.

For data ingestion, you can use [push or pull methodologies](search-what-is-data-import.md).

### [**Push APIs**](#tab/push)

Use **Documents - Index** to load vector and nonvector data into an index. The push APIs for indexing are identical across all stable and preview versions. Use any of the following APIs to load documents:

+ [2024-07-01](/rest/api/searchservice/documents)
+ [2024-05-01-preview](/rest/api/searchservice/documents/?view=rest-searchservice-2024-05-01-preview&preserve-view=true)

```http
POST https://{{search-service-name}}.search.windows.net/indexes/{{index-name}}/docs/index?api-version=2024-07-01

{
    "value": [
        {
            "id": "1",
            "title": "Azure App Service",
            "content": "Azure App Service is a fully managed platform for building, deploying, and scaling web apps. You can host web apps, mobile app backends, and RESTful APIs. It supports a variety of programming languages and frameworks, such as .NET, Java, Node.js, Python, and PHP. The service offers built-in auto-scaling and load balancing capabilities. It also provides integration with other Azure services, such as Azure DevOps, GitHub, and Bitbucket.",
            "category": "Web",
            "titleVector": [
                -0.02250031754374504,
                 . . . 
                        ],
            "contentVector": [
                -0.024740582332015038,
                 . . .
            ],
            "@search.action": "upload"
        },
        {
            "id": "2",
            "title": "Azure Functions",
            "content": "Azure Functions is a serverless compute service that enables you to run code on-demand without having to manage infrastructure. It allows you to build and deploy event-driven applications that automatically scale with your workload. Functions support various languages, including C#, F#, Node.js, Python, and Java. It offers a variety of triggers and bindings to integrate with other Azure services and external services. You only pay for the compute time you consume.",
            "category": "Compute",
            "titleVector": [
                -0.020159931853413582,
                . . .
            ],
            "contentVector": [
                -0.02780858241021633,
                 . . .
            ],
            "@search.action": "upload"
        }
        . . .
    ]
}
```

### [**Pull APIs (indexers)**](#tab/pull)

Pull APIs refer to indexers that automate multiple indexing steps, from data retrieval and refresh to [integrated vectorization](vector-search-integrated-vectorization.md), which encodes content for vector search.

+ Data sources must be a [supported type](search-indexer-overview.md#supported-data-sources).

+ Skillsets provide the [Text Split skill](cognitive-search-skill-textsplit.md) for data chunking, plus skills that connect to embedding models. Some skills are generally available, while others are still in preview. Skills and vectorizers are used to generate embeddings. The skill you choose for indexing should be paired with an [equivalent vectorizer](vector-search-integrated-vectorization.md#using-integrated-vectorization-in-queries) for queries. For vectorization during indexing, choose from the following skills:

  + [AzureOpenAIEmbedding skill](cognitive-search-skill-azure-openai-embedding.md)
  + [Custom Web API skill](cognitive-search-custom-skill-web-api.md)
  + [Azure AI Vision multimodal embeddings skill (preview)](cognitive-search-skill-vision-vectorize.md)
  + [AML skill (preview)](cognitive-search-aml-skill.md) to generate embeddings for models hosted in the Azure AI Foundry model catalog. For more information, see [Use embedding models from Azure AI Foundry model catalog for integrated vectorization](vector-search-integrated-vectorization-ai-studio.md).

+ Indexes provide the vector field definitions and vector search configurations. This article describes those definitions.

+ Indexers drive the indexing pipeline. For more information, see [Create an indexer](search-howto-create-indexers.md).

If you're familiar with indexers and skillsets:

+ Field mappings, output field mappings, and deletion detection settings apply to vector and nonvector fields equally.

+ If vector data is sourced in files, we recommend a nondefault `parsingMode`, such as `json`, `jsonLines`, or `csv` based on the shape of the data.

+ For data sources, [Azure blob indexers](search-howto-indexing-azure-blob-storage.md) and [Azure Cosmos DB for NoSQL indexers](search-howto-index-cosmosdb.md) with one of the aforementioned parsingModes have been tested and confirmed to work.

+ The dimensions of all vectors from the data source must be the same and match their index definition for the field they're mapping to. The indexer throws an error on any documents that don’t match.

---

## Query your index for vector content

For validation purposes, you can query the index using Search Explorer in the Azure portal or a REST API call. Because Azure AI Search can't convert a vector to human-readable text, try to return fields from the same document that provide evidence of the match. For example, if the vector query targets the `titleVector` field, you could select `title` for the search results.

Fields must be attributed as `retrievable` to be included in the results.

### [**Azure portal**](#tab/portal-check-index)

+ Review the indexes in **Search management** > **Indexes** to view index size all-up and vector index size. A positive vector index size indicates vectors are present.

+ Use [Search Explorer](search-explorer.md) to query an index. Search Explorer has two views: Query view (default) and JSON view. 

  + Set **Query options** > **Hide vector values in search results** for more readable results.

  + [Use the JSON view for vector queries](vector-search-how-to-query.md). You can paste a JSON definition of the vector query you want to execute. If your index has a [vectorizer assignment](vector-search-how-to-configure-vectorizer.md), you can also use the built-in text-to-vector or image-to-vector conversion. For more information about image search, see [Quickstart: Search for images in Search Explorer](search-get-started-portal-image-search.md).

  + Use the default Query view for a quick confirmation that the index contains vectors. The query view is for full-text search. Although you can't use it for vector queries, you can send an empty search (`search=*`) to check for content. The content of all fields, including vector fields, is returned as plain text.

For more information, see [Create a vector query](vector-search-how-to-query.md).

### [**REST API**](#tab/rest-check-index)

The following REST API example is a vector query, but it returns only nonvector fields (`title`, `content`, and `category`). Only fields marked as `retrievable` can be returned in search results.

```http
POST https://my-search-service.search.windows.net/indexes/my-index/docs/search?api-version=2024-07-01
Content-Type: application/json
api-key: {{admin-api-key}}
{
    "vector": {
        "value": [
            -0.009154141,
            0.018708462,
            . . . 
            -0.02178128,
            -0.00086512347
        ],
        "fields": "contentVector",
        "k": 5
    },
    "select": "title, content, category"
}
```

---

## Update a vector index

To update a vector index, modify the schema and reload documents to populate new fields. APIs for schema updates include [Create or Update Index (REST)](/rest/api/searchservice/indexes/create-or-update), [CreateOrUpdateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createorupdateindexasync) in the Azure SDK for .NET, [create_or_update_index](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python#azure-search-documents-indexes-searchindexclient-create-or-update-index&preserve-view=true) in the Azure SDK for Python, and similar methods in other Azure SDKs.

For standard guidance on updating an index, see [Update or rebuild an index](search-howto-reindex.md).

Key points include:

+ Drop and full index rebuild is often required for updates to and deletion of existing fields.

+ You can make the following modifications with no rebuild requirement:

  + Add new fields to a fields collection.
  + Add new vector configurations, assigned to new fields but not existing fields that are already vectorized.
  + Change `retrievable` (values are true or false) on an existing field. Vector fields must be searchable and retrievable, but if you want to disable access to a vector field in situations where drop and rebuild isn't feasible, you can set retrievable to false.

## Next steps

As a next step, we recommend [Create a vector query](vector-search-how-to-query.md).

Code samples in the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repository demonstrate end-to-end workflows that include schema definition, vectorization, indexing, and queries.

There's demo code for [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python), [C#](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet), and [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript).
