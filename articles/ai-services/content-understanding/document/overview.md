---
title: Azure AI Content Understanding document overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding document solutions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
---

# Content Understanding document solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding delivers advanced document analysis capabilities that empower organizations to transform unstructured content into actionable, structured data.
By leveraging [customizable analyzers](../concepts/prebuilt-analyzers.md), Content Understanding can intelligently extract key information, fields, and relationships from a wide variety of documents and forms.

## Business use cases

Document analyzers can process complex documents in various formats and templates:

* **Contract lifecycle management**: Extract key fields, clauses, and obligations from various contract types.
* **Loan and mortgage applications**: Automate processing to enable quicker handling by banks, lenders, and government entities.
* **Financial services**: Analyze complex documents like financial reports and asset management reports.
* **Expense management**: Parse receipts and invoices from various retailers to validate expenses across different formats and templates.

## Document analyzer capabilities

:::image type="content" source="../media/document/document-capabilities.png" alt-text="Screenshot of document extraction flow.":::

### Content Extraction

Content extraction forms the foundation of Azure AI Content Understanding's document analysis capabilities, transforming unstructured documents into structured, machine-readable data.
It precisely captures both printed and handwritten text while preserving the document's structure through advanced layout analysis.

- Content Analysis
  - **Text**: Processes multilingual content, including both machine-printed and handwritten text from hundreds of languages.
  - **Selection marks**: Identifies and extracts selection indicators such as checkboxes, radio buttons, and similar markers.
  - **Barcode detection**: Scans and decodes information from over a dozen types of linear and two-dimensional barcodes.
  - **Mathematical formulas**: Captures and preserves complex mathematical expressions in LaTeX format.
  - **Image elements**: Locates and extracts images, diagrams, and charts along with their related captions and annotations.
- Structure Analysis
  - **Paragraphs**: Detects and categorizes text segments based on their document context and role.
  - **Tabular data**: Recognizes and extracts table structures, including complex formats with spanning cells and multi-page layouts.
  - **Hierarchical sections**: Maps content organization through section headers and nested content relationships.

### Field extraction

Field extraction enables the extraction, classification, and generation of structured data from various forms and documents tailored to your specific needs. By converting unstructured document content into structured, actionable information, field extraction streamlines data organization, enhances searchability, and facilitates automated processing workflows. For example, you can efficiently extract customer details, billing addresses, and itemized charges from invoices, or identify contractual parties, renewal dates, and payment terms from legal agreements. To achieve optimal results, you can leverage prebuilt analyzer templates—such as those designed for invoices—or create customized analyzers from scratch, further refining accuracy by labeling additional sample documents.

### Field extraction methods

Azure AI Content Understanding provides versatile methods for field extraction, enabling precise and tailored processing of document content:

- **Extract**: Define and retrieve specific data fields from your documents, such as transaction dates from receipts or detailed line items from invoices, ensuring targeted and accurate data capture.

- **Classify**: Categorize document content into predefined categories, such as classifying sentiment in customer call transcript or classifying hotel receipt items. 

- **Generate**: Produce new insights or summaries from your documents, including document summaries, chapter overviews enhancing content accessibility and comprehension.

## Key benefits

Content Understanding delivers powerful document analysis capabilities designed to address critical enterprise and business scenarios such as Retrieval-Augmented Generation (RAG) and Robotic Process Automation (RPA). Key benefits include:

- **Intelligent search enablement:** Transform unstructured documents into structured, searchable data assets, significantly improving information discoverability and accessibility across your organization.

- **Grounded data extraction:** Maintain clear traceability and localization of extracted data, facilitating efficient human-in-the-loop review processes and ensuring transparency and compliance.

- **Confidence-driven automation:** Leverage built-in confidence scoring to intelligently automate document processing tasks, optimizing resource allocation, reducing operational costs, and enhancing decision-making accuracy.

- **Flexible customization:** Easily adapt and tailor document analyzers to align with specific business processes and workflows, enabling precise extraction and classification tailored to your organization's unique requirements.

- **Enhanced accuracy and reliability:** Achieve precise extraction and classification of critical business data, significantly reducing errors and improving operational efficiency across automated workflows.

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
