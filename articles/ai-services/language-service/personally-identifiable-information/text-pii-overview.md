---
title: Text Personally Identifiable Information (PII) redaction overview
titleSuffix: Foundry Tools
description: Learn how text PII redaction in Azure Language detects and redacts sensitive data in raw text for applications and workflows.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/15/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Text Personally Identifiable Information (PII) redaction overview

Text PII redaction helps you detect and redact sensitive data in raw text strings. It is designed for application workflows where you process chat messages, logs, prompts, forms, or other text content directly.

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

## How it differs from other PII modalities

All PII modalities use predefined entity categories, but they optimize for different input types:

* Text PII is optimized for direct string-based input and app integration.
* Conversation PII is optimized for turn-based conversational structures.
* Document-based PII is optimized for native-file workflows and file output fidelity.

## Supported formats and limits

* Input format: raw text content
* See [language support](language-support.md) and [quotas and limits](../concepts/data-limits.md) for current support details.

## Pricing

Text PII redaction uses Azure AI Language pricing. For current pricing details, see [Azure AI Language pricing](https://aka.ms/unifiedLanguagePricing).

## Next steps

* [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md)
* [PII feature overview](overview.md)
