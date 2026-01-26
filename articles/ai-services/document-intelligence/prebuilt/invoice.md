---
title: Invoice data extraction – Document Intelligence
titleSuffix: Foundry Tools
description: Automate invoice data extraction with Document Intelligence's invoice model.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: references_regions
---

<!-- markdownlint-disable MD033 -->

# Document Intelligence invoice model

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

The Document Intelligence invoice model uses powerful Optical Character Recognition (OCR) capabilities to analyze and extract key fields and line items from sales invoices, utility bills, and purchase orders. Invoices can be of various formats and quality including phone-captured images, scanned documents, and digital PDFs. The API analyzes invoice text; extracts key information such as customer name, billing address, due date, and amount due; and returns a structured JSON data representation. The model currently supports invoices in 27 languages.

**Supported document types:**

* Invoices
* Utility bills
* Sales orders
* Purchase orders

## Automated invoice processing

Automated invoice processing is the process of extracting key `accounts payable` fields from billing account documents. Extracted data includes line items from invoices integrated with your accounts payable (AP) workflows for reviews and payments. Historically, the accounts payable process is performed manually and, hence, very time consuming. Accurate extraction of key data from invoices is typically the first and one of the most critical steps in the invoice automation process.

::: moniker range=">=doc-intel-3.0.0"

**Sample invoice processed with [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)**:

:::image type="content" source="../media/studio/overview-invoices.png" alt-text="Screenshot of a sample invoice analyzed in the Document Intelligence Studio." lightbox="../media/overview-invoices-big.jpg":::

::: moniker-end

::: moniker range="doc-intel-2.1.0"

**Sample invoice processed with [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net)**:

:::image type="content" source="../media/invoice-example-new.jpg" alt-text="Screenshot of a sample invoice.":::

::: moniker-end

## Development options

::: moniker range="doc-intel-4.0.0"

Document Intelligence v4.0: **2024-11-30** (GA) supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Invoice model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|**prebuilt-invoice**|
::: moniker-end

::: moniker range="doc-intel-3.1.0"

Document Intelligence v3.1 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Invoice model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)|**prebuilt-invoice**|
::: moniker-end

::: moniker range="doc-intel-3.0.0"

Document Intelligence v3.0 supports the following tools, applications, and libraries:

| Feature | Resources | Model ID |
|----------|-------------|-----------|
|**Invoice model**|&bullet; [**Document Intelligence Studio**](https://formrecognizer.appliedai.azure.com)</br>&bullet;  [**REST API**](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)</br>&bullet;  [**C# SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Python SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**Java SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)</br>&bullet;  [**JavaScript SDK**](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)|**prebuilt-invoice**|
::: moniker-end

::: moniker range="doc-intel-2.1.0"

Document Intelligence v2.1 supports the following tools, applications, and libraries:

| Feature | Resources |
|----------|-------------------------|
|**Invoice model**|&bullet; [**Document Intelligence labeling tool**](https://fott-2-1.azurewebsites.net/prebuilts-analyze)</br>&bullet;  [**REST API**](../how-to-guides/use-sdk-rest-api.md?pivots=programming-language-rest-api&view=doc-intel-2.1.0&preserve-view=true&tabs=windows)</br>&bullet;  [**Client-library SDK**](../how-to-guides/use-sdk-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&bullet;  [**Document Intelligence Docker container**](../containers/install-run.md?tabs=id-document#run-the-container-with-the-docker-compose-up-command)|
::: moniker-end

## Input requirements

::: moniker range=">=doc-intel-3.0.0"

[!INCLUDE [input requirements](../includes/input-requirements.md)]

::: moniker-end

::: moniker range="doc-intel-2.1.0"

* Supported file formats: JPEG, PNG, PDF, and TIFF.
* Supported PDF and TIFF, up to 2,000 pages are processed. For free tier subscribers, only the first two pages are processed.
* Supported file size must be less than 50 MB and dimensions at least 50 x 50 pixels and at most 10,000 x 10,000 pixels.

::: moniker-end

## Invoice model data extraction

See how data, including customer information, vendor details, and line items, is extracted from invoices. You need the following resources:

* An Azure subscription—you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* A [Document Intelligence instance](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) in the Azure portal. You can use the free pricing tier (`F0`) to try the service. After your resource deploys, select **Go to resource** to get your key and endpoint.

 :::image type="content" source="../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

::: moniker range=">=doc-intel-3.0.0"

1. On the [Document Intelligence Studio home page](https://documentintelligence.ai.azure.com/studio), select **Invoices**.

1. You can analyze the sample invoice or upload your own files.

1. Select the **Run analysis** button and, if necessary, configure the **Analyze options** :

    :::image type="content" source="../media/studio/run-analysis-analyze-options.png" alt-text="Screenshot of Run analysis and Analyze options buttons in the Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Try Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)

::: moniker-end

::: moniker range="doc-intel-2.1.0"

## Document Intelligence Sample Labeling tool

1. Navigate to the [Document Intelligence Sample Tool](https://fott-2-1.azurewebsites.net/).

1. On the sample tool home page, select the **Use prebuilt model to get data** tile.

    :::image type="content" source="../media/label-tool/prebuilt-1.jpg" alt-text="Screenshot of layout model analyze results process.":::

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

    :::image type="content" source="../media/fott-select-form-type.png" alt-text="Screenshot showing the select-form-type dropdown menu.":::

1. Select **Run analysis**. The Document Intelligence Sample Labeling tool calls the Analyze Prebuilt API and analyze the document.

1. View the results - see the key-value pairs extracted, line items, highlighted text extracted, and tables detected.

    :::image type="content" source="../media/invoice-example-new.jpg" alt-text="Screenshot of layout model analyze results operation.":::

> [!NOTE]
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) does not support the BMP file format. This is a limitation of the tool not the Document Intelligence Service.

::: moniker-end

## Supported languages and locales

For a complete list of supported languages, *see* our [prebuilt model language support](../language-support/prebuilt.md) page.

## Field extraction


:::moniker range=">=doc-intel-3.1.0"

* For supported document extraction fields, *see* the [**invoice model schema**](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-11-30-ga/invoice.md) page in our GitHub sample repository.

* The invoice key-value pairs and line items extracted are in the `documentResults` section of the JSON output.


### Key-value pairs

The prebuilt invoice model supports the optional return of key-value pairs. By default, the return of key-value pairs is disabled. Key-value pairs are specific spans within the invoice that identify a label or key and its associated response or value. In an invoice, these pairs could be the label and the value the user entered for that field or telephone number. The AI model is trained to extract identifiable keys and values based on a wide variety of document types, formats, and structures.

Keys can also exist in isolation when the model detects that a key exists, with no associated value or when processing optional fields. For example, a middle name field can be left blank on a form in some instances. Key-value pairs are always spans of text contained in the document. For documents where the same value is described in different ways, for example, customer/user, the associated key is either customer or user (based on context).
::: moniker-end

### JSON output

The JSON output has three parts:

* `"readResults"` node contains all of the recognized text and selection marks. Text is organized via page, then by line, then by individual words.
* `"pageResults"` node contains the tables and cells extracted with their bounding boxes, confidence, and a reference to the lines and words in *readResults*.
* `"documentResults"` node contains the invoice-specific values and line items that the model discovered. It's where to find all the fields from the invoice such as invoice ID, ship to, bill to, customer, total, line items and lots more.

## Migration guide

* Follow our [**Document Intelligence v3.1 migration guide**](../v3-1-migration-guide.md) to learn how to use the v3.0 version in your applications and workflows.

::: moniker-end

## Next steps

::: moniker range=">=doc-intel-3.0.0"

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

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
