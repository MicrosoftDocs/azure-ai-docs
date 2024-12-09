---
title: Check extraction - Document Intelligence 
titleSuffix: Azure AI services
description: OCR and machine learning based check extraction in Document Intelligence extracts key data from cheques.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/16/2024
ms.author: lajanuar
monikerRange: '>=doc-intel-4.0.0'
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence bank check model

The Document Intelligence bank check model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract data from US bank statements. The API analyzes printed checks; extracts key information, and returns a structured JSON data representation.

| Feature   | version| Model ID |
|----------  |---------|--------|
| Check model|&bullet; v4.0:2024-07-31 (preview)|**`prebuilt-check.us`**|

## Check data extraction

A check is a secure way to transfer amount from payee's account to receiver's account. Businesses use check to pay their vendors as a signed document to instruct the bank for payment. See how data, including check details, account details, amount, memo, is extracted from bank statement US. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/free/cognitive-services/)

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Document Intelligence Studio

> [!NOTE]
> Document Intelligence Studio is available with v3.1 and v3.0 APIs.

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **check**.

1. You can analyze the sample check or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

    > [!div class="nextstepaction"]
    > [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=businessCard)

## Input requirements

[!INCLUDE [input requirements](../includes/input-requirements.md)]

## Supported languages and locales

 For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extractions

For supported document extraction fields, refer to the [bank check model schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-07-31-preview/bank-check.md) page in our GitHub sample repository.

## Supported locales

The **`prebuilt-check.us`** version 2024-07-31-preview supports the **en-us** locale.

## Next steps

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.
