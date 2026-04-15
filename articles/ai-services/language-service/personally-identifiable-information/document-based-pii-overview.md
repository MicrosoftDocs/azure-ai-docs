---
title: Document-based Personally Identifiable Information (PII) redaction overview
titleSuffix: Foundry Tools
description: Learn how document-based PII redaction in Azure Language detects and redacts sensitive data from native documents while preserving file structure.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/15/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Document-based Personally Identifiable Information (PII) redaction overview

Document-based PII redaction helps you detect and redact sensitive data directly in native document files. It is designed for workflows where output file quality matters, such as compliance review, external sharing, and record processing.

## Why use document-based PII?

Many custom pipelines require multiple steps to extract text, run detection, and rebuild the document. Document-based PII simplifies this workflow with a single asynchronous API pattern and output artifacts tailored for document operations.

Document-based PII is especially useful when you need to:

* Redact PII in `.pdf`, `.docx`, and `.txt` files.
* Preserve document layout for downstream business processes.
* Generate structured JSON output for auditing and integration.

## What it returns

When a job succeeds, the service returns:

* A redacted document in your target storage container.
* A JSON result file with detected entities, categories, confidence scores, and processing metadata.

## How it works

Document-based PII uses an asynchronous workflow:

1. Submit a job with source and target storage locations.
2. Poll the job status by using the operation location.
3. Retrieve output artifacts from your target storage location.

For implementation details and request samples, see [Detect and redact Personally Identifiable Information in native documents](how-to/redact-document-pii.md).

## How it differs from text PII

Text PII and document-based PII both use predefined entity categories, but they optimize for different goals:

* Text PII is optimized for direct string input and low-latency API integration.
* Document-based PII is optimized for native-file redaction workflows and file output fidelity.

## Supported formats and limits

* Supported formats: `.txt`, `.pdf`, `.docx`
* See [language support](language-support.md) and [quotas and limits](../concepts/data-limits.md) for current support details.

## Pricing

Document-based PII redaction uses Azure AI Language pricing. For current pricing details, see [Azure AI Language pricing](https://aka.ms/unifiedLanguagePricing).

## Next steps

* [Detect and redact Personally Identifiable Information in native documents](how-to/redact-document-pii.md)
* [PII feature overview](overview.md)
