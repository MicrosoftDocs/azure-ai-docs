---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
---

In this quickstart, you use the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results. This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) GitHub repository to populate the index.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Keyword-Search) on GitHub.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use a free service for this quickstart.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

- [Git](https://git-scm.com/downloads) to clone the sample repository.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```console
   git clone https://github.com/Azure-Samples/azure-search-python-samples
   ```

1. Open the `azure-search-python-samples/Quickstart-Keyword-Search` folder in Visual Studio Code.

1. Open the `azure-search-quickstart.ipynb` file.

1. Create a virtual environment for installing the packages.

    # [Windows](#tab/windows)
    
    ```bash
    py -3 -m venv .venv
    .venv\scripts\activate
    ```
    
    # [Linux](#tab/linux)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    # [macOS](#tab/macos)
    
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
    ---

1. In the upper-right corner of the notebook, select **Select Kernel**, and then select the virtual environment you created.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Run the first code cell to install the required packages.

1. In the second code cell, replace the placeholder value for `search_endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Run the second code cell to import the required libraries and set up the search client.

1. Run the remaining code cells sequentially to create an index, load documents, and run queries.

### Output

Each code cell prints its output to the notebook. The following example is the output of the first query, an empty search that returns all documents in the index.

```
Total Documents Matching Query: 4
1.0
Gastronomic Landscape Hotel
['restaurant', 'bar', 'continental breakfast']
Description: The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.
1.0
Old Century Hotel
['pool', 'free wifi', 'concierge']
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
1.0
Sublime Palace Hotel
['concierge', 'view', 'air conditioning']
Description: Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
1.0
Stay-Kay City Hotel
['view', 'air conditioning', 'concierge']
Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)
1. [Remove the index](#remove-the-index)

### Create a search index

`SearchIndexClient` is used to create and manage indexes for Azure AI Search. Each field is identified by a `name` and has a specified `type`. 

Each field also has a series of index attributes that specify whether Azure AI Search can search, filter, sort, and facet upon the field. Most of the fields are simple data types, but some, like `AddressType` are complex types that allow you to create rich data structures in your index. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create). 

### Upload documents to the index

Use an [index action](/python/api/azure-search-documents/azure.search.documents.models.indexaction) for the operation type, such as upload or merge-and-upload. Documents originate from the [HotelsData](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/hotels/HotelsData_toAzureSearch.JSON) sample on GitHub.

### Query the index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

Use the *search* method of the [search.client class](/python/api/azure-search-documents/azure.search.documents.searchclient).

The sample queries in the notebook are:

- Basic query: Executes an empty search (`search=*`), returning an unranked list (search score = 1.0) of arbitrary documents. Because there are no criteria, all documents are included in results.
- Term query: Adds whole terms to the search expression ("wifi"). This query specifies that results contain only those fields in the `select` statement. Limiting the fields that come back minimizes the amount of data sent back over the wire and reduces search latency.
- Filtered query: Add a filter expression, returning only those hotels with a rating greater than four, sorted in descending order.
- Fielded scoping: Add `search_fields` to scope query execution to specific fields.
- Facets: Generate facets for positive matches found in search results. There are no zero matches. If search results don't include the term *wifi*, then *wifi* doesn't appear in the faceted navigation structure.
- Look up a document: Return a document based on its key. This operation is useful if you want to provide drill through when a user selects an item in a search result.
- Autocomplete: Provide potential matches as the user types into the search box. Autocomplete uses a suggester (`sg`) to know which fields contain potential matches to suggester requests. In this quickstart, those fields are `Tags`, `Address/City`, `Address/Country`. To simulate autocomplete, pass in the letters *sa* as a partial string. The autocomplete method of [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient) sends back potential term matches.

### Remove the index

If you're finished with this index, you can delete it by running the `Clean up` code cell. Deleting unnecessary indexes frees up space for stepping through more quickstarts and tutorials.