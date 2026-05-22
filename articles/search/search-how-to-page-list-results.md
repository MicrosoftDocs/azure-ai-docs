---
title: Page List API Results
description: Learn how to page through Azure AI Search list APIs in preview, including supported operations and continuation patterns.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Use paging with Azure AI Search list APIs

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

Paging support in the `2026-05-01-preview` API makes Azure AI Search list
operations easier to use at scale. Instead of assuming a list call returns the
full collection, callers can request one page at a time, process the results,
and continue until the collection is exhausted.

Use paging for management tools, admin workflows, and inventory jobs that
enumerate large collections of indexes, indexers, data sources, skillsets,
knowledge bases, or knowledge sources.

## Prerequisites

+ An Azure AI Search service with objects to enumerate.

+ Permission to call the list operation you want to page through.

::: zone pivot="csharp"

+ The latest preview [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package: `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest preview [azure-search-documents](https://pypi.org/project/azure-search-documents/) package: `pip install azure-search-documents --pre`

::: zone-end

::: zone pivot="rest"

+ A client that can call the `2026-05-01-preview` REST APIs.

::: zone-end

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Choose paging parameters

Supported preview list operations accept paging parameters that control the
page size, offset, and count behavior.

| Parameter | Type | Default | Maximum | Description |
| --- | --- | --- | --- | --- |
| `$top` | Integer | `50` | `1000` | Number of items to retrieve in the page. |
| `$skip` | Integer | `0` | No fixed maximum other than the number of objects in the list. | Number of items to skip before returning results. |
| `$count` | Boolean | `false` | Not applicable | Returns the total item count when set to `true`. |

If `$top` is omitted, the service returns up to 50 items by default. If a
request asks for more than 1,000 items, the service returns at most 1,000 items
in the page and includes continuation information when more items remain.
Filtering and ordering parameters, such as `$filter` and `$orderby`, aren't
part of this preview paging contract.

For knowledge base and knowledge source list operations, the service orders
resources by name before applying `$skip` and `$top`, so paging is stable across
requests when the collection doesn't change.

## Send the first paged request

The following example requests five indexes and asks the service to include
the total count.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var page = indexClient.GetIndexesAsync(top: 5, skip: 0).AsPages().GetAsyncEnumerator();
await page.MoveNextAsync();
foreach (var index in page.Current.Values)
{
    Console.WriteLine(index.Name);
}
```

**Reference:** [SearchIndexClient.GetIndexesAsync](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint="search_url", credential=AzureKeyCredential("api_key"))

for index in index_client.list_indexes(top=5, skip=0):
    print(index.name)
```

**Reference:** [SearchIndexClient.list_indexes](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
GET {{search-url}}/indexes?$top=5&$skip=0&$count=true&api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{search-api-key}}
```

The response includes the first page of values. When you specify `$top`, request
subsequent pages by increasing `$skip`.

```json
{
  "@odata.count": 43,
  "value": [
    { "name": "index-1" },
    { "name": "index-2" },
    { "name": "index-3" },
    { "name": "index-4" },
    { "name": "index-5" }
  ]
}
```

::: zone-end

## Continue through all pages

When you control `$top`, continue by increasing `$skip` until the response
contains fewer items than requested. If the service applies the default page
size because `$top` is omitted, or caps a request above the maximum page size,
the response can include `@odata.nextLink` when more results remain. Treat
`@odata.nextLink` as opaque when it's present.

::: zone pivot="csharp"

The .NET SDK pages through results transparently. Iterating an `AsyncPageable<T>`
fetches each page on demand, so a simple `await foreach` covers the entire
collection. Set `top` to control the page size that the SDK requests from the
service.

```csharp
await foreach (var index in indexClient.GetIndexesAsync(top: 50))
{
    Console.WriteLine(index.Name);
}
```

::: zone-end

::: zone pivot="python"

The Python SDK pages through results transparently. Iterating the iterator
returned by `list_indexes` fetches each page on demand, so a simple `for` loop
covers the entire collection. Set `top` to control the page size that the SDK
requests from the service.

```python
for index in index_client.list_indexes(top=50):
    print(index.name)
```

::: zone-end

::: zone pivot="rest"

The following pseudocode shows the basic paging loop for REST callers:

```text
top = 50
skip = 0

while true:
    response = GET "/indexes?$top={top}&$skip={skip}&$count=true&api-version=2026-05-01-preview"
    process response.value

    if response.value.length < top:
        break

    skip = skip + top
```

::: zone-end

## Supported list operations

The following list operations support paging in the preview:

+ List Indexes
+ List Index Statistics Summary
+ List Synonym Maps
+ List Indexers
+ List Data Sources
+ List Skillsets
+ List Knowledge Bases
+ List Knowledge Sources

Aliases aren't included in the preview paging scope.

Knowledge base and knowledge source list operations support `$top`, `$skip`,
and `$count` in the `2026-05-01-preview` API.

## Related content

+ [Manage Azure AI Search using REST APIs](search-manage-rest.md)
+ [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
+ [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
