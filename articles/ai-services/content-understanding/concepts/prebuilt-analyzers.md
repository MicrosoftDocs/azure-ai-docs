---
title: Azure AI Content Understanding prebuilt analyzers
titleSuffix: Azure AI services
description: Learn about prebuilt analyzers, base analyzers, RAG analyzers, vertical analyzers, and how to use and customize them in Azure AI Content Understanding.
author: PatrickFarley 
ms.author: admaheshwari
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Prebuilt analyzers in Azure AI Content Understanding

Azure AI Content Understanding prebuilt analyzers enable you to add intelligent domain-specific content processing to your apps and flows without training and building your own models. Prebuilt analyzers are ready-to-use tools designed to streamline common content processing tasks, from content ingestion for search and retrieval-augmented generation (RAG) workflows to intelligent document processing (IDP) for extracting data from invoices or analyzing call center recordings. You can also [customize these analyzers](../tutorial/create-custom-analyzer.md) to extract additional fields or refine outputs to better fit your specific workflow requirements.

## Analyzer types

Azure AI Content Understanding provides several categories of analyzers to support different scenarios:

### Base analyzers

Base analyzers provide fundamental content processing capabilities and are intended primarily for use as a `baseAnalyzerId` when [creating custom analyzers](../tutorial/create-custom-analyzer.md). While you can use these analyzers directly, they're most powerful when extended with custom field schemas.

* `prebuilt-audio` - Base audio processing
* `prebuilt-document` - Base document processing
* `prebuilt-image` - Base image processing
* `prebuilt-video` - Base video processing
* `prebuilt-callCenter` - Base call center audio processing

> [!NOTE]
> Currently, you can only derive custom analyzers from base analyzers. Support for deriving from other prebuilt analyzers is planned for future releases.

### RAG analyzers

RAG analyzers are optimized for retrieval-augmented generation scenarios. These analyzers extract content with layout as markdown and perform semantic analysis to enhance retrieval quality for downstream applications.

#### `prebuilt-documentAnalyzer`

* Extracts various content and layout elements such as paragraphs, and tables, figure descriptions from documents
* Enables figure description to add textual descriptions of images, charts and diagrams
* Enabled annotation so that hand-written markup on the document file is captured
* Generates a one-paragraph description of the document content
* Supports a wide range of file formats including PDF, images, Office documents, and text files
* Recommended for document ingestion in RAG workflows

#### `prebuilt-imageAnalyzer`

* Analyzes images to generate descriptions and insights
* Generates a one-paragraph description of the image content
* Extracts visual content for search and retrieval applications

#### `prebuilt-audioAnalyzer`

* Transcribes conversations from audio and video files
* Generates a one-paragraph summary of the conversation content
* Supports multiple locales for international content processing
* Optimized for conversation analysis and content extraction

#### `prebuilt-videoAnalyzer`

* Analyzes videos to extract transcripts and descriptions for each segment
* Automatically segments videos into meaningful sections based on topic shifts, scene changes, or visual cues
* Generates detailed summaries focusing on people, places, and actions for each segment
* Supports scene splitting and comprehensive video content analysis
* Provides transcript extraction along with contextual segment descriptions

### Vertical analyzers

Vertical analyzers are preconfigured for common document categories in popular industries. These analyzers provide specialized field extraction for specific document types and formats.

See the [complete list of vertical analyzers](#vertical-analyzer-reference) at the end of this article.

### Utility analyzers

Utility analyzers provide specialized functionality for schema generation and field extraction.

#### `prebuilt-documentFieldSchema`

* Analyzes documents to propose an appropriate field schema
* Useful for discovering structure in new document types

#### `prebuilt-documentFields`

* Extracts key-value pairs from documents
* Used internally by vertical analyzers when the input doesn't match any of the predefined schemas (for example, `prebuilt-idDocument`)

### OCR analyzers

OCR analyzers focus on optical character recognition and layout analysis.

#### `prebuilt-read`

* Extracts text from documents and images
* Provides basic OCR capabilities

#### `prebuilt-layout`

* Extracts text with detailed layout information
* Identifies document structure including tables, sections, and formatting

#### `prebuilt-layoutWithFigures`

* Extends layout extraction with figure detection and analysis
* Extracts charts, diagrams, and images with their context

## Use prebuilt analyzers

To analyze content with a prebuilt analyzer, make a POST request to the analyze endpoint:

```http
POST /analyzers/prebuilt-idDocument:analyze
```

Replace `prebuilt-idDocument` with the analyzer ID that matches your scenario.

## Customize prebuilt analyzers

You can use any prebuilt analyzer as a template for creating a custom analyzer that better fits your specific needs.

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

Include your modified analyzer definition in the request body. See [Create a custom analyzer](../tutorial/create-custom-analyzer.md) for detailed instructions.

> [!IMPORTANT]
> Prebuilt analyzer definitions are subject to change across API versions. To ensure consistent behavior, make a copy of the prebuilt analyzer rather than relying on the prebuilt version directly in production scenarios.

### Lock analyzer behavior

To create a stable copy of a prebuilt analyzer that won't change with API updates:

```http
POST /analyzers/myIdDocument:copy
{
  "source": "prebuilt-idDocument"
}
```

This creates a new analyzer with a fixed definition copied from the prebuilt analyzer at the time of the copy operation.

## Vertical analyzer reference

The following sections list all available vertical analyzers for specialized document processing. These prebuilt models enable you to add intelligent domain-specific document processing to your apps and flows without having to train and build your own models.

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

* `prebuilt-idDocument` - Driver licenses, identification cards, residency permits, passports (worldwide), Social Security cards (US), military IDs (US), PAN cards (India), Aadhaar cards (India)
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
* `prebuilt-tax.us.1099SA` - Distributions from HSA or MSA
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
