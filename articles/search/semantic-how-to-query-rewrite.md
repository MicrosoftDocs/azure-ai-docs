---
title: Rewrite queries with semantic ranker in Azure AI Search
titleSuffix: Azure AI Search
description: Learn how to rewrite queries with semantic ranker in Azure AI Search
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 11/19/2024
---

# Rewrite queries with semantic ranker in Azure AI Search (Preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Query rewriting is the process of transforming a user's query into a more effective one. The search service sends the search query (or a variation of it) to a generative model that generates alternative queries.

Search with query rewriting works like this: 
- The user query is sent via the `search` property in the request.
- The search service sends the search query (or a variation of it) to a generative model that generates alternative queries.
- The search service uses the original query and the rewritten queries to retrieve search results.

Query rewriting is an optional feature. Without query rewriting, the search service just uses the original query to retrieve search results. 

## Prerequisites

+ A search service, Basic tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md). Review [semantic ranking](semantic-search-overview.md) if you need an introduction to the feature. 

> [!IMPORTANT]
> Semantic ranker is currently required for query rewriting.

+ An existing search index with a [semantic configuration](semantic-how-to-configure.md) and rich text content. The examples in this guide use the [hotels-sample-index](search-get-started-portal.md) sample data to demonstrate query rewriting. You can use your own data and index to test query rewriting.

+ You need a web client that supports REST API requests. The examples in this guide were tested with [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension. 

> [!TIP]
> Content that includes explanations or definitions work best for semantic ranking. 

## Make a search request with query rewrites

In this REST API example, we use [Search Documents](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-11-01-preview&branch=searchindex202411&preserve-view=true) to formulate the request. For more information about the request and response properties, see the [API reference documentation](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-11-01-preview&branch=searchindex202411&preserve-view=true).

1. Paste the following request into a web client as a template. 

    ```http
    POST https://[search-service-name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2024-11-01-preview
    {
        "search": "newer hotel near the water with a great restaurant",
        "semanticConfiguration":"en-semantic-config",
        "queryType":"semantic",
        "queryRewrites":"generative|count-5",
        "queryLanguage":"en",
        "debug":"queryRewrites",
        "top": 1
    }
    ```

    - You replace `search-service-name` with your search service name.
    - You replace `hotels-sample-index` with your index name if it's different. 
    - We set "search" to a full text search query. The search property is required for query rewriting, unless you specify [vector queries](#vector-queries-with-query-rewrite). If you specify vector queries, then the "search" text must match the `"text"` property of the `"vectorQueries"` object. Your search string can support either the [simple syntax](query-simple-syntax.md) or [full Lucene syntax](query-lucene-syntax.md).
    - We set "semanticConfiguration" to a [predefined semantic configuration](semantic-how-to-configure.md) embedded in your index.
    - We set "queryType" to "semantic". We either need to set "queryType" to "semantic" or include a nonempty "semanticQuery" property in the request. [Semantic ranking](semantic-search-overview.md) is required for query rewriting.
    - We set "queryRewrites" to "generative|count-5" to get up to five query rewrites. You can set the count to any value between 1 and 10. 
    - We set "queryLanguage" to the target language ("en") of the query rewrites. 
    - We set "debug" to "queryRewrites" to get the query rewrites in the response. Set the `"debug": "queryRewrites"` property for testing purposes. For better performance, don't use debug in production.
    - We set "top" to 1 to return only the top search result. 
    
1. Send the request to execute the query and return results.

Next, we evaluate the search results with the query rewrites.

## Evaluate the response

Here's an example of a response that includes query rewrites:

```json
"@search.debug": {
  "semantic": null,
  "queryRewrites": {
    "text": {
      "inputQuery": "newer hotel near the water with a great restaurant",
      "rewrites": [
        "new waterfront hotels with top-rated eateries",
        "new waterfront hotels with top-rated restaurants",
        "new waterfront hotels with excellent dining",
        "new waterfront hotels with top-rated dining",
        "new water-side hotels with top-rated restaurants"
      ]
    },
    "vectors": []
  }
},
"value": [
  {
    "@search.score": 58.992092,
    "@search.rerankerScore": 2.815633535385132,
    "HotelId": "18",
    "HotelName": "Ocean Water Resort & Spa",
    "Description": "New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.",
    "Description_fr": "Nouvel h\u00f4tel de luxe pour des vacances inoubliables. Vue sur la baie depuis chaque chambre, emplacement pr\u00e8s de la jet\u00e9e, piscine sur le toit, restaurant au bord de l'eau et plus encore.",
    "Category": "Luxury",
    "Tags": [
      "view",
      "pool",
      "restaurant"
    ],
    "ParkingIncluded": true,
    "LastRenovationDate": "2020-11-14T00:00:00Z",
    "Rating": 4.2,
    "Location": {
      "type": "Point",
      "coordinates": [
        -82.537735,
        27.943701
      ],
      "crs": {
        "type": "name",
        "properties": {
          "name": "EPSG:4326"
        }
      }
    },
    //... more properties redacted for brevity
  }
]
```

Here are some key points to note:
- Because we set the "debug" property to "queryRewrites", the response includes a `@search.debug` object with the text input query and query rewrites. 
- Because we set the "queryRewrites" property to "generative|count-5", the response includes up to five query rewrites.
- The `"inputQuery"` value is the query sent to the generative model for query rewriting. The input query isn't always the same as the user's `"search"` query.
- The top search score (58.992092) can be considerably higher than the search score without query rewrites.

Here's an example of a response without query rewrites. If you don't use query rewrites for this specific query and sample data, the top search score (7.774868) is lower than the search score with query rewrites. 

```json
"@search.debug": {
  "semantic": null,
  "queryRewrites": {
    "text": {
      "inputQuery": "",
      "rewrites": []
    },
    "vectors": []
  }
},
"value": [
  {
    "@search.score": 7.774868,
    "@search.rerankerScore": 2.815633535385132,
    "HotelId": "18",
    "HotelName": "Ocean Water Resort & Spa",
    "Description": "New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.",
    "Description_fr": "Nouvel h\u00f4tel de luxe pour des vacances inoubliables. Vue sur la baie depuis chaque chambre, emplacement pr\u00e8s de la jet\u00e9e, piscine sur le toit, restaurant au bord de l'eau et plus encore.",
    "Category": "Luxury",
    "Tags": [
      "view",
      "pool",
      "restaurant"
    ],
    "ParkingIncluded": true,
    "LastRenovationDate": "2020-11-14T00:00:00Z",
    "Rating": 4.2,
    "Location": {
      "type": "Point",
      "coordinates": [
        -82.537735,
        27.943701
      ],
      "crs": {
        "type": "name",
        "properties": {
          "name": "EPSG:4326"
        }
      }
    },
    //... more properties redacted for brevity
  }
]
```

## Vector queries with query rewrite

You can include vector queries in your search request to combine keyword search and vector search into a single request and a unified response.

Here's an example of a query that includes a vector query with query rewrites. We modified a [previous example](#make-a-search-request-with-query-rewrites) to include a vector query.

```http
POST https://[search-service-name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2024-11-01-preview
{
    "search": "newer hotel near the water with a great restaurant",
    "vectorQueries": [
        {
            "kind": "text",
            "text": "newer hotel near the water with a great restaurant",
            "k": 50,
            "fields": "Description",
            "queryRewrites": "generative|count-3"
        }
    ],
    "semanticConfiguration":"en-semantic-config",
    "queryType":"semantic",
    "queryRewrites":"generative|count-5",
    "queryLanguage":"en",
    "debug":"queryRewrites",
    "top": 1
}
```

Here are some key points to note:
- We added a "vectorQueries" object to the request. This object includes a vector query with the "kind" set to "text". 
- The "text" value is the same as the "search" value. These values must be identical for query rewriting to work.
    
The response includes query rewrites for both the text query and the vector query. 

## Debugging query rewrites

You should test your query rewrites to ensure that they're working as expected. Set the `"debug": "queryRewrites"` property in your query request to get the query rewrites in the response. Setting `"debug"` is optional for testing purposes. For better performance, don't set this property in production.

You might observe that the response includes an empty array for the `text.rewrites` and `vectors` properties.

```json
{
  "@odata.context": "https://demo-search-svc.search.windows.net/indexes('hotels-sample-index')/$metadata#docs(*)",
  "@search.debug": {
    "semantic": null,
    "queryRewrites": {
      "text": {
        "rewrites": []
      },
      "vectors": []
    }
  },
  "@search.semanticPartialResponseReason": "Transient",
  "@search.semanticQueryRewriteResultType": "OriginalQueryOnly",
  //... more properties redacted for brevity
}
```

In the preceding example, the response includes a `@search.semanticPartialResponseReason` property with a value of "Transient". This message means that at least one of the queries failed to complete. The response also includes a `@search.semanticQueryRewriteResultType` property with a value of "OriginalQueryOnly". This message means that the query rewrites are unavailable. Only the original query is used to retrieve search results.

## Next steps

Semantic ranking can be used in hybrid queries that combine keyword search and vector search into a single request and a unified response.

> [!div class="nextstepaction"]
> [Hybrid query with semantic ranker](hybrid-search-how-to-query.md#semantic-hybrid-search)