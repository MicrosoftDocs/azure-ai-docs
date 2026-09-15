---
title: Azure Content Understanding in Foundry Tools prebuilt analyzers
titleSuffix: Foundry Tools
description: Learn about prebuilt analyzers, base analyzers, RAG analyzers, vertical analyzers, and how to use and customize them in Azure Content Understanding in Foundry Tools.
author: PatrickFarley 
ms.author: pafarley
manager: mcleans
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
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
- **[Domain-specific analyzers](#domain-specific-analyzers-in-detail)** - Preconfigured analyzers for common document categories with specialized field extraction for invoice processing, tax forms, ID verification, mortgage documents, and contracts.
- **[Utility analyzers](#utility-analyzers)** - Specialized tools for schema generation and field extraction to discover document structure and extract key-value pairs.

### Content extraction analyzers

Content extraction analyzers focus on optical character recognition and layout analysis. These analyzers are built on top of `prebuilt-document` and provide progressively richer extraction capabilities.

> [!NOTE]
> In the `2026-06-01-preview` API version, `prebuilt-read`, `prebuilt-layout`, and `prebuilt-digitalParse` return embedded document metadata, such as author, creation date, and title. In the `2025-11-01` GA version, only `prebuilt-digitalParse` returns metadata by default. For information on how different extraction operations are billed, see the [Pricing explainer](/azure/ai-services/content-understanding/pricing-explainer#document-content-extraction-meters).


#### `prebuilt-layout`

* Extracts content and layout elements such as words, figures, paragraphs, and tables from documents.
* Identifies document structure, including sections and formatting.
* Extracts hyperlinks embedded within documents.
* Captures annotations such as highlights, underlines, and strikethroughs in digital PDFs.
* Provides detailed layout information beyond basic text extraction.
* Detects figure types including charts, diagrams, pictures, icons, and other images, providing location information (PDF files only).
* Detects signatures and returns their location, along with any recognized text (`2026-06-01-preview` API version).

This prebuilt doesn't require a language model or embedding model.

#### `prebuilt-read`

* Extracts content elements such as words, paragraphs, formulas, and barcodes from documents.
* Provides basic optical character recognition (OCR) capabilities.
* Provides foundational text extraction without layout analysis.

This prebuilt doesn't require a language model or embedding model.


#### `prebuilt-digitalParse`
 
- Extracts machine-readable content from documents by directly analyzing the file’s internal structure and encoding.
- For scanned or image-based documents, use `prebuilt-read` or `prebuilt-layout`.

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
* Produces chunked output ready for embedding and vector indexing, preserving document structure across chunk boundaries with support for both fixed-size and layout-aware semantic chunking.
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

Domain-specific analyzers are preconfigured for common categories in popular industries. These analyzers provide specialized field extraction for specific document types and formats, powered by rich knowledge bases of real-world examples. 

Key categories include:

* **Procurement documents**: Extract structured data from procurement documents like invoices, receipts, and purchase orders. Tuned schemas capture line items, dates, and other key fields from procurement documents. See the [procurement documents](#procurement-documents) section.
* **Tax documents (US)**: Extract data from a comprehensive set of US tax forms, including Form 1040, W-2, and many more tax forms. Tuned schemas capture tax identifiers, amounts, and other meaningful tax fields. See the [tax documents](#tax-documents-us) section.
* **Legal documents**: Extract key information from contracts and business agreements. See the [legal and business documents](#legal-documents) section. 
* **Identity verification**: Process passports, health insurance cards, and other identification documents from multiple countries and regions. See the [identity documents](#identity-documents) section.
* **Financial documents**: Extract structured data from credit card statements, credit memos, and other bank statements. See the [financial documents](#financial-documents) section. 
* **Mortgage documents (US)**: Automate extraction from US mortgage documents, like appraisals, employment verifications, underwriting summaries, and closing disclosures. Includes a composed analyzer that automatically classifies and routes a wide range of mortgage documents. See the [mortgage documents](#mortgage-documents-us) section.
* **Personal records**: Extract information from personal documents like pay stubs, marriage certificates, and utility bills. See the [personal records](#personal-records) sections. 
* **Other prebuilt analyzers**: Analyze specialized content, such as call center recordings to extract topics, sentiment, and key insights. See the [other specialized analyzers](#other-prebuilt-analyzers) sections.


See the [complete list of domain-specific analyzers](#domain-specific-analyzers-in-detail) at the end of this article.

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

## Domain-specific analyzers (in detail)

The following sections list all available domain-specific analyzers for specialized document processing. These prebuilt models enable you to add intelligent domain-specific document processing to your apps and flows without having to train and build your own models.

For information about supported file formats and input requirements, see [Service limits](../service-limits.md).

### Procurement documents

* `prebuilt-procurement` - A composed prebuilt analyzer that classifies and routes a procurement document to the correct procurement analyzer for extraction. ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/procurement.md))
* `prebuilt-invoice` - Invoices, utility bills, sales orders, purchase orders ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/invoice.md))
* `prebuilt-receipt` - Sales receipts from retail and dining establishments ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/receipt/receipt.md))
* `prebuilt-receipt.generic` - General sales receipts ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/receipt/receipt.generic.md))
* `prebuilt-receipt.hotel` - Hotel receipts and folios ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/receipt/receipt.hotel.md))
* `prebuilt-utilityBill` - Utility bills (electricity, water, gas, internet, phone) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/utilityBill.md))
* `prebuilt-purchaseOrder` - Purchase order forms ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/purchaseOrder.md))
* `prebuilt-creditMemo` - Credit memo documents. ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/creditMemo.md))


### Tax documents (US)

#### Income tax forms

* `prebuilt-tax.us` - A composed prebuilt analyzer that classifies and routes a US tax form to the correct tax analyzer for extraction ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.md))
* `prebuilt-tax.us.1040` - Form 1040 (US Individual Income Tax Return) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040.md))
* `prebuilt-tax.us.1040Senior` - Form 1040 for senior taxpayers ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040Senior.md))
* `prebuilt-tax.us.1040Schedule1` - Additional Income and Adjustments to Income ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040Schedule1.md))
* `prebuilt-tax.us.1040Schedule2` - Additional Taxes ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040Schedule2.md))
* `prebuilt-tax.us.1040Schedule3` - Additional Credits and Payments ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040Schedule3.md))
* `prebuilt-tax.us.1040Schedule8812` - Credits for Qualifying Children ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040Schedule8812.md))
* `prebuilt-tax.us.1040ScheduleA` - Itemized Deductions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleA.md))
* `prebuilt-tax.us.1040ScheduleB` - Interest and Ordinary Dividends ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleB.md))
* `prebuilt-tax.us.1040ScheduleC` - Profit or Loss from Business ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleC.md))
* `prebuilt-tax.us.1040ScheduleD` - Capital Gains and Losses ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleD.md))
* `prebuilt-tax.us.1040ScheduleE` - Supplemental Income and Loss ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleE.md))
* `prebuilt-tax.us.1040ScheduleEIC` - Earned Income Credit ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleEIC.md))
* `prebuilt-tax.us.1040ScheduleF` - Profit or Loss from Farming ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleF.md))
* `prebuilt-tax.us.1040ScheduleH` - Household Employment Taxes ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleH.md))
* `prebuilt-tax.us.1040ScheduleJ` - Income Averaging for Farmers ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleJ.md))
* `prebuilt-tax.us.1040ScheduleR` - Credit for the Elderly or Disabled ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleR.md))
* `prebuilt-tax.us.1040ScheduleSE` - Self-Employment Tax ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1040ScheduleSE.md))

#### Form 1099 variants

* `prebuilt-tax.us.1099Combo` - Combined 1099 forms ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099Combo.md))
* `prebuilt-tax.us.1099A` - Acquisition or Abandonment of Secured Property ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099A.md))
* `prebuilt-tax.us.1099B` - Proceeds from Broker and Barter Exchange Transactions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099B.md))
* `prebuilt-tax.us.1099C` - Cancellation of Debt ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099C.md))
* `prebuilt-tax.us.1099CAP` - Changes in Corporate Control and Capital Structure ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099CAP.md))
* `prebuilt-tax.us.1099DA` - Debt Cancellation from Foreclosure ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099DA.md))
* `prebuilt-tax.us.1099DIV` - Dividends and Distributions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099DIV.md))
* `prebuilt-tax.us.1099G` - Certain Government Payments ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099G.md))
* `prebuilt-tax.us.1099H` - Health Coverage Tax Credit Advance Payments ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099H.md))
* `prebuilt-tax.us.1099INT` - Interest Income ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099INT.md))
* `prebuilt-tax.us.1099K` - Payment Card and Third Party Network Transactions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099K.md))
* `prebuilt-tax.us.1099LS` - Reportable Life Insurance Sale ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099LS.md))
* `prebuilt-tax.us.1099LTC` - Long-Term Care Benefits ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099LTC.md))
* `prebuilt-tax.us.1099MISC` - Miscellaneous Income ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099MISC.md))
* `prebuilt-tax.us.1099NEC` - Nonemployee Compensation ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099NEC.md))
* `prebuilt-tax.us.1099OID` - Original Issue Discount ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099OID.md))
* `prebuilt-tax.us.1099PATR` - Taxable Distributions from Cooperatives ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099PATR.md))
* `prebuilt-tax.us.1099Q` - Payments from Qualified Education Programs ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099Q.md))
* `prebuilt-tax.us.1099QA` - Distributions from ABLE Accounts ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099QA.md))
* `prebuilt-tax.us.1099R` - Distributions from Pensions and Annuities ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099R.md))
* `prebuilt-tax.us.1099S` - Proceeds from Real Estate Transactions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099S.md))
* `prebuilt-tax.us.1099SA` - Distributions from Health Savings Account (HSA) or Medical Savings Account (MSA) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099SA.md))
* `prebuilt-tax.us.1099SB` - Seller's Investment in Life Insurance Contract ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099SB.md))
* `prebuilt-tax.us.1099SSA` - Social Security Benefit Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1099SSA.md))

#### Form 1098 variants

* `prebuilt-tax.us.1098` - Mortgage Interest Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1098.md))
* `prebuilt-tax.us.1098E` - Student Loan Interest Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1098E.md))
* `prebuilt-tax.us.1098T` - Tuition Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1098T.md))

#### Form 1095 variants

* `prebuilt-tax.us.1095A` - Health Insurance Marketplace Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1095A.md))
* `prebuilt-tax.us.1095C` - Employer-Provided Health Insurance ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.1095C.md))

#### Employment tax forms

* `prebuilt-tax.us.w2` - Wage and Tax Statement ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.w2.md))
* `prebuilt-tax.us.w4` - Employee's Withholding Certificate ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/tax.us/tax.us.w4.md))

#### Schedule K-1 tax forms (preview)
* `prebuilt-tax.us.1041ScheduleK1` - Estate and Trust Schedule K-1 (Form 1041) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2026-06-01-preview/tax.us/tax.us.1041ScheduleK1/tax.us.1041ScheduleK1.md))
* `prebuilt-tax.us.1120SScheduleK1` - S-Corporation Schedule K-1 (Form 1120-S) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2026-06-01-preview/tax.us/tax.us.1120SScheduleK1/tax.us.1120SScheduleK1.md))
* `prebuilt-tax.us.1065ScheduleK1` - Partnership Schedule K-1 (Form 1065) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2026-06-01-preview/tax.us/tax.us.1065ScheduleK1/tax.us.1065ScheduleK1.md))
* `prebuilt-tax.us.8865ScheduleK1` - Foreign Partnership Schedule K-1 (Form 8865) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2026-06-01-preview/tax.us/tax.us.8865ScheduleK1/tax.us.8865ScheduleK1.md))

#### State-specific tax forms (preview)
* `prebuilt-tax.us.mn.m1` - Minnesota Form M1 — Individual Income Tax Return ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2026-06-01-preview/tax.us.mn.m1/tax.us.mn.m1.md))

### Legal documents

* `prebuilt-contract` - Business contracts and agreements ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/legal/contract.md))

### Identity documents

* `prebuilt-idDocument` - Driver licenses, identification cards (IDs), residency permits, passports (worldwide), Social Security cards (US), military IDs (US), PAN cards (India), Aadhaar cards (India) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/idDocument/idDocument.md))
* `prebuilt-idDocument.generic` - Generic identification documents from various regions ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/idDocument/idDocument.generic.md))
* `prebuilt-idDocument.passport` - Passport books and passport cards (worldwide) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/idDocument/idDocument.passport.md))
* `prebuilt-healthInsuranceCard.us` - US health insurance cards ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/personalRecords/healthInsuranceCard.us.md))

### Financial documents

* `prebuilt-creditCard` - Credit card statements ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/finance/creditCard.md))
* `prebuilt-creditMemo` - Credit memos and refund documents ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/creditMemo.md))
* `prebuilt-check.us` - US bank checks ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/finance/check.us.md))
* `prebuilt-bankStatement.us` - US bank statements ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/finance/bankStatement.us.md))

### Mortgage documents (US)

* `prebuilt-mortgage.us` - A composed prebuilt analyzer that classifies and routes a mortgage document to the correct mortgage analyzer for extraction ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.md))
* `prebuilt-mortgage.us.1003` - Uniform Residential Loan Application ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.1003.md))
* `prebuilt-mortgage.us.1004` - Uniform Residential Appraisal Report ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.1004.md))
* `prebuilt-mortgage.us.1005` - Verification of Employment ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.1005.md))
* `prebuilt-mortgage.us.1008` - Uniform Underwriting and Transmittal Summary ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.1008.md))
* `prebuilt-mortgage.us.closingDisclosure` - Closing Disclosure ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/mortgage.us/mortgage.us.closingDisclosure.md))

### Personal records

* `prebuilt-payStub.us` - US pay stubs and earnings statements ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/finance/payStub.us.md))
* `prebuilt-marriageCertificate.us` - US marriage certificates ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/personalRecords/marriageCertificate.us.md))
* `prebuilt-healthInsuranceCard.us` - US health insurance cards ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/personalRecords/healthInsuranceCard.us.md))
* `prebuilt-utilityBill` - Utility bills (electricity, water, gas, internet, phone) ([schema](https://github.com/Azure/content-understanding-toolkit/blob/main/prebuilt-schema/2025-11-01/procurement/utilityBill.md))

### Other prebuilt analyzers

* `prebuilt-callCenter` - Call recordings to extract topics, sentiment, and key topics

## Next steps

* [Try out prebuilt analyzers using REST API](../quickstart/use-rest-api.md)
* [Customize prebuilt analyzers](../tutorial/create-custom-analyzer.md)
