---
title: Transparency note - Named Entity Recognition feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Azure Language in Foundry Tools supports named entity recognition to identify and categorize information in your text. The Personally Identifiable Information (PII) feature is part of NER and it can identify and redact sensitive entities in text that are associated with an individual person such as phone number, email address, mailing address, passport number.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/10/2021
---

# Transparency note for Named Entity Recognition including Personally Identifiable Information (PII)

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> This article assumes that you're familiar with guidelines and best practices for Azure Language in Foundry Tools. For more information, see [Transparency note for Language](transparency-note.md).

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see Responsible AI principles from Microsoft.

## Introduction to Named Entity Recognition and Personally Identifiable Information (PII)

Language supports [named entity recognition](/azure/ai-services/language-service/named-entity-recognition/overview) to identify and categorize information in your text. These include general entities such as Product and Event and Personally Identifiable Information (PII) entities. A [wide variety of personal entities](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=personal) such as names, organizations, addresses, phone numbers, [financial account numbers](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=personal#identification) or codes and [government and country or region specific identification numbers](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=personal#government-and-countryregion-specific-identification) can be recognized. A subset of these personal entities is protected health information (PHI). If you specify domain=phi in your request, you will only get the PHI entities returned. The full list of PII and PHI entity categories can be found in the table [here](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=personal). In addition, the PII recognition supports the ability to specify specific entity categories you want in the response and redact PII entities in the response.  The PII entities will be replaced by asterisks in the `redactedText` property of the response.

[Read example NER request and example response](/azure/ai-services/language-service/named-entity-recognition/quickstart) to see how to send text to the service and what to expect back.

## Example use cases

Customers may want to recognize various categories of named entities two main reasons:

* **Enhance search capabilities** - Customers can build knowledge graphs based on entities detected in documents to enhance document search.
* **Enhance or automate business processes** - For example, when reviewing insurance claims, recognized entities like name and location could be highlighted to facilitate the review.  Or a support ticket could be generated with a customer's name and company automatically from an email.

Customers may want to recognize various categories of PII entities specifically for several reasons:

* **Apply sensitivity labels** - For example, based on the results from the PII service, a public sensitivity label might be applied to documents where no PII entities are detected. For documents where US addresses and phone numbers are recognized, a confidential label might be applied. A highly confidential label might be used for documents where bank routing numbers are recognized.
* **Redact some categories of personal information from documents to protect privacy** - For example, if customer contact records are accessible to first line support representatives, the company may want to redact unnecessary customer's personal information from customer history to preserve the customer's privacy.
* **Redact personal information in order to reduce unconscious bias** - For example, during a company's resume review process, they may want to block name, address and phone number to help reduce unconscious gender or other biases.
* **Replace personal information in source data for machine learning to reduce unfairness** – For example, if you want to remove names that might reveal gender when training a machine learning model, you could use the service to identify them and you could replace them with generic placeholders for model training.

## Considerations when choosing a use case

**Do not use**

* PII only - Do not use for automatic redaction or information classification scenarios – Any scenario where failures to redact personal information could expose people to the risk of identity theft and physical or psychological harms should include careful human oversight.
* NER and PII - Do not use for scenarios that use personal information for a purpose that consent was not obtained for - For example, a company has resumes from past job applicants. The applicants did not give their consent to be contacted for promotional events when they submitted their resumes. Based on this scenario, both NER and PII services should not be used to identify contact information for the purpose of inviting the past applicants to a trade show.
* NER and PII - Customers are prohibited from using of this service to harvest personal information from publicly available content without consent from person(s) whom are the subject of the personal information.
* NER and PII - Do not use for scenarios that replace personal information in text with the intent to mislead people.

[!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]
## Characteristics and limitations

Depending on your scenario, input data and the entities you wish to extract, you could experience different levels of performance. The following sections are designed to help you understand key concepts about performance as they apply to using the Language NER and PII services.

### Understand and measure performance of NER

Since both false positive and false negative errors can occur, it is important to understand how both types of errors might affect your overall system. With Named Entity Recognition (NER), a false positive occurs when an entity is not present in the text, but is recognized and returned by the system.  A false negative is when an entity is present in the text, but is not recognized and returned by the system. 

#### Understanding performance for PII

In redaction scenarios, for example, false negatives could lead to personal information leakage. For redaction scenarios, consider a process for human review to account for this type of error. For sensitivity label scenarios, both false positives and false negatives could lead to misclassification of documents. The audience may unnecessarily limited for documents labelled as confidential where a false positive occurred. PII could be leaked where a false negative occurred and a public label was applied.

You can adjust the threshold for confidence score your system uses to tune your system. If it is more important to identify all potential instances of PII, you can use a lower threshold. This means that you may get more false positives (non- PII data being recognized as PII entities), but fewer false negatives (PII entities not recognized as PII). If it is more important for your system to recognize only true PII data, you can use a higher threshold. Threshold values may not have consistent behavior across individual categories of PII entities. Therefore, it is critical that you test your system with real data it will process in production.

### System limitations and best practices for enhancing performance

* Make sure you understand all the entity categories for [NER](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=general) and [PII](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=personal) that can be recognized by the system. Depending on your scenario, your data may include other information that could be considered personal but is not covered by the categories the service currently supports.
* Context is important for all entity categories to be correctly recognized by the system, as it often is for humans to recognize an entity. For example, without context a ten-digit number is just a number. However, given context like "You can reach me at my office phone number 2345678901," both the system and a human can recognize the ten-digit number as a phone number. Always include context when sending text to the system to obtain the best possible performance.
* Person names in particular require linguistic context. Send as much context as possible for better person name detection.
* For conversational data, consider sending more than a single turn in the conversation to ensure higher likelihood that the required context is included with the actual entities.  
  In the following conversation, if you send a single row at a time, the passport number will not have any context associated with it and the EU Passport Number PII category will not be recognized. 
  > Hi, how can I help you today? <br/>
  >I want to renew my passport <br/>
  > Sure, what is your current passport number? <br/>
  > Its 123456789, thanks. 

  However, if you send the whole conversation it will be recognized because the context is included.
* Sometimes multiple entity categories can be recognized for the same entity. If we take the previous example:
  > Hi, how can I help you today?<br/>
  > I want to renew my passport<br/>
  > Sure, what is your current passport number?<br/>
  > Its 123456789, thanks.<br/>

  Several different countries have the same format for passport numbers, so several different specific entity categories may be recognized. In some cases, using the highest confidence score may not be sufficient to choose the right entity class. If your scenario depends on the specific entity category being recognized, you may need to disambiguate the result elsewhere in your system either through a human review or additional validation code. Thorough testing on real life data can help you identify if you're likely to see multiple entity categories for recognized for your scenario.<br/>

* Not all entity categories are supported in all languages for both NER and PII.  Be sure to check the [entity type](/azure/ai-services/language-service/named-entity-recognition/concepts/named-entity-categories?tabs=general) article for the entities in the language you want to detect.

* Many international PII entities are supported. By default, the entity categories returned are those that match the language code sent with the API call. If you expect entities from locales other than the one specified, you will need to specify them with the `piiCategories` parameter. Learn more about how to specify what your response will include in the [API reference](https://westus2.dev.cognitive.microsoft.com/docs/services/TextAnalytics-v3-1/operations/EntitiesRecognitionPii). Learn more about the categories supported for each locale in the [named entity types documentation](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories).

* In PII redaction scenarios, if you are using the version of the API that includes the optional parameter `piiCategories`, it is important that you consider all the PII categories that could be present in your text. If you are redacting only specific entity categories or the default entity categories for a specific locale, other PII entity categories that unexpectedly appear in your text will be leaked. For example, if you have sent the EN-US locale and not specified any optional PII categories and a German Driver's License Number is present in your text, it will be leaked. To prevent this you would need to specify the German Driver's License Number category in the `piiCategories` parameter.  In addition, if you have specified one or more categories using the `piiCategories` parameter for the specified locale, be aware that those are the *only* categories that would be redacted. For example, if you have sent the EN-US locale and have specified U.S. Social Security Number (SSN) as the PII category for redaction, then any other EN-US categories such as U.S. Driver's License Number or U.S. Passport Number would be leaked if they appear in the input text.

* Since the PII service returns PII categories that match the language code in the call, consider verifying the language the input text is in if you're not sure what language or locale it will be. You can use the [Language Detection](/azure/ai-services/language-service/language-detection/overview) feature to do this.

* The PII service only takes text as an input. If you are redacting information from documents in other formats, make sure to carefully test your redaction code to ensure identified entities are not accidentally leaked.


## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for the health feature](transparency-note-health.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Data Privacy and Security for  Language](data-privacy.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
