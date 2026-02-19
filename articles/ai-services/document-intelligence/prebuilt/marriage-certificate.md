---
title: Document Intelligence marriage certificate
titleSuffix: Foundry Tools
description: Automate marriage certificate data extraction with Document Intelligence's marriage certificate model.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-4.0.0'
---
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD049 -->
<!-- markdownlint-disable MD001 -->

# Document Intelligence marriage certificate model

**This content applies to:** ![checkmark](../media/yes-icon.png) **v4.0 (GA)** 

The Document Intelligence Marriage Certificate model uses powerful Optical Character Recognition (OCR) capabilities to analyze and extract key fields from Marriage Certificates. Marriage certificates  can be of various formats and quality including phone-captured images, scanned documents, and digital PDFs. The API analyzes document text; extracts key information such as Spouse names, Issue date, and marriage place; and returns a structured JSON data representation. The model currently supports English-language document formats.

## Automated marriage certificate processing

Automated marriage certificate processing is the process of extracting key  fields from Marriage certificates. Historically, the marriage certificate analysis process is achieved manually and, hence, very time consuming. Accurate extraction of key data from marriage certificates is typically the first and one of the most critical steps in the marriage certificate automation process.

## Development options

::: moniker range="doc-intel-4.0.0"

Document Intelligence v4.0: **2024-11-30** (GA) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**prebuilt-marriageCertificate.us**|&bullet; [**Document Intelligence Studio**](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=marriageCertificate.us&formType=marriageCertificate.us)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**prebuilt-marriageCertificate.us**|

::: moniker-end

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Try marriage certificate document data extraction

To see how data extraction works for the marriage certificate card service, you need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **Marriage Certificate**.

1. You can analyze the sample Marriage certificates or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options**:

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extraction

* For supported document extraction fields, *see* the [**marriage certificate model schema**](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-11-30-ga/marriage-certificate.md) page in our GitHub sample repository.

* The marriage certificate key-value pairs and line items extracted are in the `documentResults` section of the JSON output.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
