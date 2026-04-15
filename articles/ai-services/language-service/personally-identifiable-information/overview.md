---
title: What is the Personally Identifiable Information (PII) detection feature in Azure Language?
titleSuffix: Foundry Tools
description: An overview of the PII detection feature in Azure Language, which helps you extract entities and sensitive information (PII) in text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 04/15/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# What is PII detection in Azure Language?

Personally Identifiable Information (PII) detection is an Azure Language [core capability](../overview.md#core-capabilities). It helps you **detect and redact** sensitive personal data in text, conversations, and native documents.

> [!TIP]
> Try PII detection in [Microsoft Foundry](https://ai.azure.com/) and choose the modality that matches your scenario.

---

## Choose the right PII modality

Use the following table to select the right experience before you start implementation:

| Modality | Input | Best for | Key strength |
| --- | --- | --- | --- |
| [Text PII](text-pii-overview.md) | Raw text strings | Apps, prompts, logs, tickets | Broad language coverage and flexible redaction options |
| [Conversation PII](conversation-pii-overview.md) | Turn-based chat or transcript data | Contact centers, meetings, voice transcripts | Conversational context and transcript-aware output |
| [Document-based PII](document-based-pii-overview.md) | Native files (`.pdf`, `.docx`, `.txt`) | Compliance workflows and document sharing | Redacted files with document fidelity and JSON metadata |

## Get started

[!INCLUDE [development options](./includes/development-options.md)]

For hands-on setup, start with:

* [Quickstart: Detect personally identifiable information (PII)](quickstart.md)
* [Detect and redact Personally Identifiable Information in text](how-to/redact-text-pii.md)
* [Detect and redact Personally Identifiable Information in conversations](how-to/redact-conversation-pii.md)
* [Detect and redact Personally Identifiable Information in native documents](how-to/redact-document-pii.md)

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

## What differs across modalities?

All modalities use predefined entity categories and return PII detections with confidence scores. The implementation model differs by input type:

* Text PII is optimized for synchronous string-based input.
* Conversation PII is optimized for turn-based transcript and chat structures.
* Document-based PII is asynchronous and optimized for processing native files while preserving document structure.

> [!NOTE]
> Document-based PII focuses on document redaction workflows. Some text-only configuration options may not be available in every document API version.

## GA and preview guidance

To avoid unexpected behavior, use API versions and features that match your deployment target:

* Use generally available (GA) API versions for production workloads.
* Use preview API versions only when you need preview-only features.
* Avoid combining request payload examples from different API versions.

Each modality how-to article calls out preview-specific sections where applicable.

## Input requirements and service limits

* [Language support for text, document, and conversation PII](language-support.md)
* [Quotas and limits](../concepts/data-limits.md)
* [Model lifecycle and API version guidance](../concepts/model-lifecycle.md)

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people affected by it, and the deployment environment. Read the [transparency note for PII](/azure/ai-foundry/responsible-ai/language-service/transparency-note-personally-identifiable-information) to learn about responsible AI use and deployment in your systems. For more information, see the following articles:

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Example scenarios

* **Apply sensitivity labels** - For example, based on the results from the PII service, a public sensitivity label might be applied to documents where no PII entities are detected. For documents where US addresses and phone numbers are recognized, a confidential label might be applied. A highly confidential label might be used for documents where bank routing numbers are recognized.
* **Redact some categories of personal information from documents that get wider circulation** - For example, if customer contact records are accessible to frontline support representatives, the company can redact the customer's personal information besides their name from the version of the customer history to preserve the customer's privacy.
* **Redact personal information in order to reduce unconscious bias** - For example, during a company's resume review process, they can block name, address, and phone number to help reduce unconscious gender or other biases.
* **Replace personal information in source data for machine learning to reduce unfairness** – For example, if you want to remove names that might reveal gender when training a machine learning model, you could use the service to identify them and you could replace them with generic placeholders for model training.
* **Remove personal information from call center transcription** – For example, if you want to remove names or other PII data that happen between the agent and the customer in a call center scenario. You could use the service to identify and remove them.
* **Data cleaning for data science** - PII can be used to make the data ready for data scientists and engineers to be able to use these data to train their machine learning models. Redacting the data to make sure that customer data isn't exposed.

## Next steps

* [Text PII overview](text-pii-overview.md)
* [Conversation PII overview](conversation-pii-overview.md)
* [Document-based PII overview](document-based-pii-overview.md)
* [Native document PII how-to](how-to/redact-document-pii.md)
