---
title: Receipt data extraction - Document Intelligence 
titleSuffix: Azure AI services
description: Use machine learning powered receipt data extraction model to digitize receipts.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/16/2024
ms.author: lajanuar
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence receipt model

::: moniker range="doc-intel-4.0.0"
[!INCLUDE [preview-version-notice](../includes/preview-notice.md)]

[!INCLUDE [applies to v4.0](../includes/applies-to-v40.md)]
::: moniker-end

::: moniker range="doc-intel-3.1.0"
[!INCLUDE [applies to v3.1](../includes/applies-to-v31.md)]
::: moniker-end

::: moniker range="doc-intel-3.0.0"
[!INCLUDE [applies to v3.0](../includes/applies-to-v30.md)]
::: moniker-end

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](../includes/applies-to-v21.md)]
::: moniker-end

The Document Intelligence receipt model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract key information from sales receipts. Receipts can be of various formats and quality including printed and handwritten receipts. The API extracts key information such as merchant name, merchant phone number, transaction date, tax, and transaction total and returns structured JSON data.

**Supported receipt types:**

* Thermal
* Credit Card
* Gas
* Parking
* Hotel
* Transportation
* Communication
* Entertainment
* Flight
* Training
* Pharmacy/Medical

## Receipt data extraction

Receipt digitization encompasses the transformation of various types of receipts, including scanned, photographed, and printed copies, into a digital format for streamlined downstream processing. Examples include expense management, consumer behavior analysis, tax automation, etc. Using Document Intelligence with OCR (Optical Character Recognition) technology can extract and interpret data from these diverse receipt formats. Document Intelligence processing simplifies the conversion process but also significantly reduces the time and effort required, thus facilitating efficient data management, and retrieval.

::: moniker range=">=doc-intel-3.0.0"

***Sample receipt processed with [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=receipt)***:

:::image type="content" source="../media/studio/overview-receipt.png" alt-text="Screenshot of a sample receipt processed in the Document Intelligence Studio." lightbox="../media/overview-receipt.jpg":::

::: moniker-end

::: moniker range="doc-intel-2.1.0"

**Sample receipt processed with [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/connection)**:

:::image type="content" source="../media/analyze-receipt-fott.png" alt-text="Screenshot of a sample receipt processed with the Form Sample Labeling tool.":::

::: moniker-end

## Development options

::: moniker range="doc-intel-4.0.0"

Document Intelligence v4.0 (2024-07-31-preview) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Receipt model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**prebuilt-receipt**|
::: moniker-end

::: moniker range="doc-intel-3.1.0"

Document Intelligence v3.1 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Receipt model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)|**prebuilt-receipt**|
::: moniker-end

::: moniker range="doc-intel-3.0.0"

Document Intelligence v3.0 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Receipt model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)|**prebuilt-receipt**|
::: moniker-end

::: moniker range="doc-intel-2.1.0"

Document Intelligence v2.1 supports the following tools, applications, and libraries:

| Feature | Resources |
|----------|-------------------------|
|**Receipt model**|&bullet; [**Document Intelligence labeling tool**](https://fott-2-1.azurewebsites.net/prebuilts-analyze)</br>&bullet;  [**REST API**](../how-to-guides/use-sdk-rest-api.md?pivots=programming-language-rest-api&view=doc-intel-2.1.0&preserve-view=true&tabs=windows)</br>&bullet;  [**Client-library SDK**](../how-to-guides/use-sdk-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&bullet;  [**Document Intelligence Docker container**](../containers/install-run.md?tabs=id-document#run-the-container-with-the-docker-compose-up-command)|
::: moniker-end

## Input requirements

::: moniker range=">=doc-intel-3.0.0"

[!INCLUDE [input requirements](../includes/input-requirements.md)]

::: moniker-end

::: moniker range="doc-intel-2.1.0"

* Supported file formats: JPEG, PNG, PDF, and TIFF.
* Supported page allowance for PDF and TIFF: Document Intelligence can process up to 2,000 pages for standard tier subscribers or only the first two pages for free-tier subscribers.
* Supported file size: less than 50 MB; minimum pixels 50 x 50 px;  maximum pixels 10,000 x 10,000 px.

::: moniker-end

### Receipt model data extraction

See how Document Intelligence extracts data, including time and date of transactions, merchant information, and amount totals from receipts. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/free/cognitive-services/).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

::: moniker range=">=doc-intel-3.0.0"

> [!NOTE]
> Document Intelligence Studio is available with v3.1 and v3.0 APIs and later versions.

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **Receipts**.

1. You can analyze the sample receipt or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options**:

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

    > [!div class="nextstepaction"]
    > [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=receipt).

::: moniker-end

::: moniker range="doc-intel-2.1.0"

## Document Intelligence Sample Labeling tool

1. Navigate to the [Document Intelligence Sample Tool](https://fott-2-1.azurewebsites.net/).

1. On the sample tool home page, select the **Use prebuilt model to get data** tile.

    :::image type="content" source="../media/label-tool/prebuilt-1.jpg" alt-text="Screenshot of the layout model analyze results process.":::

1. Select the **Form Type**  to analyze from the dropdown menu.

1. Choose a URL for the file you would like to analyze from the below options:

    * [**Sample invoice document**](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/invoice_sample.jpg).

    * [**Sample ID document**](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/DriverLicense.png).

    * [**Sample receipt image**](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg).

    * [**Sample business card image**](https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/samples/sample_forms/business_cards/business-card-english.jpg).

1. In the **Source** field, select **URL** from the dropdown menu, paste the selected URL, and select the **Fetch** button.

    :::image type="content" source="../media/label-tool/fott-select-url.png" alt-text="Screenshot of source location dropdown menu.":::

1. In the **Document Intelligence service endpoint** field, paste the endpoint that you obtained with your Document Intelligence subscription.

1. In the **key** field, paste  the key you obtained from your Document Intelligence resource.

    :::image type="content" source="../media/fott-select-form-type.png" alt-text="Screenshot of the select-form-type dropdown menu.":::

1. Select **Run analysis**. The Document Intelligence Sample Labeling tool calls the Analyze Prebuilt API and analyze the document.

1. View the results - see the key-value pairs extracted, line items, highlighted text extracted, and tables detected.

    :::image type="content" source="../media/receipts-example.jpg" alt-text="Screenshot of the layout model analyze results operation.":::

> [!NOTE]
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) does not support the BMP file format. This is a limitation of the tool not the Document Intelligence Service.

::: moniker-end

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt models language support](../language-support/prebuilt.md) page.

## Field extraction

::: moniker range="doc-intel-2.1.0"

|Name| Type | Description | Standardized output |
|:-----|:----|:----|:----|
| ReceiptType | String | Type of sales receipt |  Itemized |
| MerchantName | String | Name of the merchant issuing the receipt |  |
| MerchantPhoneNumber | phoneNumber | Listed phone number of merchant | +1 xxx xxx xxxx |
| MerchantAddress | String | Listed address of merchant |   |
| TransactionDate | Date | Date the receipt was issued | yyyy-mm-dd |
| TransactionTime | Time | Time the receipt was issued | hh-mm-ss (24-hour)  |
| Total | Number (USD)| Full transaction total of receipt | Two-decimal float|
| Subtotal | Number (USD) | Subtotal of receipt, often before taxes are applied | Two-decimal float|
| Tax | Number (USD) | Total tax on receipt (often sales tax, or equivalent). **Renamed to "TotalTax" in 2022-06-30 version**. | Two-decimal float |
| Tip | Number (USD) | Tip included by buyer | Two-decimal float|
| Items | Array of objects | Extracted line items, with name, quantity, unit price, and total price extracted | |
| Name | String | Item description. **Renamed to "Description" in 2022-06-30 version**. | |
| Quantity | Number | Quantity of each item | Two-decimal float |
| Price | Number | Individual price of each item unit| Two-decimal float |
| TotalPrice | Number | Total price of line item | Two-decimal float |

::: moniker-end

::: moniker range=">=doc-intel-3.0.0"

For supported document extraction fields, refer to the [receipt model schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-07-31-preview/receipt.md) page in our GitHub sample repository.
 
::: moniker-end

::: moniker range="doc-intel-2.1.0"

### Migration guide and REST API v3.1

* Follow our [**Document Intelligence v3.1 migration guide**](../v3-1-migration-guide.md) to learn how to use the v3.1 version in your applications and workflows.

::: moniker-end

## Next steps

::: moniker range=">=doc-intel-3.0.0"

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

::: moniker-end

::: moniker range="doc-intel-4.0.0"
* [Find more samples on GitHub.](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/main/Python(v4.0)/Prebuilt_model)
:::moniker-end

::: moniker range="doc-intel-3.1.0"
* [Find more samples on GitHub.](https://github.com/Azure-Samples/document-intelligence-code-samples/tree/v3.1(2023-07-31-GA)/Python(v3.1)/Prebuilt_model)
:::moniker-end

::: moniker range="doc-intel-2.1.0"

* Try processing your own forms and documents with the [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

::: moniker-end
