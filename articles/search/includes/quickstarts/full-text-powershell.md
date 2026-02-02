---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/30/2026
---

In this quickstart, you use PowerShell and the [Azure AI Search REST APIs](/rest/api/searchservice/) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results. This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) GitHub repository to populate the index.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-powershell-samples/tree/main/Quickstart) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md). You can use a free service for this quickstart.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

+ The latest version of [PowerShell](https://github.com/PowerShell/PowerShell).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```powershell
   git clone https://github.com/Azure-Samples/azure-search-powershell-samples
   ```

1. Navigate to the `Quickstart` folder.

   ```powershell
   cd azure-search-powershell-samples/Quickstart
   ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account.

    ```azurecli
    az login
    ```

1. Open the `azure-search-quickstart.ps1` file in a text editor.

1. Set the `$baseUrl` variable to the URL you obtained in [Get endpoint](#get-endpoint).

## Run the code

In the same terminal window, run the following PowerShell script to execute this quickstart.

```powershell
.\azure-search-quickstart.ps1
```

### Output

The script creates a search index, uploads documents, and runs multiple full-text search queries. The result of each operation is printed to the console. The following example shows the response when searching for `restaurant wifi`:

```json
{
  "value": [
    {
      "@search.score": 0.6931472,
      "HotelName": "Old Century Hotel",
      "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
      "Tags": ["pool", "free wifi", "concierge"]
    },
    {
      "@search.score": 0.5575875,
      "HotelName": "Gastronomic Landscape Hotel",
      "Description": "The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services.",
      "Tags": ["restaurant", "bar", "continental breakfast"]
    }
  ]
}
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a search index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured. An index is conceptually similar to a table in a relational database, but it's specifically designed for search operations, such as full-text search.

This quickstart calls [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) to build a search index named `hotels-quickstart` and its physical data structures on your search service.

Within the index schema, the `fields` collection defines the structure of hotel documents. Each field has a `name`, data `type`, and attributes that determine its behavior during indexing and queries. The `HotelId` field is marked as the key, which Azure AI Search requires to uniquely identify each document in an index.

Key points about the index schema:

+ Use string fields (`Edm.String`) to make numeric data full-text searchable. Other [supported data types](/rest/api/searchservice/supported-data-types), such as `Edm.Int32`, are filterable, sortable, facetable, and retrievable but aren't searchable.

+ Most of our fields are simple data types, but you can define complex types to represent nested data, such as the `Address` field.

+ Field attributes determine allowed actions. The REST APIs allow [many actions by default](/rest/api/searchservice/indexes/create#request-body). For example, all strings are searchable and retrievable. With the REST APIs, you might only use attributes if you need to disable a behavior.

### Upload documents to the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents as inline JSON. In production scenarios, however, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

This quickstart calls [Documents - Index (REST API)](/rest/api/searchservice/documents/) to add four sample hotel documents to your index. Compared to the previous request, the URI is extended to include the `docs` collection and `index` operation.

Each document in the `value` array represents a hotel and contains fields that match the index schema. The `@search.action` parameter specifies the operation to perform for each document. Our example uses `upload`, which adds the document if it doesn't exist or updates the document if it does exist.

### Query the index

Now that documents are loaded into your index, you can use full-text search to find specific terms or phrases within their fields.

This quickstart calls [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post) to find hotel documents that match your search criteria. The URI now targets the `/docs/search` operation.

Full-text search requests always include a `search` parameter that contains the query text. The query text can include one or more terms, phrases, or operators. In addition to `search`, you can specify other parameters to refine the search behavior and results.

Our query searches for the terms "attached restaurant" in the `Description` and `Tags` fields of each hotel document. The `$select` parameter limits the fields returned in the response to `HotelId`, `HotelName`, `Tags`, and `Description`. The `$count` parameter requests the total number of matching documents.

#### Other query examples

Run the following commands to explore the query syntax. You can perform string searches, use `$filter` expressions, limit result sets, select specific fields, and more. Remember to replace `<YOUR-SEARCH-SERVICE>` with the value you obtained in [Get endpoint](#get-endpoint).

```powershell
# Query example 1
# Search the index for the terms 'restaurant' and 'wifi'
# Return only the HotelName, Description, and Tags fields
$url = '<YOUR-SEARCH-SERVICE>/indexes/hotels-quickstart/docs?api-version=2025-09-01&search=restaurant wifi&$count=true&$select=HotelName,Description,Tags'

# Query example 2 
# Use a filter to find hotels rated 4 or higher
# Return only the HotelName and Rating fields
$url = '<YOUR-SEARCH-SERVICE>/indexes/hotels-quickstart/docs?api-version=2025-09-01&search=*&$filter=Rating gt 4&$select=HotelName,Rating'

# Query example 3
# Take the top two results
# Return only the HotelName and Category fields
$url = '<YOUR-SEARCH-SERVICE>/indexes/hotels-quickstart/docs?api-version=2025-09-01&search=boutique&$top=2&$select=HotelName,Category'

# Query example 4
# Sort by a specific field (Address/City) in ascending order
# Return only the HotelName, Address/City, Tags, and Rating fields
$url = '<YOUR-SEARCH-SERVICE>/indexes/hotels-quickstart/docs?api-version=2025-09-01&search=pool&$orderby=Address/City asc&$select=HotelName, Address/City, Tags, Rating'
```
