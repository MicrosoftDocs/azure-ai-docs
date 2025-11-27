---
title: Create an index for agentic retrieval
titleSuffix: Azure AI Search
description: Create an index that has fields and configurations that work for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
---

# Create an index for agentic retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, agentic retrieval uses context and user questions to generate a range of subqueries that can execute against your content in a [knowledge source](agentic-knowledge-source-overview.md). A knowledge source can point to indexed content on Azure AI Search, or remote content that's retrieved using the APIs that are native to the provider. When indexes are used in agentic retrieval, they are either:

+ An *existing index* containing searchable content. You can make an existing index available to agentic retrieval through a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md) definition.

+ A *generated index* created from an indexed [knowledge source](agentic-knowledge-source-overview.md). Indexed knowledge sources create a copy of an external data source inside a search index using a full indexer pipeline (data source, skillset, indexer, and index) for agentic retrieval. Multiple knowledge sources can generate an indexer pipeline that results in a searchable index. These include:

  + [Azure blobs](agentic-knowledge-source-how-to-blob.md)
  + [Microsoft OneLake](agentic-knowledge-source-how-to-onelake.md)
  + [SharePoint (Indexed)](agentic-knowledge-source-how-to-sharepoint-indexed.md)

A generated index is based on a template that meets all of the criteria for knowledge bases and agentic retrieval.

This article explains which index elements affect agentic retrieval query logic. None of the required elements are new or specific to agentic retrieval, which means you can use an existing index if it meets the criteria identified in this article, even if it was created using earlier API versions.

> [!NOTE]
> The following knowledge sources access external sources directly and don't require a search index: [Web Knowledge Source (Bing)](agentic-knowledge-source-how-to-web.md) and [SharePoint (Remote)](agentic-knowledge-source-how-to-sharepoint-remote.md).

## Criteria for agentic retrieval

An index that's used in agentic retrieval must have these elements:

+ String fields attributed as `searchable` and `retrievable`.
+ A [semantic configuration](semantic-search-overview.md), with a `defaultSemanticConfiguration` or a semantic configuration override in the knowledge source.

It should also have fields that can be used for citations, such as  document or file name, page or chapter name, or at least a chunk ID.

It should have [vector fields and a vectorizer](vector-search-how-to-create-index.md) if you want to include text-to-vector query conversion in the pipeline.

Optionally, the following index elements increase your opportunities for optimization:

+ `scoringProfile` with a `defaultScoringProfile`, for boosting relevance
+ `synonymMaps` for terminology or jargon 
+ `analyzers` for linguistics rules or patterns (like whitespace preservation, or special characters)

## Example index definition

Here's an example index that works for agentic retrieval. It meets the criteria for required elements. It includes vector fields as a best practice.

```json
{
  "name": "earth_at_night",
  "description": "Contains images an descriptions of our planet in darkness as captured from space by Earth-observing satellites and astronauts on the International Space Station over the past 25 years.",
  "fields": [
    {
      "name": "id", "type": "Edm.String",
      "searchable": true, "retrievable": true, "filterable": true, "sortable": true, "facetable": true,
      "key": true,
      "stored": true,
      "synonymMaps": []
    },
    {
      "name": "page_chunk", "type": "Edm.String",
      "searchable": true, "retrievable": true, "filterable": false, "sortable": false, "facetable": false,
      "analyzer": "en.microsoft",
      "stored": true,
      "synonymMaps": []
    },
    {
      "name": "page_chunk_vector_text_3_large", "type": "Collection(Edm.Single)",
      "searchable": true, "retrievable": false, "filterable": false, "sortable": false, "facetable": false,
      "dimensions": 3072,
      "vectorSearchProfile": "hnsw_text_3_large",
      "stored": false,
      "synonymMaps": []
    },
    {
      "name": "page_number", "type": "Edm.Int32",
      "searchable": false, "retrievable": true, "filterable": true, "sortable": true, "facetable": true,
      "stored": true,
      "synonymMaps": []
    },
    {
      "name": "chapter_number", "type": "Edm.Int32",
      "searchable": false, "retrievable": true, "filterable": true, "sortable": true, "facetable": true,
      "stored": true,
      "synonymMaps": []
    }
  ],
  "semantic": {
    "defaultConfiguration": "semantic_config",
    "configurations": [
      {
        "name": "semantic_config",
        "flightingOptIn": false,
        "prioritizedFields": {
          "prioritizedContentFields": [
            {
              "fieldName": "page_chunk"
            }
          ],
          "prioritizedKeywordsFields": []
        }
      }
    ]
  },
  "vectorSearch": {
    "algorithms": [
      {
        "name": "alg",
        "kind": "hnsw",
        "hnswParameters": {
          "metric": "cosine",
          "m": 4,
          "efConstruction": 400,
          "efSearch": 500
        }
      }
    ],
    "profiles": [
      {
        "name": "hnsw_text_3_large",
        "algorithm": "alg",
        "vectorizer": "azure_openai_text_3_large"
      }
    ],
    "vectorizers": [
      {
        "name": "azure_openai_text_3_large",
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "https://YOUR-AOAI-RESOURCE.openai.azure.com",
          "deploymentId": "text-embedding-3-large",
          "apiKey": "<redacted>",
          "modelName": "text-embedding-3-large"
        }
      }
    ],
    "compressions": []
  }
}
```

**Key points**:

A well-designed index that's used for generative AI or retrieval augmented generation (RAG) structure has these components:

+ A description that an LLM or agent can use to determine whether an index should be used or skipped.

+ Chunks of human readable text that can be passed as input tokens to an LLM for answer formulation.

+ A semantic ranker configuration because agentic retrieval uses level 2 (L2) semantic ranking to identify the most relevant chunks.

+ Optionally, vector-equivalent versions of the human readable chunks of text for complementary vector search.

Chunked text is important because LLMs consume and emit tokenized strings of human readable plain text content. For this reason, you want `searchable` fields that provide plain text strings, and are `retrievable` in the response. In Azure AI Search, chunked text can be created using [built-in or third-party solutions](vector-search-how-to-chunk-documents.md).

A built-in assumption for chunked content is that the original source documents have large amounts of verbose content. If your source content is structured data, such as a product database, then your index should forego chunking and instead include fields that map to the original data source (for example, a product name, category, description, and so forth). Attribution of `searchable` and `retrievable` applies to structured data as well. Searchable makes the content in-scope for queries, and retrievable adds it to the search results (grounding data).

Vector content can be useful because it adds *similarity search* to information retrieval. At query time, when vector fields are present in the index, the agentic retrieval engine executes a vector query in parallel to the text query. Because vector queries look for similar content rather than matching words, a vector query can find a highly relevant result that a text query might miss. Adding vectors can enhance and improve the quality of your grounding data, but aren't otherwise strictly required. Azure AI Search has a [built-in approach for vectorization](vector-search-overview.md).

Vector fields are used only for query execution on Azure AI Search. You don't need the vector in results because it isn't human or LLM readable. We recommend that you set `retrievable` and `stored` to false to minimize space requirements. For more information, see [Optimize vector storage and processing](vector-search-how-to-configure-compression-storage.md).

If you use vectors, having a [vectorizer](vector-search-how-to-configure-vectorizer.md) defined in the vector search configuration is critical. It determines whether your vector field is used during query execution. The vectorizer encodes string subqueries into vectors at query time for similarity search over the vectors. The vectorizer must be the same embedding model used to create the vectors in the index.

By default, all `searchable` fields are included in query execution, and all `retrievable` fields are returned in results. You can choose which fields to use for each action in the [search index knowledge source definition](agentic-knowledge-source-how-to-search-index.md).

## Add a description

An index `description` field is a user-defined string that you can use to provide guidance to LLMs and Model Context Protocol (MCP) servers when deciding to use a specific index for a query. This human-readable text is invaluable when a system must access several indexes and make a decision based on the description. 

An index description is a schema update, and you can add it without having to rebuild the entire index.

+ String length is 4,000 characters maximum.
+ Content must be human-readable, in Unicode. Your use case should determine which language to use (for example, English or another language).

## Add a semantic configuration

The index must have at least one semantic configuration. The semantic configuration must have:

+ A named configuration.
+ A `prioritizedContentFields` set to at least one string field that is both `searchable` and `retrievable`.

There are two ways to specify a semantic configuration by name. If index has `defaultSemanticConfiguration` set to a named configuration, retrieval uses it. Alternatively, you can specify the semantic configuration inside the [search index knowledge source](agentic-knowledge-source-how-to-search-index.md).

Within the configuration, `prioritizedContentFields` is required. Title and keywords are optional. For chunked content, you might not have either. However, if you add [entity recognition](cognitive-search-skill-entity-recognition-v3.md) or [key phrase extraction](cognitive-search-skill-keyphrases.md), you might have some keywords associated with each chunk that can be useful in search scenarios, perhaps in a scoring profile.

Here's an example of a semantic configuration that works for agentic retrieval:

```json
"semantic":{
   "defaultConfiguration":"semantic_config",
   "configurations":[
      {
         "name":"semantic_config",
         "flightingOptIn":false,
         "prioritizedFields":{
            "prioritizedFields":{
               "titleField":{
                  "fieldName":""
               },
               "prioritizedContentFields":[
                  {
                     "fieldName":"page_chunk"
                  }
               ],
               "prioritizedKeywordsFields":[
                  {
                     "fieldName":"Category"
                  },
                  {
                     "fieldName":"Tags"
                  },
                  {
                     "fieldName":"Location"
                  }
               ]
            }
         }
      }
   ]
}
```

> [!NOTE]
> The response provides `title`, `terms`, and `content`, which map to the prioritized fields in this configuration.

## Add a vectorizer

If you have vector fields in the index, the query plan includes them if they're `searchable` and have a `vectorizer` assignment.

A [vectorizer](vector-search-how-to-configure-vectorizer.md) specifies an embedding model that provides text-to-vector conversions at query time. It must point to the same embedding model used to encode the vector content in your index. You can use any embedding model supported by Azure AI Search. Vectorizers are specified on vector fields by way of a *vector profile*.

Recall the **vector field definition** in the index example. Attributes on a vector field include dimensions or the number of embeddings generated by the model, and the profile.

```json
  {
    "name": "page_chunk_text_3_large", "type": "Collection(Edm.Single)",
    "searchable": true, "retrievable": false, "filterable": false, "sortable": false, "facetable": false,
    "dimensions": 3072,
    "vectorSearchProfile": "hnsw_text_3_large",
    "stored": false,
    "synonymMaps": []
  }
```

Vector profiles are configurations of vectorizers, algorithms, and compression techniques. Each vector field can only use one profile, but your index can have many in case you want unique profiles for every vector field.

Querying vectors and calling a vectorizer adds latency to the overall request, but if you want similarity search it might be worth the trade-off.

Here's an example of a vectorizer that works for agentic retrieval, as it appears in a vectorSearch configuration. There's nothing in the vectorizer definition that needs to be changed to work with agentic retrieval.

```json
"vectorSearch": {
  "algorithms": [
    {
      "name": "alg",
      "kind": "hnsw",
      "hnswParameters": {
        "metric": "cosine",
        "m": 4,
        "efConstruction": 400,
        "efSearch": 500
      }
    }
  ],
  "profiles": [
    {
      "name": "hnsw_text_3_large",
      "algorithm": "alg",
      "vectorizer": "azure_openai_text_3_large"
    }
  ],
  "vectorizers": [
    {
      "name": "azure_openai_text_3_large",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://YOUR-AOAI-RESOURCE.openai.azure.com",
        "deploymentId": "text-embedding-3-large",
        "apiKey": "<redacted>",
        "modelName": "text-embedding-3-large"
      }
    }
  ],
  "compressions": []
}  
```

## Add a scoring profile

[Scoring profiles](index-add-scoring-profiles.md) are criteria for relevance boosting. They're applied to non-vector fields (text and numbers) and are evaluated during query execution, although the precise behavior depends on the API version used to create the index. 

A scoring profile is more likely to add value to your solution if your index is based on structured data. Structured data is indexed into multiple discrete fields, which means your scoring profile can have criteria that target the content or characteristics of a specific field.

If you create the index using 2025-05-01-preview or later, the scoring profile executes last. If the index is created using an earlier API version, scoring profiles are evaluated before semantic reranking. Because agentic retrieval is available in newer preview APIs, the scoring profile executes last. The actual order of semantically ranked results is determined by the [rankingOrder property](/rest/api/searchservice/indexes/create-or-update#rankingorder) in the index, which is either set to `boostedRerankerScore` (a scoring profile was applied) or `rerankerScore` (no scoring profile).

You can use any scoring profile that makes sense for your index. Here's an example of one that boosts the search score of a match if the match is found in a specific field. Fields are weighted by boosting multipliers. For example if a match was found in the "Category" field, the boosted score is multiplied by 5.

```json
"scoringProfiles": [  
    {  
      "name": "boostSearchTerms",  
      "text": {  
        "weights": {  
          "Location": 2,  
          "Category": 5 
        }  
      }  
    }
]
```

## Add analyzers

[Analyzers](search-analyzers.md) apply to text fields and can be language analyzers or custom analyzers that control tokenization in the index, such as preserving special characters or whitespace.

Analyzers are defined within a search index and assigned to fields. The [fields collection example](#example-index-definition) includes an analyzer reference on the text chunks. In this example, the default analyzer (standard Lucene) is replaced with a Microsoft language analyzer for the English language.

```json
{
  "name": "page_chunk", "type": "Edm.String",
  "searchable": true, "retrievable": true, "filterable": false, "sortable": false, "facetable": false,
  "analyzer": "en.microsoft",
  "stored": true,
  "synonymMaps": []
}
```

## Add a synonym map

[Synonym maps](search-synonyms.md) expand queries by adding synonyms for named terms. For example, you might have scientific or medical terms for common terms.

Synonym maps are defined as a top-level resource on a search index and assigned to fields. The [fields collection example](#example-index-definition) doesn't include a synonym map, but if you had variant spellings of country names in synonym map, here's what an example might look like if it was assigned to a hypothetical "locations" field.

```json
{
    "name":"locations",
    "type":"Edm.String",
    "searchable":true,
    "synonymMaps":[ "country-synonyms" ]
}
```

## Add your index to a knowledge source

If you have a standalone index that already exists, and it isn't generated by a knowledge source, create the following objects:

+ A [searchIndex knowledge source](agentic-knowledge-source-how-to-search-index.md) to encapsulate your indexed content.

+ A [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that represents one or more knowledge sources and other instructions for knowledge retrieval.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
