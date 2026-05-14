---
title: "Start batch translation"
titleSuffix: Foundry Tools
description: Submit an asynchronous batch document translation job to the Document Translation service using the REST API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 05/14/2026
ai-usage: ai-assisted
---

# Start batch translation

Submit one or more documents stored in Azure Blob Storage for asynchronous translation. The service returns an `operation-location` header containing the job ID, which you use to poll for status. Each target container in a batch must be unique; submitting documents to a target container that already has translated output causes a file conflict error. Use the `targetUrl` for a specific container, not a shared destination.

**HTTP method:** POST
**API version:** 2026-03-01

## Request

```http
POST {endpoint}/translator/document/batches?api-version=2026-03-01
```

### Request headers

| Header | Required | Description |
|---|---|---|
| `Ocp-Apim-Subscription-Key` | Yes | Your Translator resource key from the Azure portal. |
| `Ocp-Apim-Subscription-Region` | Conditional | Required if you use a regional resource. |
| `Content-Type` | Yes | `application/json` |

### Request body

| Field | Required | Description |
|---|---|---|
| `inputs` | Yes | Array of batch input objects. Each object defines a source and one or more translation targets. |
| `inputs[].source` | Yes | Source document location. |
| `inputs[].source.sourceUrl` | Yes | SAS URL for the source Blob Storage container or file. |
| `inputs[].source.language` | No | Source language code (for example, `en`). If omitted, the service auto-detects the language. |
| `inputs[].source.filter` | No | File filter object with `prefix` and `suffix` fields to limit which source files are included. |
| `inputs[].targets` | Yes | Array of translation targets. |
| `inputs[].targets[].targetUrl` | Yes | SAS URL for the target Blob Storage container. Must be unique across all inputs in the request. |
| `inputs[].targets[].language` | Yes | Target language code (for example, `fr`). |
| `inputs[].targets[].deploymentName` | No | LLM deployment name for LLM-based translation (for example, `gpt-5.1`, `gpt-5.2`, `gpt-5.2-chat`). Omit to use NMT. |
| `inputs[].targets[].glossaries` | No | Array of glossary objects. Each glossary requires `glossaryUrl` (SAS URL) and `format` (for example, `TSV`). |
| `inputs[].storageType` | No | Storage source type. Supported values: `Folder` (default), `File`. |
| `translateWithinImage` | No | Boolean. Set to `true` to translate text within images in `.docx` and `.pptx` files. |

## Example requests

### NMT-based translation

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "https://{storage}.blob.core.windows.net/source?{sas}"
        },
        "targets": [
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-fr?{sas}",
            "language": "fr"
          }
        ]
      }
    ]
  }'
```

### LLM-based translation

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "https://{storage}.blob.core.windows.net/source?{sas}"
        },
        "targets": [
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-de?{sas}",
            "language": "de",
            "deploymentName": "gpt-5.1"
          }
        ]
      }
    ]
  }'
```

### Multiple target languages

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "https://{storage}.blob.core.windows.net/source?{sas}"
        },
        "targets": [
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-es?{sas}",
            "language": "es"
          },
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-ja?{sas}",
            "language": "ja"
          }
        ]
      }
    ]
  }'
```

### Translation with glossary

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "https://{storage}.blob.core.windows.net/source?{sas}"
        },
        "targets": [
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-pt?{sas}",
            "language": "pt",
            "glossaries": [
              {
                "glossaryUrl": "https://{storage}.blob.core.windows.net/glossaries/terms.tsv?{sas}",
                "format": "TSV"
              }
            ]
          }
        ]
      }
    ]
  }'
```

### Translate images in Word and PowerPoint documents

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "https://{storage}.blob.core.windows.net/source?{sas}"
        },
        "targets": [
          {
            "targetUrl": "https://{storage}.blob.core.windows.net/target-ko?{sas}",
            "language": "ko"
          }
        ],
        "translateWithinImage": true
      }
    ]
  }'
```

## Response

### Response status codes

| Status code | Description |
|---|---|
| `202` | Accepted. The batch job was queued successfully. |
| `400` | Bad request. Check the request body for missing or invalid fields. |
| `401` | Authentication failed. Check your subscription key. |
| `429` | Too many requests. Reduce request frequency. |
| `500` | Internal server error. |

### Response headers

| Header | Description |
|---|---|
| `operation-location` | URL containing the job ID for polling. Format: `{endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01`. |

## Related content

* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Get translation status](get-status-specific-translation.md)
* [Get status for all documents](get-status-all-documents.md)
