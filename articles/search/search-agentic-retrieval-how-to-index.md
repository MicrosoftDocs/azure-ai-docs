---
title: Define an index for agentic retrieval
titleSuffix: Azure AI Search
description: Create an index that has fields and configurations that work for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/30/2025
---

# Define an index for agentic retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new query architecture that uses a conversational language model for query planning and parallel query execution. 

Queries are created internally. Certain aspects of those generated queries are determined by your search index. This article explains which index elements affect agentic retrieval. You can use an existing index if it meets the criteria identified in this article, even if it was created using earlier API versions.

Summarized, the search index specified in the `targetIndexes` of an [agent definition](search-agentic-retrieval-how-to-create.md) must have these elements:

+ String fields attributed as `searchable` and `retrievable`
+ A semantic configuration, with a `defaultSemanticConfiguration`
+ A vectorizer if you want to include vector queries in the pipeline

Optionally, the following index elements increase your opportunities for optimization:

+ `scoringProfile` with a `defaultScoringProfile`, for boosting relevance
+ `synonymMaps` for terminology or jargon
+ `analyzers` for linguistics rules or patterns (like whitespace preservation, or special characters)

## Example index definition

Here's an example index that works for agentic retrieval. It meets the criteria for required elements.

```json
{
  "name": "earth_at_night",
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
      "name": "page_chunk_text_3_large", "type": "Collection(Edm.Single)",
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
  "scoringProfiles": [],
  "suggesters": [],
  "analyzers": [],
  "normalizers": [],
  "tokenizers": [],
  "tokenFilters": [],
  "charFilters": [],
  "similarity": {
    "@odata.type": "#Microsoft.Azure.Search.BM25Similarity"
  },
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

Recall that the large language model (LLM) is used twice. First, it's used to create a query plan. After the query plan is executed, search results are passed to the LLM again, this time as grounding data. LLMs consume and emit tokenized strings of human readable plain text content. The fields in this index support model usage by providing plain text strings that are both `searchable` and `retrievable` in the response.

This index includes a vector field that's used at query time. You don't need the vector in results because it isn't human or LLM readable, but it does need to be searchable. Since you don't need vectors in the response, both `retrievable` and `stored` are false. 

The vectorizer defined in the vector search configuration is critical. It encodes subqueries into vectors at query time for similarity search over the vectors. The vectorizer must be the same embedding model used to create the vectors in the index.

<!-- 
> [!div class="checklist"]
> + A fields collection with `searchable` text and vetor fields, and `retrievable` text fields
> + Vector fields that are queried are fields having a vectorizer
> + Fields selected in the response string are semantic fields (title, terms, content)
> + Fields in reference source data are all `retrievable` fields, assuming reference source data is true -->

## Add a semantic configuration

The index must have at least one semantic configuration. The semantic configuration must have:

+ A `defaultSemanticConfiguration` set to a named configuration.
+ A `prioritizedContentFields` set to at least one string field that is both `searchable` and `retrievable`.

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

Querying vectors and calling a vectorizer adds latency to the overall request, but if you want similarity search it might be worth the trade off.

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

If you create the index using 2025-05-01-preview, the scoring profile executes last. If the index is created using an earlier API version, scoring profiles are evaluated before semantic reranking.

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

Analyzers are defined within a search index and assigned to fields. The [fields collection example](#example-index-definition) includes an analyzer reference on the text chunks. In this example, the default analyzer (standard Lucene) is replaced with a Microsoft language analyzer.

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

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
