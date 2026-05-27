---
title: Get Status for a Specific Document
titleSuffix: Foundry Tools
description: Retrieve the translation status and details for a single document within a batch translation job using the Document Translation REST API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Get status for a single document

Retrieve status details for a single document within a batch translation job. The response includes translation status, progress, output URL, and character usage. This is the most targeted way to retrieve error details or the output URL for one document without paging through the full document list.

**HTTP method:** GET
**API version:** 2026-03-01

## Request

```http
GET {endpoint}/translator/document/batches/{jobId}/documents/{documentId}?api-version=2026-03-01
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
| `documentId` | Yes | The document ID returned by [Get status for all documents](get-status-all-documents.md). |

## Example request

```bash
curl -X GET "{endpoint}/translator/document/batches/{jobId}/documents/{documentId}?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns status and metadata for the specified document. |
| `401` | Authentication failed. Check your subscription key. |
| `404` | Document or job not found. Verify both `jobId` and `documentId`. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `id` | string | Document ID. |
| `sourcePath` | string | Source file path in the Blob Storage container. |
| `status` | string | Document translation status: `NotStarted`, `Running`, `Succeeded`, `Failed`, `Cancelled`, `Cancelling`, or `ValidationFailed`. |
| `to` | string | Target language code. |
| `progress` | number | Translation progress as a value between 0 and 1. |
| `characterCharged` | integer | Number of characters billed for this document. |
| `error` | object | Error details if the document failed. Includes `code` and `message` fields. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get status for all documents](get-status-all-documents.md)
* [Get translation status](get-status-specific-translation.md)
