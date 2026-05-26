---
title: Get Translation Status
titleSuffix: Foundry Tools
description: Retrieve the overall status and document summary for a specific batch translation job using the Document Translation REST API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Get translation status

Retrieve the overall status and document summary for a specific batch translation job. Poll this endpoint after submitting a batch request until the job reaches a terminal state: `Succeeded`, `Failed`, `Cancelled`, or `ValidationFailed`.

**HTTP method:** GET
**API version:** 2026-03-01

## Request

```http
GET {endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
```

### Request headers

| Header | Required | Description |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | Yes | Your Translator resource key from the Azure portal. |
| `Ocp-Apim-Subscription-Region` | Conditional | Required if you use a regional resource. |

### Path parameters

| Parameter | Required | Description |
|---|---|---|
| `jobId` | Yes | The job ID returned in the `operation-location` header when you submitted the batch request. |

## Example request

```bash
curl -X GET "{endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns overall job status and a document summary. |
| `401` | Authentication failed. Check your subscription key. |
| `404` | Job not found. Verify the `jobId`. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `id` | string | Job ID. |
| `status` | string | Overall job status: `NotStarted`, `Running`, `Succeeded`, `Failed`, `Cancelled`, `Cancelling`, or `ValidationFailed`. |
| `createdDateTimeUtc` | string | Job creation datetime (UTC). |
| `lastActionDateTimeUtc` | string | Last status change datetime (UTC). |
| `summary` | object | Counts of documents by status: succeeded, failed, inProgress, notStarted, canceled, total. |
| `error` | object | Error details if the job failed. Includes `code` and `message` fields. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get status for all documents](get-status-all-documents.md)
* [Start batch translation](translate-asynchronous.md)
