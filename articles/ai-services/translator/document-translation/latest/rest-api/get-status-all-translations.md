---
title: Get Status for All Translation Jobs
titleSuffix: Foundry Tools
description: Retrieve a list of all batch translation jobs submitted to your Document Translation resource and their current status.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Get status for all document translation jobs

Retrieve a list of all batch translation jobs submitted to your resource, along with status and summary information for each job. The response supports paging and filtering, which is useful for auditing job history or recovering a job ID.

HTTP method: **GET**
API version: **2026-03-01**

## Request

```http
GET {endpoint}/translator/document/batches?api-version=2026-03-01
```

### Request headers

| Header | Required | Description |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | Yes | Your Translator resource key from the Azure portal. |
| `Ocp-Apim-Subscription-Region` | Conditional | Required if you use a regional resource. |

### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `api-version` | Yes | Version of the API. Current value: `2026-03-01`. |
| `$top` | No | Maximum number of records to return. |
| `$skip` | No | Number of records to skip (for paging). |
| `$orderBy` | No | Sort field. Supported values: `createdDateTimeUtc`, `lastActionDateTimeUtc`. |
| `statuses` | No | Filter by status. Supported values: `NotStarted`, `Running`, `Succeeded`, `Failed`, `Cancelled`, `Cancelling`, `ValidationFailed`. |
| `createdDateTimeUtcStart` | No | Filter to jobs created after this datetime (UTC, ISO 8601). |
| `createdDateTimeUtcEnd` | No | Filter to jobs created before this datetime (UTC, ISO 8601). |

## Example requests

### Get the most recent jobs

```bash
curl -X GET "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

### Filter by status

```bash
curl -X GET "{endpoint}/translator/document/batches?api-version=2026-03-01&statuses=Succeeded&statuses=Cancelled" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns a list of translation jobs and their status. |
| `401` | Authentication failed. Check your subscription key. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `value` | array | Array of translation job status objects. |
| `value[].id` | string | Job ID. Use this value to call [Get translation status](get-status-specific-translation.md). |
| `value[].status` | string | Overall job status. |
| `value[].createdDateTimeUtc` | string | Job creation datetime (UTC). |
| `value[].lastActionDateTimeUtc` | string | Last status change datetime (UTC). |
| `value[].summary` | object | Summary of document counts by status. |
| `nextLink` | string | URL for the next page of results, if paging applies. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get translation status](get-status-specific-translation.md)
* [Get status for all documents](get-status-all-documents.md)
