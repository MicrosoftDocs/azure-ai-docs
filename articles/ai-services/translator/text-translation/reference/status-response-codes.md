---
title: Azure Translator in Foundry Tools response codes and messages
titleSuffix: Foundry Tools
description: Understand response status and error code messages for the Azure Translator operations.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools response codes and messages

When you use `HTTP` protocol to access content on a server running `IIS`, the server returns a numeric code indicating the outcome of the request and the nature of the response, including its success or failure.
The status code's first digit categorizes the response class, while the last two digits serve no classification purpose. The first digit can be one of five values:

* **1xx** (Informational): An interim response indicating that the request was received and processing continues.
* **2xx** (Successful): The server successfully received and accepted the client request.
* **3xx** (Redirection): More action is required to complete the request.
* **4xx** (Client Error): An error occurred originating with the client browser and can't be fulfilled.
* **5xx** (Server Error): The server encountered an error and the request failed.

## Status codes

The following are the possible HTTP status codes that a request returns.

|Status code | Description |
| --- | --- |
|200 | Success. |
|400 |One of the query parameters is missing or not valid. Correct request parameters before retrying. |
|401 | The request couldn't be authenticated. Check that credentials are specified and valid. |
|403 | The request isn't authorized. Check the details error message. This status code often indicates that you used all the free translations provided with a trial subscription. |
|408 | The request couldn't be fulfilled because a resource is missing. Check the details error message. When the request includes a custom category, this status code often indicates that the custom translation system isn't yet available to serve requests. The request should be retried after a waiting period (for example, 1 minute). |
|429 | The server rejected the request because the client exceeded request limits. |
|500 |  An unexpected error occurred. If the error persists, report it with: date and time of the failure, request identifier from response header X-RequestId, and client identifier from request header X-ClientTraceId. |
|503 |Server temporarily unavailable. Retry the request. If the error persists, report it with: date and time of the failure, request identifier from response header X-RequestId, and client identifier from request header X-ClientTraceId. |

If an error occurs, the request returns a JSON error response. The error code is a 6-digit number combining the 3-digit HTTP status code followed by a 3-digit number to further categorize the error:

## Error codes

A standard error response is a JSON object with name/value pair named `error`. The value is also a JSON object with properties:

* `code`: A server-defined error code.
* `message`: A string giving a human-readable representation of the error.

For example, a customer with a free trial subscription would receive the following error once the free quota is exhausted:

```json
{
  "error": {
    "code":403001,
    "message":"The operation isn't allowed because the subscription has exceeded its free quota."
    }
}
```

The error code is a 6-digit number combining the 3-digit HTTP status code followed by a 3-digit number to further categorize the error. Common error codes are:

| Code | Description |
|:----|:-----|
| 400000| One of the request inputs isn't valid.|
| 400001| The "scope" parameter is invalid.|
| 400002| The "category" parameter is invalid.|
| 400003| A language specifier is missing or invalid.|
| 400004| A target script specifier ("To script") is missing or invalid.|
| 400005| An input text is missing or invalid.|
| 400006| The combination of language and script isn't valid.|
| 400018| A source script specifier ("From script") is missing or invalid.|
| 400019| One of the specified languages isn't supported.|
| 400020| One of the elements in the array of input text isn't valid.|
| 400021| The API version parameter is missing or invalid.|
| 400023| One of the specified language pair isn't valid.|
| 400035| The source language ("From" field) isn't valid.|
| 400036| The target language ("To" field) is missing or invalid.|
| 400042| One of the options specified ("Options" field) isn't valid.|
| 400043| The client trace ID (ClientTraceId field or X-ClientTraceId header) is missing or invalid.|
| 400050| The input text is too long. View [request limits](../../service-limits.md).|
| 400064| The "translation" parameter is missing or invalid.|
| 400070| The number of target scripts (ToScript parameter) doesn't match the number of target languages (To parameter).|
| 400071| The value isn't valid for TextType.|
| 400072| The array of input text has too many elements.|
| 400073| The script parameter isn't valid.|
| 400074| The body of the request isn't valid JSON.|
| 400075| The language pair and category combination isn't valid.|
| 400077| The maximum request size is exceeded. View [request limits](../../service-limits.md).|
| 400079| The custom system requested for translation between from and to language doesn't exist.|
| 400080| Transliteration isn't supported for the language or script.|
| 401000| The request isn't authorized because credentials are missing or invalid.|
| 401015| "The credentials provided are for the Speech API. This request requires credentials for the Text API. Use a subscription to Translator."|
| 403000| The operation isn't allowed.|
| 403001| The operation isn't allowed because the subscription exceeded its free quota.|
| 405000| The request method isn't supported for the requested resource.|
| 408001| The translation system requested is being prepared. Retry in a few minutes.|
| 408002| Request timed out waiting on incoming stream. The client didn't produce a request within the time that the server was prepared to wait. The client may repeat the request without modifications at any later time.|
| 415000| The Content-Type header is missing or invalid.|
| 429000, 429001, 429002| The server rejected the request because the client exceeded request limits.|
| 500000| An unexpected error occurred. If the error persists, report it with date/time of error, request identifier from response header X-RequestId, and client identifier from request header X-ClientTraceId.|
| 503000| Service is temporarily unavailable. Retry. If the error persists, report it with date/time of error, request identifier from response header X-RequestId, and client identifier from request header X-ClientTraceId.|
