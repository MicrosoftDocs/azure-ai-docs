---
title: Examples of simple syntax
titleSuffix: Azure AI Search
description: Explore query examples that demonstrate the simple syntax for full text search, filter search, and geo search against an Azure AI Search index.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 04/14/2025
ms.update-cycle: 365-days
---

# Examples of *simple* search queries in Azure AI Search

In Azure AI Search, the [simple query syntax](query-simple-syntax.md) invokes the default query parser for full text search. The parser is fast and handles common scenarios, including full text search, filtered and faceted search, and prefix search. This article uses examples to illustrate simple syntax usage in a [Search Documents (REST API)](/rest/api/searchservice/documents/search-post) request.

> [!NOTE]
> An alternative query syntax is [Lucene](query-lucene-syntax.md), which supports more complex query structures, such as fuzzy and wildcard search. For more information, see [Examples of full Lucene search syntax ](search-query-lucene-examples.md).

## Hotels sample index

The following queries are based on the hotels-sample-index, which you can create by following the instructions in [Quickstart: Full-text search in the Azure portal](search-get-started-portal.md).

Example queries are articulated using the REST API and POST requests. You can paste and run them in a [REST client](search-get-started-text.md). Or, use the JSON view of [Search explorer](search-explorer.md) in the Azure portal. In JSON view, you can paste in the query examples shown here in this article.

Request headers must have the following values:

| Key | Value |
|-----|-------|
| Content-Type | application/json|
| api-key  | `<your-search-service-api-key>`, either query or admin key |

URI parameters must include your search service endpoint with the index name, docs collections, search command, and API version, similar to the following example:

```http
https://{{service-name}}.search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
```

The request body should be formed as valid JSON:

```json
{
    "search": "*",
    "queryType": "simple",
    "select": "HotelId, HotelName, Category, Tags, Description",
    "count": true
}
```

+ `search` set to * is an unspecified query, equivalent to null or empty search. It's not especially useful, but it's the simplest search you can do, and it shows all retrievable fields in the index, with all values.

+ `queryType` set to *simple* is the default and can be omitted, but it's included to emphasize that the query examples in this article are expressed in the simple syntax.

+ `select` set to a comma-delimited list of fields is used for search result composition, including just those fields that are useful in the context of search results.

+ `count` returns the number of documents matching the search criteria. On an empty search string, the count is all documents in the index (50 in the hotels-sample-index).

## Example 1: Full text search

Full text search can be any number of standalone terms or quote-enclosed phrases, with or without Boolean operators. 

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "pool spa +airport",
    "searchMode": "any",
    "queryType": "simple",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

A keyword search that's composed of important terms or phrases tend to work best. String fields undergo text analysis during indexing and querying, dropping nonessential words like *the*, *and*, *it*. To see how a query string is tokenized in the index, pass the string in an [Analyze Text](/rest/api/searchservice/indexes/analyze) call to the index.

The `searchMode` parameter controls precision and recall. If you want more recall, use the default *any* value, which returns a result if any part of the query string is matched. If you favor precision, where all parts of the string must be matched, change `searchMode` to *all*. Try the preceding query both ways to see how searchMode changes the outcome.

The response for the *pool spa +airport* query should look similar to the following example.

```json
"@odata.count": 4,
"value": [
{
    "@search.score": 6.090657,
    "HotelId": "12",
    "HotelName": "Winter Panorama Resort",
    "Description": "Plenty of great skiing, outdoor ice skating, sleigh rides, tubing and snow biking. Yoga, group exercise classes and outdoor hockey are available year-round, plus numerous options for shopping as well as great spa services. Newly-renovated with large rooms, free 24-hr airport shuttle & a new restaurant. Rooms/suites offer mini-fridges & 49-inch HDTVs.",
    "Category": "Resort and Spa"
},
{
    "@search.score": 4.314683,
    "HotelId": "21",
    "HotelName": "Good Business Hotel",
    "Description": "1 Mile from the airport. Free WiFi, Outdoor Pool, Complimentary Airport Shuttle, 6 miles from Lake Lanier & 10 miles from downtown. Our business center includes printers, a copy machine, fax, and a work area.",
    "Category": "Suite"
},
{
    "@search.score": 3.575948,
    "HotelId": "27",
    "HotelName": "Starlight Suites",
    "Description": "Complimentary Airport Shuttle & WiFi. Book Now and save - Spacious All Suite Hotel, Indoor Outdoor Pool, Fitness Center, Florida Green certified, Complimentary Coffee, HDTV",
    "Category": "Suite"
},
{
    "@search.score": 2.6926985,
    "HotelId": "25",
    "HotelName": "Waterfront Scottish Inn",
    "Description": "Newly Redesigned Rooms & airport shuttle. Minutes from the airport, enjoy lakeside amenities, a resort-style pool & stylish new guestrooms with Internet TVs.",
    "Category": "Suite"
}
]
```

Notice the search score in the response. This is the relevance score of the match. By default, a search service returns the top 50 matches based on this score.

Uniform scores of *1.0* occur when there's no rank, either because the search wasn't full text search, or because no criteria were provided. For example, in an empty search (search=`*`), rows come back in arbitrary order. When you include actual criteria, you'll see search scores evolve into meaningful values.

## Example 2: Look up by ID

After search results are returned, a logical next step is to provide a details page that includes more fields from the document. This example shows you how to return a single document using [Get Document](/rest/api/searchservice/documents/get) by passing in the document ID.

```http
GET /indexes/hotels-sample-index/docs/41?api-version=2025-09-01
```

All documents have a unique identifier. If you're using the Azure portal, select the index from the **Indexes** tab and then look at the field definitions to determine which field is the key. In the REST API, the [GET Index](/rest/api/searchservice/indexes/get) call returns the index definition in the response body.

The response for the preceding query consists of the document whose key is *41*. Any field that is marked as *retrievable* in the index definition can be returned in search results and rendered in your app.

```json
{
    "HotelId": "41",
    "HotelName": "Windy Ocean Motel",
    "Description": "Oceanfront hotel overlooking the beach features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away.",
    "Description_fr": "Cet hôtel en bord de mer donnant sur la plage propose des chambres dotées d'un balcon privé et de 2 piscines intérieure et extérieure. Inspiré par la beauté naturelle de l'île, chaque chambre comprend une peinture originale de scènes locales par le propriétaire. Les chambres comprennent un mini-réfrigérateur, une cafetière Keurig et une télévision à écran plat. Divers magasins et divertissements artistiques se trouvent sur la promenade, à quelques pas.",
    "Category": "Suite",
    "Tags": [
    "pool",
    "air conditioning",
    "bar"
    ],
    "ParkingIncluded": true,
    "LastRenovationDate": "2021-05-10T00:00:00Z",
    "Rating": 3.5,
    "Location": {
    "type": "Point",
    "coordinates": [
        -157.846817,
        21.295841
    ],
    "crs": {
        "type": "name",
        "properties": {
        "name": "EPSG:4326"
        }
    }
    },
    "Address": {
    "StreetAddress": "1450 Ala Moana Blvd 2238 Ala Moana Ctr",
    "City": "Honolulu",
    "StateProvince": "HI",
    "PostalCode": "96814",
    "Country": "USA"
    }
}
```

## Example 3: Filter on text

[Filter syntax](search-query-odata-filter.md) is an OData expression that you can use by itself or with `search`. When used together in the same request, `filter` is applied first to the entire index, and then the `search` is performed on the results of the filter. Filters can therefore be a useful technique to improve query performance since they reduce the set of documents that the search query needs to process.

Filters can be defined on any field marked as `filterable` in the index definition. For hotels-sample-index, filterable fields include *Category*, *Tags*, *ParkingIncluded*, *Rating*, and most *Address* fields.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "art tours",
    "queryType": "simple",
    "filter": "Category eq 'Boutique'",
    "searchFields": "HotelName,Description,Category",
    "select": "HotelId,HotelName,Description,Category",
    "count": true
}
```

The response for the preceding query is scoped to only those hotels categorized as *Boutique*, and that include the terms *art* or *tours*. In this case, there's just one match.

```json
"value": [
{
    "@search.score": 1.2814453,
    "HotelId": "2",
    "HotelName": "Old Century Hotel",
    "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
    "Category": "Boutique"
}
]
```

## Example 4: Filter functions

Filter expressions can include [search.ismatch and search.ismatchscoring functions](search-query-odata-full-text-search-functions.md), allowing you to build a search query within the filter. This filter expression uses a wildcard on *free* to select amenities including free wifi, free parking, and so forth.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
  {
    "search": "",
    "filter": "search.ismatch('free*', 'Tags', 'full', 'any')",
    "select": "HotelName, Tags, Description",
    "count": true
  }
```

The response for the preceding query matches on 27 hotels that offer free amenities. Notice that the search score is a uniform *1* throughout the results. This is because the search expression is null or empty, resulting in verbatim filter matches, but no full text search. Relevance scores are only returned on full text search. If you're using filters without `search`, make sure you have sufficient sortable fields so that you can control search rank.

```json
  "@odata.count": 27,
  "value": [
    {
      "@search.score": 1,
      "HotelName": "Country Residence Hotel",
      "Description": "All of the suites feature full-sized kitchens stocked with cookware, separate living and sleeping areas and sofa beds. Some of the larger rooms have fireplaces and patios or balconies. Experience real country hospitality in the heart of bustling Nashville. The most vibrant music scene in the world is just outside your front door.",
      "Tags": [
        "laundry service",
        "restaurant",
        "free parking"
      ]
    },
    {
      "@search.score": 1,
      "HotelName": "Downtown Mix Hotel",
      "Description": "Mix and mingle in the heart of the city. Shop and dine, mix and mingle in the heart of downtown, where fab lake views unite with a cheeky design.",
      "Tags": [
        "air conditioning",
        "laundry service",
        "free wifi"
      ]
    },
    {
      "@search.score": 1,
      "HotelName": "Starlight Suites",
      "Description": "Complimentary Airport Shuttle & WiFi. Book Now and save - Spacious All Suite Hotel, Indoor Outdoor Pool, Fitness Center, Florida Green certified, Complimentary Coffee, HDTV",
      "Tags": [
        "pool",
        "coffee in lobby",
        "free wifi"
      ]
    },
. . .
```

## Example 5: Range filters

Range filtering is supported through filters expressions for any data type. The following examples illustrate numeric and string ranges. Data types are important in range filters and work best when numeric data is in numeric fields, and string data in string fields. Numeric data in string fields isn't suitable for ranges because numeric strings aren't comparable.

The following query is a numeric range. In hotels-sample-index, the only filterable numeric field is `Rating`.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "*",
    "filter": "Rating ge 2 and Rating lt 4",
    "select": "HotelId, HotelName, Rating",
    "orderby": "Rating desc",
    "count": true
}
```

The response for this query should look similar to the following example, trimmed for brevity.

```json
"@odata.count": 27,
"value": [
{
    "@search.score": 1,
    "HotelId": "22",
    "HotelName": "Lion's Den Inn",
    "Rating": 3.9
},
{
    "@search.score": 1,
    "HotelId": "25",
    "HotelName": "Waterfront Scottish Inn",
    "Rating": 3.8
},
{
    "@search.score": 1,
    "HotelId": "2",
    "HotelName": "Old Century Hotel",
    "Rating": 3.6
},
...
```

The next query is a range filter over a string field (Address/StateProvince):

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "*",
    "filter": "Address/StateProvince ge 'A*' and Address/StateProvince lt 'D*'",
    "select": "HotelId, HotelName, Address/StateProvince",
    "count": true
}
```

The response for this query should look similar to the following example, trimmed for brevity. In this example, it's not possible to sort by `StateProvince` because the field isn't attributed as *sortable* in the index definition.

```json
{
  "@odata.count": 9,
  "value": [
    {
      "@search.score": 1,
      "HotelId": "39",
      "HotelName": "White Mountain Lodge & Suites",
      "Address": {
        "StateProvince": "CO"
      }
    },
    {
      "@search.score": 1,
      "HotelId": "9",
      "HotelName": "Smile Up Hotel",
      "Address": {
        "StateProvince": "CA "
      }
    },
    {
      "@search.score": 1,
      "HotelId": "7",
      "HotelName": "Roach Motel",
      "Address": {
        "StateProvince": "CA "
      }
    },
    {
      "@search.score": 1,
      "HotelId": "34",
      "HotelName": "Lakefront Captain Inn",
      "Address": {
        "StateProvince": "CT"
      }
    },
    {
      "@search.score": 1,
      "HotelId": "37",
      "HotelName": "Campus Commander Hotel",
      "Address": {
        "StateProvince": "CA "
      }
    },
. . . 
```

## Example 6: Geospatial search

The hotels-sample-index includes a *Location* field with latitude and longitude coordinates. This example uses the [geo.distance function](search-query-odata-geo-spatial-functions.md#examples) that filters on documents within the circumference of a starting point, out to an arbitrary distance (in kilometers) that you provide. You can adjust the last value in the query (10) to reduce or enlarge the surface area of the query.

```http
POST /indexes/v/docs/search?api-version=2025-09-01
{
    "search": "*",
    "filter": "geo.distance(Location, geography'POINT(-122.335114 47.612839)') le 10",
    "select": "HotelId, HotelName, Address/City, Address/StateProvince",
    "count": true
}
```

The response for this query returns all hotels within a 10-kilometer distance of the coordinates provided:

```json
{
  "@odata.count": 3,
  "value": [
    {
      "@search.score": 1,
      "HotelId": "45",
      "HotelName": "Happy Lake Resort & Restaurant",
      "Address": {
        "City": "Seattle",
        "StateProvince": "WA"
      }
    },
    {
      "@search.score": 1,
      "HotelId": "24",
      "HotelName": "Uptown Chic Hotel",
      "Address": {
        "City": "Seattle",
        "StateProvince": "WA"
      }
    },
    {
      "@search.score": 1,
      "HotelId": "16",
      "HotelName": "Double Sanctuary Resort",
      "Address": {
        "City": "Seattle",
        "StateProvince": "WA"
      }
    }
  ]
}
```

## Example 7: Booleans with searchMode

Simple syntax supports Boolean operators in the form of characters (`+, -, |`) to support AND, OR, and NOT query logic. Boolean search behaves as you might expect, with a few noteworthy exceptions. 

In a Boolean search, consider adding the `searchMode` parameter as a mechanism for influencing precision and recall. Valid values include `"searchMode": "any"` favoring recall (a document that satisfies any of the criteria is considered a match), and `"searchMode": "all"` favoring precision (all criteria must be matched in a document). 

In the context of a Boolean search, the default `"searchMode": "any"` can be confusing if you're stacking a query with multiple operators and getting broader instead of narrower results. This is particularly true with NOT, where results include all documents *not containing* a specific term or phrase.

The following example provides an illustration. The query looks for matches on *restaurant* that exclude the phrase *air conditioning*. If you run the following query with searchMode (any), 43 documents are returned: those containing the term *restaurant*, plus all documents that *don't* have the phrase *air conditioning. 

Notice that there's no space between the boolean operator (`-`) and the phrase *air conditioning*. The quotation marks are escaped (`\"`).

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "restaurant -\"air conditioning\"",
    "searchMode": "any",
    "searchFields": "Tags",
    "select": "HotelId, HotelName, Tags",
    "count": true
}
```

Changing to `"searchMode": "all"` enforces a cumulative effect on criteria and returns a smaller result set (seven matches) consisting of documents containing the term *restaurant*, minus those containing the phrase *air conditioning*.

The response for this query would now look similar to the following example, trimmed for brevity.

```json
{
  "@odata.count": 14,
  "value": [
    {
      "@search.score": 3.1383743,
      "HotelId": "18",
      "HotelName": "Ocean Water Resort & Spa",
      "Tags": [
        "view",
        "pool",
        "restaurant"
      ]
    },
    {
      "@search.score": 2.028083,
      "HotelId": "22",
      "HotelName": "Lion's Den Inn",
      "Tags": [
        "laundry service",
        "free wifi",
        "restaurant"
      ]
    },
    {
      "@search.score": 2.028083,
      "HotelId": "34",
      "HotelName": "Lakefront Captain Inn",
      "Tags": [
        "restaurant",
        "laundry service",
        "coffee in lobby"
      ]
    },
...
```

## Example 8: Paging results

In previous examples, you learned about parameters that affect search results composition, including `select` that determines which fields are in a result, sort orders, and how to include a count of all matches. This example is a continuation of search result composition in the form of paging parameters that allow you to batch the number of results that appear in any given page. 

By default, a search service returns the top 50 matches. To control the number of matches in each page, use `top` to define the size of the batch, and then use `skip` to pick up subsequent batches.

The following example uses a filter and sort order on the `Rating` field (Rating is both filterable and sortable) because it's easier to see the effects of paging on sorted results. In a regular full search query, the top matches are ranked and paged by `@search.score`.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "*",
    "filter": "Rating gt 4",
    "select": "HotelName, Rating",
    "orderby": "Rating desc",
    "top": 5,
    "count": true
}
```

The query finds 21 matching documents, but because you specified `top`, the response returns just the top five matches, with ratings starting at 4.9, and ending at 4.7 with *Lakeside B & B*. 

To get the next five, skip the first batch:

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "*",
    "filter": "Rating gt 4",
    "select": "HotelName, Rating",
    "orderby": "Rating desc",
    "top": 5,
    "skip": 5,
    "count": true
}
```

The response for the second batch skips the first five matches, returning the next five, starting with *Pull'r Inn Motel*. To continue with more batches, you would keep `top` at five, and then increment `skip` by five on each new request (skip=5, skip=10, skip=15, and so forth).

```json
{
  "@odata.count": 21,
  "value": [
    {
      "@search.score": 1,
      "HotelName": "Head Wind Resort",
      "Rating": 4.7
    },
    {
      "@search.score": 1,
      "HotelName": "Sublime Palace Hotel",
      "Rating": 4.6
    },
    {
      "@search.score": 1,
      "HotelName": "City Skyline Antiquity Hotel",
      "Rating": 4.5
    },
    {
      "@search.score": 1,
      "HotelName": "Nordick's Valley Motel",
      "Rating": 4.5
    },
    {
      "@search.score": 1,
      "HotelName": "Winter Panorama Resort",
      "Rating": 4.5
    }
  ]
}
```

## Related content

Now that you have some practice with the basic query syntax, try specifying queries in code. The following link covers how to set up search queries using the Azure SDKs.

+ [Quickstart: Full-text search](search-get-started-text.md)

More syntax reference, query architecture, and examples can be found in the following links:

+ [Examples of full Lucene search syntax](search-query-lucene-examples.md)
+ [Full text search in Azure AI Search](search-lucene-query-architecture.md)
+ [Simple query syntax in Azure AI Search](query-simple-syntax.md)
+ [Lucene query syntax in Azure AI Search](query-lucene-syntax.md)
+ [OData $filter syntax in Azure AI Search](search-query-odata-filter.md)
