---
title: Bank statement US extraction model - Document Intelligence 
titleSuffix: Foundry Tools
description: OCR and machine learning based bank statement US extraction in Document Intelligence extracts key data from bank statements.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: references_regions
monikerRange: '>=doc-intel-4.0.0'
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence bank statement model

The Document Intelligence bank statement model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract data from US bank statements. The API analyzes printed bank statements; extracts key information such as account number, bank details, statement details, transaction details, and fees;  and returns a structured JSON data representation. With V4.0 GA, you can now extract check tables in the US bank statements.

| Feature   | version| Model ID |
|----------  |---------|--------|
| Bank statement model|v4.0: [**2024-11-30**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true) (GA)|**`prebuilt-bankStatement.us`**|

## Bank statement data extraction

A bank statement helps review account's activities during a specified period. It's an official statement that helps in detecting fraud, tracking expenses, accounting errors and record the period's activities. See how data is extracted using the `prebuilt-bankStatement.us` model. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

    :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **bank statements**.

1. You can analyze the sample bank statement or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

    > [!div class="nextstepaction"]
    > [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=businessCard)

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extractions

For supported document extraction fields, *see* the [**bank statement model schema**](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-11-30-ga/bank-statement.md) page in our GitHub sample repository.

## Supported locales

The **prebuilt-bankStatement.us** version 2027-11-30 supports the **en-us** locale.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
