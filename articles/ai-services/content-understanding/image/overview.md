---
title: Azure Content Understanding in Foundry Tools image overview
titleSuffix: Foundry Tools
description: Learn how to use Azure Content Understanding in Foundry Tools image solutions
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - build-2025
---

# Azure Content Understanding in Foundry Tools image solutions


Azure Content Understanding standardizes the extraction of data from images, making it easier to analyze large volumes of unstructured image data. Standardized extraction speeds up time-to-value and simplifies integration into downstream analytical workflows. With the Content Understanding APIs, you can define schemas to specify the fields, descriptions, and output types for extraction. The service then analyzes your images and provides structured data that can be applied in various use cases, such as:

* **Retrieval-augmented generation (RAG) applications:** Extract key details from your images to build a robust index that powers user-facing chat experiences. This index enables users to ask questions and receive accurate answers based on the content of your images.

* **Financial analysis and business intelligence:** Analyze business performance charts and trends to generate real-time reports that help analysts, managers, and executives make faster, more informed decisions.

* **Manufacturing quality control:** Automate the detection of defects and anomalies, such as scratches, cracks, or misalignments, in production lines and manufacturing environments.

* **Shelf analysis and inventory management:** Detect, count, and extract specific details about retail products, optimizing operations, and improving customer satisfaction by ensuring products are well-stocked and properly organized.

## Key benefits

Content Understanding offers several key benefits for extracting information from images, including,

* **Enhanced data usability and structure:** By providing structured data, Content Understanding simplifies integration with databases, spreadsheets, and systems like Customer Relationship Management (CRM) or Enterprise Resource Planning (ERP) tools.

* **Improved accuracy for specific use cases:** Content Understanding enables targeted data extraction that aligns directly with your unique requirements, helping to improve model accuracy by focusing on the most important data points.

* **Faster and more cost-effective automation:**  The extracting of only the necessary fields enables Content Understanding to streamlines automation. Thus allowing organizations to scale their data processing workflows efficiently and reduce the storage and processing of irrelevant data.

:::image type="content" source="../media/image/image-flow-diagram.jpg" alt-text="Screenshot of a data flow diagram for image processing in content understanding.":::

## Face description fields

> [!NOTE]
>
>  This feature is limited access; customers need to request to disable face blur for Azure OpenAI models with an Azure support request. Learn more [Manage an Azure support request](/azure/azure-portal/supportability/how-to-manage-azure-support-request).

The field extraction capability can optionally be enhanced to provide detailed descriptions of faces in the images. This capability includes attributes such as facial hair, facial expression, and the presence of celebrities, which can be crucial for various analytical and indexing purposes. To enable face description capabilities set `disableFaceBlurring : true` in the analyzer configuration.

**Examples:**

* **Example field: facialHairDescription:** Describes the type of facial hair (for example, `beard`, `mustache`, `clean-shaven`)
* **Example field: nameOfProminentPerson:** Provides a name if possible of a celebrity in the image (for example, `Satya Nadella`)
* **Example field: faceSmilingFrowning:** Provides a description of whether a person is smiling or frowning

## Get started

Get started with processing images with Content Understanding by following our [REST API quickstart](../quickstart/use-rest-api.md?tabs=image) or visiting [Microsoft Foundry](https://aka.ms/cu-landing) for a no-code experience. 

> [!NOTE]
> Image analyzers are not optimized for scenarios where analysis is based primarily on extracted text. If your main goal is to extract and analyze text from images, consider using a document field extraction schema instead.


> [!IMPORTANT]
> If you're using Microsoft products or services to process Biometric Data, you're responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate, and required under applicable Data Protection Requirements. <!--"Biometric Data" has the meaning articulated in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements.--> For related information, see [Data and Privacy for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security).

## Related content

* For guidance on optimizing your Content Understanding implementations, including schema design tips, see our detailed [Best practices guide](../concepts/best-practices.md).
* For detailed information on supported input image formats, *see* [Service quotas and limits](../service-limits.md).
* To review code samples, *see* [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* For more information on trust and security, *see* [Data, protection, and privacy policy](https://www.microsoft.com/trust-center/privacy).
