---
title: Native document support for Azure Language in Foundry Tools (preview)
titleSuffix: Foundry Tools
description: How to use native document with Azure Language Personally Identifiable Information and Summarization capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
---
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD049 -->
<!-- markdownlint-disable MD001 -->

# Native document support for Azure Language in Foundry Tools (preview)

> [!IMPORTANT]
>
> * Azure Language in Foundry Tools public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change, before General Availability (GA), based on user feedback.

Language is a cloud-based service that applies Natural Language Processing (NLP) features to text-based data. The native document support capability enables you to send API requests asynchronously, using an HTTP POST request body to send your data and HTTP GET request query string to retrieve the status results. Your processed documents are located in your Azure Blob Storage target container.

A native document refers to the file format used to create the original document such as Microsoft Word (docx) or a portable document file (pdf). Native document support eliminates the need for text preprocessing before using Language resource capabilities. Currently, native document support is available for the following capabilities:

* [Personally Identifiable Information (PII)](../personally-identifiable-information/overview.md). The PII detection feature can identify, categorize, and redact sensitive information in unstructured text. The `PiiEntityRecognition` API supports native document processing.

* [Document summarization](../summarization/overview.md). Document summarization uses natural language processing to generate extractive (salient sentence extraction) or abstractive (contextual word extraction) summaries for documents. Both `AbstractiveSummarization` and `ExtractiveSummarization` APIs support native document processing.

## Supported document formats

 Applications use native file formats to create, save, or open native documents. Currently **PII** and **Document summarization** capabilities supports the following native document formats:

|File type|File extension|Description|
|---------|--------------|-----------|
|Text| `.txt`|An unformatted text document.|
|Adobe PDF| `.pdf`|A portable document file formatted document.|
|Microsoft Word| `.docx`|A Microsoft Word document file.|

## Input guidelines

***Supported file formats***

|Type|support and limitations|
|---|---|
|**PDFs**| Fully scanned PDFs aren't supported.|
|**Text within images**| Digital images with embedded text aren't supported.|
|**Digital tables**| Tables in scanned documents aren't supported.|

***Document Size***

|Attribute|Input limit|
|---|---|
|**Total number of documents per request** |**≤ 20**|
|**Total content size per request**| **≤ 10 MB**|

## Request headers and parameters

|parameter  |Description  |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your Language resource endpoint for accessing the API.        |
|`--header Content-Type: application/json`     | The content type for sending JSON data.          |
|`--header "Ocp-Apim-Subscription-Key:<key>`    | Specifies Azure Language resource key for accessing the API.        |
|`-data`     | The JSON file containing the data you want to pass with your request.         |

## Related content

> [!div class="nextstepaction"]
> [PII detection overview](../personally-identifiable-information/overview.md "Learn more about Personally Identifiable Information detection.") [Document Summarization overview](../summarization/overview.md "Learn more about automatic document summarization.")
