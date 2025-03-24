---
title: Add a faceted navigation category hierarchy
titleSuffix: Azure AI Search
description: Add faceted navigation for self-directed navigation in applications that integrate with Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 03/21/2025
---

# Add faceted navigation to a search app

Faceted navigation is used for self-directed filtering on query results in a search app, where your application offers form controls for scoping search to groups of documents (for example, categories or brands), and Azure AI Search provides the data structures and filters to back the experience.

In this article, learn the steps for returning a faceted navigation structure in Azure AI Search. Once you're familiar with basic concepts and clients, continue to [Facet examples](#return-facets-in-a-query) for syntax about various use cases, including basic faceting and distinct counts. The following facet capabilities are available through preview APIs: hierarchical facet structures, facet filtering, and facet aggregations.

## Faceted navigation in a search page

Facets are dynamic and returned on a query. A search response brings with it all of the facet categories used to navigate the documents in the result. The query executes first, and then facets are pulled from the current results and assembled into a faceted navigation structure.

In Azure AI Search, facets are one layer deep and can't be hierarchical unless you use the preview API. If you aren't familiar with faceted navigation structures, the following example shows one on the left. Counts indicate the number of matches for each facet. The same document can be represented in multiple facets.

:::image source="media/search-faceted-navigation/azure-search-facet-nav.png" alt-text="Screenshot of faceted search results.":::

Facets can help you find what you're looking for, while ensuring that you don't get zero results. As a developer, facets let you expose the most useful search criteria for navigating your search index.

## Faceted navigation in code

Facets are enabled on supported fields in an index, and then specified on a query. At query time, a dynamic faceted navigation structure is returned at the top of the response.

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

You can add facets to new fields that contain plain text or numeric content. Supported data types include strings, dates, boolean fields, and numeric fields (but not vectors).

You can use the Azure portal, REST APIs, Azure SDKs or any method that supports the creation or update of index schemas in Azure AI Search. As a first step, identify which fields to use for faceting.

### Choose which fields to attribute

Facets can be calculated over single-value fields and collections. Fields that work best in faceted navigation have these characteristics:

* Human readable (nonvector) content.
* Low cardinality (a few distinct values that repeat throughout documents in your search corpus).
* Short descriptive values (one or two words) that render nicely in a navigation tree.

The values within a field, and not the field name itself, produce the facets in a faceted navigation structure. If the facet is a string field named *Color*, facets are blue, green, and any other value for that field. As a best practice, review field values to ensure there are no typos, nulls, or casing differences. Consider [assigning a normalizer](search-normalizers.md) to a "filterable" and "facetable" field to smooth out minor variations in the text.

You can't set facets on existing fields, on vector fields, or fields of type `Edm.GeographyPoint` or `Collection(Edm.GeographyPoint)`.

On complex field collections, "facetable" must be null. 

### Start with new field definitions

Attributes that affect how a field is indexed can only be set when fields are created. This restriction applies to facets and filters. 

If your index already exists, you can add a new field definition that provides facets. Existing documents in the index get a null value for the new field. This null value is replaced the next time you [refresh the index](search-howto-reindex.md).

#### [**Azure portal**](#tab/portal-facet)

1. In the search services page of the [Azure portal](https://portal.azure.com), go to the **Fields** tab of the index and select **Add field**.

1. Provide a name, data type, and attributes. We recommend adding filterable because it's common to set filters based on a facet category in the response. We recommend sortable because filters produce unordered results, and you might want to sort them in your application.

   You can also set searchable if you also want to support full text search on the field, and retrievable if you want to include the field in the search response.

   :::image type="content" source="media/search-faceted-navigation/portal-add-facetable-field.png" alt-text="Screenshot of the Add fields page in the Azure portal." border="true" lightbox="media/search-faceted-navigation/portal-add-facetable-field.png":::

1. Save the field definition.

#### [**REST**](#tab/rest-facet)

When you define an index schema, facets are enabled when you set `"facetable": true` on new fields that you add to an index. Although it's not strictly required, it's a best practice to also set the "filterable" attribute so that you can build the necessary filters that back the faceted navigation experience in your search application.

Start with [Create or Update Index](search-how-to-create-search-index.md) request and specify the fields collection.

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

#### Defaults in REST

Both the Azure portal and the REST API have defaults for field attributes based on the [data type](/rest/api/searchservice/supported-data-types). The following data types are "filterable" and "facetable" by default:

* `Edm.String` and `Collection(Edm.String)`
* `Edm.DateTimeOffset` and `Collection(Edm.DateTimeOffset)`
* `Edm.Boolean` and`Collection(Edm.Boolean)`
* `Edm.Int32`, `Edm.Int64`, `Edm.Double`, and their collection equivalents

#### [**Azure SDKs**](#tab/sdk-facet)

If you're using one of the Azure SDKs, your code must explicitly set facetable on a field.

Assign the facet property to fields using APIs that create or update an index.

* [Azure SDK for .NET: SearchIndex.Fields Property](/dotnet/api/azure.search.documents.indexes.models.searchindex.fields)
* [Azure SDK for Python: SearchField Class](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchfield)
* [Azure SDK for Java: SearchField Class](/java/api/com.azure.search.documents.indexes.models.searchfield)
* [Azure SDK for JavaScript: Simple Field interface](/javascript/api/@azure/search-documents/simplefield)

---

## Return facets in a query

Recall that facets are dynamically calculated from results in a query response. You only get facets for documents found by the current query.

This section provides query syntax. It also includes the following examples:

* [Basic examples](#basic-facet-example)
* [Distinct values  example](#distinct-values-example)
* [Facet hierarchy example (preview)](#facet-hierarchy-example)
* [Facet filtering example (preview)](#facet-filtering-example)
* [Facet aggregations example (preview)]()

#### [**Azure portal**](#tab/portal-facet-response)

Use JSON view in Search Explorer to set facet parameters in the [Azure portal](https://portal.azure.com).

1. Select an index and open Search Explorer in JSON View.
1. Provide a query in JSON. You can type it out, copy the JSON from a REST example, or use intellisense to help with syntax. Refer to the REST example in the next tab for reference on facet expressions.
1. Select **Search** to return faceted results, articulated in JSON.

Here's a screenshot of the [basic facet query example](#basic-facet-example) on the [hotels sample index](search-get-started-portal.md). You can paste in other examples in this article to return the results in Search Explorer.

:::image type="content" source="media/search-faceted-navigation/portal-facet-query.png" alt-text="Screenshot of the Search Explorer page in the Azure portal." border="true" lightbox="media/search-faceted-navigation/portal-facet-query.png":::

#### [**REST**](#tab/rest-facet-response)

1. Facets are configured at query-time. Use the [Search POST](/rest/api/searchservice/documents/search-post) or [Search GET](/rest/api/searchservice/documents/search-get) request, or an equivalent Azure SDK API, to specify facets. 

1. Set facet query parameters in the request. In Search POST, `facets` are an array of facet expressions to apply to the search query. Each facet expression contains a field name, optionally followed by a comma-separated list of name-value pairs. Valid facet parameters are `count`, `sort`, `values`, `interval`, and `timeoffset`.

    | Facet parameter | Description and usage |
    |-----------------|-----------------------|
    | `count` | Maximum number of facet terms per structure; default is 10. An example is `Tags,count:5`. There's no upper limit on the number of terms, but higher values degrade performance, especially if the faceted field contains a large number of unique terms. This is due to the way faceting queries are distributed across shards. You can set count to zero or to a value that's greater than or equal to the number of unique values in the "facetable" field to get an accurate count across all shards. The tradeoff is increased latency.
    | `sort` | Set to `count`, `-count`, `value`, `-value`. Use `count` to sort descending by count. Use `-count` to sort ascending by count. Use `value` to sort ascending by value. Use `-value` to sort descending by value (for example, `"facet=category,count:3,sort:count"` gets the top three categories in facet results in descending order by the number of documents with each city name). If the top three categories are Budget, Motel, and Luxury, and Budget has five hits, Motel has 6, and Luxury has 4, then the buckets are in the order Motel, Budget, Luxury. For `-value`, `"facet=rating,sort:-value"` produces buckets for all possible ratings, in descending order by value (for example, if the ratings are from 1 to 5, the buckets are ordered 5, 4, 3, 2, 1, irrespective of how many documents match each rating). |
    | `values` | Set to pipe-delimited numeric or `Edm.DateTimeOffset` values specifying a dynamic set of facet entry values. For example, `"facet=baseRate,values:10 | 20"` produces three buckets: one for base rate 0 up to but not including 10, one for 10 up to but not including 20, and one for 20 and higher. A string `"facet=lastRenovationDate,values:2010-02-01T00:00:00Z"` produces two buckets: one for hotels renovated before February 2010, and one for hotels renovated February 1, 2010 or later. The values must be listed in sequential, ascending order to get the expected results. |
    | `interval` | An integer interval greater than zero for numbers, or minute, hour, day, week, month, quarter, year for date time values. For example, `"facet=baseRate,interval:100"` produces buckets based on base rate ranges of size 100. If base rates are all between $60 and $600, there are buckets for 0-100, 100-200, 200-300, 300-400, 400-500, and 500-600. The string `"facet=lastRenovationDate,interval:year"` produces one bucket for each year when hotels were renovated. |
    | `timeoffset` | Can be set to (`[+-]hh:mm, [+-]hhmm, or [+-]hh`). If used, the `timeoffset` parameter must be combined with the interval option, and only when applied to a field of type `Edm.DateTimeOffset`. The value specifies the UTC time offset to account for in setting time boundaries. For example: `"facet=lastRenovationDate,interval:day,timeoffset:-01:00"` uses the day boundary that starts at 01:00:00 UTC (midnight in the target time zone). |

`count` and `sort` can be combined in the same facet specification, but they can't be combined with interval or values, and interval and values can't be combined together.

Interval facets on date time are computed based on the UTC time if `timeoffset` isn't specified. For example, for `"facet=lastRenovationDate,interval:day"`, the day boundary starts at 00:00:00 UTC.

---

### Basic facet example

The following facet queries work against the [hotels sample index](search-get-started-portal.md). You can use **JSON view** in Search Explorer to paste in the JSON query. 

This first query retrieves facets for categories, ratings, tags, and items with baseRate in specific ranges. Notice the last facet is on a subfield of the Rooms collection. Facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response determines the number of *hotels* that have any rooms in each price bucket.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{  
  "search": "ocean view",  
  "facets": [ "Category", "Rating", "Tags", "Rooms/BaseRate,values:80|150|220" ],
  "count": true 
}  
```

This second example uses a filter to narrow down the previous faceted query result after the user selects Rating 3 and category "Motel".

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{  
  "search": "water view",  
  "facets": [ "Tags", "Rooms/BaseRate,values:80|150|220" ],
  "filter": "Rating eq 3 and Category eq 'Motel'",
  "count": true  
} 
```

The third example sets an upper limit on unique terms returned in a query. The default is 10, but you can increase or decrease this value using the count parameter on the facet attribute. This example returns facets for city, limited to 5.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{  
  "search": "view",  
  "facets": [ "Address/City,count:5" ],
  "count": true
} 
```

This example shows three facets for "Category", "Tags", and "Rating", with a count override on "Tags" and a range override for "Rating", which is otherwise stored as a double in the index.

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

You can formulate a query that returns a distinct value count for each "facetable" field. This example formulates an empty or unqualified query (`"search": "*"`) that matches on all documents, but by setting `top` to zero, you get just the counts, with no results.

For brevity, this query includes just two fields marked as "facetable" in the hotels sample index.

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

### Facet hierarchy example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Starting in [2025-03-01-preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-03-01-preview&preserve-view=true) and available in the Azure portal, you can configure a facet hierarchy using the `>` and `;` operators.

The nesting (hierarchical) operator `>` denotes a parent–child relationship, and the semicolon operator `;` denotes children of a shared parent. The parent must contain only one field. Both the parent and child fields must be facetable. 

The order of operations in a facet expression that includes facet hierarchies are:

* options operator (comma `,`) that separates facet parameters for the facet field, such as the comma in `Rooms/BaseRate,values`
* parentheses, such as the ones enclosing `Rooms/BaseRate`.
* nesting operator (angled bracket `>`)
* append operator (semicolon `;`), demonstrated in a second example `"Tags>(Rooms/BaseRate,values:50;Rooms/Type)"` in this section, where two child facets are peers under the Tags parent.

Here's a query that returns just a few documents, which is helpful for viewing a full response. Facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response determines the number of *hotels* that have any rooms in each facet bucket.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{
  "search": "+ocean",  
  "facets": ["Address/StateProvince>Address/City", "Tags>(Rooms/BaseRate,values:50)"],
  "select": "HotelName, Description, Tags, Address/StateProvince, Address/City",
  "count": true 
}
```

The response should look similar to the following example. Both hotels have pools. For other tags, only one hotel provides the amenity.

```json
{
  "@odata.count": 2,
  "@search.facets": {
    "Tags": [
      {
        "value": "pool",
        "count": 2,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 2
            }
          ]
        }
      },
      {
        "value": "air conditioning",
        "count": 1,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 1
            }
          ]
        }
      },
      {
        "value": "bar",
        "count": 1,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 1
            }
          ]
        }
      },
      {
        "value": "restaurant",
        "count": 1,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 1
            }
          ]
        }
      },
      {
        "value": "view",
        "count": 1,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 1
            }
          ]
        }
      }
    ],
    "Address/StateProvince": [
      {
        "value": "FL",
        "count": 1,
        "@search.facets": {
          "Address/City": [
            {
              "value": "Tampa",
              "count": 1
            }
          ]
        }
      },
      {
        "value": "HI",
        "count": 1,
        "@search.facets": {
          "Address/City": [
            {
              "value": "Honolulu",
              "count": 1
            }
          ]
        }
      }
    ]
  },
  "value": [
    {
      "@search.score": 1.6076145,
      "HotelName": "Ocean Water Resort & Spa",
      "Description": "New Luxury Hotel for the vacation of a lifetime. Bay views from every room, location near the pier, rooftop pool, waterfront dining & more.",
      "Tags": [
        "view",
        "pool",
        "restaurant"
      ],
      "Address": {
        "City": "Tampa",
        "StateProvince": "FL"
      }
    },
    {
      "@search.score": 1.0594962,
      "HotelName": "Windy Ocean Motel",
      "Description": "Oceanfront hotel overlooking the beach features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away.",
      "Tags": [
        "pool",
        "air conditioning",
        "bar"
      ],
      "Address": {
        "City": "Honolulu",
        "StateProvince": "HI"
      }
    }
  ]
}
```

This example extends the previous one, demonstrating multiple top-level facets with multiple children. Notice the semicolon (`;`) operator separates each child.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{  
  "search": "+ocean",  
  "facets": ["Address/StateProvince>Address/City", "Tags>(Rooms/BaseRate,values:50;Rooms/Type)"],
  "select": "HotelName, Description, Tags, Address/StateProvince, Address/City",
  "count": true 
}  
```

A partial response, trimmed for brevity, shows Tags with child facets for the rooms base rate and type. In the hotels sample index, both hotels that match to `+ocean` have rooms in each type and a pool.

```json
{
  "@odata.count": 2,
  "@search.facets": {
    "Tags": [
      {
        "value": "pool",
        "count": 2,
        "@search.facets": {
          "Rooms/BaseRate": [
            {
              "to": 50,
              "count": 0
            },
            {
              "from": 50,
              "count": 2
            }
          ],
          "Rooms/Type": [
            {
              "value": "Budget Room",
              "count": 2
            },
            {
              "value": "Deluxe Room",
              "count": 2
            },
            {
              "value": "Standard Room",
              "count": 2
            },
            {
              "value": "Suite",
              "count": 2
            }
          ]
        }}]},
  ...
}
```

### Facet filtering example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Starting in [2025-03-01-preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-03-01-preview&preserve-view=true) and available in the Azure portal, you can configure facet filters.

Facet filtering enables you to constrain the facet values returned to those matching a specified regular expression. Two new parameters accept a regular expression that is applied to the facet field:

* `includeTermFilter` filters the facet values to those that match the regular expression
* `excludeTermFilter` filters the facet values to those that don't match the regular expression 

If a facet string satisfies both conditions, the `excludeTermFilter` takes precedence. Otherwise, the set of bucket strings are first evaluated with `includeTermFilter` and then excluded with `excludeTermFilter`.

Only those facet values that match the regular expression are returned. You can combine these parameters with other facet options (for example, `count`, `sort`, and [hierarchical faceting](#facet-hierarchy-example)) on string fields.

Because the regular expression is nested within a JSON string value, you must escape both the double quote (`"`) and the backslash (`\`) characters. The regular expression itself is delimited by the forward slash (`/`). For more information about escape patterns, see [Regular expression search](query-lucene-syntax.md#bkmk_regex).

The following example shows how to escape special characters in your regular expression such as backslash, double quotes, or regular expression syntax characters. 

```json
{
    "search": "*", 
    "facets": ["name,includeTermFilter:/EscapeBackslash\\OrDoubleQuote\\"OrRegexCharacter\\(/"] 
}
```

Here's an example of a facet filter that matches on Budget and Extended-Stay hotels, with Rating as a child of each hotel category.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview
{ 
    "search": "*", 
    "facets": ["(Category,includeTermFilter:/(Budget|Extended-Stay)/)>Rating,values:1|2|3|4|5"],
    "select": "HotelName, Category, Rating",
    "count": true 
} 
```

The following example is an abbreviated response (hotel documents are omitted for brevity).

```json
{
  "@odata.count": 50,
  "@search.facets": {
    "Category": [
      {
        "value": "Budget",
        "count": 13,
        "@search.facets": {
          "Rating": [
            {
              "to": 1,
              "count": 0
            },
            {
              "from": 1,
              "to": 2,
              "count": 0
            },
            {
              "from": 2,
              "to": 3,
              "count": 4
            },
            {
              "from": 3,
              "to": 4,
              "count": 5
            },
            {
              "from": 4,
              "to": 5,
              "count": 4
            },
            {
              "from": 5,
              "count": 0
            }
          ]
        }
      },
      {
        "value": "Extended-Stay",
        "count": 6,
        "@search.facets": {
          "Rating": [
            {
              "to": 1,
              "count": 0
            },
            {
              "from": 1,
              "to": 2,
              "count": 0
            },
            {
              "from": 2,
              "to": 3,
              "count": 4
            },
            {
              "from": 3,
              "to": 4,
              "count": 1
            },
            {
              "from": 4,
              "to": 5,
              "count": 1
            },
            {
              "from": 5,
              "count": 0
            }
          ]
        }
      }
    ]
  }, 
  "value": [  ALL 50 HOTELS APPEAR HERE ]
}
```

### Facet aggregation example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Starting in [2025-03-01-preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-03-01-preview&preserve-view=true) and available in the Azure portal, you can aggregate facets.

Facet aggregations allow you to compute metrics from facet values. The aggregation capability works alongside the existing faceting options. The only supported metric is `sum`. Adding `metric: sum` to a numeric facet aggregates all the values of each bucket.

You can sum any facetable field of a numeric data type (except vectors and geographic coordinates). 

Here's an example using the hotels-sample-index. The Rooms/SleepsCount field is facetable and numeric. You can sum it to get the sleep count for the entire hotel. Recall that facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response determines the number of *hotels* that have any rooms in each facet bucket. HotelName isn't facetable or filterable, but HotelId qualifies, and we can return both fields in the results.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-03-01-Preview

{ 
      "search": "*",
      "filter": "HotelId eq '41'",
      "facets": [ "Rooms/SleepsCount, metric: sum"],
      "select": "HotelId, HotelName, Rooms/Type, Rooms/SleepsCount",
      "count": true
}
```

A response for the query might look like the following example. Windy Ocean Model can accommodate a total of 40 guests.

```json
{
  "@odata.count": 1,
  "@search.facets": {
    "Rooms/SleepsCount": [
      {
        "sum": 40.0
      }
    ]
  },
  "value": [
    {
      "@search.score": 1.0,
      "HotelId": "41",
      "HotelName": "Windy Ocean Motel",
      "Rooms": [
        {
          "Type": "Suite",
          "SleepsCount": 4
        },
        {
          "Type": "Deluxe Room",
          "SleepsCount": 2
        },
        {
          "Type": "Budget Room",
          "SleepsCount": 2
        },
        {
          "Type": "Budget Room",
          "SleepsCount": 2
        },
        {
          "Type": "Suite",
          "SleepsCount": 2
        },
        {
          "Type": "Standard Room",
          "SleepsCount": 2
        },
        {
          "Type": "Deluxe Room",
          "SleepsCount": 2
        },
        {
          "Type": "Suite",
          "SleepsCount": 2
        },
        {
          "Type": "Suite",
          "SleepsCount": 4
        },
        {
          "Type": "Standard Room",
          "SleepsCount": 4
        },
        {
          "Type": "Standard Room",
          "SleepsCount": 2
        },
        {
          "Type": "Deluxe Room",
          "SleepsCount": 2
        },
        {
          "Type": "Suite",
          "SleepsCount": 2
        },
        {
          "Type": "Standard Room",
          "SleepsCount": 2
        },
        {
          "Type": "Deluxe Room",
          "SleepsCount": 2
        },
        {
          "Type": "Deluxe Room",
          "SleepsCount": 2
        },
        {
          "Type": "Standard Room",
          "SleepsCount": 2
        }
      ]
    }
  ]
}
```

## Best practices for working with facets

This section is a collection of tips and workarounds that are helpful for application development.

### Initialize a faceted navigation structure with an unqualified or empty search string

It's useful to initialize a search page with an open query (`"search": "*"`) to completely fill in the faceted navigation structure. As soon as you pass query terms in the request, the faceted navigation structure is scoped to just the matches in the results, rather than the entire index. This practice is helpful for verifying facet and filter behaviors during testing. If you include match criteria in the query, the response excludes documents that don't match, which has the potential downstream effect of excluding facets.

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
