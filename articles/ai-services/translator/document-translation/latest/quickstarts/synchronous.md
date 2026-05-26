---
title: "Quickstart: Synchronous Document Translation"
titleSuffix: Foundry Tools
description: Learn how to use the synchronous translation process of the Document Translation API to translate a single document without Azure Blob Storage. The translated document is returned directly in the response.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 06/02/2026
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->
# Quickstart: Synchronous document translation

Synchronous translation lets you translate a single document and receive the output directly in the API response — no Azure Blob Storage required. Use this approach for interactive scenarios, lightweight integrations, or single-file requests.

## Prerequisites

You need one of the following resources to get started:

* An **Azure AI Translator resource**, or a Microsoft **Foundry resource** if you choose to translate using LLMs.

For more information, see [Prerequisites and setup](../prerequisites.md).

## Step 1: Prepare your document

The synchronous API accepts one document per request as a multipart form upload. Confirm your document is in one of the [supported document formats](../../overview.md#supported-document-and-glossary-formats) and note its MIME type — you specify it in the request so the service can parse the file correctly.

## Step 2: Submit a synchronous translation request

Send a POST request to the `/document:translate` endpoint with your document attached as a multipart form field. Specify the target language using the `targetLanguage` query parameter. The `-o` option writes the translated document to a local file. Replace `{endpoint}` and `{key}` with the values from your Translator resource.

```bash
curl -i -X POST "{endpoint}/translator/document:translate?targetLanguage=fr&api-version=2026-03-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -F "document=@sample.docx;type=application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -o translated.docx
```

## Step 3: Review the response

A successful request returns a `200 OK` response. The translated document is returned directly in the response body and written to the output file you specified with `-o`.

**Optional: include a glossary**

To apply custom terminology, add a glossary file as a second form field in the same request:

```bash
-F "glossary=@glossary.tsv;type=text/tab-separated-values"
```

For more information, see [Create and use a glossary](../../how-to-guides/create-use-glossaries.md).
