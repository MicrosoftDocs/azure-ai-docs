---
title: Azure Content Understanding in Foundry Tools prebuilt analyzers
titleSuffix: Foundry Tools
description: Learn about prebuilt analyzers, base analyzers, RAG analyzers, vertical analyzers, and how to use and customize them in Azure Content Understanding in Foundry Tools.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Prebuilt analyzers in Azure Content Understanding in Foundry Tools

Azure Content Understanding prebuilt analyzers provide a set of domain-specific extraction capabilities that go beyond predefined schemas. They're powered by knowledge bases of real-world document examples. They understand how information is structured and used, adapting to the nuances of each content type.

Prebuilt analyzers are ready-to-use tools that streamline common content processing tasks. You can use them for content ingestion in search and retrieval-augmented generation (RAG) workflows. You can also use them for intelligent document processing (IDP) to extract data from invoices or analyze call center recordings. These analyzers can also be used in agentic flows as tools for extracting structured representations from input files. You can also [customize these analyzers](../tutorial/create-custom-analyzer.md) to extract other fields or refine outputs to better fit your specific workflow requirements.

## Analyzer types

Content Understanding provides several categories of analyzers to support different scenarios:

- **[Content extraction analyzers](#content-extraction-analyzers)** - Focus on OCR and layout analysis with progressively richer extraction capabilities for basic text extraction, layout analysis, and barcode detection.
- **[Base analyzers](#base-analyzers)** - Fundamental content processing capabilities for each modality, used as parent analyzers when creating custom analyzers for document, image, audio, and video content.
- **[RAG analyzers](#retrieval-augmented-generation-rag-analyzers)** - Optimized for retrieval-augmented generation scenarios with semantic analysis and markdown extraction for document ingestion, search applications, and knowledge bases.
- **[Domain-specific analyzers](#domain-specific-analyzer-reference)** - Preconfigured analyzers for common document categories with specialized field extraction for invoice processing, tax forms, ID verification, mortgage documents, and contracts.
- **[Utility analyzers](#utility-analyzers)** - Specialized tools for schema generation and field extraction to discover document structure and extract key-value pairs.

### Content extraction analyzers

Content extraction analyzers focus on optical character recognition and layout analysis. These analyzers are built on top of `prebuilt-document` and provide progressively richer extraction capabilities.

#### `prebuilt-read`

* Extracts content elements such as words, paragraphs, formulas, and barcodes from documents.
* Provides basic optical character recognition (OCR) capabilities.
* Provides foundational text extraction without layout analysis.

This prebuilt doesn't require a language model or embedding model.

#### `prebuilt-layout`

* Extracts content and layout elements such as words, figures, paragraphs, and tables from documents.
* Identifies document structure, including sections and formatting.
* Extracts hyperlinks embedded within documents.
* Captures annotations such as highlights, underlines, and strikethroughs in digital PDFs.
* Provides detailed layout information beyond basic text extraction.
* Detects figure types including charts, diagrams, pictures, icons, and other images, providing location information (PDF files only).

This prebuilt doesn't require a language model or embedding model.

### Base analyzers

Base analyzers provide fundamental content processing capabilities specific to a content type. Use them primarily as a parent to inherit from when [creating custom analyzers](../tutorial/create-custom-analyzer.md). When you create a custom analyzer, include one of these base analyzers by using the `baseAnalyzerId` property. 

* `prebuilt-audio` - Base audio processing
* `prebuilt-document` - Base document processing
* `prebuilt-image` - Base image processing
* `prebuilt-video` - Base video processing

> [!NOTE]
> Currently, you can only derive custom analyzers from this set of four base analyzers.

### Retrieval-augmented generation (RAG) analyzers

Content Understanding provides a set of analyzers optimized for retrieval-augmented generation (RAG) scenarios. These analyzers extract content with layout as markdown and perform semantic analysis to enhance retrieval quality for downstream applications.

#### `prebuilt-documentSearch`

* Extracts various content and layout elements such as paragraphs, tables, and figures from documents.
* Provides detailed figure descriptions with textual explanations of images, charts, and diagrams<sup>1</sup>.
* Analyzes charts and diagrams, providing structured output as chart.js syntax for charts or mermaid.js syntax for diagrams<sup>1</sup>.
* Captures hand-written annotations and markup on the document.
* Generates a one-paragraph summary of the entire document content.
* Supports a [wide range of file formats](/azure/ai-services/content-understanding/service-limits#input-file-limits) including PDF, images, Office documents, and text files.
* Recommended for document ingestion in RAG workflows.

<sup>1</sup> Figure analysis is only supported for PDF and image file formats.

#### `prebuilt-imageSearch`

* Analyzes images to generate descriptions and insights.
* Generates a one-paragraph description of the image content.
* Extracts visual content for search and retrieval applications.

#### `prebuilt-audioSearch`

* Transcribes conversations from audio and video files.
* Generates a one-paragraph summary of the conversation content.
* Supports multiple locales for international content processing.
* Optimized for conversation analysis and content extraction.

#### `prebuilt-videoSearch`

* Analyzes videos to extract transcripts and descriptions for each segment.
* Automatically segments videos into meaningful sections based on topic shifts, scene changes, or visual cues.
* Generates detailed summaries focusing on people, places, and actions for each segment.
* Supports scene splitting and comprehensive video content analysis.
* Provides transcript extraction along with contextual segment descriptions.

### Domain-specific analyzers

Domain-specific analyzers are preconfigured for common document categories in popular industries. These analyzers provide specialized field extraction for specific document types and formats, powered by rich knowledge bases of real-world examples. 

Key categories include:

* **Finance and tax**: Extract structured data from invoices, receipts, bank statements, credit card statements, and comprehensive US tax forms including 1040, W-2, 1099 variants, and 1098 series. Tuned schemas capture amounts, dates, tax identifiers, and financial entities. See the [financial documents](#financial-documents) and [tax documents](#tax-documents-us) sections.
* **Identity verification**: Process passports, driver's licenses, ID cards, health insurance cards, and identity documents from multiple countries and regions with `prebuilt-idDocument` and related analyzers. Extract personal information, document numbers, and verification details with support for worldwide formats. See the [identity documents](#identity-documents) section.
* **Mortgage and lending**: Automate extraction from US mortgage applications (Form 1003), appraisal reports (Form 1004), verification of employment (Form 1005), and closing disclosures. Capture borrower details, property information, loan terms, and financial disclosures. See the [mortgage documents](#mortgage-documents-us) section.
* **Procurement and contracts**: Process purchase orders, contracts, procurement documents, and credit memos to extract vendor information, line items, pricing, terms, and contractual obligations. See the [procurement documents](#procurement-documents) and [legal and business documents](#legal-and-business-documents) sections.
* **Utilities and billing**: Extract structured data from utility bills, invoices, and billing statements across industries, capturing account information, usage details, and payment data. See the [financial documents](#financial-documents) and [other specialized analyzers](#other-specialized-analyzers) sections.

See the [complete list of domain-specific analyzers](#domain-specific-analyzer-reference) at the end of this article.

### Utility analyzers

Utility analyzers provide specialized functionality for schema generation and field extraction.

#### `prebuilt-documentFieldSchema`

* Analyzes documents to propose an appropriate field schema
* Useful for discovering structure in new document types

#### `prebuilt-documentFields`

* Extracts key-value pairs from documents
* Used internally by domain-specific analyzers when the input doesn't match any of the predefined schemas (for example, `prebuilt-idDocument`)

## Use prebuilt analyzers

To analyze content by using a prebuilt analyzer, make a POST request to the analyze endpoint:

```http
POST /analyzers/prebuilt-idDocument:analyze
```

Replace `prebuilt-idDocument` with the analyzer ID that matches your scenario.

## Customize prebuilt analyzers

Use any prebuilt analyzer as a template for creating a custom analyzer that better fits your specific needs.

### Get an analyzer definition

To retrieve the configuration and schema of a prebuilt analyzer:

```http
GET /analyzers/prebuilt-idDocument
```

The response returns a JSON definition with the field schema and configuration options. You can edit this definition and create your own analyzer based on it.

### Create a custom analyzer from a template

After retrieving and modifying an analyzer definition:

```http
PUT /analyzers/prebuilt-myIdDocument
```

Include your modified analyzer definition in the request body. For detailed instructions, see [Create a custom analyzer](../tutorial/create-custom-analyzer.md).

> [!IMPORTANT]
> Prebuilt analyzer definitions can change across API versions. To ensure consistent behavior, make a copy of the prebuilt analyzer instead of relying on the prebuilt version directly in production scenarios.

### Lock analyzer behavior

The definition of prebuilt analyzers might change in the next API version of Content Understanding. To create a stable copy of a prebuilt analyzer that doesn't change with API updates, use the Copy operations by calling it as follows:

```http
POST /analyzers/myIdDocument:copy
{
  "source": "prebuilt-idDocument"
}
```

This operation creates a new analyzer with a fixed definition copied from the prebuilt analyzer at the time of the copy operation.

## Domain-specific analyzer reference

The following sections list all available domain-specific analyzers for specialized document processing. These prebuilt models enable you to add intelligent domain-specific document processing to your apps and flows without having to train and build your own models.

For information about supported file formats and input requirements, see [Service limits](../service-limits.md).

### Financial documents

* `prebuilt-invoice` - Invoices, utility bills, sales orders, purchase orders
* `prebuilt-receipt` - Sales receipts from retail and dining establishments
* `prebuilt-receipt.generic` - General sales receipts
* `prebuilt-receipt.hotel` - Hotel receipts and folios
* `prebuilt-creditCard` - Credit card statements
* `prebuilt-creditMemo` - Credit memos and refund documents
* `prebuilt-check.us` - US bank checks
* `prebuilt-bankStatement.us` - US bank statements

### Identity documents

* `prebuilt-idDocument` - Driver licenses, identification cards (IDs), residency permits, passports (worldwide), Social Security cards (US), military IDs (US), PAN cards (India), Aadhaar cards (India)
* `prebuilt-idDocument.generic` - Generic identification documents from various regions
* `prebuilt-idDocument.passport` - Passport books and passport cards (worldwide)
* `prebuilt-healthInsuranceCard.us` - US health insurance cards

### Tax documents (US)

#### Income tax forms

* `prebuilt-tax.us` - General US tax forms
* `prebuilt-tax.us.1040` - Form 1040 (US Individual Income Tax Return)
* `prebuilt-tax.us.1040Senior` - Form 1040 for senior taxpayers
* `prebuilt-tax.us.1040Schedule1` - Additional Income and Adjustments to Income
* `prebuilt-tax.us.1040Schedule2` - Additional Taxes
* `prebuilt-tax.us.1040Schedule3` - Additional Credits and Payments
* `prebuilt-tax.us.1040Schedule8812` - Credits for Qualifying Children
* `prebuilt-tax.us.1040ScheduleA` - Itemized Deductions
* `prebuilt-tax.us.1040ScheduleB` - Interest and Ordinary Dividends
* `prebuilt-tax.us.1040ScheduleC` - Profit or Loss from Business
* `prebuilt-tax.us.1040ScheduleD` - Capital Gains and Losses
* `prebuilt-tax.us.1040ScheduleE` - Supplemental Income and Loss
* `prebuilt-tax.us.1040ScheduleEIC` - Earned Income Credit
* `prebuilt-tax.us.1040ScheduleF` - Profit or Loss from Farming
* `prebuilt-tax.us.1040ScheduleH` - Household Employment Taxes
* `prebuilt-tax.us.1040ScheduleJ` - Income Averaging for Farmers
* `prebuilt-tax.us.1040ScheduleR` - Credit for the Elderly or Disabled
* `prebuilt-tax.us.1040ScheduleSE` - Self-Employment Tax

#### Form 1099 variants

* `prebuilt-tax.us.1099Combo` - Combined 1099 forms
* `prebuilt-tax.us.1099A` - Acquisition or Abandonment of Secured Property
* `prebuilt-tax.us.1099B` - Proceeds from Broker and Barter Exchange Transactions
* `prebuilt-tax.us.1099C` - Cancellation of Debt
* `prebuilt-tax.us.1099CAP` - Changes in Corporate Control and Capital Structure
* `prebuilt-tax.us.1099DA` - Debt Cancellation from Foreclosure
* `prebuilt-tax.us.1099DIV` - Dividends and Distributions
* `prebuilt-tax.us.1099G` - Certain Government Payments
* `prebuilt-tax.us.1099H` - Health Coverage Tax Credit Advance Payments
* `prebuilt-tax.us.1099INT` - Interest Income
* `prebuilt-tax.us.1099K` - Payment Card and Third Party Network Transactions
* `prebuilt-tax.us.1099LS` - Reportable Life Insurance Sale
* `prebuilt-tax.us.1099LTC` - Long-Term Care Benefits
* `prebuilt-tax.us.1099MISC` - Miscellaneous Income
* `prebuilt-tax.us.1099NEC` - Nonemployee Compensation
* `prebuilt-tax.us.1099OID` - Original Issue Discount
* `prebuilt-tax.us.1099PATR` - Taxable Distributions from Cooperatives
* `prebuilt-tax.us.1099Q` - Payments from Qualified Education Programs
* `prebuilt-tax.us.1099QA` - Distributions from ABLE Accounts
* `prebuilt-tax.us.1099R` - Distributions from Pensions and Annuities
* `prebuilt-tax.us.1099S` - Proceeds from Real Estate Transactions
* `prebuilt-tax.us.1099SA` - Distributions from Health Savings Account (HSA) or Medical Savings Account (MSA)
* `prebuilt-tax.us.1099SB` - Seller's Investment in Life Insurance Contract
* `prebuilt-tax.us.1099SSA` - Social Security Benefit Statement

#### Form 1098 variants

* `prebuilt-tax.us.1098` - Mortgage Interest Statement
* `prebuilt-tax.us.1098E` - Student Loan Interest Statement
* `prebuilt-tax.us.1098T` - Tuition Statement

#### Form 1095 variants

* `prebuilt-tax.us.1095A` - Health Insurance Marketplace Statement
* `prebuilt-tax.us.1095C` - Employer-Provided Health Insurance

#### Employment tax forms

* `prebuilt-tax.us.w2` - Wage and Tax Statement
* `prebuilt-tax.us.w4` - Employee's Withholding Certificate

### Mortgage documents (US)

* `prebuilt-mortgage.us` - General US mortgage documents
* `prebuilt-mortgage.us.1003` - Uniform Residential Loan Application
* `prebuilt-mortgage.us.1004` - Uniform Residential Appraisal Report
* `prebuilt-mortgage.us.1005` - Verification of Employment
* `prebuilt-mortgage.us.1008` - Uniform Underwriting and Transmittal Summary
* `prebuilt-mortgage.us.closingDisclosure` - Closing Disclosure

### Legal and business documents

* `prebuilt-contract` - Business contracts and agreements
* `prebuilt-marriageCertificate.us` - US marriage certificates

### Procurement documents

* `prebuilt-procurement` - Purchase orders, invoices, and procurement-related documents
* `prebuilt-purchaseOrder` - Purchase order forms

### Other specialized analyzers

* `prebuilt-payStub.us` - US pay stubs and earnings statements
* `prebuilt-utilityBill` - Utility bills (electricity, water, gas, internet, phone)

## Next steps

* [Try out prebuilt analyzers using REST API](../quickstart/use-rest-api.md)
* [Customize prebuilt analyzers](../tutorial/create-custom-analyzer.md)
