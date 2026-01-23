---
title: What is document translation?
titlesuffix: Foundry Tools
description: Learn about Azure Translator document translation for batch and single-file translation while preserving document structure and formatting.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 01/21/2026
ms.author: lajanuar
ms.custom: references_regions, pilot-ai-workflow-jan-2026
recommendations: false
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD049 -->
<!-- markdownlint-disable MD001 -->

# What is Azure Translator document translation in Foundry Tools?

Document translation is a cloud-based machine translation feature of [Azure Translator](../overview.md). You can translate multiple and complex documents across all [supported languages and dialects](../../language-support.md) while preserving original document structure and data format. The Document translation API supports two translation processes:

* [Asynchronous batch translation](#key-features) supports the processing of multiple documents and large files. The batch translation process requires an Azure Blob storage account with storage containers for your source and translated documents.

* [Synchronous single file](#key-features) supports the processing of single file translations. The file translation process doesn't require an Azure Blob storage account. The final response contains the translated document and is returned directly to the calling client.

## Prerequisites

### Asynchronous batch translation prerequisites

Before you start, you need:

* An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A Translator resource. For resource creation and endpoint/key retrieval steps, see [Use Document translation APIs programmatically](how-to-guides/use-rest-api-programmatically.md).
* An Azure Blob Storage account with source and target containers. For setup guidance, see [Create Azure Blob Storage containers](how-to-guides/use-rest-api-programmatically.md#create-azure-blob-storage-containers).
* A way to authorize access to your storage URLs:
	* [Shared access signature (SAS) tokens](how-to-guides/create-sas-tokens.md), or
	* [Managed identities for Document translation](how-to-guides/create-use-managed-identities.md).

### Synchronous translation prerequisites

Before you start, you need:

* An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A Translator resource with a custom domain endpoint. For setup and endpoint/key retrieval, see [Use Document translation APIs programmatically](how-to-guides/use-rest-api-programmatically.md).

> [!TIP]
> Store subscription keys in a secure location such as [Azure Key Vault](/azure/key-vault/general/overview), and avoid putting keys in source control.

## Key features

### [Asynchronous (batch)](#tab/async)

|Feature | Description |
| ---------| -------------|
|**Translate large files**| Translate whole documents asynchronously.|
|**Translate numerous files**|Translate multiple files across all supported languages and dialects while preserving document structure and data format.|
|**Translate image file formats (preview)** 🆕| &bullet; [Translate text within an image while maintaining the original design and layout](reference/start-batch-translation.md#translate-image-files).<br>&bullet; **Supported formats**: `.jpeg`, `.png`, `.bmp`, `.webp`<br>&bullet; **Pricing**: Calculated on a per image basis. For more information, *see* [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator)|
|[**Translate image text in Word document files (.docx)**](how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-document-files-docx).| This feature is available with the [batch document translation](how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-document-files-docx) API for `.docx` file format.|
|**Preserve source file presentation**| Translate files while preserving the original layout and format.|
|**Apply custom translation**| Translate documents using general and [custom translation](../custom-translator/concepts/customization.md#azure-translator-in-foundry-tools-custom-translator) models.|
|**Apply custom glossaries**|Translate documents using custom glossaries.|
|**Automatically detect document language**|Let the Document translation service determine the language of the document.|
|**Translate documents with content in multiple languages**|Use the autodetect feature to translate documents with content in multiple languages into your target language.|

### [Synchronous](#tab/sync)

|Feature | Description |
| ---------| -------------|
|**Translate single-page files**| The synchronous request accepts only a single document as input.|
|**Preserve source file presentation**| Translate files while preserving the original layout and format.|
|**Apply custom translation**| Translate documents using general and [custom translation](../custom-translator/concepts/customization.md#azure-translator-in-foundry-tools-custom-translator) models.|
|**Apply custom glossaries**|Translate documents using custom glossaries. For guidance, see [Use glossaries with Document translation](how-to-guides/create-use-glossaries.md).|
|**Single language translation**|Translate to and from one [supported language](../language-support.md).|
|**Automatically detect document language**|Let the Document translation service determine the language of the document.|

---

## How document translation works

### Asynchronous (batch)

1. Upload source documents to your source container.
2. Submit a batch translation request.
3. Monitor job and document status.
4. Download translated documents from your target container.

For detailed request/response flows, see the [Document translation REST API reference guide](reference/rest-api-guide.md).

### Synchronous

1. Send a request that includes one document (and an optional glossary).
2. Receive the translated document in the response.

For request details and examples, see [Synchronous document translation](reference/translate-document.md).

## Development options

Add document translation to your projects and applications using the following development options.

> [!NOTE]
> Microsoft Foundry currently supports synchronous (single-file) document translation only. Use the REST API or client libraries for asynchronous batch document translation.

### [Asynchronous (batch)](#tab/async)

Use asynchronous workflows to translate multiple documents and large files.

|Development option|Description|
|---|---|
|**REST API**|The [REST API](reference/rest-api-guide.md) is a language agnostic interface that enables you to create HTTP requests and authorization headers to translate documents.|
|**Client libraries (SDKs)**|The [client-library (SDKs)](quickstarts/client-library-sdks.md) are language-specific classes, objects, methods, and code that you can quickly use by adding a reference in your project. Currently Document translation has programming language support for [C#/.NET](/dotnet/api/azure.ai.translation.document?view=azure-dotnet&preserve-view=true) and [Python](https://azuresdkdocs.z19.web.core.windows.net/python/azure-ai-translation-document/latest/azure.ai.translation.document.html).|

### [Synchronous](#tab/sync)

Use synchronous document translation to translate a single file and return the translated file in the response.

|Development option|Description|
|---|---|
|**Microsoft Foundry (classic)**|Use Microsoft Foundry to try synchronous document translation in the Translator playground. In the **Classic** portal, upload your own document and translate the document end-to-end. To open the Translator playground, go to [Microsoft Foundry](https://ai.azure.com/), ensure **New Foundry** is not selected, then **Playgrounds** > **Translator**.|
|**Microsoft Foundry (new)**|The **New** Microsoft Foundry portal uses a sample document and translates only into a predefined set of languages. Does not support customer-provided documents. For more information, see [What is Microsoft Foundry?](../../../ai-foundry/what-is-foundry.md).|
|**REST API**|Integrate synchronous document translation into your applications using the [REST API](reference/translate-document.md).|
|**Client libraries (SDKs)**|Get started integrating translation capabilities into your applications using the [client libraries (SDKs)](quickstarts/client-library-sdks.md).|
| **Docker container** | &bullet; To use the Translator container, you must complete and submit the [**Foundry Tools application for Gated Services**](https://aka.ms/csgate-translator) online request form for approval for access to the container.<br>&bullet; The [**Translator container image**](https://mcr.microsoft.com/product/azure-cognitive-services/translator/text-translation/about) supports limited features compared to cloud offerings.<br>For more information, *see* [Container: Translate Documents](../containers/translate-document-parameters.md).|

---

## Supported document and glossary formats

### [Asynchronous (batch)](#tab/async)

### Batch document supported formats

The [Get supported document formats method](reference/get-supported-document-formats.md) returns a list of document formats supported by the Document translation service. The list includes common file extensions and content types.

| File type| File extension|Description|
|---|---|---|
|Adobe PDF|`pdf`|Portable document file format. Document translation uses optical character recognition (OCR) technology to extract and translate text in scanned PDF document while retaining the original layout.|
|Comma-Separated Values |`csv`| A comma-delimited raw-data file used by spreadsheet programs.|
|HTML|`html`, `htm`|Hyper Text Markup Language.|
|Image (2025-12-01-preview)|`.jpeg`, `.png`, `.bmp`, `.webp`|Files that store digital image data.|
|OpenDocument Presentation|`odp`|An open-source presentation file.|
|OpenDocument Spreadsheet|`ods`|An open-source spreadsheet file.|
|OpenDocument Text|`odt`|An open-source text document file.|
|Markdown| `markdown`, `mdown`, `mkdn`, `md`, `mkd`, `mdwn`, `mdtxt`, `mdtext`, `rmd`| A lightweight markup language for creating formatted text.|
|M&#8203;HTML|`mhtml`, `mht`| A web page archive format used to combine HTML code and its companion resources.|
|Microsoft Excel|`xls`, `xlsx`|A spreadsheet file for data analysis and documentation.|
|Microsoft Outlook|`msg`|An email message created or saved within Microsoft Outlook.|
|Microsoft PowerPoint|`ppt`, `pptx`| A presentation file used to display content in a slideshow format.|
|Microsoft Word|`doc`, `docx`| A text document file.|
|Rich text format|`rtf`|A text document containing formatting.|
|Tab separated values/TAB|`tsv`/`tab`| A tab-delimited raw-data file used by spreadsheet programs.|
|Text|`txt`| An unformatted text document.|
|XLIFF|`xlf`|A parallel document format used in translation and localization.|

### Batch Legacy file types

Source file types are preserved during the document translation with the following **exceptions**:

| Source file extension | Translated file extension|
| --- | --- |
| .doc, .odt, .rtf, | .docx |
| .xls, .ods | .xlsx |
| .ppt, .odp | .pptx |

### Batch glossary supported formats

Document translation supports the following glossary file types:

| File type| File extension|Description|
|---|---|--|
|Comma-Separated Values| `csv` |A comma-delimited raw-data file used by spreadsheet programs.|
|XLIFF|`xlf`|A parallel document format used in translation and localization.|
|Tab-Separated Values/TAB|`tsv`, `tab`| A tab-delimited raw-data file used by spreadsheet programs.|

### [Synchronous](#tab/sync)

### Synchronous document supported formats

|File type|File extension| Content type|Description|
|---|---|--|---|
|**Plain Text**|`.txt`|`text/plain`| An unformatted text document.|
|**Tab Separated Values**|`.tsv`<br> `.tab`|`text/tab-separated-values`|A text file format that uses tabs to separate values and newlines to separate records.|
|**Comma Separated Values**|`.csv`|`text/csv`|A text file format that uses commas as a delimiter between values.|
|**HyperText Markup Language**|`.html`<br> `.htm`|`text/html`|HTML is a standard markup language used to structure web pages and content.|
|**M&#8203;HTML**|`.mhtml`<br> `.mht`|`message/rfc822`<br>`application/x-mimearchive`<br>`multipart/related`|A web page archive file format.|
|**Microsoft PowerPoint**|`.pptx`|`application/vnd.openxmlformats-officedocument.presentationml.presentation` |An XML-based file format used for PowerPoint slideshow presentations.|
|**Microsoft Excel**|`.xlsx`| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`| An XML-based file format used for Excel spreadsheets.|
|**Microsoft Word**|`.docx`| `application/vnd.openxmlformats-officedocument.wordprocessingml.document`|An XML-based file format used for Word documents.|
|**Microsoft Outlook**|`.msg`|`application/vnd.ms-outlook`|A file format used for stored Outlook mail message objects.|
|**XLIFF**|`.xlf`|`application/xliff+xml`|A standardized XML-based file format widely used in translation and localization software processing.|

### Synchronous glossary supported formats

Document translation supports the following glossary file types:

| File type| File extension|Description|
|---|---|--|
|**Comma-Separated Values**| `csv` |A comma-delimited raw-data file used by spreadsheet programs.|
|**XLIFF**|`xlf`|An XML-based format designed to standardize how data is passed during the localization process.|
|**TabSeparatedValues**|`tsv`, `tab`| A tab-delimited raw-data file used by spreadsheet programs.|

---

## Document translation request limits

For detailed information regarding Azure Translator request limits, *see* [**Document translation request limits**](../service-limits.md#document-translation).

## Document translation data residency

Document translation data residency depends on the Azure region where your Translator resource was created:

✔️ Feature: **Document translation**</br>
✔️ Service endpoint: **Custom domain: `https://<your-resource-name>.cognitiveservices.azure.com`**

|Resource created region| Request processing data center |
|----------------------------------|-----------------------|
|**Global**|Closest available data center.|
|**Americas**|East US 2 &bull; West US 2|
|**Asia Pacific**| Japan East &bull; Southeast Asia|
|**Europe (except Switzerland)**| France Central &bull; West Europe|
|**Switzerland**|Switzerland North &bull; Switzerland West|

## Troubleshooting

If you run into issues, use these checks to unblock yourself.

### Batch translation

* If translated files don't appear in the target container, check job status using [Get status for a specific translation job](reference/get-translation-status.md) and document status using [Get status for a specific document](reference/get-document-status.md).
* If the service can't read from or write to your storage containers, confirm storage authorization:
	* If you use SAS tokens, see [Create shared access signature (SAS) tokens for storage containers and blobs](how-to-guides/create-sas-tokens.md).
	* If you use managed identities, see [Create and use managed identities](how-to-guides/create-use-managed-identities.md).
* If a job fails due to unsupported inputs, confirm the format using [Get supported document formats](reference/get-supported-document-formats.md).

### Synchronous translation

* If the request fails due to invalid parameters or unsupported file types, review the required parameters and supported formats in [Synchronous document translation](reference/translate-document.md).
* If you hit rate limits, see [Document translation request limits](../service-limits.md#document-translation).

## Next steps

In the quickstart, you learn how to get started with batch and synchronous translation.

> [!div class="nextstepaction"]
> [Get started with Document translation REST APIs](quickstarts/rest-api.md)

> [!div class="nextstepaction"]
> [Use Document translation APIs programmatically](how-to-guides/use-rest-api-programmatically.md)

> [!div class="nextstepaction"]
> [Use glossaries with Document translation](how-to-guides/create-use-glossaries.md)

> [!div class="nextstepaction"]
> [See the Document translation REST API reference](reference/rest-api-guide.md)
