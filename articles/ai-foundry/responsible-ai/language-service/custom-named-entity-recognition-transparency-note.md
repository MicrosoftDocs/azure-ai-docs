---
title: Transparency note for custom NER
titleSuffix: Foundry Tools
description: Transparency note for custom named entity recognition
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 09/29/2021
---

# Use cases for custom named entity recognition

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *Transparency Notes* to help you understand how our AI technology works. This includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to custom named entity recognition

Custom named entity recognition (custom NER) is a cloud-based API service for information extraction. The service applies machine-learning intelligence so you can build custom models for information extraction tasks.

Custom NER can be used to extract information from .txt files. For example, a financial institution might want to build an automated notification system to remind clients of their payments due. The organization uses custom NER to extract relevant information from loan agreements, such as the client name, loan amount, interest rate, and payment date. The system can further process the extracted entities to send a reminder to the client with the next payment date and amount due.

### The basics of custom named entity recognition

Custom named entity recognition enables its users to build custom machine learning models to extract domain-specific entities from unstructured text, such as contracts or financial documents.

By creating a custom NER project, developers can iteratively tag entities within the data, train, evaluate, and improve model performance before making it available for consumption. The quality of the tagged data greatly affects model performance. To simplify building and customizing your model, the service offers a custom web portal that can be accessed through [Language Studio](https://aka.ms/languageStudio).

### Custom NER terminology

The following terms are commonly used with this feature:

|Term| Definition|
|:-----|:----|
|Project| A *project* is a work area for building your custom ML models based on your data. Your project can only be accessed by you and others who have access to the Azure resource being used. Within a project you can tag entities within the data, build models, evaluate and improve models where necessary, and eventually deploy a model. You can have multiple models within your project, all built on the same dataset.|
|Model | A *model* is an object that is trained to do a certain task, in this case custom entity recognition. Models are trained by providing tagged data to learn from so they can later be used for recognition tasks.|
| Entity | An *entity* is a span of text that indicates a certain type of information. The text span can consist of one or more words. In the scope of custom NER, entities represent the information that the user wants to extract from the text. Developers tag entities within their data with the needed entities before passing it to the model for training. For example "Invoice number", "Start date", "Shipment number", "Birthplace", "Origin city", "Supplier name" or "Client address". |

## Example use cases

Here are some examples of when you might use custom NER:

* **Knowledge mining to enhance semantic search:** Search is foundational to any app that surfaces text content to users. Common scenarios include catalog or document search, retail product search, or knowledge mining for data science. Many enterprises across various industries want to build a rich search experience over private, heterogeneous content, which includes both structured and unstructured documents. As a part of their pipeline, developers can use custom NER for extracting entities from the text that are relevant to their industry. These entities can be used to enrich the indexing of the file for a more customized search experience.

* **Information extraction from unstructured text:** Many financial and legal organizations extract and normalize data from thousands of complex, unstructured text sources on a daily basis. Such sources include bank statements, legal agreements, or bank forms. For example, mortgage application data extraction done manually by human reviewers may take several days to extract. Automating these steps simplifies the process and saves cost, time, and effort.

* **Audit and compliance:** Instead of manually reviewing significantly long text files to audit and apply policies, IT departments in financial or legal enterprises can use custom NER to build automated solutions. These solutions can be helpful to enforce compliance policies, and set up necessary business rules based on knowledge mining pipelines that process structured and unstructured content.

## Considerations when choosing a use case

Be aware of the following guidance when you use custom NER:

* **Avoid using custom NER for decisions that might have serious adverse impacts.** For example, avoid scenarios that include medical or health diagnosis based on extracted information from an individual’s medical history form, or charging a user’s bank account based on extracted values. Additionally, it's advisable to include human review of decisions that have the potential for serious impacts on individuals.

* **Avoid creating custom entities that extract unnecessary or sensitive information.** Avoid extracting sensitive user information if it's not required for your use case. For example, if your scenario requires extracting your user's city and country/region, create entities that extract only the city and country/region from a user's address instead of extracting the entire address

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Introduction to custom NER](/azure/ai-services/language-service/custom-named-entity-recognition/overview)

* [Characteristics and limitations for using custom NER](custom-named-entity-recognition-characteristics-and-limitations.md)

* [Data privacy and security](custom-named-entity-recognition-data-privacy-security.md)

* [Guidance for integration and responsible use](custom-named-entity-recognition-guidance-integration-responsible-use.md)

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
