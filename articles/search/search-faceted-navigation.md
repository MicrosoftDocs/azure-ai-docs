---
title: Add a faceted navigation category hierarchy
titleSuffix: Azure AI Search
description: Add faceted navigation for self-directed filtering in applications that integrate with Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 02/26/2025
---

# Add faceted navigation to a search app

Faceted navigation is used for self-directed drill-down filtering on query results in a search app, where your application offers form controls for scoping search to groups of documents (for example, categories or brands), and Azure AI Search provides the data structures and filters to back the experience.

In this article, learn how to return a faceted navigation structure in Azure AI Search.

## Faceted navigation in a search page

Facets are dynamic and returned on a query. A search response brings with it all of the facet categories used to navigate the documents in the result. The query executes first, and then facets are pulled from the current results and assembled into a faceted navigation structure.

In Azure AI Search, facets are one layer deep and can't be hierarchical. If you aren't familiar with faceted navigation structures, the following example shows one on the left. Counts indicate the number of matches for each facet. The same document can be represented in multiple facets.

:::image source="media/search-faceted-navigation/azure-search-facet-nav.png" alt-text="Screenshot of faceted search results.":::

Facets can help you find what you're looking for, while ensuring that you don't get zero results. As a developer, facets let you expose the most useful search criteria for navigating your search index.

## Faceted navigation in code

Facets are enabled on supported fields in an index, and then specified on a query. At query time, a faceted navigation structure is returned at the top of the response.

The following REST example is an unqualified query (`"search": "*"`) that is scoped to the entire index (see the [built-in hotels sample](search-get-started-portal.md)). It returns a faceted navigation structure for the "Category" field.

```http
POST https://{{service_name}}.search.windows.net/indexes/hotels/docs/search?api-version={{api_version}}
{
    "search": "*",
    "queryType": "simple",
    "select": "",
    "searchFields": "",
    "filter": "",
    "facets": [ "Category"], 
    "orderby": "",
    "count": true
}
```

The response for the example includes the faceted navigation structure at the top. The structure consists of "Category" values and a count of the hotels for each one. It's followed by the rest of the search results, trimmed here to just one document for brevity. This example works well for several reasons. The number of facets for this field fall under the limit (default is 10) so all of them appear, and every hotel in the index of 50 hotels is represented in exactly one of these categories.

```json
{
    "@odata.context": "https://demo-search-svc.search.windows.net/indexes('hotels')/$metadata#docs(*)",
    "@odata.count": 50,
    "@search.facets": {
        "Category": [
            {
                "count": 13,
                "value": "Budget"
            },
            {
                "count": 12,
                "value": "Resort and Spa"
            },
            {
                "count": 9,
                "value": "Luxury"
            },
            {
                "count": 7,
                "value": "Boutique"
            },
            {
                "count": 5,
                "value": "Suite"
            },
            {
                "count": 4,
                "value": "Extended-Stay"
            }
        ]
    },
    "value": [
        {
            "@search.score": 1.0,
            "HotelId": "1",
            "HotelName": "Stay-Kay City Hotel",
            "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
            "Category": "Boutique",
            "Tags": [
                "pool",
                "air conditioning",
                "concierge"
            ],
            "ParkingIncluded": false,
        }
    ]
}
```

## Enable facets on fields

During [index creation or update](search-how-to-create-search-index.md), facets are enabled when you set `"facetable": true` on new fields that you add to an index. Although it's not strictly required, it's a best practice to also set the "filterable" attribute so that you can build the necessary filters that back the faceted navigation experience in your search application.

Here's a JSON example of the hotels sample index, showing "facetable" and "filterable" on low cardinality fields that contain single values or short phrases: "Category", "Tags", "Rating".

```json
{
  "name": "hotels",  
  "fields": [
    { "name": "hotelId", "type": "Edm.String", "key": true, "searchable": false, "sortable": false, "facetable": false },
    { "name": "Description", "type": "Edm.String", "filterable": false, "sortable": false, "facetable": false },
    { "name": "HotelName", "type": "Edm.String", "facetable": false },
    { "name": "Category", "type": "Edm.String", "filterable": true, "facetable": true },
    { "name": "Tags", "type": "Collection(Edm.String)", "filterable": true, "facetable": true },
    { "name": "Rating", "type": "Edm.Int32", "filterable": true, "facetable": true },
    { "name": "Location", "type": "Edm.GeographyPoint" }
  ]
}
```

### Prerequisites

Add faceting to new fields that contain plain text or numeric content. Supported data types include strings, dates, boolean fields, and numeric fields (but not vectors).

You can't set facets on existing fields, on vector fields, or fields of type `Edm.GeographyPoint` or `Collection(Edm.GeographyPoint)`.

On complex fields, "facetable" must be null.

### Start with new field definitions

Because attribution determines how a field is indexed, many attributes can only be set when fields are created. This restriction applies to facets and filters. If your index already exists and you add a new field definition, existing documents in the index get a null value for the new field. This null value is replaced the next time you [refresh the index](search-howto-reindex.md).

### Choosing which fields to attribute

Facets can be calculated over single-value fields and collections. Fields that work best in faceted navigation have these characteristics:

* Human readable (nonvector) content.

* Low cardinality (a few distinct values that repeat throughout documents in your search corpus).

* Short descriptive values (one or two words) that render nicely in a navigation tree.

The values within a field, and not the field name itself, produce the facets in a faceted navigation structure. If the facet is a string field named *Color*, facets are blue, green, and any other value for that field.

### Defaults in REST and Azure SDKs

If you're using one of the Azure SDKs, your code must explicitly set the "facetable" attribute on a field.

The REST API has defaults for field attributes based on the [data type](/rest/api/searchservice/supported-data-types). The following data types are "filterable" and "facetable" by default:

* `Edm.String` and `Collection(Edm.String)`
* `Edm.DateTimeOffset` and `Collection(Edm.DateTimeOffset)`
* `Edm.Boolean` and`Collection(Edm.Boolean)`
* `Edm.Int32`, `Edm.Int64`, `Edm.Double`, and their collection equivalents

## Return facets in a query

Recall that facets are calculated from results in a query response. You only get facets for documents found by the current query. 

1. Facets are configured at query-time. Use the [Search POST](/rest/api/searchservice/documents/search-post) or [Search GET](/rest/api/searchservice/documents/search-get) request, or an equivalent Azure SDK API, to specify facets. 

1. Set facet query parameters in the request. In Search POST, facets are an array of facet expressions to apply to the search query. Each facet expression contains a field name, optionally followed by a comma-separated list of name:value pairs. Valid facet parameters are `count`, `sort`, `values`, `interval`, and `timeoffset`.

    | Facet parameter | Description and usage |
    |-----------------|-----------------------|
    | `count` | Maximum number of facet terms; default is 10. An example is `Tags,count:5`. There's no upper limit on the number of terms, but higher values degrade performance, especially if the faceted field contains a large number of unique terms. This is due to the way faceting queries are distributed across shards. You can set count to zero or to a value that's greater than or equal to the number of unique values in the facetable field to get an accurate count across all shards. The tradeoff is increased latency.
    | `sort` | Set to "count", "-count", "value", "-value". Use count to sort descending by count. Use -count to sort ascending by count. Use value to sort ascending by value. Use -value to sort descending by value (for example, `"facet=category,count:3,sort:count"` gets the top three categories in facet results in descending order by the number of documents with each city name). If the top three categories are Budget, Motel, and Luxury, and Budget has five hits, Motel has 6, and Luxury has 4, then the buckets are in the order Motel, Budget, Luxury. For -value, `"facet=rating,sort:-value"` produces buckets for all possible ratings, in descending order by value (for example, if the ratings are from 1 to 5, the buckets are ordered 5, 4, 3, 2, 1, irrespective of how many documents match each rating). |
    | `values` | Set to pipe-delimited numeric or `Edm.DateTimeOffset` values specifying a dynamic set of facet entry values. For example, `"facet=baseRate,values:10 \| 20"` produces three buckets: one for base rate 0 up to but not including 10, one for 10 up to but not including 20, and one for 20 and higher. A string "`facet=lastRenovationDate,values:2010-02-01T00:00:00Z"` produces two buckets: one for hotels renovated before February 2010, and one for hotels renovated February 1, 2010 or later. The values must be listed in sequential, ascending order to get the expected results. |
    | interval| An integer interval greater than zero for numbers, or minute, hour, day, week, month, quarter, year for date time values. For example, `"facet=baseRate,interval:100"` produces buckets based on base rate ranges of size 100. If base rates are all between $60 and $600, there are buckets for 0-100, 100-200, 200-300, 300-400, 400-500, and 500-600. The string `"facet=lastRenovationDate,interval:year"` produces one bucket for each year when hotels were renovated. |
    | `timeoffset` | Can be set to ([+-]hh:mm, [+-]hhmm, or [+-]hh). If used, the timeoffset parameter must be combined with the interval option, and only when applied to a field of type Edm.DateTimeOffset. The value specifies the UTC time offset to account for in setting time boundaries. For example: `"facet=lastRenovationDate,interval:day,timeoffset:-01:00"` uses the day boundary that starts at 01:00:00 UTC (midnight in the target time zone).

`count` and `sort` can be combined in the same facet specification, but they can't be combined with interval or values, and interval and values can't be combined together.

Interval facets on date time are computed based on the UTC time if `timeoffset` isn't specified. For example: for "facet=lastRenovationDate,interval:day", the day boundary starts at 00:00:00 UTC.

### Basic facet example

The following example works against the [hotels sample index](search-get-started-portal.md). You can use **JSON view** in Search Explorer to paste in the JSON query. This example shows three facets for "Category", "Tags", and "Rating", with a count override on "Tags" and a range override for "Rating", which is otherwise stored as a double in the index.

```http
POST https://{{service_name}}.search.windows.net/indexes/hotels/docs/search?api-version={{api_version}}
{
    "search": "*",
    "facets": [ 
        "Category", 
        "Tags,count:5", 
        "Rating,values:1|2|3|4|5"
    ],
    "count": true
}
```

For each faceted navigation tree, there's a default limit of the top 10 facet instances found by the query. This default makes sense for navigation structures because it keeps the values list to a manageable size. You can override the default by assigning a value to "count". For example, `"Tags,count:5"` reduces the number of tags under the Tags section to the top five.

For Numeric and DateTime values only, you can explicitly set values on the facet field (for example, `facet=Rating,values:1|2|3|4|5`) to separate results into contiguous ranges (either ranges based on numeric values or time periods). Alternatively, you can add "interval", as in `facet=Rating,interval:1`. 

Each range is built using 0 as a starting point, a value from the list as an endpoint, and then trimmed of the previous range to create discrete intervals.

### Distinct values example

You can formulate a query that returns a distinct value count for each "facetable" field. This example formulates a query that sets `top` to zero, returning just the counts, with no results.

For brevity, it includes just two fields marked as "facetable" in the hotels sample index.

```http
POST https://{{service_name}}.search.windows.net/indexes/hotels/docs/search?api-version={{api_version}}
{
    "search": "*",
    "count": true,
    "top": 0,
    "facets": [ 
        "Category", "Address/StateProvince""
    ]
}
```

Results from this query are as follows:

```json
{
  "@odata.count": 50,
  "@search.facets": {
    "Address/StateProvince": [
      {
        "count": 9,
        "value": "WA"
      },
      {
        "count": 6,
        "value": "CA "
      },
      {
        "count": 4,
        "value": "FL"
      },
      {
        "count": 3,
        "value": "NY"
      },
      {
        "count": 3,
        "value": "OR"
      },
      {
        "count": 3,
        "value": "TX"
      },
      {
        "count": 2,
        "value": "GA"
      },
      {
        "count": 2,
        "value": "MA"
      },
      {
        "count": 2,
        "value": "TN"
      },
      {
        "count": 1,
        "value": "AZ"
      }
    ],
    "Category": [
      {
        "count": 13,
        "value": "Budget"
      },
      {
        "count": 12,
        "value": "Suite"
      },
      {
        "count": 7,
        "value": "Boutique"
      },
      {
        "count": 7,
        "value": "Resort and Spa"
      },
      {
        "count": 6,
        "value": "Extended-Stay"
      },
      {
        "count": 5,
        "value": "Luxury"
      }
    ]
  },
  "value": []
}
```

## Best practices for working with facets

This section is a collection of tips and workarounds that are helpful for application development.

### Initialize a faceted navigation structure

It's useful to initialize a search page with an open query (`"search": "*"`) to completely fill in the faceted navigation structure. As soon as you pass query terms in the request, the faceted navigation structure is scoped to just the matches in the results, rather than the entire index.

### Clear facets

When you design the user experience, remember to add a mechanism for clearing facets. A common approach for clearing facets is issuing an open query to reset the page.

### Disable faceting to save on storage and improve performance

For performance and storage optimization, set `"facetable": false` for fields that should never be used as a facet. Examples include string fields for unique values, such as an ID or product name, to prevent their accidental (and ineffective) use in faceted navigation. This best practice is especially important for the REST API, which enables filters and facets on string fields by default.

Remember that you can't use `Edm.GeographyPoint` or `Collection(Edm.GeographyPoint)` fields in faceted navigation. Recall that facets work best on fields with low cardinality. Due to how geo-coordinates resolve, it's rare that any two sets of coordinates are equal in a given dataset. As such, facets aren't supported for geo-coordinates. You should use a city or region field to facet by location.

### Check for bad data

As you prepare data for indexing, check fields for null values, misspellings or case discrepancies, and single and plural versions of the same word. By default, filters and facets don't undergo lexical analysis or [spell check](speller-how-to-add.md), which means that all values of a "facetable" field are potential facets, even if the words differ by one character. Optionally, you can [assign a normalizer](search-normalizers.md) to a "filterable" and "facetable" field to smooth out variations in casing and characters.

### Discrepancies in facet counts

Under certain circumstances, you might find that facet counts aren't fully accurate due to the [sharding architecture](index-similarity-and-scoring.md#sharding-effects-on-query-results). Every search index is spread across multiple shards, and each shard reports the top N facets by document count, which are then combined into a single result. Because it's just the top N facets for each shard, it's possible to miss or under-count matching documents in the facet response.

To guarantee accuracy, you can artificially inflate the count:\<number> to a large number to force full reporting from each shard. You can specify `"count": "0"` for unlimited facets. Or, you can set "count" to a value that's greater than or equal to the number of unique values of the faceted field. For example, if you're faceting by a "size" field that has five unique values, you could set `"count:5"` to ensure all matches are represented in the facet response. 

The tradeoff with this workaround is increased query latency, so use it only when necessary.

### Preserve a facet navigation structure asynchronously of filtered results

In Azure AI Search, facets exist for current results only. However, it's a common application requirement to retain a static set of facets so that the user can navigate in reverse, retracing steps to explore alternative paths through search content. 

If you want a static set of facets alongside a dynamic drilldown experience, you can implement it by using two filtered queries: one scoped to the results, the other used to create a static list of facets for navigation purposes.

### Offset large facet counts through filters

Search results and facet results that are too large can be trimmed by [adding filters](search-filters.md). In the following example, in the query for *cloud computing*, 254 items have *internal specification* as a content type. If results are too large, adding filters can help your users refine the query by adding more criteria.

Items aren't mutually exclusive. If an item meets the criteria of both filters, it's counted in each one. This duplication is possible when faceting on `Collection(Edm.String)` fields, which are often used to implement document tagging.

```output
Search term: "cloud computing"
Content type
   Internal specification (254)
   Video (10)
```

## Next steps

We recommend the [C#: Add search to web apps](tutorial-csharp-overview.md) for an example of faceted navigation that includes code for the presentation layer. The sample also includes filters, suggestions, and autocomplete. It uses JavaScript and React for the presentation layer.
