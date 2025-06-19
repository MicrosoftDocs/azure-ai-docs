---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 05/30/2025
---

## Create or download the code file

You use one `.rest` or `.http` file to run all the requests in this quickstart. You can download the REST file that contains the code for this quickstart, or you can create a new file in Visual Studio Code and copy the code into it.

1. In Visual Studio Code, create a new file with a `.rest` or `.http` file extension. For example, `az-search-vector-quickstart.rest`. Copy and paste the raw contents of the [Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-vectors/az-search-vector-quickstart.rest](https://raw.githubusercontent.com/Azure-Samples/azure-search-rest-samples/refs/heads/main/Quickstart-vectors/az-search-vector-quickstart.rest) file into this new file. 

1. At the top of the file, replace the placeholder value for `@baseUrl` with your search service URL. See the [Retrieve resource information](#retrieve-resource-information) section for instructions on how to find your search service URL.


   ```http
   @baseUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
   ```

1. At the top of the file, replace the placeholder value for authentication. See the [Retrieve resource information](#retrieve-resource-information) section for instructions on how to get your Microsoft Entra token or API key.

    For the **recommended** keyless authentication via Microsoft Entra ID, you need to replace `@apiKey` with the `@token` variable.

   ```http
   @token = PUT-YOUR-MICROSOFT-ENTRA-TOKEN-HERE
   ```

    If you prefer to use an API key, replace `@apiKey` with the key you copied from the Azure portal.

    ```http
    @apiKey = PUT-YOUR-ADMIN-KEY-HERE
    ```

1. For the **recommended** keyless authentication via Microsoft Entra ID, you need to replace `api-key: {{apiKey}}` with `Authorization: Bearer {{token}}` in the request headers. Replace all instances of `api-key: {{apiKey}}` that you find in the file.


## Create a vector index

You use the [Create Index](/rest/api/searchservice/indexes/create) REST API to create a vector index and set up the physical data structures on your search service.

The index schema in this example is organized around hotel content. Sample data consists of vector and nonvector names and descriptions of fictitious hotels. This schema includes configurations for vector indexing and queries, and for semantic ranking.

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Create a new index` code block in the file. This block contains the request to create the `hotels-vector-quickstart` index on your search service. 
    

    ```http
    ### Create a new index
    POST  {{baseUrl}}/indexes?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}

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
                "name": "Description_fr", 
                "type": "Edm.String",
                "searchable": true, 
                "filterable": false, 
                "retrievable": true, 
                "sortable": false, 
                "facetable": false,
                "analyzer": "en.microsoft"
            },
            {
                "name": "Description_frvector",
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
                "name": "ParkingIncluded",
                "type": "Edm.Boolean",
                "searchable": false,
                "filterable": true,
                "retrievable": true,
                "sortable": true,
                "facetable": true
            },
            {
                "name": "LastRenovationDate",
                "type": "Edm.DateTimeOffset",
                "searchable": false,
                "filterable": true,
                "retrievable": true,
                "sortable": true,
                "facetable": true
            },
            {
                "name": "Rating",
                "type": "Edm.Double",
                "searchable": false,
                "filterable": true,
                "retrievable": true,
                "sortable": true,
                "facetable": true
            },
            {
                "name": "Address", 
                "type": "Edm.ComplexType",
                "fields": [
                    {
                        "name": "StreetAddress", "type": "Edm.String",
                        "searchable": true, "filterable": false, "retrievable": true, "sortable": false, "facetable": false
                    },
                    {
                        "name": "City", "type": "Edm.String",
                        "searchable": true, "filterable": true, "retrievable": true, "sortable": true, "facetable": true
                    },
                    {
                        "name": "StateProvince", "type": "Edm.String",
                        "searchable": true, "filterable": true, "retrievable": true, "sortable": true, "facetable": true
                    },
                    {
                        "name": "PostalCode", "type": "Edm.String",
                        "searchable": true, "filterable": true, "retrievable": true, "sortable": true, "facetable": true
                    },
                    {
                        "name": "Country", "type": "Edm.String",
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
                },
                {
                    "name": "my-hnsw-vector-config-2",
                    "kind": "hnsw",
                    "hnswParameters": 
                    {
                        "m": 4,
                        "metric": "euclidean"
                    }
                },
                {
                    "name": "my-eknn-vector-config",
                    "kind": "exhaustiveKnn",
                    "exhaustiveKnnParameters": 
                    {
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
                            { "fieldName": "Category" }
                        ]
                    }
                }
            ]
        }
    }
    ```

1. Select **Send request**. You should have an `HTTP/1.1 201 Created` response. 

The response body should include the JSON representation of the index schema.

```json
{
    "@odata.context": "https://my-demo-search.search.windows.net/$metadata#indexes/$entity",
    "@odata.etag": "\"0x8DD2E70E6C36D8E\"",
    "name": "hotels-vector-quickstart",
    "defaultScoringProfile": null,
    "fields": [
    {
        "name": "HotelId",
        "type": "Edm.String",
        "searchable": false,
        "filterable": true,
        "retrievable": true,
        "sortable": false,
        "facetable": false,
        "key": true,
        "indexAnalyzer": null,
        "searchAnalyzer": null,
        "analyzer": null,
        "dimensions": null,
        "vectorSearchProfile": null,
        "synonymMaps": []
    },
    [MORE FIELD DEFINITIONS OMITTED FOR BREVITY]
    ],
    "scoringProfiles": [],
    "corsOptions": null,
    "suggesters": [],
    "analyzers": [],
    "tokenizers": [],
    "tokenFilters": [],
    "charFilters": [],
    "encryptionKey": null,
    "similarity": {
    "@odata.type": "#Microsoft.Azure.Search.BM25Similarity",
    "k1": null,
    "b": null
    },
    "vectorSearch": {
    "algorithms": [
        {
        "name": "my-hnsw-vector-config-1",
        "kind": "hnsw",
        "hnswParameters": {
            "metric": "cosine",
            "m": 4,
            "efConstruction": 400,
            "efSearch": 500
        },
        "exhaustiveKnnParameters": null
        },
        {
        "name": "my-hnsw-vector-config-2",
        "kind": "hnsw",
        "hnswParameters": {
            "metric": "euclidean",
            "m": 4,
            "efConstruction": 400,
            "efSearch": 500
        },
        "exhaustiveKnnParameters": null
        },
        {
        "name": "my-eknn-vector-config",
        "kind": "exhaustiveKnn",
        "hnswParameters": null,
        "exhaustiveKnnParameters": {
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
    "defaultConfiguration": null,
    "configurations": [
        {
        "name": "my-semantic-config",
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
            }
            ]
        }
        }
    ]
    }
}
```

Key takeaways about the [Create Index](/rest/api/searchservice/indexes/create) REST API:

- The `fields` collection includes a required key field and text and vector fields (such as `Description` and `DescriptionVector`) for text and vector search. Colocating vector and nonvector fields in the same index enables hybrid queries. For instance, you can combine filters, text search with semantic ranking, and vectors into a single query operation.

- Vector fields must be `type: Collection(Edm.Single)` with `dimensions` and `vectorSearchProfile` properties.

- The `vectorSearch` section is an array of approximate nearest neighbor algorithm configurations and profiles. Supported algorithms include hierarchical navigable small world and exhaustive k-nearest neighbor. For more information, see [Relevance scoring in vector search](vector-search-ranking.md).

- The (optional) `semantic` configuration enables reranking of search results. You can rerank results in queries of type `semantic` for string fields that are specified in the configuration. To learn more, see [Semantic ranking overview](semantic-search-overview.md).

## Upload documents

Creating and loading the index are separate steps. You created the index schema [in the previous step](#create-a-vector-index). Now you need to load documents into the index.
 
In Azure AI Search, the index contains all searchable data and queries run on the search service. For REST calls, the data is provided as JSON documents. Use [Documents- Index REST API](/rest/api/searchservice/documents/) for this task. The URI is extended to include the `docs` collection and the `index` operation.

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Upload documents` code block in the file. This block contains the request to upload documents to the `hotels-vector-quickstart` index on your search service.

    ```http
    ### Upload documents
    POST {{baseUrl}}/indexes/hotels-quickstart-vectors/docs/index?api-version=2023-11-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}
    
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

    > [!IMPORTANT]
    > The code in this example isn't runnable. Several characters or lines are removed for brevity. Use the code in your `az-search-vector-quickstart.rest` file to run the request.

1. Select **Send request**. You should have an `HTTP/1.1 200 OK` response. The response body should include the JSON representation of the search documents.

Key takeaways about the [Documents - Index REST API](/rest/api/searchservice/documents/) request:

- Documents in the payload consist of fields defined in the index schema.

- Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 3,072 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the Azure OpenAI **text-embedding-ada-002** model.

## Run queries

Now that documents are loaded, you can issue vector queries against them by using [Documents - Search Post (REST)](/rest/api/searchservice/documents/search-post).

In the next sections, we run queries against the `hotels-vector-quickstart` index. The queries include:

- [Single vector search](#single-vector-search)
- [Single vector search with filter](#single-vector-search-with-filter)
- [Hybrid search](#hybrid-search)
- [Semantic hybrid search with filter](#semantic-hybrid-search-with-a-filter)

The example vector queries are based on two strings:

- **Search string**: `historic hotel walk to restaurants and shopping`
- **Vector query string** (vectorized into a mathematical representation): `classic lodging near running trails, eateries, retail`

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `classic lodging near running trails, eateries, retail`, results are zero. We use this example to show how you can get relevant results even if there are no matching terms.

### Single vector search

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Run a single vector query` code block in the file. This block contains the request to query the search index.


    ```http
    ### Run a single vector query
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}
        
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

    > [!IMPORTANT]
    > The code in this example isn't runnable. Several characters or lines are removed for brevity. Use the code in your `az-search-vector-quickstart.rest` file to run the request.

1. Select **Send request**. You should have an `HTTP/1.1 200 OK` response. The response body should include the JSON representation of the search results.

The response for the vector equivalent of `classic lodging near running trails, eateries, retail` includes seven results. Each result provides a search score and the fields listed in `select`. In a similarity search, the response always includes `k` results ordered by the value similarity score.

```json
{
  "@odata.context": "https://my-demo-search.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 7,
  "value": [
    {
      "@search.score": 0.85773647,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.8399132,
      "HotelId": "49",
      "HotelName": "Old Carrabelle Hotel",
      "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
      "Category": "Luxury"
    },
    {
      "@search.score": 0.83839583,
      "HotelId": "13",
      "HotelName": "Historic Lion Resort",
      "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort",
      "Category": "Resort and Spa"
    },
    {
      "@search.score": 0.82543474,
      "HotelId": "4",
      "HotelName": "Sublime Cliff Hotel",
      "Description": "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace.",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.82380104,
      "HotelId": "1",
      "HotelName": "Secret Point Hotel",
      "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York.",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.8151413,
      "HotelId": "2",
      "HotelName": "Twin Dome Hotel",
      "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
      "Category": "Boutique"
    },
    {
      "@search.score": 0.8133767,
      "HotelId": "3",
      "HotelName": "Triple Landscape Hotel",
      "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel\u2019s restaurant services.",
      "Category": "Resort and Spa"
    }
  ]
}
```

### Single vector search with filter

You can add filters, but the filters are applied to the nonvector content in your index. In this example, the filter applies to the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Run a vector query with a filter` code block in the file. This block contains the request to query the search index.


    ```http
    ### Run a vector query with a filter
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}
    
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

    > [!IMPORTANT]
    > The code in this example isn't runnable. Several characters or lines are removed for brevity. Use the code in your `az-search-vector-quickstart.rest` file to run the request.

1. Select **Send request**. You should have an `HTTP/1.1 200 OK` response. The response body should include the JSON representation of the search results.

The query was the same as the previous [single vector search example](#single-vector-search), but it includes a post-processing exclusion filter and returns only the three hotels that have free Wi-Fi.

```json
{
  "@odata.context": "https://my-demo-search.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 3,
  "value": [
    {
      "@search.score": 0.85773647,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
      "Category": "Boutique",
      "Tags": [
        "continental breakfast",
        "air conditioning",
        "free wifi"
      ]
    },
    {
      "@search.score": 0.83839583,
      "HotelId": "13",
      "HotelName": "Historic Lion Resort",
      "Description": "Unmatched Luxury.  Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium, we feature the best in comfort",
      "Category": "Resort and Spa",
      "Tags": [
        "view",
        "free wifi",
        "pool"
      ]
    },
    {
      "@search.score": 0.8151413,
      "HotelId": "2",
      "HotelName": "Twin Dome Hotel",
      "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
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

### Hybrid search

Hybrid search consists of keyword queries and vector queries in a single search request. This example runs the vector query and full text search concurrently:

- **Search string**: `historic hotel walk to restaurants and shopping`
- **Vector query string** (vectorized into a mathematical representation): `classic lodging near running trails, eateries, retail`

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Run a hybrid query` code block in the file. This block contains the request to query the search index.


    ```http
    ### Run a hybrid query
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}
        
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

    > [!IMPORTANT]
    > The code in this example isn't runnable. Several characters or lines are removed for brevity. Use the code in your `az-search-vector-quickstart.rest` file to run the request.

1. Select **Send request**. You should have an `HTTP/1.1 200 OK` response. The response body should include the JSON representation of the search results.
   
Because this is a hybrid query, results are [ranked by Reciprocal Rank Fusion (RRF)](hybrid-search-ranking.md). RRF evaluates search scores of multiple search results, takes the inverse, and then merges and sorts the combined results. The `top` number of results are returned.

Review the response:

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

1. In Visual Studio Code, open the `az-search-vector-quickstart.rest` file you [created earlier](#create-or-download-the-code-file).

1. Find the `### Run a hybrid query with semantic reranking` code block in the file. This block contains the request to query the search index.

    ```http
    ### Run a hybrid query with semantic reranking
    POST {{baseUrl}}/indexes/hotels-vector-quickstart/docs/search?api-version=2023-11-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}

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

    > [!IMPORTANT]
    > The code in this example isn't runnable. Several characters or lines are removed for brevity. Use the code in your `az-search-vector-quickstart.rest` file to run the request.

1. Select **Send request**. You should have an `HTTP/1.1 200 OK` response. The response body should include the JSON representation of the search results.

Review the response. The response is three hotels, which are filtered by location and faceted by `StateProvince` and semantically reranked to promote results that are closest to the search string query (`historic hotel walk to restaurants and shopping`).

The Swirling Currents Hotel now moves into the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel, within walking distance to dining (restaurants) and shopping."

```json
{
  "@odata.context": "https://my-demo-search.search.windows.net/indexes('hotels-vector-quickstart')/$metadata#docs(*)",
  "@odata.count": 2,
  "@search.facets": {
    "Address/StateProvince": [
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
      "@search.rerankerScore": 2.8773112297058105,
      "HotelId": "49",
      "HotelName": "Old Carrabelle Hotel",
      "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
      "Category": "Luxury",
      "Address": {
        "City": "Arlington",
        "StateProvince": "VA"
      }
    },
    {
      "@search.score": 0.03306011110544205,
      "@search.rerankerScore": 2.1703834533691406,
      "HotelId": "48",
      "HotelName": "Nordick's Motel",
      "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
      "Category": "Boutique",
      "Address": {
        "City": "Washington D.C.",
        "StateProvince": null
      }
    }
  ]
}
```

Key takeaways about [Documents - Search Post](/rest/api/searchservice/documents/search-post) REST API:

- Vector search is specified through the `vectors.value` property. Keyword search is specified through the `search` property.

- In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors. In this final query, there's no semantic `answer` because the system didn't produce one that was sufficiently strong.

- Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request in the REST client.

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.

If you want to keep the search service, but delete the index and documents, you can use the `DELETE` command in the REST client. This command (at the end of your `az-search-vector-quickstart.rest` file) deletes the `hotels-vector-quickstart` index:

```http
### Delete an index
DELETE  {{baseUrl}}/indexes/hotels-vector-quickstart?api-version=2023-11-01 HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}
```