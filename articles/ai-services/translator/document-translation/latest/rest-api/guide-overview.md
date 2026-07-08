---
title: Document Translation REST API Guide
titleSuffix: Foundry Tools
description: Overview of the Document Translation REST API operations for synchronous and asynchronous batch document translation.
author: laujan
ms.author: lajanuar
manager: mcleans
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Document Translation REST API guide overview

The Document Translation REST API (version 2026-03-01) supports two translation models and a set of discovery operations. Synchronous translation processes a single document without Blob Storage and returns the translated file directly. Asynchronous batch translation processes one or more documents stored in Azure Blob Storage and lets you poll for status. Both models use neural machine translation (NMT) by default.

All requests require a custom domain endpoint. The format is `https://{your-resource-name}.cognitiveservices.azure.com/`.

## Synchronous operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Translate a document | `POST` | Translate a single document and receive the translated output in the response. No Blob Storage required. | [Synchronous document translation](translate-synchronous.md) |

## Asynchronous batch operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Start batch translation | `POST` | Submit one or more documents for asynchronous translation. Documents must be in Azure Blob Storage. Returns a job ID. | [Start batch translation](translate-asynchronous.md) |
| Get translation status | `GET` | Retrieve the overall status and document summary for a specific batch job. Poll until the job reaches a terminal state. | [Get translation status](get-status-specific-translation.md) |
| Get status for all translations | `GET` | List all batch translation jobs submitted to your resource. Supports filtering and paging. | [Get status for all translation jobs](get-status-all-translations.md) |
| Get status for all documents | `GET` | Retrieve per-document status for all documents in a specific job. | [Get status for all documents](get-status-all-documents.md) |
| Get status for a specific document | `GET` | Retrieve status and output details for a single document within a job. | [Get status for a specific document](get-status-specific-document.md) |
| Cancel translation | `DELETE` | Cancel a job that is queued or in progress. | [Cancel translation](cancel-translation.md) |

## Discovery operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Get supported document formats | `GET` | Retrieve a list of supported document formats and their MIME types. | [Get supported document formats](get-supported-document-formats.md) |
| Get supported glossary formats | `GET` | Retrieve a list of supported glossary formats and their MIME types. | [Get supported glossary formats](get-supported-glossary-formats.md) |

## Related content

* [Document Translation overview](../../overview.md)
* [End-to-end batch translation workflow](../end-to-end-batch-workflow.md)
* [Prerequisites](../prerequisites.md)
