---
title: What is Azure Translator document translation?
titleSuffix: Foundry Tools
description: Learn about Azure Translator document translation for batch and single-file translation while preserving document structure and formatting.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 06/02/2026
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
<!-- markdownlint-disable MD025 -->

# What is Azure Translator document translation?

Document translation (**2026-03-01** GA) is a cloud-based feature of Azure Translator and part of the Foundry Tools family of REST APIs. It provides:

* **Translation** across all [supported languages and dialects](../../language-support.md).
* **Preservation** of the original document structure and data format.
* **Neural machine translation (NMT) engine support** for standard translations (default).
* **Large language model (LLM) support** for higher-quality, context-aware translations (optional).

The Document Translation API supports two translation processes:

* **[Asynchronous batch translation](#key-features):** Translate multiple documents or large files in parallel. Upload documents to Blob Storage, submit a batch job, poll for status, then download translated output from your target container. Requires an Azure Blob Storage account with source and target containers. For a full walkthrough, see [Quickstart: asynchronous document translation](quickstarts/asynchronous.md) and [End-to-end batch translation workflow](end-to-end-batch-workflow.md).

* **[Synchronous single-file translation](#key-features):** POST a single document and receive the translated output directly in the response. No Azure Blob Storage required. For a full walkthrough, see [Quickstart: synchronous document translation](quickstarts/synchronous.md).

## What's new in version 2026-03-01

API version **2026-03-01** introduces the following capabilities for Document Translation:

* **Large language model (LLM) selection (public preview)**: By default, Document Translation uses NMT models. With this version, you can optionally select an LLM supported model, for example, GPT-5.4, based on quality, cost, and other factors. LLM-based translation requires a Microsoft Foundry resource. For more information, see [Configure Azure resources](../../how-to/create-translator-resource.md).

* **Image translation**: Translate text within standalone image files (`.jpeg`, `.png`, `.bmp`, `.webp`), with translated content rendered back into the image.

* **PDF translation with Azure Document Intelligence (batch only)**: Translate PDF files using Azure Document Intelligence to preserve layout and structure in the translated output.

* **Image translation in Office documents (batch only)**: Translate text embedded in images within Word (`.docx`) and PowerPoint (`.pptx`) documents while preserving overall document structure.

## Before you begin

Prerequisites differ by translation method:

* **Asynchronous batch translation**: Requires an Azure Blob Storage account and storage authorization (SAS tokens or managed identity).
* **Synchronous single-file translation**: Requires only a Translator resource with a custom domain endpoint.

For the full prerequisites list, see [Prerequisites and setup](prerequisites.md).

## Key features

Document Translation supports different features for each translation method. Select the tab for your scenario.

### [**Asynchronous (batch)**](#tab/async)

| Feature | Description |
| --- | --- |
| **Translate large files** | Translate whole documents asynchronously. |
| **Translate numerous files** | Translate multiple files across all supported languages and dialects while preserving document structure and data format. |
| **Translate image file formats** 🆕 | &bull; [Translate text within an image while maintaining the original design and layout](../latest/rest-api/translate-asynchronous.md).<br>&bull; **Supported formats**: `.jpeg`, `.png`, `.bmp`, `.webp`<br>&bull; **Pricing**: Calculated on a per-image basis. For more information, see [Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator). |
| [**Translate image text in Word documents (.docx) and PowerPoint files (.pptx)** 🆕](../how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-documents-docx-and-powerpoint-files-pptx). | This feature is available with the [batch document translation](../how-to-guides/use-rest-api-programmatically.md#translate-images-in-word-documents-docx-and-powerpoint-files-pptx) API for `.docx` and `.pptx` file formats. |
| **Preserve source file presentation** | Translate files while preserving the original layout and format. |
| **Apply custom translation** | Translate documents using general and [custom translation](../../custom-translator/concepts/customization.md#azure-translator-in-foundry-tools-custom-translator) models. |
| **Apply custom glossaries** | Translate documents using custom glossaries. |
| **Automatically detect document language** | Let the Document translation service determine the language of the document. |
| **Translate documents with content in multiple languages** | Use the autodetect feature to translate documents with content in multiple languages into your target language. |

### [**Synchronous**](#tab/sync)

|Feature | Description |
| ---------| -------------|
|**Translate single-page files**| The synchronous request accepts only a single document as input.|
|**Preserve source file presentation**| Translate files while preserving the original layout and format.|
|**Apply custom translation**| Translate documents using general and [custom translation](../../custom-translator/concepts/customization.md#azure-translator-in-foundry-tools-custom-translator) models.|
|**Apply custom glossaries**|Translate documents using custom glossaries. For guidance, see [Use glossaries with Document translation](../how-to-guides/create-use-glossaries.md).|
|**Single language translation**|Translate to and from one [supported language](../../language-support.md).|
|**Automatically detect document language**|Let the Document translation service determine the language of the document.|

---

## Language support

For the full list of languages supported for document translation features, including LLM-based translation, see [Language support](../../language-support.md).

### LLM data processing

When you deploy an LLM, the configuration you choose — global, data zone, or regional — determines where your data is processed. Your selections during resource setup define the geographical boundaries for model processing.

## Development options

Add document translation to your projects and applications using the following development options.

> [!NOTE]
> Foundry portal currently supports synchronous (single-file) document translation only. Use the REST API or client libraries for asynchronous batch document translation.

### [**Asynchronous (batch)**](#tab/async)

Use asynchronous workflows to translate multiple documents and large files.

|Development option|Description|
|---|---|
|**REST API**|The [REST API](rest-api/guide-overview.md) is a language agnostic interface that enables you to create HTTP requests and authorization headers to translate documents.|
|**Client libraries (SDKs)**|The [client-library (SDKs)](../quickstarts/client-library-sdks.md) are language-specific classes, objects, methods, and code that you can quickly use by adding a reference in your project. Currently Document translation has programming language support for [C#/.NET](/dotnet/api/azure.ai.translation.document?view=azure-dotnet&preserve-view=true) and [Python](https://azuresdkdocs.z19.web.core.windows.net/python/azure-ai-translation-document/latest/azure.ai.translation.document.html).|

### [**Synchronous**](#tab/sync)

Use synchronous document translation to translate a single file and return the translated file in the response.

|Development option|Description|
|---|---|
|**Foundry portal (classic)**|Try synchronous document translation in the Translator playground. In the classic portal, upload your own document and translate it end-to-end. To open the Translator playground, go to [Foundry portal](https://ai.azure.com/), ensure **New Foundry** is not selected, then select **Playgrounds** > **Translator**.|
|**Foundry portal (new)**|The new Foundry portal uses a sample document and translates only into a predefined set of languages. Doesn't support customer-provided documents. For more information, see [What is Microsoft Foundry?](../../../../foundry/what-is-foundry.md).|
|**REST API**|Integrate synchronous document translation into your applications by using the [REST API](rest-api/guide-overview.md#synchronous-operations).|
|**Client libraries (SDKs)**|Integrate translation capabilities into your applications by using the [client libraries (SDKs)](../quickstarts/client-library-sdks.md).|
|**Docker container**|&bull; To use the Translator container, complete and submit the [**Gated Services application**](https://aka.ms/csgate-translator) online request form for approval to access the container.<br>&bull; The [**Translator container image**](https://mcr.microsoft.com/product/azure-cognitive-services/translator/text-translation/about) supports limited features compared to cloud offerings.<br>For more information, see [Container: Translate Documents](../../containers/translate-document-parameters.md).|

---

## Supported document and glossary formats

Document translation supports a broad range of file formats for both translation input and glossary files. Supported formats differ slightly between asynchronous batch and synchronous translation.

To query supported formats at runtime:

* **Document formats**: Use the [Get supported document formats](rest-api/get-supported-document-formats.md) API.
* **Glossary formats**: Use the [Get supported glossary formats](rest-api/get-supported-glossary-formats.md) `[TO VERIFY]` API.

For a complete list of supported formats by method, see [Supported document formats](rest-api/guide-overview.md).

## Document translation request limits

Document translation enforces limits on request size, document count, file size, and concurrent operations. Understanding these limits helps you design batch jobs and avoid throttling errors. For detailed information, see [Document translation request limits](../../service-limits.md#document-translation).

## Document translation data residency

Data residency determines where your document content is processed and temporarily stored during translation. For document translation, the processing location is determined by the Azure region where your Translator resource was created. The following table maps resource regions to their corresponding request processing data centers:

✔️ Feature: **Document translation**
✔️ Service endpoint: **Custom domain: `https://<your-resource-name>.cognitiveservices.azure.com`**

|Resource created region| Request processing data center |
|----------------------------------|-----------------------|
|**Global**|Closest available data center.|
|**Americas**|East US 2 &bull; West US 2|
|**Asia Pacific**| Japan East &bull; Southeast Asia|
|**Europe (except Switzerland)**| France Central &bull; West Europe|
|**Switzerland**|Switzerland North &bull; Switzerland West|

## Service limits and troubleshooting

If you encounter unexpected behavior, errors, or performance issues, the following resources can help you diagnose and resolve them:

* **Service limits:** See [Document translation request limits](../../service-limits.md#document-translation).

* **Translation errors and known issues:** See [Known issues](../../reference/known-issues.md).

## Pricing

Pricing depends on whether you use NMT-based or LLM-based translation. The two models have different billing units.

* Document translations using **NMT models** are billed by the number of characters or images in the source document. For more information, see [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).

* Document translations using **LLMs** are charged by the number of input and output tokens processed. For more information, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Related content

* [Quickstart: asynchronous document translation](quickstarts/asynchronous.md)
* [Quickstart: synchronous document translation](quickstarts/synchronous.md)
* [End-to-end batch translation workflow](end-to-end-batch-workflow.md)

