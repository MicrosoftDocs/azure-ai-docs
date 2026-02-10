---
title: Transparency Note for Optical Character Recognition (OCR) - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Transparency note for optical character recognition (OCR) of images and documents with printed and handwritten text using the Azure Vision in Foundry Tools API.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 10/15/2025
---

# Transparency note and use cases for optical character recognition

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article provides information about use cases for optical character recognition (OCR).

## What is a transparency note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *transparency notes* to help you understand how our AI technology works. This includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use transparency notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft's AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to optical character recognition (OCR)

Businesses today frequently need to convert text from images, scanned paper documents, and digital files into actionable insights. These insights power knowledge mining, business process automation, and accessibility of content for everyone. Optical character recognition (OCR) is an AI service used to extract text from visual content such as images and documents. OCR currently supports several languages for extraction of print text ([see OCR supported languages](/azure/ai-services/computer-vision/language-support#optical-character-recognition-ocr)). Handwritten OCR is currently supported exclusively for English.

### The basics of OCR

The [OCR technology](/azure/ai-services/computer-vision/overview-ocr) from Microsoft is offered via the Azure Vision in Foundry Tools Read API. Customers call the Read API with their content to get the extracted text, its location, and other insights in machine readable text output. They process the output within their business applications to implement content intelligence, business process automation, and other scenarios for their users.

| Term | Definition |
|:-----|:----|
| Asynchronous | Asynchronous means that the service doesn't immediately return the extracted text. Instead, the process starts in the background. The customer application will need to check back at a later time to obtain the extracted text. |
| Read | The Read operation is an asynchronous call that accepts images and documents to begin analysis and text extraction, which is returned via another call. |
| Get Read Results | While the analysis and extraction process is active, the Get Read Results operation outputs the progress status. When the process is complete, the Get Read Results operation outputs the extracted text (in the form of text lines and words) and confidence values. |
| Confidence value | The Get Read Results operation returns confidence values in the range between 0 and 1 for all extracted words. This value represents the service's estimate of how many times it correctly extracts the word out of 100. For example, a word that's estimated to be extracted correctly 82% of the time will result in a confidence value of 0.82.|

## Example use cases

The following use cases are popular examples for the OCR technology.

- **Images and documents search and archive**: Unstructured documents such as legal contracts, technical documents, and news content contain rich information and metadata that are not available for processes such as automated tagging, categorization, and search. OCR allows the text from these documents to be machine readable for analysis, search, and retrieval.
- **Image content moderation and localization**: eCommerce companies, user-generated content publishers, and online gaming and social media communities need to moderate images to be compliant with online safety regulations. In certain cases, they also need to localize content for international audiences. OCR allows you to extract text from images to apply downstream processing.
- **Business process automation**: Business process automation requires integrating user-entered data and preferences in documents and application screens with complex business processes. OCR unlocks the text embedded in documents and images and makes it available for use in the steps of the business workflows.
- **Financial and healthcare documents processing**: When used in back office processing of financial and insurance application forms, OCR helps save time and effort in document processing. Similarly, OCR applied to medical claim reimbursements and medical information forms speeds up reimbursements and qualification for services and benefits.

## Considerations when choosing other use cases

Consider the following factors when you choose a use case.

- **Carefully consider when using for awarding or denying of benefits**: Using OCR output directly for awarding or denying benefits can result in errors if based on incorrect or incomplete information. For example, when filling out medical forms, users can make errors or fail to include important information. Additionally, OCR can potentially misread or not detect parts of the form. To ensure fair and high-quality decisions for consumers, combine OCR-based automation with human oversight.
- **Avoid use for signature identification**: When you extract handwritten text, avoid using the OCR results on signatures to identify individuals. Signatures are hard to read for humans and machines alike. A better way to use OCR is to use it for detecting the presence of a signature for further analysis.
- **Don’t use OCR for decisions that may have serious adverse impacts**: Examples of such use cases include processing medical prescriptions and dispensing medication. The machine learning models that extract text from prescriptions can result in undetected or incorrect text output. Decisions based on incorrect output could have serious adverse impacts. Additionally, it is advisable to include human review of decisions that have the potential for serious impacts on individuals.

- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]
