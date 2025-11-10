---

title: Faceted navigation examples
titleSuffix: Azure AI Search
description: Examples that demonstrate query syntax for facet hierarchies, distinct counts, facet aggregations, and facet filters.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
ms.update-cycle: 365-days
---

# Faceted navigation examples

This section extends [faceted navigation configuration](search-faceted-navigation.md) with examples that demonstrate basic usage and other scenarios.

Facetable fields are defined in an index, but facet parameters and expressions are defined in query requests. If you have an index with facetable fields, you can try new preview features like [facet hierarchies](#facet-hierarchy-example), [facet aggregations](#facet-aggregation-example), and [facet filters](#facet-filtering-example) on existing indexes.

## Facet parameters and syntax

Depending on the API, a facet query is usually an array of facet expressions that are applied to search results. Each facet expression contains a facetable field name, optionally followed by a comma-separated list of name-value pairs.

+ *facet query* is a query request that includes a facet property.
+ *facetable field* is a field definition in the search index attributed with the `facetable` property.
+ *count* is the number of matches for each facet found in the search results.

The following table describes facet parameters used in the examples.

| Facet parameter | Description | Usage | Example |
|-----------------|-------------|-------|---------|
| `count` | Maximum number of facet terms per structure.| Integer. Default is 10. There's no upper limit, but higher values degrade performance, especially if the faceted field contains a large number of unique terms. This is due to the way facet queries are distributed across shards. You can set `count` to zero or to a value that's greater than or equal to the number of unique values in the facetable field to get an accurate count across all shards. The tradeoff is increased latency. | `Tags,count:5` limits the faceted navigation response to 5 facet buckets that containing the most facet counts, but they can be in any order. |
| `sort` | Determines order of facet buckets. | Valid values are `count`, `-count`, `value`, `-value`. Use `count` to list facets from greatest to smallest. Use `-count` to sort in ascending order (smallest to greatest). Use `value` to sort alphanumerically by facet value in ascending order. Use `-value` to sort descending by value. | `"facet=Category,count:3,sort:count"` gets the top three facet buckets in search results, listed in descending order by the number of matches in each Category. If the top three categories are Budget, Extended-Stay, and Luxury, and Budget has 5 hits, Extended-Stay has 6, and Luxury has 4, then the facet buckets are ordered as Extended-Stay, Budget, Luxury. Another example is`"facet=Rating,sort:-value"`. It produces facets for all possible ratings, in descending order by value. If ratings are from 1 to 5, the facets are ordered 5, 4, 3, 2, 1, irrespective of how many documents match each rating. |
| `values` | Provides values for facet labels. | Set to pipe-delimited numeric or `Edm.DateTimeOffset` values specifying a dynamic set of facet entry values. The values must be listed in sequential, ascending order to get the expected results. | `"facet=baseRate,values:10 | 20"` produces three facet buckets: one for base rate 0 up to but not including 10, one for 10 up to but not including 20, and one for 20 and higher. A string `"facet=lastRenovationDate,values:2024-02-01T00:00:00Z"` produces two facet buckets: one for hotels renovated before February 2024, and one for hotels renovated February 1, 2024 or later. |
| `interval` | Provides an interval sequence for facets that can be grouped into intervals. | An integer interval greater than zero for numbers, or minute, hour, day, week, month, quarter, year for date time values. | `"facet=baseRate,interval:100"` produces facet buckets based on base rate ranges of size 100. If base rates are all between $60 and $600, there are facet buckets for 0-100, 100-200, 200-300, 300-400, 400-500, and 500-600. The string `"facet=lastRenovationDate,interval:year"` produces one facet bucket for each year a hotel was renovated. |
| `timeoffset` | Specifies the UTC time offset to account for in setting time boundaries. | Set to (`[+-]hh:mm, [+-]hhmm, or [+-]hh`). If used, the `timeoffset` parameter must be combined with the interval option, and only when applied to a field of type `Edm.DateTimeOffset`. | `"facet=lastRenovationDate,interval:day,timeoffset:-01:00"` uses the day boundary that starts at 01:00:00 UTC (midnight in the target time zone). |

`count` and `sort` can be combined in the same facet specification, but they can't be combined with `interval` or `values`.

`interval` and `values` can't be combined together.

Interval facets on date time are computed based on the UTC time if `timeoffset` isn't specified. For example, for `"facet=lastRenovationDate,interval:day"`, the day boundary starts at 00:00:00 UTC.

## Basic facet example

The following facet queries work against the [hotels sample index](search-get-started-portal.md). You can use **JSON view** in Search Explorer to paste in the JSON query. For help with getting started, see [Add faceted navigation to search results](search-faceted-navigation.md).

This first query retrieves facets for Categories, Ratings, Tags, and rooms with baseRate values in specific ranges. Notice the last facet is on a subfield of the Rooms collection. Facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response determines the number of *hotels* that have any rooms in each pricing category.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version={{api_version}}
{  
  "search": "ocean view",  
  "facets": [ "Category", "Rating", "Tags", "Rooms/BaseRate,values:80|150|220" ],
  "count": true 
}  
```

This second example uses a filter to narrow down the previous faceted query result after the user selects Rating 3 and category "Motel".

```rest
POST /indexes/hotels-sample-index/docs/search?api-version={{api_version}}
{  
  "search": "water view",  
  "facets": [ "Tags", "Rooms/BaseRate,values:80|150|220" ],
  "filter": "Rating eq 3 and Category eq 'Motel'",
  "count": true  
} 
```

The third example sets an upper limit on unique terms returned in a query. The default is 10, but you can increase or decrease this value using the count parameter on the facet attribute. This example returns facets for city, limited to 5.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version={{api_version}}
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

## Distinct values example

You can formulate a query that returns a distinct value count for each facetable field. This example formulates an empty or unqualified query (`"search": "*"`) that matches on all documents, but by setting `top` to zero, you get just the counts, with no results.

For brevity, this query includes just two fields marked as `facetable` in the hotels sample index.

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

## Facet hierarchy example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Using the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or the Azure portal, you can configure a facet hierarchy using the `>` and `;` operators.

| Operator | Description |
|-|-|
| `>` | Nesting (hierarchical) operator denotes a parent–child relationship. |
| `;` | Semicolon operator  denotes multiple fields at the same nesting level, which are all children of the same parent. The parent must contain only one field. Both the parent and child fields must be `facetable`. |

The order of operations in a facet expression that includes facet hierarchies are:

+ The options operator (comma `,`) that separates facet parameters for the facet field, such as the comma in `Rooms/BaseRate,values`
+ The parentheses, such as the ones enclosing `(Rooms/BaseRate,values:50 ; Rooms/Type)`.
+ The nesting operator (angled bracket `>`)
+ The append operator (semicolon `;`), demonstrated in a second example `"Tags>(Rooms/BaseRate,values:50 ; Rooms/Type)"` in this section, where two child facets are peers under the Tags parent.

Notice that parentheses are processed before nesting and append operations: `A > B ; C` would be different than `A > (B ; C)`.

There are several examples for facet hierarchies. The first example is a query that returns just a few documents, which is helpful for viewing a full response. Facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response determines the number of *hotels* that have any rooms in each facet bucket.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-11-01-Preview
{
  "search": "ocean",  
  "facets": ["Address/StateProvince>Address/City", "Tags>Rooms/BaseRate,values:50"],
  "select": "HotelName, Description, Tags, Address/StateProvince, Address/City",
  "count": true 
}
```

Results from this query are as follows. Both hotels have pools. For other tags, only one hotel provides the amenity.

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

This second example extends the previous one, demonstrating multiple top-level facets with multiple children. Notice the semicolon (`;`) operator separates each child.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-11-01-Preview
{  
  "search": "+ocean",  
  "facets": ["Address/StateProvince > Address/City", "Tags > (Rooms/BaseRate,values:50 ; Rooms/Type)"],
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

This last example shows precedence rules for parentheses that affects nesting levels. Suppose you want to return a facet hierarchy in this order.

```
Address/StateProvince
  Address/City
    Category
    Rating
```

To return this hierarchy, create a query where Category and Rating are siblings under Address/City.

```json
  { 
    "search": "beach",  
    "facets": [
        "Address/StateProvince > (Address/City > (Category ; Rating))"
        ],
    "select": "HotelName, Description, Tags, Address/StateProvince, Address/City",
    "count": true 
  }
```

If you remove the innermost parentheses, Category and Rating are no longer siblings because the precedence rules mean that the `>` operator is evaluated before `;`.

```json
  { 
    "search": "beach",  
    "facets": [
        "Address/StateProvince > (Address/City > Category ; Rating)"
        ],
    "select": "HotelName, Description, Tags, Address/StateProvince, Address/City",
    "count": true 
  }
```

The top-level parent is still Address/StateProvince, but now Address/City and Rating are on same level.

```
Address/StateProvince
  Rating
  Address/City
    Category
```

## Facet filtering example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Using the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or the Azure portal, you can configure facet filters.

Facet filtering enables you to constrain the facet values returned to those matching a specified regular expression. Two new parameters accept a regular expression that is applied to the facet field:

+ `includeTermFilter` filters the facet values to those that match the regular expression
+ `excludeTermFilter` filters the facet values to those that don't match the regular expression 

If a facet string satisfies both conditions, the `excludeTermFilter` takes precedence because the set of bucket strings is first evaluated with `includeTermFilter` and then excluded with `excludeTermFilter`.

Only those facet values that match the regular expression are returned. You can combine these parameters with other facet options (for example, `count`, `sort`, and [hierarchical faceting](#facet-hierarchy-example)) on string fields.

Because the regular expression is nested within a JSON string value, you must escape both the double quote (`"`) and the backslash (`\`) characters. The regular expression itself is delimited by the forward slash (`/`). For more information about escape patterns, see [Regular expression search](query-lucene-syntax.md#bkmk_regex).

The following example shows how to escape special characters in your regular expression such as backslash, double quotes, or regular expression syntax characters. 

```json
{
    "search": "*", 
    "facets": ["name,includeTermFilter:/EscapeBackslash\\\OrDoubleQuote\\"OrRegexCharacter\\(/"] 
}
```

Here's an example of a facet filter that matches on Budget and Extended-Stay hotels, with Rating as a child of each hotel category.

```http
POST /indexes/hotels-sample-index/docs/search?api-version=2025-11-01-Preview
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

## Facet aggregation example

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Using the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or the Azure portal, you can aggregate facets.

Facet aggregations allow you to compute metrics from facet values. The aggregation capability works alongside the existing faceting options.

| Aggregator | Description |
|------------|-------------|
| Sum | Returns the total accumulated value from the field across all documents. Applies to numeric types only. Supported in earlier preview releases. |
| Min | Returns the minimum value from the field across all documents. Applies to numeric types only. |
| Max | Returns the maximum value from the field across all documents. Applies to numeric types only.|
| Avg | Returns the average value from the field across all documents. Applies to numeric types only. |
| Cardinality | Returns the approximate count of distinct values from the field across all documents using the [HyperLogLog algorithm](https://en.wikipedia.org/wiki/HyperLogLog). You can request `cardinality` on facetable fields, including string and datetime fields (along with their corresponding collection forms). |

### Setting precision thresholds for cardinality aggregation

On a cardinality aggregation, you can set a `precisionThreshold` option as a demarcation between counts that are expected to be close to accurate, and counts that can be less accurate. The maximum value is 40,000. The default value is 3,000.

Faceting is performed in memory. Increasing `precisionThreshold` results in more memory consumption (the `precisionThreshold` value multiplied by 8 bytes).

### Example: Sum facet aggregation

You can sum any facetable field of a numeric data type (except vectors and geographic coordinates). 

Here's an example using the hotels-sample-index. The Rooms/SleepsCount field is facetable and numeric, so we choose this field to demonstrate sum. If we sum that field, we get the sleep count for the entire hotel. Recall that facets count the parent document (Hotels) and not intermediate subdocuments (Rooms), so the response sums the SleepsCount of all rooms for the entire hotel. In this query, we add a filter to sum the SleepsCount for just one hotel.

```rest
POST /indexes/hotels-sample-index/docs/search?api-version=2025-11-01-Preview

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

### Example: A composite of all aggregations

Here's an example using a hypothetical 'facets' index that shows the syntax for each aggregation. Notice that cardinality has an extra `precisionThreshold` option (default is 3,000) set to 40,000 in this example.

```http
POST https://search-service.search.windows.net/indexes/facets/docs/search?api-version=2025-11-01-Preview 
Authorization: Bearer {{token}}
Content-Type: application/json

{
    "search": "*",
    "facets": [// field names are named <something>Value in this example 
        "cardinalityValue, metric: cardinality,precisionThreshold: 40000", 
        "sumValue,metric: sum", 
        "avgValue,metric: avg", 
        "minValue,metric: min", 
        "maxValue,metric: max" 
    ] 
}
```

A response for the query might look like the following example.

```json
{ 
    "@search.facets": { 
        "cardinalityValue": [ 
            { 
                "cardinality": 24000 // Number of distinct values in "cardinalityValue" field 
            } 
        ], 
        "sumValue": [ 
            { 
                "sum": 1200000 // Sum of all values in "sumValue" field 
            } 
        ], 
        "avgValue": [ 
            { 
                "avg": 50 // Average of all values in "avgValue" field 
            } 
        ], 
        "minValue": [ 
            { 
                "min": 1 // Minimum value in "minValue" field 
            } 
        ], 
        "maxValue": [ 
            { 
                "max": 100 // Maximum value in "maxValue" field 
            } 
        ] 
    } 
}
```

### Example: Specify a default to substitute for missing values

All metrics support specifying a default value when a document doesn't contain a value. 

+ For nonstring types (numeric, datetime, boolean), set the `default` parameter to a specific value: `"default: 42" `.

+ For string types, set the `default` parameter to a string, delimited using the single apostrophe delimiter: `"default: 'mystringhere'"`.

You can add a default value to use if a document contains a null for that field: `"facets": [ "Rooms/SleepsCount, metric: sum, default:2"]`. If a room has a null value for the Rooms/SleepsCount field, the default substitutes for the missing value.

Here's a request that illustrates the default specification for each field type.

```http
POST https://search-service.search.windows.net/indexes/facets/docs/search?api-version=2025-11-01-Preview 
Authorization: Bearer {{token}} 
Content-Type: application/json 

{ 
    "search": "*", 
    "facets": [// field names are named <datatype>Value in this example 
        "stringfield, metric: cardinality, default: 'my string goes here'", 
        "doubleField,metric: sum, default: 5.0", 
        "intField,metric: sum, default: 5", 
        "longField,metric: sum, default: 5" 
    ] 
} 
```

For string fields, a default value is delimited using the single quote character. To escape the character, prefix it with the backslash "\'". All characters are valid within the string delimiters. The terminating character can't be a backslash.

### Example: Multiple metrics on the same field

If the underlying data supports the use case, you can specify multiple metrics on the same field.

```http
POST https://search-service.search.windows.net/indexes/facets/docs/search?api-version=2025-11-01-Preview 
Authorization: Bearer {{token}} 
Content-Type: application/json 

{ 
    "search": "*", 
    "facets": [ 
        "fieldA, metric: cardinality, precisionThreshold: 40000", 
        "fieldA, metric: sum", 
        "fieldA, metric: avg", 
        "fieldA, metric: min", 
        "fieldA, metric: max" 
    ] 
}
```
 
A response for the query might look like the following example.

```json
{ 
    "@search.facets": { 
        "fieldA": [ 
            { 
                "cardinality": 24000 // Number of distinct values in "fieldA" field 
            }, 
            { 
                "sum": 1200000 // Sum of all values in " fieldA " field 
            }, 
            { 
                "avg": 5 // Avg of all values in " fieldA " field
            }, 
            { 
                "min": 0 // Min of all values in " fieldA " field 
            }, 
            { 
                "max": 1200 // Max of all values in " fieldA " field 
            } 
        ] 
    } 
}
```

## Next steps

Revisit [facet navigation configuration](search-faceted-navigation.md) for tools and APIs, and review [best practices](search-faceted-navigation.md#best-practices-for-working-with-facets) for working with facets in code.

We recommend the [C#: Add search to web apps](tutorial-csharp-overview.md) for an example of faceted navigation that includes code for the presentation layer. The sample also includes filters, suggestions, and autocomplete. It uses JavaScript and React for the presentation layer.
