---
title: What's new in Document Intelligence
titleSuffix: Foundry Tools
description: Learn the latest updates to the Azure Document Intelligence in Foundry Tools.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: whats-new
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom:
  - references_regions
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD049 -->

# What's new in Azure Document Intelligence?

[!INCLUDE [applies to v4.0, v3.1, v3.0, and v2.1](includes/applies-to-v40-v31-v30-v21.md)]

Document Intelligence service is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

> [!IMPORTANT]
> Preview API versions are retired once the GA API is released. The 2023-02-28-preview API version is retiring. If you're still using the preview API or the associated SDK versions, update your code to target the latest API version `2024-11-30 (GA)`. </br>

## Latest updates

**Content Understanding: The Next Step Forward for Document Intelligence**
</br>
In November 2025, the GA version of **Content Understanding** was released (**2025-11-01** API version). Content Understanding is an evolution of Document Intelligence that expands multimodal processing capabilities to support text, images, audio, and video content types.

Key features include:

* **Multimodal content analysis**. Process and extract insights from text, images, audio, and video within a unified API framework.
* **Enhanced AI integration**. Seamlessly integrate with Azure AI services for intelligent content processing and decision-making workflows.
* **Flexible deployment options**. Build applications, automate document workflows, or enable AI-driven analytics with scalable cloud infrastructure.
* **Unified content extraction**. Utilize a single service to handle diverse content types, reducing complexity and improving operational efficiency.

## June 2025

**Document Intelligence v4.0 Read container is now available!**
</br>
This container image includes highly requested Read features like searchable PDF! For more information, *see:*

* [Install and run containers](containers/install-run.md?view=doc-intel-4.0.0&preserve-view=true)
* [Container image tags](containers/image-tags.md?view=doc-intel-4.0.0&preserve-view=true)

## April 2025

**Document Intelligence v4.0 Layout container is now available!**
</br>
For more information, *see:*

* [Install and run containers](containers/install-run.md?view=doc-intel-4.0.0&preserve-view=true)
* [Container image tags](containers/image-tags.md?view=doc-intel-4.0.0&preserve-view=true)

## December 2024

**Document Intelligence v4.0 programming language SDKs are now generally available (GA)**! </br></br>The latest client libraries default to the [**2024-11-30 REST API (GA)**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true) version of the service.</br></br>
For more information, *see* client libraries for the following supported programming languages:

* [.NET (C#)](versioning/changelog-release-history.md?view=doc-intel-4.0.0&tabs=csharp&preserve-view=true)

* [Java](versioning/changelog-release-history.md?view=doc-intel-4.0.0&tabs=java&preserve-view=true)

* [JavaScript](versioning/changelog-release-history.md?view=doc-intel-4.0.0&tabs=javascript&preserve-view=true)

* [Python](versioning/changelog-release-history.md?view=doc-intel-4.0.0&tabs=python&preserve-view=true)

## November 2024

**Document Intelligence REST API v4.0: [**2024-11-30 REST API (GA)**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true) is now generally available (GA)**! The v4.0 REST API includes the following changes:

* [Batch API](concept-batch-analysis.md)
  * Batch API now supports all models, including all read, layout, prebuilt verticals, and custom models.
  * Batch API supports LIST function to allow users to list batch jobs within past seven days.
  * Batch API supports DELETE function to explicitly delete batch job for GDPR and privacy compliance.
  * GetAnalyzeBatchResult supports resultId in response to LIST all resultIds.

* Searchable PDF. The [prebuilt read](prebuilt/read.md) model now supports images formats (JPEG/JPG, PNG, BMP, TIFF, HEIF)  and language expansion to include Chinese, Japanese, and Korean for  [PDF output](prebuilt/read.md#searchable-pdf).

* [Custom classification model](train/custom-model.md#custom-classification-model)
  * Custom classification model supports incremental training. You can add new samples to existing classes or add new classes by referencing an existing classifier.
  * With v4.0, custom classification model doesn't split documents by default during analysis. You need to explicitly set 'splitMode' property to auto to preserve the older behavior.
  * Custom classification model now supports 25,000 pages as new training page limit.

* [Custom Neural Model](train/custom-neural.md)
  * Custom Neural model now supports signature detection.
  * Custom neural models support paid training for longer duration when you need to train model with a larger labeled dataset. The first 20 training runs in a calendar month continue to be free. Any training operations over 20 is on the paid tier. Learn more details on [billing](train/custom-neural.md#billing).

* [ US Bank statement model](concept-bank-statement.md)
  * US Bank Statement Model now supports check table extraction.

* [Check model](concept-bank-check.md)
  * Supports Payer's Signature extraction

* [Mortgage documents model](concept-mortgage-documents.md)
  * Mortgage model now supports signature detection for  forms 1003, 1004, 1005 and closing disclosure.

* [Receipt Model](concept-receipt.md)
  * Receipt Model now supports more fields including ReceiptType, Tax rate, CountryRegion, net amount and description.

* [US Tax model](prebuilt/tax-document.md)
  * New prebuilt tax models added for `1095A`, `1095C`, `1099SSA`, and `W4`.

* [Delete analyze response](/rest/api/aiservices/document-models/delete-analyze-result?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true&tabs=HTTP)
  * Analyze response is stored for 24 hours from when the operation completes for retrieval. For scenarios where you want to delete the response sooner, use the delete analyze response API to delete the response.

* The v4.0 API includes cumulative updates from preview releases as listed:
  * [August 2024](#august-2024)
  * [May 2024](#may-2024)
  * [Feb 2024](#february-2024)

## August 2024

The Document Intelligence [**2024-07-31-preview**](/rest/api/aiservices/document-models?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true) REST API is now available. This preview API introduces new and updated capabilities:

* Public preview version [**2024-07-31-preview**](/rest/api/aiservices/operation-groups?view=rest-aiservices-2024-07-31-preview&preserve-view=true) is currently available only in the following Azure regions. The new document field extraction model in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) is only available in North Central US region:

* **East US**
* **West US2**
* **West Europe**
* **North Central US**

* [Model compose with custom classifiers](train/composed-models.md)
  * Document Intelligence now adds support for composing model with an explicit custom classification model. [Learn more about the benefits](train/composed-models.md) of using the new compose capability.
* [Custom classification model](train/custom-model.md#custom-classification-model)
  * Custom classification model now supports updating the model in-place as well.
  * Custom classification model adds support for model copy operation to enable backup and disaster recovery.
  * Custom classification model now supports explicitly specifying pages to be classified from an input document.
* [Mortgage documents model](concept-mortgage-documents.md)
  * Extract information from Appraisal (Form 1004).
  * Extract information from Validation of Employment (Form 1005).
* [Check model](concept-bank-check.md)
  * Extract payee, amount, date, and other relevant information from checks.​
* [Pay Stub model](concept-pay-stub.md)
  * New prebuilt to process pay stubs to extract wages, hours, deductions, net pay and more.​
* [Bank statement model](concept-bank-statement.md)
  * New prebuilt to extract account information including beginning and ending balances, transaction details from bank statements.​
* [US Tax model](prebuilt/tax-document.md)
  * New unified US tax model that can extract from forms such as W-2, 1098, 1099, and 1040.
* Searchable PDF. The [prebuilt read](prebuilt/read.md) model now supports [PDF output](prebuilt/read.md#searchable-pdf)  to download PDFs with embedded text from extraction results, allowing for PDF to be utilized in scenarios such as search copy of contents.
* [Layout model](prebuilt/layout.md) now supports improved [figure detection](prebuilt/layout.md#figures) where figures from documents can now be downloaded as an image file to be used for further figure understanding. The layout model also features improvements to the `OCR` model for scanned text targeting improvements for single characters, boxed text, and dense text documents.
* [Batch API](concept-batch-analysis.md)
  * Document Intelligence now adds support for batch analysis operation to support analyzing a set of documents to simplify developer experience and improve efficiency.
* [Add-on capabilities](concept-add-on-capabilities.md)
  * [Query fields](concept-add-on-capabilities.md#query-fields) AI quality of extraction is improved with the latest model.

## May 2024

The Document Intelligence Studio adds support for Microsoft Entra (formerly Azure Active Directory) authentication. For more information, *see* [Authentication in Document Intelligence Studio](quickstarts/get-started-studio.md#authentication-in-document-intelligence-studio).

## February 2024

The Document Intelligence [**2024-07-31-preview**](/rest/api/aiservices/document-models?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true) REST API is now available. This preview API introduces new and updated capabilities:

* Public preview version [**2024-07-31-preview**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true) is currently available only in the following Azure regions:

  * **East US**
  * **West US2**
  * **West Europe**

* [Layout model](prebuilt/layout.md) now supports [figure detection](prebuilt/layout.md#figures) and [hierarchical document structure analysis (sections and subsections)](prebuilt/layout.md#sections). The AI quality of reading order and logical roles detection is also improved.
* [Custom extraction models](train/custom-model.md#custom-extraction-models)
  * Custom extraction models now support cell, row, and table level confidence scores. Learn more about [table, row, and cell confidence](concept/accuracy-confidence.md#table-row-and-cell-confidence).
  * Custom extraction models have AI quality improvements for field extraction.
  * Custom template extraction model now supports extracting overlapping fields. Learn more about [overlapping fields and how you use them](train/custom-neural.md#overlapping-fields).
* [Custom classification model](train/custom-model.md#custom-classification-model)
  * Custom classification model now supported incremental training for scenarios where you need to update the classifier model with added samples or classes. Learn more about [incremental training](train/custom-classifier.md#incremental-training).
  * Custom classification model adds support for Office document types (.docx, .pptx, and .xls). Learn more about [expanded document type support](train/custom-classifier.md#office-document-type-support).
* [Invoice model](prebuilt/invoice.md)
  * Support for new locales:

  |Locale| Code|
  |---|---|
  |Arabic | (`ar`)|
  |Bulgarian| (`bg`)|
  |Greek |(`el`)|
  |Hebrew |(`he`)|
  |Macedonian|(`mk`)|
  |Russian (`ru`)| Serbian Cyrillic (`sr-cyrl`)|
  |Ukrainian |(`uk`)|
  |Thai|(`th`)|
  |Turkish|(`tr`)|
  |Vietnamese |(`vi`)|

  * Support for new currency codes:

  |Currency|Locale| Code|
  |---|---|---|
  |`BAM` | Bosnian Convertible Mark|(`ba`)|
  |`BGN`| Bulgarian Lev| (`bg`)|
  |`ILS` | Israeli New Shekel| (`il`)|
  |`MKD` | Macedonian Denar |(`mk`)|
  |`RUB` | Russian Ruble | (`ru`)|
  |`THB` | Thai Baht |(`th`) |
  |`TRY` | Turkish Lira| (`tr`)|
  |`UAH` | Ukrainian Hryvnia |(`ua`)|
  |`VND` | Vietnamese Dong| (`vn`) |

  * Tax items support expansion for Germany (`de`), Spain (`es`), Portugal (`pt`), English Canada `en-CA`.

* [ID model](prebuilt/id-document.md)
  * [Expanded field support](prebuilt/id-document.md#supported-document-types) for European Union identification cards and driver licenses.
* [Mortgage documents](concept-mortgage-documents.md)
  * Extract information from Uniform Residential Loan Application (Form 1003).
  * Extract information from Uniform Underwriting and Transmittal Summary or Form 1008.
  * Extract information from mortgage closing disclosure.
* [Credit/Debit card model](concept-credit-card.md)
  * Extract information from bank cards.
* [Marriage certificate](concept-marriage-certificate.md)
  * New prebuilt to extract information from marriage certificates.

## December 2023

The [Document Intelligence client libraries](sdk-overview-v4-0.md) targeting REST API **2023-10-31-preview** are now available for use!

## November 2023

The Document Intelligence [**2023-10-31-preview**](/rest/api/aiservices/document-models?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true) REST API is now available. This preview API introduces new and updated capabilities:

* Public preview version [**2023-10-31-preview**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true) is currently only available in the following Azure regions:

  * **East US**
  * **West US2**
  * **West Europe**

* [Read model](prebuilt/contract.md)
  * Language Expansion for Handwriting: Russian(`ru`), Arabic(`ar`), Thai(`th`).
  * Cyber Executive Order (EO) compliance.
* [Layout model](prebuilt/layout.md)
  * Support office and HTML files.
  * Markdown output support.
  * Table extraction, reading order, and section heading detection improvements.
  * With the Document Intelligence 2023-10-31-preview, the general document model (prebuilt-document) is deprecated. Going forward, to extract key-value pairs from documents, use the
    `prebuilt-layout` model with the optional query string parameter `features=keyValuePairs` enabled.
* [Receipt model](prebuilt/receipt.md)
  * Now extracts currency for all price-related fields.
* [Health Insurance Card model](prebuilt/health-insurance-card.md)
  * New field support for Medicare and Medicaid information.
* [US Tax Document models](prebuilt/tax-document.md)
  * New 1099 tax model. Supports base 1099 form and the following variations: A, B, C, CAP, DIV, G, H, INT, K, LS, LTC, MISC, NEC, OID, PATR, Q, QA, R, S, SA, SB​.
* [Invoice model](prebuilt/invoice.md)
  * Support for `KVK` field.
  * Support for `BPAY` field.
  * Numerous field refinements.
* [Custom Classification](train/custom-classifier.md)
  * Support for multi-language documents.
  * New page splitting options: autosplit, always split by page, no split.
* [Add-on capabilities](concept-add-on-capabilities.md)
  * [Query fields](concept-add-on-capabilities.md#query-fields) are available with the `2023-10-31-preview` release.
  * Add-on capabilities are available within all models excluding the [Read model](prebuilt/read.md).

>[!NOTE]
> With the `2022-08-31` API general availability (GA) release, the associated preview APIs are being deprecated. If you're using the 2021-09-30-preview, 2022-01-30-preview, or 2022-06-30-preview API versions, update your applications to target the `2022-08-31` API version. There are a few minor changes involved, for more information, _see_ the [migration guide](v3-1-migration-guide.md).


