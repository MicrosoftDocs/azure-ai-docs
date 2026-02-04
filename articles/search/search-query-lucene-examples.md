---
title: Examples of full Lucene query syntax
titleSuffix: Azure AI Search
description: Explore query examples that demonstrate the Lucene query syntax for fuzzy search, proximity search, term boosting, regular expression search, and wildcard searches in an Azure AI Search index.
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

# Examples of *full* Lucene search syntax (advanced queries)

When constructing queries for Azure AI Search, you can replace the default [simple query parser](query-simple-syntax.md) with the more powerful [Lucene query parser](query-lucene-syntax.md) to formulate specialized and advanced query expressions.

The Lucene parser supports complex query formats, such as field-scoped queries, fuzzy search, infix and suffix wildcard search, proximity search, term boosting, and regular expression search. The extra power comes with more processing requirements so you should expect a slightly longer execution time. In this article, you can step through examples that demonstrate query operations based on full syntax.

> [!NOTE]
> Many of the specialized query constructions enabled through the full Lucene query syntax are not [text-analyzed](search-lucene-query-architecture.md#stage-2-lexical-analysis), which can be surprising if you expect stemming or lemmatization. Lexical analysis is only performed on complete terms (a term query or phrase query). Query types with incomplete terms (prefix query, wildcard query, regex query, fuzzy query) are added directly to the query tree, bypassing the analysis stage. The only transformation performed on partial query terms is lowercasing. 
>

## Hotels sample index

The following queries are based on the hotels-sample-index, which you can create by following the instructions in this [quickstart](search-get-started-portal.md).

Example queries are articulated using the REST API and POST requests. You can paste and run them in a [REST client](search-get-started-text.md). Or, use the JSON view of [Search Explorer](search-explorer.md) in the Azure portal. In JSON view, you can paste in the query examples shown here in this article.

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
    "queryType": "full",
    "select": "HotelId, HotelName, Category, Tags, Description",
    "count": true
}
```

+ `search` set to * is an unspecified query, equivalent to null or empty search. It's not especially useful, but it's the simplest search you can do, and it shows all retrievable fields in the index, with all values.

+ `queryType` set to *full* invokes the full Lucene query parser and it's required for this syntax.

+ `select` set to a comma-delimited list of fields is used for search result composition, including only those fields that are useful in the context of search results.

+ `count` returns the number of documents matching the search criteria. On an empty search string, the count is all documents in the index (50 in the hotels-sample-index).

## Example 1: Fielded search

Fielded search scopes individual, embedded search expressions to a specific field. This example searches for hotel names with the term *hotel* in them, but not *motel*. You can specify multiple fields using `AND`.

When you use this query syntax, you can omit the `searchFields` parameter when the fields you want to query are in the search expression itself. If you include `searchFields` with fielded search, the `fieldName:searchExpression` always takes precedence over `searchFields`.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "HotelName:(hotel NOT motel) AND Category:'Boutique'",
    "queryType": "full",
    "select": "HotelName, Category",
    "count": true
}
```

The response for this query should look similar to the following example, filtered on *Boutique*, returning hotels that include *hotel* in the name, while excluding results that include *motel* in the name.

```json
{
  "@odata.count": 5,
  "value": [
    {
      "@search.score": 2.2289815,
      "HotelName": "Stay-Kay City Hotel",
      "Category": "Boutique"
    },
    {
      "@search.score": 1.3862944,
      "HotelName": "City Skyline Antiquity Hotel",
      "Category": "Boutique"
    },
    {
      "@search.score": 1.355046,
      "HotelName": "Old Century Hotel",
      "Category": "Boutique"
    },
    {
      "@search.score": 1.355046,
      "HotelName": "Sublime Palace Hotel",
      "Category": "Boutique"
    },
    {
      "@search.score": 1.355046,
      "HotelName": "Red Tide Hotel",
      "Category": "Boutique"
    }
  ]
}
```

The search expression can be a single term or a phrase, or a more complex expression in parentheses, optionally with Boolean operators. Some examples include the following:

+ `HotelName:(hotel NOT motel)`
+ `Address/StateProvince:("WA" OR "CA")`
+ `Tags:("free wifi" NOT "free parking") AND "coffee in lobby"`

Be sure to put a phrase within quotation marks if you want both strings to be evaluated as a single entity, as in this case searching for two distinct locations in the `Address/StateProvince` field. Depending on the client, you might need to escape (`\`) the quotation marks.

The field specified in `fieldName:searchExpression` must be a searchable field. To learn how field definitions are attributed, see [Create Index (REST API)](/rest/api/searchservice/indexes/create).

## Example 2: Fuzzy search

Fuzzy search matches on terms that are similar, including misspelled words. To do a fuzzy search, append the tilde `~` symbol at the end of a single word with an optional parameter, a value between 0 and 2, that specifies the edit distance. For example, `blue~` or `blue~1` would return blue, blues, and glue.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "Tags:conserge~",
    "queryType": "full",
    "select": "HotelName, Category, Tags",
    "searchFields": "HotelName, Category, Tags",
    "count": true
}
```

The response for this query resolves to *concierge* in the matching documents, trimmed for brevity:

```json
{
  "@odata.count": 9,
  "value": [
    {
      "@search.score": 1.4947624,
      "HotelName": "Twin Vortex Hotel",
      "Category": "Luxury",
      "Tags": [
        "bar",
        "restaurant",
        "concierge"
      ]
    },
    {
      "@search.score": 1.1685618,
      "HotelName": "Stay-Kay City Hotel",
      "Category": "Boutique",
      "Tags": [
        "view",
        "air conditioning",
        "concierge"
      ]
    },
    {
      "@search.score": 1.1465473,
      "HotelName": "Old Century Hotel",
      "Category": "Boutique",
      "Tags": [
        "pool",
        "free wifi",
        "concierge"
      ]
    },
. . .
  ]
}
```

Phrases aren't supported directly but you can specify a fuzzy match on each term of a multi-part phrase, such as `search=Tags:landy~ AND sevic~`. This query expression finds 15 matches on *laundry service*.

> [!Note]
> Fuzzy queries are not [analyzed](search-lucene-query-architecture.md#stage-2-lexical-analysis). Query types with incomplete terms (prefix query, wildcard query, regex query, fuzzy query) are added directly to the query tree, bypassing the analysis stage. The only transformation performed on partial query terms is lower casing.
>

## Example 3: Proximity search

Proximity search finds terms that are near each other in a document. Insert a tilde `~` symbol at the end of a phrase followed by the number of words that create the proximity boundary.

This query searches for the terms *hotel* and  *airport* within five words of each other in a document. The quotation marks are escaped (`\"`) to preserve the phrase:

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "Description: \"hotel airport\"~5",
    "queryType": "full",
    "select": "HotelName, Description",
    "searchFields": "HotelName, Description",
    "count": true
}
```

The response for this query should look similar to the following example:

```json
{
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 0.69167054,
      "HotelName": "Trails End Motel",
      "Description": "Only 8 miles from Downtown. On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, All non-smoking hotel. Only 15 miles from airport."
    }
  ]
}
```

## Example 4: Term boosting

Term boosting refers to ranking a document higher if it contains the boosted term, relative to documents that don't contain the term. To boost a term, use the caret, `^`, symbol with a boost factor (a number) at the end of the term you're searching. The boost factor default is 1, and although it must be positive, it can be less than 1 (for example, 0.2). Term boosting differs from scoring profiles in that scoring profiles boost certain fields, rather than specific terms.

In this *before* query, search for *beach access* and notice that there are six documents that match on one or both terms.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "beach access",
    "queryType": "full",
    "select": "HotelName, Description, Tags",
    "searchFields": "HotelName, Description, Tags",
    "count": true
}
```

In fact, only two documents match on *access*. The first instance is in second position, even though the document is missing the term *beach*.

```json
{
  "@odata.count": 6,
  "value": [
    {
      "@search.score": 1.068669,
      "HotelName": "Johnson's Family Resort",
      "Description": "Family oriented resort located in the heart of the northland. Operated since 1962 by the Smith family, we have grown into one of the largest family resorts in the state. The home of excellent Smallmouth Bass fishing with 10 small cabins, we're a home not only to fishermen but their families as well. Rebuilt in the early 2000's, all of our cabins have all the comforts of home. Sporting a huge **beach** with multiple water toys for those sunny summer days and a Lodge full of games for when you just can't swim anymore, there's always something for the family to do. A full marina offers watercraft rentals, boat launch, powered dock slips, canoes (free to use), & fish cleaning facility. Rent pontoons, 14' fishing boats, 16' fishing rigs or jet ski's for a fun day or week on the water. Pets are accepted in the lakeside cottages.",
      "Tags": [
        "24-hour front desk service",
        "pool",
        "coffee in lobby"
      ]
    },
    {
      "@search.score": 1.0162708,
      "HotelName": "Campus Commander Hotel",
      "Description": "Easy **access** to campus and steps away from the best shopping corridor in the city. From meetings in town or gameday, enjoy our prime location between the union and proximity to the university stadium.",
      "Tags": [
        "free parking",
        "coffee in lobby",
        "24-hour front desk service"
      ]
    },
    {
      "@search.score": 0.9050383,
      "HotelName": "Lakeside B & B",
      "Description": "Nature is Home on the **beach**. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
      "Tags": [
        "laundry service",
        "concierge",
        "free parking"
      ]
    },
    {
      "@search.score": 0.8955848,
      "HotelName": "Windy Ocean Motel",
      "Description": "Oceanfront hotel overlooking the **beach** features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away.",
      "Tags": [
        "pool",
        "air conditioning",
        "bar"
      ]
    },
    {
      "@search.score": 0.83636594,
      "HotelName": "Happy Lake Resort & Restaurant",
      "Description": "The largest year-round resort in the area offering more of everything for your vacation – at the best value! What can you enjoy while at the resort, aside from the mile-long sandy **beaches** of the lake? Check out our activities sure to excite both young and young-at-heart guests. We have it all, including being named “Property of the Year” and a “Top Ten Resort” by top publications.",
      "Tags": [
        "pool",
        "bar",
        "restaurant"
      ]
    },
    {
      "@search.score": 0.7808502,
      "HotelName": "Swirling Currents Hotel",
      "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking **access** to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs. ",
      "Tags": [
        "air conditioning",
        "laundry service",
        "24-hour front desk service"
      ]
    }
  ]
}
```

In the *after* query, repeat the search, this time boosting results with the term *beach* over the term *access*. A human readable version of the query is `search=Description:beach^2 access`. Depending on your client, you might need to express `^2` as `%5E2`.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "Description:beach^2 access",
    "queryType": "full",
    "select": "HotelName, Description, Tags",
    "searchFields": "HotelName, Description, Tags",
    "count": true
}
```

After you boost the term *beach*, the match on Campus Commander Hotel moves down to fifth place.

```json
{
  "@odata.count": 6,
  "value": [
    {
      "@search.score": 2.137338,
      "HotelName": "Johnson's Family Resort",
      "Description": "Family oriented resort located in the heart of the northland. Operated since 1962 by the Smith family, we have grown into one of the largest family resorts in the state. The home of excellent Smallmouth Bass fishing with 10 small cabins, we're a home not only to fishermen but their families as well. Rebuilt in the early 2000's, all of our cabins have all the comforts of home. Sporting a huge beach with multiple water toys for those sunny summer days and a Lodge full of games for when you just can't swim anymore, there's always something for the family to do. A full marina offers watercraft rentals, boat launch, powered dock slips, canoes (free to use), & fish cleaning facility. Rent pontoons, 14' fishing boats, 16' fishing rigs or jet ski's for a fun day or week on the water. Pets are accepted in the lakeside cottages.",
      "Tags": [
        "24-hour front desk service",
        "pool",
        "coffee in lobby"
      ]
    },
    {
      "@search.score": 1.8100766,
      "HotelName": "Lakeside B & B",
      "Description": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
      "Tags": [
        "laundry service",
        "concierge",
        "free parking"
      ]
    },
    {
      "@search.score": 1.7911696,
      "HotelName": "Windy Ocean Motel",
      "Description": "Oceanfront hotel overlooking the beach features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away.",
      "Tags": [
        "pool",
        "air conditioning",
        "bar"
      ]
    },
    {
      "@search.score": 1.6727319,
      "HotelName": "Happy Lake Resort & Restaurant",
      "Description": "The largest year-round resort in the area offering more of everything for your vacation – at the best value! What can you enjoy while at the resort, aside from the mile-long sandy beaches of the lake? Check out our activities sure to excite both young and young-at-heart guests. We have it all, including being named “Property of the Year” and a “Top Ten Resort” by top publications.",
      "Tags": [
        "pool",
        "bar",
        "restaurant"
      ]
    },
    {
      "@search.score": 1.0162708,
      "HotelName": "Campus Commander Hotel",
      "Description": "Easy access to campus and steps away from the best shopping corridor in the city. From meetings in town or gameday, enjoy our prime location between the union and proximity to the university stadium.",
      "Tags": [
        "free parking",
        "coffee in lobby",
        "24-hour front desk service"
      ]
    },
    {
      "@search.score": 0.7808502,
      "HotelName": "Swirling Currents Hotel",
      "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs. ",
      "Tags": [
        "air conditioning",
        "laundry service",
        "24-hour front desk service"
      ]
    }
  ]
}
```

<!-- Consider a scoring profile that boosts matches in a certain field, such as "genre" in a music app. Term boosting could be used to further boost certain search terms higher than others. For example, "rock^2 electronic" will boost documents that contain the search terms in the "genre" field higher than other searchable fields in the index. Furthermore, documents that contain the search term "rock" will be ranked higher than the other search term "electronic" as a result of the term boost value (2). -->

## Example 5: Regex

A regular expression search finds a match based on the contents between forward slashes `/` and lower-case strings, as documented in the [RegExp class](https://lucene.apache.org/core/6_6_1/core/org/apache/lucene/util/automaton/RegExp.html).

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "HotelName:/(Mo|Ho)tel/",
    "queryType": "full",
    "select": "HotelName",
    "count": true
}
```

The response for this query should look similar to the following example (trimmed for brevity):

```json
{
  "@odata.count": 25,
  "value": [
    {
      "@search.score": 1,
      "HotelName": "Country Residence Hotel"
    },
    {
      "@search.score": 1,
      "HotelName": "Downtown Mix Hotel"
    },
    {
      "@search.score": 1,
      "HotelName": "Gastronomic Landscape Hotel"
    },
    . . . 
    {
      "@search.score": 1,
      "HotelName": "Trails End Motel"
    },
    {
      "@search.score": 1,
      "HotelName": "Nordick's Valley Motel"
    },
    {
      "@search.score": 1,
      "HotelName": "King's Cellar Hotel"
    }
  ]
}
```

> [!Note]
> Regex queries are not [analyzed](./search-lucene-query-architecture.md#stage-2-lexical-analysis). The only transformation performed on partial query terms is lower casing.
>

## Example 6: Wildcard search

You can use generally recognized syntax for multiple (`*`) or single (`?`) character wildcard searches. The Lucene query parser supports the use of these symbols with a single term, and not a phrase.

In this query, search for hotel names that contain the prefix *sc*. You can't use a `*` or `?` symbol as the first character of a search.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-09-01
{
    "search": "HotelName:sc*",
    "queryType": "full",
    "select": "HotelName",
    "count": true
}
```

The response for this query should look similar to the following example:

```json
{
  "@odata.count": 1,
  "value": [
    {
      "@search.score": 1,
      "HotelName": "Waterfront Scottish Inn"
    }
  ]
}
```

> [!Note]
> Wildcard queries are not [analyzed](./search-lucene-query-architecture.md#stage-2-lexical-analysis). The only transformation performed on partial query terms is lower casing.
>

## Related content

Try specifying queries in code. The following link covers how to set up search queries using the Azure SDKs.

+ [Quickstart: Full-text search](search-get-started-text.md)

More syntax reference, query architecture, and examples can be found in the following articles:

+ [Full text search in Azure AI Search](search-lucene-query-architecture.md)
+ [Simple query syntax](query-simple-syntax.md)
+ [Lucene query syntax in Azure AI Search](query-lucene-syntax.md)
+ [OData $filter syntax in Azure AI Search](search-query-odata-filter.md)
