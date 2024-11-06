---
title: Azure AI Content Understanding image overview
titleSuffix: Azure AI services
description: Learn how to use Azure AI Content Understanding image solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# Content Understanding image solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI's Content Understanding service enables you to extract structured data from unstructured image input stores. You provide a custom field extraction schema, including the fields, field descriptions, and desired field output types. The Content Understanding service converts your image data into structured information that can be used in downstream processes, such as:

* **Retrieval-augmented generation (RAG) applications**. Extract key information from your images to create a powerful index that fuels user-facing chat experiences. The index enables users to ask questions and receive accurate answers based on the contents of your images.

**Financial analysis and business intelligence**. Analyze business performance charts and trends to generate real-time reports that empower analysts, managers, and executives to make faster, more informed decisions.

**manufacturing quality control**. Automate the identification and detection of defects and anomalies, such as scratches, cracks, or misalignments, in production lines and manufacturing environments.

**Shelf analysis and inventory management**. Recognize, detect, count, and extract specific information about retail products, optimizing business operations and, enhancing customer satisfaction by ensuring products are available and well-organized.

## Key Benefits

With its field-value approach, Content Understanding offers distinct advantages for extracting information from your image data, including:

* **Increased data usability and structure**. Content Understanding provides structured data, making it easy to integrate into databases, spreadsheets, and Customer Relationship Management (`CRM`) or Enterprise Resource Planning (`ERP`) systems.

* **Improved accuracy for specific use cases**. Content Understanding offers targeted extraction that aligns directly with your current use case and produces  improving model accuracy for the most important data points.

**Faster and More Cost-Effective Automation**. Content Understanding enables faster automation by extracting only necessary fields, allowing organizations to scale data processing workflows efficiently and minimize storage and processing of irrelevant data.

## Supported file formats

> [!NOTE]
> For best results, image schema should only be used to process non-document-based images.
> Text heavy images of documents should be processed using a document schema.
> Use cases that require extraction of text from document images or scanned documents in image formats should be processed using a document field extraction schema.

Content Understanding supports the following image file formats in preview:

|Supported file types| File size| Resolution (pixels)|
|---|---|---|
.jpg, .png, .bmp, .heif|≤ 20 MB | Minimum: 50 x 50 px</be>Maximum: 10,000 x 10,000 px|

## Supported field types

| Data type|Supported format|Schema limits|Example|
| --- | --- |---|
| **String**| √ Plain Text||
|**Date** | √ Normalized to ISO 8601 (YYYY-MM-DD) format|2023-10-31|
| **Time**| √ Normalized to ISO 8601 (hh:mm:ss) format|14:30:00|
| **number**| √ Float number normalized to double precision floating point|3.14159|
| **Integer**| √ Integer number, normalized to 64-bit signed integer|42, 1024|
| **Boolean**| √ Boolean value, normalized to `true` or `false`||
| **array**| √ List of subfields of the same type||
| **Object**| √ Named list of subfields of potentially different types. ||

## Data privacy and security

As with all the Azure AI services, developers using the Content Understanding service should be aware of Microsoft's policies on customer data. See our [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page to learn more.

> [!IMPORTANT]
> If you are using Microsoft products or services to process Biometric Data, you are responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate and required under applicable Data Protection Requirements. "Biometric Data" will have the meaning set forth in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and Privacy for Face](/legal/cognitive-services/face/data-privacy-security).

## Next steps

Try processing your content and data using Content Understanding in the [Azure AI Studio](https://ai.azure.com/?tid=888d76fa-54b2-4ced-8ee5-aac1585adee7).