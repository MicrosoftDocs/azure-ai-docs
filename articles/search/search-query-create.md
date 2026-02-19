---
title: Create a full text query 
titleSuffix: Azure AI Search
description: Learn how to construct a query request for full text search in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: how-to
ms.date: 01/20/2026
ai-usage: ai-assisted
ms.update-cycle: 180-days
---

# Create a full text query in Azure AI Search

If you're building a query for [full text search](search-lucene-query-architecture.md), this article provides steps for setting up the request. It also introduces a query structure, and explains how field attributes and linguistic analyzers can affect query outcomes.

## Prerequisites

+ An Azure AI Search service (any tier). [Create a service](search-create-service-portal.md) or [find an existing one](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

+ A [search index](search-how-to-create-search-index.md) with string fields attributed as *searchable*. You can also use an [index alias](search-how-to-alias.md) as the endpoint of your query request.

+ Permissions to query the index:
  + **Key-based authentication**: A [query API key](search-security-api-keys.md) for your search service.
  + **Role-based authentication**: [Search Index Data Reader](search-security-rbac.md) role.

+ For SDK development, install the Azure Search client library:
  + Python: [azure-search-documents](https://pypi.org/project/azure-search-documents/)
  + .NET: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
  + JavaScript: [@azure/search-documents](https://www.npmjs.com/package/@azure/search-documents)
  + Java: [azure-search-documents](https://central.sonatype.com/artifact/com.azure/azure-search-documents)

> [!TIP]
> For a quick code example, skip to [Example of a full text query request](#example-of-a-full-text-query-request).

## Example of a full text query request

In Azure AI Search, a query is a read-only request against the docs collection of a single search index, with parameters that both inform query execution and shape the response coming back. 

A full text query is specified in a `search` parameter and consists of terms, quote-enclosed phrases, and operators. Other parameters add more definition to the request.

The following [Search POST REST API](/rest/api/searchservice/documents/search-post) call illustrates a query request using `search` and other parameters.

```http
POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "NY +view",
    "queryType": "simple",
    "searchMode": "all",
    "searchFields": "HotelName, Description, Address/City, Address/StateProvince, Tags",
    "select": "HotelName, Description, Address/City, Address/StateProvince, Tags",
    "top": 10,
    "count": true
}
```

**Reference:** [Search POST](/rest/api/searchservice/documents/search-post)

### Key points

+ **`search`** provides the match criteria, usually whole terms or phrases, with or without operators. Any field that is attributed as *searchable* in the index schema is within scope for a search operation.

+ **`queryType`** sets the parser: *simple*, *full*. The [default simple query parser](search-query-simple-examples.md) is optimal for full text search. The [full Lucene query parser](search-query-lucene-examples.md) is for advanced query constructs like regular expressions, proximity search, fuzzy and wildcard search. This parameter can also be set to *semantic* for [semantic ranking](semantic-search-overview.md) for advanced semantic modeling on the query response.

+ **`searchMode`** specifies whether matches are based on *all* criteria (favors precision) or *any* criteria (favors recall) in the expression. The default is *any*. If you anticipate heavy use of Boolean operators, which is more likely in indexes that contain large text blocks (a content field or long descriptions), be sure to test queries with the `searchMode=Any|All` parameter to evaluate the impact of that setting on Boolean search.

+ **`searchFields`** constrains query execution to specific searchable fields. During development, it's helpful to use the same field list for select and search. Otherwise a match might be based on field values that you can't see in the results, creating uncertainty as to why the document was returned.

Parameters used to shape the response:

+ **`select`** specifies which fields to return in the response. Only fields marked as *retrievable* in the index can be used in a select statement.

+ **`top`** returns the specified number of best-matching documents. In this example, only 10 hits are returned. You can use top and skip (not shown) to page the results.

+ **`count`** tells you how many documents in the entire index match overall, which can be more than what are returned. Valid values are "true" or "false". Defaults to "false". Count is accurate if the index is stable, but will under or over-report any documents that are actively added, updated, or deleted. If you’d like to get only the count without any documents, you can use $top=0.

+ **`orderby`** is used if you want to sort results by a value, such as a rating or location. Otherwise, the default is to use the relevance score to rank results. A field must be attributed as *sortable* to be a candidate for this parameter.

## Choose a client

For early development and proof-of-concept testing, start with the Azure portal or a REST client or a Jupyter notebook. These approaches are interactive, useful for targeted testing, and help you assess the effects of different properties without having to write any code.

To call search from within an app, use the `Azure.Document.Search` client libraries in the Azure SDKs for .NET, Java, JavaScript, and Python.

### [**Azure portal**](#tab/portal-text-query)

In the Azure portal, when you open an index, you can work with Search Explorer alongside the index JSON definition in side-by-side tabs for easy access to field attributes. Check the **Fields** table to see which ones are searchable, sortable, filterable, and facetable while testing queries.

1. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. In your service, select **Indexes** and choose an index.

1. An index opens to the [**Search explorer**](search-explorer.md) tab so that you can query right away. Switch to **JSON view** to specify query syntax. 

   Here's a full text search query expression that works for the Hotels sample index:

   ```json
      {
          "search": "pool spa +airport",
          "queryType": "simple",
          "searchMode": "any",
          "searchFields": "Description, Tags",
          "select": "HotelName, Description, Tags",
          "top": 10,
          "count": true
      }
    ```

   **Reference:** [Search POST](/rest/api/searchservice/documents/search-post)

   The following screenshot illustrates the query and response:

   :::image type="content" source="media/search-explorer/search-explorer-full-text-query-hotels.png" alt-text="Screenshot of Search Explorer with a full text query.":::

### [**REST API**](#tab/rest-text-query)

When called with GET, the length of the request URL can't exceed 8 KB. This length is enough for most applications. However, some applications produce large queries, specifically when OData filter expressions are used. For these applications, HTTP POST is a better choice because it allows larger filters than GET.

With POST, the number of clauses in a filter is the limiting factor, not the size of the raw filter string since the request size limit for POST is approximately 16 MB. Even though the POST request size limit is large, filter expressions can't be arbitrarily complex. For more information about filter complexity limitations, see [OData Expression Syntax](query-odata-filter-orderby-syntax.md).

Use a REST client to set up a request. If you need help with getting started, see [Quickstart: Full-text search using REST](search-get-started-text.md).

The following example calls the REST API for full text search:

```http
POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "NY +view",
    "queryType": "simple",
    "searchMode": "all",
    "searchFields": "HotelName, Description, Address/City, Address/StateProvince, Tags",
    "select": "HotelName, Description, Address/City, Address/StateProvince, Tags",
    "count": true
}
```

**Reference:** [Search POST](/rest/api/searchservice/documents/search-post)

**Continuation of Partial Search Responses**

Sometimes Azure AI Search can't return all the requested results in a single Search response. A partial response can happen for different reasons, such as when the query returns too many documents by not specifying $top, or by specifying a value for $ top that's too large. In such cases, Azure AI Search includes the @odata.nextLink annotation in the response body, and also @search.nextPageParameters if it was a POST request. You can use the values of these annotations to formulate another Search request to get the next part of the search response. This behavior is called a *continuation* of the original Search request, and the annotations are called *continuation tokens*. See the example in the Response section for details on the syntax of these annotations and where they appear in the response body.  

The reasons why Azure AI Search might return continuation tokens are implementation-specific and subject to change. Robust clients should always be ready to handle cases where fewer documents than expected are returned and a continuation token is included to continue retrieving documents. Also note that you must use the same HTTP method as the original request in order to continue. For example, if you sent a GET request, any continuation requests you send must also use GET (and likewise for POST).

> [!NOTE]
> The purpose of @odata.nextLink and @search.nextPageParameters is to protect the service from queries that request too many results, not to provide a general mechanism for paging. If you want to page through results, use $top and $skip together. For example, if you want pages of size 10, your first request should have $top=10 and $skip=0, the second request should have $top=10 and $skip=10, the third request should have $top=10 and $skip=20, and so on.

### [**Azure SDKs**](#tab/sdk-text-query)

The following examples show how to run a full-text query using the Azure SDKs.

#### Python

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Set up the client
service_name = "<your-search-service-name>"
index_name = "hotels-sample-index"
api_key = "<your-query-api-key>"

endpoint = f"https://{service_name}.search.windows.net"
credential = AzureKeyCredential(api_key)
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Run a full-text search query
results = client.search(
    search_text="NY +view",
    search_mode="all",
    search_fields=["HotelName", "Description", "Address/City", "Tags"],
    select=["HotelName", "Description", "Address/City", "Tags"],
    top=10,
    include_total_count=True
)

print(f"Total documents matching query: {results.get_count()}")
for result in results:
    print(f"Hotel: {result['HotelName']}")
```

**Reference:** [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient), [search](/python/api/azure-search-documents/azure.search.documents.searchclient#azure-search-documents-searchclient-search)

#### C#

```csharp
using Azure;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

// Set up the client
string serviceName = "<your-search-service-name>";
string indexName = "hotels-sample-index";
string apiKey = "<your-query-api-key>";

Uri endpoint = new Uri($"https://{serviceName}.search.windows.net");
AzureKeyCredential credential = new AzureKeyCredential(apiKey);
SearchClient searchClient = new SearchClient(endpoint, indexName, credential);

// Run a full-text search query
SearchOptions options = new SearchOptions
{
    SearchMode = SearchMode.All,
    IncludeTotalCount = true,
    Size = 10
};
options.SearchFields.Add("HotelName");
options.SearchFields.Add("Description");
options.Select.Add("HotelName");
options.Select.Add("Description");

SearchResults<SearchDocument> response = await searchClient.SearchAsync<SearchDocument>("NY +view", options);

Console.WriteLine($"Total documents matching query: {response.TotalCount}");
await foreach (SearchResult<SearchDocument> result in response.GetResultsAsync())
{
    Console.WriteLine($"Hotel: {result.Document["HotelName"]}");
}
```

**Reference:** [SearchClient](/dotnet/api/azure.search.documents.searchclient), [SearchAsync](/dotnet/api/azure.search.documents.searchclient.searchasync), [SearchOptions](/dotnet/api/azure.search.documents.searchoptions)

#### Additional SDK resources

| Azure SDK | Client | Examples |
| --------- | ------ | -------- |
| .NET | [SearchClient](/dotnet/api/azure.search.documents.searchclient) | [DotNetHowTo](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowTo) |
| Java | [SearchClient](/java/api/com.azure.search.documents.searchclient) | [SearchForDynamicDocumentsExample.java](https://github.com/Azure/azure-sdk-for-java/blob/azure-search-documents_11.1.3/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/SearchForDynamicDocumentsExample.java) |
| JavaScript | [SearchClient](/javascript/api/@azure/search-documents/searchclient) | [SDK examples](/javascript/api/overview/azure/search-documents-readme?view=azure-node-latest#examples&preserve-view=true) |
| Python | [SearchClient](/python/api/azure-search-documents/azure.search.documents.searchclient) | [sample_simple_query.py](https://github.com/Azure/azure-sdk-for-python/blob/7cd31ac01fed9c790cec71de438af9c45cb45821/sdk/search/azure-search-documents/samples/sample_simple_query.py) |

---

## Choose a query type: simple | full

If your query is full text search, a query parser is used to process any text that's passed as search terms and phrases. Azure AI Search offers two query parsers. 

+ The simple parser understands the [simple query syntax](query-simple-syntax.md). This parser was selected as the default for its speed and effectiveness in free form text queries. The syntax supports common search operators (AND, OR, NOT) for term and phrase searches, and prefix (`*`) search (as in `sea*` for Seattle and Seaside). A general recommendation is to try the simple parser first, and then move on to full parser if application requirements call for more powerful queries.

+ The [full Lucene query syntax](query-Lucene-syntax.md#bkmk_syntax), enabled when you add `queryType=full` to the request, is based on the [Apache Lucene Parser](https://lucene.apache.org/core/6_6_1/queryparser/org/apache/lucene/queryparser/classic/package-summary.html).

Full syntax and simple syntax overlap to the extent that both support the same prefix and Boolean operations, but the full syntax provides more operators. In full, there are more operators for Boolean expressions, and more operators for advanced queries such as fuzzy search, wildcard search, proximity search, and regular expressions.

## Choose query methods

Search is fundamentally a user-driven exercise, where terms or phrases are collected from a search box, or from click events on a page. The following table summarizes the mechanisms by which you can collect user input, along with the expected search experience.

| Input | Experience |
|-------|---------|
| [Search method](/rest/api/searchservice/documents/search-post) | A user types the terms or phrases into a search box, with or without operators, and selects **Search** to send the request. Search can be used with filters on the same request, but not with autocomplete or suggestions. |
| [Autocomplete method](/rest/api/searchservice/documents/autocomplete-post) | A user types a few characters, and queries are initiated after each new character is typed. The response is a completed string from the index. If the string provided is valid, the user selects **Search** to send that query to the service. |
| [Suggestions method](/rest/api/searchservice/documents/suggest-post) | As with autocomplete, a user types a few characters and incremental queries are generated. The response is a dropdown list of matching documents, typically represented by a few unique or descriptive fields. If any of the selections are valid, the user selects one and the matching document is returned. |
| [Faceted navigation](/rest/api/searchservice/documents/search-post#searchrequest) | A page shows clickable navigation links or breadcrumbs that narrow the scope of the search. A faceted navigation structure is composed dynamically based on an initial query. For example, `search=*` to populate a faceted navigation tree composed of every possible category. A faceted navigation structure is created from a query response, but it's also a mechanism for expressing the next query. n REST API reference, `facets` is documented as a query parameter of a Search Documents operation, but it can be used without the `search` parameter.|
| [Filter method](/rest/api/searchservice/documents/search-post#searchrequest) | Filters are used with facets to narrow results. You can also implement a filter behind the page, for example to initialize the page with language-specific fields. In REST API reference, `$filter` is documented as a query parameter of a Search Documents operation, but it can be used without the `search` parameter.|

## Effect of field attributes on queries

If you're familiar with [query types and composition](search-query-overview.md), you might remember that the parameters on a query request depend on field attributes in an index. For example, only fields marked as *searchable* and *retrievable* can be used in queries and search results. When setting the `search`, `filter`, and `orderby` parameters in your request, you should check attributes to avoid unexpected results.

In the following screenshot of the [hotels sample index](search-get-started-portal.md), only the last two fields **LastRenovationDate** and **Rating** are *sortable*, a requirement for use in an `"$orderby"` only clause.

:::image type="content" source="media/search-query-overview/hotel-sample-index-definition.png" alt-text="Screenshot that shows the index definition for the hotel sample.":::

For field attribute definitions, see [Create Index (REST API)](/rest/api/searchservice/indexes/create).

## Effect of tokens on queries

During indexing, the search engine uses a text analyzer on strings to maximize the potential for finding a match at query time. At a minimum, strings are lower-cased, but depending on the analyzer, might also undergo lemmatization and stop word removal. Larger strings or compound words are typically broken up by whitespace, hyphens, or dashes, and indexed as separate tokens. 

The key point is that what you think your index contains, and what's actually in it, can be different. If queries don't return expected results, you can inspect the tokens created by the analyzer through the [Analyze Text (REST API)](/rest/api/searchservice/indexes/analyze). For more information about tokenization and the effect on queries, see [Partial term search and patterns with special characters](search-query-partial-matching.md).

## Troubleshoot queries

The following table lists common query issues and how to resolve them.

| Issue | Cause | Resolution |
| ----- | ----- | ---------- |
| Empty results | No documents match query terms. | Verify field is marked *searchable* in schema. Use [Analyze Text API](/rest/api/searchservice/indexes/analyze) to check tokenization. |
| Unexpected results | Query matches unintended fields. | Use `searchFields` to limit which fields are searched. |
| Too many results | Query is too broad. | Add filters, use `searchMode=all`, or add required terms with `+` operator. |
| Results not ranked as expected | Relevance scoring doesn't match expectations. | Consider [scoring profiles](index-add-scoring-profiles.md) or [semantic ranking](semantic-search-overview.md). |
| Partial matches missing | Analyzer tokenized differently than expected. | Use wildcard (`*`) suffix or check analyzer behavior with Analyze Text API. |
| Filter not working | Field isn't marked *filterable*. | Update index schema to set `filterable: true` on the field. |

## Related content

Now that you have a better understanding of how query requests work, try the following quickstarts for hands-on experience.

+ [Search explorer](search-explorer.md)
+ [Quickstart: Full-text search](search-get-started-text.md)
+ [Simple query syntax](query-simple-syntax.md)
+ [Full Lucene query syntax](query-lucene-syntax.md)
+ [OData filter syntax](query-odata-filter-orderby-syntax.md)
