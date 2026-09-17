---
title: Custom Web API Vectorizer
description: Use the Custom Web API vectorizer to integrate your custom code for generating embeddings at query time.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2024
ms.topic: concept-article
ms.date: 08/05/2026
ms.update-cycle: 365-days
ai-usage: ai-assisted
---

# Custom Web API vectorizer

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

The **Custom Web API** vectorizer lets you configure search queries to call a web API endpoint that generates embeddings at query time. The required JSON payload structure for the endpoint is described later in this article. Your data is processed in the [geography](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your model is deployed.

Although vectorizers are used at query time, you specify them in index definitions and reference them on vector fields through a vector profile. For more information, see [Configure a vectorizer in a search index](vector-search-how-to-configure-vectorizer.md).

The custom web API vectorizer is called `WebApiVectorizer` in the REST API. Use the latest stable version of [Indexes - Create (REST API)](/rest/api/searchservice/indexes/create) or an Azure SDK package that provides the feature.

## Vectorizer parameters

Parameters are case sensitive.

| Parameter name	 | Description |
|--------------------|-------------|
| `uri` | The URI of the Web API to which the JSON payload is sent. Only the **https** URI scheme is allowed. When you retrieve the index with GET, the service returns the `?code=` query parameter value as `?code=<redacted>` to prevent exposure of function keys. To update the vectorizer without changing the stored URI, set `uri` to `<unchanged>`. |
| `httpMethod` | The method used to send the payload. Allowed methods are `PUT` or `POST`. |
| `httpHeaders` | A collection of key-value pairs in which keys are header names and values are sent to your web API. The following headers are prohibited: `Accept`, `Accept-Charset`, `Accept-Encoding`, `Content-Length`, `Content-Type`, `Cookie`, `Host`, `TE`, `Upgrade`, and `Via`. GET returns the sentinel value `<redacted>` for every header value. For update requirements, see [Update header values after GET](#update-header-values-after-get). |
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
                "api-key": "<your-header-value>"
            },
            "timeout": "PT60S",
            "authResourceId": null,
            "authIdentity": null
        }
    }
]
```

### Update header values after GET

When you retrieve an index definition, the service returns the sentinel `<redacted>` for every `httpHeaders` value in a Custom Web API vectorizer. For example:

```json
{
    "name": "my-custom-web-api-vectorizer",
    "kind": "customWebApi",
    "customWebApiParameters": {
        "uri": "https://contoso.embeddings.com",
        "httpMethod": "POST",
        "httpHeaders": {
            "api-key": "<redacted>"
        },
        "timeout": "PT60S",
        "authResourceId": null,
        "authIdentity": null
    }
}
```

To reuse the stored `api-key` value, update the same existing vectorizer with the same `name` and `kind`, leave its `uri` unchanged, and resubmit the sentinel for the matching header name:

```json
{
    "name": "my-custom-web-api-vectorizer",
    "kind": "customWebApi",
    "customWebApiParameters": {
        "uri": "https://contoso.embeddings.com",
        "httpMethod": "POST",
        "httpHeaders": {
            "api-key": "<redacted>"
        },
        "timeout": "PT60S",
        "authResourceId": null,
        "authIdentity": null
    }
}
```

With an unchanged `uri`, you can mix `<redacted>` for retained header values with actual replacement values for other existing headers. Provide an actual value for each added or renamed header because the sentinel applies only to an existing header with the same name on the same vectorizer.

If you change the `uri`, provide actual values for every `httpHeaders` entry in the same update. The service doesn't reuse stored values for a different `uri`:

```json
{
    "name": "my-custom-web-api-vectorizer",
    "kind": "customWebApi",
    "customWebApiParameters": {
        "uri": "https://new.contoso.embeddings.com",
        "httpMethod": "POST",
        "httpHeaders": {
            "api-key": "<new-header-value>"
        },
        "timeout": "PT60S",
        "authResourceId": null,
        "authIdentity": null
    }
}
```

If the credentials are unavailable and you must change the `uri`, rotate or regenerate them at the external endpoint. Then submit the new `uri` and header values together.

The `<redacted>` value is a service sentinel, not a credential. It can't create a vectorizer or retrieve or reuse a header value stored for another vectorizer.

## JSON payload structure

The required JSON payload structure for an endpoint used with the Custom Web API vectorizer is the same as the structure used by the Custom Web API skill. For more information, see [the skill documentation](cognitive-search-custom-skill-web-api.md#sample-input-json-structure).

Keep the following considerations in mind when implementing a web API endpoint for the Custom Web API vectorizer:

+ The vectorizer sends only one record at a time in the `values` array when making a request to the endpoint.
+ The vectorizer passes the data to be vectorized in a specific key in the `data` JSON object in the request payload. That key is `text`, `imageUrl`, or `imageBinary`, depending on which type of vector query was requested.
+ The vectorizer expects the resulting embedding to be under the `vector` key in the `data` JSON object in the response payload.
+ The vectorizer ignores any errors or warnings returned by the endpoint. These errors and warnings aren't available for query-time debugging.
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
