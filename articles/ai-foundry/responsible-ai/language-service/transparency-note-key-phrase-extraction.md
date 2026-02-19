---
title: Transparency note - Key Phrase Extraction feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Azure Language in Foundry Tools key phrase extraction allows you to quickly identify the main concepts in text. For example, in the text "The food was delicious and there were wonderful staff", Key Phrase Extraction will return the main talking points "food" and "wonderful staff".
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 09/29/2021
---

# Transparency note for Key Phrase Extraction

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> This article assumes that you're familiar with guidelines and best practices for Azure Language in Foundry Tools. For more information, see [Transparency note for Language](transparency-note.md).

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see Responsible AI principles from Microsoft.

## Introduction to key phrase extraction

Language [Key Phrase Extraction](/azure/ai-services/language-service/key-phrase-extraction/overview) feature allows you to quickly identify the main concepts in text. For example, in the text "The food was delicious and there were wonderful staff", Key Phrase Extraction will return the main talking points: "food" and "wonderful staff". Non-essential words are discarded single terms or phrases that appear to be the subject or object of a sentence are returned.

Note that no confidence score is returned for this feature, unlike some other Language features. 

## Example use cases

Key Phrase Extraction is used in multiple scenarios across a variety of industries. Some examples include:

* **Enhancing search**. Key phrases can be used to create a search index that can enhance search results. For example, customers can provide thousands of documents and then run Key Phrase Extraction on top of it using the built-in [Azure Search skill](/azure/search/cognitive-search-concept-intro). The outcome of this are key phrases from the input dataset, which can then be used to create an index. This index can be updated by running the skill again whenever there is a new document set available.
* **View aggregate trends in text data**. For example, a word cloud can be generated with key phrases to help visualize key concepts in text comments or feedback. For example, a hotel could generate a word cloud based on key phrases identified in their comments and might see that people are commenting most frequently about the location, cleanliness and helpful staff.

## Considerations when choosing a use case

**Do not use**

* Do not use for automatic actions without human intervention for high risk scenarios.  A person should always review source data when another person's economic situation, health or safety is affected.

[!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Characteristics and limitations

Depending on your scenario and input data, you could experience different levels of performance. The following information is designed to help you understand key concepts about performance as they apply to using the Language key phrase extraction feature.

### System limitations and best practices for enhancing performance

Unlike other Language features' models, the key phrase extraction model is an unsupervised model that is not trained on human labeled ground truth data. All of the noun phrases in the text sent to the service are detected and then ranked based on frequency and co-occurrence. Therefore, what is returned by the model may not agree with what a human would choose as the most important phrases. In some cases the model may appear partially correct, in that a noun is returned without the adjective that modifies it.

* Longer text will perform better.  Do not break your source text up into pieces like sentences or paragraphs.  Send the entire text, for example, a complete customer review or paper abstract. 
* If your text includes some boilerplate or other text that has no topical relevance to the actual content you're trying to analyze, the words in this text will affect your results.  For example, emails might have "Subject:", "Body:", "Sender:", etc. included in the text. We recommend removing any known text that is not part of the actual content you are trying to analyze before sending it to the service. 

## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for the health feature](transparency-note-health.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Data Privacy and Security for  Language](data-privacy.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
