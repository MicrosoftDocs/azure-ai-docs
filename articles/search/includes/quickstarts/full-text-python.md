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

- [Python 3.8](https://www.python.org/downloads/) or later.

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions.

- [Git](https://git-scm.com/downloads) to clone the sample repository.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-python-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-python-samples/Quickstart-Keyword-Search
    code .
    ```

1. Open `azure-search-quickstart.ipynb`.

1. Press **Ctrl+Shift+P**, select **Notebook: Select Notebook Kernel**, and follow the prompts to create a virtual environment.

   When complete, you should see a `.venv` folder in the project directory.

1. Run the first code cell to install the required packages.

1. In the second code cell, replace the placeholder value for `search_endpoint` with the URL you obtained in [Get endpoint](#get-endpoint), and run the cell.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

## Run the code

Run the remaining code cells sequentially to create an index, upload documents, and query the index.

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

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create the clients](#create-the-clients)
1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)
1. [Remove the index](#remove-the-index)

### Create the clients

The notebook creates two clients:

- [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient) creates and manages indexes.
- [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient) loads documents and runs queries.

Both clients require the service endpoint and a credential. In this quickstart, you use [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) for keyless authentication with Microsoft Entra ID.

### Create a search index

This quickstart builds a hotels index that you load with hotel data and run queries against. In this step, you define the fields in the index. Each field definition includes a name, data type, and attributes that determine how the field is used.

The notebook uses `SimpleField`, `SearchableField`, and `ComplexField` from the [models package](/python/api/azure-search-documents/azure.search.documents.indexes.models) to define the schema. You can read more about [supported data types](/rest/api/searchservice/supported-data-types) and index attributes described in [Create Index (REST)](/rest/api/searchservice/indexes/create).

```python
# Create a search schema
index_client = SearchIndexClient(
    endpoint=search_endpoint, credential=credential)
fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SearchableField(name="HotelName", type=SearchFieldDataType.String, sortable=True),
        SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SearchableField(name="Category", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),

        SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True),

        SimpleField(name="ParkingIncluded", type=SearchFieldDataType.Boolean, facetable=True, filterable=True, sortable=True),
        SimpleField(name="LastRenovationDate", type=SearchFieldDataType.DateTimeOffset, facetable=True, filterable=True, sortable=True),
        SimpleField(name="Rating", type=SearchFieldDataType.Double, facetable=True, filterable=True, sortable=True),

        ComplexField(name="Address", fields=[
            SearchableField(name="StreetAddress", type=SearchFieldDataType.String),
            SearchableField(name="City", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="StateProvince", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="PostalCode", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="Country", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
        ])
    ]

scoring_profiles = []
suggester = [{'name': 'sg', 'source_fields': ['Tags', 'Address/City', 'Address/Country']}]

# Create the search index=
index = SearchIndex(name=index_name, fields=fields, suggesters=suggester, scoring_profiles=scoring_profiles)
result = index_client.create_or_update_index(index)
print(f' {result.name} created')
```

### Upload documents to the index

Azure AI Search searches over content stored in the service. In this step, you load JSON documents that conform to the hotel index you created.

In Azure AI Search, documents are data structures that are both inputs to indexing and outputs from queries. The notebook defines a documents payload as a list of dictionaries containing hotel data.

```python
# Create a documents payload
documents = [
    {
    "@search.action": "upload",
    "HotelId": "1",
    "HotelName": "Stay-Kay City Hotel",
    "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
    "Category": "Boutique",
    "Tags": [ "view", "air conditioning", "concierge" ],
    "ParkingIncluded": "false",
    "LastRenovationDate": "2020-01-18T00:00:00Z",
    "Rating": 3.60,
    "Address": {
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
    "ParkingIncluded": "false",
    "LastRenovationDate": "2019-02-18T00:00:00Z",
    "Rating": 3.60,
    "Address": {
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
    "ParkingIncluded": "true",
    "LastRenovationDate": "2015-09-20T00:00:00Z",
    "Rating": 4.80,
    "Address": {
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
    "Category": "Boutique",
    "Tags": [ "concierge", "view", "air conditioning" ],
    "ParkingIncluded": "true",
    "LastRenovationDate": "2020-02-06T00:00:00Z",
    "Rating": 4.60,
    "Address": {
        "StreetAddress": "7400 San Pedro Ave",
        "City": "San Antonio",
        "StateProvince": "TX",
        "PostalCode": "78216",
        "Country": "USA"
        }
    }
]
```

The `upload_documents` method adds documents to the index, creating them if they don't exist or updating them if they do.

```python
search_client = SearchClient(endpoint=search_endpoint,
                      index_name=index_name,
                      credential=credential)

try:
    result = search_client.upload_documents(documents=documents)
    print("Upload of new document succeeded: {}".format(result[0].succeeded))
except Exception as ex:
    print (ex.message)
```

### Query the index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

Use the `search` method of [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient) to run queries.

The sample queries in the notebook demonstrate common patterns:

- **Empty search**: Executes an empty search (`search_text="*"`), returning an unranked list (search score = 1.0) of arbitrary documents. Because there are no criteria, all documents are included in results.

- **Term search**: Adds whole terms to the search expression (`search_text="wifi"`). This query specifies that results contain only those fields in the `select` parameter. Limiting the fields that come back minimizes the amount of data sent back over the wire and reduces search latency.

- **Filtered search**: Adds a filter expression, returning only those hotels with a rating greater than four, sorted in descending order.

- **Fielded search**: Adds `search_fields` to scope query execution to specific fields.

- **Faceted search**: Generates facets for positive matches found in search results. There are no zero matches. If search results don't include the term "wifi", then "wifi" doesn't appear in the faceted navigation structure.

- **Document lookup**: Returns a document based on its key. This operation is useful if you want to provide drillthrough when a user selects an item in a search result.

- **Autocomplete**: Provides potential matches as the user types into the search box. Autocomplete uses a suggester (`sg`) to know which fields contain potential matches to suggester requests. In this quickstart, those fields are `Tags`, `Address/City`, and `Address/Country`. To simulate autocomplete, pass in the letters "sa" as a partial string. The `autocomplete` method of `SearchClient` sends back potential term matches.

### Remove the index

If you're finished with this index, you can delete it by running the `Clean up` code cell. Deleting unnecessary indexes frees up space for stepping through more quickstarts and tutorials.

```python
try:
    result = index_client.delete_index(index_name)
    print ('Index', index_name, 'Deleted')
except Exception as ex:
    print (ex)
```