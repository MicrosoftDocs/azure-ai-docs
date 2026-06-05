---
title: "Quickstart: Asynchronous Document Translation"
titleSuffix: Foundry Tools
description: Learn how to use the asynchronous batch translation process of the Document Translation API to translate multiple documents or large files in parallel using Azure Blob Storage for input and output.
author: laujan
ms.author: lajanuar
manager: mcleans
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 06/02/2026
ai-usage: ai-assisted
---

# Quickstart: Asynchronous document translation

Asynchronous batch translation lets you submit multiple documents or large files for translation in a single request. The service processes the documents in parallel and writes the translated output to your Azure Blob Storage target container. Because the operation runs asynchronously, you poll a job ID to track progress rather than waiting for an immediate response. Use this approach when you need to translate high volumes of content or files too large for a synchronous request.

## Prerequisites

* An **Azure AI Translator resource**, or a Microsoft **Foundry resource**.
* An **Azure Blob Storage account** with a source container (input files) and a target container (output files).
* **SAS tokens** or **Managed Identity** configured for both containers.

For more information, see [Prerequisites and setup](../prerequisites.md).

## Step 1: Upload your documents

Before you submit a translation request, upload your source documents to the Blob Storage container you designated as the input location. The service reads documents from this container when the job runs.

## Step 2: Authorize access to your Blob Storage account

The API needs authorization to read from your source container and write to your target container. Set up one of the following authorization methods before you build your request:

* To use managed identity, see [Create and use managed identities](../../how-to-guides/create-use-managed-identities.md).
* To use SAS tokens, see [Create shared access signature (SAS) tokens](../../how-to-guides/create-sas-tokens.md).

## Step 3: Submit a batch translation request

Send a POST request to the `/batches` endpoint with a JSON body that specifies your source and target container URLs, the target language, and any additional options. Choose the option that matches your translation engine and requirements.

### NMT-based translation

Use this option for standard neural machine translation.

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "{source-container-SAS-URL} or {source-container-name-for-managed-identity}"
        },
        "targets": [
          {
            "targetUrl": "{target-container-SAS-URL} or {target-container-name-for-managed-identity}",
            "language": "fr"
          }
        ]
      }
    ]
  }'
```

### Translate images in Word and PowerPoint documents

Use this option to translate text embedded in images within Word (`.docx`) and PowerPoint (`.pptx`) files. Set `translateWithinImage` to `true` in the `options` object.

```bash
curl -X POST "{endpoint}/translator/document/batches?api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "source": {
          "sourceUrl": "{source-container-SAS-URL} or {source-container-name-for-managed-identity}"
        },
        "targets": [
          {
            "targetUrl": "{target-container-SAS-URL} or {target-container-name-for-managed-identity}",
            "language": "fr"
          }
        ]
      }
    ],
    "options": { "translateWithinImage": true }
  }'
```

## Step 4: Check status

Because the translation runs asynchronously, the service immediately returns a `202 Accepted` response instead of the translated documents. To track progress, extract the job ID from the `operation-location` header in the response and poll that URL until the job completes.

```bash
operation-location: https://{your-endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
```

**Example response**

* Status code: `202`
* Status: `Accepted`

```http


response headers: {
  'Transfer-Encoding': 'chunked',
  'Content-Type': 'application/json; charset=utf-8',
  'x-requestid': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  'operation-location': 'https://{your-endpoint}/translator/document/batches/jjjjjjjj-jjjj-jjjj-jjjj-jjjjjjjjjjjj?api-version=2026-03-01',
  'x-envoy-upstream-service-time': '366',
  'apim-request-id': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
  'x-content-type-options': 'nosniff',
  'x-ms-region': 'Japan East',
  'Date': 'Mon, 04 May 2026 16:06:08 GMT'
           }
```
To monitor progress, use the `operation-location` URL to poll the job status. For more information, see [Get translation job status](../rest-api/get-status-specific-translation.md).

## Step 5: View results

When the job status shows as succeeded, your translated documents are available in the target container of your Azure Blob Storage account. Download them directly from the container or access them programmatically using the Azure SDK.
