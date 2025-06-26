---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/26/2025
---

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md). Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results.

This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) repo to populate the index.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart) to start with a finished project or follow these steps to create your own.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. For this quickstart, you can use a free service.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

## Configure access

You can connect to your Azure AI Search service using API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Settings** > **Keys**.

1. Under **API Access control**, select **Both**.

   This option enables both key-based and keyless authentication. After you assign roles, you can return to this step and select **Role-based access control**.

1. From the left pane, select **Access control (IAM)**.

1. Select **Add** > **Add role assignment**.

1. Assign the **Search Service Contributor** and **Search Index Data Contributor** roles to your user account.

For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Get resource information

In the next section, you specify the following endpoint and token to establish a connection to your Azure AI Search service. These steps assume that you [configured role-based access](#configure-access).

To get your resource information:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Overview**.

1. Make a note of the URL, which should be similar to `https://my-service.search.windows.net`.

1. On your local system, open a terminal.

1. Sign in to your Azure subscription. If you have multiple subscriptions, select the one that contains your search service.

    ```azurecli
    az login
    ```

1. Make a note of your Microsoft Entra token.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default
    ```

## Set up your file

Before you can make REST API calls to your Azure AI Search service, you must create a file to store your service endpoint, authentication token, and eventual requests. The REST Client extension in Visual Studio Code supports this task.

To set up your request file:

1. On your local system, open Visual Studio Code.

1. Create a `.rest` or `.http` file.

1. Paste the following placeholders and request into the file.

    ```http
    @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
    @token = PUT-YOUR-PERSONAL-IDENTITY-TOKEN-HERE

    ### List existing indexes by name
        GET {{baseUrl}}/indexes?api-version=2024-07-01
        Authorization: Bearer {{token}}
    ```

1. Replace the `@baseUrl` and `@token` placeholders with the values you obtained in [Get resource information](#get-resource-information). Don't include quotation marks.

1. Under `### List existing indexes by name`, select **Send Request**.

    A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK`, you're ready for the next steps.

    :::image type="content" source="../../media/search-get-started-rest/rest-client-request-setup.png" lightbox="../../media/search-get-started-rest/rest-client-request-setup.png" alt-text="Screenshot that shows a REST client configured for a search service request.":::

## Create, load, and query a search index

In this section, you make REST API calls to create a search index, upload documents to the index, and query the indexed documents. Visual Studio Code displays the response to each request in an adjacent pane. For more information about each step, see [Explaining the code](#explaining-the-code).

To create, load, and query an index:

1. Paste the following requests into your file.

    ```http
    ### Create a new index
    POST {{baseUrl}}/indexes?api-version=2024-07-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}
    
        {
            "name": "hotels-quickstart",  
            "fields": [
                {"name": "HotelId", "type": "Edm.String", "key": true, "filterable": true},
                {"name": "HotelName", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": true, "facetable": false},
                {"name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "en.lucene"},
                {"name": "Category", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                {"name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "sortable": false, "facetable": true},
                {"name": "ParkingIncluded", "type": "Edm.Boolean", "filterable": true, "sortable": true, "facetable": true},
                {"name": "LastRenovationDate", "type": "Edm.DateTimeOffset", "filterable": true, "sortable": true, "facetable": true},
                {"name": "Rating", "type": "Edm.Double", "filterable": true, "sortable": true, "facetable": true},
                {"name": "Address", "type": "Edm.ComplexType", 
                    "fields": [
                    {"name": "StreetAddress", "type": "Edm.String", "filterable": false, "sortable": false, "facetable": false, "searchable": true},
                    {"name": "City", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                    {"name": "StateProvince", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                    {"name": "PostalCode", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                    {"name": "Country", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true}
                    ]
                }
            ]
        }
 
    ### Upload documents
    POST {{baseUrl}}/indexes/hotels-quickstart/docs/index?api-version=2024-07-01  HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer {{token}}
    
        {
            "value": [
            {
            "@search.action": "upload",
            "HotelId": "1",
            "HotelName": "Stay-Kay City Hotel",
            "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
            "Category": "Boutique",
            "Tags": [ "view", "air conditioning", "concierge" ],
            "ParkingIncluded": false,
            "LastRenovationDate": "2022-01-18T00:00:00Z",
            "Rating": 3.60,
            "Address": 
                {
                "StreetAddress": "677 5th Ave",
                "City": "New York",
                "StateProvince": "NY",
                "PostalCode": "10022",
                "Country": "USA"
                } 
            },
            {
            "@search.action": "upload",
            "HotelId": "2",
            "HotelName": "Old Century Hotel",
            "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
             "Category": "Boutique",
            "Tags": [ "pool", "free wifi", "concierge" ],
            "ParkingIncluded": false,
            "LastRenovationDate": "2019-02-18T00:00:00Z",
            "Rating": 3.60,
            "Address": 
                {
                "StreetAddress": "140 University Town Center Dr",
                "City": "Sarasota",
                "StateProvince": "FL",
                "PostalCode": "34243",
                "Country": "USA"
                } 
            },
            {
            "@search.action": "upload",
            "HotelId": "3",
            "HotelName": "Gastronomic Landscape Hotel",
            "Description": "The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
            "Category": "Suite",
            "Tags": [ "restaurant", "bar", "continental breakfast" ],
            "ParkingIncluded": true,
            "LastRenovationDate": "2015-09-20T00:00:00Z",
            "Rating": 4.80,
            "Address": 
                {
                "StreetAddress": "3393 Peachtree Rd",
                "City": "Atlanta",
                "StateProvince": "GA",
                "PostalCode": "30326",
                "Country": "USA"
                } 
            },
            {
            "@search.action": "upload",
            "HotelId": "4",
            "HotelName": "Sublime Palace Hotel",
            "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.",
            "Tags": [ "concierge", "view", "air conditioning" ],
            "ParkingIncluded": true,
            "LastRenovationDate": "2020-02-06T00:00:00Z",
            "Rating": 4.60,
            "Address": 
                {
                "StreetAddress": "7400 San Pedro Ave",
                "City": "San Antonio",
                "StateProvince": "TX",
                "PostalCode": "78216",
                "Country": "USA"
                }
            }
          ]
        }

    ### Run a query
    POST {{baseUrl}}/indexes/hotels-quickstart/docs/search?api-version=2024-07-01  HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer {{token}}
      
      {
          "search": "attached restaurant",
          "select": "HotelId, HotelName, Tags, Description",
          "searchFields": "Description, Tags",
          "count": true
      }
    ```

1. Under each `###` delimiter, select **Send Request** to make the corresponding REST API call.

    + For `### Create a new index`, you should receive an `HTTP/1.1 201 Created` response whose body contains the JSON representation of the index schema.

    + For `### Upload documents`, you should receive an `HTTP/1.1 200 OK` response whose body contains the key and status of each uploaded document.

    + For `### Run a query`, you should receive an `HTTP/1.1 200 OK` response whose body contains the document that matched your query, its relevance score, and its selected fields.

## Explaining the code

This section explains the REST API calls that you made to:

+ [Create an index](#create-an-index)
+ [Load documents into the index](#load-documents-into-the-index)
+ [Query the index](#query-the-index)

### Create an index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured. An index is conceptually similar to a table in a relational database, but it's specifically designed for search operations, such as full-text search.

This quickstart calls [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) to build a search index named `hotels-quickstart` and its physical data structures on your search service.

```http
POST {{baseUrl}}/indexes?api-version=2024-07-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}

    {
        "name": "hotels-quickstart",  
        "fields": [
            {"name": "HotelId", "type": "Edm.String", "key": true, "filterable": true},
            {"name": "HotelName", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": true, "facetable": false},
            {"name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": false, "analyzer": "en.lucene"},
            {"name": "Category", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
            {"name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "sortable": false, "facetable": true},
            {"name": "ParkingIncluded", "type": "Edm.Boolean", "filterable": true, "sortable": true, "facetable": true},
            {"name": "LastRenovationDate", "type": "Edm.DateTimeOffset", "filterable": true, "sortable": true, "facetable": true},
            {"name": "Rating", "type": "Edm.Double", "filterable": true, "sortable": true, "facetable": true},
            {"name": "Address", "type": "Edm.ComplexType", 
                "fields": [
                {"name": "StreetAddress", "type": "Edm.String", "filterable": false, "sortable": false, "facetable": false, "searchable": true},
                {"name": "City", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                {"name": "StateProvince", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                {"name": "PostalCode", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
                {"name": "Country", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true}
                ]
            }
        ]
    }
```

Within our index schema, the `fields` collection defines the structure of hotel documents. Each field has a `name`, data `type`, and attributes that determine its behavior during indexing and queries. The `HotelId` field is marked as the key, which Azure AI Search requires to uniquely identify each document in an index.

Key points about the index schema:

+ Use string fields (`Edm.String`) to make numeric data full-text searchable. Other [supported data types](/rest/api/searchservice/supported-data-types), such as `Edm.Int32`, are filterable, sortable, facetable, and retrievable but aren't searchable.

+ Most of our fields are simple data types, but you can define complex types to represent nested data, such as the `Address` field.

+ Field attributes determine allowed actions. The REST APIs allow [many actions by default](/rest/api/searchservice/indexes/create#request-body). For example, all strings are searchable and retrievable. With the REST APIs, you might only use attributes if you need to disable a behavior.

### Load documents into the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents as inline JSON. In production scenarios, however, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

This quickstart calls [Documents - Index (REST API)](/rest/api/searchservice/documents/) to add four sample hotel documents to your index. Compared to the previous request, the URI is extended to include the `docs` collection and `index` operation.

```http
POST {{baseUrl}}/indexes/hotels-quickstart/docs/index?api-version=2024-07-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{token}}

    {
        "value": [
        {
        "@search.action": "upload",
        "HotelId": "1",
        "HotelName": "Stay-Kay City Hotel",
        "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
        "Category": "Boutique",
        "Tags": [ "view", "air conditioning", "concierge" ],
        "ParkingIncluded": false,
        "LastRenovationDate": "2022-01-18T00:00:00Z",
        "Rating": 3.60,
        "Address": 
            {
            "StreetAddress": "677 5th Ave",
            "City": "New York",
            "StateProvince": "NY",
            "PostalCode": "10022",
            "Country": "USA"
            } 
        },
        // OTHER DOCUMENTS OMITTED FOR BREVITY
      ]
    }
```

Each document in the `value` array represents a hotel and contains fields that match the index schema. The `@search.action` parameter specifies the operation to perform for each document. Our example uses `upload`, which adds the document if it doesn't exist or updates the document if it does exist.

### Query the index

Now that documents are loaded into your index, you can issue full-text queries against them.

This quickstart calls [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post) to find hotel documents that match your search criteria. The URI now targets the `/docs/search` operation.

```http
POST {{baseUrl}}/indexes/hotels-quickstart/docs/search?api-version=2024-07-01  HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}
  
  {
      "search": "attached restaurant",
      "select": "HotelId, HotelName, Tags, Description",
      "searchFields": "Description, Tags",
      "count": true
  }
```

Full-text search requests always include a `search` parameter that contains the query text. The query text can include one or more terms, phrases, or operators. In addition to `search`, you can specify other parameters to refine the search behavior and results.

Our query searches for the terms "attached restaurant" in the `Description` and `Tags` fields of each hotel document. The `select` parameter limits the fields returned in the response to `HotelId`, `HotelName`, `Tags`, and `Description`. The `count` parameter requests the total number of matching documents.

The response should be similar to the following example, which shows one matching hotel document, its relevance score, and its selected fields.

```json
{
  "@odata.context": "https://my-service.search.windows.net/indexes('hotels-quickstart')/$metadata#docs(*)",
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 0.5575875,
      "HotelId": "3",
      "HotelName": "Gastronomic Landscape Hotel",
      "Description": "The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel\u2019s restaurant services.",
      "Tags": [
        "restaurant",
        "bar",
        "continental breakfast"
      ]
    }
  ]
}
```
