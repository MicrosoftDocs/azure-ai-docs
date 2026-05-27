---
title: "End-to-end Batch Translation Workflow"
titleSuffix: Foundry Tools
description: Learn how to manage the full lifecycle of an asynchronous batch translation job, from submitting a job to monitoring status, retrieving results, and canceling jobs.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# End-to-end batch translation workflow

Batch document translation is an asynchronous workflow with a fixed API call sequence. It differs from [synchronous translation](rest-api/translate-synchronous.md) in that the service processes your documents in the background and stores the translated output in your Azure Blob Storage target container. Because each step depends on the previous one, understanding the full sequence helps you build reliable, retry-safe integrations. Here, we walk you through each step in order:

* **Submit** a translation job and capture the returned job ID.
* **Poll** for job-level and document-level status until the job reaches a terminal state.
* **Retrieve** translated output from your Azure Blob Storage target container.
* **Optionally list** all jobs or **cancel** an in-progress job.

## Workflow overview

The batch translation API exposes the following operations. Each step builds on the previous one: you need the job ID from Step 2 before you can call any of the status or cancel endpoints.

1. [**Start a batch translation job**](rest-api/translate-asynchronous.md): `POST` a request with your source and target container URLs and target language. The service queues the job and returns a `202 Accepted` response.
1. [**Capture the job ID**](rest-api/translate-asynchronous.md): Extract the GUID from the `operation-location` response header. This ID is required for all subsequent status and cancel calls.
1. [**GET job status**](rest-api/get-status-specific-translation.md): `GET` the overall job state and a document summary. Poll until the status reaches a terminal state: `Succeeded`, `Failed`, `Cancelled`, or `ValidationFailed`.
1. [**GET status for all documents**](rest-api/get-status-all-documents.md): `GET` per-document status for a completed or failed job. Supports paging, sorting, and filtering for large document sets.
1. [**GET status for a specific document**](rest-api/get-status-specific-document.md): `GET` status and error details for one document by `jobId` and `documentId`. Use this to retrieve the output URL or diagnose a single document failure.
1. [**List all jobs**](rest-api/get-status-all-translations.md): `GET` all translation jobs submitted to the resource, with paging and filtering. Useful for auditing or recovering a job ID.
1. [**Cancel a job**](rest-api/cancel-translation.md): `DELETE` a job in `NotStarted` or `Running` state. Documents that have already completed are retained in the target container and billed normally.

## Step 1: Start a batch translation job

Submit an asynchronous translation job using the Start batch translation API. The request body specifies your source and target Azure Blob Storage container URLs and the target language. Each target language requires a unique `targetUrl`.

```bash
   POST {endpoint}/translator/document/batches?api-version=2026-03-01
```

> [!IMPORTANT]
> If a file with the same name already exists in the target container, the job fails. Ensure your target container is empty or that file names don't conflict before submitting.

For the full request schema, see [Start batch translation](rest-api/translate-asynchronous.md).

## Step 2: Capture the job ID

Extract and store the job ID from the `operation-location` response header returned with the `202 Accepted` response. The job ID is the GUID in the path segment of that URL and is required for all subsequent status and cancel calls.

```bash
operation-location: {endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
```

## Step 3: GET job status

Poll the job status endpoint to retrieve the overall state of the translation job and a summary of document-level results. Call this endpoint repeatedly until the status transitions out of `NotStarted` or `Running` to a terminal state.

```bash
GET {endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
```

The response includes a `status` field that returns one of the following values: `NotStarted`, `Running`, `Succeeded`, `Failed`, `Cancelled`, `Cancelling`, or `ValidationFailed`.

For response details, see [GET translation status](rest-api/get-status-specific-translation.md).

## Step 4: GET status for all documents in a job

Retrieve the translation status for each document in a job. Use this operation when the overall job status shows `Succeeded` or `Failed` and you need to identify which individual documents completed, failed, or were skipped. The response supports paging, sorting, and filtering so you can efficiently query large jobs.

```bash
GET {endpoint}/translator/document/batches/{jobId}/documents?api-version=2026-03-01
```

For response details, see [GET status for all documents](rest-api/get-status-all-documents.md).

## Step 5: GET status for a specific document

Retrieve status details for a single document using both the job ID and the `documentId`. This is the most efficient way to get error details or the output URL for one document without paging through the full document list. The `documentId` is returned in the response from the **GET status for all documents** operation.

```bash
GET {endpoint}/translator/document/batches/{jobId}/documents/{documentId}?api-version=2026-03-01
```

For response details, see [GET document status](rest-api/get-status-specific-document.md).

## Step 6: List all jobs

Retrieve all translation jobs submitted to your resource. This operation supports paging and filtering, which is useful for auditing job history, tracking submission patterns, or recovering a job ID you didn't capture at submission time.

```bash
GET {endpoint}/translator/document/batches?api-version=2026-03-01
```

For response details, see [GET status for all translation jobs](rest-api/get-status-all-translations.md).

## Step 7: Cancel a job

Cancel a job that is in a `NotStarted` or `Running` state. The service attempts to halt processing, but any documents that have already completed translation are retained in your target container and billed normally. Jobs in a terminal state (`Succeeded`, `Failed`, `Cancelled`) can't be canceled.

```bash
DELETE {endpoint}/translator/document/batches/{jobId}?api-version=2026-03-01
```

For request details, see [Cancel translation](rest-api/cancel-translation.md).

## Related content

* [REST API guide](rest-api/guide-overview.md)
* [Start batch translation](rest-api/translate-asynchronous.md)
* [Synchronous translation](rest-api/translate-synchronous.md)