---
title: Add scoring profiles
titleSuffix: Azure AI Search
description: Boost search relevance scores for Azure AI Search results by adding scoring profiles to a search index.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 01/20/2026
ms.update-cycle: 365-days
---

# Add scoring profiles to boost search scores

Scoring profiles are used to boost or suppress the ranking of matching documents based on user-defined criteria. In this article, learn how to specify and assign a scoring profile that boosts a search score based on parameters that you provide. You can create scoring profiles based on:

+ Weighted string fields, where boosting is based on a match found in a designated field. For example, matches found in a "Subject" field are considered more relevant than the same match found in a "Description" field.

+ Functions for numeric fields, including dates and geographic coordinates. Functions for numeric content support boosting on distance (applies to geographic coordinates), freshness (applies to datetime fields), range, and magnitude.

+ Functions for string collections (tags). A tags function boosts a document's search score if any item in the collection is matched by the query.

+ (preview) [An aggregation of distinct boosts](#example-function-aggregation). Within a single scoring profile, you can specify multiple scoring functions, and then set `"functionAggregation": "product"`. Documents that score highly across all functions are prioritized, while those that score weak in one or more fields are suppressed.

You can add a scoring profile to an index by editing its JSON definition in the Azure portal or programmatically through APIs like [Create or Update Index REST](/rest/api/searchservice/indexes/create-or-update) or equivalent index update APIs in any Azure SDK. There's no index rebuild requirements so you can add, modify, or delete a scoring profile with no effect on indexed documents.

By the end of this article, you can create and apply scoring profiles to boost search relevance based on field weights, freshness, distance, or custom criteria.

## Prerequisites

+ An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

+ A search index with text or numeric (nonvector) fields.

+ **Permissions**: You need **Search Index Data Contributor** to create or update an index with scoring profiles. To query using a scoring profile, you need **Search Index Data Reader**. For more information, see [Connect using roles](search-security-rbac.md).

+ **SDK installation (optional)**:

  + Python: `pip install azure-search-documents`
  + C#: `dotnet add package Azure.Search.Documents`

> [!TIP]
> For immediate code examples, skip to [Scoring profile definition](#scoring-profile-definition).

## Rules for scoring profiles

You can use scoring profiles in [keyword search](search-lucene-query-architecture.md), [vector search](vector-search-overview.md), [hybrid search](hybrid-search-overview.md), and with [semantic reranking)](semantic-search-overview.md). However, scoring profiles only apply to nonvector fields, so make sure your index has text or numeric fields that can be boosted or weighted. 

You can have up to 100 scoring profiles within an index (see [service Limits](search-limits-quotas-capacity.md)), but you can only specify one profile at a time in any given query.

You can use [semantic ranking](semantic-how-to-query-request.md) with scoring profiles and apply a [scoring profile after semantic ranking](semantic-how-to-enable-scoring-profiles.md) occurs. Otherwise, when multiple ranking or relevance features are in play, semantic ranking is the last step. [How search scoring works](search-relevance-overview.md#diagram-of-ranking-algorithms) provides an illustration of the order of operations.

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

**Reference**: [scoringProfiles](/rest/api/searchservice/indexes/create#scoringprofile) | [scoringFunction](/rest/api/searchservice/indexes/create#scoringfunction) | [distance function](/rest/api/searchservice/indexes/create#distancescoringfunction)

To use this scoring profile, your query is formulated to specify `scoringProfile` parameter in the request. If you're using the REST API, queries are specified through GET and POST requests. In the following example, "currentLocation" has a delimiter of a single dash (`-`). It's followed by longitude and latitude coordinates, where longitude is a negative value.

```http
POST /indexes/hotels/docs&api-version=2025-09-01
{
    "search": "inn",
    "scoringProfile": "geo",
    "scoringParameters": ["currentLocation--122.123,44.77233"]
}
```  

**Reference**: [Search Documents (REST)](/rest/api/searchservice/documents/search-post) | [scoringProfile parameter](/rest/api/searchservice/documents/search-post#searchrequest) | [scoringParameters](/rest/api/searchservice/documents/search-post#searchrequest)

Query parameters, including `scoringParameters`, are described in [Search Documents (REST API)](/rest/api/searchservice/documents/search-post).  

For more scenarios, see the examples for [freshness and distance](#example-boosting-by-freshness-or-distance) and [weighted text and functions](#example-boosting-by-weighted-text-and-functions) in this article.

### Query with a scoring profile using the SDKs

#### [Python](#tab/python)

```python
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

# Set up the client
endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
index_name = "hotels"
credential = DefaultAzureCredential()

client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

# Execute search with scoring profile
results = client.search(
    search_text="inn",
    scoring_profile="geo",
    scoring_parameters=["currentLocation--122.123,44.77233"],
    select=["HotelName", "Description", "Rating"]
)

for result in results:
    print(f"{result['HotelName']} (Score: {result['@search.score']})")
```

**Reference**: [SearchClient.search](/python/api/azure-search-documents/azure.search.documents.searchclient#azure-search-documents-searchclient-search) | [scoring_profile parameter](/python/api/azure-search-documents/azure.search.documents.searchclient)

#### [C#](#tab/csharp)

```csharp
using Azure;
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.Models;

// Set up the client
string endpoint = Environment.GetEnvironmentVariable("AZURE_SEARCH_ENDPOINT");
string indexName = "hotels";

SearchClient client = new SearchClient(
    new Uri(endpoint),
    indexName,
    new DefaultAzureCredential());

// Execute search with scoring profile
SearchResults<SearchDocument> results = client.Search<SearchDocument>(
    "inn",
    new SearchOptions
    {
        ScoringProfile = "geo",
        ScoringParameters = { "currentLocation--122.123,44.77233" },
        Select = { "HotelName", "Description", "Rating" }
    });

await foreach (SearchResult<SearchDocument> result in results.GetResultsAsync())
{
    Console.WriteLine($"{result.Document["HotelName"]} (Score: {result.Score})");
}
```

**Reference**: [SearchClient.Search](/dotnet/api/azure.search.documents.searchclient.search) | [SearchOptions.ScoringProfile](/dotnet/api/azure.search.documents.searchoptions.scoringprofile)

---

## Add a scoring profile to a search index

1. Start with an [index definition](/rest/api/searchservice/indexes/create). You can add and update scoring profiles on an existing index without having to rebuild it. Use [Get Index](/rest/api/searchservice/indexes/get) to pull down an existing index, and use [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) request to post a revision.

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

## Use text-weighted fields

Use text-weighted fields when field context is important and queries include `searchable` string fields. For example, if a query includes the term "airport", you might favor "airport" in the HotelName field rather than the Description field. 

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
| freshness | Boost by values in a datetime field (`Edm.DateTimeOffset`). [Set boostingDuration](#set-boostingduration-for-freshness-function) to specify a value representing a timespan over which boosting occurs. | Use when you want to promote recent (newer) dates. You can also boost items like calendar events with future dates such that are closer to the present, as compared with items that are further into the future. One end of the range is fixed to the current time.  |
| magnitude | Magnitude is the computed distance between the document’s value (such as a date or location) and the reference point (such as "now" or a target location). It’s the input to the scoring function and determines how much boost is applied. Alter rankings based on the range of values for a numeric field. The value must be an integer or floating-point number. For star ratings of 1 through 4, this would be 1. For margins over 50%, this would be 50. This function can only be used with `Edm.Double` and `Edm.Int` fields. For the magnitude function, you can reverse the range, high to low, if you want the inverse pattern (for example, to boost lower-priced items more than higher-priced items). Given a range of prices from $100 to $1, you would set `boostingRangeStart` at 100 and `boostingRangeEnd` at 1 to boost the lower-priced items. | Use when you want to boost by profit margin, ratings, clickthrough counts, number of downloads, highest price, lowest price, or a count of downloads. When two items are relevant, the item with the higher rating is displayed first. |
| tag  | Boost by tags that are common to both search documents and query strings. Tags are provided in a `tagsParameter`. This function can only be used with search fields of type `Edm.String` and `Collection(Edm.String)`. | Use when you have tag fields. If a given tag within the list is itself a comma-delimited list, you can [use a text normalizer](search-normalizers.md) on the field to strip out the commas at query time (map the comma character to a space). This approach "flattens" the list so that all terms are a single, long string of comma-delimited terms. | 

Freshness and distance scoring are special cases of magnitude-based scoring, where the magnitude is automatically computed from a datetime or geographic field.

### Rules for using functions

+ Functions can only be applied to fields that are attributed as `filterable`.
+ Function type ("freshness", "magnitude", "distance", "tag") must be lower case.
+ Functions can't include null or empty values.
+ Functions can only have a single field per function definition. To use magnitude twice in the same profile, provide two definitions magnitude, one for each field.

### Set interpolations

Interpolations set the shape of the slope used for boosting freshness and distance. Because scoring is high to low, the slope is always decreasing, but the interpolation determines the curve of the downward slope and how aggressively the boost score changes as document dates get older. 

| Interpolation | Description |  
|-|-|  
|`linear`|For items that are within the max and min range, boosting is applied in a constantly decreasing amount. Recommended when you want a gradual decay in relevance. Linear is the default interpolation for a scoring profile.|  
|`constant`|For items that are within the start and ending range, a constant boost is applied to the rank results. Use this when you want a flat penalty regardless of age.|  
|`quadratic`|Quadratic initially decreases at smaller pace and then accelerates as it approaches the end range, it decreases at a much higher interval. Use this interpolation when you want to strongly favor the most recent documents and sharply demote older ones. This interpolation option isn't allowed in the tag scoring function.|  
|`logarithmic` |Logarithmic initially decreases at higher pace and then as it approaches the end range, it decreases at a much smaller interval. Recommended when you have a strong preference for very recent content but less sensitivity as documents age. This interpolation option isn't allowed in the tag scoring function.|  
  
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

The shape of the boost curve (constant, linear, logarithmic, quadratic) affects how aggressively scores change across the range. 

When using the freshness function, if you want the boost to have a more dramatic effect on more recent dates, choose a quadratic interpolation. Quadratic amplifies the effect of near recent dates and closer locations and tapers off more slowly at the far end of the range. In contrast, a logarithmic curve shifts more sharply at the far end.

Here's an example scoring profile that demonstrates how to boost by freshness.

```json
{
    "name": "docs-index",
    "fields": [
      { "name": "id", "type": "Edm.String", "key": true, "filterable": true },
      { "name": "title", "type": "Edm.String", "searchable": true },
      { "name": "content", "type": "Edm.String", "searchable": true },
      { "name": "lastUpdated", "type": "Edm.DateTimeOffset", "filterable": true, "sortable": true }
    ],
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
            "boost": 2.0,
            "interpolation": "quadratic",
            "parameters": {
              "boostingDuration": "365D"
            }
          }
        ]
    }
  ]
}
```

+ The `freshness` function computes a magnitude from "now" to `lastUpdated`.
+ A positive boost with quadratic interpolation increases lift for recent dates, tapering quickly for older ones. 
+ `"boostingDuration": "365D"` defines the time window over which freshness is evaluated, for example boosting documents dated within the last year.
+ `"interpolation": "quadratic"` means the boost effect is stronger for documents closer to the current date and tapers off more sharply for older ones.

In the next example, a linear interpolation provides a steady preference for most‑recent content across the 30‑day window. Increase boost if the signal needs to win against other relevance factors.

```json
{
  "name": "freshness30_linear",
  "functions": [
    {
      "type": "freshness",
      "fieldName": "lastUpdated",
      "boost": 3.0,
      "interpolation": "linear",
      "parameters": { "boostingDuration": "P30D" }
    }
  ]
}
```

**Reference**: [freshness function](/rest/api/searchservice/indexes/create#freshnessscoringfunction) | [boostingDuration](/rest/api/searchservice/indexes/create#freshnessscoringparameters)

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

## Example: function aggregation

> [!NOTE]
> This capability is currently in preview, available through the [2025-11-01-preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) and in Azure SDK preview packages that provide the feature.

Within a single scoring profile, you can specify multiple scoring functions, and then set `"functionAggregation": "product"`. Documents that score highly across all functions are prioritized, while those that score weak in one or more fields are suppressed.

In this example, create a scoring profile that includes two boosting functions that boost by `rating` and `baseRate`, and then set `functionAggregation` to `product`.

```http
### Create a new index
PUT {{url}}/indexes/hotels-scoring?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{key}}

{
    "name": "hotels-scoring",  
    "fields": [
        {"name": "HotelId", "type": "Edm.String", "key": true, "filterable": true, "facetable": true},
        {"name": "HotelName", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": true, "facetable": true},
        {"name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "sortable": false, "facetable": true, "analyzer": "en.lucene"},
        {"name": "Category", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
        {"name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "sortable": false, "facetable": true},
        {"name": "ParkingIncluded", "type": "Edm.Boolean", "filterable": true, "sortable": true, "facetable": true},
        {"name": "LastRenovationDate", "type": "Edm.DateTimeOffset", "filterable": true, "sortable": true, "facetable": true},
        {"name": "Rating", "type": "Edm.Double", "filterable": true, "sortable": true, "facetable": true},
        {"name": "BaseRate", "type": "Edm.Double", "filterable": true, "sortable": true, "facetable": true },
        {"name": "Address", "type": "Edm.ComplexType", 
            "fields": [
            {"name": "StreetAddress", "type": "Edm.String", "filterable": false, "sortable": false, "facetable": true, "searchable": true},
            {"name": "City", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
            {"name": "StateProvince", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true},
            {"name": "PostalCode", "type": "Edm.String", "searchable": true, "filterable": true, "sortable": true, "facetable": true}
            ]
        }
    ],
    "scoringProfiles": [
        {
            "name": "productAggregationProfile",
            "functions": [
                {
                    "type": "magnitude",
                    "fieldName": "Rating",
                    "boost": 2.0,
                    "interpolation": "linear",
                    "magnitude": {
                        "boostingRangeStart": 1.0,
                        "boostingRangeEnd": 5.0,
                        "constantBoostBeyondRange": false
                    }
                },
                {
                    "type": "magnitude",
                    "fieldName": "BaseRate",
                    "boost": 1.5,
                    "interpolation": "linear",
                    "magnitude": {
                        "boostingRangeStart": 50.0,
                        "boostingRangeEnd": 400.0,
                        "constantBoostBeyondRange": false
                    }
                }
            ],
            "functionAggregation": "product"
        }
    ],
    "defaultScoringProfile": "productAggregationProfile"
}
```

This next request loads the index with searchable content that tests the profile.

```http
### Upload documents to the index
POST {{url}}/indexes/hotels-scoring/docs/index?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{key}}

  {
        "value": [
        {
        "@search.action": "upload",
        "HotelId": "1",
        "HotelName": "Stay-Kay City Hotel",
        "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
        "Category": "Boutique",
        "Tags": [ "view", "air conditioning", "concierge" ],
        "ParkingIncluded": false,
        "LastRenovationDate": "2022-01-18T00:00:00Z",
        "Rating": 3.60,
        "BaseRate": 200.0,
        "Address": 
            {
            "StreetAddress": "677 5th Ave",
            "City": "New York",
            "StateProvince": "NY",
            "PostalCode": "10022"
            } 
        },
        {
        "@search.action": "upload",
        "HotelId": "2",
        "HotelName": "Old Century Hotel",
        "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
         "Category": "Boutique",
        "Tags": [ "pool", "free wifi", "concierge" ],
        "ParkingIncluded": false,
        "LastRenovationDate": "2019-02-18T00:00:00Z",
        "Rating": 3.60,
        "BaseRate": 150.0,
        "Address": 
            {
            "StreetAddress": "140 University Town Center Dr",
            "City": "Sarasota",
            "StateProvince": "FL",
            "PostalCode": "34243"
            } 
        },
        {
        "@search.action": "upload",
        "HotelId": "3",
        "HotelName": "Gastronomic Landscape Hotel",
        "Description": "The Gastronomic Landscape Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel’s restaurant services.",
        "Category": "Suite",
        "Tags": [ "restaurant", "bar", "continental breakfast" ],
        "ParkingIncluded": true,
        "LastRenovationDate": "2015-09-20T00:00:00Z",
        "Rating": 4.80,
        "BaseRate": 350.0,
        "Address": 
            {
            "StreetAddress": "3393 Peachtree Rd",
            "City": "Atlanta",
            "StateProvince": "GA",
            "PostalCode": "30326"
            } 
        },
        {
        "@search.action": "upload",
        "HotelId": "4",
        "HotelName": "Sublime Palace Hotel",
        "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.",
        "Tags": [ "concierge", "view", "air conditioning" ],
        "ParkingIncluded": true,
        "LastRenovationDate": "2020-02-06T00:00:00Z",
        "Rating": 4.60,
        "BaseRate": 275.0,
        "Address": 
            {
            "StreetAddress": "7400 San Pedro Ave",
            "City": "San Antonio",
            "StateProvince": "TX",
            "PostalCode": "78216"
            }
        }
    ]
}
```

Run a query that uses the criteria in the scoring profile to boost results based on a high rating and high base rate. The boosting scores are aggregated to further promote results that score high in both functions.

```http
### Search with boost
POST {{url}}/indexes/hotels-scoring/docs/search?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{key}}

{
    "search": "expensive and good hotels",
    "count": true,
    "select": "HotelId, HotelName, Description, Rating, BaseRate",
    "scoringProfile": "productAggregationProfile"
}
```

The top response for this query is "Gastronomic Landscape Hotel" with a search score that is almost twice as high as next closest match. This particular hotel has both the highest rating and the highest base rate, so the compounding of both functions promotes this match to the top.

```json
{
  "@odata.count": 4,
  "value": [
    {
      "@search.score": 1.0541908,
      "HotelId": "3",
      "HotelName": "Gastronomic Landscape Hotel",
      "Description": "The Gastronomic Hotel stands out for its culinary excellence under the management of William Dough, who advises on and oversees all of the Hotel\u2019s restaurant services.",
      "Rating": 4.8,
      "BaseRate": 350.0
    },
    {
      "@search.score": 0.53451097,
      "HotelId": "2",
      "HotelName": "Old Century Hotel",
      "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music.",
      "Rating": 3.6,
      "BaseRate": 150.0
    },
    {
      "@search.score": 0.53185254,
      "HotelId": "1",
      "HotelName": "Stay-Kay City Hotel",
      "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
      "Rating": 3.6,
      "BaseRate": 200.0
    },
    {
      "@search.score": 0.44853577,
      "HotelId": "4",
      "HotelName": "Sublime Palace Hotel",
      "Description": "Sublime Palace Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience.",
      "Rating": 4.6,
      "BaseRate": 275.0
    }
  ]
}
```

## Tuning tips

+ Start conservative: boost in the 1.25–2.0 range; increase only if recency is truly decisive.

+ Window sizing: Use P30D for hot content, P90D/P180D for moderate recency, P365D for long‑tail.

+ Interpolation choice:

  + quadratic when you want a strong push to recent.
  + linear when you want a steady gradient.
  + logarithmic when you want a gentle preference.

+ Aggregation: If combining multiple functions, sum is easiest; switch to max when you want a single signal to dominate

## Troubleshoot scoring profiles

Use the following table to diagnose common issues with scoring profiles.

| Issue | Possible cause | Resolution |
| ------- | --------------- | ------------ |
| Scoring profile not applied | Profile name not specified in query | Add `scoringProfile` parameter to your search request with the exact profile name. |
| No boost effect observed | Field isn't marked as `filterable` | Functions can only be applied to fields attributed as `filterable`. Update your index schema. |
| Unexpected ranking results | Boost value too low or high | Start with boost values in the 1.25–2.0 range and adjust based on testing. |
| Freshness not boosting recent docs | `boostingDuration` too short or wrong format | Verify the duration format (e.g., "P30D" for 30 days) and extend the window if needed. |
| Distance function not working | Field isn't `Edm.GeographyPoint` | The distance function only works with `Edm.GeographyPoint` fields. |
| Tag function returns no boost | Tags don't match query values | Verify the `tagsParameter` matches values in the search request's `scoringParameters`. |
| Profile exists but query fails | Invalid field name in profile | Ensure all field names in the scoring profile exist in the index schema. |

## Related content

+ [Relevance and scoring in Azure AI Search](index-similarity-and-scoring.md)
+ [Scoring profile REST API reference](/rest/api/searchservice/indexes/create#scoringprofile)
+ [Search Documents REST API](/rest/api/searchservice/documents/search-post)
+ [Semantic ranking](semantic-how-to-query-request.md)
+ [ScoringProfile class (.NET)](/dotnet/api/azure.search.documents.indexes.models.scoringprofile)
+ [ScoringProfile class (Python)](/python/api/azure-search-documents/azure.search.documents.indexes.models.scoringprofile)