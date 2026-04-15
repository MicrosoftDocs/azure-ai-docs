---
title: Conversation Personally Identifiable Information (PII) redaction overview
titleSuffix: Foundry Tools
description: Learn how conversation PII redaction in Azure Language detects and redacts sensitive data in turn-based conversational inputs.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/15/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Conversation Personally Identifiable Information (PII) redaction overview

Conversation PII redaction helps you detect and redact sensitive data in chat and transcript-style conversation input. It is designed for scenarios like customer support conversations, call transcripts, and meeting transcripts.

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

## How it differs from other PII modalities

All PII modalities use predefined entity categories, but they optimize for different input types:

* Conversation PII is optimized for turn-based and transcript-oriented conversational input.
* Text PII is optimized for direct string-based input and app integration.
* Document-based PII is optimized for native-file workflows and file output fidelity.

## Supported formats and limits

* Input format: conversation items (chat or transcript structures)
* See [language support](language-support.md) and [quotas and limits](../concepts/data-limits.md) for current support details.

## Pricing

Conversation PII redaction uses Azure AI Language pricing. For current pricing details, see [Azure AI Language pricing](https://aka.ms/unifiedLanguagePricing).

## Next steps

* [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md)
* [PII feature overview](overview.md)
