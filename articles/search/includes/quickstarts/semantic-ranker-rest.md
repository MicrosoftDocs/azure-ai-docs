---
manager: nitinme
author: heidisteen
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/20/2025
---

[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, you use a REST client and the [Azure AI Search REST APIs](/rest/api/searchservice) to configure and use a semantic ranker.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for this quickstart.

> [!TIP]
> You can download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-ranking) to start with a finished project or follow these steps to create your own.

1. Start Visual Studio Code and open the [semantic-index-update.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-semantic-ranking/semantic-index-update.rest) file or create a new file.

1. At the top, set environment variables for your search service, authorization, and index name.

   + For @searchURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @personalAccessToken, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal access token.

1. To test the connection, send your first request.

   ```http
   ### List existing indexes by name (verify the connection)
    GET  {{searchUrl}}/indexes?api-version=2025-09-01&$select=name  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
   ```

1. Select **Send Request**.

   :::image type="content" source="../../media/search-get-started-semantic/visual-studio-code-send-request.png" alt-text="Screenshot of the REST client send request link.":::

1. Output for this GET request returns a list of existing indexes. You should get an HTTP 200 Success status code and a list of indexes, including hotels-sample-index used in this quickstart.

## Update the index

To update an index using the REST API, you must provide the entire schema, plus the modifications you want to make. This request provides hotels-sample-index schema, plus the semantic configuration. The modification consists of the following JSON.

```json
"semantic": {
   "configurations": [
   {
      "name": "semantic-config",
      "rankingOrder": "BoostedRerankerScore",
      "prioritizedFields": {
         "titleField": { "fieldName": "HotelName" },
         "prioritizedContentFields": [{ "fieldName": "Description" }],
         "prioritizedKeywordsFields": [{ "fieldName": "Tags" }]
      }
   }
   ]
}
```

1. Formulate a PUT request specifying the index name, operation, and full JSON schema. All required elements of the schema must be present. This request includes the full schema for hotels-sample-index plus the semantic configuration.

    ```http
    PUT {{searchUrl}}/indexes/hotels-sample-index?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}
    
    {
       "name": "hotels-sample-index",
       "fields": [
           { "name": "HotelId", "type": "Edm.String", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "key": true },
           { "name": "HotelName", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
           { "name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
           { "name": "Description_fr", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "fr.microsoft" },
           { "name": "Category", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
           { "name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
           { "name": "ParkingIncluded", "type": "Edm.Boolean", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true },
           { "name": "LastRenovationDate", "type": "Edm.DateTimeOffset", "searchable": false, "filterable": false, "retrievable": true, "stored": true, "sortable": true, "facetable": false },
           { "name": "Rating", "type": "Edm.Double", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": true, "facetable": true },
           { "name": "Address", "type": "Edm.ComplexType", "fields": [
              { "name": "StreetAddress", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
              { "name": "City", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
              { "name": "StateProvince", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
              { "name": "PostalCode", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
              { "name": "Country", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" }]},
           { "name": "Location", "type": "Edm.GeographyPoint", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": true, "facetable": false },
           { "name": "Rooms", "type": "Collection(Edm.ComplexType)", "fields": [
              { "name": "Description", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "en.microsoft" },
              { "name": "Description_fr", "type": "Edm.String", "searchable": true, "filterable": false, "retrievable": true, "stored": true, "sortable": false, "facetable": false, "analyzer": "fr.microsoft" },
              { "name": "Type", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
              { "name": "BaseRate", "type": "Edm.Double", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true },
              { "name": "BedOptions", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" },
              { "name": "SleepsCount", "type": "Edm.Int64", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true },
              { "name": "SmokingAllowed", "type": "Edm.Boolean", "searchable": false, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true },
              { "name": "Tags", "type": "Collection(Edm.String)", "searchable": true, "filterable": true, "retrievable": true, "stored": true, "sortable": false, "facetable": true, "analyzer": "en.microsoft" }]},
           { "name": "id", "type": "Edm.String", "searchable": false, "filterable": false, "retrievable": false, "stored": true, "sortable": false, "facetable": false },
           { "name": "rid", "type": "Edm.String", "searchable": false, "filterable": false, "retrievable": false, "stored": true, "sortable": false, "facetable": false }],
      "scoringProfiles": [],
      "suggesters": [],
      "analyzers": [],
      "normalizers": [],
      "tokenizers": [],
      "tokenFilters": [],
      "charFilters": [],
      "similarity": {
        "@odata.type": "#Microsoft.Azure.Search.BM25Similarity"
      },
      "semantic": {
        "configurations": [
          {
            "name": "semantic-config",
            "rankingOrder": "BoostedRerankerScore",
            "prioritizedFields": {
              "titleField": {
                "fieldName": "HotelName"
              },
              "prioritizedContentFields": [
                {
                  "fieldName": "Description"
                }
              ],
              "prioritizedKeywordsFields": [
                {
                  "fieldName": "Tags"
                }
              ]
            }
          }
        ]
      }
    }
    ```

1. Select **Send Request**.

1. Output for this POST request is an `HTTP 200 Success` status message.

## Run semantic queries

Required semantic parameters include `query_type` and `semantic_configuration_name`. Here's an example of a basic semantic query using the minimum parameters.

1. Open the [semantic-query.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-semantic-ranking/semantic-query.rest) file or create a new file.

1. At the top of the file, set environment variables for your search service, authorization, and index name.

   + For @searchURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @personalAccessToken, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal access token.

1. Test the connection with a GET request that returns the hotels-sample-index.

    ```http
    GET {{searchUrl}}/indexes/hotels-sample-index?api-version=2025-09-01  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
    ```

1. Send a query that includes the semantic query type and configuration name.

   ```http
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}
    
    {
      "search": "walking distance to live music",
      "select": "HotelId, HotelName, Description",
      "count": true,
      "top": 7,
      "queryType": "simple"
    }
   ```

1. Output consists of JSON search results. Thirteen hotels match the query. The top seven are included in this example.

   ```json
   {
      "@odata.count": 13,
      "@search.answers": [],
      "value": [
        {
          "@search.score": 5.074317,
          "@search.rerankerScore": 2.613231658935547,
          "HotelId": "24",
          "HotelName": "Uptown Chic Hotel",
          "Description": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance."
        },
        {
          "@search.score": 5.5153193,
          "@search.rerankerScore": 2.271434783935547,
          "HotelId": "2",
          "HotelName": "Old Century Hotel",
          "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music."
        },
        {
          "@search.score": 4.8959594,
          "@search.rerankerScore": 1.9861756563186646,
          "HotelId": "4",
          "HotelName": "Sublime Palace Hotel",
          "Description": "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience."
        },
        {
          "@search.score": 0.7334347,
          "@search.rerankerScore": 1.9615401029586792,
          "HotelId": "39",
          "HotelName": "White Mountain Lodge & Suites",
          "Description": "Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings."
        },
        {
          "@search.score": 1.5502293,
          "@search.rerankerScore": 1.9085469245910645,
          "HotelId": "15",
          "HotelName": "By the Market Hotel",
          "Description": "Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service."
        },
        {
          "@search.score": 1.7595702,
          "@search.rerankerScore": 1.90234375,
          "HotelId": "49",
          "HotelName": "Swirling Currents Hotel",
          "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs. "
        },
        {
          "@search.score": 2.0364518,
          "@search.rerankerScore": 1.9012802839279175,
          "HotelId": "31",
          "HotelName": "Country Residence Hotel",
          "Description": "All of the suites feature full-sized kitchens stocked with cookware, separate living and sleeping areas and sofa beds. Some of the larger rooms have fireplaces and patios or balconies. Experience real country hospitality in the heart of bustling Nashville. The most vibrant music scene in the world is just outside your front door."
        }
      ]
    }
    ```

### Return captions

Optionally, you can add captions to extract portions of the text and apply hit highlighting to the important terms and phrases. This query adds captions that include hit highlighting.

1. Add the `captions` parameter and send the request.

    ```http
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}
    
    {
      "search": "walking distance to live music",
      "select": "HotelId, HotelName, Description",
      "count": true,
      "queryType": "semantic",
      "semanticConfiguration": "semantic-config",
      "captions": "extractive|highlight-true"
    }
    ```

1. Output consists of the same results, with the addition of `"@search.captions"`. Here's the JSON for a single document. Each match includes search scores, captions in plain text and highlight formatting, and the select fields.

   ```json
   {
      "@search.score": 5.074317,
      "@search.rerankerScore": 2.613231658935547,
      "@search.captions": [
        {
          "text": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance.",
          "highlights": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops. Visit<em> Seattle Art Museum </em>by day, and then head over to<em> Benaroya Hall </em>to catch the evening's concert performance."
        }
      ],
      "HotelId": "24",
      "HotelName": "Uptown Chic Hotel",
      "Description": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance."
   }
   ```

### Return semantic answers

In this final query, return semantic answers.

Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it won't include composed content like what you might expect from a chat completion model. If the semantic answer isn't useful for your scenario, you can omit `semantic_answers` from your code.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer. For demonstration purposes, the question in this example is designed to get a response so that you can see the syntax.

1. Formulate the request using a search string that asks a question.

    ```http
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}
    
    {
      "search": "what's a good hotel for people who like to read",
      "select": "HotelId, HotelName, Description",
      "count": true,
      "queryType": "semantic",
      "semanticConfiguration": "semantic-config"
      "answers": "extractive"
    }
    ```

1. Output consists of 41 results for the new query, with "@search.answers" for the question in the query about hotels for people who like to read.

   Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

   In this example, the answer is considered as a strong fit for the question.

    ```json
    {
      "@odata.count": 41,
      "@search.answers": [
        {
          "key": "38",
          "text": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
          "highlights": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply.",
          "score": 0.9829999804496765
        }
      ],
      "value": [
        {
          "@search.score": 2.0361428,
          "@search.rerankerScore": 2.124817371368408,
          "HotelId": "1",
          "HotelName": "Stay-Kay City Hotel",
          "Description": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Times Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities."
        },
        {
          "@search.score": 3.759768,
          "@search.rerankerScore": 2.0705394744873047,
          "HotelId": "16",
          "HotelName": "Double Sanctuary Resort",
          "Description": "5 star Luxury Hotel - Biggest Rooms in the city. #1 Hotel in the area listed by Traveler magazine. Free WiFi, Flexible check in/out, Fitness Center & espresso in room."
        },
        {
          "@search.score": 0.7308748,
          "@search.rerankerScore": 2.041472911834717,
          "HotelId": "38",
          "HotelName": "Lakeside B & B",
          "Description": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply."
        },
        {
          "@search.score": 3.391012,
          "@search.rerankerScore": 2.0231292247772217,
          "HotelId": "2",
          "HotelName": "Old Century Hotel",
          "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music."
        },
        {
          "@search.score": 1.3198771,
          "@search.rerankerScore": 2.021622657775879,
          "HotelId": "15",
          "HotelName": "By the Market Hotel",
          "Description": "Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service."
        },
        {
          "@search.score": 1.3983066,
          "@search.rerankerScore": 2.005582809448242,
          "HotelId": "5",
          "HotelName": "Red Tide Hotel",
          "Description": "On entering this charming hotel in Scarlet Harbor, you'll notice an uncommon blend of antiques, original artwork, and contemporary comforts that give this hotel its signature look. Each suite is furnished to accentuate the views and unique characteristics of the building's classic architecture. No two suites are alike. However, all guests are welcome in the mezzanine plaza, the surrounding gardens, and the northside terrace for evening refreshments."
        },
        {
          "@search.score": 1.4815493,
          "@search.rerankerScore": 1.9739465713500977,
          "HotelId": "24",
          "HotelName": "Uptown Chic Hotel",
          "Description": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance."
        }
      ]
    }
    ```
