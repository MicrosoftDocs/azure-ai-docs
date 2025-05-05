---
title: OCR - Optical Character Recognition
titleSuffix: Azure AI services
description: Learn how the optical character recognition (OCR) services extract print and handwritten text from images and documents in global languages.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: overview
ms.date: 10/16/2024
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.author: pafarley
ms.custom: devx-track-csharp
---

# OCR - Optical Character Recognition

> [!WARNING]
> This service, including the Azure AI Vision legacy [OCR API in v3.2](/rest/api/computervision/recognize-printed-text?view=rest-computervision-v3.2) and [RecognizeText API in v2.1](/rest/api/computervision/recognize-printed-text/recognize-printed-text?view=rest-computervision-v2.1), is not recommended for use.

[!INCLUDE [read-editions](includes/read-editions.md)]


OCR or Optical Character Recognition is also referred to as text recognition or text extraction. Machine-learning-based OCR techniques allow you to extract printed or handwritten text from images such as posters, street signs and product labels, as well as from documents like articles, reports, forms, and invoices. The text is typically extracted as words, text lines, and paragraphs or text blocks, enabling access to digital version of the scanned text. This eliminates or significantly reduces the need for manual data entry.



## OCR engine

Microsoft's **Read** OCR engine is composed of multiple advanced machine-learning based models supporting [global languages](./language-support.md). It can extract printed and handwritten text including mixed languages and writing styles. **Read** is available as cloud service and on-premises container for deployment flexibility. It's also available as a synchronous API for single, non-document, image-only scenarios with performance enhancements that make it easier to implement OCR-assisted user experiences.




## How is OCR related to Intelligent Document Processing (IDP)?

Intelligent Document Processing (IDP) uses OCR as its foundational technology to additionally extract structure, relationships, key-values, entities, and other document-centric insights with an advanced machine-learning based AI service like [Document Intelligence](../../ai-services/document-intelligence/overview.md). Document Intelligence includes a document-optimized version of **Read** as its OCR engine while delegating to other models for higher-end insights. If you are extracting text from scanned and digital documents, use [Document Intelligence Read OCR](../document-intelligence/prebuilt/read.md).

## How to use OCR

Try out OCR by using Vision Studio. Then follow one of the links to the Read edition that best meet your requirements.

> [!div class="nextstepaction"]
> [Try Vision Studio](https://portal.vision.cognitive.azure.com/)

:::image type="content" source="Images/vision-studio-ocr-demo.png" alt-text="Screenshot: Read OCR demo in Vision Studio.":::

## OCR supported languages

Both **Read** versions available today in Azure AI Vision support several languages for printed and handwritten text. OCR for printed text includes support for English, French, German, Italian, Portuguese, Spanish, Chinese, Japanese, Korean, Russian, Arabic, Hindi, and other international languages that use Latin, Cyrillic, Arabic, and Devanagari scripts. OCR for handwritten text includes support for English, Chinese Simplified, French, German, Italian, Japanese, Korean, Portuguese, and Spanish languages.

Refer to the full list of [OCR-supported languages](./language-support.md#optical-character-recognition-ocr).

## OCR common features

The Read OCR model is available in Azure AI Vision and Document Intelligence with common baseline capabilities while optimizing for respective scenarios. The following list summarizes the common features:

* Printed and handwritten text extraction in supported languages
* Pages, text lines and words with location and confidence scores
* Support for mixed languages, mixed mode (print and handwritten)
* Available as Distroless Docker container for on-premises deployment

## Use the OCR cloud APIs or deploy on-premises

The cloud APIs are the preferred option for most customers because of their ease of integration and fast productivity out of the box. Azure and the Azure AI Vision service handle scale, performance, data security, and compliance needs while you focus on meeting your customers' needs.

For on-premises deployment, the [Read Docker container](./computer-vision-how-to-install-containers.md) enables you to deploy the Azure AI Vision v3.2 generally available OCR capabilities in your own local environment. Containers are great for specific security and data governance requirements.


## Input requirements

The **Read** API takes images and documents as its input. The images and documents must meet the following requirements:

* Supported file formats are JPEG, PNG, BMP, PDF, and TIFF.
* For PDF and TIFF files, up to 2,000 pages (only the first two pages for the free tier) are processed.
* The file size of images must be less than 500 MB (4 MB for the free tier) with dimensions at least 50 x 50 pixels and at most 10,000 x 10,000 pixels. PDF files don't have a size limit.
* The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 image, which corresponds to about 8-point font text at 150 DPI.

>[!NOTE]
> You don't need to crop an image for text lines. Send the whole image to the Read API and it recognizes all texts.

## OCR data privacy and security

As with all of the Azure AI services, developers using the Azure AI Vision service should be aware of Microsoft's policies on customer data. See the [Azure AI services page](https://www.microsoft.com/trustcenter/cloudservices/cognitiveservices) on the Microsoft Trust Center to learn more.

## Next steps

- OCR for general (non-document) images: try the [Azure AI Vision 4.0 preview Image Analysis REST API quickstart](./concept-ocr.md).
- OCR for PDF, Office and HTML documents and document images: start with [Document Intelligence Read](../../ai-services/document-intelligence/concept-read.md).
- Looking for the previous GA version? Refer to the [Azure AI Vision 3.2 GA SDK or REST API quickstarts](./quickstarts-sdk/client-library.md).
