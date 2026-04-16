---
title: What is the Personally Identifiable Information (PII) detection feature in Azure Language?
titleSuffix: Foundry Tools
description: An overview of the PII detection feature in Azure Language, which helps you extract entities and sensitive information (PII) in text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/16/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# What is PII detection in Azure Language?

Personally Identifiable Information (PII) detection is an Azure Language [core capability](../overview.md#core-capabilities) that helps you identify, classify, and redact sensitive data across text, conversations, and native documents. Submit content to the service and receive structured output with entity categories, confidence scores, and redacted results based on your API configuration. You can use this capability to implement privacy controls, reduce sensitive data exposure, and support compliance requirements in application and data-processing workflows.

> [!TIP]
> Try PII detection in [Microsoft Foundry](https://ai.azure.com/) and choose the feature type that matches your input data.

## PII documentation by feature type

PII capabilities are grouped by feature type. Each feature type maps to a specific input format and processing model.

:::image type="content" source="media/feature-types.png" alt-text="Screenshot of PII feature types diagram.":::

Choose the feature type that matches your data shape and runtime requirements.

### Text PII

[**Text PII**](text-pii-overview.md) processes string-based payloads and returns synchronous detection and redaction results. Use this feature when your system handles request-time processing for messages, prompts, logs, and other text fields.

Use the following documentation to implement and tune Text PII workloads:

* [Quickstart: Detect personally identifiable information (PII)](quickstart.md)
* [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md)
* [Text PII recognized entity categories (extended format)](concepts/entity-categories.md)
* [Text PII recognized entity categories (list format)](concepts/entity-categories-list.md)

### Conversation PII

[**Conversation PII**](conversation-pii-overview.md) processes multi-turn exchanges and transcript-oriented payloads where turn boundaries and conversation context affect detection and masking behavior. Use this feature for asynchronous workloads that analyze chat and transcript structures.

Use the following documentation to implement Conversation PII job-based processing:

* [Conversation PII overview](conversation-pii-overview.md)
* [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md)
* [Conversation PII recognized entity categories (extended format)](concepts/conversations-entity-categories.md)
* [Conversation PII recognized entity categories (list format)](concepts/conversations-entities-list.md)

### Document-based PII

[**Document-based PII**](document-based-pii-overview.md) processes native files and returns redaction output that preserves document structure while also producing machine-readable metadata. Use this feature for asynchronous, storage-based pipelines that handle `.pdf`, `.docx`, and `.txt` inputs.

Use the following documentation to implement Document-based PII in native-file pipelines:

* [Document-based PII overview](document-based-pii-overview.md)
* [Detect and redact Personally Identifiable Information in native documents](how-to/redact-document-pii.md)

---

## Choose the right PII feature

Use the following table to select the right experience before you start implementation:

| Feature type | Input | Best for | Key strength |
| --- | --- | --- | --- |
| [Text PII](text-pii-overview.md) | Raw text strings | Apps, prompts, logs, tickets | Broad language coverage and flexible redaction options |
| [Conversation PII](conversation-pii-overview.md) | Turn-based chat or transcript data | Contact centers, meetings, voice transcripts | Conversational context and transcript-aware output |
| [Document-based PII](document-based-pii-overview.md) | Native files (`.pdf`, `.docx`, `.txt`) | Compliance workflows and document sharing | Redacted files with document fidelity and JSON metadata |

## Get started

[!INCLUDE [development options](./includes/development-options.md)]

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## What differs across feature types?

All feature types use predefined entity categories and return confidence-scored detections. They differ mainly by input format and processing model:

* **Text PII** is optimized for synchronous string-based input.
* **Conversation PII** is optimized for turn-based transcript and chat structures.
* **Document-based PII** is asynchronous and optimized for processing native files while preserving document structure.

> [!NOTE]
> **Document-based PII** focuses on native-file redaction workflows. Some text-only options are not available in every document API version.

## GA and preview guidance

To avoid integration issues, use API versions and features that match your deployment target:

* Use generally available (GA) API versions for production workloads.
* Use preview API versions only when you need preview-only features.
* Avoid combining request payload examples from different API versions.

Each feature-specific how-to article identifies preview-only sections where applicable.

## Input requirements and service limits

Use the following references to verify language coverage, service limits, and model-version behavior:

* [Language support for text, document, and conversation PII](language-support.md)
* [Quotas and limits](../concepts/data-limits.md)
* [Model lifecycle and API version guidance](../concepts/model-lifecycle.md)

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Responsible AI

You should design responsible solutions by considering the model behavior, the users who operate the system, and the people affected by the output. Read the [transparency note for PII](/azure/ai-foundry/responsible-ai/language-service/transparency-note-personally-identifiable-information) to understand responsible deployment guidance. For more information, see the following articles:

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Common use cases

PII detection is useful when you need to apply privacy controls before storage, analytics, sharing, or downstream AI processing.

Typical examples include:

* Applying sensitivity labels based on detected PII categories.
* Redacting personal information in documents that are distributed more broadly.
* Masking personal identifiers in resume screening workflows to reduce bias risk.
* Replacing sensitive values with placeholders in machine learning training datasets.
* Redacting names and contact details in call center transcription workflows.
* Preparing datasets for analytics and data science without exposing customer data.

## Next steps

Use the following references to continue implementation:

* [Quickstart: Detect personally identifiable information (PII)](quickstart.md)
* [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md)
* [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md)
* [Detect and redact Personally Identifiable Information in native documents](how-to/redact-document-pii.md)
* [Language support for text, document, and conversation PII](language-support.md)
* [Quotas and limits](../concepts/data-limits.md)
