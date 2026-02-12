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

1. Run the remaining cells sequentially to create a vector index, upload documents, and run different types of vector queries.

### Output

Each code cell prints its output to the notebook. The following example is the output of `Single vector search`, which shows vector search results ranked by similarity score.

```output
Total results: 7
- HotelId: 48, HotelName: Nordick's Valley Motel, Category: Boutique
- HotelId: 13, HotelName: Luxury Lion Resort, Category: Luxury
- HotelId: 4, HotelName: Sublime Palace Hotel, Category: Boutique
- HotelId: 49, HotelName: Swirling Currents Hotel, Category: Suite
- HotelId: 2, HotelName: Old Century Hotel, Category: Boutique
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

Before you add content to Azure AI Search, you must create an index to define how the content is stored and structured.

The index schema is organized around hotel content. Sample data consists of vector and nonvector descriptions of fictitious hotels. The `Create an index` cell in the notebook creates the index schema, including the vector field `DescriptionVector`.

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

    + [Faceted search](../../search-faceted-navigation.md) (fields marked with `facetable`)

    + [Geo-spatial search](../../search-query-odata-geo-spatial-functions.md) (`Location` field with `SearchFieldDataType.GeographyPoint`)

    + [Filtering](../../search-filters.md) and sorting (fields marked with `filterable` and `sortable`)

+ The `vector_search_dimensions` property must match the output size of your embedding model. This quickstart uses 1,536 dimensions to match the `text-embedding-ada-002` model.

+ The `VectorSearch` configuration defines the Approximate Nearest Neighbor (ANN) algorithm. Supported algorithms include Hierarchical Navigable Small World (HNSW) and exhaustive K-Nearest Neighbor (KNN). For more information, see [Relevance in vector search](../../vector-search-ranking.md).

### Upload documents to the index

Newly created indexes are empty. To populate an index and make it searchable, you must upload JSON documents that conform to the index schema.

In Azure AI Search, documents serve as both inputs for indexing and outputs for queries. For simplicity, this quickstart provides sample hotel documents with precomputed vectors. In production scenarios, content is often pulled from connected data sources and transformed into JSON using [indexers](../../search-indexer-overview.md).

The `Create documents payload` and `Upload the documents` cells load documents into the index.

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

Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the [`azure-search-documents`](/python/api/overview/azure/search-documents-readme) package. The `SearchClient` provides access to index operations, such as:

+ Data ingestion: `upload_documents()`, `merge_documents()`, `delete_documents()`

+ Search operations: `search()`, `autocomplete()`, `suggest()`

### Query the index

The queries in the notebook demonstrate different search patterns. The example vector queries are based on two strings:

+ Full-text search string: `"historic hotel walk to restaurants and shopping"`

+ Vector query string: `"quintessential lodging near running trails, eateries, retail"` (vectorized into a mathematical representation)

The vector query string is semantically similar to the full-text search string, but it includes terms that don't exist in the index. A keyword-only search for the vector query string returns zero results. However, vector search finds relevant matches based on meaning rather than exact keywords.

The following examples start with a basic vector query and progressively add filters, keyword search, and semantic reranking.

#### Single vector search

The `Single vector search` cell demonstrates a basic scenario where you want to find document descriptions that closely match the vector query string. `VectorizedQuery` configures the vector search:

+ `k_nearest_neighbors` limits how many results are returned based on vector similarity.
+ `fields` specifies the vector field to search against.

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

#### Single vector search with a filter

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

#### Single vector search with a geo filter

You can specify a [geo-spatial filter](../../search-query-odata-geo-spatial-functions.md) to limit results to a specific geographic area. The `Single vector search with geo filter` cell specifies a geographic point (Washington D.C., using longitude and latitude coordinates) and returns hotels within 300 kilometers. The `vector_filter_mode` parameter determines when the filter runs. In this case, `postFilter` runs the filter after the vector search.

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

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines full-text and vector queries in a single request. The `Hybrid search` cell runs both query types concurrently, and then uses Reciprocal Rank Fusion (RRF) to merge the results into a unified ranking. RRF uses the inverse of result rankings from each result set to produce a merged ranking. Notice that hybrid search scores are uniformly smaller than single-query scores.

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

#### Semantic hybrid search

The `Semantic hybrid search` cell demonstrates [semantic ranking](../../semantic-search-overview.md), which reranks results based on language understanding.

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

Compare these results with the hybrid search results from the previous query. Without semantic reranking, Sublime Palace Hotel ranks first because Reciprocal Rank Fusion (RRF) combines the text and vector scores to produce a merged result. After semantic reranking, Swirling Currents Hotel moves to the top spot.

The semantic ranker uses machine comprehension models to evaluate how well each result matches the intent of the query. Swirling Currents Hotel's description mentions `"walking access to shopping, dining, entertainment and the city center"`, which aligns closely with the search query's `"walk to restaurants and shopping"`. This semantic match for nearby dining and shopping elevates it above Sublime Palace Hotel, which doesn't emphasize walkable amenities in its description.

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters and semantic ranking apply to textual content only, not vectors.

+ Actual results include more detail, including semantic captions and highlights. This quickstart modifies results for readability. To get the full structure of the response, use REST to run the request.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, you can run the `Clean up` code cell to delete the index you created in this quickstart.
