---
title: OData full-text search function reference
titleSuffix: Azure AI Search
description: OData full-text search functions, search.ismatch and search.ismatchscoring, in Azure AI Search queries.
manager: nitinme
author: bevloh
ms.author: beloh
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 07/10/2025
ms.update-cycle: 365-days

---
# OData full-text search functions in Azure AI Search - `search.ismatch` and `search.ismatchscoring`

Azure AI Search supports full-text search in the context of [OData filter expressions](query-odata-filter-orderby-syntax.md) via the `search.ismatch` and `search.ismatchscoring` functions. These functions allow you to combine full-text search with strict Boolean filtering in ways that aren't possible just by using the top-level `search` parameter of the [Search API](/rest/api/searchservice/documents/search-post).

> [!NOTE]
> The `search.ismatch` and `search.ismatchscoring` functions are only supported in filters in the [Search API](/rest/api/searchservice/documents/search-post). They aren't supported in the [Suggest](/rest/api/searchservice/documents/suggest-post) or [Autocomplete](/rest/api/searchservice/documents/autocomplete-post) APIs.

## Syntax

The following EBNF ([Extended Backus-Naur Form](https://en.wikipedia.org/wiki/Extended_Backus–Naur_form)) defines the grammar of the `search.ismatch` and `search.ismatchscoring` functions:

<!-- Upload this EBNF using https://bottlecaps.de/rr/ui to create a downloadable railroad diagram. -->

```
search_is_match_call ::=
    'search.ismatch'('scoring')?'(' search_is_match_parameters ')'

search_is_match_parameters ::=
    string_literal(',' string_literal(',' query_type ',' search_mode)?)?

query_type ::= "'full'" | "'simple'"

search_mode ::= "'any'" | "'all'"
```

An interactive syntax diagram is also available:

> [!div class="nextstepaction"]
> [OData syntax diagram for Azure AI Search](https://azuresearch.github.io/odata-syntax-diagram/#search_is_match_call)

> [!NOTE]
> See [OData expression syntax reference for Azure AI Search](search-query-odata-syntax-reference.md) for the complete EBNF.

### search.ismatch

The `search.ismatch` function evaluates a full-text search query as a part of a filter expression. Matching documents are returned in the result set. The following overloads of this function are available:

- `search.ismatch(search)`
- `search.ismatch(search, searchFields)`
- `search.ismatch(search, searchFields, queryType, searchMode)`

The parameters are defined in the following table:

| Parameter name | Type | Description |
| --- | --- | --- |
| `search` | `Edm.String` | The search query (in either [simple](query-simple-syntax.md) or [full](query-lucene-syntax.md) Lucene query syntax). |
| `searchFields` | `Edm.String` | Comma-separated list of searchable fields to search in; defaults to all searchable fields in the index. When you use [fielded search](query-lucene-syntax.md#bkmk_fields) in the `search` parameter, the field specifiers in the Lucene query override any fields specified in this parameter. |
| `queryType` | `Edm.String` | `'simple'` or `'full'`; defaults to `'simple'`. Specifies what query language was used in the `search` parameter. |
| `searchMode` | `Edm.String` | `'any'` or `'all'`, defaults to `'any'`. Indicates whether any or all of the search terms in the `search` parameter must be matched in order to count the document as a match. When you use the [Lucene Boolean operators](query-lucene-syntax.md#bkmk_boolean) in the `search` parameter, they take precedence over this parameter. |

All the above parameters are equivalent to the corresponding [search request parameters in the Search API](/rest/api/searchservice/documents/search-post).

The `search.ismatch` function returns a value of type `Edm.Boolean`, which allows you to compose it with other filter subexpressions using the Boolean [logical operators](search-query-odata-logical-operators.md).

> [!NOTE]
> Azure AI Search doesn't support using `search.ismatch` or `search.ismatchscoring` inside lambda expressions. This means it isn't possible to write filters over collections of objects that can correlate full-text search matches with strict filter matches on the same object. For more information on this limitation as well as examples, see [Troubleshooting collection filters in Azure AI Search](search-query-troubleshoot-collection-filters.md). For more in-depth information on why this limitation exists, see [Understanding collection filters in Azure AI Search](search-query-understand-collection-filters.md).

### search.ismatchscoring

The `search.ismatchscoring` function, like the `search.ismatch` function, returns `true` for documents that match the full-text search query passed as a parameter. The difference between them is that the relevance score of documents matching the `search.ismatchscoring` query contributes to the overall document score, whereas for `search.ismatch`, the document score doesn't change. The following overloads of this function are available with parameters identical to those of `search.ismatch`:

- `search.ismatchscoring(search)`
- `search.ismatchscoring(search, searchFields)`
- `search.ismatchscoring(search, searchFields, queryType, searchMode)`

Both the `search.ismatch` and `search.ismatchscoring` functions can be used in the same filter expression.

## Examples

Find documents with the word "waterfront". This filter query is identical to a [search request](/rest/api/searchservice/documents/search-post) with `search=waterfront`.

```odata-filter-expr
    search.ismatchscoring('waterfront')
```

Here's the full query syntax for this request, which you can run in Search Explorer in the Azure portal. Output consists of matches on waterfront, water, and front.

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description",
  "searchMode": "all",
  "queryType": "simple",
  "count": true,
  "filter": "search.ismatchscoring('waterfront')"
}
```

Find documents with the word "pool" and rating greater or equal to 4, or documents with the word "motel" and equal to 3.2. Note, this request couldn't be expressed without the `search.ismatchscoring` function.

```odata-filter-expr
    search.ismatchscoring('pool') and Rating ge 4 or search.ismatchscoring('motel') and Rating eq 3.2
```

Here's the full query syntax for this request for Search Explorer. Output consists of matches on hotels with pools having a rating greater than 4, *or* motels with a rating equal to 3.2.

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description, Tags, Rating",
  "searchMode": "all",
  "queryType": "simple",
  "count": true,
  "filter": "search.ismatchscoring('pool') and Rating ge 4 or search.ismatchscoring('motel') and Rating eq 3.2"
}
```

Find documents without the word "luxury".

```odata-filter-expr
    not search.ismatch('luxury')
```

Here's the full query syntax for this request. Output consists of matches on the term luxury.

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description, Tags, Rating",
  "searchMode": "all",
  "queryType": "simple",
  "count": true,
  "filter": "not search.ismatch('luxury')"
}
```

Find documents with the phrase "ocean" or rating equal to 3.2. The `search.ismatchscoring` query is executed only against fields `HotelName` and `Description`.

Here's the full query syntax for this request. Documents that match only the second clause of the disjunction are returned too (specifically, hotels with `Rating` equal to `3.2`). To make it clear that those documents didn't match any of the scored parts of the expression, they're returned with score equal to zero.

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description, Rating",
  "searchMode": "all",
  "queryType": "full",
  "count": true,
  "filter": "search.ismatchscoring('ocean', 'Description,HotelName') or Rating eq 3.2"
}
```

Output consists of 4 matches: hotels that mention "ocean" in the Description or Hotel Name, or hotels with a rating of 3.2. Notice the search score of zero for matches on the second clause.

```json
{
  "@odata.count": 4,
  "value": [
    {
      "@search.score": 1.6076145,
      "HotelId": "18",
      "HotelName": "Ocean Water Resort & Spa",
      "Description": "New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.",
      "Rating": 4.2
    },
    {
      "@search.score": 1.0594962,
      "HotelId": "41",
      "HotelName": "Windy Ocean Motel",
      "Description": "Oceanfront hotel overlooking the beach features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away.",
      "Rating": 3.5
    },
    {
      "@search.score": 0,
      "HotelId": "40",
      "HotelName": "Trails End Motel",
      "Description": "Only 8 miles from Downtown. On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, All non-smoking hotel. Only 15 miles from airport.",
      "Rating": 3.2
    },
    {
      "@search.score": 0,
      "HotelId": "26",
      "HotelName": "Planetary Plaza & Suites",
      "Description": "Extend Your Stay. Affordable home away from home, with amenities like free Wi-Fi, full kitchen, and convenient laundry service.",
      "Rating": 3.2
    }
  ]
}
```

Find documents where the terms "hotel" and "airport" are within 5 words from each other in the description of the hotel, and where smoking isn't allowed in at least some of the rooms.

```odata-filter-expr
    search.ismatch('"hotel airport"~5', 'Description', 'full', 'any') and Rooms/any(room: not room/SmokingAllowed)
```

Here's the full query syntax. To run in Search Explorer, escape the interior quotation marks with a backslash character.

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description, Tags, Rating",
  "searchMode": "all",
  "queryType": "simple",
  "count": true,
  "filter": "search.ismatch('\"hotel airport\"~5', 'Description', 'full', 'any') and Rooms/any(room: not room/SmokingAllowed)"
}
```

Output consists of a single document where the terms "hotel" and "airport" are within 5 words distance. Smoking is allowed for several rooms in most hotels, including the one in this search result.

```json
{
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 1,
      "HotelId": "40",
      "HotelName": "Trails End Motel",
      "Description": "Only 8 miles from Downtown. On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, All non-smoking hotel. Only 15 miles from airport.",
      "Tags": [
        "bar",
        "free wifi",
        "restaurant"
      ],
      "Rating": 3.2
    }
  ]
}
```

Find documents that have a word that starts with the letters "lux" in the Description field. This query uses [prefix search](query-simple-syntax.md#prefix-queries) in combination with `search.ismatch`.

```odata-filter-expr
    search.ismatch('lux*', 'Description')
```

Here's a full query:

```json
{
  "search": "*",
  "select": "HotelId, HotelName, Description, Tags, Rating",
  "searchMode": "all",
  "queryType": "simple",
  "count": true,
  "filter": "search.ismatch('lux*', 'Description')"
}
```

Output consists of the following matches.

```json
{
  "@odata.count": 4,
  "value": [
    {
      "@search.score": 1,
      "HotelId": "18",
      "HotelName": "Ocean Water Resort & Spa",
      "Description": "New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.",
      "Tags": [
        "view",
        "pool",
        "restaurant"
      ],
      "Rating": 4.2
    },
    {
      "@search.score": 1,
      "HotelId": "13",
      "HotelName": "Luxury Lion Resort",
      "Description": "Unmatched Luxury. Visit our downtown hotel to indulge in luxury accommodations. Moments from the stadium and transportation hubs, we feature the best in convenience and comfort.",
      "Tags": [
        "bar",
        "concierge",
        "restaurant"
      ],
      "Rating": 4.1
    },
    {
      "@search.score": 1,
      "HotelId": "16",
      "HotelName": "Double Sanctuary Resort",
      "Description": "5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room.",
      "Tags": [
        "view",
        "pool",
        "restaurant",
        "bar",
        "continental breakfast"
      ],
      "Rating": 4.2
    },
    {
      "@search.score": 1,
      "HotelId": "14",
      "HotelName": "Twin Vortex Hotel",
      "Description": "New experience in the making. Be the first to experience the luxury of the Twin Vortex. Reserve one of our newly-renovated guest rooms today.",
      "Tags": [
        "bar",
        "restaurant",
        "concierge"
      ],
      "Rating": 4.4
    }
  ]
}
```

## Next steps  

- [Filters in Azure AI Search](search-filters.md)
- [OData expression language overview for Azure AI Search](query-odata-filter-orderby-syntax.md)
- [OData expression syntax reference for Azure AI Search](search-query-odata-syntax-reference.md)
- [Search Documents &#40;Azure AI Search REST API&#41;](/rest/api/searchservice/documents/search-post)
