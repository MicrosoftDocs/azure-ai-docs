---
manager: nitinme
author: haileytapia
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/03/2025
---

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An [Azure OpenAI resource](/azure/ai-services/openai/how-to/create-resource).
  - [Choose a region](/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) that supports the chat completion model you want to use (gpt-4o, gpt-4o-mini, or an equivalent model).
  - [Deploy the chat completion model](/azure/ai-foundry/how-to/deploy-models-openai) in Azure AI Foundry or [use another approach](/azure/ai-services/openai/how-to/working-with-models).
- An [Azure AI Search resource](../../search-create-service-portal.md).
  - We recommend using the Basic tier or higher.
  - [Enable semantic ranking](../../semantic-how-to-enable-disable.md).
- [Visual Studio Code](https://code.visualstudio.com/download) with the [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) .

## Download file

[Download a .rest file](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-RAG) from GitHub to send the requests in this quickstart. For more information, see [Downloading files from GitHub](https://docs.github.com/get-started/start-your-journey/downloading-files-from-github).

You can also start a new file on your local system and create requests manually by using the instructions in this article.

## Configure access

Requests to the search endpoint must be authenticated and authorized. You can use API keys or roles for this task. Keys are easier to start with, but roles are more secure. This quickstart assumes roles.

You're setting up two clients, so you need permissions on both resources.

Azure AI Search is receiving the query request from your local system. Assign yourself the **Search Index Data Reader** role assignment if the hotels sample index already exists. If it doesn't exist, assign yourself **Search Service Contributor** and **Search Index Data Contributor** roles so that you can create and query the index.

Azure OpenAI is receiving the query and the search results from your local system. Assign yourself the **Cognitive Services OpenAI User** role on Azure OpenAI.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. Configure Azure AI Search for role-based access:

    1. In the Azure portal, find your Azure AI Search service.

    1. On the left menu, select **Settings** > **Keys**, and then select either **Role-based access control** or **Both**.

1. Assign roles:

    1. On the left menu, select **Access control (IAM)**.

    1. On Azure AI Search, select these roles to create, load, and query a search index, and then assign them to your Microsoft Entra ID user identity:

       - **Search Index Data Contributor**
       - **Search Service Contributor**

    1. On Azure OpenAI, select **Access control (IAM)** to assign this role to yourself on Azure OpenAI:

       - **Cognitive Services OpenAI User**

It can take several minutes for permissions to take effect.

## Create an index

A search index provides grounding data for the chat model. We recommend the hotels-sample-index, which can be created in minutes and runs on any search service tier. This index is created using built-in sample data.

1. In the Azure portal, [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, select [**Import data**](../../search-get-started-portal.md) to start the wizard.

1. On the **Connect to your data** page, select **Samples** from the dropdown list.

1. Choose the **hotels-sample**.

1. Select **Next** through the remaining pages, accepting the default values.

1. Once the index is created, select **Search management** > **Indexes** from the left menu to open the index.

1. Select **Edit JSON**. 

1. Scroll to the end of the index, where you can find placeholders for constructs that can be added to an index.

   ```json
   "analyzers": [],
   "tokenizers": [],
   "tokenFilters": [],
   "charFilters": [],
   "normalizers": [],
   ```

1. On a new line after "normalizers", paste in the following semantic configuration. This example specifies a `"defaultConfiguration"`, which is important to the running of this quickstart.

    ```json
    "semantic":{
       "defaultConfiguration":"semantic-config",
       "configurations":[
          {
             "name":"semantic-config",
             "prioritizedFields":{
                "titleField":{
                   "fieldName":"HotelName"
                },
                "prioritizedContentFields":[
                   {
                      "fieldName":"Description"
                   }
                ],
                "prioritizedKeywordsFields":[
                   {
                      "fieldName":"Category"
                   },
                   {
                      "fieldName":"Tags"
                   }
                ]
             }
          }
       ]
    },
    ```

1. **Save** your changes.

1. Run the following query in [Search Explorer](../../search-explorer.md) to test your index: `complimentary breakfast`.

   Output should look similar to the following example. Results that are returned directly from the search engine consist of fields and their verbatim values, along with metadata like a search score and a semantic ranking score and caption if you use semantic ranker. We used a [select statement](../../search-query-odata-select.md) to return just the HotelName, Description, and Tags fields.

   ```
   {
   "@odata.count": 18,
   "@search.answers": [],
   "value": [
      {
         "@search.score": 2.2896252,
         "@search.rerankerScore": 2.506816864013672,
         "@search.captions": [
         {
            "text": "Head Wind Resort. Suite. coffee in lobby\r\nfree wifi\r\nview. The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a **complimentary continental breakfast** in the lobby, and free Wi-Fi throughout the hotel..",
            "highlights": ""
         }
         ],
         "HotelName": "Head Wind Resort",
         "Description": "The best of old town hospitality combined with views of the river and cool breezes off the prairie. Our penthouse suites offer views for miles and the rooftop plaza is open to all guests from sunset to 10 p.m. Enjoy a complimentary continental breakfast in the lobby, and free Wi-Fi throughout the hotel.",
         "Tags": [
         "coffee in lobby",
         "free wifi",
         "view"
         ]
      },
      {
         "@search.score": 2.2158256,
         "@search.rerankerScore": 2.288334846496582,
         "@search.captions": [
         {
            "text": "Swan Bird Lake Inn. Budget. continental breakfast\r\nfree wifi\r\n24-hour front desk service. We serve a continental-style breakfast each morning, featuring a variety of food and drinks. Our locally made, oh-so-soft, caramel cinnamon rolls are a favorite with our guests. Other breakfast items include coffee, orange juice, milk, cereal, instant oatmeal, bagels, and muffins..",
            "highlights": ""
         }
         ],
         "HotelName": "Swan Bird Lake Inn",
         "Description": "We serve a continental-style breakfast each morning, featuring a variety of food and drinks. Our locally made, oh-so-soft, caramel cinnamon rolls are a favorite with our guests. Other breakfast items include coffee, orange juice, milk, cereal, instant oatmeal, bagels, and muffins.",
         "Tags": [
         "continental breakfast",
         "free wifi",
         "24-hour front desk service"
         ]
      },
      {
         "@search.score": 0.92481667,
         "@search.rerankerScore": 2.221315860748291,
         "@search.captions": [
         {
            "text": "White Mountain Lodge & Suites. Resort and Spa. continental breakfast\r\npool\r\nrestaurant. Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings..",
            "highlights": ""
         }
         ],
         "HotelName": "White Mountain Lodge & Suites",
         "Description": "Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings.",
         "Tags": [
         "continental breakfast",
         "pool",
         "restaurant"
         ]
      },
      . . .
   ]}
   ```

## Get service endpoints

In the remaining sections, you set up API calls to Azure OpenAI and Azure AI Search. Get the service endpoints so that you can provide them as variables in your code.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. [Find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

1. On the **Overview** home page, copy the URL. An example endpoint might look like `https://example.search.windows.net`. 

1. [Find your Azure OpenAI service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.CognitiveServices%2Faccounts).

1. On the **Overview** home page, select the link to view the endpoints. Copy the URL. An example endpoint might look like `https://example.openai.azure.com/`.


<!-- MODIFY THIS -->
## Set up the client

In this quickstart, you use a REST client and the [Azure AI Search REST APIs](/rest/api/searchservice) to implement the RAG pattern.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for this quickstart.

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-rag) to start with a finished project or follow these steps to create your own. 

1. Start Visual Studio Code and open the [quickstart-rag.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-rag/quickstart-rag.rest) file or create a new file.

1. At the top, set environment variables for your search service, authorization, and index name.

   + For @searchURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @personalAccessToken, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal access token.

1. To test the connection, send your first request.

   ```http
   ### List existing indexes by name (verify the connection)
    GET  {{searchUrl}}/indexes?api-version=2025-05-01-preview&$select=name  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
   ```

1. Select **Sent request**.

   :::image type="content" source="../../media/search-get-started-semantic/visual-studio-code-send-request.png" alt-text="Screenshot of the REST client send request link.":::

1. Output for this GET request returns... TBD

## Set up the query and chat thread

This section uses Visual Studio Code and REST to call the chat completion APIs on Azure OpenAI.

<!-- CODE TBD -->

## Send a complex RAG query

Azure AI Search supports [complex types](../../search-howto-complex-data-types.md) for nested JSON structures. In the hotels-sample-index, `Address` is an example of a complex type, consisting of `Address.StreetAddress`, `Address.City`, `Address.StateProvince`, `Address.PostalCode`, and `Address.Country`. The index also has complex collection of `Rooms` for each hotel.

If your index has complex types, your query can provide those fields if you first convert the search results output to JSON, and then pass the JSON to the chat model. The following example adds complex types to the request. The formatting instructions include a JSON specification.

<!-- CODE TBD -->

## Troubleshooting errors

<!-- CODE TBD -->

## Clean up

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by using the **All resources** or **Resource groups** link in the leftmost pane.







[!INCLUDE [Semantic ranker introduction](semantic-ranker-intro.md)]

## Set up the client

In this quickstart, you use a REST client and the [Azure AI Search REST APIs](/rest/api/searchservice) to configure and use a semantic ranker.

We recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for this quickstart.

> [!TIP]
> You can [download the source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-search) to start with a finished project or follow these steps to create your own. 

1. Start Visual Studio Code and open the [semantic-search-index-update.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-semantic-search/semantic-search-index-update.rest) file or create a new file.

1. At the top, set environment variables for your search service, authorization, and index name.

   + For @searchURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @personalAccessToken, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal access token.

1. To test the connection, send your first request.

   ```http
   ### List existing indexes by name (verify the connection)
    GET  {{searchUrl}}/indexes?api-version=2025-05-01-preview&$select=name  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
   ```

1. Select **Sent request**.

   :::image type="content" source="../../media/search-get-started-semantic/visual-studio-code-send-request.png" alt-text="Screenshot of the REST client send request link.":::

1. Output for this GET request returns a list of existing indexes. You should get an HTTP 200 Success status code and a list of indexes, including hotels-sample-index used in this quickstart.

## Update the index

To update an index using the REST API, you must provide the entire schema, plus the modifications you want to make. This request provides hotels-sample-index schema, plus the semantic configuration. The modification consists of the following JSON.

```json
"semantic": {
   "configurations": [
   {
      "name": "semantic-config",
      "flightingOptIn": false,
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

1. Formulate a POST request specifying the index name, operation, and full JSON schema. All required elements of the schema must be present. This request includes the full schema for hotels-sample-index plus the semantic configuration.

    ```http
    POST  {{searchUrl}}/indexes?api-version=2025-05-01-preview  HTTP/1.1
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
      "suggesters": [
        {
          "name": "sg",
          "searchMode": "analyzingInfixMatching",
          "sourceFields": ["Address/City", "Address/Country", "Rooms/Type", "Rooms/Tags"]
        }
      ],
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
            "flightingOptIn": false,
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

1. Select **Sent request**.

1. Output for this POST request is an HTTP 200 Success status message.

## Run semantic queries

Required semantic parameters include `query_type` and `semantic_configuration_name`. Here's an example of a basic semantic query using the minimum parameters.

1. Open the [semantic-search-query.rest](https://github.com/Azure-Samples/azure-search-rest-samples/blob/main/Quickstart-semantic-search/semantic-search-query.rest) file or create a new file.

1. At the top of the file, set environment variables for your search service, authorization, and index name.

   + For @searchURL, sign in to the Azure portal and copy the URL from the search service **Overview** page.

   + For @personalAccessToken, follow the instructions in [Connect without keys](../../search-get-started-rbac.md) to get your personal access token.

1. Test the connection with a GET request that returns the hotels-sample-index.

    ```http
    GET  {{searchUrl}}/indexes/hotels-sample-index?api-version=2025-05-01-preview  HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
    ```

1. Send a query that includes the semantic query type and configuration name.

   ```http
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-05-01-preview  HTTP/1.1
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
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-05-01-preview  HTTP/1.1
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
    POST {{searchUrl}}/indexes/hotels-sample-index/docs/search?api-version=2025-05-01-preview  HTTP/1.1
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

   Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, considering using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../search-agentic-retrieval-concept.md).

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
