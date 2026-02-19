---
title: Transparency note - Language Detection feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: The language detection feature of Azure Language in Foundry Tools detects the language an input text is written in and reports a single language code for every document submitted on the request in a wide range of languages, variants, dialects, and some regional/cultural languages. The language code is paired with a confidence score.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 01/31/2024
---

# Transparency note for Language Detection

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> This article assumes that you're familiar with guidelines and best practices for Azure Language in Foundry Tools. For more information, see [Transparency note for Language](transparency-note.md).

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see Responsible AI principles from Microsoft.

## Introduction to language detection

The [language detection](/azure/ai-services/language-service/language-detection/overview) feature of Language detects the language an input text is written in and reports a single language code for every document submitted on the request in a wide range of languages, variants, dialects, and some regional/cultural languages. The language code is paired with a confidence score.

Be sure to check the list of [supported languages](/azure/ai-services/language-service/language-detection/language-support) to ensure the languages you need are supported.

## Example use cases

Language detection is used in multiple scenarios across a variety of industries. Some examples include:

* **Preprocessing text of other Language features**. Other Language features require a language code to be sent in the request to identify the source language. If you don't know the source language of your text, you can use language detection as a pre-processor to obtain the language code.

* **Detect languages for business workflow**. For example, if a company receives email in various languages from customers, they could use language detection to route the emails by language to native speakers that can communicate best with those customers.

## Considerations when choosing a use case

**Do not use** 
* Do not use for automatic actions without human intervention for high risk scenarios.  A person should always review source data when another person's economic situation, health or safety is affected.

[!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Characteristics and limitations

Depending on your scenario and input data, you could experience different levels of performance. The following information is designed to help you understand key concepts about performance as they apply to using Language's language detection.

### System limitations and best practices for enhancing performance

* For inputs that include [mixed-language content](/azure/ai-services/language-service/language-detection/how-to/call-api) only a single language is returned. In general the language with the largest representation in the content is returned, but with a lower confidence score.
* The service does not yet support the romanized versions of all languages that do not use the Latin script. For example, Pinyin is not supported for Chinese and Franco-Arabic is not supported for Arabic.
* Some words exist in multiple languages. For example, "impossible" is common to both English and French. For short samples that include ambiguous words, you may not get the right language.  
* If you have some idea about the country or region of origin of your text, and you encounter mixed languages, you can use the `countryHint` [parameter](/azure/ai-services/language-service/language-detection/how-to/call-api#ambiguous-content) to pass in a 2 letter country/region code.
* In general longer inputs are more likely to be correctly recognized.  Full phrases or sentences are more likely to be correctly recognized than single words or sentence fragments.
* Not all languages will be recognized. Be sure to check the list of [supported languages and scripts](/azure/ai-services/language-service/language-detection/language-support).
* To distinguish between multiple scripts used to write certain languages such as Kazakh, the language detection feature returns a script name and script code according to the [ISO 15924 standard](https://wikipedia.org/wiki/ISO_15924) for a limited set of scripts.
* The service supports language detection of text only if it is in native script.  For example, Pinyin is not supported for Chinese and Franco-Arabic is not supported for Arabic.
* Due to unknown gaps in our training data, certain dialects and language varieties less represented in web data may not be properly recognized.

## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for Health](transparency-note-health.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Data Privacy and Security for  Language](data-privacy.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
