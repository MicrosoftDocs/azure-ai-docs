---
manager: nitinme
author: heidisteen
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/30/2026
ai-usage: ai-assisted
---

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to add [semantic ranking](../../semantic-search-overview.md) to an existing search index.

In Azure AI Search, semantic ranking is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort.

You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is most effective for text that's informational or descriptive.

> [!TIP]
> Want to get started right away? Download the [source code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-semantic-ranking) on GitHub.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md) with [semantic ranker enabled](../../semantic-how-to-enable-disable.md).

+ An [index](../../search-how-to-create-search-index.md) with descriptive text fields that are attributed as `searchable` and `retrievable`. This quickstart assumes the [hotels-sample-index](../../search-get-started-portal.md).

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

1. Navigate to the quickstart folder and open it in Visual Studio Code. The folder contains two `.rest` files:

    ```bash
    cd azure-search-rest-samples/Quickstart-semantic-ranking
    code .
    ```

    + `semantic-index-update.rest` for updating the index with a semantic configuration.
    + `semantic-query.rest` for running semantic queries.

1. In both `.rest` files, replace the placeholder value for `@searchUrl` with the URL you obtained in [Get endpoint](#get-endpoint).

1. For keyless authentication with Microsoft Entra ID, sign in to your Azure account. If you have multiple subscriptions, select the one that contains your Azure AI Search service.

    ```azurecli
    az login
    ```

1. Generate an access token.

    ```azurecli
    az account get-access-token --scope https://search.azure.com/.default --query accessToken --output tsv
    ```

1. In both `.rest` files, replace the placeholder value for `@personalAccessToken` with the token you obtained.

## Run the requests

Send each request in sequence to see the full progression from index verification to semantic queries. Select **Send Request** above each HTTP request block in the `.rest` files.

:::image type="content" source="../../media/search-get-started-semantic/visual-studio-code-send-request.png" alt-text="Screenshot of the REST client send request link.":::

1. **Verify the connection.** In `semantic-index-update.rest`, send the first GET request to list existing indexes.

    ```http
    GET {{searchUrl}}/indexes
        ?api-version=2025-09-01&$select=name
        HTTP/1.1
    Authorization: Bearer {{personalAccessToken}}
    ```

   Output is a list of indexes. You should see `hotels-sample-index` in the list.

1. **Update the index with a semantic configuration.** In the same file, send the PUT request. This request provides the full `hotels-sample-index` schema plus the semantic configuration.

   Output is an `HTTP 200 Success` status with the updated index schema.

1. **Run a simple query (no semantic ranking).** In `semantic-query.rest`, send the first POST request for a baseline comparison.

    ```http
    POST {{searchUrl}}/indexes
        /hotels-sample-index/docs/search
        ?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}

    {
      "search":
          "walking distance to live music",
      "select":
          "HotelId, HotelName, Description",
      "count": true,
      "queryType": "simple"
    }
    ```

   Output consists of 13 results ordered by BM25 score.

1. **Run a semantic query.** Send the next POST request to see semantic ranking applied.

    ```http
    POST {{searchUrl}}/indexes
        /hotels-sample-index/docs/search
        ?api-version=2025-09-01  HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer {{personalAccessToken}}

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

   Output consists of the same 13 results, reranked by semantic relevance. Compare the ordering against the simple query results.

1. **Run a semantic query with captions.** Send the next request to add extractive captions with hit highlighting.

1. **Run a semantic query with answers.** Send the final request for a question-like query with extractive answers.

### Output

Output from the captions query adds `@search.captions` to each result. Captions are the most relevant passages in a result. If your index includes larger text, a caption is helpful for extracting the most interesting sentences.

```json
{
    "@search.score": 5.074317,
    "@search.rerankerScore": 2.613231658935547,
    "@search.captions": [
        {
            "text": "Chic hotel near the city...",
            "highlights": "Chic hotel near the city.
                High-rise hotel in downtown,
                within walking distance
                to<em> theaters, </em>art
                galleries, restaurants and
                shops. Visit<em> Seattle Art
                Museum </em>by day, and then
                head over to<em> Benaroya Hall
                </em>to catch the evening's
                concert performance."
        }
    ],
    "HotelId": "24",
    "HotelName": "Uptown Chic Hotel",
    "Description": "Chic hotel near the city..."
}
```

Output from the answers query includes `@search.answers` with a semantic answer (verbatim content) pulled from one of the results that best matches the question.

```json
{
    "@odata.count": 41,
    "@search.answers": [
        {
            "key": "38",
            "text": "Nature is Home on the beach.
                Explore the shore by day, and
                then come home to our shared
                living space to relax around a
                stone fireplace, sip something
                warm, and explore the library
                by night...",
            "highlights": "Nature is Home on the
                beach. Explore the shore by day,
                and then come home to our shared
                living space to relax around a
                stone fireplace, sip something
                warm, and explore the<em>
                library </em>by night...",
            "score": 0.9829999804496765
        }
    ]
}
```

Recall that answers are *verbatim content* pulled from your index and might be missing phrases that a user would expect to see. To get *composed answers* as generated by a chat completion model, consider using a [RAG pattern](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).

## Understand the requests

[!INCLUDE [understand code note](../understand-code-note.md)]

Now that you've sent the requests, let's break down the key steps:

1. [Variables and authentication](#variables-and-authentication)
1. [Update the index with a semantic configuration](#update-the-index-with-a-semantic-configuration)
1. [Semantic query parameters](#semantic-query-parameters)

### Variables and authentication

Each `.rest` file defines variables at the top for reuse across all requests.

```http
@searchUrl=
    PUT-YOUR-SEARCH-SERVICE-URL-HERE
@personalAccessToken=
    PUT-YOUR-PERSONAL-ACCESS-TOKEN-HERE
@api-version = 2025-09-01
```

Key takeaways:

+ `@searchUrl` is your service endpoint URL from the Azure portal.

+ `@personalAccessToken` is a Microsoft Entra ID token obtained from the Azure CLI. This replaces API keys with keyless authentication.

+ `Authorization: Bearer {{personalAccessToken}}` is included in every request header for authentication.

### Update the index with a semantic configuration

The PUT request in `semantic-index-update.rest` sends the full index schema along with a new `semantic` section. The REST API requires the complete schema for any update operation, so you can't send only the semantic configuration.

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

### Semantic query parameters

After the index has a semantic configuration, you can include semantic parameters in POST requests to the [search documents API](/rest/api/searchservice/documents/search-post).

The minimum semantic query includes `queryType` and `semanticConfiguration`:

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

#### Extractive captions

Add the `captions` parameter to extract the most relevant passages from each result with hit highlighting.

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

#### Semantic answers

Add the `answers` parameter using a question-like query to get extractive answers. Semantic ranker can produce an answer to a query string that has the characteristics of a question. The generated answer is extracted verbatim from your content so it doesn't include composed content like what you might expect from a chat completion model.

To produce a semantic answer, the question and answer must be closely aligned, and the model must find content that clearly answers the question. If potential answers fail to meet a confidence threshold, the model doesn't return an answer.

```json
{
    "search":
        "what's a good hotel for people "
        "who like to read",
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

+ For composed answers, consider [RAG patterns](../../retrieval-augmented-generation-overview.md) or [agentic retrieval](../../agentic-retrieval-overview.md).
