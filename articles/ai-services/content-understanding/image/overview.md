---
title: Azure AI Content Understanding image overview
titleSuffix: Azure AI services
description: Learn how to use Azure AI Content Understanding image solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.date: 04/14/2025
ms.custom: ignite-2024-understanding-release
---

# Content Understanding image solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding standardizes the extraction of data from images, making it easier to analyze large volumes of unstructured data. Standardized extraction speeds up time-to-value and simplifies integration into downstream analytical workflows. With the Content Understanding APIs, you can define schema to specify the fields, descriptions, and output types for extraction. The service then analyses the images and provides structured data, which can be applied in various use cases, such as:

* **Retrieval-augmented generation (RAG) applications:** Extract key details from your images to build a robust index that powers user-facing chat experiences. This index enables users to ask questions and receive accurate answers based on the content of your images.

* **Financial analysis and business intelligence:** Analyze business performance charts and trends to generate real-time reports that help analysts, managers, and executives make faster, more informed decisions.

* **Manufacturing quality control:** Automate the detection of defects and anomalies, such as scratches, cracks, or misalignments, in production lines and manufacturing environments.

* **Shelf analysis and inventory management:** Detect, count, and extract specific details about retail products, optimizing operations, and improving customer satisfaction by ensuring products are well-stocked and properly organized.

## Key Benefits

Content Understanding offers several key benefits for extracting information from images, including,

* **Enhanced data usability and structure:** By providing structured data, Content Understanding simplifies integration with databases, spreadsheets, and systems like Customer Relationship Management (CRM) or Enterprise Resource Planning (ERP) tools.

* **Improved accuracy for specific use cases:** Content Understanding enables targeted data extraction that aligns directly with your unique requirements, helping to improve model accuracy by focusing on the most important data points.

* **Faster and more cost-effective automation:**  The extracting of only the necessary fields enables Content Understanding to streamlines automation. Thus allowing organizations to scale their data processing workflows efficiently and reduce the storage and processing of irrelevant data.


## Input requirements
For detailed information on supported input file formats, refer to our [Service quotas and limits](../service-limits.md) page.

> [!NOTE]
> For best results, image schema should only be used to process non-document-based images.
> Text heavy images of documents should be processed using a document schema.
> Use cases that require extraction of text from document images or scanned documents should be processed using a document field extraction schema.

## Supported languages and regions
For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

## Supported field types/azure/ai-foundry/responsible-ai/
For detailed information on supported field types, refer to our [Service quotas and limits](../service-limits.md#field-type-limits) page.

## Data privacy and security

As with all the Azure AI services, developers using the Content Understanding service should be aware of Microsoft's policies on customer data. See our [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page to learn more.

> [!IMPORTANT]
> If you're using Microsoft products or services to process Biometric Data, you're responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate, and required under applicable Data Protection Requirements. "Biometric Data" has the meaning articulated in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and Privacy for Face](/legal/cognitive-services/face/data-privacy-security).

## Next steps

* Try processing your video content using Content Understanding in [Azure AI Foundry portal](https://aka.ms/cu-landing).
* Learn to analyze video content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: [**image, text, and table, content extraction**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python#samples).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
