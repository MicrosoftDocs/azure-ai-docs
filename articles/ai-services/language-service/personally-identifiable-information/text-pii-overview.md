---
title: Text Personally Identifiable Information (PII) redaction overview
titleSuffix: Foundry Tools
description: Learn how text PII redaction in Azure Language detects and redacts sensitive data in raw text for applications and workflows.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/16/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Text Personally Identifiable Information (PII) redaction overview

Text PII redaction in Azure AI Language helps you detect and redact sensitive data in raw text strings. You can use this feature when your application handles logs, prompts, forms, chat messages, or other text content directly.

Text PII is optimized for synchronous request/response integration and configurable redaction behavior, so you can apply PII controls inline in application and data-processing workflows.

## At a glance

Text PII provides the following capabilities:

* Direct text redaction for unstructured string input.
* Low-latency request/response integration for application pipelines.
* Configurable entity filters and redaction policies.
* Structured entity output with categories, offsets, and confidence scores.

## Why use text PII?

Text PII is optimized for low-latency integration and direct request/response workflows. It supports broad language coverage and configurable redaction behavior for many real-time and batch scenarios.

Text PII is especially useful when you need to:

* Redact sensitive entities in user-generated text.
* Integrate PII protection directly into application pipelines.
* Apply entity filters and redaction policies in API requests.

## What it returns

When a request succeeds, the service returns:

* Detected entities with categories, subcategories, offsets, and confidence scores.
* Redacted text output based on your selected redaction behavior.

## How it works

Text PII is typically used with a synchronous workflow:

1. Submit text input for analysis.
2. Configure optional parameters like entity filters and redaction behavior.
3. Process entities and redacted output in your application.

For implementation details and request samples, see [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md).

## How it differs from other PII feature types

All PII feature types use predefined entity categories, but they optimize for different input types:

* Text PII is optimized for direct string-based input and app integration.
* Conversation PII is optimized for turn-based conversational structures.
* Document-based PII is optimized for native-file workflows and file output fidelity.

## Common use cases

Text PII is useful when you need to detect and redact sensitive data before storage, analytics, sharing, or downstream AI processing.

Typical examples include:

* User input and output fields in web and mobile applications.
* Application logs and telemetry data streams.
* Prompt and response filtering in AI workflows.
* Batch preprocessing for unstructured text datasets.

## Supported formats and limits

* Input format: raw text content
* See [language support](language-support.md) and [quotas and limits](../concepts/data-limits.md) for current support details.

## Pricing

Text PII redaction uses Azure AI Language pricing. For current pricing details, see [Azure AI Language pricing](https://aka.ms/unifiedLanguagePricing).

## Next steps

Use the following references to continue implementation:

* [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md)
* [PII feature overview](overview.md)
