---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 06/27/2025
---

In this quickstart, you learn about the index and query modifications that invoke semantic ranker.

In Azure AI Search, [semantic ranking](../../semantic-search-overview.md) is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and the query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort. Semantic ranking is also required for [agentic retrieval (preview)](../../search-agentic-retrieval-concept.md).

You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective on content that's informational or descriptive.

In this quickstart:

> [!div class="checklist"]
> - Add a semantic configuration to a search index
> - Add semantic parameters to a query

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](../../search-create-service-portal.md), at Basic tier or higher, with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ A [new or existing index](../../search-how-to-create-search-index.md) with descriptive or verbose text fields, attributed as retrievable in your index. 

## Configure access

You can connect to your Azure AI Search service [using API keys](../../search-security-api-keys.md) or Microsoft Entra ID with role assignments. Keys are easier to start with, but roles are more secure.

To configure the recommended role-based access:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Settings** > **Keys**.

1. Under **API Access control**, select **Both**.

   This option enables both key-based and keyless authentication. After you assign roles, you can return to this step and select **Role-based access control**.

1. From the left pane, select **Access control (IAM)**.

1. Select **Add** > **Add role assignment**.

1. Assign the **Search Service Contributor** and **Search Index Data Contributor** roles to your user account.

For more information, see [Connect to Azure AI Search using roles](../../search-security-rbac.md).

## Start with an index

This quickstart assumes an existing index, modified to include a semantic configuration. We recommend the [hotels-sample-index](../../search-get-started-portal.md) that you can create in minutes using an Azure portal wizard.

If you don't have access to the Azure portal, you can create a hotels-quickstart-index by following the instructions in [Quickstart: Full text search](../../search-get-started-text.md).

Both indexes have a "Description" field that's suitable for demonstrating the semantic ranker.

1. Sign in to the [Azure portal](https://portal.azure.com/) and find your search service.

1. Under **Search management** > **Indexes**, open the hotels index. Make sure the index doesn't have a semantic configuration.

   :::image type="content" source="../../media/search-get-started-semantic/no-semantic-configuration.png" alt-text="Screenshot of an empty semantic configuration page in the Azure portal.":::

1. In **Search explorer**, enter this search string "good trails for running or biking and outdoor activities" so that you can view the response *before* semantic ranking is applied. Your response should be similar to the following example, as scored by the default L1 ranker for full text search. For readability, the example below selects just the "HotelName" and "Description" fields.

   ```json
   "@odata.count": 11,
   "value": [
        {
          "@search.score": 3.5593667,
          "HotelName": "Winter Panorama Resort",
          "Description": "Plenty of great skiing, outdoor ice skating, sleigh rides, tubing and snow biking. Yoga, group exercise classes and outdoor hockey are available year-round, plus numerous options for shopping as well as great spa services. Newly-renovated with large rooms, free 24-hr airport shuttle & a new restaurant. Rooms/suites offer mini-fridges & 49-inch HDTVs."
        },
        {
          "@search.score": 3.0720026,
          "HotelName": "Good Business Hotel",
          "Description": "1 Mile from the airport. Free WiFi, Outdoor Pool, Complimentary Airport Shuttle, 6 miles from Lake Lanier & 10 miles from downtown. Our business center includes printers, a copy machine, fax, and a work area."
        },
        {
          "@search.score": 2.2779887,
          "HotelName": "Trails End Motel",
          "Description": "Only 8 miles from Downtown. On-site bar/restaurant, Free hot breakfast buffet, Free wireless internet, All non-smoking hotel. Only 15 miles from airport."
        },
        {
          "@search.score": 1.7617674,
          "HotelName": "Royal Cottage Resort",
          "Description": "Your home away from home. Brand new fully equipped premium rooms, fast WiFi, full kitchen, washer & dryer, fitness center. Inner courtyard includes water features and outdoor seating. All units include fireplaces and small outdoor balconies. Pets accepted."
        },
        {
          "@search.score": 1.5327098,
          "HotelName": "City Center Summer Wind Resort",
          "Description": "Eco-friendly from our gardens to table, with a rooftop serenity pool and outdoor seating to take in the sunset. Just steps away from the Convention Center. Located in the heart of downtown with modern rooms with stunning city views, 24-7 dining options, free WiFi and easy valet parking."
        },
        {
          "@search.score": 1.5104222,
          "HotelName": "Foot Happy Suites",
          "Description": "Downtown in the heart of the business district. Close to everything. Leave your car behind and walk to the park, shopping, and restaurants. Or grab one of our bikes and take your explorations a little further."
        },
        {
          "@search.score": 1.4453387,
          "HotelName": "Economy Universe Motel",
          "Description": "Local, family-run hotel in bustling downtown Redmond. We are a pet-friendly establishment, near expansive Marymoor park, haven to pet owners, joggers, and sports enthusiasts. Close to the highway and just a short drive away from major cities."
        },
        {
          "@search.score": 1.3732712,
          "HotelName": "Starlight Suites",
          "Description": "Complimentary Airport Shuttle & WiFi. Book Now and save - Spacious All Suite Hotel, Indoor Outdoor Pool, Fitness Center, Florida Green certified, Complimentary Coffee, HDTV"
        },
        {
          "@search.score": 1.2054883,
          "HotelName": "Happy Lake Resort & Restaurant",
          "Description": "The largest year-round resort in the area offering more of everything for your vacation – at the best value! What can you enjoy while at the resort, aside from the mile-long sandy beaches of the lake? Check out our activities sure to excite both young and young-at-heart guests. We have it all, including being named “Property of the Year” and a “Top Ten Resort” by top publications."
        },
        {
          "@search.score": 1.161385,
          "HotelName": "White Mountain Lodge & Suites",
          "Description": "Live amongst the trees in the heart of the forest. Hike along our extensive trail system. Visit the Natural Hot Springs, or enjoy our signature hot stone massage in the Cathedral of Firs. Relax in the meditation gardens, or join new friends around the communal firepit. Weekend evening entertainment on the patio features special guest musicians or poetry readings."
        },
        {
          "@search.score": 0.8955848,
          "HotelName": "Windy Ocean Motel",
          "Description": "Oceanfront hotel overlooking the beach features rooms with a private balcony and 2 indoor and outdoor pools. Inspired by the natural beauty of the island, each room includes an original painting of local scenes by the owner. Rooms include a mini fridge, Keurig coffee maker, and flatscreen TV. Various shops and art entertainment are on the boardwalk, just steps away."
        }
      ]
   ```

Later, you can try this query again after semantic ranking is configured to see how the response changes.

> [!TIP]
> You can add a semantic configuration in the Azure portal. However, if you want to learn how to add a semantic configuration programmatically, continue with the instructions in this quickstart.
>
