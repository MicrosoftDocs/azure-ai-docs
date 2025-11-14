---
title: "Document translation REST API reference guide"
titleSuffix: Foundry Tools
description: View a list of with links to the Document translation REST APIs.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Document translation operations

Reference</br>
Feature: **Azure Translator → Document translation**</br>

Document translation is a cloud-based feature of the Azure Translator and is part of the Foundry Tool family of REST APIs. The Batch Document translation API translates documents across all [supported languages and dialects](../../language-support.md) while preserving document structure and data format. The available methods are listed in the following tables:

## API Version: **2024-05-01**

> [!NOTE]
>
> * The current version is backward compatible with the legacy version.
>
> * With this current version and later versions, the `get supported storage sources` method is no longer supported. The Translator only supports Azure Blob storage.

| Request|Method| Description|API path|
|---------|:-------:|-------|-----|
|***Single*** |***Synchronous***|***Document***|***Translation***|
|[**Translate document**](translate-document.md)|POST|Synchronously translate a single document.|`{document-translation-endpoint}/translator/document:translate?targetLanguage={target_language}&api-version={date}`|
|||||
|***Batch***|***Asynchronous***|***Documents***| ***Translation***|
|[**Start translation**](start-translation.md)|POST| Start a batch document translation job.|`{document-translation-endpoint}/translator/document/batches?api-version={date}`|
|[**Get status for all translation jobs**](get-translations-status.md)|GET| Request a list and the status of translation jobs submitted by the user.|`{document-translation-endpoint}/translator/document/batches?api-version={date}`|
|[**Get status for a specific translation job**](get-translation-status.md) |GET| Request a summary of the status for a specific translation job. The response includes the overall job status and the status for documents that are being translated as part of that job.|`{document-translation-endpoint}/translator/document/batches/{id}?api-version={date}`|
|[**Get status for all documents**](get-documents-status.md)|GET|Request the status of all documents in a translation job.|`{document-translation-endpoint}/translator/document/batches/{id}/documents?api-version={date}`|
|[**Get status for a specific document**](get-document-status.md)|GET| Request the status for a specific document in a job. |`{document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}?api-version={date}`|
|[**Cancel translation**](cancel-translation.md)|DELETE| Cancel a document translation job that's currently processing or queued.|`{document-translation-endpoint}/translator/document/batches/{id}?api-version={date}`|
|[**Get supported document formats**](get-supported-document-formats.md)|GET| Request a list of supported document formats.|`{document-translation-endpoint}/translator/document/formats?api-version={date}&type=document`|
|[**Get supported glossary formats**](get-supported-glossary-formats.md)|GET|Request a list of supported glossary formats.|`{document-translation-endpoint}/translator/document/formats?api-version={date}&type=glossary`|

## Legacy

> [!NOTE]
>
> * The legacy version is backward compatible with the current version. You can use either version's operations to translate documents.
> * We recommend migrating your applications to the newest version to benefit from an enhanced experience and advanced capabilities.
>

| Request|Method| Description|API path|
|---------|:-------|-------|-----|
|***Single*** |***Synchronous***|***Document***|***Translation***|
|[**Translate document**](translate-document.md)|POST|Synchronously translate a single document.|`{document-translation-endpoint}/translator/document:translate?sourceLanguage={source language}&targetLanguage={target language}&api-version=2024-05-01" -H "Ocp-Apim-Subscription-Key:{your-key}"  -F "document={path-to-your-document-with-file-extension};type={ContentType}/{file-extension}" -F "glossary={path-to-your-glossary-with-file-extension};type={ContentType}/{file-extension}" -o "{path-to-output-file}"`|
|||||
|***Batch***|***Asynchronous***|***Documents***| ***Translation***|
|[**Start translation**](start-translation.md)|POST|Start a batch document translation job.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches`|
|[**Get status for all translation jobs**](get-translations-status.md)|GET|Request a list and the status of translation jobs submitted by the user.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches`|
|[**Get status for a specific translation job**](get-translation-status.md)|GET| Request a summary of the status for a specific translation job. The response includes the overall job status and the status for documents that are being translated as part of that job.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches/{id}`|
|[**Get status for all documents**](get-documents-status.md)|GET| Request the status for a specific document in a job.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches/{id}/documents`|
|[**Get status for a specific document**](get-document-status.md)|GET| Request the status for a specific document in a job.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches/{id}/documents/{documentId}`|
|[**Cancel translation**](cancel-translation.md)|DELETE| Cancel a document translation job that's currently processing or queued.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/batches/{id}`|
| [**Get supported document formats**](get-supported-document-formats.md)|GET| Request a list of supported document formats.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/documents/formats`|
|[**Get supported glossary formats**](get-supported-glossary-formats.md)|GET|Request a list of supported glossary formats.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/glossaries/formats`|
|[**Get supported storage sources**](get-supported-storage-sources.md)|GET|Request a list of supported storage sources/options. Currently, Translator only supports Azure Blob storage.|`{document-translation-endpoint}.cognitiveservices.azure.com/translator/text/batch/v1.1/storagesources`|

> [!div class="nextstepaction"]
> [Explore our client libraries and SDKs for C# and Python programming languages.](../quickstarts/client-library-sdks.md).
