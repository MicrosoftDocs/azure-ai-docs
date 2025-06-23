---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/23/2025
---

In this quickstart, you use the [Search REST APIs](/rest/api/searchservice) to create, load, and query a search index with sample data for [full-text search](../../search-lucene-query-architecture.md). Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results.

This quickstart creates and queries a small `hotels-quickstart` index containing data about four hotels.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart) to start with a finished project or follow these steps to create your own.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. For this quickstart, you can use a free service.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

- [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

## Configure role-based access

You can use search service API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. [Enable role-based access](../../search-security-enable-roles.md) on your search service.

1. Assign the `Search Service Contributor` and `Search Index Data Contributor` roles to your user account. For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Retrieve service information

In your code, you specify the following endpoint and token to establish a connection with your Azure AI Search service. These steps assume that you [configured role-based access](#configure-role-based-access).

To retrieve your service information:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Overview**.

1. Copy the URL, which should be similar to `https://my-service.search.windows.net`.

1. On your local system, open a terminal.

1. Run the following command to sign in to Azure. If you have multiple subscriptions, select the one that contains your search service.

    ```azurecli
    az login
    ```

1. Run the following command to obtain your Microsoft Entra token. You specify this value in the next section.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default
    ```

## Set up your file

1. In Visual Studio Code, create a `.rest` or `.http` file.

1. Paste the following placeholders and request into the file.

    ```http
    @baseUrl = PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE
    @token = PUT-YOUR-PERSONAL-IDENTITY-TOKEN-HERE

    ### List existing indexes by name
        GET {{baseUrl}}/indexes?api-version=2023-11-01
        Authorization: Bearer {{token}}
    ```

1. Replace the `@baseUrl` and `@token` placeholders with the values you obtained in [Retrieve service information](#retrieve-service-information).

1. Under `### List existing indexes by name`, select **Send Request** to verify that you can connect to Azure AI Search.

    A response should appear in an adjacent pane. If you have existing indexes, they're listed. Otherwise, the list is empty. If the HTTP code is `200 OK`, you're ready for the next steps.

    :::image type="content" source="../../media/search-get-started-rest/rest-client-request-setup.png" lightbox="media/search-get-started-rest/rest-client-request-setup.png" alt-text="Screenshot that shows a REST client configured for a search service request.":::

## Create, load, and query a search index

In this section, you use the same file to create a search index, load the index with documents, and run queries. For a detailed explanation of the code, see [Explaining the code](#explaining-the-code).

To send the remaining requests for this quickstart:

1. Paste the following request to create the `hotels-quickstart` index on your search service.

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
    ```

1. Under `### Create a new index`, select **Send Request**. You should receive an `HTTP/1.1 201 Created` response whose body includes the JSON representation of the index schema.

1. Paste the following request to upload JSON documents to the  index.

    ```http
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
    ```

1. Under `### Upload documents`, select **Send Request**. You should receive an `HTTP/1.1 200 OK` response.

1. Paste the following request to query the index.

    ```http
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

1. Under `### Run a query`, select **Send Request**. You should receive an `HTTP/1.1 200 OK` response.

## Explaining the code

This section explains the requests that you sent to create, load, and query the `hotels-quickstart` search index.

### Create an index

### Load documents

### Search an index
