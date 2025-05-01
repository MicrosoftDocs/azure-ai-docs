---
title: Document Intelligence US tax documents data extraction
titleSuffix: Azure AI services
description: Automate US tax document data extraction with Document Intelligence US tax document models.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 11/19/2024
ms.author: lajanuar
monikerRange: ">=doc-intel-3.0.0"
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence US tax document models



**This content applies to:** ![checkmark](../media/yes-icon.png) **v4.0 (GA)** | **Previous versions:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru)
:::moniker-end

:::moniker range="doc-intel-3.1.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)** | **Latest version:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0 (GA)**](?view=doc-intel-4.0.0&preserve-view=true)
:::moniker-end

The Document Intelligence tax model uses powerful Optical Character Recognition (OCR) capabilities to analyze and extract key fields and line items from a select group of tax documents. Tax documents can be of various formats like 1099, 1098, W2, 1040, 1095A, 1095C, W-4, 1099-SSA. Input format can include phone-captured images, scanned documents, and digital PDFs. The API analyzes document text; extracts key information and returns a structured JSON data representation. The model currently supports certain English tax document formats.

**Supported tax form types:**

* Unified tax US
* W-2
* 1098
* 1098-E
* 1098-T
* 1099 and variations (added 1099-SSA)
* 1040 and variations
* 1095A, 1095C
* W-4

## Automated tax document processing

Automated tax document processing is the process of extracting key fields from tax documents. Historically, tax documents were processed manually. This model allows for the easy automation of tax scenarios.

## Unified Tax US

The `Unified US Tax` prebuilt model automatically detects and extracts data from `W2`, `1098`, `1040`, and `1099`  tax forms in submitted documents. These documents can be composed of many tax or non-tax-related documents. The model only processes the forms it supports.

:::image type="content" source="../media/us-unified-tax-diagram.png" alt-text="Screenshot of a Unified Tax processing diagram.":::

## Development options

::: moniker range="doc-intel-4.0.0"


Document Intelligence v4.0: **2024-11-30** (GA) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**US tax form models**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**&bullet; prebuilt-tax.us</br>&bullet; prebuilt-tax.us.w2</br>&bullet;  prebuilt-tax.us.W-4</br>&bullet;  prebuilt-tax.us.1095A</br>&bullet; prebuilt-tax.us.1095C</br>&bullet; prebuilt-tax.us.1098</br>&bullet; prebuilt-tax.us.1098E</br>&bullet; prebuilt-tax.us.1098T</br>&bullet; prebuilt-tax.us.1099A</br>&bullet; prebuilt-tax.us.1099B</br>&bullet; prebuilt-tax.us.1099C</br>&bullet; prebuilt-tax.us.1099CAP</br>&bullet; prebuilt-tax.us.1099Combo</br>&bullet; prebuilt-tax.us.1099DIV</br>&bullet; prebuilt-tax.us.1099G</br>&bullet; prebuilt-tax.us.1099H</br>&bullet; prebuilt-tax.us.1099INT</br>&bullet; prebuilt-tax.us.1099K</br>&bullet; prebuilt-tax.us.1099LS</br>&bullet; prebuilt-tax.us.1099LTC</br>&bullet; prebuilt-tax.us.1099MISC</br>&bullet; prebuilt-tax.us.1099NEC</br>&bullet; prebuilt-tax.us.1099OID</br>&bullet; prebuilt-tax.us.1099PATR</br>&bullet; prebuilt-tax.us.1099Q</br>&bullet; prebuilt-tax.us.1099QA</br>&bullet; prebuilt-tax.us.1099R</br>&bullet; prebuilt-tax.us.1099S</br>&bullet; prebuilt-tax.us.1099SA</br>&bullet; prebuilt-tax.us.1099SB</br>&bullet; prebuilt-tax.us.1099SSA</br>&bullet; prebuilt-tax.us.1040</br>&bullet; prebuilt-tax.us.1040Schedule1</br>&bullet; prebuilt-tax.us.1040Schedule2</br>&bullet; prebuilt-tax.us.1040Schedule3</br>&bullet; prebuilt-tax.us.1040Schedule8812</br>&bullet; prebuilt-tax.us.1040ScheduleA</br>&bullet; prebuilt-tax.us.1040ScheduleB</br>&bullet; prebuilt-tax.us.1040ScheduleC</br>&bullet; prebuilt-tax.us.1040ScheduleD</br>&bullet; prebuilt-tax.us.1040ScheduleE</br>&bullet; prebuilt-tax.us.1040ScheduleEIC</br>&bullet; prebuilt-tax.us.1040ScheduleF</br>&bullet; prebuilt-tax.us.1040ScheduleH</br>&bullet; prebuilt-tax.us.1040ScheduleJ</br>&bullet; prebuilt-tax.us.1040ScheduleR</br>&bullet; prebuilt-tax.us.1040ScheduleSE</br>&bullet; prebuilt-tax.us.1040Senior**|

::: moniker-end

::: moniker range="doc-intel-3.1.0"

Document Intelligence v3.1 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**US tax form models**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)|**&bullet; prebuilt-tax.us.w2</br>&bullet; prebuilt-tax.us.1098</br>&bullet; prebuilt-tax.us.1098E</br>&bullet; prebuilt-tax.us.1098T**|
::: moniker-end

::: moniker range="doc-intel-3.0.0"

Document Intelligence v3.0 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**US tax form models**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)|**&bullet; prebuilt-tax.us.w2</br>&bullet; prebuilt-tax.us.1098</br>&bullet; prebuilt-tax.us.1098E</br>&bullet; prebuilt-tax.us.1098T**|
::: moniker-end

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Try tax document data extraction

See how data, including customer information, vendor details, and line items, is extracted from invoices. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/free/cognitive-services/).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

1. On the [Document Intelligence Studio home page](https://formrecognizer.appliedai.azure.com/studio), select the supported tax document model.

1. You can analyze a sample tax document or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)

## Supported languages and locales

*See* our [Language Support—prebuilt models](../language-support/prebuilt.md) page for a complete list of supported languages.

## Field extraction

For supported document extraction fields, *see* the [**tax document model schema**](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/main/schema/2024-11-30-ga/us-tax) pages in our GitHub sample repository.

The tax documents key-value pairs and line items extracted are in the `documentResults` section of the JSON output.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

::: moniker range="doc-intel-4.0.0"

[Find more samples on GitHub.](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/main/Python(v4.0)/Prebuilt_model)
:::moniker-end

::: moniker range="doc-intel-3.1.0"

[Find more samples on GitHub.](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/v3.1(2023-07-31-GA)/Python(v3.1)/Prebuilt_model)
:::moniker-end
