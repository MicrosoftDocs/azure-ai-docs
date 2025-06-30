---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 06/27/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-search/SemanticSearchQuickstart) to start with a finished project or follow these steps to create your own. 

## Set up the client

In this quickstart, you use an IDE and the [**Azure.Search.Documents**](/dotnet/api/overview/azure/search.documents-readme) client library to add semantic ranking to an existing search index.

We recommend [Visual Studio](https://visualstudio.microsoft.com/vs/community/) for this quickstart.

### Install libraries

1. Start Visual Studio and create a new project for a console app.

1. In **Tools** > **NuGet Package Manager**, select **Manage NuGet Packages for Solution...**.

1. Select **Browse**.

1. Search for the [Azure.Search.Documents package](https://www.nuget.org/packages/Azure.Search.Documents/) and select the latest stable version.

1. Select **Install** to add the assembly to your project and solution.

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI or Azure PowerShell to log in: `az login` or `az connect`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

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

## Update and query the index

In this section, you update a search index and send a query that invokes semantic ranking. The code runs all operations in sequence, from index updates through a series of queries. For more information about each step, see [Explaining the code](#explaining-the-code). The code performs two types of tasks:

+ [Add a semantic configuration to an index](#add-a-semantic-configuration-to-the-hotels-sample-index)
+ [Add semantic parameters to a query](#add-semantic-parameters-to-a-query)

### Add a semantic configuration to the hotels-sample-index

```csharp
CODE GOES HERE
```

### Add semantic parameters to a query

```csharp
CODE GOES HERE
```

### Run the program

Press F5 to rebuild the app and run the program in its entirety.

Output includes messages from [Console.WriteLine](/dotnet/api/system.console.writeline), with the addition of query information and results.

## Explaining the code

This section explains the updates to the index and queries. If you're updating an existing index, the additional of a semantic configuration doesn't require a reindexing because the structure of your documents is unchanged.

### Index updates

To update the index, provide the existing schema in its entirety, plus the new `SemanticConfiguration` section. We recommend retrieving the index schema from the search service to ensure you're working with the current version. If the original and updated schemas differ in field definitions or other constructs, the update fails.

This example highlights the C# code that adds a semantic configuration to an index.

```csharp
CODE GOES HERE
```

### Query parameters

Required semantic parameters include `query_type` and `semantic_configuration_name`. Here is an example of a basic semantic query using the minimum parameters.

```csharp
Console.WriteLine("Example of a semantic query.");

options = new SearchOptions()
{
    QueryType = Azure.Search.Documents.Models.SearchQueryType.Semantic,
    SemanticSearch = new()
    {
        SemanticConfigurationName = "semantic-config"
    }
};
options.Select.Add("HotelName");
options.Select.Add("Category");
options.Select.Add("Description");

// response = srchclient.Search<Hotel>("*", options);
response = srchclient.Search<Hotel>("walking distance to live music", options);
WriteDocuments(response);
```

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions.

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
response = srchclient.Search<Hotel>("walking distance to live music", options);
WriteDocuments(response);
```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To get a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

```csharp
CODE GOES HERE
```
