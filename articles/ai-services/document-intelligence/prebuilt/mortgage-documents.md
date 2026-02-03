---
title: Document Intelligence US mortgage documents
titleSuffix: Foundry Tools
description: Use Document Intelligence prebuilt models to analyze and extract key fields from mortgage documents.
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

# Document Intelligence mortgage document models

**This content applies to:** ![checkmark](../media/yes-icon.png) **v4.0 (GA)** 

The Document Intelligence Mortgage models use powerful Optical Character Recognition (OCR) capabilities and deep learning models to analyze and extract key fields from mortgage documents. Mortgage documents can be of various formats and quality. The API analyzes mortgage documents and returns a structured JSON data representation. The models currently support English-language documents only. With the latest V4.0, you can now extract signatures from mortgage applications and forms.

**Supported document types:**

* Uniform Residential Loan Application (Form 1003)
* Uniform Residential Appraisal Report (Form 1004)
* Verification of employment form (Form 1005)
* Uniform Underwriting and Transmittal Summary (Form 1008)
* Closing Disclosure form

## Development options

::: moniker range="doc-intel-4.0.0"

Document Intelligence v4.0 (2024-11-30-GA) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Mortgage model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**&bullet; prebuilt-mortgage.us.1003</br>&bullet; prebuilt-mortgage.us.1004</br>&bullet; prebuilt-mortgage.us.1005</br>&bullet; prebuilt-mortgage.us.1008</br>&bullet; prebuilt-mortgage.us.closingDisclosure**|

::: moniker-end

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Try mortgage documents data extraction

To see how data extraction works for the mortgage documents service, you need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **Mortgage**.

1. You can analyze the sample mortgage documents or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options**:

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)

## Supported languages and locales

*See* our [Language Support—prebuilt models](../language-support/prebuilt.md) page for a complete list of supported languages.

## Field extraction

For supported document extraction fields, *see* the [**mortgage document model schema**](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/main/schema/2024-11-30-ga/us-mortgage)  pages in our GitHub sample repository.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
