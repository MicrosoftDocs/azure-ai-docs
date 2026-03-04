---
manager: nitinme
author: heidisteen
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 03/04/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index and query the index.

Semantic ranking is query-side functionality that uses machine reading comprehension to rescore search results, promoting the most semantically relevant matches to the top of the list. You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for informational or descriptive text.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields attributed as `searchable` and `retrievable`.  This quickstart assumes the [hotels-sample](../../search-get-started-portal.md) index.

+ [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

+ [Git](https://git-scm.com/downloads) to clone the sample repository.

+ The [Azure CLI](/cli/azure/install-azure-cli) for keyless authentication with Microsoft Entra ID.

## Configure access

[!INCLUDE [resource authentication](../resource-authentication-semantic.md)]

## Get endpoint

[!INCLUDE [resource endpoint](../resource-endpoint.md)]

## Start with an index

[!INCLUDE [start with an index](semantic-ranker-index.md)]

## Set up the environment

1. Use Git to clone the sample repository.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-rest-samples
    ```

1. Navigate to the quickstart folder and open it in Visual Studio Code.

    ```bash
    cd azure-search-rest-samples/Quickstart-semantic-ranking
    code .
    ```

1. In `semantic-index-update.rest`, replace the placeholder value for `@searchUrl` with the URL you obtained in [Get endpoint](#get-endpoint).

1. Repeat the previous step for `semantic-query.rest`.

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

1. For keyless authentication with Microsoft Entra ID, generate an access token.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
    ```

1. In both `.rest` files, replace the placeholder value for `@personalAccessToken` with the token from the previous step.

## Run the code

1. Open `semantic-index-update.rest`.

1. Select **Send Request** on the first GET request to verify your connection.

    A response should appear in an adjacent pane. If you have existing indexes, they're listed by name. If the HTTP code is `200 OK`, you're ready to proceed.

1. Send the `### Update the hotels-sample index to include a semantic configuration` request to add a semantic configuration to the index.

    If you get a `400 Bad Request` error, your index schema differs from the sample. Send the `### Get the schema of the index` request, copy the response JSON, add the `semantic` section from the source code to the JSON, and replace the PUT request body with your merged schema.

1. Switch to `semantic-query.rest` and send the requests sequentially: a simple query for baseline comparison, and then semantic queries with ranking, captions, and answers.

### Output

The `Send a search query to the hotels-sample index` request returns results ranked by BM25 relevance, which is indicated by the `@search.score` field.

```json
{
  "@odata.count": 30,
  "value": [
    {
      "@search.score": 5.004435,
      "HotelId": "2",
      "HotelName": "Old Century Hotel",
      "Description": "The hotel is situated in a nineteenth century plaza..."
    },
    // Trimmed for brevity
  ]
}
```

The `Send a search query to the hotels-sample index with semantic ranking` request adds `@search.rerankerScore`. Notice that the order changes from the simple query.

```json
{
  "@odata.count": 30,
  "@search.answers": [],
  "value": [
    {
      "@search.score": 4.555706,
      "@search.rerankerScore": 2.613231658935547,
      "HotelId": "24",
      "HotelName": "Uptown Chic Hotel",
      "Description": "Chic hotel near the city. High-rise hotel in downtown..."
    },
    // Trimmed for brevity
  ]
}
```

The `Return captions in the query` request adds `@search.captions` with extracted text and highlights.

```json
{
  "value": [
    {
      "@search.score": 4.555706,
      "@search.rerankerScore": 2.613231658935547,
      "@search.captions": [
        {
          "text": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to theaters, art galleries, restaurants and shops...",
          "highlights": "Chic hotel near the city. High-rise hotel in downtown, within walking distance to<em> theaters, </em>art galleries, restaurants and shops..."
        }
      ],
      "HotelId": "24",
      "HotelName": "Uptown Chic Hotel"
    },
    // Trimmed for brevity
  ]
}
```

The `Return semantic answers in the query` request returns an extractive answer in `@search.answers` when the query is phrased as a question.

```json
{
  "@odata.count": 46,
  "@search.answers": [
    {
      "key": "38",
      "text": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the library by night...",
      "highlights": "Nature is Home on the beach. Explore the shore by day, and then come home to our shared living space to relax around a stone fireplace, sip something warm, and explore the<em> library </em>by night...",
      "score": 0.9829999804496765
    }
  ],
  "value": [
    {
      "@search.score": 2.060124,
      "@search.rerankerScore": 2.124817371368408,
      "@search.captions": [
        {
          "text": "This classic hotel is fully-refurbished and ideally located on the main commercial artery of the city...",
          "highlights": "This classic hotel is<em> fully-refurbished </em>and ideally located on the main commercial artery of the city..."
        }
      ],
      "HotelId": "1",
      "HotelName": "Stay-Kay City Hotel"
    },
    // Trimmed for brevity
  ]
}
```

## Understand the code

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've run the code, let's break down the key steps:

1. [Configuration and authentication](#configuration-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Query the index](#query-the-index)

### Configuration and authentication

Both `.rest` files define variables at the top for reuse across all requests.

```http
@searchUrl = PUT-YOUR-SEARCH-SERVICE-URL-HERE
@personalAccessToken = PUT-YOUR-PERSONAL-ACCESS-TOKEN-HERE
@api-version = 2025-09-01
```

Key takeaways:

+ `@searchUrl` is the endpoint of your search service.
+ `@personalAccessToken` is a Microsoft Entra ID token obtained from the Azure CLI. This replaces API keys with keyless authentication.
+ `Authorization: Bearer {{personalAccessToken}}` is included in every request header for authentication.

### Update the index with a semantic configuration

The `### Update the hotels-sample index to include a semantic configuration` request in `semantic-index-update.rest` sends the full index schema along with a new `semantic` section. The REST API requires the complete schema for any update operation, so you can't send only the semantic configuration.

The key addition is the `semantic` section:

```json
"semantic": {
    "configurations": [
        {
            "name": "semantic-config",
            "rankingOrder":
                "BoostedRerankerScore",
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
```

Key takeaways:

+ `titleField` identifies which field contains the document title for semantic evaluation.
+ `prioritizedContentFields` identifies the main content fields. Semantic ranker evaluates these first when scoring relevance.
+ `prioritizedKeywordsFields` identifies keyword or tag fields for additional context.
+ `rankingOrder: BoostedRerankerScore` combines the BM25 score with the semantic reranker score.
+ The REST API requires the full schema for PUT operations. Only the `semantic` section is new; all other fields are unchanged.

### Query the index

The requests in `semantic-query.rest` progress from a simple keyword search to semantic ranking with captions and answers. All queries are POST requests to the [Documents - Search Post](/rest/api/searchservice/documents/search-post) (REST API).

#### Simple query

The `### Send a search query to the hotels-sample index` request is a simple keyword search that doesn't use semantic ranking. It serves as a baseline for comparing results with and without semantic reranking.

```json
{
    "search":
        "walking distance to live music",
    "select":
        "HotelId, HotelName, Description",
    "count": true,
    "queryType": "simple"
}
```

Key takeaways:

+ `queryType: "simple"` uses the default BM25 ranking algorithm.
+ Results are ranked by keyword relevance (`@search.score`) only.

#### Semantic query (no captions, no answers)

The `### Send a search query to the hotels-sample index with semantic ranking` request adds semantic ranking. The following JSON shows the minimum requirement for invoking semantic ranking.

```json
{
    "search":
        "walking distance to live music",
    "select":
        "HotelId, HotelName, Description",
    "count": true,
    "queryType": "semantic",
    "semanticConfiguration": "semantic-config"
}
```

Key takeaways:

+ `queryType: "semantic"` enables semantic ranking on the query.
+ `semanticConfiguration` specifies which semantic configuration to use.

#### Semantic query with captions

The `### Return captions in the query` request adds captions to extract the most relevant passages from each result, with hit highlighting applied to the important terms and phrases.

```json
{
    "search":
        "walking distance to live music",
    "select":
        "HotelId, HotelName, Description",
    "count": true,
    "queryType": "semantic",
    "semanticConfiguration": "semantic-config",
    "captions": "extractive|highlight-true"
}
```

Key takeaways:

+ `captions: "extractive|highlight-true"` enables extractive captions with `<em>` tags around important terms.
+ Captions appear in the `@search.captions` array for each result.

#### Semantic query with answers

The `### Return semantic answers in the query` request adds semantic answers. It uses a question as the search text because semantic answers work best when the query is phrased as a question. The answer is a verbatim passage extracted from your index, not a composed response from a chat completion model.

The query and the indexed content must be closely aligned for an answer to be returned. If no candidate meets the confidence threshold, the response doesn't include an answer. This example uses a question that's known to produce a result so that you can see the syntax. If answers aren't useful for your scenario, omit the `answers` parameter from your request. For composed answers, consider a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

```json
{
    "search":
        "what's a good hotel for people who like to read",
    "select":
        "HotelId, HotelName, Description",
    "count": true,
    "queryType": "semantic",
    "semanticConfiguration": "semantic-config",
    "captions": "extractive|highlight-true",
    "answers": "extractive"
}
```

Key takeaways:

+ `answers: "extractive"` enables extractive answers for question-like queries.
+ Answers appear in the top-level `@search.answers` array, separate from individual results.
+ Answers are verbatim content extracted from your index, not generated text.
