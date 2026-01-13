---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/20/2025
---

In this quickstart, you learn how to use [semantic ranking](../../semantic-search-overview.md) by adding a semantic configuration to a search index and adding semantic parameters to a query. You can use the hotels-sample-index or one of your own.

In Azure AI Search, semantic ranking is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and the query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort.

You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective on text that's informational or descriptive.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ A [new or existing index](../../search-how-to-create-search-index.md) with descriptive or verbose text fields that are attributed as retrievable. This quickstart assumes the [hotels-sample-index](../../search-get-started-portal.md).

## Configure access

You can connect to your Azure AI Search service using API keys or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure. For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

To configure role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Settings** > **Keys**.

1. Under **API Access control**, select **Role-based access control** or **Both** if you need time to transition clients to role-based access.

1. From the left pane, select **Access control (IAM)**.

1. Select **Add** > **Add role assignment**.

1. Assign the **Search Service Contributor** and **Search Index Data Contributor** roles to your user account.

## Start with an index

This quickstart assumes an existing index and modifies it to include a semantic configuration. We recommend the [hotels-sample-index](../../search-get-started-portal.md) that you can create in minutes using an Azure portal wizard.

To start with an existing index:

1. Sign in to the [Azure portal](https://portal.azure.com/) and find your search service.

1. Under **Search management** > **Indexes**, select the hotels-sample-index.

1. Select **Semantic configurations** to ensure the index doesn't have a semantic configuration.

   :::image type="content" source="../../media/search-get-started-semantic/no-semantic-configuration.png" alt-text="Screenshot of an empty semantic configuration page in the Azure portal.":::

1. Select **Search explorer**, and then select the **JSON view**.

1. Paste the following JSON into the query editor.

    ```json
    {
      "search": "walking distance to live music",
      "select": "HotelId, HotelName, Description",
      "count": true
    }
    ```

   :::image type="content" source="../../media/search-get-started-semantic/search-explorer-simple-query.png" alt-text="Screenshot of a query in Search Explorer in the portal.":::

1. Select **Search** to run the query.

   This query is a keyword search. The response should be similar to the following example, as scored by the default BM25 L1 ranker for full-text search.

   For readability, the example only selects the `HotelId`, `HotelName`, and `Description` fields. The results contain verbatim matches on the query terms (`walking`, `distance`, `live`, `music`) or linguistic variants (`walk`, `living`).

    ```json
    "@odata.count": 13,
    "value": [
      {
        "@search.score": 5.5153193,
        "HotelId": "2",
        "HotelName": "Old Century Hotel",
        "Description": "The hotel is situated in a nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts. The hotel also regularly hosts events like wine tastings, beer dinners, and live music."
      },
      {
        "@search.score": 5.074317,
        "HotelId": "24",
        "HotelName": "Uptown Chic Hotel",
        "Description": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops. Visit Seattle Art Museum by day, and then head over to Benaroya Hall to catch the evening's concert performance."
      },
      {
        "@search.score": 4.8959594,
        "HotelId": "4",
        "HotelName": "Sublime Palace Hotel",
        "Description": "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 19th century resort, updated for every modern convenience."
      },
      {
        "@search.score": 2.5966604,
        "HotelId": "35",
        "HotelName": "Bellevue Suites",
        "Description": "Comfortable city living in the very center of downtown Bellevue. Newly reimagined, this hotel features apartment-style suites with sleeping, living and work spaces. Located across the street from the Light Rail to downtown. Free shuttle to the airport."
      },
      {
        "@search.score": 2.566386,
        "HotelId": "47",
        "HotelName": "Country Comfort Inn",
        "Description": "Situated conveniently at the north end of the village, the inn is just a short walk from the lake, offering reasonable rates and all the comforts home inlcuding living room suites and functional kitchens. Pets are welcome."
      },
      {
        "@search.score": 2.2405157,
        "HotelId": "9",
        "HotelName": "Smile Up Hotel",
        "Description": "Experience the fresh, modern downtown. Enjoy updated rooms, bold style & prime location. Don't miss our weekend live music series featuring who's new/next on the scene."
      },
      {
        "@search.score": 2.1737604,
        "HotelId": "8",
        "HotelName": "Foot Happy Suites",
        "Description": "Downtown in the heart of the business district. Close to everything. Leave your car behind and walk to the park, shopping, and restaurants. Or grab one of our bikes and take your explorations a little further."
      },
      {
        "@search.score": 2.0364518,
        "HotelId": "31",
        "HotelName": "Country Residence Hotel",
        "Description": "All of the suites feature full-sized kitchens stocked with cookware, separate living and sleeping areas and sofa beds. Some of the larger rooms have fireplaces and patios or balconies. Experience real country hospitality in the heart of bustling Nashville. The most vibrant music scene in the world is just outside your front door."
      },
      {
        "@search.score": 1.7595702,
        "HotelId": "49",
        "HotelName": "Swirling Currents Hotel",
        "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center. Each room comes equipped with a microwave, a coffee maker and a minifridge. In-room entertainment includes complimentary W-Fi and flat-screen TVs. "
      },
      {
        "@search.score": 1.5502293,
        "HotelId": "15",
        "HotelName": "By the Market Hotel",
        "Description": "Book now and Save up to 30%. Central location. Walking distance from the Empire State Building & Times Square, in the Chelsea neighborhood. Brand new rooms. Impeccable service."
      },
      {
        "@search.score": 1.3302404,
        "HotelId": "42",
        "HotelName": "Rock Bottom Resort & Campground",
        "Description": "Rock Bottom is nestled on 20 unspoiled acres on a private cove of Rock Bottom Lake. We feature both lodging and campground accommodations to suit just about every taste. Even though we are out of the traffic of the city, getting there is only a short drive away."
      },
      {
        "@search.score": 0.9050383,
        "HotelId": "38",
        "HotelName": "Lakeside B & B",
        "Description": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night. Save up to 30 percent. Valid Now through the end of the year. Restrictions and blackouts may apply."
      },
      {
        "@search.score": 0.7334347,
        "HotelId": "39",
        "HotelName": "White Mountain Lodge & Suites",
        "Description": "Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings."
      }
    ]
   ```

This query shows how the response looks *before* semantic ranking is applied. Later, you can run the same query after semantic ranking is configured to see how the response changes.

> [!TIP]
> You can add a semantic configuration in the Azure portal. However, if you want to learn how to add a semantic configuration programmatically, continue with this quickstart.
