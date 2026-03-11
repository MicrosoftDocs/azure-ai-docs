---
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: include
ms.date: 03/04/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and query the index.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for informational or descriptive text.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample index](../../search-get-started-portal.md).

+ [.NET 9](https://dotnet.microsoft.com/download) or later.

+ [Visual Studio Code](https://code.visualstudio.com/download).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication-semantic.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Start with an index

[!INCLUDE [start with an index](semantic-ranker-index.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-dotnet-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-dotnet-samples/quickstart-semantic-ranking
    code .
    ```

1. In `BuildIndex/Program.cs`, replace the placeholder value for `endpoint` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Repeat the previous step for `QueryIndex/Program.cs`.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Run the first project to update the index with a semantic configuration.

    ```bash
    dotnet run --project BuildIndex
    ```

1. Run the second project to query the index. Press **Enter** between queries to see the progression from simple query to semantic query with captions and answers.

    ```bash
    dotnet run --project QueryIndex
    ```

### Output

The first project updates the hotels-sample index with a semantic configuration. The output includes confirmation of the semantic configuration.

```output
Here's a list of all indexes on the search service. You should see hotels-sample:
hotels-sample

Added new semantic configuration 'semantic-config' to the index definition.
Index updated successfully.
Here is the revised index definition:
{
  "Name": "hotels-sample",
  ... // Trimmed for brevity
  "SemanticSearch": {
    "DefaultConfigurationName": "semantic-config",
    "Configurations": [
      {
        "Name": "hotels-sample-semantic-configuration",
        ... // Trimmed for brevity
      },
      {
        "Name": "semantic-config",
        "PrioritizedFields": {
          "TitleField": {
            "FieldName": "HotelName"
          },
          "ContentFields": [
            {
              "FieldName": "Description"
            }
          ],
          "KeywordsFields": [
            {
              "FieldName": "Tags"
            }
          ]
        },
        "RankingOrder": {}
      }
    ]
  }
}
```

The second project runs four queries. The output includes the search results with relevance scores, captions, and answers.

```output
Query 1: Simple query using the search string 'walking distance to live music'.
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
@search.score: 5.004435
----------------------------------------
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
@search.score: 4.555706
----------------------------------------
... // Trimmed for brevity
Press Enter to continue to the next query...


Query 2: Semantic query (no captions, no answers) for 'walking distance to live music'.
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
@search.score: 4.555706
@search.rerankerScore: 2.613231658935547
----------------------------------------
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.
@search.score: 5.004435
@search.rerankerScore: 2.271434783935547
----------------------------------------
... // Trimmed for brevity
Press Enter to continue to the next query...


Query 3: Semantic query with captions.
Caption: Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance.
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.
@search.score: 4.555706
@search.rerankerScore: 2.613231658935547
----------------------------------------
... // Trimmed for brevity
Press Enter to continue to the next query...


Query 4: Semantic query with a verbatim answer from the Description field for 'what's a good hotel for people who like to read'.
Extractive Answers:
  Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.
----------------------------------------
... // Trimmed for brevity
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Query the index](#query-the-index)

### Configuration and authentication

Both projects share the same configuration pattern. The `Program.cs` files define the search endpoint and use `DefaultAzureCredential` for keyless authentication.

```csharp
var endpoint = new Uri("PUT-YOUR-SEARCH-SERVICE-ENDPOINT-HERE");
var credential = new DefaultAzureCredential();
var indexClient = new SearchIndexClient(endpoint, credential);
```

Key takeaways:

+ `DefaultAzureCredential` provides keyless authentication using Microsoft Entra ID. It chains multiple credential types, including the Azure CLI credential from `az login`.
+ `SearchIndexClient` manages index-level operations, such as updating the index schema.
+ `SearchClient` handles document-level operations, such as querying the index.

### Update the index with a semantic configuration

The following code in `BuildIndex/Program.cs` adds a semantic configuration to the existing index. This operation doesn't delete any search documents, and your index remains operational after the configuration is added.

```csharp
static void AddSemanticConfiguration(
    SearchIndex index,
    string semanticConfigName)
{
    if (index.SemanticSearch == null)
    {
        index.SemanticSearch = new SemanticSearch();
    }
    var configs = index.SemanticSearch.Configurations;
    if (!configs.Any(c => c.Name == semanticConfigName))
    {
        var prioritizedFields =
            new SemanticPrioritizedFields
        {
            TitleField = new SemanticField("HotelName"),
            ContentFields =
            {
                new SemanticField("Description")
            },
            KeywordsFields =
            {
                new SemanticField("Tags")
            }
        };

        configs.Add(
            new SemanticConfiguration(
                semanticConfigName,
                prioritizedFields
            )
        );
    }
    index.SemanticSearch.DefaultConfigurationName =
        semanticConfigName;
}
```

Key takeaways:

+ A semantic configuration specifies the fields used for semantic ranking.
+ Semantic configurations can be added to existing indexes without rebuilding.
+ `TitleField` sets the field that represents the document title.
+ `ContentFields` sets the fields containing the main content.
+ `KeywordsFields` sets the fields containing keywords or tags.

### Query the index

The `QueryIndex` project runs four queries in sequence, progressing from a simple keyword search to semantic ranking with captions and answers.

#### Simple query

The first query is a simple keyword search that doesn't use semantic ranking. This query serves as a baseline for comparing results with and without semantic reranking.

```csharp
await RunQuery(client, searchText, new SearchOptions
{
    Size = 5,
    QueryType = SearchQueryType.Simple,
    IncludeTotalCount = true,
    Select = { "HotelId", "HotelName", "Description" }
});
```

Key takeaways:

+ `SearchQueryType.Simple` uses the default BM25 ranking algorithm.
+ Results are ranked by keyword relevance (`@search.score`) only.

#### Semantic query (no captions, no answers)

The next query adds semantic ranking with no captions or answers. The following code shows the minimum requirement for invoking semantic ranking.

```csharp
var semanticOptions = new SearchOptions
{
    Size = 5,
    QueryType = SearchQueryType.Semantic,
    SemanticSearch = new SemanticSearchOptions
    {
        SemanticConfigurationName = "semantic-config"
    },
    IncludeTotalCount = true,
    Select =
    {
        "HotelId", "HotelName", "Description"
    }
};
await RunQuery(client, searchText, semanticOptions);
```

Key takeaways:

+ `SearchQueryType.Semantic` enables semantic ranking on the query.
+ `SemanticConfigurationName` specifies which semantic configuration to use.
+ `@search.rerankerScore` indicates semantic relevance (higher is better).
+ The initial results from the term query are rescored using semantic ranking models. For this dataset and query, the effects of semantic ranking are more pronounced in the lower-ranked results.

#### Semantic query with captions

The following code adds captions to extract the most relevant passages from each result, with hit highlighting applied to the important terms and phrases.

```csharp
var captionsOptions = new SearchOptions
{
    Size = 5,
    QueryType = SearchQueryType.Semantic,
    SemanticSearch = new SemanticSearchOptions
    {
        SemanticConfigurationName = "semantic-config",
        QueryCaption =
            new QueryCaption(QueryCaptionType.Extractive)
        {
            HighlightEnabled = true
        }
    },
    IncludeTotalCount = true,
    Select =
    {
        "HotelId", "HotelName", "Description"
    }
};
captionsOptions.HighlightFields.Add("Description");
await RunQuery(
    client, searchText, captionsOptions, showCaptions: true
);
```

Key takeaways:

+ `QueryCaption` enables extractive captions from the content fields.
+ Captions surface the most relevant passages and add `<em>` tags around important terms.

#### Semantic query with answers

The final query adds semantic answers. This query uses a different search string (`searchText2`) because semantic answers work best when the query is phrased as a question. The answer is a verbatim passage extracted from your index, not a composed response from a chat completion model.

The query and the indexed content must be closely aligned for an answer to be returned. If no candidate meets the confidence threshold, the response doesn't include an answer. This example uses a question that's known to produce a result so that you can see the syntax. If answers aren't useful for your scenario, omit `QueryAnswer` from your code. For composed answers, consider a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

```csharp
var answersOptions = new SearchOptions
{
    Size = 5,
    QueryType = SearchQueryType.Semantic,
    SemanticSearch = new SemanticSearchOptions
    {
        SemanticConfigurationName = "semantic-config",
        QueryAnswer =
            new QueryAnswer(QueryAnswerType.Extractive)
    },
    IncludeTotalCount = true,
    Select =
    {
        "HotelId", "HotelName", "Description"
    }
};
await RunQuery(
    client, searchText2, answersOptions, showAnswers: true
);
```

Key takeaways:

+ `QueryAnswer` enables extractive answers for question-like queries.
+ Answers are verbatim content extracted from your index, not generated text.
