---
title: Get translations status
titleSuffix: Azure AI services
description: The get translations status method returns a list of batch requests submitted and the status for each request.
manager: nitinme
ms.author: lajanuar
author: laujan
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 04/14/2025
---

# Get status for all translation jobs

Reference</br>
Feature: **Azure AI Translator → Document translation**</br>
API Version: **2024-05-01**</br>
HTTP method: **GET**

* Use the `get translations status` method to request a list and the status of all translation jobs submitted by the user (associated with the resource).

* `$top`, `$skip`, and `$maxpagesize` query parameters can be used to specify the number of results to return and an offset for the collection.
  * `$top` indicates the total number of records to be returned across all pages.
  * `$skip` indicates the number of records to skip from the list of batches based on the sorting method specified. By default, records are sorted by descending start time.
  * `$maxpagesize` is the maximum items returned in a page.
  * If more items are requested via `$top` (or `$top` isn't specified and there are more items to be returned), `@nextLink` will contain the link to the next page.
  * The server honors the values specified by the client. However, clients must be prepared to handle responses that contain a different page size or contain a continuation token.
  * When both `$top` and `$skip` are included, the server first applies `$skip` and then `$top` on the collection.

> [!NOTE]
> If the server can't honor `$top` and/or `$skip`, the server must return an error to the client informing about it instead of just ignoring the query options. This action reduces the risk of the client making assumptions about the data returned.

* `$orderBy` query parameter can be used to sort the returned list (ex: `$orderBy=createdDateTimeUtc asc` or `$orderBy=createdDateTimeUtc desc`).
  * The default sorting is descending by `createdDateTimeUtc`. Some query parameters can be used to filter the returned list (ex: `status=Succeeded,Cancelled`) returns succeeded and canceled operations.
  * The `createdDateTimeUtcStart` and `createdDateTimeUtcEnd` query parameters can be combined or used separately to specify a range of datetime to filter the returned list.
  * The supported filtering query parameters are (`status`, `id`, `createdDateTimeUtcStart`, and  `createdDateTimeUtcEnd`).

## Request URL

```bash
  curl -i -X GET "{document-translation-endpoint}/translator/document/batches?api-version={date}"
```

> [!IMPORTANT]
>
> **All API requests to the Document translation feature require a custom domain endpoint that is located on your resource overview page in the Azure portal**.

## Request parameters

Request parameters passed on the query string are:

|Query parameter|In|Required|Type|Description|
|--- |--- |--- |---|---|
|`$maxpagesize`|query|False|integer int32|`$maxpagesize` is the maximum items returned in a page. If more items are requested via `$top` (or `$top` isn't specified and there are more items to be returned), @nextLink will contain the link to the next page. Clients MAY request server-driven paging with a specific page size by specifying a `$maxpagesize` preference. The server SHOULD honor this preference if the specified page size is smaller than the server's default page size.|
|`$orderBy`|query|False|array|The sorting query for the collection (ex: `CreatedDateTimeUtc asc`, `CreatedDateTimeUtc desc`)|
|`$skip`|query|False|integer int32|`$skip` indicates the number of records to skip from the list of records held by the server based on the sorting method specified. By default, we sort by descending start time. Clients MAY use `$top` and `$skip` query parameters to specify the number of results to return and an offset into the collection. When the client returns both `$top` and `$skip`, the server SHOULD first apply `$skip` and then `$top` on the collection.Note: If the server can't honor `$top` and/or `$skip`, the server MUST return an error to the client informing about it instead of just ignoring the query options.|
|`$top`|query|False|integer int32|`$top` indicates the total number of records the user wants to be returned across all pages. Clients MAY use `$top` and `$skip` query parameters to specify the number of results to return and an offset into the collection. When the client returns both `$top` and `$skip`, the server SHOULD first apply `$skip` and then `$top` on the collection.Note: If the server can't honor `$top` and/or `$skip`, the server MUST return an error to the client informing about it instead of just ignoring the query options.|
|`createdDateTimeUtcEnd`|query|False|string date-time|The end datetime to get items before.|
|`createdDateTimeUtcStart`|query|False|string date-time|The start datetime to get items after.|
|`ids`|query|False|array|IDs to use in filtering.|
|`statuses`|query|False|array|Statuses to use in filtering.|

## Request headers

Request headers are:

|Headers|Description|Condition|
|--- |--- |---|
|**Ocp-Apim-Subscription-Key**|Your Translator service API key from the Azure portal.|***Required***|
|**Ocp-Apim-Subscription-Region**|The region where your resource was created. |***Required*** when using a regional (geographic) resource like **West US**.</br>&bullet.|
|**Content-Type**|The content type of the payload. The accepted value is **application/json** or **charset=UTF-8**.|***Required***|

## Response status codes

The following are the possible HTTP status codes that a request returns.

|Status Code|Description|
|--- |--- |
|200|OK. Successful request and returns the status of the all the operations. HeadersRetry-After: integerETag: string|
|400|Bad Request. Invalid request. Check input parameters.|
|401|Unauthorized. Check your credentials.|
|500|Internal Server Error.|
|Other Status Codes|&bullet; Too many requests<br>&bullet; Server temporary unavailable|

## Get translations status response

### Successful get translations status response

The following information is returned in a successful response.

|Name|Type|Description|
|--- |--- |--- |
|@nextLink|string|Url for the next page. Null if no more pages available.|
|value|TranslationStatus[]|TranslationStatus[] Array|
|value.id|string|ID of the operation.|
|value.createdDateTimeUtc|string|Operation created date time.|
|value.lastActionDateTimeUtc|string|Date time in which the operation's status was updated.|
|value.status|String|List of possible statuses for job or document:<br> &bullet; Canceled<br>&bullet; Cancelling<br>&bullet; Failed<br>&bullet; NotStarted<br>&bullet; Running<br>&bullet; Succeeded<br>&bullet; ValidationFailed|
|value.summary|StatusSummary[]|Summary containing the listed details.|
|value.summary.total|integer|Count of total documents.|
|value.summary.failed|integer|Count of documents failed.|
|value.summary.success|integer|Count of documents successfully translated.|
|value.summary.inProgress|integer|Count of documents in progress.|
|value.summary.notYetStarted|integer|Count of documents not yet started processing.|
|value.summary.cancelled|integer|Count of documents canceled.|
|value.summary.totalCharacterCharged|integer|Total count of characters charged.|

### Error response

|Name|Type|Description|
|--- |--- |--- |
|code|string|Enums containing high-level error codes. Accepted values:<br/>&bullet; InternalServerError<br>&bullet; InvalidArgument<br>&bullet; InvalidRequest<br>&bullet; RequestRateTooHigh<br>&bullet; ResourceNotFound<br>&bullet; ServiceUnavailable<br>&bullet; Unauthorized|
|message|string|Gets high-level error message.|
|target|string|Gets the source of the error. For example, it would be `documents` or `document id` if there was an invalid document.|
|innerError|InnerTranslationError|New Inner Error format that conforms to Azure AI services API Guidelines. This error message contains required properties ErrorCode, message, and optional properties target, details (key value pair), inner error (it can be nested).|
|innerError.code|string|Gets code error string.|
|innerError.message|string|Gets high-level error message.|
|innerError.target|string|Gets the source of the error. For example, it would be `documents` or `document id` if there was an invalid document.|

## Examples

> [!TIP]
> You can use this method to retrieve the job `id` parameter for the [get-translation-status](get-translation-status.md) query string.

### Example successful response

The following JSON object is an example of a successful response.

```JSON
{
    "value": [
        {
            "id": "36724748-f7a0-4db7-b7fd-f041ddc75033",
            "createdDateTimeUtc": "2021-06-18T03:35:30.153374Z",
            "lastActionDateTimeUtc": "2021-06-18T03:36:44.6155316Z",
            "status": "Succeeded",
            "summary": {
                "total": 3,
                "failed": 2,
                "success": 1,
                "inProgress": 0,
                "notYetStarted": 0,
                "cancelled": 0,
                "totalCharacterCharged": 0
            }
        },
        {
            "id": "1c7399a7-6913-4f20-bb43-e2fe2ba1a67d",
            "createdDateTimeUtc": "2021-05-24T17:57:43.8356624Z",
            "lastActionDateTimeUtc": "2021-05-24T17:57:47.128391Z",
            "status": "Failed",
            "summary": {
                "total": 1,
                "failed": 1,
                "success": 0,
                "inProgress": 0,
                "notYetStarted": 0,
                "cancelled": 0,
                "totalCharacterCharged": 0
            }
        },
        {
            "id": "daa2a646-4237-4f5f-9a48-d515c2d9af3c",
            "createdDateTimeUtc": "2021-04-14T19:49:26.988272Z",
            "lastActionDateTimeUtc": "2021-04-14T19:49:43.9818634Z",
            "status": "Succeeded",
            "summary": {
                "total": 2,
                "failed": 0,
                "success": 2,
                "inProgress": 0,
                "notYetStarted": 0,
                "cancelled": 0,
                "totalCharacterCharged": 21899
            }
        }
    ],
    ""@nextLink": "https://westus.cognitiveservices.azure.com/translator/text/batch/v1.1/operations/727BF148-F327-47A0-9481-ABAE6362F11E/documents?`$top`=5&`$skip`=15"
}

```

### Example error response

The following JSON object is an example of an error response. The schema for other error codes is the same.

Status code: 500

```JSON
{
  "error": {
    "code": "InternalServerError",
    "message": "Internal Server Error",
    "target": "Operation",
    "innerError": {
      "code": "InternalServerError",
      "message": "Unexpected internal server error has occurred"
    }
  }
}
```

## Next steps

Follow our quickstart to learn more about using Document translation and the client library.

> [!div class="nextstepaction"]
> [Get started with Document translation](../how-to-guides/use-rest-api-programmatically.md)
