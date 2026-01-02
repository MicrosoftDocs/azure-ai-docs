---
title: Use cases for summarization
titleSuffix: Foundry Tools
description: Summarization is a feature in Azure Language in Foundry Tools that produces a summary by extracting sentences from a document or text conversation. The feature condenses articles, papers, or documents to key sentences.
author: laujan
ms.author: lajanuar
manager: yabinl
ms.service: azure-ai-language
ms.topic: article
ms.date: 05/18/2022
---

# Transparency note for summarization

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]


## What is a transparency note?

A transparency note explains how an AI feature works, its capabilities and limitations, and the factors that can influence its behavior and performance.
<!-- Edited to replace multi-paragraph boilerplate with a single fact-bearing sentence -->

Transparency notes are intended to support informed design, deployment, and use decisions by system owners and stakeholders.
<!-- Edited to remove marketing language and clarify intent in one sentence -->

Transparency notes reflect Microsoft’s broader responsible AI commitments. For more information, see [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).
<!-- Edited to condense program-level context into a single factual statement -->

## The basics of Summarization

### Introduction
Summarization uses natural language processing techniques to condense articles, papers, or documents into key sentences. This feature is provided as an API for developers to build intelligent solutions based on extracted information and supports multiple use cases.
<!-- Minor edit to remove promotional phrasing and keep one clear intent -->

## Capabilities

### [Document summarization](#tab/document)

Document summarization generates a summary for documents using natural language processing techniques. There are two general approaches to auto-summarization: *extractive* and *abstractive*.
<!-- Edited to reduce repetition and remove non-essential wording -->

### The basics of document extractive summarization

Extractive summarization identifies and returns sentences from the original text that represent the most important information. The selected sentences collectively convey the main idea of the document.
<!-- Edited for clarity and concision -->

### The basics of document abstractive summarization

Abstractive summarization generates new sentences or phrases that capture the core meaning of the document rather than directly extracting text.
<!-- Edited to simplify comparison wording -->

### Example use cases

You can use document summarization across a variety of industries and scenarios. For example, extractive summarization can:
<!-- Edited to remove generic phrasing -->

* **Assist document processing.** Distill critical information from lengthy documents and highlight key sentences to support efficient review.
<!-- Edited to remove marketing tone and fix spacing issues -->

* **Extract key information from public news articles** to identify trends, generate insights, or produce summarized news content.

* **Classify or cluster documents by content.** Use summarized key concepts to group documents with similar topics.

* **Support downstream solutions** such as search, question answering, and decision support by distilling important information from long documents.
<!-- Edited to reduce promotional language -->

#### [Conversation summarization](#tab/conversation)

Conversation summarization generates structured summaries from chat transcripts or transcribed phone calls, where relevant information may be distributed across long conversations.
<!-- Edited to condense explanation into a single sentence -->

This capability is designed primarily for customer service and call center scenarios, where agents typically document issues and resolutions after or during calls.
<!-- Edited to remove repetitive detail -->

The feature generates summaries of issues and resolutions in two-party conversations, such as interactions between a customer and a support agent.
<!-- Edited for clarity and focus -->

### Example use cases

You can use conversation summarization in several scenarios, including:
<!-- Edited to remove boilerplate phrasing -->

* **Customer support:** Summarize solutions provided during customer interactions.

* **Resource planning:** Classify customer calls to support staffing, training, and resource allocation.

* **Knowledge base creation:** Distill recurring issues and resolutions from past conversations.

* **Inventory planning:** Classify customer calls to inform inventory and procurement decisions.

* **Sales calls:** Summarize call reasons and discussion points for follow-up actions.

* **Meeting summarization:** Summarize key statements or segment long conversations into titled sections.
<!-- Edited to standardize tone and remove redundancy -->

---

## Considerations when you choose a use case

Choose use cases that align with your specific context and requirements, and conduct scenario-specific testing to support responsible integration.
<!-- Edited to condense guidance into one actionable sentence -->

Summarization models may reflect biases present in their training data and can generate unfair or undesirable content. As a result, avoid high-stakes scenarios where inaccurate or biased output could cause harm.
<!-- Edited to reduce repetition and clarify risk -->

* **Avoid real-time, critical safety alerting.** Do not rely on summarization for scenarios that require immediate intervention to prevent injury, such as controlling heavy machinery.

* **The feature is not suitable for scenarios requiring up-to-date or fully accurate information** without human review. The models lack awareness of events after training and may produce incomplete or inaccurate outputs.

* **Avoid scenarios with significant legal or life-impacting consequences.** Do not use summarization in contexts that could affect legal status, rights, or access to essential services such as credit, employment, healthcare, housing, or social benefits.

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]


## Next steps

* [Transparency note for Azure Language in Foundry Tools](/azure/ai-foundry/responsible-ai/language-service/transparency-note)
* [Transparency note for named entity recognition](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition)
* [Transparency note for health](/azure/ai-foundry/responsible-ai/language-service/transparency-note-health)
* [Transparency note for key phrase extraction](/azure/ai-foundry/responsible-ai/language-service/transparency-note-key-phrase-extraction)
* [Transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis)
* [Guidance for integration and responsible use with language](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use)
* [Data privacy for language](/azure/ai-foundry/responsible-ai/language-service/data-privacy)