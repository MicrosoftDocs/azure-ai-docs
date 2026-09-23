---
title: moreLikeThis Query Feature
description: Describes the moreLikeThis feature, which is available in preview versions of the Azure AI Search REST API.
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 02/19/2026
ms.update-cycle: 365-days
ai-usage: ai-assisted
---

# moreLikeThis in Azure AI Search (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [preview-terms](./includes/previews/preview-terms.md)]

The `moreLikeThis` query parameter (preview), specified as `moreLikeThis=[key]` in the [Search Documents API](/rest/api/searchservice/documents/search-post), finds documents similar to a source document identified by its key. When a search request includes `moreLikeThis`, Azure AI Search generates a query from the terms that best describe the source document. You can't combine `moreLikeThis` with `search=[string]`.

By default, the contents of all top-level searchable fields are considered. If you want to specify particular fields instead, you can use the `searchFields` parameter. 

The `moreLikeThis` parameter isn't supported for [complex types](search-howto-complex-data-types.md) and the presence of complex types will impact your query logic. If your index is a complex type, you must set `searchFields` to the top-level searchable fields over which `moreLikeThis` iterates. For example, if the index has a searchable `field1` of type `Edm.String`, and `field2` that's a complex type with searchable subfields, the value of `searchFields` must be set to `field1` to exclude `field2`.

## Examples

All following examples use the hotels sample from [Quickstart: Full-text search in the Azure portal](search-get-started-portal.md).

### Simple query

The following query finds documents whose description fields are most similar to the field of the source document as specified by the `moreLikeThis` parameter:

```http
GET /indexes/hotels-sample/docs?moreLikeThis=29&searchFields=Description&api-version=2026-08-01-preview
```

In this example, the request searches for hotels similar to the one with `HotelId` 29.
Rather than using HTTP GET, you can also invoke `MoreLikeThis` using HTTP POST:

```http
POST /indexes/hotels-sample/docs/search?api-version=2026-08-01-preview
    {
      "moreLikeThis": "29",
      "searchFields": "Description"
    }
```

### Apply filters

`MoreLikeThis` can be combined with other common query parameters like `$filter`. For instance, the query can be restricted to only hotels whose category is 'Budget' and where the rating is higher than 3.5:

```http
GET /indexes/hotels-sample/docs?moreLikeThis=20&searchFields=Description&$filter=(Category eq 'Budget' and Rating gt 3.5)&api-version=2026-08-01-preview
```

### Select fields and limit results

The `$top` selector can be used to limit how many results should be returned in a `MoreLikeThis` query. Also, fields can be selected with `$select`. Here the top three hotels are selected along with their ID, Name, and Rating: 

```http
GET /indexes/hotels-sample/docs?moreLikeThis=20&searchFields=Description&$filter=(Category eq 'Budget' and Rating gt 3.5)&$top=3&$select=HotelId,HotelName,Rating&api-version=2026-08-01-preview
```

## Next steps

You can use any REST client for this exercise.

> [!div class="nextstepaction"]
> [Quickstart: Full-text search using REST](search-get-started-text.md)
