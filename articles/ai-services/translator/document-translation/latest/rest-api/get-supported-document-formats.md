---
title: Get Supported Document Formats
titleSuffix: Foundry Tools
description: Retrieve the list of document formats supported by the Document Translation service for translation.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Get supported document formats list

Retrieve a list of document formats supported by the Document Translation service. Use this endpoint to validate file types before submitting a translation job and to discover supported MIME types and format-specific versioning.

HTTP method: **GET**
API version: **2026-03-01**

## Request

```http
GET {endpoint}/translator/document/formats?api-version=2026-03-01&type=document
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
| `type` | No | Filter results by format type. Use `document` to retrieve document formats. Omit to return all formats. |

## Example request

```bash
curl -X GET "{endpoint}/translator/document/formats?api-version=2026-03-01&type=document" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns a list of supported document formats. |
| `401` | Authentication failed. Check your subscription key. |
| `500` | Internal server error. |

### Response body

| Field | Type | Description |
|---|---|---|
| `value` | array | Array of `FileFormat` objects. |
| `value[].format` | string | Format name (for example, `DOCX`). |
| `value[].fileExtensions` | array | List of supported file extensions (for example, `.docx`). |
| `value[].contentTypes` | array | List of MIME types for this format. |
| `value[].defaultVersion` | string | Default format version used when `storageInputFileFormat` is not specified. |
| `value[].versions` | array | Available format versions. |

## Related content

* [Get supported glossary formats](get-supported-glossary-formats.md)
* [Start batch translation](translate-asynchronous.md)
* [Synchronous document translation](translate-synchronous.md)
