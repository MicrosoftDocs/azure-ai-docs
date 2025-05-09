---
title: Azure AI Content Understanding document overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding document solutions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/01/2025
ms.custom: ignite-2024-understanding-release
---

# Content Understanding document solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Content Understanding is a cloud-based [Azure AI Service](../../what-are-ai-services.md) designed to efficiently extract content and structured fields from documents and forms. It provides a comprehensive suite of APIs and an intuitive UX experience for optimal efficiency.

Content Understanding enables organization to streamline data collection and processing, enhance operational efficiency, optimize data-driven decision making, and empower innovation. With customizable analyzers, Content Understanding allows for easy extraction of content or fields from documents and forms, tailored to specific business needs.

## April updates

* **Invoice prebuilt template**: Extract predefined schemas from various invoice formats. The out-of-the-box schema can be customized by adding or removing fields to suit your specific needs.

* **Generative and classify methods**: Added support for both generative and classification-based methods, enabling you to create generative fields such as summaries or categorize document details into multiple classes using the classify method.

## Business use cases

Document analyzers can process complex documents in various formats and templates:

* **Contract lifecycle management**: Extract key fields, clauses, and obligations from various contract types.
* **Loan and mortgage applications**: Automate processing to enable quicker handling by banks, lenders, and government entities.
* **Financial services**: Analyze complex documents like financial reports and asset management reports.
* **Expense management**: Parse receipts and invoices from various retailers to validate expenses across different formats and templates.


## Document analyzer capabilities

:::image type="content" source="../media/document/extraction-overview.png" alt-text="Screenshot of document extraction flow.":::

Content extraction enables the extraction of both printed and handwritten text from forms and documents, delivering business-ready content that is immediately actionable, usable, or adaptable for further development within your organization.

### Add-on capabilities

Enhance your document extraction with optional add-on features, which can incur added costs. These features can be enabled or disabled based on your needs. Currently supported add-ons include:

* **Layout**: Extracts layout information such as paragraphs, sections, tables, and more.
* **Barcode**: Identifies and decodes all barcodes in the documents.
* **Formula**: Recognizes all identified mathematical equations from the documents.


### Field extraction

Field extraction enables the extraction of structured data from various forms and documents tailored to your specific needs. For instance, you can extract customer names, billing addresses, and line items from invoices; or parties, renewal date, and payment clause from contracts. You can start field extraction right after defining the schema or enhance it by labeling more sample documents to improve extraction quality.

## Key Benefits

* **Accuracy and reliability:** Ensure precise data extraction, reducing errors and boosting efficiency.
* **Scalability:** Seamlessly scale out document processing to meet business demands.
* **Customizable:** Adapt document analyzer to fit specific workflows.
* **Grounding source:** Localize extracted data for human review workflows.
* **Confidence scores:** Enhance automation with estimated confidence scores to maximize efficiency and minimize costs.

## Input requirements
For detailed information on supported input document formats, refer to our [Service quotas and limits](../service-limits.md) page.

## Supported languages and regions
For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

## Data privacy and security
Developers using Content Understanding should review Microsoft's policies on customer data. For more information, visit our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) page.

## Next step
* Try processing your document content using Content Understanding in [Azure AI Foundry](https://aka.ms/cu-landing).
* Learn to analyze document content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: [**visual document search**](https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python/blob/main/notebooks/search_with_visual_document.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
