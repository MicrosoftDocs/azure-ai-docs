---
title: Azure AI Translator 2025-05-01-preview transliterate method
titleSuffix: Azure AI services
description: Convert text from one script to another script with the Azure AI Translator 2025-05-01-preview transliterate method.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 09/04/2025
ms.author: lajanuar
---

# Transliterate (2025-05-01-preview)

The Text transliteration API maps your source language script or alphabet to a target language script or alphabet. Unlike translation, transliteration doesn't return the meaning, only the way the text is written.

## Request URL

### Global endpoint configuration

**Send a `POST` request to**:

```bash
curl -X POST https://api.cognitive.microsofttranslator.com/transliterate?api-version=2025-05-01-preview
 -H "Ocp-Apim-Subscription-Key:<your-key>" ^
 -H "Ocp-Apim-Subscription-Region:<your-resource-region>" ^
 -H "Content-Type: application/json" ^
 -d "<your-request-body>"
```

***Linux or macOS***

```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/transliterate?api-version=2025-05-01-preview" \
-H "Ocp-Apim-Subscription-Key:<your-key>" \
-H "Ocp-Apim-Subscription-Region:<your-resource-region>" \
-H "Content-Type: application/json" \
-d "<your-request-body>"
```
### Custom endpoint configuration

 Your custom domain endpoint is a URL formatted with your resource name and hostname and is available in the Azure portal. When you created your Translator resource, the value that you entered in the `Name` field is the custom domain name parameter for the endpoint.

**Send a `POST` request**:

***Windows***

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com//transliterate?api-version=2025-05-01-preview"^
    -H "Ocp-Apim-Subscription-Key:<your-key>"^
    -H "Ocp-Apim-Subscription-Region:<your-resource-region>"^
    -H "Content-Type: application/json"^
    -d "<your-request-body>"
```
***Linux or macOS***

```bash
curl -X POST "https://<your-resource-name>.cognitiveservices.azure.com//transliterate?api-version=2025-05-01-preview" \
    -H "Ocp-Apim-Subscription-Key:<your-key>" \
    -H "Ocp-Apim-Subscription-Region:<your-resource-region>" \
    -H "Content-Type: application/json" \
    -d "<your-request-body>"
```

### Private endpoint

For more information on Translator service selected network and private endpoint configuration and support, *see* [**Virtual Network Support**](../reference/authentication.md).

## Request headers 

| Headers | Required| Description |
| --- | --- |---|
| **Authentication headers** |**True**| *See* [available options for authentication](../reference/authentication.md). |
| **Content-Type** |**True**| Specifies the content type of the payload. Accepted values are: `application/json`; `charset=UTF-8`|
| **Content-Length** |False| The length of the request body. |
| **X-ClientTraceId** |False| A client-generated GUID to uniquely identify the request. You can omit this optional header if you include the trace ID in the query string using a query parameter named `ClientTraceId`. |

## Request parameters

Request parameters passed on the query string areas are as follows:

| Parameter |Type| Required | Description |
| --- | --- |---|---|
|**api-version**|string|**True**|Version of the API requested by the client. Accepted value is 2025-05-01-preview.|
| **fromScript**| string|**True**| Specifies the script used by the input text. Look up [supported languages](get-languages.md) using the `transliteration` scope, to find input scripts available for the selected language. |
| **toScript** |string| **True**| Specifies the output script. Look up [supported languages](get-languages.md) using the `transliteration` scope, to find output scripts available for the selected combination of input language and input script. |
|**language** | string | False | Specifies the language code for the `source` text. If not specified, the system autodetects the language of the source text. Accepted values are list of language code supported by the specified model. |

## Request body

The body of the request is a JSON array. Each array element is a JSON object with a string property named `Text`, which represents the string to convert.

```json
[
    {"Text":"こんにちは"},
    {"Text":"さようなら"}
]
```

The following limitations apply:

* The array can have at most 10 elements.
* The text value of an array element can't exceed 1,000 characters including spaces.
* The entire text included in the request can't exceed 5,000 characters including spaces.

## Response body

A successful response is a JSON array with one result for each element in the input array. A result object includes the following properties:

* `text`: A string that results from converting the input string to the output script.

* `script`: A string specifying the script used in the output.

An example JSON response is:

```json
[
    {"text":"konnnichiha","script":"Latn"},
    {"text":"sayounara","script":"Latn"}
]
```

## Response headers

| Headers | Description |
| --- | --- |
| **X-RequestId** | Value generated by the service to identify the request and used for troubleshooting purposes. |

## Example

The following example shows how to convert two Japanese strings into Romanized Japanese.

```bash
  curl -X POST "https://api.cognitive.microsofttranslator.com/transliterate?api-version=2025-05-01-preview&language=ja&fromScript=Jpan&toScript=Latn" -H "X-ClientTraceId: 875030C7-5380-40B8-8A03-63DACCF69C11" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json" -d @request.txt
```

The JSON payload for the request in this example:

```json
[{"text":"こんにちは","script":"jpan"},{"text":"さようなら","script":"jpan"}]
```

## Response status codes

The following are the possible HTTP status codes that a request returns.

| Status Code | Description |
| --- | --- |
| 200 | Success. |
| 400 | One of the query parameters is missing or not valid. Correct request parameters before retrying. |
| 401 | The request couldn't be authenticated. Check that credentials are specified and valid. |
| 403 | The request isn't authorized. Check the details error message. This code often indicates that all free translations provided with a trial subscription are used. |
| 429 | The server rejected the request because the client exceeded request limits. |
| 500 | An unexpected error occurred. If the error persists, report it with: date and time of the failure, request identifier from response header `X-RequestId`, and client identifier from request header `X-ClientTraceId`. |
| 503 | Server temporarily unavailable. Retry the request. If the error persists, report it with: date and time of the failure, request identifier from response header `X-RequestId`, and client identifier from request header `X-ClientTraceId`. |

If an error occurs, the request also returns a JSON error response. The error code is a 6-digit number combining the 3-digit HTTP status code followed by a 3-digit number to further categorize the error. Common error codes can be found on the [Status code reference page](../reference/status-response-codes.md).


## Next steps

> [!div class="nextstepaction"]
> [View 2025-05-01-preview migration guide](../how-to/migrate-to-preview.md)

