---
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 10/22/2024
---

Build a console application by using the [**Azure.Search.Documents**](/dotnet/api/overview/azure/search.documents-readme) client library to add semantic ranking to an existing search index.

Alternatively, you can [download the source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-search/SemanticSearchQuickstart) to start with a finished project.

#### Set up your environment

1. Start Visual Studio and create a new project for a console app.

1. In **Tools** > **NuGet Package Manager**, select **Manage NuGet Packages for Solution...**.

1. Select **Browse**.

1. Search for the [Azure.Search.Documents package](https://www.nuget.org/packages/Azure.Search.Documents/) and select the latest stable version.

1. Select **Install** to add the assembly to your project and solution.

#### Create a search client

1. In *Program.cs*, add the following `using` directives.

   ```csharp
   using Azure;
   using Azure.Search.Documents;
   using Azure.Search.Documents.Indexes;
   using Azure.Search.Documents.Indexes.Models;
   using Azure.Search.Documents.Models;
   ```

1. Create two clients: [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient) creates the index, and [SearchClient](/dotnet/api/azure.search.documents.searchclient) loads and queries an existing index.

    Both clients need the service endpoint and an admin API key for authentication with create/delete rights. However, the code builds out the URI for you, so specify only the search service name for the `serviceName` property. Don't include `https://` or `.search.windows.net`.

   ```csharp
    static void Main(string[] args)
    {
        string serviceName = "<YOUR-SEARCH-SERVICE-NAME>";
        string apiKey = "<YOUR-SEARCH-ADMIN-API-KEY>";
        string indexName = "hotels-quickstart";
        

        // Create a SearchIndexClient to send create/delete index commands
        Uri serviceEndpoint = new Uri($"https://{serviceName}.search.windows.net/");
        AzureKeyCredential credential = new AzureKeyCredential(apiKey);
        SearchIndexClient adminClient = new SearchIndexClient(serviceEndpoint, credential);

        // Create a SearchClient to load and query documents
        SearchClient srchclient = new SearchClient(serviceEndpoint, indexName, credential);
        . . . 
    }
    ```

#### Create an index

Create or update an index schema to include a `SemanticConfiguration`. If you're updating an existing index, this modification doesn't require a reindexing because the structure of your documents is unchanged.

```csharp
// Create hotels-quickstart index
private static void CreateIndex(string indexName, SearchIndexClient adminClient)
{

    FieldBuilder fieldBuilder = new FieldBuilder();
    var searchFields = fieldBuilder.Build(typeof(Hotel));

    var definition = new SearchIndex(indexName, searchFields);
    var suggester = new SearchSuggester("sg", new[] { "HotelName", "Category", "Address/City", "Address/StateProvince" });
    definition.Suggesters.Add(suggester);
    definition.SemanticSearch = new SemanticSearch
    {
        Configurations =
        {
            new SemanticConfiguration("my-semantic-config", new()
            {
                TitleField = new SemanticField("HotelName"),
                ContentFields =
                {
                    new SemanticField("Description"),
                    new SemanticField("Description_fr")
                },
                KeywordsFields =
                {
                    new SemanticField("Tags"),
                    new SemanticField("Category")
                }
            })
        }
    };

    adminClient.CreateOrUpdateIndex(definition);
}
```

The following code creates the index on your search service:

```csharp
// Create index
Console.WriteLine("{0}", "Creating index...\n");
CreateIndex(indexName, adminClient);

SearchClient ingesterClient = adminClient.GetSearchClient(indexName);
```

#### Load documents

Azure AI Search searches over content stored in the service. The code for uploading documents is identical to the [C# quickstart for full text search](/azure/search/search-get-started-text) so we don't need to duplicate it here. You should have four hotels with names, addresses, and descriptions. Your solution should have types for Hotels and Addresses.

#### Search an index

Here's a query that invokes semantic ranker, with search options for specifying parameters:

```csharp
Console.WriteLine("Example of a semantic query.");

options = new SearchOptions()
{
    QueryType = Azure.Search.Documents.Models.SearchQueryType.Semantic,
    SemanticSearch = new()
    {
        SemanticConfigurationName = "my-semantic-config",
        QueryCaption = new(QueryCaptionType.Extractive)
    }
};
options.Select.Add("HotelName");
options.Select.Add("Category");
options.Select.Add("Description");

// response = srchclient.Search<Hotel>("*", options);
response = srchclient.Search<Hotel>("what hotel has a good restaurant on site", options);
WriteDocuments(response);
```

For comparison, here are results from a query that uses the default BM25 ranking, based on term frequency and proximity. Given the query "what hotel has a good restaurant on site", the BM25 ranking algorithm returns matches in the order shown in this screenshot:

:::image type="content" source="../../media/quickstart-semantic/bm25-ranking.png" alt-text="Screenshot showing matches ranked by BM25.":::

In contrast, when semantic ranking is applied to the same query ("what hotel has a good restaurant on site"), the results are reranked based on semantic relevance to the query. This time, the top result is the hotel with the restaurant, which aligns better to user expectations.

:::image type="content" source="../../media/quickstart-semantic/semantic-ranking.png" alt-text="Screenshot showing matches ranked based on semantic ranking.":::

#### Run the program

Press F5 to rebuild the app and run the program in its entirety.

Output includes messages from [Console.WriteLine](/dotnet/api/system.console.writeline), with the addition of query information and results.
