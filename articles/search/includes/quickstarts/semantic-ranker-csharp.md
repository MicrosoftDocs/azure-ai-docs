---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: include
ms.date: 03/02/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search client library for .NET](/dotnet/api/overview/azure/search) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and run semantic queries.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for text that's informational or descriptive.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample](../../search-get-started-portal.md) index.

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

1. In `BuildIndex/Program.cs`, replace the placeholder value for `searchServiceName` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Repeat the previous step for `QueryIndex/Program.cs`.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

## Run the code

1. Run the first project to update the index with a semantic configuration.

    ```console
    dotnet run --project BuildIndex
    ```

1. Run the second project to query the index. Press **Enter** between queries to see the progression from simple query to semantic query with captions and answers.

    ```console
    dotnet run --project QueryIndex
    ```

### Output

The first project updates the hotels-sample index with a semantic configuration. Output includes confirmation of the semantic configuration.

```output
Here's a list of all indexes on the search service. You should see hotels-sample:
hotels-sample

Added new semantic configuration 'semantic-config' to the index definition.
Index updated successfully.
Here is the revised index definition:
{
  "Name": "hotels-sample",
  ...
  "SemanticSearch": {
    "DefaultConfigurationName": "semantic-config",
    "Configurations": [
      {
        "Name": "semantic-config",
        "PrioritizedFields": {
          "TitleField": {
            "FieldName": "HotelName"
          },
          "PrioritizedContentFields": [
            {
              "FieldName": "Description"
            }
          ],
          "PrioritizedKeywordsFields": [
            {
              "FieldName": "Tags"
            }
          ]
        }
      }
    ]
  }
}
```

The second project runs queries. Press Enter between queries to see the progression from simple query to semantic query with captions and answers.

```output
Query 1: Simple query using the search string 'walking distance to live music'.
HotelId: 2
HotelName: Old Century Hotel
Description: The hotel is situated in a nineteenth century plaza...
@search.score: 5.5153193
----------------------------------------
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city...
@search.score: 5.074317
----------------------------------------

Query 2: Semantic query (no captions, no answers) for 'walking distance to live music'.
HotelId: 24
HotelName: Uptown Chic Hotel
Description: Chic hotel near the city...
@search.score: 5.074317
@search.rerankerScore: 2.613231658935547
----------------------------------------

Query 3: Semantic query with captions.
Caption: Chic hotel near the city. High-rise hotel in downtown,
within walking distance to<em> theaters, </em>art galleries...
HotelId: 24
HotelName: Uptown Chic Hotel
@search.rerankerScore: 2.613231658935547
----------------------------------------

Query 4: Semantic query with a verbatim answer for 'what's a good
hotel for people who like to read'.
Extractive Answers:
  Nature is Home on the beach. Explore the shore by day, and then
come home to our shared living space to relax around a stone
fireplace, sip something warm, and explore the<em> library </em>by
night...
```

Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, consider using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Run semantic queries](#run-semantic-queries)

### Update the index with a semantic configuration

The following code in `BuildIndex/Program.cs` adds a semantic configuration to the existing index:

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
+ `TitleField` sets the field that represents the document title.
+ `ContentFields` sets the fields containing the main content.
+ `KeywordsFields` sets the fields containing keywords or tags.
+ Semantic configurations can be added to existing indexes without rebuilding.

### Run semantic queries

The following code in `QueryIndex/Program.cs` runs a semantic query with captions:

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

+ `QueryType.Semantic` enables semantic ranking.
+ `SemanticConfigurationName` specifies which semantic configuration to use.
+ `QueryCaption` enables extractive captions with highlighting.
+ The `@search.rerankerScore` indicates semantic relevance (higher is better).

#### Semantic answers

The following code demonstrates semantic answers for question-like queries:

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
+ Answers are verbatim content extracted from your index.
+ Answers require a strong alignment between the question and content.
+ For composed answers, consider [RAG patterns](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).
