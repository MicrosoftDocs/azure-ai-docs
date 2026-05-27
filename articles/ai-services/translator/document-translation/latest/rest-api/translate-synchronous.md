---
title: Synchronous Document Translation
titleSuffix: Foundry Tools
description: Translate a single document synchronously using the Document Translation REST API. No Azure Blob Storage required.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Translate a single document

Translate a single document and receive the translated output in the HTTP response. This operation doesn't require Azure Blob Storage, which makes it well-suited for interactive translation, lightweight integrations, and testing. The request uses multipart/form-data to pass the document and returns the translated file as binary data in the response body.

HTTP method: **POST**
API version: **2026-03-01**

## Request

```http
POST {endpoint}/translator/document:translate?targetLanguage={targetLanguage}&api-version=2026-03-01
```

### Request headers

| Header | Required | Description |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | Yes | Your Translator resource key from the Azure portal. |
| `Ocp-Apim-Subscription-Region` | Conditional | Required if you use a regional resource. |
| `Content-Type` | Yes | `multipart/form-data` |

### Query parameters

| Parameter | Required | Description |
|---|---|---|
| `targetLanguage` | Yes | Target language code (for example, `fr`, `de`, `ja`). |
| `sourceLanguage` | No | Source language code. If omitted, the service auto-detects the source language. |
| `deploymentName` | No | LLM deployment name (for example, `gpt-5.1`, `gpt-5.2`, `gpt-5.2-chat`). Omit to use NMT. |
| `category` | No | Custom Translator category ID. |
| `allowFallback` | No | Boolean. Set to `true` to allow fallback to general translation if a custom system isn't available. Default: `true`. |
| `api-version` | Yes | Version of the API. Current value: `2026-03-01`. |

### Request body

The request uses `multipart/form-data`. Include the following parts:

| Part | Required | Description |
|---|---|---|
| `document` | Yes | The file to translate. Specify the file content and MIME type. |
| `glossary` | No | A glossary file to apply custom terminology. Specify the file content and MIME type. |

## Example requests

### NMT-based translation

```bash
curl -X POST "{endpoint}/translator/document:translate?targetLanguage=fr&api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -F "document=@{path/to/document.docx};type=application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -o translated.docx
```

### LLM-based translation

```bash
curl -X POST "{endpoint}/translator/document:translate?targetLanguage=de&deploymentName=gpt-5.1&api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -F "document=@{path/to/document.pdf};type=application/pdf" \
  -o translated.pdf
```

### Translation with glossary

```bash
curl -X POST "{endpoint}/translator/document:translate?targetLanguage=es&api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -F "document=@{path/to/document.docx};type=application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -F "glossary=@{path/to/glossary.tsv};type=text/tab-separated-values" \
  -o translated.docx
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `200` | OK. Returns the translated document as binary data. |
| `400` | Bad request. Check query parameters and form data. |
| `401` | Authentication failed. Check your subscription key. |
| `415` | Unsupported media type. Verify the MIME type of the document. |
| `429` | Too many requests. Reduce request frequency. |
| `500` | Internal server error. |

The `200` response body is the translated document file. Save it using the `-o` flag in curl or the equivalent in your HTTP client.

## Related content

* [Get supported document formats](get-supported-document-formats.md)
* [Get supported glossary formats](get-supported-glossary-formats.md)
* [Quickstart: synchronous document translation](../quickstarts/synchronous.md)
