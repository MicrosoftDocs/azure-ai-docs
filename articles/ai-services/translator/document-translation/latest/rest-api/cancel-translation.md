---
title: "Cancel translation"
titleSuffix: Foundry Tools
description: Cancel an asynchronous batch translation job that is queued or in progress using the Document Translation REST API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 05/14/2026
ai-usage: ai-assisted
---

# Cancel translation

Cancel a batch translation job that is in a `NotStarted` or `Running` state. The service makes a best-effort attempt to stop processing. Documents that have already completed translation are retained in the target container and billed normally. Jobs in a terminal state (`Succeeded`, `Failed`, `Cancelled`) cannot be canceled.

**HTTP method:** DELETE
**API version:** 2026-03-01

## Request

```http
DELETE {endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
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
curl -X DELETE "{endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | Cancel request accepted. The job transitions to `Cancelling`. |
| `401` | Authentication failed. Check your subscription key. |
| `404` | Job not found. Verify the `jobId`. |
| `409` | Job is already in a terminal state and cannot be canceled. |
| `500` | Internal server error. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get translation status](get-status-specific-translation.md)
* [Start batch translation](translate-asynchronous.md)
