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

   A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK` or `201 Created`, you're ready for the next steps.

1. Send the remaining requests in sequence to create an index, upload documents, and query the index.

### Output

Each query request returns JSON results. For example, the single vector search returns results like this:

```json
{
    "@odata.count": 7,
    "value": [
        {
            "@search.score": 0.857736,
            "HotelId": "48",
            "HotelName": "Nordick's Valley Motel",
            "Description": "Only 90 miles (about 2 hours) from the nation's capital...",
            "Category": "Boutique"
        },
        {
            "@search.score": 0.8399129,
            "HotelId": "49",
            "HotelName": "Swirling Currents Hotel",
            "Description": "Spacious rooms, glamorous suites and residences...",
            "Category": "Luxury"
        }
    ]
}
```

The vector query string is "quintessential lodging near running trails, eateries, retail", which is semantically similar to "historic hotel walk to restaurants and shopping" but uses different terms. Vector search finds relevant results even without matching keywords.

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

[!INCLUDE [understand code note](../understand-code-note.md)]

### Create a vector index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured. This quickstart calls [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) to build a vector index named `hotels-vector-quickstart` and its physical data structures on your search service.

The index schema is organized around hotel content. Sample data consists of vector and nonvector descriptions of fictitious hotels. The following excerpt shows the key structure of the `### Create a new index` request in the `.rest` file:

```http
POST {{baseUrl}}/indexes?api-version=2025-09-01  HTTP/1.1
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

+ The `fields` collection includes a required key field and text and vector fields (such as `Description` and `DescriptionVector`) for text and vector search. Colocating vector and nonvector fields in the same index enables hybrid queries. For instance, you can combine filters, text search with semantic ranking, and vectors into a single query operation.

+ Vector fields must be one of the [EDM data types used for vectors](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields), such as `type: Collection(Edm.Single)`. Vector fields also have `dimensions` and `vectorSearchProfile` properties. Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

+ The `vectorSearch` section is an array of Approximate Nearest Neighbor (ANN) algorithm configurations and profiles. Supported algorithms include Hierarchical Navigable Small World (HNSW) and exhaustive K-Nearest Neighbor. For more information, see [Relevance scoring in vector search](../../vector-search-ranking.md).

+ The (optional) `semantic` configuration enables reranking of search results. You can rerank results in queries of type `semantic` for string fields that are specified in the configuration. To learn more, see [Semantic ranking overview](../../semantic-search-overview.md).

### Upload documents to the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents as inline JSON. In production scenarios, however, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

This quickstart calls [Documents - Index (REST API)](/rest/api/searchservice/documents/) to add sample hotel documents to your index. The following excerpt shows the structure of the `### Upload 7 documents` request:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/index?api-version=2025-09-01  HTTP/1.1
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

+ Vector fields contain floating point values. Each document includes a `DescriptionVector` field with 1,536 embeddings, which is the size generated by the `text-embedding-ada-002` model.

### Query the index

The queries in the sample file demonstrate different search patterns. The example vector queries are based on two strings:

+ Full-text search string: "historic hotel walk to restaurants and shopping"
+ Vector query string: "quintessential lodging near running trails, eateries, retail" (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but includes terms that don't exist in the search index. If you do a keyword search for "quintessential lodging near running trails, eateries, retail", results are zero. This example shows how vector search finds relevant results even without matching keywords.

#### Single vector search

The `### Run a single vector query` request demonstrates a basic scenario where you want to find document descriptions that closely match the search string:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2025-09-01  HTTP/1.1
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

Key takeaways about [Documents - Search Post](/rest/api/searchservice/documents/search-post) (REST API):

+ The `vectorQueries.vector` is the vector query string. It's a vector representation of "quintessential lodging near running trails, eateries, retail", which is vectorized into 1,536 embeddings for this query.

+ `fields` determines which vector fields are searched.

+ `kind` set to `vector` means that the query string is a vector. If `kind` was set to `text`, you would need extra capability (a [vectorizer](../../vector-search-how-to-configure-vectorizer.md)) to encode a human readable text string into a vector at query time. Vectorizers are omitted from this quickstart to keep the exercise simple.

+ `k` specifies the number of matches to return in the response. A `count` parameter specifies the number of matches found in the index. Including count is a best practice for queries, but it's less useful for similarity search where the algorithm can find some degree of similarity in almost any document.

The response includes k-5 results although the search engine found 7 matches. The top results are considered the most semantically similar to the query. Each result provides a search score and the fields listed in `select`. In a similarity search, the response always includes `k` results ordered by the similarity score.

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `### Run a vector query with a filter` request filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2025-09-01  HTTP/1.1
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

This search returns only hotels that provide free Wi-Fi.

#### Single vector search with geo filter

You can also apply a geo filter to limit results to a specific geographic area. The `### Run a vector query with a geo filter` request limits results to hotels within 300 kilometers of Washington D.C.:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2025-09-01  HTTP/1.1
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

This search returns only hotels within 300 kilometers of the specified coordinates.

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. The `### Run a hybrid query` request runs the full-text and vector query strings concurrently:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2025-09-01  HTTP/1.1
Content-Type: application/json
Authorization: Bearer {{token}}

{
    "count": true,
    "search": "historic hotel walk to restaurants and shopping",
    "select": "HotelId, HotelName, Category, Tags, Description",
    "top": 5,
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

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

This example adds [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding. The `### Run a hybrid query with semantic reranking` request adds semantic ranking:

```http
POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2025-09-01  HTTP/1.1
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

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, you can send the following request to delete the index you created in this quickstart.

```http
### Delete an index
DELETE  {{baseUrl}}/indexes/hotels-vector-quickstart?api-version=2025-09-01 HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}
```
