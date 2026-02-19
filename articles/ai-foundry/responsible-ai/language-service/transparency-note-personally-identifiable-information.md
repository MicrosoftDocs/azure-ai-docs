---
title: Transparency note - Personally Identifiable Information (PII) feature of Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: The Azure Language Personally Identifiable Information (PII) feature is part of named entity recognition (NER) and it can identify and redact sensitive entities in text that are associated with an individual person such as phone number, email address, mailing address, passport number.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/05/2025
---

# Transparency note for Personally Identifiable Information (PII)

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

> [!IMPORTANT]
> This article assumes that you're familiar with guidelines and best practices for Azure Language. For more information, see [Transparency note for Azure Language](transparency-note.md).

An AI system includes not only the technology, but also the people who use it, the people affected by it, and the environment where it's deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment.

You can use Transparency Notes when developing or deploying your own system, or share them with the people who use or are affected by your system.

Microsoft's Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see Responsible AI principles from Microsoft.

## Introduction to the Personally Identifiable Information (PII) feature

Azure Language supports named entity recognition to identify and categorize information in your text. [The PII feature](/azure/ai-services/language-service/personally-identifiable-information/overview) supports the detection of personal (PII) categories of entities. A [wide variety of personal entities](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories) such as names, organizations, addresses, phone numbers, [financial account numbers](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories#category-international-banking-account-number-iban), or codes and [government and country or region specific identification numbers](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories#government-and-countryregion-specific-identification) can be recognized. A subset of these personal entities is protected health information (PHI). If you specify domain=phi in your request, you only get the PHI entities returned. The full list of PII and PHI entity categories can be found in the table [here](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories?branch=release-cogsvcs-language-service).

[Read example NER request and example response](/azure/ai-services/language-service/personally-identifiable-information/quickstart    ) to see how to send text to the service and what to expect back.

## Example use cases

Customers may want to recognize various categories of PII for several reasons:

* **Apply sensitivity labels** - For example, based on the results from the PII service, a public sensitivity label might be applied to documents where no PII entities are detected. For documents where US addresses and phone numbers are recognized, a confidential label might be applied. A highly confidential label might be used for documents where bank routing numbers are recognized.
* **Redact some categories of personal information from documents that get wider circulation** - For example, if customer contact records are accessible to frontline support representatives, the company may want to redact the customer's personal information besides their name from the version of the customer history to preserve the customer's privacy.
* **Redact personal information in order to reduce unconscious bias** - For example, during a company's resume review process, they may want to block name, address, and phone number to help reduce unconscious gender or other biases.
* **Replace personal information in source data for machine learning to reduce unfairness** – For example, if you want to remove names that might reveal gender when training a machine learning model, you could use the service to identify them and you could replace them with generic placeholders for model training.
* **Remove personal information from call center transcription** – For example, if you want to remove names or other PII data that happen between the agent and the customer in a call center scenario. You could use the service to identify and remove them.

## Considerations when choosing a use case

* **Avoid high-risk automatic redaction or information classification scenarios** – Any scenario where failures to redact personal information could expose people to the risk of identity theft and physical or psychological harms should include careful human oversight.
* **Avoid scenarios that use personal information for a purpose that consent was not obtained for** - For example, a company has resumes from past job applicants. The applicants didn't give their consent to be contacted for promotional events when they submitted their resumes. Based on this scenario, the PII service shouldn't be used to identify contact information for the purpose of inviting the past applicants to a trade show.
* **Avoid scenarios that use the service to harvest personal information from publicly available content**.
* **Avoid scenarios that replace personal information in text with the intent to mislead people**.
* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Characteristics and limitations

Depending on your scenario, input data and the entities you wish to extract, you could experience different levels of performance. The following sections are designed to help you understand key concepts about performance as they apply to using the Azure Language PII service.

### Understand and measure performance

Since both false positive and false negative errors can occur, it's important to understand how both types of errors might affect your overall system. In redaction scenarios, for example, false negatives could lead to personal information leakage. For redaction scenarios, consider a process for human review to account for this type of error. For sensitivity label scenarios, both false positives and false negatives could lead to misclassification of documents. The audience may unnecessarily limit documents labeled as confidential where a false positive occurred. PII could be leaked where a false negative occurred and a public label was applied.

You can adjust the threshold for confidence score your system uses to tune your system. If it's more important to identify all potential instances of PII, you can use a lower threshold. This means that you may get more false positives (non- PII data being recognized as PII entities), but fewer false negatives (PII entities not recognized as PII). If it is more important for your system to recognize only true PII data, you can use a higher threshold. Threshold values may not have consistent behavior across individual categories of PII entities. Therefore, it is critical that you test your system with real data it will process in production.

### System limitations and best practices for enhancing performance

* Make sure you understand all the [entity categories](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories) that can be recognized by the system. Depending on your scenario, your data may include other information that could be considered personal but isn't covered by the categories the service currently supports.
* Context is important for all entity categories to be correctly recognized by the system, as it often is for humans to recognize an entity. For example, without context, a ten-digit number is just a number, not a PII entity. However, given context like You can reach me at my office number 2345678901, both the system and a human can recognize the ten-digit number as a phone number. Always include context when sending text to the system to obtain the best possible performance.
* Person names in particular require linguistic context. Send as much context as possible for better person name detection.
* For conversational data, consider sending more than a single turn in the conversation to ensure higher likelihood that the required context is included with the actual entities.
  In the following conversation, if you send a single row at a time, the passport number doesn't have any context associated with it and the EU Passport Number PII category isn't recognized.
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

  Several different countries have the same format for passport numbers, so several different specific entity categories may be recognized. In some cases, using the highest confidence score may not be sufficient to choose the right entity class. If your scenario depends on the specific entity category being recognized, you may need to disambiguate the result elsewhere in your system either through a human review or additional validation code. Thorough testing on real life data can help you identify if you're likely to see multiple entity categories for recognized for your scenario.<br/><br/>
  Although many international entities are supported, currently the service only supports English text. Consider verifying the language the input text is in if you're not sure it's all in English.
* The PII service only takes text as an input. If you are redacting information from documents in other formats, make sure to carefully test your redaction code to ensure identified entities aren't accidentally leaked.

* The anonymization feature (2025-11-15-preview) substitutes personally identifiable information (PII) with randomly chosen values from a predefined list specific to each entity category. For example, a person's name is replaced with a name selected from a relevant preset list.

   * The preset list of names includes both gender-specific and gender-agnostic options, along with names from diverse cultural backgrounds. However, when a name is associated with a particular gender or cultural context, those associations are not preserved during replacement. As a result, this may cause unintended effects in scenarios where gender or cultural identifiers associated with name-based personal information are expected.
   * Using the  anonymization feature can also create confusion for the end users of the redacted text because, once PII values are replaced, end users may not realize that any PII values were redacted.

## See also

* [Transparency note for Azure Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for health feature](transparency-note-health.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Data Privacy and Security for  Azure Language](data-privacy.md)
* [Guidance for integration and responsible use with Azure Language](guidance-integration-responsible-use.md)