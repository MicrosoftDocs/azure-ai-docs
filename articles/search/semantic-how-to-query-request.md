---
title: Add semantic ranking
titleSuffix: Azure AI Search
description: Set a semantic query type to attach the deep learning models of semantic ranker.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - ignite-2024
ms.topic: how-to
ms.date: 11/06/2025
---

# Add semantic ranking to queries in Azure AI Search

You can apply semantic ranking to text queries, hybrid queries, and vector queries if your search documents contain string fields and the [vector query has a text representation](vector-search-how-to-query.md#query-with-integrated-vectorization) in the search document.

This article explains how to invoke the semantic ranker on queries. It assumes you're using the most recent stable or preview APIs. For help with older versions, see [Migrate semantic ranking code](semantic-code-migration.md).

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md) in any [region that provides semantic ranking](search-region-support.md), with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An existing search index with a [semantic configuration](semantic-how-to-configure.md) and rich text content.

+ Familiarity with [semantic ranking](semantic-search-overview.md).

> [!NOTE]
> Captions and answers are extracted verbatim from text in the search document. The semantic subsystem uses machine reading comprehension to recognize content having the characteristics of a caption or answer, but doesn't compose new sentences or phrases except in the case of [query rewrite](semantic-how-to-query-rewrite.md). For this reason, content that includes explanations or definitions work best for semantic ranking. If you want chat-style interaction with generated responses, see [Agentic retrieval](agentic-retrieval-overview.md) or [Retrieval Augmented Generation (RAG)](retrieval-augmented-generation-overview.md).

## Choose a client

You can use any of the following tools and SDKs to build a query that uses semantic ranking:

+ [Azure portal](https://portal.azure.com), using the index designer to add a semantic configuration.
+ [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
+ [Azure SDK for .NET](https://www.nuget.org/packages/Azure.Search.Documents)
+ [Azure SDK for Python](https://pypi.org/project/azure-search-documents)
+ [Azure SDK for Java](https://central.sonatype.com/artifact/com.azure/azure-search-documents)
+ [Azure SDK for JavaScript](https://www.npmjs.com/package/@azure/search-documents)

## Avoid features that bypass relevance scoring

A few query capabilities bypass relevance scoring, which makes them incompatible with semantic ranking. If your query logic includes the following features, you can't semantically rank your results:

+ A query with `search=*` or an empty search string, such as pure filter-only query, won't work because there's nothing to measure semantic relevance against and so the search scores are zero. The query must provide terms or phrases that can be evaluated during processing, and that produces search documents that are scored for relevance. Scored results are inputs to the semantic ranker.

+ Sorting (orderBy clauses) on specific fields overrides search scores and a semantic score. Given that the semantic score is supposed to provide the ranking, adding an orderby clause results in an HTTP 400 error if you apply semantic ranking over ordered results.

## Set up the query

By default, queries don't use semantic ranking. To use semantic ranking, two different parameters can be used. Each parameter supports a different set of query formats.

All semantic queries, whether specified through `search` plus `queryType`, or through `semanticQuery`, must be plain text and they can't be empty. As you can see from the table below, the `queryType-semantic` parameter supports a subset of query formats.

| Parameter | [Plain text search](search-query-create.md) | [Simple text search syntax](query-simple-syntax.md) | [Full text search syntax](query-lucene-syntax.md) | [Vector search](vector-search-how-to-query.md) | [Hybrid Search](hybrid-search-how-to-query.md) | [Semantic answers](semantic-answers.md) and captions |
|-|-|-|-|-|-|-|
| `queryType-semantic` <sup>1</sup> | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| `semanticQuery="<your plain text query>"`<sup>2</sup> | ✅ | ✅ | ✅ | ✅ |✅ | ✅ |

<sup>1</sup> `queryType=semantic` can't support explicit `simple` or `full` values because the `queryType` parameter is being used for `semantic`. The effective query behaviors are the defaults of the simple parser.

<sup>2</sup> The `semanticQuery` parameter can be used for all query types. However, it isn't supported in the Azure portal [Search Explorer](search-explorer.md).

Regardless of the parameter chosen, the index should contain text fields with rich semantic content and a [semantic configuration](semantic-how-to-configure.md).

### [**Azure portal**](#tab/portal-query)

[Search explorer](search-explorer.md) includes options for semantic ranking. Recall that you can't set the `semanticQuery` parameter in the Azure portal.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Open a search index and select **Search explorer**.

1. Select **Query options**. If you already defined a semantic configuration, it's selected by default. If you don't have one, [create a semantic configuration](semantic-how-to-configure.md) for your index.

    :::image type="content" source="./media/semantic-search-overview/search-explorer-semantic-query-options-v2.png" alt-text="Screenshot showing query options in Search explorer." border="true":::

1. Enter a query, such as "historic hotel with good food", and select **Search**.

1. Alternatively, select **JSON view** and paste definitions into the query editor. The Azure portal doesn't support using `semanticQuery`, so setting `queryType` to `"semantic"` is required:

   :::image type="content" source="./media/semantic-search-overview/semantic-portal-json-query.png" alt-text="Screenshot showing JSON query syntax in the Azure portal." border="true":::

   JSON example for setting query type to semantic that you can paste into the view:

    ```json
    {
      "search": "funky or interesting hotel with good food on site",
      "count": true,
      "queryType": "semantic",
      "semanticConfiguration": "my-semantic-config",
      "captions": "extractive|highlight-true",
      "answers": "extractive|count-3",
      "highlightPreTag": "<strong>",
      "highlightPostTag": "</strong>",
      "select": "HotelId,HotelName,Description,Category"
    }
    ```

### [**REST API**](#tab/rest-query)

Use [Search Documents](/rest/api/searchservice/documents/search-post) to formulate the request.

A response includes an `@search.rerankerScore` automatically. If you want captions or answers in the response, enable semantic ranking by setting `queryType` to `semantic` or setting `semanticQuery` and adding captions and answers to the request.

The following examples in this section use the [hotels-sample-index](search-get-started-portal.md) to demonstrate semantic ranking with semantic answers and captions.

#### Use queryType=semantic

If you want to set `queryType` to `semantic`, paste the following request into a web client as a template. Replace `search-service-name` with your search service name and replace `hotels-sample-index` if you have a different index name.

```http
POST https://[search-service-name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
      "search": "interesting hotel with restaurant on site and cozy lobby or shared area",
      "count": true,
      "queryType": "semantic",
      "semanticConfiguration": "semantic-config",
      "captions": "extractive|highlight-true",
      "answers": "extractive|count-3",
      "highlightPreTag": "<strong>",
      "highlightPostTag": "</strong>",
      "select": "HotelId,HotelName,Description,Category"
}
```

1. Set `queryType` to `semantic`. This improves precision of search results by reranking the top 50 matches using a ranking model trained on the Bing corpus for queries expressed in natural language as opposed to keywords. If you set the query type to semantic, you must also set semanticConfiguration. You can optionally set answers if you want to also return the top 3 answers if the query input was formulated in natural language ("what is a ...), and you can optionally set captions to extract key passages from the highest ranked documents.

1. Set `search` to a simple plain text query. Since the `queryType` is set to `semantic`,  [simple syntax](query-simple-syntax.md) or [full Lucene syntax](query-lucene-syntax.md) aren't supported. Supplying `*` or an empty string results in no semantic ranking being applied to the query. 

1. Set `semanticConfiguration` to a [predefined semantic configuration](semantic-how-to-configure.md) that's embedded in your index.

1. Set `answers` to specify whether [semantic answers](semantic-answers.md) are included in the result. Valid values for this parameter are `extractive` and `none`. This parameter is only valid if the query type is "semantic". When set to "extractive", the query formulates and returns answers from key passages in the highest semantically ranked documents. The default is one answer, but you can specify up to 10 by adding a count. For example, `"answers": "extractive|count-3"` returns three answers. For an answer to be returned, there must be verbatim content in the targeted field that looks like an answer. The language models used for answers are trained to recognize answers, not generate them. In addition, the query itself must look like a question.

1. Set `captions` to specify whether semantic captions are included in the result. Valid values are "none" and "extractive". Defaults to "none". This parameter is only valid if the query type is "semantic". When set to "extractive", the query returns captions extracted from key passages in the highest ranked documents. 

   When captions is set to 'extractive', highlighting is enabled by default, and can be configured by appending the pipe character '|' followed by the `highlight-<true/false>` option, such as `extractive|highlight-true`. This example returns captions without highlights: `extractive|highlight-false`.

   The basis for captions and answers are the fields referenced in the "semanticConfiguration". These fields are under a combined limit in the range of 2,000 tokens or approximately 20,000 characters. If you anticipate a token count exceeding this limit, consider a [data chunking step](vector-search-how-to-chunk-documents.md) using the [Text split skill](cognitive-search-skill-textsplit.md). This approach introduces a dependency on an [AI enrichment pipeline](cognitive-search-concept-intro.md) and [indexers](search-indexer-overview.md).

1. Set `highlightPreTag` and `highlightPostTag` if you want to override the default highlight formatting that's applied to captions.

   Captions apply highlight formatting over key passages in the document that summarize the response. The default is `<em>`. If you want to specify the type of formatting (for example, yellow background), you can set the highlightPreTag and highlightPostTag.

1. Set [select](search-query-odata-select.md) to specify which fields are returned in the response, and "count" to return the number of matches in the index. These parameters improve the quality of the request and readability of the response.

1. Send the request to execute the query and return results.

#### Use semanticQuery

By using `semanticQuery`, you can explicitly apply [simple text syntax](query-simple-syntax.md) or [full text syntax](query-lucene-syntax.md), which means you can now do fielded search, term boosting, and proximity search. You can also specify a [pure vector query](vector-search-how-to-query.md) instead of just hybrid.

Adjust your request to the following JSON to use `semanticQuery`.

```http
POST https://[search-service-name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "Description:breakfast",
    "semanticQuery": "interesting hotel with restaurant on site and cozy lobby or shared area",
    "count": true,
    "queryType": "full",
    "semanticConfiguration": "semantic-config",
    "captions": "extractive|highlight-true",
    "answers": "extractive|count-3",
    "highlightPreTag": "<strong>",
    "highlightPostTag": "</strong>",
    "select": "HotelId,HotelName,Description,Category"
}
```

1. Set `queryType` to the search syntax you're using, either [simple](query-simple-syntax.md) or [full](query-lucene-syntax.md).

1. Set `semanticQuery` to the simple plain text query you want to use for semantic ranking. Empty queries aren't supported. Avoid operators or any query syntax inside the string itself.

### [**.NET SDK**](#tab/dotnet-query)

Use QueryType or SemanticQuery to invoke semantic ranker on a semantic query. The [following example](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample08_SemanticSearch.md) is from the Azure SDK team.

```csharp
SearchResults<Hotel> response = await searchClient.SearchAsync<Hotel>(
    "interesting hotel with restaurant on site and cozy lobby or shared area",
    new SearchOptions
    {
        SemanticSearch = new()
        {
            SemanticConfigurationName = "my-semantic-config",
            QueryCaption = new(QueryCaptionType.Extractive),
            QueryAnswer = new(QueryAnswerType.Extractive)
        },
        QueryType = SearchQueryType.Semantic
    });

int count = 0;
Console.WriteLine($"Semantic Search Results:");

Console.WriteLine($"\nQuery Answer:");
foreach (QueryAnswerResult result in response.SemanticSearch.Answers)
{
    Console.WriteLine($"Answer Highlights: {result.Highlights}");
    Console.WriteLine($"Answer Text: {result.Text}");
}

await foreach (SearchResult<Hotel> result in response.GetResultsAsync())
{
    count++;
    Hotel doc = result.Document;
    Console.WriteLine($"{doc.HotelId}: {doc.HotelName}");

    if (result.SemanticSearch.Captions != null)
    {
        var caption = result.SemanticSearch.Captions.FirstOrDefault();
        if (caption.Highlights != null && caption.Highlights != "")
        {
            Console.WriteLine($"Caption Highlights: {caption.Highlights}");
        }
        else
        {
            Console.WriteLine($"Caption Text: {caption.Text}");
        }
    }
}
Console.WriteLine($"Total number of search results:{count}");
```

To use `semanticQuery` instead of setting `queryType` to `semantic`, the search code snippet can be replaced with the following code snippet:

```csharp
SearchResults<Hotel> response = await searchClient.SearchAsync<Hotel>(
    "Luxury hotel",
    new SearchOptions
    {
        SemanticSearch = new()
        {
            SemanticConfigurationName = "my-semantic-config",
            QueryCaption = new(QueryCaptionType.Extractive),
            QueryAnswer = new(QueryAnswerType.Extractive),
            SemanticQuery = "Is there any hotel located on the main commercial artery of the city in the heart of New York?"
        }
    });
```

---

## Evaluate the response

Only the top 50 matches from the initial results can be semantically ranked. As with all queries, a response is composed of all fields marked as retrievable, or just those fields listed in the `select` parameter. A response includes the original relevance score, and might also include a count, or batched results, depending on how you formulated the request.

In semantic ranking, the response has more elements: a new [semantically ranked relevance score](semantic-search-overview.md#how-results-are-scored), an optional caption in plain text and with highlights, and an optional [answer](semantic-answers.md). If your results don't include these extra elements, then your query might be misconfigured. As a first step towards troubleshooting the problem, check the semantic configuration to ensure it's specified in both the index definition and query.

In a client app, you can structure the search page to include a caption as the description of the match, rather than the entire contents of a specific field. This approach is useful when individual fields are too dense for the search results page.

The response for the above example query (*"interesting hotel with restaurant on site and cozy lobby or shared area"*) returns three answers (`"answers": "extractive|count-e"`). Captions are returned because the "captions" property is set, with plain text and highlighted versions. If an answer can't be determined, it's omitted from the response. For brevity, this example shows just the three answers and the three highest scoring results from the query.

```json
{
  "@odata.count": 29,
  "@search.answers": [
    {
      "key": "24",
      "text": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.",
      "highlights": "Chic hotel near the city. <strong>High-rise hotel in downtown, </strong>within<strong> walking distance to </strong>theaters, art<strong> galleries, restaurants and shops.</strong> Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.",
      "score": 0.9340000152587891
    },
    {
      "key": "40",
      "text": "Only 8 miles from Downtown. On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, All non-smoking hotel. Only 15 miles from airport.",
      "highlights": "Only 8 miles from Downtown. <strong>On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, </strong>All non-smoking<strong> hotel.</strong> Only 15 miles from airport.",
      "score": 0.9210000038146973
    },
    {
      "key": "38",
      "text": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
      "highlights": "Nature is Home on the beach. Explore the shore by day, and then come home to our<strong> shared living space </strong>to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
      "score": 0.9200000166893005
    }
  ],
  "value": [
    {
      "@search.score": 3.2328331,
      "@search.rerankerScore": 2.575303316116333,
      "@search.captions": [
        {
          "text": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a complimentary continental breakfast in the lobby, and free Wi-Fi throughout the hotel.",
          "highlights": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our<strong> penthouse </strong>suites offer views for miles and the rooftop<strong> plaza </strong>is open to all guests from sunset to 10 p.m. Enjoy a<strong> complimentary continental breakfast in the lobby, </strong>and free Wi-Fi<strong> throughout </strong>the hotel."
        }
      ],
      "HotelId": "50",
      "HotelName": "Head Wind Resort",
      "Description": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a complimentary continental breakfast in the lobby, and free Wi-Fi throughout the hotel.",
      "Category": "Suite"
    },
    {
      "@search.score": 0.632956,
      "@search.rerankerScore": 2.5425150394439697,
      "@search.captions": [
        {
          "text": "Every stay starts with a warm cookie. Amenities like the Counting Sheep sleep experience, our Wake-up glorious breakfast buffet and spacious workout facilities await.",
          "highlights": "Every stay starts with a warm cookie. Amenities like the<strong> Counting Sheep sleep experience, </strong>our<strong> Wake-up glorious breakfast buffet and spacious workout facilities </strong>await."
        }
      ],
      "HotelId": "34",
      "HotelName": "Lakefront Captain Inn",
      "Description": "Every stay starts with a warm cookie. Amenities like the Counting Sheep sleep experience, our Wake-up glorious breakfast buffet and spacious workout facilities await.",
      "Category": "Budget"
    },
    {
      "@search.score": 3.7076726,
      "@search.rerankerScore": 2.4554927349090576,
      "@search.captions": [
        {
          "text": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.",
          "highlights": "Chic hotel near the city. <strong>High-rise hotel in downtown, </strong>within<strong> walking distance to </strong>theaters, art<strong> galleries, restaurants and shops.</strong> Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance."
        }
      ],
      "HotelId": "24",
      "HotelName": "Uptown Chic Hotel",
      "Description": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.",
      "Category": "Suite"
    },
   . . .
  ]
}
```

## Expected workloads

For semantic ranking, you should expect a search service to support up to 10 concurrent queries per replica. 

The service throttles semantic ranking requests if volumes are too high. An error message that includes these phrases indicate the service is at capacity for semantic ranking:

```json
Error in search query: Operation returned an invalid status 'Partial Content'`
@search.semanticPartialResponseReason`
CapacityOverloaded
```

If you anticipate consistent throughput requirements near, at, or higher than this level, please file a support ticket so that we can provision for your workload.

## Next steps

Semantic ranking can be used in hybrid queries that combine keyword search and vector search into a single request and a unified response.

> [!div class="nextstepaction"]
> [Hybrid query with semantic ranker](hybrid-search-how-to-query.md#example-semantic-hybrid-search)
