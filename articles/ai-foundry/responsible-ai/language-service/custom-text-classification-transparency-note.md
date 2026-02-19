---
title: Use cases for custom text classification
titleSuffix: Foundry Tools
description: Learn about use cases for custom text classification.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 04/26/2023
---

# Use cases for custom text classification

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI Principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to custom text classification

[Custom text classification](/azure/ai-services/language-service/custom-text-classification/overview) is a cloud-based API service that applies machine-learning intelligence to enable you to build custom models for text classification tasks.

Custom text classification supports two types of projects:

- **Single label classification**: You assign only one label for each file in your dataset. For example, if a file is a movie script, it could only be classified as "Action," "Thriller," or "Romance."
- **Multiple label classification**: You assign multiple labels for each file in your dataset. For example, if a file is a movie script, it could be classified as "Action" or "Action" and "Thriller."

### The basics of custom text classification

Custom text classification is offered as part of the custom features within Azure Language in Foundry Tools. This feature enables its users to build custom AI models to classify text into custom categories predefined by the user. By creating a custom text classification project, developers can iteratively tag data and train, evaluate, and improve model performance before they make it available for consumption. The quality of the tagged data greatly affects model performance.

To simplify building and customizing your model, the service offers a custom web portal that can be accessed through the [Language Studio](https://aka.ms/languageStudio). You can easily get started with the service by following the steps in this [quickstart](/azure/ai-services/language-service/custom-text-classification/quickstart).

### Custom text classification terminology

The following terms are commonly used within custom text classification:


|Term| Definition|
|:-----|:----|
|Project| A project is a work area for building your custom AI models based on your data. Your project can only be accessed by you and others who have contributor access to the Azure resource being used. Within a project, you can tag data, build models, evaluate and improve them where necessary, and eventually deploy a model to be ready for consumption. You can build multiple models within your project on the same dataset.|
|Model | A model is an object that's trained to do a certain task. For this system, the models classify text. Models are trained by learning from tagged data.|
| Class | A class is a user-defined category that indicates the overall classification of the text. Developers tag their data with their assigned classes before they pass it to the model for training.|

## Example use cases for custom text classification

Custom text classification can be used in multiple scenarios across a variety of industries. Some examples are:

* **Automatic emails or ticket triaging:** Support centers of all types receive a high volume of emails or tickets containing unstructured, freeform text and attachments. Timely review, acknowledgment, and routing to subject matter experts within internal teams is critical. Email triage at this scale requires people to review and route to the right departments, which takes time and resources. Custom text classification can be used to analyze incoming text, and triage and categorize the content to be automatically routed to the relevant departments for further action.

* **Knowledge mining to enhance and enrich semantic search:** Search is foundational to any app that surfaces text content to users. Common scenarios include catalog or document searches, retail product searches, or knowledge mining for data science. Many enterprises across various industries are seeking to build a rich search experience over private, heterogeneous content, which includes both structured and unstructured documents. As a part of their pipeline, developers can use custom text classification to categorize their text into classes that are relevant to their industry. The predicted classes can be used to enrich the indexing of the file for a more customized search experience.

## Considerations when you choose a use case

* **Avoid using custom text classification for decisions that might have serious adverse impacts.** Include human review of decisions that have the potential for serious impacts on individuals. For example, identifying whether to accept or reject an insurance claim based on a user's description of an incident.

* **Avoid creating classes that are ambiguous and not representative.** When you design your schema, avoid classes that are so similar to each other that there might be difficulty differentiating them from each other. For example, if you're classifying movie scripts, avoid creating a class for romance, comedy, and rom-com. Instead, consider using a multiple-label classification model with romance and comedy classes. Then, for rom-com movies, assign both classes.

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Introduction to custom text classification](/azure/ai-services/language-service/custom-text-classification/overview)
* [Characteristics and limitations for using custom text classification](custom-text-classification-characteristics-and-limitations.md)
* [Data privacy and security](custom-text-classification-data-privacy-security.md)
* [Guidance for integration and responsible use](custom-text-classification-guidance-integration-responsible-use.md)
* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
