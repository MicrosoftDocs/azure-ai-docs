---
title: "Get status for all documents"
titleSuffix: Foundry Tools
description: Retrieve the translation status for all documents in a batch translation job using the Document Translation REST API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 05/14/2026
ai-usage: ai-assisted
---

# Get status for all documents

Retrieve the translation status for every document in a batch translation job. The response includes per-document status, progress, output location, and character usage. This operation supports paging, sorting, and filtering, which is useful for large jobs.

**HTTP method:** GET
**API version:** 2026-03-01

## Request

```http
GET {endpoint}/translator/document/batches/{jobId}/documents?api-version=2026-03-01
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

### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `api-version` | Yes | Version of the API. Current value: `2026-03-01`. |
| `$top` | No | Maximum number of records to return (for paging). |
| `$skip` | No | Number of records to skip (for paging). |
| `$orderBy` | No | Sort field. Supported values: `createdDateTimeUtc`, `lastActionDateTimeUtc`. |

## Example request

```bash
curl -X GET "{endpoint}/translator/document/batches/{jobId}/documents?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns a list of documents and their translation status. |
| `401` | Authentication failed. Check your subscription key. |
| `404` | Job not found. Verify the `jobId`. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `value` | array | Array of document status objects. |
| `value[].id` | string | Document ID. Use this value to call [Get status for a specific document](get-status-specific-document.md). |
| `value[].sourcePath` | string | Source file path in the Blob Storage container. |
| `value[].status` | string | Document translation status. |
| `value[].to` | string | Target language code. |
| `value[].progress` | number | Translation progress as a value between 0 and 1. |
| `value[].characterCharged` | integer | Number of characters billed for this document. |
| `nextLink` | string | URL for the next page of results, if paging applies. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get status for a specific document](get-status-specific-document.md)
* [Get translation status](get-status-specific-translation.md)
