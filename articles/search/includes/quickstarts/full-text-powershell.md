---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/26/2025
---

In this quickstart, you use PowerShell and the [Azure AI Search REST APIs](/rest/api/searchservice/) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md). Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results.

This quickstart creates and queries a small index containing data about four fictional hotels.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-powershell-samples/tree/main/Quickstart) to start with a finished project or follow these steps to create your own.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. For this quickstart, you can use a free service.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ [PowerShell 7.3](https://github.com/PowerShell/PowerShell) or later. This quickstart uses the [Invoke-RestMethod](/powershell/module/Microsoft.PowerShell.Utility/Invoke-RestMethod) cmdlet to make REST API calls.

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

## Get resource name

In the next section, you specify the following endpoint to establish a connection to your Azure AI Search service. These steps assume that you [configured role-based access](#configure-access).

To get your resource name:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Overview**.

1. Take note of the name before `.search.windows.net` in the URL, such as `my-service` in `https://my-service.search.windows.net`.

## Connect to Azure AI Search

Before you can make REST API calls to Azure AI Search, you must authenticate and connect to your search service.

You start by using the Azure CLI to sign in to Azure and obtain your Microsoft Entra token. You then configure the HTTP header and service URL used in subsequent requests. To maintain authentication throughout this quickstart, all of these commands are run in the same PowerShell session.

To connect to your search service:

1. On your local system, open PowerShell.

1. Sign in to your Azure subscription. If you have multiple subscriptions, select the one that contains your search service.

    ```powershell
    az login
    ```

1. Create a `$token` object to store your access token.

    ```powershell
    $token = az account get-access-token --resource https://search.azure.com/ --query accessToken --output tsv
    ```

1. Create a `$headers` object to store your token and content type.

    ```powershell
    $headers = @{
    'Authorization' = "Bearer $token"
    'Content-Type' = 'application/json' 
    'Accept' = 'application/json' }
    ```

    You only need to set the header once per session, but you must add it to each request.

1. Create a `$url` object that targets the indexes collection on your search service. Replace `<YOUR-SEARCH-SERVICE>` with the value you obtained in [Get resource name](#get-resource-name).

    ```powershell
    $url = "https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes?api-version=2024-07-01&`$select=name"
    ```

1. Run `Invoke-RestMethod` to send a GET request to your search service and verify the connection. Include `ConvertTo-Json` to view responses from the service.

    ```powershell
    Invoke-RestMethod -Uri $url -Headers $headers | ConvertTo-Json
    ```

   If your service is empty and has no indexes, the response is similar to the following example. Otherwise, you see a JSON representation of index definitions.

    ```
    {
        "@odata.context":  "https://my-service.search.windows.net/$metadata#indexes",
        "value":  [

                  ]
    }
    ```

## Create, load, and query a search index

In this section, you run PowerShell commands to create a search index, upload documents to the index, and query the indexed documents. Responses to the `Invoke-RestMethod` commands are displayed in the PowerShell console. For more information about each step, see [Explaining the code](#explaining-the-code).

For each command that updates the `$url` object, replace `<YOUR-SEARCH-SERVICE>` with the value you obtained in [Get resource name](#get-resource-name).

To create, load, and query an index:

1. Define the index schema in a `$body` object.

    ```powershell
    $body = @"
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
    "@
    ```

1. Update the `$url` object to target the new index.

    ```powershell
    $url = "https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart?api-version=2024-07-01"
    ```

1. Run `Invoke-RestMethod` with `$url`, `$headers`, and `$body` to create the index on your search service.

    ```powershell
    Invoke-RestMethod -Uri $url -Headers $headers -Method Put -Body $body | ConvertTo-Json
    ```

    The response should contain the JSON representation of the index schema.

1. Create a `$body` object that contains sample documents to upload to your index.

    ```powershell
    $body = @"
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
    "@
    ```

1. Update the `$url` object to target the `docs/index` endpoint of your index.

    ```powershell
    $url = "https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs/index?api-version=2024-07-01"
    ```

1. Run `Invoke-RestMethod` with `$url`, `$headers`, and `$body` to upload the documents to your index.

    ```powershell
    Invoke-RestMethod -Uri $url -Headers $headers -Method Post -Body $body | ConvertTo-Json
    ```

    The response should contain the key and status of each uploaded document.

1. Update the `$url` object to target the `docs` endpoint of your index and specify a query string in a `search` parameter.

    ```powershell
    $url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=*&$count=true'
    ```

1. Run `Invoke-RestMethod` with `$url` and `$headers` to query the documents in your index.

    ```powershell
    Invoke-RestMethod -Uri $url -Headers $headers | ConvertTo-Json
    ```

    The response should contain the total count of documents and an array of the documents themselves.

## Explaining the code

This section explains the PowerShell commands that you ran to:

+ [Create an index](#create-an-index)
+ [Load documents into the index](#load-documents-into-the-index)
+ [Query the index](#query-the-index)

### Create an index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured. An index is conceptually similar to a table in a relational database, but it's specifically designed for search operations, such as full-text search.

This quickstart calls [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) to build a search index named `hotels-quickstart` and its physical data structures on your search service.

```powershell
$body = @"
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
"@

$url = "https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart?api-version=2024-07-01"
```

Within our index schema, the `fields` collection defines the structure of hotel documents. Each field has a `name`, data `type`, and attributes that determine its behavior during indexing and queries. The `HotelId` field is marked as the key, which Azure AI Search requires to uniquely identify each document in an index.

Key points about the index schema:

+ Use string fields (`Edm.String`) to make numeric data full-text searchable. Other [supported data types](/rest/api/searchservice/supported-data-types), such as `Edm.Int32`, are filterable, sortable, facetable, and retrievable but aren't searchable.

+ Most of our fields are simple data types, but you can define complex types to represent nested data, such as the `Address` field.

+ Field attributes determine allowed actions. The REST APIs allow [many actions by default](/rest/api/searchservice/indexes/create#request-body). For example, all strings are searchable and retrievable. With the REST APIs, you might only use attributes if you need to disable a behavior.

### Load documents into the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents as inline JSON. In production scenarios, however, content is typically pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

This quickstart calls [Documents - Index (REST API)](/rest/api/searchservice/documents/index) to add four sample hotel documents to your index.

```powershell
$body = @"
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
"@

$url = "https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs/index?api-version=2024-07-01"
```

Each document in the `value` array represents a hotel and contains fields that match the index schema. The `@search.action` parameter specifies the operation to perform for each document. Our example uses `upload`, which adds the document if it doesn't exist or updates the document if it does exist.

### Query the index

Now that documents are loaded into the index, you can issue full-text queries against them using PowerShell commands.

This quickstart calls [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post) to find hotel documents in your index based on the search criteria.

```powershell
$url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=*&$count=true'
```

Full-text search requests always include a `search` parameter that contains the query text. The query text can include one or more terms, phrases, or operators. You can also specify parameters to refine the search behavior and results.

Our example performs an empty search (`search=*`) that returns all documents in the index. The `$count=true` parameter includes the total number of matching documents in the response.

#### Other query examples

Try some other query examples to explore the syntax. You can perform string searches, use `$filter` expressions, limit result sets, select specific fields, and more.

```powershell
# Query example 1
# Search the entire index for the terms 'restaurant' and 'wifi'
# Return only the HotelName, Description, and Tags fields
$url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=restaurant wifi&$count=true&$select=HotelName,Description,Tags'

# Query example 2 
# Apply a filter to the index to find hotels rated 4 or higher
# Returns the HotelName and Rating. Two documents match.
$url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=*&$filter=Rating gt 4&$select=HotelName,Rating'

# Query example 3
# Take the top two results, and show only HotelName and Category in the results
$url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=boutique&$top=2&$select=HotelName,Category'

# Query example 4
# Sort by a specific field (Address/City) in ascending order
$url = 'https://<YOUR-SEARCH-SERVICE>.search.windows.net/indexes/hotels-quickstart/docs?api-version=2024-07-01&search=pool&$orderby=Address/City asc&$select=HotelName, Address/City, Tags, Rating'
```
