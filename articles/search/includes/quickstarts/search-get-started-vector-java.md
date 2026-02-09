---
author: KarlErickson
ms.author: karler
ms.service: azure-ai-search
ms.custom: devx-track-java, dev-focus
ms.topic: include
ms.date: 02/05/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for Java](/java/api/overview/azure/search-documents-readme) to create, load, and query a [vector index](../../vector-store.md). The Java client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-vector-search) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [Java 21 (LTS)](/java/openjdk/install) and [Maven](https://maven.apache.org/download.cgi).

- [Visual Studio Code](https://code.visualstudio.com/download).

- [Git](https://git-scm.com/downloads) to clone the sample repository.

- The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Set up the environment

1. Use Git to clone the sample repository.

   ```bash
   git clone https://github.com/Azure-Samples/azure-search-java-samples
   ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

   ```bash
   cd azure-search-java-samples/quickstart-vector-search
   code .
   ```

1. In `src/main/resources/application.properties`, replace the placeholder value for `azure.search.endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Install the dependencies.

   ```bash
   mvn clean dependency:copy-dependencies
   ```

   When the build completes, you should see a `target/dependency` folder in the project directory.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

## Run the code

1. Create a vector index.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.example.search.CreateIndex"
    ```

1. Load documents that contain precomputed embeddings.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.example.search.UploadDocuments"
    ```

1. Run a vector search query.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.example.search.SearchSingle"
    ```

1. (Optional) Run additional query variations.

    ```bash
    mvn compile exec:java "-Dexec.mainClass=com.example.search.SearchSingleWithFilter"
    mvn compile exec:java "-Dexec.mainClass=com.example.search.SearchSingleWithFilterGeo"
    mvn compile exec:java "-Dexec.mainClass=com.example.search.SearchHybrid"
    mvn compile exec:java "-Dexec.mainClass=com.example.search.SearchSemanticHybrid"
    ```

### Output

The output of `CreateIndex.java` shows the index name and confirmation.

```output
Using Azure Search endpoint: https://<search-service-name>.search.windows.net
Using Azure Search index: hotels-vector-quickstart
Creating index...
hotels-vector-quickstart created
```

The output of `UploadDocuments.java` shows the success status for each indexed document.

```output
Uploading documents...
Key: 1, Succeeded: true, ErrorMessage: none
Key: 2, Succeeded: true, ErrorMessage: none
Key: 3, Succeeded: true, ErrorMessage: none
Key: 4, Succeeded: true, ErrorMessage: none
Key: 48, Succeeded: true, ErrorMessage: none
Key: 49, Succeeded: true, ErrorMessage: none
Key: 13, Succeeded: true, ErrorMessage: none
Waiting for indexing... Current count: 0
All documents indexed successfully.
```

The output of `SearchSingle.java` shows vector search results ranked by similarity score.

```output
Single Vector search found 5
- HotelId: 48, HotelName: Nordick's Valley Motel, Tags: ["continental breakfast","air conditioning","free wifi"], Score 0.6605852
- HotelId: 13, HotelName: Luxury Lion Resort, Tags: ["bar","concierge","restaurant"], Score 0.6333684
- HotelId: 4, HotelName: Sublime Palace Hotel, Tags: ["concierge","view","air conditioning"], Score 0.605672
- HotelId: 49, HotelName: Swirling Currents Hotel, Tags: ["air conditioning","laundry service","24-hour front desk service"], Score 0.6026341
- HotelId: 2, HotelName: Old Century Hotel, Tags: ["pool","free wifi","air conditioning","concierge"], Score 0.57902366
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

The following code in `CreateIndex.java` creates the index schema, including the vector field `DescriptionVector`.

```java
// Define fields
List<SearchField> fields = Arrays.asList(
    new SearchField("HotelId", SearchFieldDataType.STRING)
        .setKey(true)
        .setFilterable(true),
    new SearchField("HotelName", SearchFieldDataType.STRING)
        .setSortable(true)
        .setSearchable(true),
    new SearchField("Description", SearchFieldDataType.STRING)
        .setSearchable(true),
    new SearchField("DescriptionVector",
        SearchFieldDataType.collection(SearchFieldDataType.SINGLE))
        .setSearchable(true)
        .setVectorSearchDimensions(1536)
        .setVectorSearchProfileName("my-vector-profile"),
    new SearchField("Category", SearchFieldDataType.STRING)
        .setSortable(true)
        .setFilterable(true)
        .setFacetable(true)
        .setSearchable(true),
    new SearchField("Tags", SearchFieldDataType.collection(
        SearchFieldDataType.STRING))
        .setSearchable(true)
        .setFilterable(true)
        .setFacetable(true),
    // Additional fields: ParkingIncluded, LastRenovationDate, Rating, Address, Location
);

var searchIndex = new SearchIndex(indexName, fields);

// Define vector search configuration
var hnswParams = new HnswParameters()
    .setM(16)
    .setEfConstruction(200)
    .setEfSearch(128);
var hnsw = new HnswAlgorithmConfiguration("hnsw-vector-config");
hnsw.setParameters(hnswParams);

var vectorProfile = new VectorSearchProfile(
    "my-vector-profile",
    "hnsw-vector-config");
var vectorSearch = new VectorSearch()
    .setAlgorithms(Arrays.asList(hnsw))
    .setProfiles(Arrays.asList(vectorProfile));
searchIndex.setVectorSearch(vectorSearch);

// Define semantic configuration
var prioritizedFields = new SemanticPrioritizedFields()
    .setTitleField(new SemanticField("HotelName"))
    .setContentFields(Arrays.asList(new SemanticField("Description")))
    .setKeywordsFields(Arrays.asList(new SemanticField("Category")));
var semanticConfig = new SemanticConfiguration(
    "semantic-config",
    prioritizedFields);
var semanticSearch = new SemanticSearch()
    .setConfigurations(Arrays.asList(semanticConfig));
searchIndex.setSemanticSearch(semanticSearch);

// Define suggesters
var suggester = new SearchSuggester("sg", Arrays.asList("HotelName"));
searchIndex.setSuggesters(Arrays.asList(suggester));

// Create the search index
SearchIndex result = searchIndexClient.createOrUpdateIndex(searchIndex);
```

Key takeaways:

+ You define an index by creating a list of fields.

+ This particular index supports multiple search capabilities:

    + [Full-text search](../../search-lucene-query-architecture.md) (`setSearchable`)

    + [Vector search](../../vector-search-overview.md) (`DescriptionVector` with `setVectorSearchProfileName`)

    + [Semantic ranking](../../semantic-search-overview.md) (`SemanticConfiguration`)

    + [Faceted search](../../search-faceted-navigation.md) (`SearchSuggester`)

    + [Geo-spatial search](../../search-query-odata-geo-spatial-functions.md) (`Location` field with `SearchFieldDataType.GEOGRAPHY_POINT`)

    + [Filtering](../../search-filters.md) and sorting (fields marked with `setFilterable` and `setSortable`)

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The following code in `UploadDocuments.java` uploads JSON-formatted documents to your search service.

```java
// Documents contain hotel data with 1536-dimension vectors for DescriptionVector
static final List<Map<String, Object>> DOCUMENTS = Arrays.asList(
    new HashMap<>() {{
        put("@search.action", "mergeOrUpload");
        put("HotelId", "1");
        put("HotelName", "Stay-Kay City Hotel");
        put("Description", "This classic hotel is fully-refurbished...");
        put("DescriptionVector", Arrays.asList(/* 1536 float values */));
        put("Category", "Boutique");
        put("Tags", Arrays.asList("view", "air conditioning", "concierge"));
        // Additional fields...
    }}
    // Additional hotel documents
);

// Upload documents to the index
IndexDocumentsResult result = searchClient.uploadDocuments(DOCUMENTS);
for (IndexingResult r : result.getResults()) {
    System.out.println("Key: %s, Succeeded: %s".formatted(r.getKey(), r.isSucceeded()));
}
```

Your code interacts with a specific search index hosted in your Azure AI Search service through the `SearchClient`, which is the main object provided by the [`azure-search-documents`](/java/api/overview/azure/search-documents-readme) package. The `SearchClient` provides access to operations such as:

+ Data ingestion: `uploadDocuments`, `mergeDocuments`, `deleteDocuments`

+ Search operations: `search`, `autocomplete`, `suggest`

+ Index management operations: `createOrUpdateIndex`, `deleteIndex`, `getIndex`

### Query the index

The queries in the search files demonstrate different search patterns. The example vector queries are based on two strings:

+ Full-text search string: "historic hotel walk to restaurants and shopping"

+ Vector query string: "quintessential lodging near running trails, eateries, retail" (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for "quintessential lodging near running trails, eateries, retail", results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

`SearchSingle.java` demonstrates a basic scenario where you want to find document descriptions that closely match the search string.

```java
var vectorQuery = new VectorizedQuery(QueryVector.getVectorList())
    .setKNearestNeighborsCount(5)
    .setFields("DescriptionVector")
    .setExhaustive(true);

var vectorSearchOptions = new VectorSearchOptions()
    .setQueries(vectorQuery)
    .setFilterMode(VectorFilterMode.POST_FILTER);

var searchOptions = new SearchOptions()
    .setTop(7)
    .setIncludeTotalCount(true)
    .setSelect("HotelId", "HotelName", "Description", "Category", "Tags")
    .setVectorSearchOptions(vectorSearchOptions);

var results = searchClient.search("*", searchOptions, Context.NONE);

for (SearchResult result : results) {
    SearchDocument document = result.getDocument(SearchDocument.class);
    System.out.println("HotelId: %s, HotelName: %s, Score: %s".formatted(
        document.get("HotelId"), document.get("HotelName"), result.getScore()));
}
```

#### Single vector search with a filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. `SearchSingleWithFilter.java` filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```java
var vectorQuery = new VectorizedQuery(QueryVector.getVectorList())
    .setKNearestNeighborsCount(5)
    .setFields("DescriptionVector")
    .setExhaustive(true);

var vectorSearchOptions = new VectorSearchOptions()
    .setQueries(vectorQuery)
    .setFilterMode(VectorFilterMode.POST_FILTER);

// Add filter for "free wifi" tag
var searchOptions = new SearchOptions()
    .setTop(7)
    .setIncludeTotalCount(true)
    .setSelect("HotelId", "HotelName", "Description", "Category", "Tags")
    .setFilter("Tags/any(tag: tag eq 'free wifi')")
    .setVectorSearchOptions(vectorSearchOptions);

var results = searchClient.search("*", searchOptions, Context.NONE);
```

#### Single vector search with a geo filter

You can specify a [geo-spatial filter](../../search-query-odata-geo-spatial-functions.md) to limit results to a specific geographic area. `SearchSingleWithFilterGeo.java` limits results to hotels within 300 kilometers of Washington D.C.

```java
var searchOptions = new SearchOptions()
    .setTop(5)
    .setIncludeTotalCount(true)
    .setSelect("HotelId", "HotelName", "Category", "Description",
               "Address/City", "Address/StateProvince")
    .setFacets("Address/StateProvince")
    .setFilter("geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300")
    .setVectorSearchOptions(vectorSearchOptions);
```

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. `SearchHybrid.java` runs the full-text and vector query strings concurrently.

```java
var vectorQuery = new VectorizedQuery(QueryVector.getVectorList())
    .setKNearestNeighborsCount(5)
    .setFields("DescriptionVector")
    .setExhaustive(true);

var vectorSearchOptions = new VectorSearchOptions()
    .setQueries(vectorQuery)
    .setFilterMode(VectorFilterMode.POST_FILTER);

var searchOptions = new SearchOptions()
    .setTop(5)
    .setIncludeTotalCount(true)
    .setSelect("HotelId", "HotelName", "Description", "Category", "Tags")
    .setVectorSearchOptions(vectorSearchOptions);

// Pass both text query and vector search options
var results = searchClient.search(
    "historic hotel walk to restaurants and shopping",
    searchOptions, Context.NONE);
```

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

`SearchSemanticHybrid.java` demonstrates [semantic ranking](../../semantic-search-overview.md), which reranks results based on language understanding.

```java
var vectorQuery = new VectorizedQuery(QueryVector.getVectorList())
    .setKNearestNeighborsCount(5)
    .setFields("DescriptionVector")
    .setExhaustive(true);

var vectorSearchOptions = new VectorSearchOptions()
    .setQueries(vectorQuery)
    .setFilterMode(VectorFilterMode.POST_FILTER);

SemanticSearchOptions semanticSearchOptions = new SemanticSearchOptions()
    .setSemanticConfigurationName("semantic-config");

var searchOptions = new SearchOptions()
    .setTop(5)
    .setIncludeTotalCount(true)
    .setSelect("HotelId", "HotelName", "Category", "Description")
    .setQueryType(QueryType.SEMANTIC)
    .setSemanticSearchOptions(semanticSearchOptions)
    .setVectorSearchOptions(vectorSearchOptions);

var results = searchClient.search(
    "historic hotel walk to restaurants and shopping",
    searchOptions, Context.NONE);
```

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. This quickstart modifies results for readability. To get the full structure of the response, run the request using REST.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]

Otherwise, run the following command to delete the index you created in this quickstart.

```bash
mvn compile exec:java "-Dexec.mainClass=com.example.search.DeleteIndex"
```
