---
manager: nitinme
author: rotabor
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/05/2026
ms.custom: dev-focus
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Python](/python/api/overview/azure/search-documents-readme) to create, load, and query a [vector index](../../vector-store.md). The Python client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Quickstart-Vector-Search) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

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
   cd azure-search-python-samples/Quickstart-Vector-Search
   code .
   ```

1. In `sample.env`, replace the placeholder value for `AZURE_SEARCH_ENDPOINT` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Rename `sample.env` to `.env`.

   ```bash
   mv sample.env .env
   ```

1. Open `vector-search-quickstart.ipynb`.

1. Press **Ctrl+Shift+P**, select **Notebook: Select Notebook Kernel**, and follow the prompts to create a virtual environment. Select **requirements.txt** for the dependencies.

   When complete, you should see a `.venv` folder in the project directory.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

## Run the code

1. Run the `Install packages and set variables` cell to load environment variables and verify the package installation.

1. Run the `Create an index` cell to create a vector index in Azure AI Search.

1. Run the `Create documents payload` cell to prepare the documents for upload.

1. Run the `Upload the documents` cell to upload documents to the index.

1. Run the `Create the vector query string` cell to load the vectorized query data.

1. Run the search cells. Start with `Single vector search`, and then try `Single vector search with filter`, `Vector query with a geo filter`, `Hybrid search`, and `Semantic hybrid search`.

### Output

The output of the `Upload the documents` cell shows the success status of each document.

```output
Key: 1, Succeeded: True, ErrorMessage: None
Key: 2, Succeeded: True, ErrorMessage: None
Key: 3, Succeeded: True, ErrorMessage: None
Key: 4, Succeeded: True, ErrorMessage: None
Key: 48, Succeeded: True, ErrorMessage: None
Key: 49, Succeeded: True, ErrorMessage: None
Key: 13, Succeeded: True, ErrorMessage: None
```

The output of the `Single vector search` cell shows vector search results.

```output
Total results: 7
- HotelId: 48, HotelName: Nordick's Valley Motel, Category: Boutique
- HotelId: 13, HotelName: Luxury Lion Resort, Category: Luxury
- HotelId: 4, HotelName: Sublime Palace Hotel, Category: Boutique
- HotelId: 49, HotelName: Swirling Currents Hotel, Category: Suite
- HotelId: 2, HotelName: Old Century Hotel, Category: Boutique
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

[!INCLUDE [understand code note](../understand-code-note.md)]

### Create a vector index

The `Create an index` cell in the notebook creates a vector index in Azure AI Search. The index schema defines the fields, including the vector field `DescriptionVector`.

```python
fields = [
    SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True, filterable=True),
    SearchableField(name="HotelName", type=SearchFieldDataType.String, sortable=True),
    SearchableField(name="Description", type=SearchFieldDataType.String),
    SearchField(
        name="DescriptionVector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-profile"
    ),
    SearchableField(name="Category", type=SearchFieldDataType.String, sortable=True, filterable=True, facetable=True),
    SearchField(name="Tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String), searchable=True, filterable=True, facetable=True),
    # Additional fields omitted for brevity
]
```

Key takeaways:

+ You define an index by creating a list of fields. Each field is created using a helper method that defines the field type and its settings.

+ This particular index supports multiple search capabilities:

    + [Full-text search](../../search-lucene-query-architecture.md) (`SearchableField`)

    + [Vector search](../../vector-search-overview.md) (`DescriptionVector` with `vector_search_profile_name`)

    + [Semantic ranking](../../semantic-search-overview.md) (`SemanticConfiguration`)

    + [Faceted search](../../search-faceted-navigation.md) (`SearchSuggester`)

    + [Geo-spatial search](../../search-query-odata-geo-spatial-functions.md) (`Location` field with `SearchFieldDataType.GeographyPoint`)

    + [Filtering](../../search-filters.md) and sorting (fields marked with `filterable` and `sortable`)

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The `Create documents payload` and `Upload the documents` cells load documents into the index. Each document includes the vectorized version of the article's description, which enables similarity search based on meaning rather than exact keywords.

```python
documents = [
    # List of hotel documents with embedded 1536-dimension vectors
    # Each document contains: HotelId, HotelName, Description, DescriptionVector,
    # Category, Tags, ParkingIncluded, LastRenovationDate, Rating, Address, Location
]

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)

result = search_client.upload_documents(documents=documents)
for r in result:
    print(f"Key: {r.key}, Succeeded: {r.succeeded}, ErrorMessage: {r.error_message}")
```

Key takeaways:

+ Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the `azure-search-documents` package. The `SearchClient` provides access to index operations, such as:

    + Data ingestion: `upload_documents()`, `merge_documents()`, `delete_documents()`
    
    + Search operations: `search()`, `autocomplete()`, `suggest()`

    + Index management operations: `get_index_statistics()`, `get_document_count()`

### Query the index

The queries in the notebook demonstrate different search patterns. The example vector queries are based on two strings:

+ Search string: "historic hotel walk to restaurants and shopping"
+ Vector query string: "quintessential lodging near running trails, eateries, retail" (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for "quintessential lodging near running trails, eateries, retail", results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

The `Single vector search` cell demonstrates a basic scenario where you want to find document descriptions that closely match the search string. The `VectorizedQuery` contains the configuration of the vectorized query.

```python
vector_query = VectorizedQuery(
    vector=vector,
    k_nearest_neighbors=5,
    fields="DescriptionVector",
    kind="vector",
    exhaustive=True
)

results = search_client.search(
    vector_queries=[vector_query],
    select=["HotelId", "HotelName", "Description", "Category", "Tags"],
    top=5,
    include_total_count=True
)
```

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. The `Single vector search with filter` cell filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```python
# vector_query omitted for brevity

results = search_client.search(
    vector_queries=[vector_query],
    filter="Tags/any(tag: tag eq 'free wifi')",
    select=["HotelId", "HotelName", "Description", "Category", "Tags"],
    top=7,
    include_total_count=True
)
```

#### Vector query with a geo filter

The `Vector query with a geo filter` cell uses [geo-spatial functions](../../search-query-odata-geo-spatial-functions.md) to filter results based on location. In this example, the filter returns hotels within 300 kilometers of Washington D.C.

```python
# vector_query omitted for brevity

results = search_client.search(
    include_total_count=True,
    top=5,
    select=[
        "HotelId", "HotelName", "Category", "Description", "Address/City", "Address/StateProvince"
    ],
    facets=["Address/StateProvince"],
    filter="geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
    vector_filter_mode="postFilter",
    vector_queries=[vector_query]
)
```

The `filter` parameter specifies a geographic point (Washington D.C., using longitude and latitude coordinates) and returns hotels within 300 kilometers. The `vector_filter_mode` parameter determines when the filter runs. In this case, `postFilter` runs the filter after the vector search.

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. The `Hybrid search` cell runs the full-text and vector query strings concurrently.

```python
# vector_query omitted for brevity

results = search_client.search(
    search_text="historic hotel walk to restaurants and shopping",
    vector_queries=[vector_query],
    select=["HotelId", "HotelName", "Description", "Category", "Tags"],
    top=5,
    include_total_count=True
)
```

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

This example adds [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding. The `Semantic hybrid search` cell adds semantic ranking.

```python
# vector_query omitted for brevity

results = search_client.search(
    search_text="historic hotel walk to restaurants and shopping",
    vector_queries=[vector_query],
    select=["HotelId", "HotelName", "Category", "Description"],
    query_type="semantic",
    semantic_configuration_name="my-semantic-config",
    top=5,
    include_total_count=True
)
```

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. This quickstart modifies results for readability. To get the full structure of the response, run the request using REST.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, you can run the `Clean up` code cell to delete the index you created in this quickstart.
