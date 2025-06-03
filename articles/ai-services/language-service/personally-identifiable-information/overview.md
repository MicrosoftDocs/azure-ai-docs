---
title: What is the Personally Identifying Information (PII) detection feature in Azure AI Language?
titleSuffix: Azure AI services
description: An overview of the PII detection feature in Azure AI services, which helps you extract entities and sensitive information (PII) in text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 03/24/2025
ms.author: lajanuar
ms.custom: language-service-pii
---

# What is Azure AI Language Personally Identifiable Information (PII) detection?

Azure AI Language Personally Identifiable Information (PII) detection is a feature offered by [Azure AI Language](../overview.md). The PII detection service is a cloud-based API that utilizes machine learning and AI algorithms to help you develop intelligent applications with advanced natural language understanding. Azure AI Language PII detection uses Named Entity Recognition (NER) to **identify and redact** sensitive information from input data. The service classifies sensitive personal data into predefined categories. These categories include phone numbers, email addresses, and identification documents. This classification helps to efficiently detect and eliminate such information.

> [!TIP]
> Try PII detection [in Azure AI Foundry portal](https://ai.azure.com/explore/language). There you can [utilize a currently existing Language Studio resource or create a new Azure AI Foundry resource](../../../ai-services/connect-services-ai-foundry-portal.md).

## What's new

The Text PII and Conversational PII detection preview API (version `2024-11-15-preview`) now supports the option to mask detected sensitive entities with a label beyond just redaction characters. Customers can specify if personal data content such as names and phone numbers, that is, `"John Doe received a call from 424-878-9192"`, are masked with a redaction character, that is, `"******** received a call from ************"`, or masked with an entity label, that is, `"[PERSON_1] received a call from [PHONENUMBER_1]"`. More on how to specify the redaction policy style for your outputs can be found in our [how-to guides](how-to-call.md). 

The Conversational PII detection models (both version `2024-11-01-preview` and `GA`) are updated to provide enhanced AI quality and accuracy. The numeric identifier entity type now also includes Drivers License and Medicare Beneficiary Identifier.

As of June 2024, we now provide General Availability support for the Conversational PII service (English-language only). Customers can now redact transcripts, chats, and other text written in a conversational style (that is, text with `um`s, `ah`s, multiple speakers, and the spelling out of words for more clarity) with better confidence in AI quality, Azure `SLA` support and production environment support, and enterprise-grade security in mind.

## Capabilities

 Currently, PII support is available for the following capabilities:

* [General text PII detection](how-to/redact-text-pii.md) for processing sensitive information (PII) and health information (PHI) in unstructured text across several [predefined categories](concepts/entity-categories.md).
* [Conversation PII detection](how-to/redact-conversation-pii.md), a specialized model designed to handle speech transcriptions and the informal, conversational tone found in meeting and call transcripts. 
* [Native Document PII detection](how-to/redact-document-pii.md) for processing structured document files.


### [Text PII](#tab/text-pii)

Azure AI Language is a cloud-based service that applies Natural Language Processing (NLP) features to detect categories of personal information (PII) in text-based data. This documentation contains the following types:

* **[Quickstarts](quickstart.md)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](how-to/redact-text-pii.md)** contain instructions for using the service in more specific or customized ways.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]

### Key features for text PII

Azure AI Language offers named entity recognition to identify and categorize information within your text. The feature detects PII categories including names, organizations, addresses, phone numbers, financial account numbers or codes, and government identification numbers. A subset of this PII is protected health information (PHI). By specifying domain=phi in your request, only PHI entities are returned.

### [Conversation PII](#tab/conversation-pii)

The Azure AI Language conversation PII API processes audio conversations to detect and remove sensitive information (PII) based on a set of predefined categories. This documentation contains the following types:

* **[Quickstarts](quickstart.md)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](how-to/redact-conversation-pii.md)** contain instructions for using the service in more specific or customized ways.

### Key features for conversation PII

Conversation PII uses natural language processing techniques to identify and categorize information within conversations. This feature supports both natural chat transcripts and transcribed transcripts from phone calls. For a chat or call, there are different kinds of important information, scattered over long text or transcripts.

### [Native document PII](#tab/native-document-pii)

The native document support feature allows you to send API requests asynchronously. You can use an HTTP POST request body to transmit your data and an HTTP GET request query string to check the status of your requests. Your processed documents are stored in your designated Azure Blob Storage container. This documentation contains the following types:

* **[Quickstarts](quickstart.md)** are getting-started instructions to guide you through making requests to the service.
* **[How-to guides](how-to/redact-document-pii.md)** contain instructions for using the service in more specific or customized ways.

### Key features for native document PII

Document PII uses natural language processing techniques to identify and categorize information within documents.

---

## Get started with PII detection

[!INCLUDE [development options](./includes/development-options.md)]

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]

## Input requirements and service limits

### [Text PII](#tab/text-pii)

* Text PII takes text for analysis. For more information, see [Data and service limits](../concepts/data-limits.md) in the how-to guide.
* PII works with various written languages. For more information, see [language support](language-support.md?tabs=text-summarization). You can specify in which [supported languages](../concepts/language-support.md) your source text is written. If you don't specify a language, the extraction defaults to English. The API may return offsets in the response to support different [multilingual and emoji encodings](../concepts/multilingual-emoji-support.md). 

### [Conversation PII](#tab/conversation-pii)

* Conversation PII takes structured text for analysis. For more information, see [data and service limits](../concepts/data-limits.md).
* Conversation summarization works with various spoken languages. For more information, see [language support](language-support.md?tabs=conversation-summarization).
* [!INCLUDE [service limits article](../includes/service-limits-link.md)]

### [Native document PII](#tab/native-document-pii)

* Native document PII takes text for analysis. For more information, see [Data and service limits](../concepts/data-limits.md) in the how-to guide.
* Native document PII works with various written languages. For more information, see [language support](language-support.md?tabs=document-summarization).

A native document refers to the file format used to create the original document such as Microsoft Word (docx) or a portable document file (pdf). Native document support eliminates the need for text preprocessing before using Azure AI Language resource capabilities. Currently, native document support is available for the [**PiiEntityRecognition**](../personally-identifiable-information/concepts/entity-categories.md) capability.

 Currently **PII** supports the following native document formats:

|File type|File extension|Description|
|---------|--------------|-----------|
|Text| `.txt`|An unformatted text document.|
|Adobe PDF| `.pdf`       |A portable document file formatted document.|
|Microsoft Word|`.docx`|A Microsoft Word document file.|

---

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people affected by it, and the deployment environment. Read the [transparency note for PII](/legal/cognitive-services/language-service/transparency-note-personally-identifiable-information?context=/azure/ai-services/language-service/context/context) to learn about responsible AI use and deployment in your systems. For more information, see the following articles:

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Example scenarios

* **Apply sensitivity labels** - For example, based on the results from the PII service, a public sensitivity label might be applied to documents where no PII entities are detected. For documents where US addresses and phone numbers are recognized, a confidential label might be applied. A highly confidential label might be used for documents where bank routing numbers are recognized.
* **Redact some categories of personal information from documents that get wider circulation** - For example, if customer contact records are accessible to frontline support representatives, the company can redact the customer's personal information besides their name from the version of the customer history to preserve the customer's privacy.
* **Redact personal information in order to reduce unconscious bias** - For example, during a company's resume review process, they can block name, address, and phone number to help reduce unconscious gender or other biases.
* **Replace personal information in source data for machine learning to reduce unfairness** – For example, if you want to remove names that might reveal gender when training a machine learning model, you could use the service to identify them and you could replace them with generic placeholders for model training.
* **Remove personal information from call center transcription** – For example, if you want to remove names or other PII data that happen between the agent and the customer in a call center scenario. You could use the service to identify and remove them.
* **Data cleaning for data science** - PII can be used to make the data ready for data scientists and engineers to be able to use these data to train their machine learning models. Redacting the data to make sure that customer data isn't exposed.

## Next steps

There are two ways to get started using the entity linking feature:
* [Azure AI Foundry](../../../ai-foundry/what-is-azure-ai-foundry.md) is a web-based platform that lets you use several Language service features without needing to write code.
* The [quickstart article](quickstart.md) for instructions on making requests to the service using the REST API and client library SDK.
