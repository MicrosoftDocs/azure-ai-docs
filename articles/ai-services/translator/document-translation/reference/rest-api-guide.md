---
title: Document Translation REST API Guide (2024-05-01)
titleSuffix: Foundry Tools
description: Overview of the legacy Document Translation REST API operations for synchronous and asynchronous batch document translation.
author: laujan
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.topic: reference
ms.date: 07/30/2026
ms.author: lajanuar
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD060 -->

# Document Translation REST API guide (2024-05-01)

The legacy Document Translation REST API (version `2024-05-01`) supports synchronous single-document translation, asynchronous batch translation, and discovery operations. Synchronous translation processes a single document without Blob Storage and returns the translated file directly. Asynchronous batch translation processes one or more documents stored in Azure Blob Storage and lets you poll for status.

All requests require a custom domain endpoint. The format is `https://{your-resource-name}.cognitiveservices.azure.com/`.

> [!NOTE]
> For new applications, use the [Document Translation REST API version 2026-03-01](../latest/rest-api/guide-overview.md).

## Synchronous operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Translate a document | `POST` | Translate a single document and receive the translated output in the response. No Blob Storage required. | [Synchronous document translation](translate-document.md) |

## Asynchronous batch operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Start batch translation | `POST` | Submit one or more documents for asynchronous translation. Documents must be in Azure Blob Storage. Returns a job ID. | [Start batch translation](start-batch-translation.md) |
| Get translation status | `GET` | Retrieve the overall status and document summary for a specific batch job. Poll until the job reaches a terminal state. | [Get translation status](get-translation-status.md) |
| Get status for all translations | `GET` | List all batch translation jobs submitted to your resource. Supports filtering and paging. | [Get status for all translation jobs](get-translations-status.md) |
| Get status for all documents | `GET` | Retrieve per-document status for all documents in a specific job. | [Get status for all documents](get-documents-status.md) |
| Get status for a specific document | `GET` | Retrieve status and output details for a single document within a job. | [Get status for a specific document](get-document-status.md) |
| Cancel translation | `DELETE` | Cancel a job that is queued or in progress. | [Cancel translation](cancel-translation.md) |

## Discovery operations

| Operation | Method | Description | Reference |
|---|---|---|---|
| Get supported document formats | `GET` | Retrieve a list of supported document formats and their MIME types. | [Get supported document formats](get-supported-document-formats.md) |
| Get supported glossary formats | `GET` | Retrieve a list of supported glossary formats and their MIME types. | [Get supported glossary formats](get-supported-glossary-formats.md) |

## Earlier v1.1 batch API

The earlier v1.1 API supports asynchronous batch and discovery operations under the `/translator/text/batch/v1.1` path. The `Get supported storage sources` operation is available only in v1.1. Translator supports Azure Blob Storage as the storage source.

We recommend that you migrate existing applications to the latest API version to use current capabilities.

| Operation | Method | API path |
|---|---|---|
| Start batch translation | `POST` | `/translator/text/batch/v1.1/batches` |
| Get status for all translation jobs | `GET` | `/translator/text/batch/v1.1/batches` |
| Get status for a specific translation job | `GET` | `/translator/text/batch/v1.1/batches/{id}` |
| Get status for all documents | `GET` | `/translator/text/batch/v1.1/batches/{id}/documents` |
| Get status for a specific document | `GET` | `/translator/text/batch/v1.1/batches/{id}/documents/{documentId}` |
| Cancel translation | `DELETE` | `/translator/text/batch/v1.1/batches/{id}` |
| Get supported document formats | `GET` | `/translator/text/batch/v1.1/documents/formats` |
| Get supported glossary formats | `GET` | `/translator/text/batch/v1.1/glossaries/formats` |
| Get supported storage sources | `GET` | `/translator/text/batch/v1.1/storagesources` |

## Related content

* [Document Translation overview](../overview.md)
* [Document Translation REST API version 2026-03-01](../latest/rest-api/guide-overview.md)
* [Document translation SDKs](../document-sdk-overview.md)
