---
title: Page list API results
description: Learn how to page through Azure AI Search list APIs in preview, including supported operations and continuation patterns.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/15/2026
ai-usage: ai-assisted
---

# Use paging with Azure AI Search list APIs

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Paging support in the `2026-05-01-preview` API makes Azure AI Search list
operations easier to use at scale. Instead of assuming a list call returns the
full collection, callers can request one page at a time, process the results,
and continue until the collection is exhausted.

Use paging for management tools, admin workflows, and inventory jobs that
enumerate large collections of indexes, indexers, data sources, skillsets,
knowledge bases, or knowledge sources.

## Prerequisites

+ An Azure AI Search service with objects to enumerate.

+ A client that can call the `2026-05-01-preview` REST APIs or an equivalent
  preview SDK.

+ Permission to call the list operation you want to page through.

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

## Send the first paged request

The following example requests five indexes and asks the service to include
the total count:

```http
GET {{search-url}}/indexes?$top=5&$skip=0&$count=true&api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{search-api-key}}
```

The response includes the first page of values. If more results are available,
the response includes `@odata.nextLink`.

```json
{
  "@odata.count": 43,
  "value": [
    { "name": "index-1" },
    { "name": "index-2" },
    { "name": "index-3" },
    { "name": "index-4" },
    { "name": "index-5" }
  ],
  "@odata.nextLink": "https://contoso.search.windows.net/indexes?$top=5&$skip=5&$count=true&api-version=2026-05-01-preview"
}
```

## Continue through all pages

Treat continuation information as opaque. Prefer following `@odata.nextLink`
when it's present instead of constructing the next request yourself.

The following pseudocode shows the basic paging loop:

```text
nextLink = "/indexes?$top=50&$count=true&api-version=2026-05-01-preview"

while nextLink is not null:
    response = GET nextLink
    process response.value
    nextLink = response["@odata.nextLink"]
```

`@odata.nextLink` is the continuation mechanism for paged list responses in
this preview. Treat it as opaque and don't depend on the `$skip` value or other
query parameters embedded in the URL.

## Supported list operations

The following list operations support paging in the preview:

| Operation | Priority |
| --- | --- |
| List Indexes | P0 |
| List Index Statistics Summary | P0 |
| List Synonym Maps | P1 |
| List Indexers | P1 |
| List Data Sources | P1 |
| List Skillsets | P1 |
| List Knowledge Bases | P1 |
| List Knowledge Sources | P1 |

Aliases aren't included in the preview paging scope.

During preview validation, `GET /indexes` accepted `$top`, `$skip`, and
`$count`, but didn't always populate `@odata.nextLink` when more pages were
available. `GET /knowledgebases` and `GET /knowledgesources` rejected `$top` and
`$skip` in the tested environment. Treat those as preview service issues if you
encounter them before the feature is fully rolled out.

## Related content

+ [Manage Azure AI Search using REST APIs](search-manage-rest.md)
+ [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
+ [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
