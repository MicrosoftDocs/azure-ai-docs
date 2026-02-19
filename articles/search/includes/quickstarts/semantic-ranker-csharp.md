---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 11/20/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, you use an IDE and the [**Azure.Search.Documents**](/dotnet/api/overview/azure/search.documents-readme) client library to add semantic ranking to an existing search index.

We recommend [Visual Studio](https://visualstudio.microsoft.com/vs/community/) for this quickstart.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking) to start with a finished project or follow these steps to create your own.

### Install libraries

1. Start Visual Studio and open the [quickstart-semantic-ranking.sln](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking) or create a new project using a console application template.

1. In **Tools** > **NuGet Package Manager**, select **Manage NuGet Packages for Solution...**.

1. Select **Browse**.

1. Search for the [Azure.Search.Documents package](https://www.nuget.org/packages/Azure.Search.Documents/) and select the latest stable version.

1. Search for the [Azure.Identity package](https://www.nuget.org/packages/Azure.Identity) and select the latest stable version.

1. Select **Install** to add the assembly to your project and solution.

### Sign in to Azure

If you signed in to the [Azure portal](https://portal.azure.com), you're signed into Azure. If you aren't sure, use the Azure CLI or Azure PowerShell to log in: `az login` or `az connect`. If you have multiple tenants and subscriptions, see [Quickstart: Connect without keys](../../search-get-started-rbac.md) for help on how to connect.

## Update the index

In this section, you update a search index to include a semantic configuration. The code gets the index definition from the search service and adds a semantic configuration.

1. Open the [BuildIndex project](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking/BuildIndex) in Visual Studio. The program consists of the following code.

   This code uses a SearchIndexClient to update an index on your search service.

    ```csharp
    class BuildIndex
    {
        static async Task Main(string[] args)
        {
            string searchServiceName = "PUT-YOUR-SEARCH-SERVICE-NAME-HERE";
            string indexName = "hotels-sample-index";
            string endpoint = $"https://{searchServiceName}.search.windows.net";
            var credential = new Azure.Identity.DefaultAzureCredential();
    
            await ListIndexesAsync(endpoint, credential);
            await UpdateIndexAsync(endpoint, credential, indexName);
        }
    
        // Print a list of all indexes on the search service
        // You should see hotels-sample-index in the list
        static async Task ListIndexesAsync(string endpoint, Azure.Core.TokenCredential credential)
        {
            try
            {
                var indexClient = new Azure.Search.Documents.Indexes.SearchIndexClient(
                    new Uri(endpoint),
                    credential
                );
    
                var indexes = indexClient.GetIndexesAsync();
    
                Console.WriteLine("Here's a list of all indexes on the search service. You should see hotels-sample-index:");
                await foreach (var index in indexes)
                {
                    Console.WriteLine(index.Name);
                }
                Console.WriteLine(); // Add an empty line for readability
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error listing indexes: {ex.Message}");
            }
        }
    
        static async Task UpdateIndexAsync(string endpoint, Azure.Core.TokenCredential credential, string indexName)
        {
            try
            {
                var indexClient = new Azure.Search.Documents.Indexes.SearchIndexClient(
                    new Uri(endpoint),
                    credential
                );
    
                // Get the existing definition of hotels-sample-index
                var indexResponse = await indexClient.GetIndexAsync(indexName);
                var index = indexResponse.Value;
    
                // Add a semantic configuration
                const string semanticConfigName = "semantic-config";
                AddSemanticConfiguration(index, semanticConfigName);
    
                // Update the index with the new information
                var updatedIndex = await indexClient.CreateOrUpdateIndexAsync(index);
                Console.WriteLine("Index updated successfully.");
    
                // Print the updated index definition as JSON
                var refreshedIndexResponse = await indexClient.GetIndexAsync(indexName);
                var refreshedIndex = refreshedIndexResponse.Value;
                var jsonOptions = new JsonSerializerOptions { WriteIndented = true };
                string indexJson = JsonSerializer.Serialize(refreshedIndex, jsonOptions);
                Console.WriteLine($"Here is the revised index definition:\n{indexJson}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error updating index: {ex.Message}");
            }
        }
    
        // This is the semantic configuration definition
        static void AddSemanticConfiguration(SearchIndex index, string semanticConfigName)
        {
            if (index.SemanticSearch == null)
            {
                index.SemanticSearch = new SemanticSearch();
            }
            var configs = index.SemanticSearch.Configurations;
            if (configs == null)
            {
                throw new InvalidOperationException("SemanticSearch.Configurations is null and cannot be assigned. Your service must be Basic tier or higher.");
            }
            if (!configs.Any(c => c.Name == semanticConfigName))
            {
                var prioritizedFields = new SemanticPrioritizedFields
                {
                    TitleField = new SemanticField("HotelName"),
                    ContentFields = { new SemanticField("Description") },
                    KeywordsFields = { new SemanticField("Tags") }
                };
    
                configs.Add(
                    new SemanticConfiguration(
                        semanticConfigName,
                        prioritizedFields
                    )
                );
                Console.WriteLine($"Added new semantic configuration '{semanticConfigName}' to the index definition.");
            }
            else
            {
                Console.WriteLine($"Semantic configuration '{semanticConfigName}' already exists in the index definition.");
            }
            index.SemanticSearch.DefaultConfigurationName = semanticConfigName;
        }
    }
    ```

1. Replace the search service URL with a valid endpoint.

1. Run the program.

1. Output is logged to a console window from [Console.WriteLine](/dotnet/api/system.console.writeline). You should see messages for each step, including the JSON of the index schema with the new semantic configuration included.

## Run semantic queries

In this section, the program runs several semantic queries in sequence.

1. Open the [QueryIndex project](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking/QueryIndex) in Visual Studio. The program consists of the following code.

   This code uses a SearchClient for sending queries to an index.

    ```csharp
    class SemanticQuery
    {
        static async Task Main(string[] args)
        {
            string searchServiceName = "PUT-YOUR-SEARCH-SERVICE-NAME-HERE";
            string indexName = "hotels-sample-index";
            string endpoint = $"https://{searchServiceName}.search.windows.net";
            var credential = new Azure.Identity.DefaultAzureCredential();
    
            var client = new SearchClient(new Uri(endpoint), indexName, credential);
    
            // Query 1: Simple query
            string searchText = "walking distance to live music";
            Console.WriteLine("\nQuery 1: Simple query using the search string 'walking distance to live music'.");
            await RunQuery(client, searchText, new SearchOptions
            {
                Size = 5,
                QueryType = SearchQueryType.Simple,
                IncludeTotalCount = true,
                Select = { "HotelId", "HotelName", "Description" }
            });
            Console.WriteLine("Press Enter to continue to the next query...");
            Console.ReadLine();
    
            // Query 2: Semantic query (no captions, no answers)
            Console.WriteLine("\nQuery 2: Semantic query (no captions, no answers) for 'walking distance to live music'.");
            var semanticOptions = new SearchOptions
            {
                Size = 5,
                QueryType = SearchQueryType.Semantic,
                SemanticSearch = new SemanticSearchOptions
                {
                    SemanticConfigurationName = "semantic-config"
                },
                IncludeTotalCount = true,
                Select = { "HotelId", "HotelName", "Description" }
            };
            await RunQuery(client, searchText, semanticOptions);
            Console.WriteLine("Press Enter to continue to the next query...");
            Console.ReadLine();
    
            // Query 3: Semantic query with captions
            Console.WriteLine("\nQuery 3: Semantic query with captions.");
            var captionsOptions = new SearchOptions
            {
                Size = 5,
                QueryType = SearchQueryType.Semantic,
                SemanticSearch = new SemanticSearchOptions
                {
                    SemanticConfigurationName = "semantic-config",
                    QueryCaption = new QueryCaption(QueryCaptionType.Extractive)
                    {
                        HighlightEnabled = true
                    }
                },
                IncludeTotalCount = true,
                Select = { "HotelId", "HotelName", "Description" }
            };
            // Add the field(s) you want captions for to the QueryCaption.Fields collection
            captionsOptions.HighlightFields.Add("Description");
            await RunQuery(client, searchText, captionsOptions, showCaptions: true);
            Console.WriteLine("Press Enter to continue to the next query...");
            Console.ReadLine();
    
            // Query 4: Semantic query with answers
            // This query uses different search text designed for an answers scenario
            string searchText2 = "what's a good hotel for people who like to read";
            searchText = searchText2; // Update searchText for the next query
            Console.WriteLine("\nQuery 4: Semantic query with a verbatim answer from the Description field for 'what's a good hotel for people who like to read'.");
            var answersOptions = new SearchOptions
            {
                Size = 5,
                QueryType = SearchQueryType.Semantic,
                SemanticSearch = new SemanticSearchOptions
                {
                    SemanticConfigurationName = "semantic-config",
                    QueryAnswer = new QueryAnswer(QueryAnswerType.Extractive)
                },
                IncludeTotalCount = true,
                Select = { "HotelId", "HotelName", "Description" }
            };
            await RunQuery(client, searchText2, answersOptions, showAnswers: true);
    
            static async Task RunQuery(
            SearchClient client,
            string searchText,
            SearchOptions options,
            bool showCaptions = false,
            bool showAnswers = false)
            {
                try
                {
                    var response = await client.SearchAsync<SearchDocument>(searchText, options);
    
                    if (showAnswers && response.Value.SemanticSearch?.Answers != null)
                    {
                        Console.WriteLine("Extractive Answers:");
                        foreach (var answer in response.Value.SemanticSearch.Answers)
                        {
                            Console.WriteLine($"  {answer.Highlights}");
                        }
                        Console.WriteLine(new string('-', 40));
                    }
    
                    await foreach (var result in response.Value.GetResultsAsync())
                    {
                        var doc = result.Document;
                        // Print captions first if available
                        if (showCaptions && result.SemanticSearch?.Captions != null)
                        {
                            foreach (var caption in result.SemanticSearch.Captions)
                            {
                                Console.WriteLine($"Caption: {caption.Highlights}");
                            }
                        }
                        Console.WriteLine($"HotelId: {doc.GetString("HotelId")}");
                        Console.WriteLine($"HotelName: {doc.GetString("HotelName")}");
                        Console.WriteLine($"Description: {doc.GetString("Description")}");
                        Console.WriteLine($"@search.score: {result.Score}");
    
                        // Print @search.rerankerScore if available
                        if (result.SemanticSearch != null && result.SemanticSearch.RerankerScore.HasValue)
                        {
                            Console.WriteLine($"@search.rerankerScore: {result.SemanticSearch.RerankerScore.Value}");
                        }
                        Console.WriteLine(new string('-', 40));
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error querying index: {ex.Message}");
                }
            }
        }
    }
    ```

1. Replace the search service URL with a valid endpoint.

1. Run the program.

1. Output is logged to a console window from [Console.WriteLine](/dotnet/api/system.console.writeline). You should see search results for each query.

### Output for semantic query (no captions or answers)

This output is from the semantic query, with no captions or answers. The query string is 'walking distance to live music'.

Here, the initial results from the term query are rescored using the semantic ranking models. For this particular dataset and query, the first several results are in similar positions. The effects of semantic ranking are more pronounced in the remainder of the results.

```bash
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
@search.score: 5.074317
@search.rerankerScore: 2.613231658935547
----------------------------------------
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
@search.score: 5.5153193
@search.rerankerScore: 2.271434783935547
----------------------------------------
HotelId: 4
HotelName: Sublime Palace Hotel
Description: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
@search.score: 4.8959594
@search.rerankerScore: 1.9861756563186646
----------------------------------------
HotelId: 39
HotelName: White Mountain Lodge & Suites
Description: Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings.
@search.score: 0.7334347
@search.rerankerScore: 1.9615401029586792
----------------------------------------
HotelId: 15
HotelName: By the Market Hotel
Description: Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service.
@search.score: 1.5502293
@search.rerankerScore: 1.9085469245910645
----------------------------------------
Press Enter to continue to the next query...
```

### Output for a semantic query with captions

Here are the results for the query that adds captions with hit highlighting.

```
Caption: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
@search.score: 5.074317
@search.rerankerScore: 2.613231658935547
----------------------------------------
Caption:
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
@search.score: 5.5153193
@search.rerankerScore: 2.271434783935547
----------------------------------------
Caption: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within<em> short walking distance </em>to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort,.
HotelId: 4
HotelName: Sublime Palace Hotel
Description: Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.
@search.score: 4.8959594
@search.rerankerScore: 1.9861756563186646
----------------------------------------
Caption: Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend<em> evening entertainment </em>on the patio features special<em> guest musicians </em>or.
HotelId: 39
HotelName: White Mountain Lodge & Suites
Description: Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings.
@search.score: 0.7334347
@search.rerankerScore: 1.9615401029586792
----------------------------------------
Caption: Book now and Save up to 30%. Central location. <em>Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood.</em> Brand new rooms. Impeccable service.
HotelId: 15
HotelName: By the Market Hotel
Description: Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service.
@search.score: 1.5502293
@search.rerankerScore: 1.9085469245910645
----------------------------------------
Press Enter to continue to the next query...
```

### Output for semantic answers

The final query returns a semantic answer. Notice that we changed the query string for this example: 'what's a good hotel for people who like to read'.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

```bash
Extractive Answers:
  Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
----------------------------------------
HotelId: 1
HotelName: Stay-Kay City Hotel
Description: This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.
@search.score: 2.0361428
@search.rerankerScore: 2.124817371368408
----------------------------------------
HotelId: 16
HotelName: Double Sanctuary Resort
Description: 5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.
@search.score: 3.759768
@search.rerankerScore: 2.0705394744873047
----------------------------------------
HotelId: 38
HotelName: Lakeside B & B
Description: Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
@search.score: 0.7308748
@search.rerankerScore: 2.041472911834717
----------------------------------------
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
@search.score: 3.391012
@search.rerankerScore: 2.0231292247772217
----------------------------------------
HotelId: 15
HotelName: By the Market Hotel
Description: Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service.
@search.score: 1.3198771
@search.rerankerScore: 2.021622657775879
----------------------------------------
```
