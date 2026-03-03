---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 03/02/2026
---

This quickstart modifies an existing index to include a semantic configuration. We recommend the hotels-sample index, which you can create in minutes using an Azure portal wizard.

To use a different index, replace the index name, field names in the semantic configuration, and field names in query `select` statements throughout the sample code. Your index should contain descriptive text fields that are attributed as `searchable` and `retrievable`.

To review and query the hotels-sample index before semantic ranking:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Search management** > **Indexes**.

1. Select **hotels-sample**.

1. Select **Semantic configurations** to verify the index doesn't have a semantic configuration.

   :::image type="content" source="../../media/search-get-started-semantic/no-semantic-configuration.png" alt-text="Screenshot of an empty semantic configuration page in the Azure portal.":::

1. Select **Search explorer**, and then select **View** > **JSON view**.

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

   The response should be similar to the following example. This is a full-text query ranked by BM25, so results match on individual query terms and linguistic variants rather than the overall meaning of the query. For example, `walking` matches `walk`, and `live` and `music` match independently rather than as a phrase.

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
      ... // Trimmed for brevity
    ]
   ```

    > [!TIP]
    > This query shows how the response looks before semantic ranking is applied. After you configure a semantic configuration, you can run the same query to see how the response changes.
