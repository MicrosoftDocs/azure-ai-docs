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

# Azure AI Content Understanding document solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding offers sophisticated document analysis capabilities, enabling organizations to convert unstructured content into actionable and organized data. Utilizing [customizable analyzers](../concepts/prebuilt-analyzers.md), it can expertly extract essential information, fields, and relationships from a diverse range of documents and forms.

## Business use cases

Document analyzers can process complex documents in various formats and templates:

* **Contract lifecycle management**: Extract key fields, clauses, and obligations from various contract types.
* **Loan and mortgage applications**: Automate processing to enable quicker handling by banks, lenders, and government entities.
* **Financial services**: Analyze complex documents like financial reports and asset management reports.
* **Expense management**: Parse receipts and invoices from various retailers to validate expenses across different formats and templates.
* **Document sets and knolwedge base scenarios**: Extract key fields from document sets as a whole, and add reference data to handle tasks like validation and enrichment by applying multi-step reasoning.

## Document analyzer capabilities

:::image type="content" source="../media/document/document-capabilities.png" alt-text="Screenshot of document extraction flow.":::

### Content extraction

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
- RAG
  - **RAG solutions**: Content extraction forms the foundation of effective RAG systems by transforming raw multimodal data into structured, searchable formats optimized for retrieval. Learn more about building RAG solutions on our [retrieval-augmented generation](../concepts/retrieval-augmented-generation.md) page.

### Field extraction

Field extraction empowers you to extract, classify, and generate structured data from various documents and forms, customized to meet your unique requirements. The process of transforming unstructured content into organized, actionable information simplifies data management, improves searchability, and supports automated workflows. For instance, you can seamlessly extract customer details, billing addresses, and itemized charges from invoices, or identify contractual parties, renewal dates, and payment terms in legal agreements. To maximize efficiency, you can utilize prebuilt analyzer templates—such as ones tailored for invoices—or design bespoke analyzers from scratch, enhancing precision through the labeling of more sample documents.

Note that confidence and grounding is an opt-in feature. Please set `estimateFieldSourceAndConfidence` as `true` to opt in for confidence and grounding for field extraction.


#### Field extraction methods

Azure AI Content Understanding provides versatile methods for field extraction, enabling precise and tailored processing of document content:

- **Extract**: Extract specific data, like transaction dates from receipts or line items from invoices, for precise and focused information capture.

- **Classify**: Categorize document content into predefined categories, such as classifying sentiment in customer call transcript or classifying hotel receipt items. 

- **Generate**: Produce new insights or summaries from your documents, including document summaries, and chapter overviews enhancing content accessibility and comprehension.

## Key benefits

Content Understanding delivers powerful document analysis capabilities designed to address critical enterprise and business scenarios such as Retrieval-Augmented Generation (RAG) and Robotic Process Automation (RPA). Key benefits include:

- **Intelligent search enablement:** Transform unstructured documents into structured, searchable data assets, significantly improving information discoverability and accessibility across your organization.

- **Grounded data extraction:** Maintain clear traceability and localization of extracted data, facilitating efficient human-in-the-loop review processes and ensuring transparency and compliance.

- **Confidence-driven automation:** Utilize built-in confidence scoring to intelligently automate document processing tasks, optimizing resource allocation, reducing operational costs, and enhancing decision-making accuracy.

- **Flexible customization:** Easily adapt and tailor document analyzers to align with specific business processes and workflows, enabling precise extraction and classification tailored to your organization's unique requirements.

- **Enhanced accuracy and reliability:** Achieve precise extraction and classification of critical business data, significantly reducing errors and improving operational efficiency across automated workflows.

- **Agents-ready:** Process diverse inputs and deliver output in a standard format that’s ready for an agent’s workflow. Outputs can give your application an understanding of user intent, with data supported by a strongly typed schema that makes it easier to quickly get data in a format ready for your code.

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
