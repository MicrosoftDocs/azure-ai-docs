---
title: Frequently asked questions - Azure AI Translator Document translation
titleSuffix: Azure AI services
description: Get answers to Azure AI Translator Document translation frequently asked questions.
author: laujan
manager: nitinme

ms.service: azure-ai-translator
ms.topic: conceptual
ms.date: 06/19/2025
ms.author: lajanuar
---

<!-- markdownlint-disable MD001 -->

# Answers to frequently asked questions

## Azure AI Translator Document translation: FAQ

#### Should I specify the source language in a request?

If the language of the content in the source document is known, we recommend that you specify the source language in the request to get a better translation. If the document has content in multiple languages or the language is unknown, then don't specify the source language in the request. Azure AI Translator Document translation automatically identifies language for each text segment and translates.

#### To what extent are document layout, structure, formatting, and font style retained?

* PDF documents generated from digital file formats (also known as "native" PDFs) provide optimal output.

* Printed documents scanned into an electronic format (scanned PDF files) can result in loss of the original formatting, layout, and style.

* The translation of text from one language to another can alter its length. This variation can affect the layout, causing the text to reflow or shift across different pages.

* Various factors influence the preservation and retention of font style. For instance, some fonts aren't available in both the source and target languages. Typically, the same font style, or an optimally suited alternative, is applied to the target language to maintain formatting that most closely resembles the original source text.

#### Can the text in an image within a document be translated?

Yes. Document translation feature supports [translating text embedded in images within documents](how-to-guides/use-rest-api-programmatically.md#translate-text-embedded-within-images-in-documents-) as an optional capability.

#### Can Azure AI Translator Document translation translate content from scanned documents?

Yes. Azure AI Translator Document translation translates content from _scanned PDF_ documents.

#### Can encrypted or password-protected documents be translated?

No. The service can't translate encrypted or password-protected documents. If your scanned or text-embedded PDFs are password-locked, you must remove the lock before submission.

#### If I'm using managed identities, do I also need a SAS token URL?

No. Don't include SAS token-appended URLs. Managed identities eliminate the need for you to include shared access signature tokens (SAS) with your HTTP requests.

#### Which PDF format renders the best results?

PDF documents generated from digital file formats (also known as "native" PDFs) provide optimal output. Scanned PDFs are images of printed documents scanned into an electronic format. Translating scanned PDF files can result in loss of the original formatting, layout, and style, and affect the quality of the translation.

#### Can I learn more about single document synchronous translation?

Yes.

* For more information, *see* [Synchronous document translation](overview.md#synchronous-translation)
* To view `synchronous document translation` sample code in our GitHub repository, *see* [.NET/C#](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/translation/Azure.AI.Translation.Document/samples/Sample5_SynchronousTranslation.md); [Python](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-translation-document_1.0.0/sdk/translation/azure-ai-translation-document/samples/sample_begin_translation.py); [REST API](quickstarts/rest-api.md#synchronously-translate-a-single-document-post)
