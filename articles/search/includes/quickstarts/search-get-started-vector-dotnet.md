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

In this quickstart, you use the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search) to create, load, and query a [vector index](../../vector-store.md). The .NET client library provides an abstraction over the REST APIs for index operations.

In Azure AI Search, a vector index has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) creates the vector index.

> [!TIP]
> + Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-vector-search) on GitHub.
> + This quickstart omits the vectorization step and provides inline embeddings. For [integrated vectorization](../../vector-search-integrated-vectorization.md) over your own content, try the [**Import data (new)** wizard](../../search-get-started-portal-import-vectors.md).

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for most of this quickstart, but we recommend Basic or higher for larger data files.

- [Semantic ranker enabled on your search service](../../semantic-how-to-enable-disable.md) for the optional semantic hybrid query.

- [.NET 8](https://dotnet.microsoft.com/download) or later.

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
   cd azure-search-dotnet-samples/quickstart-vector-search
   code .
   ```

1. In `VectorSearchCreatePopulateIndex/appsettings.json`, replace the placeholder value for `Endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Repeat the previous step for `VectorSearchExamples/appsettings.json`.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

   ```azurecli
   az login
   ```

## Run the code

1. Run the first project to create and populate the index.

    ```bash
    cd VectorSearchCreatePopulateIndex
    dotnet run
    ```

1. In `VectorSearchExamples/Program.cs`, uncomment the query methods you want to run.

1. Run the second project to execute those queries against the index.

    ```bash
    cd VectorSearchExamples
    dotnet run
    ```

### Output

The first project creates a vector index and uploads documents. The output includes confirmation of successful document uploads.

```output
Key: 1, Succeeded: True
Key: 2, Succeeded: True
Key: 3, Succeeded: True
Key: 4, Succeeded: True
Key: 48, Succeeded: True
Key: 49, Succeeded: True
Key: 13, Succeeded: True
```

The second project runs queries. Uncomment different methods in `Program.cs` to run different query types. The following example shows single vector search results.

```output
Single Vector Search Results:
Score: 0.6605852, HotelId: 48, HotelName: Nordick's Valley Motel
Score: 0.6333684, HotelId: 13, HotelName: Luxury Lion Resort
Score: 0.605672, HotelId: 4, HotelName: Sublime Palace Hotel
Score: 0.6026341, HotelId: 49, HotelName: Swirling Currents Hotel
Score: 0.57902366, HotelId: 2, HotelName: Old Century Hotel
```

## Understand the code

Now that you've run the code, let's break down the key steps:

1. [Create a vector index](#create-a-vector-index)
1. [Upload documents to the index](#upload-documents-to-the-index)
1. [Query the index](#query-the-index)

### Create a vector index

The following code in `VectorSearchCreatePopulateIndex/Program.cs` creates the index schema, including the vector field `DescriptionVector`.

```csharp
static async Task CreateSearchIndex(string indexName, SearchIndexClient indexClient)
{
    var addressField = new ComplexField("Address");
    addressField.Fields.Add(new SearchableField("StreetAddress") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft });
    addressField.Fields.Add(new SearchableField("City") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true });
    addressField.Fields.Add(new SearchableField("StateProvince") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true });
    addressField.Fields.Add(new SearchableField("PostalCode") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true });
    addressField.Fields.Add(new SearchableField("Country") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true });

    var allFields = new List<SearchField>()
    {
        new SimpleField("HotelId", SearchFieldDataType.String) { IsKey = true, IsFacetable = true, IsFilterable = true },
        new SearchableField("HotelName") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft },
        new SearchableField("Description") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft },
        new VectorSearchField("DescriptionVector", 1536, "my-vector-profile"),
        new SearchableField("Category") { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true },
        new SearchableField("Tags", collection: true) { AnalyzerName = LexicalAnalyzerName.EnMicrosoft, IsFacetable = true, IsFilterable = true },
        new SimpleField("ParkingIncluded", SearchFieldDataType.Boolean) { IsFacetable = true, IsFilterable = true },
        new SimpleField("LastRenovationDate", SearchFieldDataType.DateTimeOffset) { IsSortable = true },
        new SimpleField("Rating", SearchFieldDataType.Double) { IsFacetable = true, IsFilterable = true, IsSortable = true },
        addressField,
        new SimpleField("Location", SearchFieldDataType.GeographyPoint) { IsFilterable = true, IsSortable = true },
    };

    // Create the suggester configuration
    var suggester = new SearchSuggester("sg", new[] { "Address/City", "Address/Country" });

    // Create the semantic search
    var semanticSearch = new SemanticSearch()
    {
        Configurations =
        {
            new SemanticConfiguration(
                name: "semantic-config",
                prioritizedFields: new SemanticPrioritizedFields
                {
                    TitleField = new SemanticField("HotelName"),
                    KeywordsFields = { new SemanticField("Category") },
                    ContentFields = { new SemanticField("Description") }
                })
        }
    };

    // Add vector search configuration
    var vectorSearch = new VectorSearch();
    vectorSearch.Algorithms.Add(new HnswAlgorithmConfiguration(name: "my-hnsw-vector-config-1"));
    vectorSearch.Profiles.Add(new VectorSearchProfile(name: "my-vector-profile", algorithmConfigurationName: "my-hnsw-vector-config-1"));

    var definition = new SearchIndex(indexName)
    {
        Fields = allFields,
        Suggesters = { suggester },
        VectorSearch = vectorSearch,
        SemanticSearch = semanticSearch
    };

    // Create or update the index
    Console.WriteLine($"Creating or updating index '{indexName}'...");
    var result = await indexClient.CreateOrUpdateIndexAsync(definition);
    Console.WriteLine($"Index '{result.Value.Name}' updated.");
    Console.WriteLine();
}
```

Key takeaways:

+ You define an index by creating a list of fields.

+ This particular index supports multiple search capabilities, including full-text keyword search, vector search (enables hybrid search by collocating vector and nonvector fields), semantic search, faceted search, geo-spatial search, and filtering.

+ Vector fields contain floating point values. The dimensions attribute has a minimum of 2 and a maximum of 4096 floating point values each. This quickstart sets the dimensions attribute to 1,536 because that's the size of embeddings generated by the `text-embedding-ada-002` model.

### Upload documents to the index

The following code uploads JSON-formatted documents in the `hotel-samples.json` file to your search service.

```csharp
static async Task UploadDocs(SearchClient searchClient)
{
    var jsonPath = Path.Combine(Directory.GetCurrentDirectory(), "HotelData.json");

    // Read and parse hotel data
    var json = await File.ReadAllTextAsync(jsonPath);
    List<Hotel> hotels = new List<Hotel>();
    try
    {
        using var doc = JsonDocument.Parse(json);
        if (doc.RootElement.ValueKind != JsonValueKind.Array)
        {
            Console.WriteLine("HotelData.json root is not a JSON array.");
        }
        // Deserialize all hotel objects
        hotels = doc.RootElement.EnumerateArray()
            .Select(e => JsonSerializer.Deserialize<Hotel>(e.GetRawText()))
            .Where(h => h != null)
            .ToList();
    }
    catch (JsonException ex)
    {
        Console.WriteLine($"Failed to parse HotelData.json: {ex.Message}");
    }

    try
    {
        // Upload hotel documents to Azure Search
        var result = await searchClient.UploadDocumentsAsync(hotels);
        foreach (var r in result.Value.Results)
        {
            Console.WriteLine($"Key: {r.Key}, Succeeded: {r.Succeeded}");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine("Failed to upload documents: " + ex);
    }
}
```

Key takeaways:

+ Your code interacts with a specific search index hosted in your Azure AI Search service through the SearchClient, which is the main object provided by the Azure.Search.Documents package. The SearchClient provides access to index operations, such as:

    + Data ingestion: `UploadDocuments()`, `MergeDocuments()`, `DeleteDocuments()`

    + Search operations: `Search()`, `Autocomplete()`, `Suggest()`

    + Index management operations: `CreateOrUpdateIndex()`

### Query the index

The queries in `VectorSearchExamples` demonstrate different search patterns. The example vector queries are based on two strings:

+ Search string: `historic hotel walk to restaurants and shopping`
+ Vector query string: `quintessential lodging near running trails, eateries, retail` (vectorized into a mathematical representation)

The vector query string is semantically similar to the search string, but it includes terms that don't exist in the search index. If you do a keyword search for `quintessential lodging near running trails, eateries, retail`, results are zero. This example shows how you can get relevant results even if there are no matching terms.

#### Single vector search

The single vector search demonstrates a basic scenario where you want to find document descriptions that closely match the search string.

```csharp
public static async Task SearchSingleVector(SearchClient searchClient, ReadOnlyMemory<float> precalculatedVector)
{
    SearchResults<Hotel> response = await searchClient.SearchAsync<Hotel>(
        new SearchOptions
        {
            VectorSearch = new()
            {
                Queries = { new VectorizedQuery(precalculatedVector) { KNearestNeighborsCount = 5, Fields = { "DescriptionVector" } } }
            },
            Select = { "HotelId", "HotelName", "Description", "Category", "Tags" },
        });

    Console.WriteLine($"Single Vector Search Results:");
    await foreach (SearchResult<Hotel> result in response.GetResultsAsync())
    {
        Hotel doc = result.Document;
        Console.WriteLine($"Score: {result.Score}, HotelId: {doc.HotelId}, HotelName: {doc.HotelName}");
    }
    Console.WriteLine();
}
```

#### Single vector search with filter

In Azure AI Search, [filters](../../vector-search-filters.md) apply to nonvector fields in an index. This example filters on the `Tags` field to filter out any hotels that don't provide free Wi-Fi.

```csharp
public static async Task SearchSingleVectorWithFilter(SearchClient searchClient, ReadOnlyMemory<float> precalculatedVector)
{
    SearchResults<Hotel> responseWithFilter = await searchClient.SearchAsync<Hotel>(
        new SearchOptions
        {
            VectorSearch = new()
            {
                Queries = { new VectorizedQuery(precalculatedVector) { KNearestNeighborsCount = 5, Fields = { "DescriptionVector" } } }
            },
            Filter = "Tags/any(tag: tag eq 'free wifi')",
            Select = { "HotelId", "HotelName", "Description", "Category", "Tags" }
        });

    Console.WriteLine($"Single Vector Search With Filter Results:");
    await foreach (SearchResult<Hotel> result in responseWithFilter.GetResultsAsync())
    {
        Hotel doc = result.Document;
        Console.WriteLine($"Score: {result.Score}, HotelId: {doc.HotelId}, HotelName: {doc.HotelName}, Tags: {string.Join(String.Empty, doc.Tags)}");
    }
    Console.WriteLine();
}
```

This search returns only hotels that provide free Wi-Fi.

For a geo filter, you can specify a geospatial filter to limit results to a specific geographic area. The following example limits results to hotels within 300 kilometers of Washington D.C.

```csharp
public static async Task SingleSearchWithGeoFilter(SearchClient searchClient, ReadOnlyMemory<float> precalculatedVector)
{
    SearchResults<Hotel> responseWithGeoFilter = await searchClient.SearchAsync<Hotel>(
        new SearchOptions
        {
            VectorSearch = new()
            {
                Queries = { new VectorizedQuery(precalculatedVector) { KNearestNeighborsCount = 5, Fields = { "DescriptionVector" } } }
            },
            Filter = "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
            Select = { "HotelId", "HotelName", "Description", "Address", "Category", "Tags" },
            Facets = { "Address/StateProvince" },
        });

    Console.WriteLine($"Vector query with a geo filter:");
    await foreach (SearchResult<Hotel> result in responseWithGeoFilter.GetResultsAsync())
    {
        Hotel doc = result.Document;
        Console.WriteLine($"HotelId: {doc.HotelId}");
        Console.WriteLine($"HotelName: {doc.HotelName}");
        Console.WriteLine($"Score: {result.Score}");
        Console.WriteLine($"City/State: {doc.Address.City}/{doc.Address.StateProvince}");
        Console.WriteLine($"Description: {doc.Description}");
        Console.WriteLine();
    }
    Console.WriteLine();
}
```

#### Hybrid search

[Hybrid search](../../hybrid-search-overview.md) combines keyword and vector queries in one request. This example runs the full-text and vector query strings concurrently.

```csharp
public static async Task<SearchResults<Hotel>> SearchHybridVectorAndText(SearchClient searchClient, ReadOnlyMemory<float> precalculatedVector)
{
    SearchResults<Hotel> responseWithFilter = await searchClient.SearchAsync<Hotel>(
        "historic hotel walk to restaurants and shopping",
        new SearchOptions
        {
            VectorSearch = new()
            {
                Queries = { new VectorizedQuery(precalculatedVector) { KNearestNeighborsCount = 5, Fields = { "DescriptionVector" } } }
            },
            Select = { "HotelId", "HotelName", "Description", "Category", "Tags" },
            Size = 5,
        });

    Console.WriteLine($"Hybrid search results:");
    await foreach (SearchResult<Hotel> result in responseWithFilter.GetResultsAsync())
    {
        Hotel doc = result.Document;
        Console.WriteLine($"Score: {result.Score}");
        Console.WriteLine($"HotelId: {doc.HotelId}");
        Console.WriteLine($"HotelName: {doc.HotelName}");
        Console.WriteLine($"Description: {doc.Description}");
        Console.WriteLine($"Category: {doc.Category}");
        Console.WriteLine($"Tags: {string.Join(String.Empty, doc.Tags)}");
        Console.WriteLine();
    }
    Console.WriteLine();
    return responseWithFilter;
}
```

Because Reciprocal Rank Fusion (RRF) merges results, it helps to review the inputs. In the full-text query only, the top two results are Sublime Palace Hotel and Luxury Lion Resort, with Sublime Palace Hotel having a stronger BM25 relevance score. In the vector-only query using HNSW, Sublime Palace Hotel drops to the fourth position. Luxury Lion, which was second in the full-text search and third in the vector search, doesn't experience the same range of fluctuation, so it appears as a top match in a homogenized result set.

#### Semantic hybrid search

Add [semantic ranking](../../semantic-search-overview.md) to rerank results based on language understanding.

```csharp
public static async Task SearchHybridVectorAndSemantic(SearchClient searchClient, ReadOnlyMemory<float> precalculatedVector)
{
    SearchResults<Hotel> responseWithFilter = await searchClient.SearchAsync<Hotel>(
        "historic hotel walk to restaurants and shopping",
        new SearchOptions
        {
            IncludeTotalCount = true,
            VectorSearch = new()
            {
                Queries = { new VectorizedQuery(precalculatedVector) { KNearestNeighborsCount = 5, Fields = { "DescriptionVector" } } }
            },
            Select = { "HotelId", "HotelName", "Description", "Category", "Tags" },
            SemanticSearch = new SemanticSearchOptions
            {
                SemanticConfigurationName = "semantic-config"
            },
            QueryType = SearchQueryType.Semantic,
            Size = 5
        });

    Console.WriteLine($"Hybrid search results:");
    await foreach (SearchResult<Hotel> result in responseWithFilter.GetResultsAsync())
    {
        Hotel doc = result.Document;
        Console.WriteLine($"Score: {result.Score}");
        Console.WriteLine($"HotelId: {doc.HotelId}");
        Console.WriteLine($"HotelName: {doc.HotelName}");
        Console.WriteLine($"Description: {doc.Description}");
        Console.WriteLine($"Category: {doc.Category}");
        Console.WriteLine();
    }
    Console.WriteLine();
}
```

With semantic ranking, the Swirling Currents Hotel moves to the top spot. Without semantic ranking, Nordick's Valley Motel is number one. With semantic ranking, the machine comprehension models recognize that `historic` applies to "hotel within walking distance to dining (restaurants) and shopping."

Key takeaways:

+ In a hybrid search, you can integrate vector search with full-text search over keywords. Filters, spell check, and semantic ranking apply to textual content only, and not vectors.

+ Actual results include more detail, including semantic captions and highlights. Results were modified for readability. To get the full structure of the response, run the request using REST.

## Clean up resources

[!INCLUDE [resource-cleanup-paid](../resource-cleanup-paid.md)]
