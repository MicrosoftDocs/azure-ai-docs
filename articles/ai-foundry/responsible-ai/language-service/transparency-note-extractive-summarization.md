---
title: Use cases for summarization
titleSuffix: Foundry Tools
description: Summarization is a feature in Azure Language in Foundry Tools that produces a summary by extracting sentences from a document or text conversation. The feature condenses articles, papers, or documents to key sentences.
author: laujan
ms.author: lajanuar
manager: yabinl
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 05/18/2022
---

# Transparency note for summarization

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]


## What is a transparency note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft transparency notes are intended to help you understand how our AI technology works, and the choices that you as a system owner can make that influence system performance and behavior. It's important to think about the whole system, including the technology, the people, and the environment. You can use transparency notes when you develop or deploy your own system, or share them with the people who will use or be affected by your system.

Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Summarization

### Introduction
Summarization uses natural language processing techniques to condense articles, papers, or documents into key sentences. This feature is provided as an API for developers to build intelligent solutions based on the relevant information extracted and can support various use cases.


## Capabilities

### [Document summarization](#tab/document)

Document summarization uses natural language processing techniques to generate a summary for documents. There are two general approaches to auto-summarization: *extractive* and *abstractive*.

### The basics of document extractive summarization

This feature extracts sentences that collectively represent the most important or relevant information within the original content. It locates key sentences in an unstructured text document. These sentences collectively convey the main idea of the document.


### The basics of document abstractive summarization

Different from extractive summarization, document abstractive summarization generates a summary with concise, coherent sentences or words which are not simply extracted from the original document.

### Example use cases

You can use document summarization in multiple scenarios, across a variety of industries. For example, you can use extractive summarization to: 
* **Assist the processing of documents to improve efficiency.** Distill critical information from lengthy documents, reports, and other text forms,highlight key sentences in documents, andquickly skim documents in a library.
* **Extract key information from public news articles** to produce insights such as trends and news spotlights, and generate news feed content.
* **Classify or cluster documents by their contents.** Use Summarization to surface key concepts from documents and use those key concepts to group documents that are similar.
* **Distill important information from long documents** to empower solutions such as search, question and answering, and decision support.


#### [Conversation summarization](#tab/conversation)

Conversation summarization uses natural language processing techniques to generate a structured summary for conversations. This feature supports both natural chat transcripts and transcribed transcripts from phone calls. For a chat or call, there are different kinds of important information, scattered over a long text or transcribed transcripts.

This feature currently focuses on the needs of customer service or a call center. Customer support agents typically spend considerable time and effort writing notes after each call, or while transferring a case to the next level of support. This feature auto-generates a summary of issues and resolutions in a two-party conversation, especially between a customer and an agent.

### Example use cases

You can use conversation summarization in multiple scenarios, across a variety of industries. Some examples include:
* **Customer support:** Summarize the solutions  provided in a customer conversation (for example, what solutions an agent has provided to resolve the customer's issue). 
* **Resource planning:** Classify customer calls to plan for resource allocation and education.
* **Knowledge base:** Distill best practices from previous conversations between a customer and an agent to generate a knowledge base for improved customer engagements.
* **Inventory planning:** Classify customer calls for inventory and procurement planning.
* **Sales call:** Summarize the reason for the call, as well as information or ideas discussed for future action items.
* **Meeting summarization:** Summarize key statements made by participants in a meeting or Segment a long conversation with a short title for each section


---

## Considerations when you choose a use case

We encourage you to come up with use cases that most closely match your own particular context and requirements. Draw on actionable information that enables responsible integration in your use cases, and conduct your own testing specific to your scenarios.

The summarization models reflect certain societal views that are over-represented in the training data, relative to other, marginalized perspectives. The models reflect societal biases and other undesirable content present in the training data. As a result, we caution against using the models in high-stakes scenarios, where unfair, unreliable, or offensive behavior might be extremely costly or lead to harm.

* **Avoid real-time, critical safety alerting.** Don't rely on this feature for scenarios that require real-time alerts to trigger intervention to prevent injury. For example, don't rely on summarization for turning off a piece of heavy machinery when a harmful action is present.

* **The feature isn't suitable for scenarios where up-to-date, factually accurate information is crucial,** unless you have human reviewers. The service doesn't have information about current events after its training date, probably has missing knowledge about some topics, and might not always produce factually accurate information.

* **Avoid scenarios in which the use or misuse of the system could have a consequential impact on life opportunities or legal status.** For example, avoid scenarios in which the AI system could affect an individual's legal status or legal rights. Additionally, avoid scenarios in which the AI system could affect an individual's access to credit, education, employment, healthcare, housing, insurance, social welfare benefits, services, opportunities, or the terms on which they are provided.

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]


## Next steps

* [Transparency note for Azure Language in Foundry Tools](/azure/ai-foundry/responsible-ai/language-service/transparency-note)
* [Transparency note for named entity recognition](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition)
* [Transparency note for health](/azure/ai-foundry/responsible-ai/language-service/transparency-note-health)
* [Transparency note for key phrase extraction](/azure/ai-foundry/responsible-ai/language-service/transparency-note-key-phrase-extraction)
* [Transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis)
* [Guidance for integration and responsible use with language](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use)
* [Data privacy for language](/azure/ai-foundry/responsible-ai/language-service/data-privacy)

