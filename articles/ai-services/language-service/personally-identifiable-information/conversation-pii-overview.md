---
title: Conversation Personally Identifiable Information (PII) redaction overview
titleSuffix: Foundry Tools
description: Learn how conversation PII redaction in Azure Language detects and redacts sensitive data in turn-based conversational inputs.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/16/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Conversation Personally Identifiable Information (PII) redaction overview

Conversation PII redaction in Azure AI Language helps you detect and redact sensitive data in turn-based conversational input. You can use this feature for chat and transcript workflows such as customer support conversations, call transcripts, and meeting transcripts.

Conversation PII is optimized for asynchronous conversation jobs and conversation-level context, so you can redact sensitive data across multiple speakers and turns.

## At a glance

Conversation PII provides the following capabilities:

* Redaction for multi-turn conversation structures.
* Asynchronous processing for transcript-style workloads.
* Conversation-level handling across speakers and turns.
* Structured entity output with redacted conversation content.

## Why use conversation PII?

Conversation PII is optimized for turn-based dialogue structures and supports conversational context that differs from single-block text inputs.

Conversation PII is especially useful when you need to:

* Redact sensitive entities in multi-turn conversation data.
* Process transcript inputs from call center and speech workflows.
* Preserve conversation-level context while masking sensitive information.

## What it returns

When a job succeeds, the service returns:

* Detected entities with categories, subcategories, and confidence scores.
* Redacted conversation output for conversation items.
* Optional transcript-oriented metadata for supported transcript workflows.

## How it works

Conversation PII uses an asynchronous workflow:

1. Submit conversation items as a conversation job.
2. Poll the job status.
3. Retrieve entities and redacted conversation output.

For implementation details and request samples, see [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md).

## How it differs from other PII feature types

All PII feature types use predefined entity categories, but they optimize for different input types:

* Conversation PII is optimized for turn-based and transcript-oriented conversational input.
* Text PII is optimized for direct string-based input and app integration.
* Document-based PII is optimized for native-file workflows and file output fidelity.

## Common use cases

Conversation PII is useful when teams need to anonymize conversational data before storage, analytics, quality review, external sharing, or downstream AI processing.

Typical examples include:

* Call center transcripts and quality-assurance workflows.
* Customer support chat logs.
* Meeting transcripts and collaboration records.
* Multi-turn conversational datasets for analytics and model evaluation.

## Supported formats and limits

* Input format: conversation items (chat or transcript structures)
* See [language support](language-support.md) and [quotas and limits](../concepts/data-limits.md) for current support details.

## Pricing

Conversation PII redaction uses Azure AI Language pricing. For current pricing details, see [Azure AI Language pricing](https://aka.ms/unifiedLanguagePricing).

## Next steps

Use the following references to continue implementation:

* [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md)
* [PII feature overview](overview.md)
