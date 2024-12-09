---
title: Quickstart vector search
titleSuffix: Azure AI Search
description: In this quickstart, learn how to call the Azure AI Search REST APIs for vector workloads.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 12/03/2024
---

# Quickstart: Vector search by using REST

Learn how to use the [Search REST APIs](/rest/api/searchservice) to create, load, and query vectors in Azure AI Search.

In Azure AI Search, a [vector store](vector-store.md) has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. The [Create Index](/rest/api/searchservice/indexes/create-or-update) REST API creates the vector store.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.

> [!NOTE]
> This quickstart omits the vectorization step and provides embeddings in sample documents. If you want to add [built-in data chunking and vectorization](vector-search-integrated-vectorization.md) over your own content, try the [**Import and vectorize data** wizard](search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

- [Azure AI Search](search-what-is-azure-search.md), in any region and on any tier. You can use the Free tier for this quickstart, but Basic or higher is recommended for larger data files. [Create](search-create-service-portal.md) or [find an existing Azure AI Search resource](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) under your current subscription.

  Most existing services support vector search. For a small subset of services created prior to January 2019, an index that contains vector fields fails on creation. In this situation, a new service must be created.

- Optionally, to run the query example that invokes [semantic reranking](semantic-search-overview.md), your search service must be the Basic tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

## Download files

[Download a REST sample](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors) from GitHub to send the requests in this quickstart. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

You can also start a new file on your local system and create requests manually by using the instructions in this article.

## Get a search endpoint and an API key

You can find the search service endpoint and API keys in the Azure portal. You're pasting these values into a `.rest` or `.http` file in the next step.

Requests to the search endpoint must be authenticated and authorized. You can use API keys or roles for this task. Keys are easier to start with, but roles are more secure. Although we use API keys for this quickstart, we recommend [switching to a keyless connection](search-get-started-rbac.md).

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, find the URL. An example endpoint might look like `https://mydemo.search.windows.net`. 

   :::image type="content" source="media/search-get-started-rest/get-endpoint.png" lightbox="media/search-get-started-rest/get-endpoint.png" alt-text="Screenshot of the URL property on the overview page.":::

1. Select **Settings** > **Keys**. Either **API keys** or **Both** must be enabled. [Admin API keys](search-security-api-keys.md) are used to add, modify, and delete objects. There are two interchangeable admin keys. Copy either one.

   :::image type="content" source="media/search-get-started-rest/get-api-key.png" lightbox="media/search-get-started-rest/get-api-key.png" alt-text="Screenshot that shows the API keys in the Azure portal.":::

## Create a vector index

[Create Index (REST)](/rest/api/searchservice/indexes/create) creates a vector index and sets up the physical data structures on your search service.

The index schema is organized around hotel content. Sample data consists of vector and nonvector names and descriptions of seven fictitious hotels. This schema includes configurations for vector indexing and queries, and for semantic ranking.

1. Create a new text file in Visual Studio Code.

1. At the top of the file, add variables for the values you collected earlier.

   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
   @apiKey = PUT-YOUR-ADMIN-KEY-HERE
   ```

1. Save the file with a `.rest` or `.http` file extension.

1. Paste in the following example to create the `hotels-vector-quickstart` index on your search service.

    ```http
    ### Create a new index
    POST {{baseUrl}}/indexes?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        api-key: {{apiKey}}
    
    {
        "name": "hotels-vector-quickstart",
        "fields": [
            {
                "name": "HotelId", 
                "type": "Edm.String",
                "searchable": false, 
                "filterable": true, 
                "retrievable": true, 
                "sortable": false, 
                "facetable": false,
                "key": true
            },
            {
                "name": "HotelName", 
                "type": "Edm.String",
                "searchable": true, 
                "filterable": false, 
                "retrievable": true, 
                "sortable": true, 
                "facetable": false
            },
            {
                "name": "HotelNameVector",
                "type": "Collection(Edm.Single)",
                "searchable": true,
                "retrievable": true,
                "dimensions": 1536,
                "vectorSearchProfile": "my-vector-profile"
            },
            {
                "name": "Description", 
                "type": "Edm.String",
                "searchable": true, 
                "filterable": false, 
                "retrievable": true, 
                "sortable": false, 
                "facetable": false
            },
            {
                "name": "DescriptionVector",
                "type": "Collection(Edm.Single)",
                "searchable": true,
                "retrievable": true,
                "dimensions": 1536,
                "vectorSearchProfile": "my-vector-profile"
            },
            {
                "name": "Category", 
                "type": "Edm.String",
                "searchable": true, 
                "filterable": true, 
                "retrievable": true, 
                "sortable": true, 
                "facetable": true
            },
            {
                "name": "Tags",
                "type": "Collection(Edm.String)",
                "searchable": true,
                "filterable": true,
                "retrievable": true,
                "sortable": false,
                "facetable": true
            },
            {
                "name": "Address", 
                "type": "Edm.ComplexType",
                "fields": [
                    {
                        "name": "City", "type": "Edm.String",
                        "searchable": true, "filterable": true, "retrievable": true, "sortable": true, "facetable": true
                    },
                    {
                        "name": "StateProvince", "type": "Edm.String",
                        "searchable": true, "filterable": true, "retrievable": true, "sortable": true, "facetable": true
                    }
                ]
            },
            {
                "name": "Location",
                "type": "Edm.GeographyPoint",
                "searchable": false, 
                "filterable": true, 
                "retrievable": true, 
                "sortable": true, 
                "facetable": false
            }
        ],
        "vectorSearch": {
            "algorithms": [
                {
                    "name": "my-hnsw-vector-config-1",
                    "kind": "hnsw",
                    "hnswParameters": 
                    {
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500,
                        "metric": "cosine"
                    }
                }
            ],
            "profiles": [      
                {
                    "name": "my-vector-profile",
                    "algorithm": "my-hnsw-vector-config-1"
                }
          ]
        },
        "semantic": {
            "configurations": [
                {
                    "name": "my-semantic-config",
                    "prioritizedFields": {
                        "titleField": {
                            "fieldName": "HotelName"
                        },
                        "prioritizedContentFields": [
                            { "fieldName": "Description" }
                        ],
                        "prioritizedKeywordsFields": [
                            { "fieldName": "Tags" }
                        ]
                    }
                }
            ]
        }
    }
    ```

1. Save the file again, and then select **Send request**. You should have an `HTTP/1.1 201 Created` response. The response body should include the JSON representation of the index schema.

    Key takeaways about this REST API:

    - The `fields` collection includes a required key field and text and vector fields (such as `Description` and `DescriptionVector`) for text and vector search. Colocating vector and nonvector fields in the same index enables hybrid queries. For instance, you can combine filters, text search with semantic ranking, and vectors into a single query operation.

    - Vector fields must be `type: Collection(Edm.Single)` with `dimensions` and `vectorSearchProfile` properties.

    - The `vectorSearch` section is an array of approximate nearest neighbor algorithm configurations and profiles. Supported algorithms include hierarchical navigable small world and exhaustive k-nearest neighbor. For more information, see [Relevance scoring in vector search](vector-search-ranking.md).

    - [Optional]: The `semantic` configuration enables reranking of search results. You can rerank results in queries of type `semantic` for string fields that are specified in the configuration. To learn more, see [Semantic ranking overview](semantic-search-overview.md).

## Upload documents

Creating and loading the index are separate steps. In Azure AI Search, the index contains all searchable data and queries run on the search service. For REST calls, the data is provided as JSON documents. Use [Documents- Index REST API](/rest/api/searchservice/documents/) for this task.

The URI is extended to include the `docs` collection and the `index` operation.

> [!IMPORTANT]
> The following example isn't runnable code. For readability, we excluded vector values because each one contains 1,536 embeddings, which is too long for this article. If you want to try this step, copy runnable code from the [sample on GitHub](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors).

1. Paste in a valid request that uploads documents, similar to the example below.

1. Save the file, and then select **Send request**. You should have an `HTTP/1.1 201 Created` response. The response body should include the JSON representation of the search documents.

```http
### Upload documents
POST {{baseUrl}}/indexes/hotels-quickstart-vectors/docs/index?api-version=2023-11-01  HTTP/1.1
Content-Type: application/json
api-key: {{apiKey}}

{
    "value": [
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "1",
            "HotelName": "Stay-Kay City Hotel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "The hotel is ideally located on the main commercial artery of the city 
                in the heart of New York.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Boutique",
            "Tags": [
                "pool",
                "air conditioning",
                "concierge"
            ],
        },
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "2",
            "HotelName": "Old Century Hotel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "The hotel is situated in a  nineteenth century plaza, which has been 
                expanded and renovated to the highest architectural standards to create a modern, 
                functional and first-class hotel in which art and unique historical elements 
                coexist with the most modern comforts.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Boutique",
            "Tags": [
                "pool",
                "air conditioning",
                "free wifi",
                "concierge"
            ]
        },
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "3",
            "HotelName": "Gastronomic Landscape Hotel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "The Hotel stands out for its gastronomic excellence under the management of 
                William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Resort and Spa",
            "Tags": [
                "air conditioning",
                "bar",
                "continental breakfast"
            ]
        }
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "4",
            "HotelName": "Sublime Palace Hotel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "Sublime Palace Hotel is located in the heart of the historic center of 
                Sublime in an extremely vibrant and lively area within short walking distance to 
                the sites and landmarks of the city and is surrounded by the extraordinary beauty 
                of churches, buildings, shops and monuments. 
                Sublime Palace is part of a lovingly restored 1800 palace.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Boutique",
            "Tags": [
                "concierge",
                "view",
                "24-hour front desk service"
            ]
        },
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "13",
            "HotelName": "Luxury Lion Resort",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury 
                accommodations. Moments from the stadium, we feature the best in comfort",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Resort and Spa",
            "Tags": [
                "view",
                "free wifi",
                "pool"
            ]
        },
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "48",
            "HotelName": "Nordick's Valley Motel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "Only 90 miles (about 2 hours) from the nation's capital and nearby 
                most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring 
                the caverns?  It's all nearby and we have specially priced packages to help make 
                our B&B your home base for fun while visiting the valley.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Boutique",
            "Tags": [
                "continental breakfast",
                "air conditioning",
                "free wifi"
            ],
        },
        {
            "@search.action": "mergeOrUpload",
            "HotelId": "49",
            "HotelName": "Swirling Currents Hotel",
            "HotelNameVector": [VECTOR ARRAY OMITTED],
            "Description": 
                "Spacious rooms, glamorous suites and residences, rooftop pool, walking 
                access to shopping, dining, entertainment and the city center.",
            "DescriptionVector": [VECTOR ARRAY OMITTED],
            "Category": "Luxury",
            "Tags": [
                "air conditioning",
                "laundry service",
                "24-hour front desk service"
            ]
        }
    ]
}
```

Key takeaways about this REST API:

- Documents in the payload consist of fields defined in the index schema.

- Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 3,072 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the Azure OpenAI **text-embedding-ada-002** model.

## Run queries

Now that documents are loaded, you can issue vector queries against them by using [Documents - Search Post (REST)](/rest/api/searchservice/documents/search-post).

There are several queries to demonstrate various patterns:

- [Single vector search](#single-vector-search)
- [Single vector search with filter](#single-vector-search-with-filter)
- [Hybrid search](#hybrid-search)
- [Semantic hybrid search with filter](#semantic-hybrid-search-with-a-filter)

The vector queries in this section are based on two strings:

- **Search string**: `historic hotel walk to restaurants and shopping`
- **Vector query string** (vectorized into a mathematical representation): `classic lodging near running trails, eateries, retail`

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `classic lodging near running trails, eateries, retail`, results are zero. We use this example to show how you can get relevant results even if there are no matching terms.

> [!IMPORTANT]
> The following examples aren't runnable code. For readability, we excluded vector values because each array contains 1,536 embeddings, which is too long for this article. If you want to try these queries, copy runnable code from the [sample on GitHub](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-vectors).

### Single vector search

1. Paste in a POST request to query the search index. Save the file. Then select **Send request**. The URI is extended to include the `/docs/search` operator.

    ```http
    ### Run a query
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        api-key: {{apiKey}}
        
        {
            "count": true,
            "select": "HotelId, HotelName, Description, Category",
            "vectorQueries": [
                {
                    "vector"": [0.01944167, 0.0040178085
                        . . .  TRIMMED FOR BREVITY
                        010858015, -0.017496133],
                    "k": 7,
                    "fields": "DescriptionVector",
                    "kind": "vector",
                    "exhaustive": true
                }
            ]
        }
    ```

   This vector query is shortened for brevity. The `vectorQueries.vector` contains the vectorized text of the query input, `fields` determines which vector fields are searched, and `k` specifies the number of nearest neighbors to return.

   The vector query string is `classic lodging near running trails, eateries, retail`, which is vectorized into 1,536 embeddings for this query.

1. Review the response. The response for the vector equivalent of `classic lodging near running trails, eateries, retail` includes seven results. Each result provides a search score and the fields listed in `select`. In a similarity search, the response always includes `k` results ordered by the value similarity score.

    ```json
    {
        "@odata.context": "https://my-demo-search.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
        "@odata.count": 7,
        "value": [
            {
                "@search.score": 0.857736,
                "HotelName": "Nordick's Valley Motel",
                "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley."
            },
            {
                "@search.score": 0.8399129,
                "HotelName": "Swirling Currents Hotel",
                "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center."
            },
            {
                "@search.score": 0.8383954,
                "HotelName": "Luxury Lion Resort",
                "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort"
            },
            {
                "@search.score": 0.8254346,
                "HotelName": "Sublime Palace Hotel",
                "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace."
            },
            {
                "@search.score": 0.82380056,
                "HotelName": "Stay-Kay City Hotel",
                "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York."
            },
            {
                "@search.score": 0.81514084,
                "HotelName": "Old Century Hotel",
                "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts."
            },
            {
                "@search.score": 0.8133763,
                "HotelName": "Gastronomic Landscape Hotel",
                "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services."
            }
        ]
    }
    ```

### Single vector search with filter

You can add filters, but the filters are applied to the nonvector content in your index. In this example, the filter applies to the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

1. Paste in a POST request to query the search index.

    ```http
    ### Run a vector query with a filter
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        api-key: {{apiKey}}
    
        {
            "count": true,
            "select": "HotelId, HotelName, Category, Tags, Description",
            "filter": "Tags/any(tag: tag eq 'free wifi')",
            "vectorFilterMode": "postFilter",
            "vectorQueries": [
            {
                "vector": [ VECTOR OMITTED ],
                "k": 7,
                "fields": "DescriptionVector",
                "kind": "vector",
                "exhaustive": true
            },
        ]
    }
    ``` 

1. Review the response. The query is the same as the previous example, but it includes a post-processing exclusion filter and returns only the three hotels that have free Wi-Fi.

    ```json
    {
    
        "@odata.count": 3,
        "value": [
            {
                "@search.score": 0.857736,
                "HotelName": "Nordick's Valley Motel",
                "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
                "Tags": [
                    "continental breakfast",
                    "air conditioning",
                    "free wifi"
                ]
            },
            {
                "@search.score": 0.8383954,
                "HotelName": "Luxury Lion Resort",
                "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort",
                "Tags": [
                    "view",
                    "free wifi",
                    "pool"
                ]
            },
            {
                "@search.score": 0.81514084,
                "HotelName": "Old Century Hotel",
                "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
                "Tags": [
                    "pool",
                    "free wifi",
                    "concierge"
                ]
            }
        ]
    }
    ```

### Hybrid search

Hybrid search consists of keyword queries and vector queries in a single search request. This example runs the vector query and full text search concurrently:

- **Search string**: `historic hotel walk to restaurants and shopping`
- **Vector query string** (vectorized into a mathematical representation): `classic lodging near running trails, eateries, retail`

1. Paste in a POST request to query the search index. Then select **Send request**.

    ```http
    ### Run a hybrid query
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        api-key: {{apiKey}}
        
    {
        "count": true,
        "search": "historic hotel walk to restaurants and shopping",
        "select": "HotelName, Description",
        "top": 7,
        "vectorQueries": [
            {
                "vector": [ VECTOR OMITTED],
                "k": 7,
                "fields": "DescriptionVector",
                "kind": "vector",
                "exhaustive": true
            }
        ]
    }
    ```

   Because this is a hybrid query, results are [ranked by Reciprocal Rank Fusion (RRF)](hybrid-search-ranking.md). RRF evaluates search scores of multiple search results, takes the inverse, and then merges and sorts the combined results. The `top` number of results are returned.

1. Review the response.

    ```json
    {
        "@odata.count": 7,
        "value": [
            {
                "@search.score": 0.03279569745063782,
                "HotelName": "Luxury Lion Resort",
                "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort"
            },
            {
                "@search.score": 0.03226646035909653,
                "HotelName": "Sublime Palace Hotel",
                "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace."
            },
            {
                "@search.score": 0.03226646035909653,
                "HotelName": "Swirling Currents Hotel",
                "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center."
            },
            {
                "@search.score": 0.03205128386616707,
                "HotelName": "Nordick's Valley Motel",
                "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley."
            },
            {
                "@search.score": 0.03128054738044739,
                "HotelName": "Gastronomic Landscape Hotel",
                "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services."
            },
            {
                "@search.score": 0.03100961446762085,
                "HotelName": "Old Century Hotel",
                "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts."
            },
            {
                "@search.score": 0.03077651560306549,
                "HotelName": "Stay-Kay City Hotel",
                "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York."
            }
        ]
    }
    ```

     Because RRF merges results, it helps to review the inputs. The following results are from only the full-text query. The top two results are Sublime Palace Hotel and History Lion Resort. The Sublime Palace Hotel has a stronger BM25 relevance score.

    ```json
            {
                "@search.score": 2.2626662,
                "HotelName": "Sublime Palace Hotel",
                "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace."
            },
            {
                "@search.score": 0.86421645,
                "HotelName": "Luxury Lion Resort",
                "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort"
                },
    ```

    In the vector-only query, which uses HNSW for finding matches, the Sublime Palace Hotel drops to fourth position. Historic Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

    ```json
        "value": [
            {
                "@search.score": 0.857736,
                "HotelId": "48",
                "HotelName": "Nordick's Valley Motel",
                "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
                "Category": "Boutique"
            },
            {
                "@search.score": 0.8399129,
                "HotelId": "49",
                "HotelName": "Swirling Currents Hotel",
                "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
                "Category": "Luxury"
            },
            {
                "@search.score": 0.8383954,
                "HotelId": "13",
                "HotelName": "Luxury Lion Resort",
                "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort",
                "Category": "Resort and Spa"
            },
            {
                "@search.score": 0.8254346,
                "HotelId": "4",
                "HotelName": "Sublime Palace Hotel",
                "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Palace is part of a lovingly restored 1800 palace.",
                "Category": "Boutique"
            },
            {
                "@search.score": 0.82380056,
                "HotelId": "1",
                "HotelName": "Stay-Kay City Hotel",
                "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York.",
                "Category": "Boutique"
            },
            {
                "@search.score": 0.81514084,
                "HotelId": "2",
                "HotelName": "Old Century Hotel",
                "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
                "Category": "Boutique"
            },
            {
                "@search.score": 0.8133763,
                "HotelId": "3",
                "HotelName": "Gastronomic Landscape Hotel",
                "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
                "Category": "Resort and Spa"
            }
        ]
    ```

### Semantic hybrid search with a filter

Here's the last query in the collection. This hybrid query with semantic ranking is filtered to show only the hotels within a 500-kilometer radius of Washington D.C. You can set `vectorFilterMode` to null, which is equivalent to the default (`preFilter` for newer indexes and `postFilter` for older ones).

1. Paste in a POST request to query the search index. Then select **Send request**.

    ```http
    ### Run a hybrid query
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        api-key: {{apiKey}}

    {
        "count": true,
        "search": "historic hotel walk to restaurants and shopping",
        "select": "HotelId, HotelName, Category, Description,Address/City, Address/StateProvince",
        "filter": "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 500",
        "vectorFilterMode": null,
        "facets": [ "Address/StateProvince"],
        "top": 7,
        "queryType": "semantic",
        "answers": "extractive|count-3",
        "captions": "extractive|highlight-true",
        "semanticConfiguration": "my-semantic-config",
        "vectorQueries": [
            {
                "vector": [ VECTOR OMITTED ],
                "k": 7,
                "fields": "DescriptionVector",
                "kind": "vector",
                "exhaustive": true
            }
        ]
    }
    ```

1. Review the response. The response is three hotels, which are filtered by location and faceted by `StateProvince` and semantically reranked to promote results that are closest to the search string query (`historic hotel walk to restaurants and shopping`).

    The Swirling Currents Hotel now moves into the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel, within walking distance to dining (restaurants) and shopping."

    ```json
    {
        "@odata.count": 3,
        "@search.facets": {
            "Address/StateProvince": [
                {
                    "count": 1,
                    "value": "NY"
                },
                {
                    "count": 1,
                    "value": "VA"
                }
            ]
        },
        "@search.answers": [],
        "value": [
            {
                "@search.score": 0.03306011110544205,
                "@search.rerankerScore": 2.5094974040985107,
                "HotelId": "49",
                "HotelName": "Swirling Currents Hotel",
                "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
                "Category": "Luxury",
                "Address": {
                    "City": "Arlington",
                    "StateProvince": "VA"
                }
            },
            {
                "@search.score": 0.03306011110544205,
                "@search.rerankerScore": 2.0370211601257324,
                "HotelId": "48",
                "HotelName": "Nordick's Valley Motel",
                "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
                "Category": "Boutique",
                "Address": {
                    "City": "Washington D.C.",
                    "StateProvince": null
                }
            },
            {
                "@search.score": 0.032258063554763794,
                "@search.rerankerScore": 1.6706111431121826,
                "HotelId": "1",
                "HotelName": "Stay-Kay City Hotel",
                "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York.",
                "Category": "Boutique",
                "Address": {
                    "City": "New York",
                    "StateProvince": "NY"
                }
            }
        ]
    }
    ```

    Key takeaways about this REST API:

    - Vector search is specified through the `vectors.value` property. Keyword search is specified through the `search` property.

    - In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors. In this final query, there's no semantic `answer` because the system didn't produce one that was sufficiently strong.

    - Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

You can also try this `DELETE` command:

```http
### Delete an index
DELETE  {{baseUrl}}/indexes/hotels-vector-quickstart?api-version=2023-11-01 HTTP/1.1
    Content-Type: application/json
    api-key: {{apiKey}}
```

## Next steps

As a next step, we recommend learning how to invoke REST API calls [without API keys](search-get-started-rbac.md).

You might also want to review the demo code for [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python), [C#](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet), or [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript).
