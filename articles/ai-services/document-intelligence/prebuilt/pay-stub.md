---
title: Document Intelligence pay stub model
titleSuffix: Azure AI services
description: Automate compensation and earnings information from pay slips and stubs.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/03/2024
ms.author: admaheshwari
monikerRange: '>=doc-intel-4.0.0'
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence pay stub model

The Document Intelligence pay stub model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract compensation and earnings data from pay slips. The API analyzes documents and files with payroll related information; extracts key information and returns a structured JSON data representation.

| Feature   | version| Model ID |
|----------  |---------|--------|
|Pay stub model|&bullet; v4.0:2024-07-31 (preview)|**`prebuilt-payStub.us`**|

## Try pay stub data extraction

Pay stubs are essential documents issued by employers to employees, providing earnings, deductions, and net pay information for a specific pay period. See how data is extracted using `prebuilt-payStub.us` model. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/free/cognitive-services/)

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

    :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **payStub**.

1. You can analyze the sample pay stub or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extractions

For supported document extraction fields, refer to the [pay stub model schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-07-31-preview/pay-stub.md) page in our GitHub sample repository.

## Supported locales

The **prebuilt-payStub.us** version 2027-07-31-preview supports the **en-us** locale.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
