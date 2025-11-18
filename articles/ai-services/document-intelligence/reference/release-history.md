---
title: Azure Document Intelligence in Foundry Tools release history
titleSuffix: Foundry Tools
description: Release notes and updates for Azure Document Intelligence in Foundry Tools API.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: references_regions
---

# Azure Document Intelligence in Foundry Tools release history

Azure Document Intelligence is an innovative a cloud-based service that utilizes machine learning to streamline data processing within applications and workflows. This service is essential for boosting data-driven strategies and improving document search functionalities. Here, discover key milestones and enhancements that have contributed to the evolution of Azure Document Intelligence. For more information on recent advances, *see* [What's new?](../whats-new.md).

## July 2023

> [!NOTE]
> Form Recognizer is now **Azure Document Intelligence**!
>
> * No changes to pricing.
> * The names *Cognitive Services* and *Azure Applied AI* continue to be used in Azure billing, cost analysis, price list, and price APIs.
> * No breaking changes to application programming interfaces (APIs) or client libraries.
> * Some platforms are still awaiting the renaming update. All mention of Form Recognizer or Document Intelligence in our documentation refers to the same Azure service.

**Document Intelligence v3.1 (GA)**

The Document Intelligence version 3.1 API is now generally available (GA)! The API version corresponds to ```2023-07-31```.
The v3.1 API introduces new and updated capabilities:

* Document Intelligence APIs are now more modular and with support for optional features. You can now customize the output to specifically include the features you need. Learn more about the [optional parameters](../versioning/v3-1-migration-guide.md).
* Document classification API for splitting a single file into individual documents. [Learn more](../train/custom-classifier.md) about document classification.
* [Prebuilt contract model](../prebuilt/contract.md).
* [Prebuilt US tax form 1098 model](../prebuilt/tax-document.md).
* Support for [Office file types](../prebuilt/read.md) with Read API.
* [Barcode recognition](../prebuilt/read.md) in documents.
* Formula recognition [add-on capability](../concept/add-on-capabilities.md).
* Font recognition [add-on capability](../concept/add-on-capabilities.md).
* Support for [high resolution documents](../concept/add-on-capabilities.md).
* Custom neural models now require a single labeled sample to train.
* Custom neural models language expansion. Train a neural model for documents in 30 languages. See [language support](../language-support/custom.md) for the complete list of supported languages.
* 🆕 [Prebuilt health insurance card model](../prebuilt/health-insurance-card.md).
* [Prebuilt invoice model locale expansion](../prebuilt/invoice.md#supported-languages-and-locales).
* [Prebuilt receipt model language and locale expansion](../prebuilt/receipt.md#supported-languages-and-locales) with more than 100 languages supported.
* [Prebuilt ID model](../prebuilt/id-document.md#supported-document-types) now supports European IDs.

**Document Intelligence Studio UX Updates**

✔️ **Analyze Options**</br>

* Document Intelligence now supports more sophisticated analysis capabilities and the Studio allows one entry point (Analyze options button) for configuring the add-on capabilities with ease.
* Depending on the document extraction scenario, configure the analysis range, document page range, optional detection, and premium detection features.

    :::image type="content" source="../media/studio/analyze-options.gif" alt-text="Animated screenshot showing use of the analyze-options button to configure options in Studio.":::

    > [!NOTE]
    > Font extraction isn't visualized in Document Intelligence Studio. However, you can check the styles section of the JSON output for the font detection results.

✔️ **Auto labeling documents with prebuilt models or one of your own models**

* In custom extraction model labeling page, you can now auto label your documents using one of Document Intelligent Service prebuilt models or models you previously trained.

    :::image type="content" source="../media/studio/auto-label.gif" alt-text="Animated screenshot showing auto labeling in Studio.":::

* For some documents, there can be duplicate labels after running auto label. Make sure to modify the labels so that there are no duplicate labels in the labeling page afterwards.

    :::image type="content" source="../media/studio/duplicate-labels.png" alt-text="Screenshot showing duplicate label warning after auto labeling.":::

✔️ **Auto labeling tables**

* In custom extraction model labeling page, you can now auto label the tables in the document without having to label the tables manually.

    :::image type="content" source="../media/studio/auto-table-label.gif" alt-text="Animated screenshot showing auto table labeling in Studio.":::

✔️ **Add test files directly to your training dataset**

* Once you train a custom extraction model, make use of the test page to improve your model quality by uploading test documents to training dataset if needed.

* If a low confidence score is returned for some labels, make sure your labels are correct. If not, add them to the training dataset and relabel to improve the model quality.

:::image type="content" source="../media/studio/add-from-test.gif" alt-text="Animated screenshot showing how to add test files to training dataset.":::

✔️ **Make use of the document list options and filters in custom projects**

* Use the custom extraction model labeling page. You can now navigate through your training documents with ease by making use of the search, filter, and sort by feature.

* Utilize the grid view to preview documents or use the list view to scroll through the documents more easily.

    :::image type="content" source="../media/studio/document-options.png" alt-text="Screenshot showing document list view options and filters.":::

✔️ **Project sharing**

* Share custom extraction projects with ease. For more information, see [Project sharing with custom models](../how-to-guides/project-share-custom-models.md).

## **May** 2023

**Introducing refreshed documentation for Build 2023**

* [🆕 Document Intelligence Overview](../overview.md?view=doc-intel-3.0.0&preserve-view=true) enhanced navigation, structured access points, and enriched images.

* [🆕 Choose a Document Intelligence model](../concept/choose-model-feature.md?view=doc-intel-3.0.0&preserve-view=true) provides guidance for choosing the best Document Intelligence solution for your projects and workflows.

## April 2023

**Announcing the latest Document Intelligence client-library public preview release**

* Document Intelligence REST API Version **2023-02-28-preview** supports the public preview release client libraries. This release includes the following new features and capabilities available for .NET/C# (4.1.0-beta-1), Java (4.1.0-beta-1), JavaScript (4.1.0-beta-1), and Python (3.3.0b.1) client libraries:

  * [**Custom classification model**](../train/custom-classifier.md)

  * [**Query fields extraction**](../concept/query-fields.md)

  * [**Add-on capabilities**](../concept/add-on-capabilities.md)

* For more information, _see_ [**Document Intelligence SDK (../public preview**)](../versioning/sdk-overview-v4-0.md) and [March 2023 release](#march-2023) notes

## March 2023

> [!IMPORTANT]
> **`2023-02-28-preview`** capabilities are currently only available in the following regions:
>
> * West Europe
> * West US2
> * East US

* [**Custom classification model**](../train/custom-classifier.md) is a new capability within Document Intelligence starting with the ```2023-02-28-preview``` API.
* [**Query fields**](../concept/query-fields.md) capabilities added to the General Document model, use Azure OpenAI models to extract specific fields from documents. Try the **General documents with query fields** feature using the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio). Query fields are currently only active for resources in the `East US` region.
* [**Add-on capabilities**](../concept/add-on-capabilities.md):
  * [**Font extraction**](../concept/add-on-capabilities.md#font-property-extraction) is now recognized with the ```2023-02-28-preview``` API.
  * [**Formula extraction**](../concept/add-on-capabilities.md#formula-extraction) is now recognized with the ```2023-02-28-preview``` API.
  * [**High resolution extraction**](../concept/add-on-capabilities.md#high-resolution-extraction) is now recognized with the ```2023-02-28-preview``` API.
* [**Custom extraction model updates**](../train/custom-model.md):
  * [**Custom neural model**](../train/custom-neural.md) now supports added languages for training and analysis. Train neural models for Dutch, French, German, Italian, and Spanish.
  * [**Custom template model**](../train/custom-template.md) now has an improved signature detection capability.
* [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com/studio) updates:
  * In addition to support for all the new features like classification and query fields, the Studio now enables project sharing for custom model projects.
  * New model additions in gated preview: **Vaccination cards**, **Contracts**, **US Tax 1098**, **US Tax 1098-E**, and **US Tax 1098-T**. To request access to gated preview models, complete and submit the [**Document Intelligence private preview request form**](https://aka.ms/form-recognizer/preview/survey).
* [**Receipt model updates**](../prebuilt/receipt.md):
  * Receipt model adds support for thermal receipts.
  * Receipt model now adds language support for 18 languages and three regional languages (English, French, Portuguese).
  * Receipt model now supports `TaxDetails` extraction.
* [**Layout model**](../prebuilt/layout.md) now improves table recognition.
* [**Read model**](../prebuilt/read.md) now adds improvement for single-digit character recognition.

---

## February 2023

* Select Document Intelligence containers for v3.0 are now available for use!
* Currently **Read v3.0** and **Layout v3.0** containers are available.

  For more information, _see_ [Install and run Document Intelligence containers](../containers/install-run.md?view=doc-intel-3.0.0&preserve-view=true).

---

## January 2023

* Prebuilt receipt model -  added languages supported. The receipt model now supports these added languages and locales
  * Japanese - Japan (ja-JP)
  * French - Canada (fr-CA)
  * Dutch - Netherlands (nl-NL)
  * English - United Arab Emirates (en-AE)
  * Portuguese - Brazil (pt-BR)

* Prebuilt invoice model - added languages supported. The invoice model now supports these added languages and locales
  * English - United States (en-US), Australia (en-AU), Canada (en-CA), United Kingdom (en-UK), India (en-IN)
  * Spanish - Spain (es-ES)
  * French - France (fr-FR)
  * Italian - Italy (it-IT)
  * Portuguese - Portugal (pt-PT)
  * Dutch - Netherlands (nl-NL)

* Prebuilt invoice model - added fields recognized. The invoice model now recognizes these added fields
  * Currency code
  * Payment options
  * Total discount
  * Tax items (en-IN only)

* Prebuilt ID model - added document types supported. The ID model now supports these added document types
  * US Military ID

> [!TIP]
> All January 2023 updates are available with [REST API version **2022-08-31 (GA)**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP).

* **[Prebuilt receipt model](../prebuilt/receipt.md#supported-languages-and-locales)—additional language support**:

   The **prebuilt receipt model** adds support for the following languages:

  * English - United Arab Emirates (en-AE)
  * Dutch - Netherlands (nl-NL)
  * French - Canada (fr-CA)
  * German - (de-DE)
  * Italian - (it-IT)
  * Japanese - Japan (ja-JP)
  * Portuguese - Brazil (pt-BR)

* **[Prebuilt invoice model](../prebuilt/invoice.md)—additional language support and field extractions**

  The **prebuilt invoice model** adds support for the following languages:

  * English - Australia (en-AU), Canada (en-CA), United Kingdom (en-UK), India (en-IN)
  * Portuguese - Brazil (pt-BR)

  The **prebuilt invoice model** now adds support for the following field extractions:

  * Currency code
  * Payment options
  * Total discount
  * Tax items (en-IN only)

* **[Prebuilt ID document model](../prebuilt/id-document.md#supported-document-types)—additional document types support**

  The **prebuilt ID document model** now adds support for the following document types:

  * Driver's license expansion supporting India, Canada, United Kingdom, and Australia
  * US military ID cards and documents
  * India ID cards and documents (PAN and Aadhaar)
  * Australia ID cards and documents (photo card, Key-pass ID)
  * Canada ID cards and documents (identification card, Maple card)
  * United Kingdom ID cards and documents (national/regional identity card)

---

## December 2022

* [**Document Intelligence Studio updates**](https://formrecognizer.appliedai.azure.com/studio)

  The December Document Intelligence Studio release includes the latest updates to Document Intelligence Studio. There are significant improvements to user experience, primarily with custom model labeling support.

  * **Page range**. The Studio now supports analyzing specified pages from a document.

  * **Custom model labeling**:

    * **Run Layout API automatically**. You can opt to run the Layout API for all documents automatically in your blob storage during the setup process for custom model.

    * **Search**. The Studio now includes search functionality to locate words within a document. This improvement allows for easier navigation while labeling.

    * **Navigation**. You can select labels to target labeled words within a document.

    * **Auto table labeling**. After you select the table icon within a document, you can opt to autolabel the extracted table in the labeling view.

    * **Label subtypes and second-level subtypes** The Studio now supports subtypes for table columns, table rows, and second-level subtypes for types such as dates and numbers.

* Building custom neural models is now supported in the US Gov Virginia region.

* Preview API versions ```2022-01-30-preview``` and ```2021-09-30-preview``` will be retired January 31 2023. Update to the ```2022-08-31``` API version to avoid any service disruptions.

---

## November 2022

* **Announcing the latest stable release of Azure Document Intelligence libraries**
  * This release includes important changes and updates for .NET, Java, JavaScript, and Python client libraries. For more information, _see_ [**Azure SDK DevBlog**](https://devblogs.microsoft.com/azure-sdk/announcing-new-stable-release-of-azure-form-recognizer-libraries/).
  * The most significant enhancements are the introduction of two new clients, the **`DocumentAnalysisClient`** and the **`DocumentModelAdministrationClient`**.

---

## October 2022

* **Document Intelligence versioned content**
  * Document Intelligence documentation is updated to present a versioned experience. Now, you can choose to view content targeting the `v3.0 GA` experience or the `v2.1 GA` experience. The v3.0 experience is the default.

    :::image type="content" source="../media/versioning-and-monikers.png" alt-text="Screenshot of the Document Intelligence landing page denoting the version dropdown menu.":::

* **Document Intelligence Studio Sample Code**
  * Sample code for the [Document Intelligence Studio labeling experience](https://github.com/microsoft/Form-Recognizer-Toolkit/tree/main/SampleCode/LabelingUX) is now available on GitHub. Customers can develop and integrate Document Intelligence into their own UX or build their own new UX using the Document Intelligence Studio sample code.

* **Language expansion**
  * With the latest preview release, Document Intelligence's Read (OCR), Layout, and Custom template models support 134 new languages. These language additions include Greek, Latvian, Serbian, Thai, Ukrainian, and Vietnamese, along with several Latin, and Cyrillic languages. Document Intelligence now has a total of 299 supported languages across the most recent GA and new preview versions. Refer to the supported languages pages to see all supported languages.
  * Use the REST API parameter `api-version=2022-06-30-preview` when using the API or the corresponding SDK to support the new languages in your applications.

* **New Prebuilt Contract model**
  * A new prebuilt that extracts information from contracts such as parties, title, contract ID, execution date and more. the contracts model is currently in preview, request access [here](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUQTRDQUdHMTBWUDRBQ01QUVNWNlNYMVFDViQlQCN0PWcu_).

* **Region expansion for training custom neural models**
  * Training custom neural models now supported in added regions.
    > [!div class="checklist"]
    >
    > * East US
    > * East US2
    > * US Gov Arizona

---

## September 2022

>[!NOTE]
> Starting with version 4.0.0, a new set of clients is introduced to apply the newest features of the Document Intelligence service.

**SDK version 4.0.0 GA release includes the following updates:**

### [**C#**](#tab/csharp)

* **Version 4.0.0 GA (2022-09-08)**
* **Supports REST API v3.0 and v2.0 clients**

[**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.FormRecognizer/4.0.0)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/formrecognizer/Azure.AI.FormRecognizer/CHANGELOG.md)

[**Migration guide**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.FormRecognizer_4.0.0/sdk/formrecognizer/Azure.AI.FormRecognizer/MigrationGuide.md)

[**ReadMe**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.FormRecognizer_4.0.0/sdk/formrecognizer/Azure.AI.FormRecognizer/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.FormRecognizer_4.0.0/sdk/formrecognizer/Azure.AI.FormRecognizer/samples/README.md)

### [**Java**](#tab/java)

* **Version 4.0.0 GA (2022-09-08)**
* **Supports REST API v3.0 and v2.0 clients**

[**Package (Maven)**](https://oss.sonatype.org/#nexus-search;quick~azure-ai-formrecognizer)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-formrecognizer_4.0.0/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md)

[**Migration guide**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-formrecognizer_4.0.0/sdk/formrecognizer/azure-ai-formrecognizer/migration-guide.md)

[**ReadMe**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-formrecognizer_4.0.0/sdk/formrecognizer/azure-ai-formrecognizer/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-formrecognizer_4.0.0/sdk/formrecognizer/azure-ai-formrecognizer/src/samples/README.md)

### [**JavaScript**](#tab/javascript)

* **Version 4.0.0 GA (2022-09-08)**
* **Supports REST API v3.0 and v2.0 clients**

[**Package (npm)**](https://www.npmjs.com/package/@azure/ai-form-recognizer)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-form-recognizer_4.0.0/sdk/formrecognizer/ai-form-recognizer/CHANGELOG.md)

[**Migration guide**](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-form-recognizer_4.0.0/sdk/formrecognizer/ai-form-recognizer/MIGRATION-v3_v4.md)

[**ReadMe**](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-form-recognizer_4.0.0/sdk/formrecognizer/ai-form-recognizer/README.md)

[**Samples**](https://github.com/witemple-msft/azure-sdk-for-js/blob/7e3196f7e529212a6bc329f5f06b0831bf4cc174/sdk/formrecognizer/ai-form-recognizer/samples/v4/javascript/README.md)

### [Python](#tab/python)

> [!NOTE]
> Python 3.7 or later is required to use this package.

* **Version 3.2.0 GA (2022-09-08)**
* **Supports REST API v3.0 and v2.0 clients**

[**Package (PyPi)**](https://pypi.org/project/azure-ai-formrecognizer/3.2.0/)

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md)

[**Migration guide**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0/sdk/formrecognizer/azure-ai-formrecognizer/MIGRATION_GUIDE.md)

[**ReadMe**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0/sdk/formrecognizer/azure-ai-formrecognizer/README.md)

[**Samples**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0/sdk/formrecognizer/azure-ai-formrecognizer/samples/README.md)

---

* **Region expansion for training custom neural models now supported in six new regions**
    > [!div class="checklist"]
    >
    > * Australia East
    > * Central US
    > * East Asia
    > * France Central
    > * UK South
    > * West US2

  * For a complete list of regions where training is supported see [custom neural models](../train/custom-neural.md).

  * Document Intelligence SDK version `4.0.0 GA` release:
    * **Document Intelligence client libraries version 4.0.0 (.NET/C#, Java, JavaScript) and version 3.2.0 (Python) are generally available and ready for use in production applications!**.
    * For more information on Document Intelligence client libraries, see the [**SDK overview**](../versioning/sdk-overview-v3-1.md).
    * Update your applications using your programming language's **migration guide**.

---

## August 2022

**Document Intelligence SDK beta August 2022 preview release includes the following updates:**

### [**C#**](#tab/csharp)

**Version 4.0.0-beta.5 (2022-08-09)**

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/formrecognizer/Azure.AI.FormRecognizer/CHANGELOG.md#400-beta5-2022-08-09)

[**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.FormRecognizer/4.0.0-beta.5)

[**SDK reference documentation**](/dotnet/api/overview/azure/ai.formrecognizer-readme?view=azure-dotnet-preview&preserve-view=true)

### [**Java**](#tab/java)

**Version 4.0.0-beta.6 (2022-08-10)**

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md#400-beta6-2022-08-10)

 [**Package (Maven)**](https://oss.sonatype.org/#nexus-search;quick~azure-ai-formrecognizer)

 [**SDK reference documentation**](/java/api/overview/azure/ai-formrecognizer-readme?view=azure-java-preview&preserve-view=true)

### [**JavaScript**](#tab/javascript)

**Version 4.0.0-beta.6 (2022-08-09)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-form-recognizer_4.0.0-beta.6/sdk/formrecognizer/ai-form-recognizer/CHANGELOG.md)

 [**Package (npm)**](https://www.npmjs.com/package/@azure/ai-form-recognizer/v/4.0.0-beta.6)

 [**SDK reference documentation**](/javascript/api/overview/azure/ai-form-recognizer-readme?view=azure-node-preview&preserve-view=true)

### [Python](#tab/python)

> [!IMPORTANT]
> Python 3.6 is no longer supported in this release. Use Python 3.7 or later.

**Version 3.2.0b6 (2022-08-09)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0b6/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md)

 [**Package (PyPi)**](https://pypi.org/project/azure-ai-formrecognizer/3.2.0b6/)

 [**SDK reference documentation**](https://pypi.org/project/azure-ai-formrecognizer/3.2.0b6/)

---

* Document Intelligence v3.0 generally available

  * **Document Intelligence REST API v3.0 is now generally available and ready for use in production applications!** Update your applications with [**REST API version 2022-08-31**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP).

* Document Intelligence Studio updates
  > [!div class="checklist"]
  >
  > * **Next steps**. Under each model page, the Studio now has a next steps section. Users can quickly reference sample code, troubleshooting guidelines, and pricing information.
  > * **Custom models**. The Studio now includes the ability to reorder labels in custom model projects to improve labeling efficiency.
  > * **Copy Models** Custom models can be copied across Document Intelligence services from within the Studio. The operation enables the promotion of a trained model to other environments and regions.
  > * **Delete documents**. The Studio now supports deleting documents from labeled dataset within custom projects.

* Document Intelligence service updates

  * [**prebuilt-read**](../prebuilt/read.md). Read OCR model is now also available in Document Intelligence with paragraphs and language detection as the two new features. Document Intelligence Read targets advanced document scenarios aligned with the broader document intelligence capabilities in Document Intelligence.
  * [**prebuilt-layout**](../prebuilt/layout.md). The Layout model extracts paragraphs and whether the extracted text is a paragraph, title, section heading, footnote, page header, page footer, or page number.
  * [**prebuilt-invoice**](../prebuilt/invoice.md). The TotalVAT and Line/VAT fields now resolves to the existing fields TotalTax and Line/Tax respectively.
  * [**prebuilt-idDocument**](../prebuilt/id-document.md). Data extraction support for US state ID, social security, and green cards. Support for passport visa information.
  * [**prebuilt-receipt**](../prebuilt/receipt.md). Expanded locale support for French (fr-FR), Spanish (es-ES), Portuguese (pt-PT), Italian (it-IT) and German (de-DE).
  * [**prebuilt-businessCard**](../prebuilt/business-card.md). Address parse support to extract subfields for address components like address, city, state, country/region, and zip code.

* **AI quality improvements**

  * [**prebuilt-read**](../prebuilt/read.md). Enhanced support for single characters, handwritten dates, amounts, names, other key data commonly found in receipts and invoices and improved processing of digital PDF documents.
  * [**prebuilt-layout**](../prebuilt/layout.md). Support for better detection of cropped tables, borderless tables, and improved recognition of long spanning cells.
  * [**prebuilt-document**](../prebuilt/general-document.md). Improved value and check box detection.
  * [**custom-neural**](../train/custom-neural.md). Improved accuracy for table detection and extraction.

---

## June 2022

* Document Intelligence SDK beta June 2022 preview release includes the following updates:

### [**C#**](#tab/csharp)

**Version 4.0.0-beta.4 (2022-06-08)**

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.FormRecognizer_4.0.0-beta.4/sdk/formrecognizer/Azure.AI.FormRecognizer/CHANGELOG.md)

[**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.FormRecognizer/4.0.0-beta.4)

[**SDK reference documentation**](/dotnet/api/azure.ai.formrecognizer?view=azure-dotnet-preview&preserve-view=true)

### [**Java**](#tab/java)

**Version 4.0.0-beta.5 (2022-06-07)**

[**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-formrecognizer_4.0.0-beta.5/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md)

 [**Package (Maven)**](https://search.maven.org/artifact/com.azure/azure-ai-formrecognizer/4.0.0-beta.5/jar)

 [**SDK reference documentation**](/java/api/overview/azure/ai-formrecognizer-readme?view=azure-java-preview&preserve-view=true)

### [**JavaScript**](#tab/javascript)

**Version 4.0.0-beta.4 (2022-06-07)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/%40azure/ai-form-recognizer_4.0.0-beta.4/sdk/formrecognizer/ai-form-recognizer/CHANGELOG.md)

 [**Package (npm)**](https://www.npmjs.com/package/@azure/ai-form-recognizer/v/4.0.0-beta.4)

 [**SDK reference documentation**](/javascript/api/@azure/ai-form-recognizer/?view=azure-node-preview&preserve-view=true)

### [Python](#tab/python)

**Version 3.2.0b5 (2022-06-07**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0b5/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md)

 [**Package (PyPi)**](https://pypi.org/project/azure-ai-formrecognizer/3.2.0b5/)

 [**SDK reference documentation**](/python/api/azure-ai-formrecognizer/azure.ai.formrecognizer?view=azure-python-preview&preserve-view=true)

---

* [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio) June release is the latest update to the Document Intelligence Studio. There are considerable user experience and accessibility improvements addressed in this update:

  * **Code sample for JavaScript and C#**. The Studio code tab now adds JavaScript and C# code samples in addition to the existing Python one.
  * **New document upload UI**. Studio now supports uploading a document with drag & drop into the new upload user interface.
  * **New feature for custom projects**. Custom projects now support creating storage account and blobs when configuring the project. In addition, custom project now supports uploading training files directly within the Studio and copying the existing custom model.

* Document Intelligence v3.0 **2022-06-30-preview** release presents extensive updates across the feature APIs:

  * [**Layout extends structure extraction**](../prebuilt/layout.md). Layout now includes added structure elements including sections, section headers, and paragraphs. This update enables finer grain document segmentation scenarios. For a complete list of structure elements identified, _see_ [enhanced structure](../prebuilt/layout.md#data-extraction).
  * [**Custom neural model tabular fields support**](../train/custom-neural.md). Custom document models now support tabular fields. Tabular fields by default are also multi page. To learn more about tabular fields in custom neural models, _see_ [tabular fields](../train/custom-neural.md#tabular-fields).
  * [**Custom template model tabular fields support for cross page tables**](../train/custom-template.md). Custom form models now support tabular fields across pages. To learn more about tabular fields in custom template models, _see_ [tabular fields](../train/custom-neural.md#tabular-fields).
  * [**Invoice model output now includes general document key-value pairs**](../prebuilt/invoice.md). Where invoices contain required fields beyond the fields included in the prebuilt model, the general document model supplements the output with key-value pairs. _See_ [key value pairs](../prebuilt/invoice.md#key-value-pairs).
  * [**Invoice language expansion**](../prebuilt/invoice.md). The invoice model includes expanded language support. _See_ [supported languages](../prebuilt/invoice.md#supported-languages-and-locales).
  * [**Prebuilt business card**](../prebuilt/business-card.md) now includes Japanese language support. _See_ [supported languages](../prebuilt/business-card.md#supported-languages-and-locales).
  * [**Prebuilt ID document model**](../prebuilt/id-document.md). The ID document model now extracts DateOfIssue, Height, Weight, EyeColor, HairColor, and DocumentDiscriminator from US driver's licenses. _See_ [field extraction](../prebuilt/id-document.md).
  * [**Read model now supports common Microsoft Office document types**](../prebuilt/read.md). Document types like Word (docx), Excel (xlsx), and PowerPoint (pptx) are now supported with the Read API. See [Read data extraction](../prebuilt/read.md#data-extraction).

---

## February 2022

### [**C#**](#tab/csharp)

**Version 4.0.0-beta.3 (2022-02-10)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/formrecognizer/Azure.AI.FormRecognizer/CHANGELOG.md#400-beta3-2022-02-10)

 [**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.FormRecognizer/4.0.0-beta.3)

 [**SDK reference documentation**](/dotnet/api/azure.ai.formrecognizer.documentanalysis?view=azure-dotnet-preview&preserve-view=true)

### [**Java**](#tab/java)

**Version 4.0.0-beta.4 (2022-02-10)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md#400-beta4-2022-02-10)

 [**Package (Maven)**](https://search.maven.org/artifact/com.azure/azure-ai-formrecognizer/4.0.0-beta.4/jar)

 [**SDK reference documentation**](/java/api/overview/azure/ai-formrecognizer-readme?view=azure-java-preview&preserve-view=true)

### [**JavaScript**](#tab/javascript)

**Version 4.0.0-beta.3 (2022-02-10)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/formrecognizer/ai-form-recognizer/CHANGELOG.md#400-beta3-2022-02-10)

 [**Package (npm)**](https://www.npmjs.com/package/@azure/ai-form-recognizer/v/4.0.0-beta.3)

 [**SDK reference documentation**](/javascript/api/@azure/ai-form-recognizer/?view=azure-node-preview&preserve-view=true)

### [Python](#tab/python)

**Version 3.2.0b3 (2022-02-10)**

 [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-formrecognizer_3.2.0b3/sdk/formrecognizer/azure-ai-formrecognizer/CHANGELOG.md#320b3-2022-02-10)

 [**Package (PyPI)**](https://pypi.org/project/azure-ai-formrecognizer/3.2.0b3/)

 [**SDK reference documentation**](/python/api/azure-ai-formrecognizer/azure.ai.formrecognizer?view=azure-python-preview&preserve-view=true)

---

* Document Intelligence v3.0 preview release introduces several new features, capabilities, and enhancements:

  * [**Custom neural model**](../train/custom-neural.md) or custom document model is a new custom model to extract text and selection marks from structured forms, semi-structured and **unstructured documents**.
  * [**W-2 prebuilt model**](../prebuilt/tax-document.md) is a new prebuilt model to extract fields from W-2 forms for tax reporting and income verification scenarios.
  * [**Read**](../prebuilt/read.md) API extracts printed text lines, words, text locations, detected languages, and handwritten text, if detected.
  * [**General document**](../prebuilt/general-document.md) pretrained model is now updated to support selection marks in addition to API  text, tables, structure, and key-value pairs from forms and documents.
  * [**Invoice API**](../prebuilt/invoice.md#supported-languages-and-locales) Invoice prebuilt model expands support to Spanish invoices.
  * [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com) adds new demos for Read, W2, Hotel receipt samples, and support for training the new custom neural models.
  * [**Language Expansion**](../language-support/prebuilt.md) Document Intelligence Read, Layout, and Custom Form add support for 42 new languages including Arabic, Hindi, and other languages using Arabic and Devanagari scripts to expand the coverage to 164 languages. Handwritten language support expands to Japanese and Korean.

* Get started with the new v3.0 preview API.

* Document Intelligence model data extraction:

  | **Model**   | **Text extraction** |**Key-Value pairs** |**Selection Marks**   | **Tables** |**Signatures**|
  | --- | :---: |:---:| :---: | :---: |:---: |
  |Read | ✓  |   |   |   |   |
  |General document  | ✓  |  ✓ | ✓  | ✓  |   |
  | Layout  | ✓  |   | ✓  | ✓  |   |
  | Invoice  | ✓ | ✓  | ✓  | ✓ ||
  |Receipt  | ✓  |   ✓ |   |  |✓|
  | ID document | ✓  |   ✓  |   |   ||
  | Business card    | ✓  |   ✓ |   |   ||
  | Custom template  |✓  |  ✓ | ✓  | ✓  |  ✓ |
  | Custom neural    |✓  |  ✓ | ✓  | ✓  |   |

* Document Intelligence SDK beta preview release includes the following updates:

  * [Custom Document models and modes](../train/custom-model.md):
    * [Custom template](../train/custom-template.md) (formerly custom form).
    * [Custom neural](../train/custom-neural.md).
    * [Custom model—build mode](../train/custom-model.md#build-mode).

  * [W-2 prebuilt model](../prebuilt/tax-document.md) (../prebuilt-tax.us.w2).
  * [Read prebuilt model](../prebuilt/read.md) (../prebuilt-read).
  * [Invoice prebuilt model (Spanish)](../prebuilt/invoice.md#supported-languages-and-locales) (../prebuilt-invoice).

---