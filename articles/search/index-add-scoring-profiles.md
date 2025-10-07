---
title: Add scoring profiles
titleSuffix: Azure AI Search
description: Boost search relevance scores for Azure AI Search results by adding scoring profiles to a search index.
manager: nitinme
author: shmed
ms.author: ramero
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 09/29/2025
ms.update-cycle: 365-days
---

# Add scoring profiles to boost search scores

Scoring profiles are used to boost the ranking of matching documents based on criteria. In this article, learn how to specify and assign a scoring profile that boosts a search score based on parameters that you provide. You can create scoring profiles based on:

+ Weighted string fields, where boosting is based on a match found in a designated field. For example, matches found in a "Subject" field are considered more relevant than the same match found in a "Description" field.

+ Functions for numeric fields, including dates and geographic coordinates. Functions for numeric content support boosting on distance (applies to geographic coordinates), freshness (applies to datetime fields), range, and magnitude.

+ Functions for string collections (tags). A tags function boosts a document's search score if any item in the collection is matched by the query.

You can add a scoring profile to an index by editing its JSON definition in the Azure portal or programmatically through APIs like [Create or Update Index REST](/rest/api/searchservice/indexes/create-or-update) or equivalent index update APIs in any Azure SDK. There's no index rebuild requirements so you can add, modify, or delete a scoring profile with no effect on indexed documents.

## Prerequisites

+ A search index with text or numeric (nonvector) fields.

## Rules for scoring profiles

You can use scoring profiles in [keyword search](search-lucene-query-architecture.md), [vector search](vector-search-overview.md), [hybrid search](hybrid-search-overview.md), and [semantic reranking)](semantic-search-overview.md). However, scoring profiles only apply to nonvector fields, so make sure your index has text or numeric fields that can be boosted or weighted. 

You can have up to 100 scoring profiles within an index (see [service Limits](search-limits-quotas-capacity.md)), but you can only specify one profile at time in any given query.

You can use [semantic ranker](semantic-how-to-query-request.md) with scoring profiles and apply a [scoring profile after semantic ranking](semantic-how-to-enable-scoring-profiles.md). Otherwise, when multiple ranking or relevance features are in play, semantic ranking is the last step. [How search scoring works](search-relevance-overview.md#diagram-of-ranking-algorithms) provides an illustration.

[Extra rules](#rules-for-using-functions) apply specifically to functions.

> [!NOTE]
> Unfamiliar with relevance concepts? Visit [Relevance and scoring in Azure AI Search](index-similarity-and-scoring.md) for background. You can also watch this [video segment on YouTube](https://www.youtube.com/embed/Y_X6USgvB1g?version=3&start=463&end=970) for scoring profiles over BM25-ranked results.
>

## Scoring profile definition

A scoring profile is defined in an index schema. It consists of weighted fields, functions, and parameters.

The following definition shows a simple profile named "geo". This example boosts results that have the search term in the hotelName field. It also uses the `distance` function to favor results that are within 10 kilometers of the current location. If someone searches on the term 'inn', and 'inn' happens to be part of the hotel name, documents that include hotels with 'inn' within a 10-kilometer radius of the current location appear higher in the search results.  

```json
"scoringProfiles": [
  {  
    "name":"geo",
    "text": {  
      "weights": {  
        "hotelName": 5
      }                              
    },
    "functions": [
      {  
        "type": "distance",
        "boost": 5,
        "fieldName": "location",
        "interpolation": "logarithmic",
        "distance": {
          "referencePointParameter": "currentLocation",
          "boostingDistance": 10
        }                        
      }                                      
    ]                     
  }            
]
```  

To use this scoring profile, your query is formulated to specify `scoringProfile` parameter in the request. If you're using the REST API, queries are specified through GET and POST requests. In the following example, "currentLocation" has a delimiter of a single dash (`-`). It's followed by longitude and latitude coordinates, where longitude is a negative value.

```http
POST /indexes/hotels/docs&api-version=2025-09-01
{
    "search": "inn",
    "scoringProfile": "geo",
    "scoringParameters": ["currentLocation--122.123,44.77233"]
}
```  

Query parameters, including `scoringParameters`, are described in [Search Documents (REST API)](/rest/api/searchservice/documents/search-post).  

For more scenarios, see the examples for [freshness and distance](#example-boosting-by-freshness-or-distance) and [weighted text and functions](#example-boosting-by-weighted-text-and-functions) in this article.

## Add a scoring profile to a search index

1. Start with an [index definition](/rest/api/searchservice/indexes/create). You can add and update scoring profiles on an existing index without having to rebuild it. Use a [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) request to post a revision.

1. Paste in the [template](#template) provided in this article.  

1. Provide a name that adheres to [naming conventions](/rest/api/searchservice/naming-rules).

1. Specify boosting criteria. A single profile can contain [text weighted fields](#use-text-weighted-fields), [functions](#use-functions), or both. 

You should work iteratively, using a data set that helps you prove or disprove the efficacy of a given profile.

Scoring profiles can be defined in the Azure portal as shown in the following screenshot, or programmatically through [REST APIs](/rest/api/searchservice/indexes/create-or-update) or in Azure SDKs, such as the ScoringProfile class in [.NET](/dotnet/api/azure.search.documents.indexes.models.scoringprofile) or [Python](/python/api/azure-search-documents/azure.search.documents.indexes.models.scoringprofile) client libraries.

:::image type="content" source="media/scoring-profiles/portal-add-scoring-profile-small.png" alt-text="Screenshot showing the Add scoring profile option in the Azure portal." lightbox="media/scoring-profiles/portal-add-scoring-profile.png" border="true":::

### Template

 This section shows the syntax and template for scoring profiles. For a description of properties, see the [REST API reference](/rest/api/searchservice/indexes/create#scoringfunctionaggregation).

```json
"scoringProfiles": [  
  {   
    "name": "name of scoring profile",   
    "text": (optional, only applies to searchable fields) {   
      "weights": {   
        "searchable_field_name": relative_weight_value (positive #'s),   
        ...   
      }   
    },   
    "functions": (optional) [  
      {   
        "type": "magnitude | freshness | distance | tag",   
        "boost": # (positive or negative number used as multiplier for raw score != 1),   
        "fieldName": "(...)",   
        "interpolation": "constant | linear (default) | quadratic | logarithmic",   

        "magnitude": {
          "boostingRangeStart": #,   
          "boostingRangeEnd": #,   
          "constantBoostBeyondRange": true | false (default)
        }  

        // ( - or -)  

        "freshness": {
          "boostingDuration": "..." (value representing timespan over which boosting occurs)   
        }  

        // ( - or -)  

        "distance": {
          "referencePointParameter": "...", (parameter to be passed in queries to use as reference location)   
          "boostingDistance": # (the distance in kilometers from the reference location where the boosting range ends)   
        }   

        // ( - or -)  

        "tag": {
          "tagsParameter":  "..."(parameter to be passed in queries to specify a list of tags to compare against target field)   
        }
      }
    ],   
    "functionAggregation": (optional, applies only when functions are specified) "sum (default) | average | minimum | maximum | firstMatching"   
  }   
],   
"defaultScoringProfile": (optional) "...", 
```

## Use text-weighted fields

Use text-weighted fields when field context is important and queries include `searchable` string fields. For example, if a query includes the term "airport", you might want "airport" in the HotelName field rather than the Description field. 

Weighted fields are name-value pairs composed of a `searchable` field and a positive number that is used as a multiplier. If the original field score of HotelName is 3, the boosted score for that field becomes 6, contributing to a higher overall score for the parent document itself.

```json
"scoringProfiles": [  
    {  
      "name": "boostSearchTerms",  
      "text": {  
        "weights": {  
          "HotelName": 2,  
          "Description": 5 
        }  
      }  
    }
]
```

## Use functions

Use functions when simple relative weights are insufficient or don't apply, as is the case of distance and freshness, which are calculations over numeric data. You can specify multiple functions per scoring profile. For more information about the EDM data types used in Azure AI Search, see [Supported data types](/rest/api/searchservice/supported-data-types).

| Function | Description | Use cases |
|-|-|
| distance  | Boost by proximity or geographic location. This function can only be used with `Edm.GeographyPoint` fields. | Use for "find near me" scenarios. |
| freshness | Boost by values in a datetime field (`Edm.DateTimeOffset`). [Set boostingDuration](#set-boostingduration-for-freshness-function) to specify a value representing a timespan over which boosting occurs. | Use when you want to boost by newer or older dates. Rank items like calendar events with future dates such that items closer to the present can be ranked higher than items further in the future. One end of the range is fixed to the current time. To boost a range of times in the past, use a positive boostingDuration. To boost a range of times in the future, use a negative boostingDuration. |
| magnitude | Alter rankings based on the range of values for a numeric field. The value must be an integer or floating-point number. For star ratings of 1 through 4, this would be 1. For margins over 50%, this would be 50. This function can only be used with `Edm.Double` and `Edm.Int` fields. For the magnitude function, you can reverse the range, high to low, if you want the inverse pattern (for example, to boost lower-priced items more than higher-priced items). Given a range of prices from $100 to $1, you would set `boostingRangeStart` at 100 and `boostingRangeEnd` at 1 to boost the lower-priced items. | Use when you want to boost by profit margin, ratings, clickthrough counts, number of downloads, highest price, lowest price, or a count of downloads. When two items are relevant, the item with the higher rating is displayed first. |
| tag  | Boost by tags that are common to both search documents and query strings. Tags are provided in a `tagsParameter`. This function can only be used with search fields of type `Edm.String` and `Collection(Edm.String)`. | Use when you have tag fields. If a given tag within the list is itself a comma-delimited list, you can [use a text normalizer](search-normalizers.md) on the field to strip out the commas at query time (map the comma character to a space). This approach "flattens" the list so that all terms are a single, long string of comma-delimited terms. | 

Magnitude is the computed distance between a field's value (such as a date or location) and a reference point (such as "now" or a target location). It's the input to the scoring function and determines how much boost is applied. 

Freshness and distance scoring are special cases of magnitude-based scoring, where the magnitude is automatically computed from a datetime or geographic field. For intuitive boosting that promotes newer or closer values over older or farther values, use a negative boost value (see the [example](#example-boosting-by-freshness-or-distance) for more details).

### Rules for using functions

+ Functions can only be applied to fields that are attributed as `filterable`.
+ Function type ("freshness", "magnitude", "distance", "tag") must be lower case.
+ Functions can't include null or empty values.
+ Functions can only have a single field per function definition. To use magnitude twice in the same profile, provide two definitions magnitude, one for each field.

### Set interpolations

Interpolations set the shape of the slope used for boosting freshness and distance. 

When the boost value is positive, scoring is high to low, and the slope is always decreasing. With negative boosts, the slope is increasing (newer documents get higher scores). The interpolation values determines the curve of the upward or downward slope and how aggressively the boost score changes in response to date or distance changes. The following interpolations can be used:  

| Interpolation | Description |  
|-|-|  
|`linear`|For items that are within the max and min range, boosting is applied in a constantly decreasing amount. A negative boost penalizes older documents proportionally. Good for gradual decay in relevance. Linear is the default interpolation for a scoring profile.|  
|`constant`|For items that are within the start and ending range, a constant boost is applied to the rank results. For freshness and distance, applies the same negative boost to all documents within the range. Use this when you want a flat penalty regardless of age.|  
|`quadratic`|Quadratic initially decreases at smaller pace and then as it approaches the end range, it decreases at a much higher interval. For negative boosting, it penalizes older documents increasingly more as they age. Use this when you want to strongly favor the most recent documents and sharply demote older ones. This interpolation option isn't allowed in the tag scoring function.|  
|`logarithmic` |Logarithmic initially decreases at higher pace and then as it approaches the end range, it decreases at a much smaller interval. For negative boosting, it penalizes older documents more sharply at first, then tapers off. Ideal when you want strong preference for very recent content but less sensitivity as documents age. This interpolation option isn't allowed in the tag scoring function.|  

<!--  ![Constant, linear, quadratic, log10 lines on graph](media/scoring-profiles/azuresearch_scorefunctioninterpolationgrapht.png "AzureSearch_ScoreFunctionInterpolationGrapht") -->
  
:::image type="content" source="media/scoring-profiles/interpolation-graph.png" alt-text="Diagram of slope shapes for constant, linear, logarithmic, and quadratic interpolations over a 365 day range":::

### Set boostingDuration for freshness function

`boostingDuration` is an attribute of the `freshness` function. You use it to set an expiration period after which boosting stops for a particular document. For example, to boost a product line or brand for a 10-day promotional period, you would specify the 10-day period as "P10D" for those documents.  

`boostingDuration` must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an ISO 8601 duration value). The pattern for this is: "P[nD][T[nH][nM][nS]]".  

The following table provides several examples.  

|Duration|boostingDuration|  
|--------------|----------------------|  
|1 day|"P1D"|  
|2 days and 12 hours|"P2DT12H"|  
|15 minutes|"PT15M"|  
|30 days, 5 hours, 10 minutes, and 6.334 seconds|"P30DT5H10M6.334S"|
|1 year | "365D" |

For more examples, see [XML Schema: Datatypes (W3.org web site)](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration).

## Example: boosting by freshness or distance

In Azure AI Search, freshness scoring converts date and values into a numeric magnitude—a single number representing how far a document's date is from the current time. The older the date, the larger the magnitude. This leads to a counter-intuitive behavior: more recent documents have smaller magnitudes, which means that positive boosting factors favor older documents unless you explicitly invert the boost direction.

This same logic applies to distance boosting, where farther locations yield larger magnitudes.

To boost by freshness or distance, use negative boosting values to prioritize newer dates or closer locations. Inverting the boost direction through a negative boosting factor penalizes larger magnitudes (older dates), effectively boosting more recent ones. For example, assume a boosting function like `b * (1 - x)` (where `x` is the normalized magnitude from 0 to 1) that gives higher scores to smaller magnitudes (that is, newer dates).

The shape of the boost curve (constant, linear, logarithmic, quadratic) affects how aggressively scores change across the range. With a negative factor, the curve’s behavior flips—for example, a quadratic curve tapers off more slowly for older dates, while a logarithmic curve shifts more sharply at the far end.

Here's an example scoring profile that demonstrates how to address counter-intuitive freshness scoring using negative boosting and explains how magnitude works in this context.

```json

"scoringProfiles": [
  {
    "name": "freshnessBoost",
    "text": {
      "weights": {
        "content": 1.0
      }
    },
    "functions": [
      {
        "type": "freshness",
        "fieldName": "lastUpdated",
        "boost": -2.0,
        "interpolation": "quadratic",
        "parameters": {
          "boostingDuration": "365D"
        }
      }
    ]
  }
]
```

+ `"fieldName": "lastUpdated"` is the datetime field used to calculate freshness.
+ `"boost": -2.0` is a negative boosting factor, which inverts the default behavior. Since older dates have larger magnitudes, this penalizes them and boosts newer documents.
+ `"interpolation": "quadratic"` means the boost effect is stronger for documents closer to the current date and tapers off more sharply for older ones.
+ `"boostingDuration": "365D"` defines the time window over which freshness is evaluated.

## Example: boosting by weighted text and functions

> [!TIP]
> See this [blog post](https://farzzy.hashnode.dev/enhance-azure-ai-search-document-boosting) and [notebook](https://github.com/farzad528/azure-ai-search-python-playground/blob/main/azure-ai-search-document-boosting.ipynb) for a demonstration of using scoring profiles and document boosting in vector and generative AI scenarios.

The following example shows the schema of an index with two scoring profiles (`boostGenre`, `newAndHighlyRated`). Any query against this index that includes either profile as a query parameter uses the profile to score the result set. 

The `boostGenre` profile uses weighted text fields, boosting matches found in albumTitle, genre, and artistName fields. The fields are boosted 1.5, 5, and 2 respectively. Why is genre boosted so much higher than the others? If search is conducted over data that is somewhat homogeneous (as is the case with 'genre' in the musicstoreindex), you might need a larger variance in the relative weights. For example, in the musicstoreindex, 'rock' appears as both a genre and in identically phrased genre descriptions. If you want genre to outweigh genre description, the genre field needs a much higher relative weight.

```json
{  
  "name": "musicstoreindex",  
  "fields": [  
    { "name": "key", "type": "Edm.String", "key": true },  
    { "name": "albumTitle", "type": "Edm.String" },  
    { "name": "albumUrl", "type": "Edm.String", "filterable": false },  
    { "name": "genre", "type": "Edm.String" },  
    { "name": "genreDescription", "type": "Edm.String", "filterable": false },  
    { "name": "artistName", "type": "Edm.String" },  
    { "name": "orderableOnline", "type": "Edm.Boolean" },  
    { "name": "rating", "type": "Edm.Int32" },  
    { "name": "tags", "type": "Collection(Edm.String)" },  
    { "name": "price", "type": "Edm.Double", "filterable": false },  
    { "name": "margin", "type": "Edm.Int32", "retrievable": false },  
    { "name": "inventory", "type": "Edm.Int32" },  
    { "name": "lastUpdated", "type": "Edm.DateTimeOffset" }  
  ],  
  "scoringProfiles": [  
    {  
      "name": "boostGenre",  
      "text": {  
        "weights": {  
          "albumTitle": 1.5,  
          "genre": 5,  
          "artistName": 2  
        }  
      }  
    },  
    {  
      "name": "newAndHighlyRated",  
      "functions": [  
        {  
          "type": "freshness",  
          "fieldName": "lastUpdated",  
          "boost": -10,  
          "interpolation": "quadratic",  
          "freshness": {  
            "boostingDuration": "P365D"  
          }  
        },  
        {
          "type": "magnitude",  
          "fieldName": "rating",  
          "boost": 10,  
          "interpolation": "linear",  
          "magnitude": {  
            "boostingRangeStart": 1,  
            "boostingRangeEnd": 5,  
            "constantBoostBeyondRange": false  
          }  
        }  
      ]  
    }  
  ]
}  
```  
