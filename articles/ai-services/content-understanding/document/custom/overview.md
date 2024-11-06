---
title: Azure AI Content Understanding custom document extraction overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding document solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 11/19/2024
---

# Content Understanding Document Solutions Overview (Preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).


Content Understanding is a cloud-based [Azure AI service](articles/ai-services/what-are-ai-services.md) that provides a comprehensive set of APIs and a user-friendly studio experience to facilitate efficient extraction of content, structure (such as tables, paragraphs, sections, and figures), and specific fields from any document or form. This service enables organizations to build intelligent document processing solutions and effectively manage large volumes of data across diverse formats stored in forms and documents.
By leveraging Content Understanding, organizations can streamline data collection and processing, driving operational efficiency, data-driven decision-making, and innovation. With customizable APIs, Content Understanding allows for easy extraction of fields or content from documents and forms, adaptable to specific business needs.


## Common use cases

Document Extraction can process complex documents with various formats, templates, and unstructured data:

* **Contract Lifecycle Management**. Leverage document field extraction model to extract key fields, clauses, and obligations from a wide array of contract types.
  
* **Loan and Mortgage Applications**. Automation of loan and mortgage application process enables banks, lenders, and government entities to process loan and mortgage applications quicker.

* **Financial Services**. Analyze complex documents like financial reports and asset management reports, with the new document field extraction model.

* **Expense management**. Receipts and invoices from various retailers and businesses need to be parsed to validate the expenses. Document field extraction can extract expenses across different formats and documents with varying templates.


:::image type="content" source="../media/document-extraction-overview.jpg" alt-text="Screenshot of document extraction flow.":::


## Document Extraction Capabilities 

Content extraction enables the extraction of both printed and handwritten text from forms and documents, delivering business-ready content that is immediately actionable, usable, or adaptable for further development within your organization.

### Add-on capabilities 

Use the add-on features to extend the results to include more features extracted from your documents. Some add-on features incur extra costs. These optional features can be enabled and disabled depending on the scenario of the document extraction. To enable a feature, add the associated feature name to the features query string property. You can enable more than one add-on feature on a request by providing a comma-separated list of features. 

* Layout: Extract layout information like Paragraphs, Sections, Tables and more along with text with ‘enableLayout’ add-on capability.
  
* Barcode: The "enableBarcode" capability extracts all identified barcodes in the documents.
  
* Formula: The ‘enableFormula’ capability extracts all identified formulas, such as mathematical equations from the documents.
  
* Locales: Enabling the ‘languages’ feature predicts the detected primary language for each text line along with the confidence score.
  
### Field Extraction

Document field extraction allows you to extract distinct data from forms and documents, with a wide variety of visual templates, specific to your use case. For example, you can extract customer name, billing address, due date, and amount due, line items, and other key data from an invoice or extract termination date, agreement date, lease terms and other key data from a contract using document field extraction.

You can train field extraction model with a single document or can add additional sample documents with labelling to improve the field extraction for your document type. 

Note: The layout add-on capability must be enabled by default for Field extraction 


## Benefits of Content Understanding Document Extraction

* **Accuracy and Reliability:** Document extraction AI models are built to deliver accurate data extraction, reducing errors and improving efficiency.
  
* **Scalability:** Easily scale your document processing capabilities to meet the growing demands of your business.
  
* **Customizability:** Tailor document extraction models to your specific requirements, ensuring the perfect fit for your unique workflows.
  
*	**Grounded results:** Localize the data extracted in the documents, ensuring the response is generated from the content, to enable human review workflows.
  
* **Confidence scores:** Maximize efficiency and minimize costs in automation workflows, leveraging confidence scores.

## Input Requirements 

For a complete list of Content Understanding supported input formats, see our [Service quotas and limits](https://review.learn.microsoft.com/en-us/azure/ai-services/content-understanding/service-limits) page. 

## Supported languages and regions 

For a complete list of supported languages and regions, see our [Language and region support](https://review.learn.microsoft.com/en-us/azure/ai-services/content-understanding/language-region-support) page.

## Next Step

Get started using Content Understanding APIs with our [QuickStart: Content Understanding REST APIs](https://review.learn.microsoft.com/en-us/azure/ai-services/content-understanding/quickstart/rest-api) and learn how to add additional samples with labels to improve field extraction quality (link).




