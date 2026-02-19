---
title: Configure a suggester for autocomplete and suggestions
titleSuffix: Azure AI Search
description: Enable typeahead query actions in Azure AI Search by creating suggesters and formulating requests that invoke autocomplete or autosuggested query terms.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 09/11/2025
ms.update-cycle: 365-days
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
---

# Configure a suggester for autocomplete and suggestions in a query

In Azure AI Search, typeahead or "search-as-you-type" is enabled by using a *suggester*. A suggester is a configuration in an index that specifies which fields should be used to populate autocomplete and suggested matches. These fields undergo extra tokenization, generating prefix sequences to support matches on partial terms. For example, a suggester that includes a `city` field with a value for *Seattle* has prefix combinations of *sea*, *seat*, *seatt*, and *seattl* to support typeahead.

Matches on partial terms can be either an autocompleted query or a suggested match. The same suggester supports both experiences.

## Typeahead experiences

Typeahead  in Azure AI Search can be either *autocomplete*, which completes a partial input for a whole term query, or *suggestions* that invite click through to a particular match. Autocomplete produces a query. Suggestions produce a matching document.

The following screenshot illustrates both. Autocomplete anticipates a potential term, finishing *tw* with *in*. Suggestions are mini search results, where a field like `hotel name` represents a matching hotel search document from the index. For suggestions, you can surface any field that provides descriptive information.

:::image type="content" source="media/index-add-suggesters/hotel-app-suggestions-autocomplete.png" alt-text="Screenshot showing visual comparison of autocomplete and suggested queries.":::

You can use these features separately or together. To implement these behaviors in Azure AI Search, there's an index and query component. 

+ Add a suggester to a search index definition. The remainder of this article focuses on creating a suggester.

+ Call a suggester-enabled query, in the form of a suggestion request or autocomplete request, by using one of the APIs listed in [Use a suggester](#how-to-use-a-suggester).

Search-as-you-type is enabled on a per-field basis for string fields. You can implement both typeahead behaviors within the same search solution if you want an experience similar to the one indicated in the screenshot. Both requests target the *documents* collection of a specific index, and responses are returned after a user provides at least a three-character input string.

## How to create a suggester

To create a suggester, add one to an [index definition](/rest/api/searchservice/indexes/create). A suggester takes a name and a collection of fields over which the typeahead experience is enabled. The best time to create a suggester is when you're also defining the field that uses it.

+ Use string fields only.

+ If the string field is part of a complex type (for example, a City field within Address), include the parent in the field path: `"Address/City"` (REST, C#, and Python), or `["Address"]["City"]` (JavaScript).

+ Use the default standard Lucene analyzer (`"analyzer": null`) or a [language analyzer](index-add-language-analyzers.md) (for example, `"analyzer": "fr.microsoft"`) on the field.

If you try to create a suggester using preexisting fields, the API disallows it. Prefixes are generated during indexing, when partial terms in two or more character combinations are tokenized alongside whole terms. Given that existing fields are already tokenized, you have to rebuild the index if you want to add them to a suggester. For more information, see [Update or rebuild an index in Azure AI Search](search-howto-reindex.md).

### Choose fields

Although a suggester has several properties, it's primarily a collection of string fields for which you're enabling a search-as-you-type experience. There's one suggester for each index, so the suggester list must include all fields that contribute content for both suggestions and autocomplete.

Autocomplete benefits from a larger pool of fields to draw from because the extra content has more term completion potential.

Suggestions, on the other hand, produce better results when your field choice is selective. Remember that the suggestion is a proxy for a search document so pick fields that best represent a single result. Names, titles, or other unique fields that distinguish among multiple matches work best. If fields consist of repetitive values, the suggestions consist of identical results and a user won't know which one to choose.

To satisfy both search-as-you-type experiences, add all of the fields that you need for autocomplete, but then use `select`, `top`, `filter`, and `searchFields` to control results for suggestions.

### Choose analyzers

Your choice of an analyzer determines how fields are tokenized and prefixed. For example, for a hyphenated string like *context-sensitive*, using a language analyzer results in these token combinations: *context*, *sensitive*, *context-sensitive*. Had you used the standard Lucene analyzer, the hyphenated string wouldn't exist. 

When evaluating analyzers, consider using the [Analyze Text API](/rest/api/searchservice/indexes/analyze) for insight into how terms are processed. Once you build an index, you can try various analyzers on a string to view token output.

Fields that use [custom analyzers](index-add-custom-analyzers.md) or [built-in analyzers](index-add-custom-analyzers.md#built-in-analyzers), (except for standard Lucene) are explicitly disallowed to prevent poor outcomes.

> [!NOTE]
> If you need to work around the analyzer constraint, for example if you need a keyword or ngram analyzer for certain query scenarios, you should use two separate fields for the same content. This allows one of the fields to have a suggester, while the other can be set up with a custom analyzer configuration. If you're using an indexer, you can map a source field to two different index fields to support multiple configuations.

## Create using the Azure portal

In the Azure portal, you can specify a suggester when you select **Add index**.

1. Select **Add index** and add a string field.
1. Set field attribution to **Searchable**.
1. Select an analyzer.
1. Once fields are defined, select **Autocomplete settings**.
1. Select the searchable string fields for which you want to enable an autocomplete experience.

## Create using REST

In the REST API, add suggesters by using [Create Index](/rest/api/searchservice/indexes/create). 

  ```json
  {
    "name": "hotels-sample-index",
    "fields": [
      . . .
          {
              "name": "HotelName",
              "type": "Edm.String",
              "facetable": false,
              "filterable": false,
              "key": false,
              "retrievable": true,
              "searchable": true,
              "sortable": false,
              "analyzer": "en.microsoft",
              "indexAnalyzer": null,
              "searchAnalyzer": null,
              "synonymMaps": [],
              "fields": []
          },
    ],
    "suggesters": [
      {
        "name": "sg",
        "searchMode": "analyzingInfixMatching",
        "sourceFields": ["HotelName"]
      }
    ],
    "scoringProfiles": [
      . . .
    ]
  }
  ```

## Create using .NET

In C#, define a [SearchSuggester object](/dotnet/api/azure.search.documents.indexes.models.searchsuggester). `Suggesters` is a collection on a SearchIndex object, but it can only take one item. Add a suggester to the index definition.

```csharp
private static void CreateIndex(string indexName, SearchIndexClient indexClient)
{
    FieldBuilder fieldBuilder = new FieldBuilder();
    var searchFields = fieldBuilder.Build(typeof(Hotel));

    var definition = new SearchIndex(indexName, searchFields);

    var suggester = new SearchSuggester("sg", new[] { "HotelName", "Category", "Address/City", "Address/StateProvince" });
    definition.Suggesters.Add(suggester);

    indexClient.CreateOrUpdateIndex(definition);
}
```

## Property reference

|Property      |Description      |
|--------------|-----------------|
| name        | Specified in the suggester definition, but also called on an Autocomplete or Suggestions request. |
| sourceFields | Specified in the suggester definition. It's a list of one or more fields in the index that are the source of the content for suggestions. Fields must be of type `Edm.String`. If an analyzer is specified on the field, it must be a named lexical analyzer listed on [LexicalAnalyzerName Struct](/dotnet/api/azure.search.documents.indexes.models.lexicalanalyzername) (not a custom analyzer). </br></br>As a best practice, specify only those fields that lend themselves to an expected and appropriate response, whether it's a completed string in a search bar or a dropdown list. </br></br>A hotel name is a good candidate because it has precision. Verbose fields like descriptions and comments are too dense. Similarly, repetitive fields, such as categories and tags, are less effective. In the examples, we include *category* anyway to demonstrate that you can include multiple fields. |
| searchMode  | REST-only parameter, but also visible in the Azure portal. This parameter isn't available in the .NET SDK. It indicates the strategy used to search for candidate phrases. The only mode currently supported is `analyzingInfixMatching`, which currently matches on the beginning of a term.|

<a name="how-to-use-a-suggester"></a>

## Use a suggester

A suggester is used in a query. After a suggester is created, call one of the following APIs for a search-as-you-type experience:

+ [Suggest REST API](/rest/api/searchservice/documents/suggest-post)
+ [Autocomplete REST API](/rest/api/searchservice/documents/autocomplete-post)
+ [SuggestAsync method](/dotnet/api/azure.search.documents.searchclient.suggestasync)
+ [AutocompleteAsync method](/dotnet/api/azure.search.documents.searchclient.autocompleteasync)

In a search application, client code should use a library like [jQuery UI Autocomplete](https://jqueryui.com/autocomplete/) to collect the partial query and provide the match. For more information about this task, see [Add autocomplete or suggested results to client code](search-add-autocomplete-suggestions.md).

API usage is illustrated in the following call to the Autocomplete REST API. There are two takeaways from this example. First, as with all queries, the operation is against the documents collection of an index and the query includes a `search` parameter, which in this case provides the partial query. Second, you must add `suggesterName` to the request. If a suggester isn't defined in the index, calls to autocomplete or suggestions fail.

```http
POST /indexes/myxboxgames/docs/autocomplete?search&api-version=2025-09-01
{
  "search": "minecraf",
  "suggesterName": "sg"
}
```

## Sample code

To learn how to use an open source Suggestions package for partial term completion in the client app, see [Explore the .NET search code](tutorial-csharp-search-query-integration.md).

## Next step

Learn more about request formulation.

> [!div class="nextstepaction"]
> [Add autocomplete and search suggestions in client apps](search-add-autocomplete-suggestions.md)
