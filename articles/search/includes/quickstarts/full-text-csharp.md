---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
---

In this quickstart, you use the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search) to create, load, and query a search index for [full-text search](../../search-lucene-query-architecture.md), also known as keyword search.

Full-text search uses Apache Lucene for indexing and queries and the BM25 ranking algorithm for scoring results. This quickstart uses fictional hotel data from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) GitHub repository to populate the index.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-keyword-search) on GitHub.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use a free service for this quickstart.

- The latest version of the [.NET SDK](https://dotnet.microsoft.com/download).

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
    git clone https://github.com/Azure-Samples/azure-search-dotnet-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-dotnet-samples/quickstart-keyword-search/AzureSearchQuickstart
    code .
    ```

1. In `Program.cs`, replace the placeholder value for `serviceEndpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Install the dependencies from `AzureSearchQuickstart.csproj`.

    ```bash
    dotnet restore
    ```

    When the restore completes, verify that no errors appear in the output.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

Build and run the application.

```bash
dotnet run
```

### Output

The output should be similar to the following:

```
Deleting index...

Creating index...

Uploading documents...

Waiting for indexing...

Starting queries...

Query #1: Search on empty term '*' to return all documents, showing a subset of fields...

HotelId: 3
Name: Gastronomic Landscape Hotel
Rating: 4.8

HotelId: 2
Name: Old Century Hotel
Rating: 3.6

HotelId: 4
Name: Sublime Palace Hotel
Rating: 4.6

HotelId: 1
Name: Stay-Kay City Hotel
Rating: 3.6


Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...

HotelId: 3
Name: Gastronomic Landscape Hotel
Rating: 4.8

HotelId: 4
Name: Sublime Palace Hotel
Rating: 4.6


Query #3: Limit search to specific fields (pool in Tags field)...

HotelId: 2
Name: Old Century Hotel
Tags: [ pool, free wifi, concierge ]


Query #4: Facet on 'Category'...

HotelId: 3
Name: Gastronomic Landscape Hotel
Category: Suite

HotelId: 2
Name: Old Century Hotel
Category: Boutique

HotelId: 4
Name: Sublime Palace Hotel
Category: Boutique

HotelId: 1
Name: Stay-Kay City Hotel
Category: Boutique


Query #5: Look up a specific document...

3
Query #6: Call Autocomplete on HotelName...

san
sarasota

Complete. Press any key to end this program...
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a search client](#create-a-search-client)
1. [Create a search index](#create-a-search-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a search client

In `Program.cs`, you create two clients:

- [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient) creates the index.
- [SearchClient](/dotnet/api/azure.search.documents.searchclient) loads and queries an existing index.

Both clients require the service endpoint and a credential for authentication. In this quickstart, you use [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential) for keyless authentication with Microsoft Entra ID.

### Create a search index

This quickstart builds a hotels index that you load with hotel data and execute queries against. In this step, you define the fields in the index. Each field definition includes a name, data type, and attributes that determine how the field is used.

This example uses synchronous methods of the [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient) class for simplicity and readability. However, for production scenarios, use asynchronous methods to keep your app scalable and responsive. For example, use [CreateIndexAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindexasync) instead of [CreateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createindex).

#### Define the structures

You create two helper classes, `Hotel.cs` and `Address.cs`, to define the structure of a hotel document and its address. The `Hotel` class includes fields for a hotel ID, name, description, category, tags, parking, renovation date, rating, and address. The `Address` class includes fields for street address, city, state/province, postal code, and country/region.

In the Azure.Search.Documents client library, you can use [SearchableField](/dotnet/api/azure.search.documents.indexes.models.searchablefield) and [SimpleField](/dotnet/api/azure.search.documents.indexes.models.simplefield) to streamline field definitions. Both are helper classes that generate a [SearchField](/dotnet/api/azure.search.documents.indexes.models.searchfield) and can potentially simplify your code:

+ `SimpleField` can be any data type, is always nonsearchable (ignored for full-text search queries), and is retrievable (not hidden). Other attributes are off by default, but can be enabled. You might use a `SimpleField` for document IDs or fields used only in filters, facets, or scoring profiles. If so, apply any attributes that are necessary for the scenario, such as `IsKey = true` for a document ID.

+ `SearchableField` must be a string, and is always searchable and retrievable. Other attributes are off by default, but can be enabled. Because this field type is searchable, it supports synonyms and the full complement of analyzer properties.

Whether you use the basic `SearchField` API or either one of the helper models, you must explicitly enable filter, facet, and sort attributes. For example, [IsFilterable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfilterable), [IsSortable](/dotnet/api/azure.search.documents.indexes.models.searchfield.issortable), and [IsFacetable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfacetable) must be explicitly attributed, as shown in the previous sample.

#### Create the search index

In `Program.cs`, you create a [SearchIndex](/dotnet/api/azure.search.documents.indexes.models.searchindex) object, and then call the [CreateOrUpdateIndex](/dotnet/api/azure.search.documents.indexes.searchindexclient.createorupdateindex) method to express the index in your search service. The index also includes a [SearchSuggester](/dotnet/api/azure.search.documents.indexes.models.searchsuggester) to enable autocomplete on the specified fields.

```csharp
// Create hotels-quickstart index
private static void CreateIndex(string indexName, SearchIndexClient searchIndexClient)
{
    FieldBuilder fieldBuilder = new FieldBuilder();
    var searchFields = fieldBuilder.Build(typeof(Hotel));

    var definition = new SearchIndex(indexName, searchFields);

    var suggester = new SearchSuggester("sg", new[] { "HotelName", "Category", "Address/City", "Address/StateProvince" });
    definition.Suggesters.Add(suggester);

    searchIndexClient.CreateOrUpdateIndex(definition);
}
```

### Upload documents to the index

Azure AI Search searches over content stored in the service. In this step, you load JSON documents that conform to the hotel index you created.

In Azure AI Search, search documents are data structures that are both inputs to indexing and outputs from queries. As obtained from an external data source, document inputs might be rows in a database, blobs in Azure Blob Storage, or JSON documents on disk. In this example, you take a shortcut and embed JSON documents for four hotels directly.

When uploading documents, you must use an [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1) object. An `IndexDocumentsBatch` object contains a collection of [Actions](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1.actions), each of which contains a document and a property telling Azure AI Search what action to perform ([upload, merge, delete, and mergeOrUpload](/azure/search/search-what-is-data-import#indexing-actions)).

In `Program.cs`, you create an array of documents and index actions, and then pass the array to `IndexDocumentsBatch`. The following documents conform to the hotels-quickstart index, as defined by the hotel class.

```csharp
// Upload documents in a single Upload request.
private static void UploadDocuments(SearchClient searchClient)
{
    IndexDocumentsBatch<Hotel> batch = IndexDocumentsBatch.Create(
        IndexDocumentsAction.Upload(
            new Hotel()
            {
                HotelId = "1",
                HotelName = "Stay-Kay City Hotel",
                Description = "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
                Category = "Boutique",
                Tags = new[] { "view", "air conditioning", "concierge" },
                ParkingIncluded = false,
                LastRenovationDate = new DateTimeOffset(2022, 1, 18, 0, 0, 0, TimeSpan.Zero),
                Rating = 3.6,
                Address = new Address()
                {
                    StreetAddress = "677 5th Ave",
                    City = "New York",
                    StateProvince = "NY",
                    PostalCode = "10022",
                    Country = "USA"
                }
            }),
        // REDACTED FOR BREVITY
}
```

The `UploadDocuments` method creates an [IndexDocumentsBatch](/dotnet/api/azure.search.documents.models.indexdocumentsbatch-1) and calls [IndexDocuments](/dotnet/api/azure.search.documents.searchclient.indexdocuments) on a [SearchClient](/dotnet/api/azure.search.documents.searchclient) to upload the documents. This quickstart obtains `SearchClient` from `SearchIndexClient` using [GetSearchClient](/dotnet/api/azure.search.documents.indexes.searchindexclient.getsearchclient), which reuses the same credentials.

```csharp
SearchClient ingesterClient = searchIndexClient.GetSearchClient(indexName);

// Load documents
Console.WriteLine("{0}", "Uploading documents...\n");
UploadDocuments(ingesterClient);
```

Because this console app runs all commands sequentially, the code adds a two-second wait time between indexing and queries.

```csharp
// Wait 2 seconds for indexing to complete before starting queries (for demo and console-app purposes only)
Console.WriteLine("Waiting for indexing...\n");
System.Threading.Thread.Sleep(2000);
```

The two-second delay compensates for indexing, which is asynchronous, so that all documents can be indexed before the queries are executed. Coding in a delay is typically only necessary in demos, tests, and sample applications.

### Query the index

You can get query results as soon as the first document is indexed, but actual testing of your index should wait until all documents are indexed.

This section adds two pieces of functionality: query logic and results. For queries, use the [Search](/dotnet/api/azure.search.documents.searchclient.search) method. This method takes search text (the query string) and other [options](/dotnet/api/azure.search.documents.searchoptions).

The [SearchResults](/dotnet/api/azure.search.documents.models.searchresults-1) class represents the results.

In `Program.cs`, the `WriteDocuments` method prints search results to the console.

```csharp
// Write search results to console
private static void WriteDocuments(SearchResults<Hotel> searchResults)
{
    foreach (SearchResult<Hotel> result in searchResults.GetResults())
    {
        Console.WriteLine(result.Document);
    }

    Console.WriteLine();
}

private static void WriteDocuments(AutocompleteResults autoResults)
{
    foreach (AutocompleteItem result in autoResults.Results)
    {
        Console.WriteLine(result.Text);
    }

    Console.WriteLine();
}
```

#### Query example 1

The `RunQueries` method executes queries and returns results. Results are Hotel objects. This sample shows the method signature and the first query. This query demonstrates the `Select` parameter that lets you compose the result using selected fields from the document.

```csharp
// Run queries, use WriteDocuments to print output
private static void RunQueries(SearchClient searchClient)
{
    SearchOptions options;
    SearchResults<Hotel> response;
    
    // Query 1
    Console.WriteLine("Query #1: Search on empty term '*' to return all documents, showing a subset of fields...\n");

    options = new SearchOptions()
    {
        IncludeTotalCount = true,
        Filter = "",
        OrderBy = { "" }
    };

    options.Select.Add("HotelId");
    options.Select.Add("HotelName");
    options.Select.Add("Rating");

    response = searchClient.Search<Hotel>("*", options);
    WriteDocuments(response);
    // REDACTED FOR BREVITY
}
```

#### Query example 2

In the second query, search on a term, add a filter that selects documents where `Rating` is greater than 4, and then sort by `Rating` in descending order. A filter is a boolean expression evaluated over [IsFilterable](/dotnet/api/azure.search.documents.indexes.models.searchfield.isfilterable) fields in an index. Filter queries either include or exclude values. As such, there's no relevance score associated with a filter query.

```csharp
// Query 2
Console.WriteLine("Query #2: Search on 'hotels', filter on 'Rating gt 4', sort by Rating in descending order...\n");

options = new SearchOptions()
{
    Filter = "Rating gt 4",
    OrderBy = { "Rating desc" }
};

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Rating");

response = searchClient.Search<Hotel>("hotels", options);
WriteDocuments(response);
```

#### Query example 3

The third query demonstrates `searchFields`, used to scope a full-text search operation to specific fields.

```csharp
// Query 3
Console.WriteLine("Query #3: Limit search to specific fields (pool in Tags field)...\n");

options = new SearchOptions()
{
    SearchFields = { "Tags" }
};

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Tags");

response = searchClient.Search<Hotel>("pool", options);
WriteDocuments(response);
```

#### Query example 4

The fourth query demonstrates `facets`, which can be used to structure a faceted navigation structure.

```csharp
// Query 4
Console.WriteLine("Query #4: Facet on 'Category'...\n");

options = new SearchOptions()
{
    Filter = ""
};

options.Facets.Add("Category");

options.Select.Add("HotelId");
options.Select.Add("HotelName");
options.Select.Add("Category");

response = searchClient.Search<Hotel>("*", options);
WriteDocuments(response);
```

#### Query example 5

In the fifth query, return a specific document. A document lookup is a typical response to an `OnClick` event in a result set.

```csharp
// Query 5
Console.WriteLine("Query #5: Look up a specific document...\n");

Response<Hotel> lookupResponse;
lookupResponse = searchClient.GetDocument<Hotel>("3");

Console.WriteLine(lookupResponse.Value.HotelId);
```

#### Query example 6

The last query shows the syntax for autocomplete, simulating a partial user input of *sa* that resolves to two possible matches in the `sourceFields` associated with the suggester you defined in the index.

```csharp
// Query 6
Console.WriteLine("Query #6: Call Autocomplete on HotelName...\n");

var autoresponse = searchClient.Autocomplete("sa", "sg");
WriteDocuments(autoresponse);
```

#### Summary of queries

The previous queries show multiple [ways of matching terms in a query](/azure/search/search-query-overview#types-of-queries): full-text search, filters, and autocomplete.

The [SearchClient.Search](/dotnet/api/azure.search.documents.searchclient.search) method performs full-text search and filters. You can pass a search query in the `searchText` string, while you pass a filter expression in the [Filter](/dotnet/api/azure.search.documents.searchoptions.filter) property of the [SearchOptions](/dotnet/api/azure.search.documents.searchoptions) class. To filter without searching, just pass `"*"` for the `searchText` parameter of the [Search](/dotnet/api/azure.search.documents.searchclient.search) method. To search without filtering, leave the `Filter` property unset, or don't pass in a `SearchOptions` instance at all.

