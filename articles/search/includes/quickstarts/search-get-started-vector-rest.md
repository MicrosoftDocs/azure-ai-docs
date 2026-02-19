---
manager: nitinme
author: haileytapia
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/05/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to create, load, and query a [vector index](../../vector-store.md).

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

- [Git](https://git-scm.com/downloads) to clone the sample repository.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-rest-samples
   ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

   ```bash
   cd azure-search-rest-samples/Quickstart-vectors
   code .
   ```

1. In `az-search-quickstart-vectors.rest`, replace the placeholder value for `@baseUrl` with the URL you obtained in [Get endpoint](#get-endpoint).

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

1. For keyless authentication with Microsoft Entra ID, generate an access token.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv
    ```

1. Replace the placeholder value for `@token` with the access token from the previous step.

## Run the code

1. Under `### List existing indexes by name`, select **Send Request** to verify your connection.

   A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK`, you're ready to proceed.

1. Send the remaining requests sequentially to create a vector index, upload documents, and run different types of vector queries.

### Output

Each query request returns JSON results. The following example is the output of the `### Run a single vector query` request, which shows vector search results ranked by similarity score.

```json
{
  "@odata.count": 5,
  "value": [
    {
      "@search.score": 0.6605852,
      "HotelId": "48",
      "HotelName": "Nordick's Valley Motel",
      "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer. Hiking? Wine Tasting? Exploring the caverns? It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
      "Category": "Boutique",
      "Tags": [
        "continental breakfast",
        "air conditioning",
        "free wifi"
      ]
    },
    {
      "@search.score": 0.6333684,
      "HotelId": "13",
      "HotelName": "Luxury Lion Resort",
      "Description": "Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.",
      "Category": "Luxury",
      "Tags": [
        "bar",
        "concierge",
        "restaurant"
      ]
    },
    {
      "@search.score": 0.605672,
      "HotelId": "4",
      "HotelName": "Sublime Palace Hotel",
      "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.",
      "Category": "Boutique",
      "Tags": [
        "concierge",
        "view",
        "air conditioning"
      ]
    },
    {
      "@search.score": 0.6026341,
      "HotelId": "49",
      "HotelName": "Swirling Currents Hotel",
      "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs.",
      "Category": "Suite",
      "Tags": [
        "air conditioning",
        "laundry service",
        "24-hour front desk service"
      ]
    },
    {
      "@search.score": 0.57902366,
      "HotelId": "2",
      "HotelName": "Old Century Hotel",
      "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
      "Category": "Boutique",
      "Tags": [
        "pool",
        "free wifi",
        "air conditioning",
        "concierge"
      ]
    }
  ]
}
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured. This quickstart calls [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) to build a vector index named `hotels-vector-quickstart` and its physical data structures on your search service.

The index schema is organized around hotel content. Sample data consists of vector and nonvector descriptions of fictitious hotels. The following excerpt shows the key structure of the `### Create a new index` request.

```http
PUT {{baseUrl}}/indexes/hotels-vector-quickstart?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "name": "hotels-vector-quickstart",
    "fields": [
        { "name": "HotelId", "type": "Edm.String", "key": true, "filterable": true },
        { "name": "HotelName", "type": "Edm.String", "searchable": true },
        { "name": "Description", "type": "Edm.String", "searchable": true },
        {
            "name": "DescriptionVector",
            "type": "Collection(Edm.Single)",
            "searchable": true,
            "dimensions": 1536,
            "vectorSearchProfile": "my-vector-profile"
        },
        { "name": "Category", "type": "Edm.String", "filterable": true, "facetable": true },
        { "name": "Tags", "type": "Collection(Edm.String)", "filterable": true, "facetable": true }
        // Additional fields omitted for brevity
    ],
    "vectorSearch": {
        "algorithms": [
            { "name": "hnsw-vector-config", "kind": "hnsw" }
        ],
        "profiles": [
            { "name": "my-vector-profile", "algorithm": "hnsw-vector-config" }
        ]
    },
    "semantic": {
        "configurations": [
            {
                "name": "semantic-config",
                "prioritizedFields": {
                    "titleField": { "fieldName": "HotelName" },
                    "prioritizedContentFields": [{ "fieldName": "Description" }]
                }
            }
        ]
    }
}
```

Key takeaways:

+ This particular index supports multiple search capabilities:

    + [Full-text search](../../search-lucene-query-architecture.md) (fields with `searchable` set to `true`)

    + [Vector search](../../vector-search-overview.md) (`DescriptionVector` with `vectorSearchProfile`)

    + [Semantic ranking](../../semantic-search-overview.md) (`semantic` configuration)

    + [Faceted search](../../search-faceted-navigation.md) (fields with `facetable` set to `true`)

    + [Geo-spatial search](../../search-query-odata-geo-spatial-functions.md) (`Location` field with `Edm.GeographyPoint`)

    + [Filtering](../../search-filters.md) and sorting (fields with `filterable` and `sortable` set to `true`)

+ The `dimensions` property must match the output size of your embedding model. This quickstart uses 1,536 dimensions to match the `text-embedding-ada-002` model.

+ The `vectorSearch` section defines the Approximate Nearest Neighbor (ANN) algorithm. Supported algorithms include Hierarchical Navigable Small World (HNSW) and exhaustive K-Nearest Neighbor (KNN). For more information, see [Relevance in vector search](../../vector-search-ranking.md).

### Upload documents to the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents as inline JSON. In production scenarios, however, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

This quickstart calls [Documents - Index (REST API)](/rest/api/searchservice/documents/) to add sample hotel documents to your index. The following excerpt shows the structure of the `### Upload 7 documents` request.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/index?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "value": [
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "1",
            "HotelName": "Stay-Kay City Hotel",
            "Description": "This classic hotel is ideally located on the main commercial artery of the city...",
            "DescriptionVector": [-0.0347, 0.0289, ... ],  // 1536 floats
            "Category": "Boutique",
            "Tags": ["view", "air conditioning", "concierge"],
            "ParkingIncluded": false,
            "Rating": 3.60,
            "Address": { "City": "New York", "StateProvince": "NY" },
            "Location": { "type": "Point", "coordinates": [-73.975403, 40.760586] }
        }
        // Additional documents omitted for brevity
    ]
}
```

Key takeaways:

+ Each document in the `value` array represents a hotel and contains fields that match the index schema. The `@search.action` parameter specifies the operation to perform for each document. This quickstart uses `mergeOrUpload`, which adds the document if it doesn't exist or updates the document if it does exist.

+ Documents in the payload consist of fields defined in the index schema.

### Query the index

The queries in the sample file demonstrate different search patterns. The example vector queries are based on two strings:

+ Full-text search string: `"historic hotel walk to restaurants and shopping"`

+ Vector query string: `"quintessential lodging near running trails, eateries, retail"` (vectorized into a mathematical representation)

The vector query string is semantically similar to the full-text search string, but it includes terms that don't exist in the index. A keyword-only search for the vector query string returns zero results. However, vector search finds relevant matches based on meaning rather than exact keywords.

The following examples start with a basic vector query and progressively add filters, keyword search, and semantic reranking.

#### Single vector search

The `### Run a single vector query` request demonstrates a basic scenario where you want to find document descriptions that closely match the vector query string. The `vectorQueries` array configures the vector search:

+ `k` limits how many results are returned based on vector similarity.
+ `fields` specifies the vector field to search against.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "select": "HotelId, HotelName, Description, Category, Tags",
    "vectorQueries": [
        {
            "vector": [ ... ],  // 1536-dimensional vector of "quintessential lodging near running trails, eateries, retail"
            "k": 5,
            "fields": "DescriptionVector",
            "kind": "vector",
            "exhaustive": true
        }
    ]
}
```

#### Single vector search with a filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `### Run a vector query with a filter` request filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "select": "HotelId, HotelName, Description, Category, Tags",
    "filter": "Tags/any(tag: tag eq 'free wifi')",
    "vectorFilterMode": "postFilter",
    "vectorQueries": [
        {
            "vector": [ ... ],  // 1536-dimensional vector
            "k": 7,
            "fields": "DescriptionVector",
            "kind": "vector",
            "exhaustive": true
        }
    ]
}
```

#### Single vector search with a geo filter

You can specify a [geo-spatial filter](../../search-query-odata-geo-spatial-functions.md) to limit results to a specific geographic area. The `### Run a vector query with a geo filter` request specifies a geographic point (Washington D.C., using longitude and latitude coordinates) and returns hotels within 300 kilometers. The `vectorFilterMode` parameter determines when the filter runs. In this case, `postFilter` runs the filter after the vector search.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "select": "HotelId, HotelName, Address/City, Address/StateProvince, Description",
    "filter": "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
    "vectorFilterMode": "postFilter",
    "top": 5,
    "facets": [ "Address/StateProvince"],
    "vectorQueries": [
        {
            "vector": [ ... ],  // 1536-dimensional vector
            "k": 5,
            "fields": "DescriptionVector",
            "kind": "vector",
            "exhaustive": true
        }
    ]
}
```

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines full-text and vector queries in a single request. The `### Run a hybrid query` request runs both query types concurrently, and then uses Reciprocal Rank Fusion (RRF) to merge the results into a unified ranking. RRF uses the inverse of result rankings from each result set to produce a merged ranking. Notice that hybrid search scores are uniformly smaller than single-query scores.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "search": "historic hotel walk to restaurants and shopping",
    "select": "HotelId, HotelName, Category, Tags, Description",
    "top": 5,
    "vectorQueries": [
        {
            "vector": [ ... ],  // 1536-dimensional vector
            "k": 5,
            "fields": "DescriptionVector",
            "kind": "vector",
            "exhaustive": true
        }
    ]
}
```

#### Semantic hybrid search

The `### Run a hybrid query with semantic reranking` request demonstrates [semantic ranking](../../semantic-search-overview.md), which reranks results based on language understanding.

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version={{api-version}}  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "search": "historic hotel walk to restaurants and shopping",
    "select": "HotelId, HotelName, Category, Description",
    "queryType": "semantic",
    "semanticConfiguration": "semantic-config",
    "top": 5,
    "vectorQueries": [
        {
            "vector": [ ... ],  // 1536-dimensional vector
            "k": 7,
            "fields": "DescriptionVector",
            "kind": "vector",
            "exhaustive": true
        }
    ]
}
```

Compare these results with the hybrid search results from the previous query. Without semantic reranking, Sublime Palace Hotel ranks first because Reciprocal Rank Fusion (RRF) combines the text and vector scores to produce a merged result. After semantic reranking, Swirling Currents Hotel moves to the top spot.

The semantic ranker uses machine comprehension models to evaluate how well each result matches the intent of the query. Swirling Currents Hotel's description mentions `"walking access to shopping, dining, entertainment and the city center"`, which aligns closely with the search query's `"walk to restaurants and shopping"`. This semantic match for nearby dining and shopping elevates it above Sublime Palace Hotel, which doesn't emphasize walkable amenities in its description.

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters and semantic ranking apply to textual content only, not vectors.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, you can send the `### Delete an index` request to delete the index you created in this quickstart.

