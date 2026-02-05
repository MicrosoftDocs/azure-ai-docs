---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
---

In this quickstart, you use the [Azure AI Search client library for Java](/java/api/overview/azure/search-documents-readme) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results. This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) GitHub repository to populate the index.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-java-samples/tree/main/quickstart-keyword-search) on GitHub.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use a free service for this quickstart.

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

   ```console
   git clone https://github.com/Azure-Samples/azure-search-java-samples
   ```

1. Open the `azure-search-java-samples/quickstart-keyword-search` folder in Visual Studio Code.

1. Open the `App.java` file in the `src/main/java/azure/search/sample` folder.

1. Replace the placeholder value for `searchServiceEndpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Use a terminal in Visual Studio Code to install the dependencies.

   ```console
   mvn clean dependency:copy-dependencies
   ```

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

Compile and run the application.

```console
javac -d target/classes -cp "target/dependency/*" src/main/java/azure/search/sample/*.java
java -cp "target/classes;target/dependency/*" azure.search.sample.App
```

### Output

The output should be similar to the following:

```
Waiting for indexing...

Starting queries...

Query #1: Search on empty term '*' to return all documents, showing a subset of fields...

{"HotelId":"3","HotelName":"Gastronomic Landscape Hotel","Address":{"City":"Atlanta"}}
{"HotelId":"2","HotelName":"Old Century Hotel","Address":{"City":"Sarasota"}}
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Address":{"City":"San Antonio"}}
{"HotelId":"1","HotelName":"Stay-Kay City Hotel","Address":{"City":"New York"}}

Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...

{"HotelId":"3","HotelName":"Gastronomic Landscape Hotel","Rating":4.8}
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Rating":4.6}

Query #3: Limit search to specific fields (pool in Tags field)...

{"HotelId":"2","HotelName":"Old Century Hotel","Tags":["pool","free wifi","concierge"]}

Query #4: Facet on 'Category'...

{"HotelId":"3","HotelName":"Gastronomic Landscape Hotel","Category":"Suite"}
{"HotelId":"2","HotelName":"Old Century Hotel","Category":"Boutique"}
{"HotelId":"4","HotelName":"Sublime Palace Hotel","Category":"Boutique"}
{"HotelId":"1","HotelName":"Stay-Kay City Hotel","Category":"Boutique"}

Query #5: Look up a specific document...

3

Query #6: Call Autocomplete on HotelName that starts with 's'...

stay
sublime

Complete.
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search client](#create-a-search-client)
1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a search client

In `App.java`, you create two clients:

- [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient) creates the index.
- [SearchClient](/java/api/com.azure.search.documents.searchclient) loads and queries an existing index.

Both clients require the service endpoint and a credential for authentication. In this quickstart, you use [DefaultAzureCredential](/java/api/com.azure.identity.defaultazurecredential) for keyless authentication with Microsoft Entra ID.

### Create a search index

This quickstart builds a hotels index that you load with hotel data and execute queries against. In this step, you define the fields in the index. Each field definition includes a name, data type, and attributes that determine how the field is used.

This example uses synchronous methods of the [SearchIndexClient](/java/api/com.azure.search.documents.indexes.searchindexclient) class for simplicity and readability. However, for production scenarios, use the [SearchIndexAsyncClient](/java/api/com.azure.search.documents.indexes.searchindexasyncclient) class to keep your app scalable and responsive.

#### Define the structures

You create two helper classes, `Hotel.java` and `Address.java`, to define the structure of a hotel document and its address. The `Hotel` class includes fields for a hotel ID, name, description, category, tags, parking, renovation date, rating, and address. The `Address` class includes fields for street address, city, state/province, postal code, and country/region.

In the azure-search-documents client library, you can use [SearchableField](/java/api/com.azure.search.documents.indexes.searchablefield) and [SimpleField](/java/api/com.azure.search.documents.indexes.simplefield) to streamline field definitions. Both are annotations that you can apply to fields or methods to generate a [SearchField](/java/api/com.azure.search.documents.indexes.models.searchfield):

+ `SimpleField` can be any data type, is always nonsearchable (ignored for full-text search queries), and is retrievable (not hidden). Other attributes are off by default, but can be enabled. You might use a `SimpleField` for document IDs or fields used only in filters, facets, or scoring profiles. If so, apply any attributes that are necessary for the scenario, such as `isKey = true` for a document ID.
+ `SearchableField` must be a string, and is always searchable and retrievable. Other attributes are off by default, but can be enabled. Because this field type is searchable, it supports synonyms and the full complement of analyzer properties.

Whether you use the basic `SearchField` API or either one of the helper models, you must explicitly enable filter, facet, and sort attributes. For example, [isFilterable](/java/api/com.azure.search.documents.indexes.models.searchfield), [isSortable](/java/api/com.azure.search.documents.indexes.models.searchfield), and [isFacetable](/java/api/com.azure.search.documents.indexes.models.searchfield) must be explicitly attributed, as shown in the previous sample.

#### Create the search index

In `App.java`, you create a [SearchIndex](/java/api/com.azure.search.documents.indexes.models.searchindex) object, and then call the [createOrUpdateIndex](/java/api/com.azure.search.documents.indexes.searchindexclient) method to express the index in your search service. The index also includes a [SearchSuggester](/java/api/com.azure.search.documents.indexes.models.searchsuggester) to enable autocomplete on the specified fields.

```java
// Create Search Index for Hotel model
searchIndexClient.createOrUpdateIndex(
    new SearchIndex(indexName, SearchIndexClient.buildSearchFields(Hotel.class, null))
    .setSuggesters(new SearchSuggester("sg", Arrays.asList("HotelName"))));
```

### Upload documents to the index

Azure AI Search searches over content stored in the service. In this step, you load JSON documents that conform to the hotel index you created.

In Azure AI Search, search documents are data structures that are both inputs to indexing and outputs from queries. As obtained from an external data source, document inputs might be rows in a database, blobs in Azure Blob Storage, or JSON documents on disk. In this example, you take a shortcut and embed JSON documents for four hotels directly.

When uploading documents, you must use an [IndexDocumentsBatch](/java/api/com.azure.search.documents.indexes.models.indexdocumentsbatch) object. An `IndexDocumentsBatch` object contains a collection of [IndexActions](/java/api/com.azure.search.documents.models.indexaction), each of which contains a document and a property telling Azure AI Search what action to perform ([upload, merge, delete, and mergeOrUpload](/azure/search/search-what-is-data-import#indexing-actions)).

In `App.java`, you create an array of documents and index actions, and then pass the array to `IndexDocumentsBatch`. The following documents conform to the hotels-quickstart index, as defined by the hotel class.

```java
private static void uploadDocuments(SearchClient searchClient)
{
    var hotelList = new ArrayList<Hotel>();

    var hotel = new Hotel();
    hotel.hotelId = "1";
    hotel.hotelName = "Stay-Kay City Hotel";
    hotel.description = "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
    hotel.category = "Boutique";
    hotel.tags = new String[] { "view", "air conditioning", "concierge" };
    hotel.parkingIncluded = false;
    hotel.lastRenovationDate = OffsetDateTime.of(LocalDateTime.of(LocalDate.of(2022, 1, 18), LocalTime.of(0, 0)), ZoneOffset.UTC);
    hotel.rating = 3.6;
    hotel.address = new Address();
    hotel.address.streetAddress = "677 5th Ave";
    hotel.address.city = "New York";
    hotel.address.stateProvince = "NY";
    hotel.address.postalCode = "10022";
    hotel.address.country = "USA";
    hotelList.add(hotel);
    
    // REDACTED FOR BREVITY

    var batch = new IndexDocumentsBatch<Hotel>();
    batch.addMergeOrUploadActions(hotelList);
    try
    {
        searchClient.indexDocuments(batch);
    }
    catch (Exception e)
    {
        e.printStackTrace();
        // If for some reason any documents are dropped during indexing, you can compensate by delaying and
        // retrying. This simple demo just logs failure and continues
        System.err.println("Failed to index some of the documents");
    }
}
```

The `uploadDocuments` method creates an [IndexDocumentsBatch](/java/api/com.azure.search.documents.indexes.models.indexdocumentsbatch) and calls [indexDocuments](/java/api/com.azure.search.documents.searchclient) on a [SearchClient](/java/api/com.azure.search.documents.searchclient) to upload the documents. This quickstart creates `SearchClient` independently using [SearchClientBuilder](/java/api/com.azure.search.documents.searchclientbuilder), which requires configuring the endpoint and credentials separately.

```java
uploadDocuments(searchClient);
```

Because this console app runs all commands sequentially, the code adds a two-second wait time between indexing and queries.

```java
// Wait 2 seconds for indexing to complete before starting queries (for demo and console-app purposes only)
System.out.println("Waiting for indexing...\n");
try
{
    Thread.sleep(2000);
}
catch (InterruptedException e)
{
}
```

The two-second delay compensates for indexing, which is asynchronous, so that all documents can be indexed before the queries are executed. Coding in a delay is typically only necessary in demos, tests, and sample applications.

### Query the index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

This section adds two pieces of functionality: query logic and results. For queries, use the [search](/java/api/com.azure.search.documents.searchclient) method. This method takes search text (the query string) and other [options](/java/api/com.azure.search.documents.models.searchoptions).

The [SearchPagedIterable](/java/api/com.azure.search.documents.util.searchpagediterable) class represents the results.

In `App.java`, the `WriteDocuments` method prints search results to the console.

```java
// Write search results to console
private static void WriteSearchResults(SearchPagedIterable searchResults)
{
    searchResults.iterator().forEachRemaining(result ->
    {
        Hotel hotel = result.getDocument(Hotel.class);
        System.out.println(hotel);
    });

    System.out.println();
}

// Write autocomplete results to console
private static void WriteAutocompleteResults(AutocompletePagedIterable autocompleteResults)
{
    autocompleteResults.iterator().forEachRemaining(result ->
    {
        String text = result.getText();
        System.out.println(text);
    });

    System.out.println();
}
```

#### Query example 1

The `RunQueries` method executes queries and returns results. Results are Hotel objects. This sample shows the method signature and the first query. This query demonstrates the `Select` parameter that lets you compose the result using selected fields from the document.

```java
// Run queries, use WriteDocuments to print output
private static void RunQueries(SearchClient searchClient)
{
    // Query 1
    System.out.println("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");

    SearchOptions options = new SearchOptions();
    options.setIncludeTotalCount(true);
    options.setFilter("");
    options.setOrderBy("");
    options.setSelect("HotelId", "HotelName", "Address/City");

    WriteSearchResults(searchClient.search("*", options, Context.NONE));
}
```

#### Query example 2

In the second query, search on a term, add a filter that selects documents where `Rating` is greater than 4, and then sort by `Rating` in descending order. A filter is a boolean expression evaluated over [isFilterable](/java/api/com.azure.search.documents.indexes.models.searchfield) fields in an index. Filter queries either include or exclude values. As such, there's no relevance score associated with a filter query.

```java
// Query 2
System.out.println("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");

options = new SearchOptions();
options.setFilter("Rating gt 4");
options.setOrderBy("Rating desc");
options.setSelect("HotelId", "HotelName", "Rating");

WriteSearchResults(searchClient.search("hotels", options, Context.NONE));
```

#### Query example 3

The third query demonstrates `searchFields`, used to scope a full-text search operation to specific fields.

```java
// Query 3
System.out.println("Query #3: Limit search to specific fields (pool in Tags field)...\n");

options = new SearchOptions();
options.setSearchFields("Tags");

options.setSelect("HotelId", "HotelName", "Tags");

WriteSearchResults(searchClient.search("pool", options, Context.NONE));
```

#### Query example 4

The fourth query demonstrates `facets`, which can be used to structure a faceted navigation structure.

```java
// Query 4
System.out.println("Query #4: Facet on 'Category'...\n");

options = new SearchOptions();
options.setFilter("");
options.setFacets("Category");
options.setSelect("HotelId", "HotelName", "Category");

WriteSearchResults(searchClient.search("*", options, Context.NONE));
```

#### Query example 5

In the fifth query, return a specific document. A document lookup is a typical response to an `OnClick` event in a result set.

```java
// Query 5
System.out.println("Query #5: Look up a specific document...\n");

Hotel lookupResponse = searchClient.getDocument("3", Hotel.class);
System.out.println(lookupResponse.hotelId);
System.out.println();
```

#### Query example 6

The last query shows the syntax for autocomplete, simulating a partial user input of *s* that resolves to two possible matches in the `sourceFields` associated with the suggester you defined in the index.

```java
// Query 6
System.out.println("Query #6: Call Autocomplete on HotelName that starts with 's'...\n");

WriteAutocompleteResults(searchClient.autocomplete("s", "sg"));
```

#### Summary of queries

The previous queries show multiple [ways of matching terms in a query](/azure/search/search-query-overview#types-of-queries): full-text search, filters, and autocomplete.

The [SearchClient.search](/java/api/com.azure.search.documents.searchclient) method performs full-text search and filters. You can pass a search query in the `searchText` string, while you pass a filter expression in the [filter](/java/api/com.azure.search.documents.models.searchoptions) property of the [SearchOptions](/java/api/com.azure.search.documents.models.searchoptions) class. To filter without searching, just pass `"*"` for the `searchText` parameter of the [search](/java/api/com.azure.search.documents.searchclient) method. To search without filtering, leave the `filter` property unset, or don't pass in a `SearchOptions` instance at all.

