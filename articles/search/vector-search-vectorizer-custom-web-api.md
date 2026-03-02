---
title: Custom Web API vectorizer
titleSuffix: Azure AI Search
description: Use the Custom Web API vectorizer to integrate your custom code for generating embeddings at query time.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 02/27/2026
ms.update-cycle: 365-days
---

# Custom Web API vectorizer

The **Custom Web API** vectorizer lets you configure search queries to call a web API endpoint that generates embeddings at query time. The required JSON payload structure for the endpoint is described later in this article. Your data is processed in the [geography](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

Although vectorizers are used at query time, you specify them in index definitions and reference them on vector fields through a vector profile. For more information, see [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md).

The custom web API vectorizer is called `WebApiVectorizer` in the REST API. Use the latest stable version of [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) or an Azure SDK package that provides the feature.

## Vectorizer parameters

Parameters are case sensitive.

| Parameter name	 | Description |
|--------------------|-------------|
| `uri` | The URI of the Web API to which the JSON payload is sent. Only the **https** URI scheme is allowed. |
| `httpMethod` | The method used to send the payload. Allowed methods are `PUT` or `POST`. |
| `httpHeaders` | A collection of key-value pairs in which keys represent header names and values represent header values sent to your web API with the payload. The following headers are prohibited in this collection: `Accept`, `Accept-Charset`, `Accept-Encoding`, `Content-Length`, `Content-Type`, `Cookie`, `Host`, `TE`, `Upgrade`, `Via`. |
| `authResourceId` | (Optional) A string that, if set, indicates that this vectorizer uses a managed identity for the connection to the function or app hosting the code. This property takes an application (client) ID or app registration in Microsoft Entra ID in one of these formats: `api://<appId>`, `<appId>/.default`, `api://<appId>/.default`. This value scopes the authentication token retrieved by the query pipeline and sent with the custom web API request to the function or app. Setting this property requires that your search service is [configured for managed identity](search-how-to-managed-identities.md) and your Azure function app is [configured for Microsoft Entra sign-in](/azure/app-service/configure-authentication-provider-aad). |
| `authIdentity` | (Optional) A user-managed identity used by the search service to connect to the function or app hosting the code. You can use either a [system-managed or user-managed identity](search-how-to-managed-identities.md). To use a system-managed identity, leave `authIdentity` blank. |
| `timeout` | (Optional) The timeout for the HTTP client making the API call. It must be formatted as an XSD `dayTimeDuration` value (a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value). For example, `PT60S` means 60 seconds. If not set, the default is 30 seconds. The timeout can be between 1 and 230 seconds. |

## Supported vector query types

The Custom Web API vectorizer supports `text`, `imageUrl`, and `imageBinary` vector queries.

## Sample definition

```json
"vectorizers": [
    {
        "name": "my-custom-web-api-vectorizer",
        "kind": "customWebApi",
        "customWebApiParameters": {
            "uri": "https://contoso.embeddings.com",
            "httpMethod": "POST",
            "httpHeaders": {
                "api-key": "0000000000000000000000000000000000000"
            },
            "timeout": "PT60S",
            "authResourceId": null,
            "authIdentity": null
        }
    }
]
```

## JSON payload structure

The required JSON payload structure for an endpoint used with the Custom Web API vectorizer is the same as the structure used by the Custom Web API skill, discussed in more detail in [the skill documentation](cognitive-search-custom-skill-web-api.md#sample-input-json-structure).

Keep the following considerations in mind when implementing a web API endpoint for the Custom Web API vectorizer.

+ The vectorizer sends only one record at a time in the `values` array when making a request to the endpoint.
+ The vectorizer passes the data to be vectorized in a specific key in the `data` JSON object in the request payload. That key is `text`, `imageUrl`, or `imageBinary`, depending on which type of vector query was requested.
+ The vectorizer expects the resulting embedding to be under the `vector` key in the `data` JSON object in the response payload.
+ Any errors or warnings returned by the endpoint are ignored by the vectorizer and aren't available for query-time debugging.
+ If an `imageBinary` vector query was requested, the request payload sent to the endpoint is the following:

    ```json
    {
        "values": [
            {
                "recordId": "0",
                "data":
                {
                    "imageBinary": {
                        "data": "<base 64 encoded image binary data>"
                    }
                }
            }
        ]
    }
    ```

## See also

+ [Integrated vectorization](vector-search-integrated-vectorization.md)
+ [How to configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md)
+ [Custom Web API skill](cognitive-search-custom-skill-web-api.md)
+ [Hugging Face Embeddings Generator power skill (can be used for a custom web API vectorizer as well)](https://github.com/Azure-Samples/azure-search-power-skills/tree/main/Vector/EmbeddingGenerator)
