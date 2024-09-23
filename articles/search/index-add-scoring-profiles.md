---
title: Add scoring profiles
titleSuffix: Azure AI Search
description: Boost search relevance scores for Azure AI Search results by adding scoring profiles to a search index.

manager: nitinme
author: shmed
ms.author: ramero
ms.service: cognitive-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 09/23/2024
---

# Add scoring profiles to boost search scores

In this article, learn how to specify and assign a scoring profile that boosts a search score based on parameters that you provide. Scoring profile parameters are either:

+ Weighted fields, where a match is found in a specific string field. For example, you might want matches found in a "summary" field to be more relevant than the same match found in a "content" field.

+ Functions for numeric data, including dates, ranges, and geographic coordinates. There's also a Tags function that operates on string fields. You can choose this approach over weighted fields if you want to boost a score based on whether a match is found in a tags field (an arbitrary collection of strings).

> [!NOTE]
> Unfamiliar with relevance concepts? The following [video segment on YouTube](https://www.youtube.com/embed/Y_X6USgvB1g?version=3&start=463&end=970) fast-forwards to how scoring profiles work in Azure AI Search. You can also visit [Relevance and scoring in Azure AI Search](index-similarity-and-scoring.md) for more background.
>

## Key points about scoring profiles

+ You can use scoring profiles for keyword search, vector search, and hybrid search. However, iscoring profiles only apply to nonvector fields in the index, so make sure your index has text or numeric fields that can be used in a scoring profile. Support for vector and hybrid search is available in 2024-05-01-preview and 2024-07-01 REST APIs and in Azure SDK packages that target those releases.

+ You can create multiple profiles and then modify query logic to choose which one is used.

+ You can have up to 100 scoring profiles within an index (see [service Limits](search-limits-quotas-capacity.md)), but you can only specify one profile at time in any given query.

## Scoring profile definition

A scoring profile is named object defined in an index schema. A scoring profile is composed of weighted fields, functions, and parameters.

The following definition shows a simple profile named "geo". This example boosts results that have the search term in the hotelName field. It also uses the `distance` function to favor results that are within 10 kilometers of the current location. If someone searches on the term 'inn', and 'inn' happens to be part of the hotel name, documents that include hotels with 'inn' within a 10 KM radius of the current location will appear higher in the search results.  

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

To use this scoring profile, your query is formulated to specify scoringProfile parameter in the request. If you're using the REST API, queries are specified through GET and POST requests. In the following example, "currentLocation" has a delimiter of a single dash (`-`). It's followed by longitude and latitude coordinates, where longitude is a negative value.

```http
GET /indexes/hotels/docs?search+inn&scoringProfile=geo&scoringParameter=currentLocation--122.123,44.77233&api-version=2024-07-01
```

Notice the syntax differences when using POST. In POST, "scoringParameters" is plural and it's an array.

```http
POST /indexes/hotels/docs&api-version=2024-07-01
{
    "search": "inn",
    "scoringProfile": "geo",
    "scoringParameters": ["currentLocation--122.123,44.77233"]
}
```  

This query searches on the term "inn" and passes in the current location. Notice that this query includes other parameters, such as scoringParameter. Query parameters, including "scoringParameter", are described in [Search Documents (REST API)](/rest/api/searchservice/documents/search-post).  

See the [Extended example](#bkmk_ex) to review a more detailed example of a scoring profile.  

<a name=what-is-default-scoring></a>

## How search scoring works in Azure AI Search

Scoring profiles supplement the default scoring algorithm by boosting the scores of matches that meet the profile's criteria. Scoring functions apply to keyword search, pure vector queries, and on hybrid queries. When you use scoring profiles, all queries regardless of type are ranked using the [Reciprocal Ranking Function (RRF)](hybrid-search-ranking.md) algorithm, including standalone text and vector queries. Scoring functions directly affect the final ranking of all documents post-RRF-ranking.

:::image type="content" source="media/scoring-profiles/scoring-over-ranked-results.png" alt-text="Diagram showing which fields have a scoring profile and when ranking occurs.":::

You can use the [featuresMode (preview)](index-similarity-and-scoring.md#featuresmode-parameter-preview) parameter to request extra scoring details with the search results (including the field level scores).

## Add a scoring profile to a search index

1. Start with an [index definition](/rest/api/searchservice/indexes/create). You can add and update scoring profiles on an existing index without having to rebuild it. Use an [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) request to post a revision.

1. Paste in the [template](#bkmk_template) provided in this article.  

1. Provide a name that adheres to [naming conventions](/rest/api/searchservice/naming-rules).

1. Specify boosting criteria. A single profile can contain [weighted fields](#weighted-fields), [functions](#functions), or both. 

You should work iteratively, using a data set that will help you prove or disprove the efficacy of a given profile.

Scoring profiles can be defined in Azure portal as shown in the following screenshot, or programmatically through [REST APIs](/rest/api/searchservice/indexes/create-or-update) or in Azure SDKs, such as the [ScoringProfile](/dotnet/api/azure.search.documents.indexes.models.scoringprofile) class in the Azure SDK for .NET.

   :::image type="content" source="media/scoring-profiles/portal-add-scoring-profile-small.png" alt-text="Add scoring profiles page" lightbox="media/scoring-profiles/portal-add-scoring-profile.png" border="true":::

<a name="weighted-fields"></a>

## Use weighted fields

Use weighted fields when field context is important and queries include searchable string fields. For example, if a query includes the term "airport", you might want "airport" in the Description field to have more weight than in the HotelName. 

Weighted fields are name-value pairs composed of a searchable field and a positive number that is used as a multiplier. If the original field score of HotelName is 3, the boosted score for that field becomes 6, contributing to a higher overall score for the parent document itself.


```json
"scoringProfiles": [  
    {  
      "name": "boostKeywords",  
      "text": {  
        "weights": {  
          "HotelName": 2,  
          "Description": 5 
        }  
      }  
    }
]
```

<a name="functions"></a>

## Use functions

Use functions when simple relative weights are insufficient or don't apply, as is the case of distance and freshness, which are calculations over numeric data. You can specify multiple functions per scoring profile. For more information about the EDM data types used in Azure AI Search, see [Supported data types](/rest/api/searchservice/supported-data-types).

| Function | Description | Use cases |
|-|-|
| freshness | Boosts by values in a datetime field (`Edm.DateTimeOffset`). This function has a "boostingDuration" attribute so that you can specify a value representing a timespan over which boosting occurs. | Use this function to boost a match having a more recent date. You can also rank items like calendar events with future dates such that items closer to the present can be ranked higher than items further in the future. One end of the range is fixed to the current time. To boost a range of times in the past, use a positive boostingDuration. To boost a range of times in the future, use a negative boostingDuration. The [interpolation](#set-interpolations) parameter sets the slope. |
| magnitude | The magnitude scoring function is used to alter rankings based on the range of values for a numeric field. The value must be an integer or floating-point number. For star ratings of 1 through 4, this would be 1. For margins over 50%, this would be 50. This function can only be used with `Edm.Double` and `Edm.Int` fields. For the magnitude function, you can reverse the range, high to low, if you want the inverse pattern (for example, to boost lower-priced items more than higher-priced items). Given a range of prices from $100 to $1, you would set "boostingRangeStart" at 100 and "boostingRangeEnd" at 1 to boost the lower-priced items. | Scenarios that call for this function include boosting by profit margin, highest price, lowest price, or a count of downloads. Common usage examples of this are: </br></br>"Star ratings:" Alter the scoring based on the value within the "Star Rating" field. When two items are relevant, the item with the higher rating will be displayed first. </br>"Margin:" When two documents are relevant, a retailer might wish to boost documents that have higher margins first. </br>"Clickthrough counts:" For applications that track clickthrough actions to products or pages, you could use magnitude to boost items that tend to get the most traffic. </br>"Download counts:" For applications that track downloads, the magnitude function lets you boost items that have the most downloads.  |
| distance  | Boosts by proximity or geographic location. This function can only be used with `Edm.GeographyPoint` fields. | Use for "find near me" scenarios. |
| tag  | Boosts by tags that are common to both search documents and query strings. Tags are provided in a "tagsParameter". This function can only be used with search fields of type `Edm.String` and `Collection(Edm.String)`. | Use when you have tag fields. If a given tag within the list is itself a comma-delimited list, you can [use a text normalizer](search-normalizers.md) on the field to strip out the commas at query time (map the comma character to a space). This approach will "flatten" the list so that all terms are a single, long string of comma-delimited terms. | 

### Rules for using functions

+ Functions can only be applied to fields that are attributed as `filterable`.
+ Function type ("freshness", "magnitude", "distance", "tag") must be lower case.
+ Functions can't include null or empty values.
+ Functions can only have a single field per function definition. To use magnitude twice in the same profile, provide two definitions magnitude, one for each field.

<a name="bkmk_template"></a>

## Template

 This section shows the syntax and template for scoring profiles. For a description of properties, see the [REST API reference](/rest/api/searchservice/indexes/create?view=rest-searchservice-2024-07-01&preservice-view=true#scoringfunctionaggregation).

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
        "boost": # (positive number used as multiplier for raw score != 1),   
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

<a name="bkmk_interpolation"></a> 

## Set interpolations

Interpolations set the shape of the slope used for scoring. Because scoring is high to low, the slope is always decreasing, but the interpolation determines the curve of the downward slope. The following interpolations can be used:  

| Interpolation | Description |  
|-|-|  
|`linear`|For items that are within the max and min range, boosting is applied in a constantly decreasing amount. Linear is the default interpolation for a scoring profile.|  
|`constant`|For items that are within the start and ending range, a constant boost is applied to the rank results.|  
|`quadratic`|In comparison to a linear interpolation that has a constantly decreasing boost, Quadratic initially decreases at smaller pace and then as it approaches the end range, it decreases at a much higher interval. This interpolation option isn't allowed in tag scoring functions.|  
|`logarithmic`|In comparison to a linear interpolation that has a constantly decreasing boost, logarithmic initially decreases at higher pace and then as it approaches the end range, it decreases at a much smaller interval. This interpolation option isn't allowed in tag scoring functions.|  

 ![Constant, linear, quadratic, log10 lines on graph](media/scoring-profiles/azuresearch_scorefunctioninterpolationgrapht.png "AzureSearch_ScoreFunctionInterpolationGrapht")  

<a name="bkmk_boostdur"></a> 

## Set boostingDuration

`boostingDuration` is an attribute of the `freshness` function. You use it to set an expiration period after which boosting will stop for a particular document. For example, to boost a product line or brand for a 10-day promotional period, you would specify the 10-day period as "P10D" for those documents.  

`boostingDuration` must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an ISO 8601 duration value). The pattern for this is: "P[nD][T[nH][nM][nS]]".  

The following table provides several examples.  

|Duration|boostingDuration|  
|--------------|----------------------|  
|1 day|"P1D"|  
|2 days and 12 hours|"P2DT12H"|  
|15 minutes|"PT15M"|  
|30 days, 5 hours, 10 minutes, and 6.334 seconds|"P30DT5H10M6.334S"|  

For more examples, see [XML Schema: Datatypes (W3.org web site)](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration).  

<a name="bkmk_ex"></a>

## Extended example

The following example shows the schema of an index with two scoring profiles (`boostGenre`, `newAndHighlyRated`). Any query against this index that includes either profile as a query parameter will use the profile to score the result set. 

The `boostGenre` profile uses weighted text fields, boosting matches found in albumTitle, genre, and artistName fields. The fields are boosted 1.5, 5, and 2 respectively. Why is genre boosted so much higher than the others? If search is conducted over data that is somewhat homogenous (as is the case with 'genre' in the musicstoreindex), you might need a larger variance in the relative weights. For example, in the musicstoreindex, 'rock' appears as both a genre and in identically phrased genre descriptions. If you want genre to outweigh genre description, the genre field will need a much higher relative weight.

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
          "boost": 10,  
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
  ],  
  "suggesters": [  
    {  
      "name": "sg",  
      "searchMode": "analyzingInfixMatching",  
      "sourceFields": [ "albumTitle", "artistName" ]  
    }  
  ]   
}  
```  

## See also

+ [Relevance and scoring in Azure AI Search](index-similarity-and-scoring.md)
+ [REST API Reference](/rest/api/searchservice/)
+ [Create Index API](/rest/api/searchservice/indexes/create)
+ [Azure AI Search .NET SDK](/dotnet/api/overview/azure/search?)
+ [What Are Scoring Profiles?](https://social.technet.microsoft.com/wiki/contents/articles/26706.azure-search-what-are-scoring-profiles.aspx)
