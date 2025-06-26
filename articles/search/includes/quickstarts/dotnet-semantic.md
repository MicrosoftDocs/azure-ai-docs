---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 06/13/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

In this quickstart, build a console application by using the [**Azure.Search.Documents**](/dotnet/api/overview/azure/search.documents-readme) client library to add semantic ranking to an existing search index.

> [!TIP] 
> You can [download the source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-search/SemanticSearchQuickstart) to start with a finished project or follow these steps to create your own. 

## Set up the client

In this quickstart, you use an IDE and the [Azure.Search.Documents](TBD) library to configure and use a semantic ranker.

We recommend [Visual Studio](TBD) for this quickstart.

### Install libraries

1. Start Visual Studio and create a new project for a console app.

1. In **Tools** > **NuGet Package Manager**, select **Manage NuGet Packages for Solution...**.

1. Select **Browse**.

1. Search for the [Azure.Search.Documents package](https://www.nuget.org/packages/Azure.Search.Documents/) and select the latest stable version.

1. Select **Install** to add the assembly to your project and solution.

### Create a search client

1. In *Program.cs*, add the following `using` directives.

   ```csharp
   using Azure;
   using Azure.Search.Documents;
   using Azure.Search.Documents.Indexes;
   using Azure.Search.Documents.Indexes.Models;
   using Azure.Search.Documents.Models;
   ```

1. Create two clients: [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient) to update the index, and [SearchClient](/dotnet/api/azure.search.documents.searchclient) to query an index.

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

## Add semantic configuration to an index

TBD

## Search with semantic reranking

TBD

Here's a query that invokes semantic ranker, with search options for specifying parameters:

```csharp
Console.WriteLine("Example of a semantic query.");

options = new SearchOptions()
{
    QueryType = Azure.Search.Documents.Models.SearchQueryType.Semantic,
    SemanticSearch = new()
    {
        SemanticConfigurationName = "semantic-config",
        QueryCaption = new(QueryCaptionType.Extractive)
    }
};
options.Select.Add("HotelName");
options.Select.Add("Category");
options.Select.Add("Description");

// response = srchclient.Search<Hotel>("*", options);
response = srchclient.Search<Hotel>("restaurant on site", options);
WriteDocuments(response);
```

For comparison, here are results from a query that uses the default BM25 ranking, based on term frequency and proximity. Given the query "restaurant on site", the BM25 ranking algorithm returns matches in the order shown in this screenshot, where the match on the "site" is considered more relevant because it's rare across the dataset:

:::image type="content" source="../../media/quickstart-semantic/bm25-ranking.png" alt-text="Screenshot showing matches ranked by BM25.":::

In contrast, when semantic ranking is applied to the same query ("restaurant on site"), the results are reranked based on semantic relevance to the query. This time, the top result is the hotel with the restaurant, which aligns better to user expectations.

:::image type="content" source="../../media/quickstart-semantic/semantic-ranking.png" alt-text="Screenshot showing matches ranked based on semantic ranking.":::

### Run the program

Press F5 to rebuild the app and run the program in its entirety.

Output includes messages from [Console.WriteLine](/dotnet/api/system.console.writeline), with the addition of query information and results.
