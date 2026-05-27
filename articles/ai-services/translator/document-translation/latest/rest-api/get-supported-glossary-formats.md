---
title: Get Supported Glossary Formats
titleSuffix: Foundry Tools
description: Retrieve the list of glossary formats supported by the Document Translation service.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Get supported glossary formats list

Retrieve a list of glossary formats supported by the Document Translation service. Use this endpoint to discover which glossary file types and MIME types you can pass when applying custom terminology to a translation job.

HTTP method: **GET**
API version: **2026-03-01**

## Request

```http
GET {endpoint}/translator/document/formats?api-version=2026-03-01&type=glossary
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
| `type` | No | Filter results by format type. Use `glossary` to retrieve glossary formats. Omit to return all formats. |

## Example request

```bash
curl -X GET "{endpoint}/translator/document/formats?api-version=2026-03-01&type=glossary" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns a list of supported glossary formats. |
| `401` | Authentication failed. Check your subscription key. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `value` | array | Array of `FileFormat` objects. |
| `value[].format` | string | Glossary format name (for example, `TSV`). |
| `value[].fileExtensions` | array | List of supported file extensions (for example, `.tsv`). |
| `value[].contentTypes` | array | List of MIME types for this glossary format. |
| `value[].defaultVersion` | string | Default format version. |
| `value[].versions` | array | Available format versions. |

## Related content

* [Get supported document formats](get-supported-document-formats.md)
* [Start batch translation](translate-asynchronous.md)
* [Synchronous document translation](translate-synchronous.md)
