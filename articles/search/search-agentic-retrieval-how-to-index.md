---
title: Create an index for agentic retrieval
titleSuffix: Azure AI Search
description: Create an index for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/30/2025
---

# Create an index for agentic retrieval in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query processing architecture that uses a conversational language model for query planning and execution. 

Queries are created internally. Certain aspects of those internally created queries are determined by your search index. This article describes the index elements affecting agentic retrieval.

You can use an existing index if it meets the criteria. Summarized, the search index specified in `targetIndexes` of an [agent definition](search-agentic-retrieval-how-to-create.md) must have these elements:

+ Fields attributed as `searchable` and `retrievable`
+ `semanticConfiguration`, with a `defaultSemanticConfiguration`
+ `vectorizers`, but only if you want vector fields in your query
+ `scoringProfile` (optional), with a `defaultScoringProfile`
+ `synonymMaps` (optional) if you want more control over query expansion

## Add fields

Recall that the large language model (LLM) is used twice. First, it's used to create a query plan. After the query plan is executed, search results are passed to the LLM again, this time as grounding data. LLMs consume and emit human readable plain text.

Required:

+ You must have at least some string fields (`Edm.String`, `Collection(Edm.String)`, string subfields of `Edm.ComplexType`) to meet the requirements of semantic reranking and LLMs.
+ Only `searchable` fields are included in a query plan.
+ Only `retrievable` fields are returned in a query response sent to the LLM as grounding data. Also, fields must be retrievable if you want you them included in the reference source data portion of the retrieval response.

Optional:

+ Vector fields are used if you specify a `vectorizer` to encode text inputs for vector search
+ Text fields can also specify `synonymMaps` if that feature is useful for your scenario

Here's an example of a fields collection that works for agentic retrieval:

```json
 index_name = "earth-book"
 index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE, credential=credential)  
 fields = [
     SearchField(name="parent_id", type=SearchFieldDataType.String),  
     SearchField(name="title", type=SearchFieldDataType.String),
     SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
     SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
     SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
     SearchField(name="text_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1024, vector_search_profile_name="myHnswProfile")
     ]  
```

<!-- 
> [!div class="checklist"]
> + A fields collection with `searchable` text and vetor fields, and `retrievable` text fields
> + Vector fields that are queried are fields having a vectorizer
> + Fields selected in the response string are semantic fields (title, terms, content)
> + Fields in reference source data are all `retrievable` fields, assuming reference source data is true -->

## Add a semantic configuration

The index must have:

> [!div class="checklist"]
> + At least one `semanticConfiguration`
> + Within the configuration, `content` is required. `title` and `keyword` are recommended but optional
> + A named configuration for `defaultSemanticConfiguration`

Here's an example of a semantic configuration that's works for agentic retrieval:

```json
"semantic": {
  "configurations": [
    {
      "name": "my-semantic-config",
      "flightingOptIn": false,
      "prioritizedFields": {
        "titleField": {
          "fieldName": "HotelName"
        },
        "prioritizedContentFields": [
          {
            "fieldName": "Description"
          }
        ],
        "prioritizedKeywordsFields": [
          {
            "fieldName": "Category"
          },
          {
            "fieldName": "Tags"
          },
          {
            "fieldName": "Address/City"
          }
        ]
      }
    }
  ]
}
```

> [!NOTE]
> The response provides `title`, `terms`, and `content`, where `terms` is an alias for `keywords`.

## Add a vectorizer

If you have vector fields that you want to include in the query, the index must have:

> [!div class="checklist"]
> + A vectorizer that points to the same embedding model used to encode the vector content in your index
> + A vector profile that includes the vectorizer
> + A vector field that uses the vector profile

You can use any embedding model supported by Azure AI Search. This model is accessed at query time and adds latency to the overall request.

Here's an example of a vectorizer that's works for agentic retrieval:

```json
vector_search = VectorSearch(  
    algorithms=[  
        HnswAlgorithmConfiguration(name="my-hnsw-algorithm"),
    ],  
    profiles=[  
        VectorSearchProfile(  
            name="my-vector-profile",  
            algorithm_configuration_name="my-hnsw-algorithm",  
            vectorizer_name="my-vectorizer",  
        )
    ],  
    vectorizers=[  
        AzureOpenAIVectorizer(  
            vectorizer_name="my-vectorizer",  
            kind="azureOpenAI",  
            parameters=AzureOpenAIVectorizerParameters(  
                resource_url=AZURE_OPENAI_ACCOUNT,  
                deployment_name="text-embedding-3-large",
                model_name="text-embedding-3-large"
            ),
        ),  
    ], 
)  
```

## Add a scoring profile

[Scoring profiles](index-add-scoring-profiles) are criteria for relevance boosting. They're applied to non-vector fields (text and numbers) and are evaluated last during query execution, although the precise behavior depends on the API version used to create the index.

If you create the index using 2025-05-01-preview, the scoring profile executes last. If the index is an earlier version, scoring profiles are evaluated before semantic reranking.

Here's an example of a scoring profile that's works for agentic retrieval:

```json
"scoringProfiles": [
  {  
    "name":"geo",
    "text": {  
      "weights": {  
        "hotelName": 5
      }                              
    },
    "functions": [
      {  
        "type": "distance",
        "boost": 5,
        "fieldName": "location",
        "interpolation": "logarithmic",
        "distance": {
          "referencePointParameter": "currentLocation",
          "boostingDistance": 10
        }                        
      }                                      
    ]                     
  }            
]
```

## Add analyzers

[Analyzers](search-analyzers.md) apply to text fields and can be language analyzers or custom analyzers that control tokenization in the index, such as preserving special characters or whitespace.

Analyzers are defined within a search index and assigned to fields. The [fields collection example](#add-fields) includes an analyzer reference.

## Add a synonym map

[Synonym maps](search-synonyms.md) expand queries by adding synonyms for named terms. For example, you might have scientific or medical terms for common terms.

Synonym maps are defined as a top-level resource on a search index and assigned to fields. The [fields collection example](#add-fields) includes a synonym map reference.

<!-- ## Prerequisites

+ An [agent definition](search-agentic-retrieval-how-to-create.md) that represents a conversational language model, used during query planning and execution.

+ Azure AI Search with a managed identity for role-based access to a chat model.

+ Region requirements. Azure AI Search and your model should be in the same region.

+ API requirements. Use 2025-05-01-preview data plane REST API or a prerelease package of an Azure SDK that provides Agent APIs.

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search. -->

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
