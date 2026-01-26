---
title: Document Processing Models - Document Intelligence
titleSuffix: Foundry Tools
description: Document processing models for OCR, document layout, invoices, identity, custom models, and more to extract text, structure, and key/value pairs.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: sfi-image-nochange
---


<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD011 -->

# Document processing models

::: moniker range="doc-intel-4.0.0"


[!INCLUDE [applies to v4.0](includes/applies-to-v40.md)]
::: moniker-end

::: moniker range="doc-intel-3.1.0"
[!INCLUDE [applies to v3.1](includes/applies-to-v31.md)]
::: moniker-end

::: moniker range="doc-intel-3.0.0"
[!INCLUDE [applies to v3.0](includes/applies-to-v30.md)]
::: moniker-end

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](includes/applies-to-v21.md)]
::: moniker-end

::: moniker range=">=doc-intel-2.1.0"
 Azure Document Intelligence in Foundry Tools supports various models that you can use to add intelligent document processing to your apps and flows. You can use a prebuilt domain-specific model or train a custom model tailored to your specific business needs and use cases. You can use Document Intelligence with the REST API or Python, C#, Java, and JavaScript client libraries.
::: moniker-end

> [!NOTE]
>
> Document processing projects that involve financial data, protected health data, personal data, or highly sensitive data require careful attention. Be sure to comply with all [national/regional and industry-specific requirements](https://azure.microsoft.com/resources/microsoft-azure-compliance-offerings/).

## Model overview

The following table shows the generally available (GA) models for each stable API.

|Model type| Model|[2024-11-30 (GA)](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)|[2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[2022-08-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)|[v2.1 (GA)](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true)|
|----------------|-----------|---|--|---|---|
|Document analysis models|[Read](prebuilt/read.md)                                  | ✔️| ✔️| ✔️| Not available|
|Document analysis models|[Layout](prebuilt/layout.md)                              | ✔️| ✔️| ✔️| ✔️|
|Document analysis models|[General document**](prebuilt/general-document.md)          |Supported in<br>layout model| ✔️| ✔️| Not available|
|Prebuilt models|[Bank check](concept-bank-check.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[Bank statement](concept-bank-statement.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[payStub](concept-pay-stub.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[Contract](prebuilt/contract.md)                          | ✔️| ✔️| Not available| Not available|
|Prebuilt models|[Health insurance card](prebuilt/health-insurance-card.md)| ✔️| ✔️| ✔️| Not available|
|Prebuilt models|[ID document](prebuilt/id-document.md)                    | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[Invoice](prebuilt/invoice.md)                            | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[Receipt](prebuilt/receipt.md)                            | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[US unified tax*](prebuilt/tax-document.md)                   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US 1040 tax*](prebuilt/tax-document.md)                   | ✔️| ✔️| Not available| Not available|
|Prebuilt models|[US 1095 tax*](prebuilt/tax-document.md)                    | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US 1098 tax*](prebuilt/tax-document.md)                   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US 1099 tax*](prebuilt/tax-document.md)                 | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US W2 tax](prebuilt/tax-document.md)                     | ✔️| ✔️| ✔️| Not available|
|Prebuilt models|[US W4 tax](prebuilt/tax-document.md)                      | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US mortgage 1003 URLA](concept-mortgage-documents.md)    | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US mortgage 1004 URAR](concept-mortgage-documents.md)    | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US mortgage 1005](concept-mortgage-documents.md)    | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US mortgage 1008 summary](concept-mortgage-documents.md)       | ✔️| Not available| Not available| Not available|
|Prebuilt models|[US mortgage closing disclosure](concept-mortgage-documents.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[Marriage certificate](concept-marriage-certificate.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[Credit card](concept-credit-card.md)   | ✔️| Not available| Not available| Not available|
|Prebuilt models|[Business card](concept-business-card.md)                | deprecated|✔️|✔️|✔️ |
|Custom classification model|[Custom classifier](train/custom-classifier.md)        | ✔️| ✔️| Not available| Not available|
|Custom extraction model|[Custom neural](train/custom-neural.md)                | ✔️| ✔️| ✔️| Not available|
|Custom extraction model|[Custom template](train/custom-template.md)            | ✔️| ✔️| ✔️| ✔️|
|Custom extraction model|[Custom composed](train/composed-models.md)            | ✔️| ✔️| ✔️| ✔️|
|All models|[Add-on capabilities](concept-add-on-capabilities.md)    | ✔️| ✔️| Not available| Not available|

\* Contains submodels. See the model-specific information for supported variations and subtypes.</br>
\** All the capabilities for the general document model are available in the layout model. The general model is no longer supported.

### Latency

Latency is the amount of time it takes for an API server to handle and process an incoming request and deliver the outgoing response to the client. The time to analyze a document depends on the size (for example, number of pages) and associated content on each page. Document Intelligence is a multitenant asynchronous service where latency for similar documents is comparable but not always identical. Occasional variability in latency and performance is inherent in any microservice-based, stateless service that processes images and large documents at scale. Although we're continuously scaling up the hardware and capacity and scaling capabilities, you might still have latency issues at runtime.

### Add-on capability

The following add-on capabilities are available for Document Intelligence. For all models except the business card model, Document Intelligence now supports add-on capabilities to allow for more sophisticated analysis. You can enable and disable these optional capabilities depending on the scenario of the document extraction. The following add-on capabilities are available for the 2023-07-31 (GA) and later API version:

* [`ocrHighResolution`](concept-add-on-capabilities.md#high-resolution-extraction)
* [`formulas`](concept-add-on-capabilities.md#formula-extraction)
* [`styleFont`](concept-add-on-capabilities.md#font-property-extraction)
* [`barcodes`](concept-add-on-capabilities.md#barcode-property-extraction)
* [`languages`](concept-add-on-capabilities.md#language-detection)
* [`keyValuePairs`](concept-add-on-capabilities.md#`value-pairs)
* [`queryFields`](concept-add-on-capabilities.md#query-fields) (not available with the US tax models)
* [`searchablePDF`](prebuilt/read.md#searchable-pdf) (available only for the read model)

|Add-on capability| Add-on/Free|2024-11-30 (GA)|[2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[2022-08-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)|[v2.1 (GA)](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true)|
|----------------|-----------|---|--|---|---|
|Font property extraction|Add-on| ✔️| ✔️| Not available| Not available|
|Formula extraction|Add-on| ✔️| ✔️| Not available| Not available|
|High-resolution extraction|Add-on| ✔️| ✔️| Not available| Not available|
|Barcode extraction|Free| ✔️| ✔️| Not available| Not available|
|Language detection|Free| ✔️| ✔️| Not available| Not available|
|Key/value pairs|Free| ✔️|Not available|Not available| Not available|
|Query fields|Add-on*| ✔️|Not available|Not available| Not available|
|Searchable PDF|Add-on*| ✔️|Not available|Not available| Not available|

### Model analysis features

[!INCLUDE [model analysis features](includes/model-analysis-features.md)]

Query fields are priced differently from the other add-on features. For more information, see [Pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/).

::: moniker range=">=doc-intel-3.0.0"

### Bounding box and polygon coordinates

A bounding box (`polygon` in v3.0 and later versions) is an abstract rectangle that surrounds text elements in a document. A bounding box is used as a reference point for object detection:

* The bounding box specifies position by using an x and y coordinate plane presented in an array of four numerical pairs. Each pair represents a corner of the box in the following order: upper left, upper right, lower right, lower left.
* Image coordinates are presented in pixels. For a PDF, coordinates are presented in inches.

## Language support

The universal models in Document Intelligence that are based on deep learning support many languages. The models can extract multilingual text from your images and documents, including text lines with mixed languages. Language support varies by Document Intelligence service functionality. For a complete list, see the following articles:

* [Language support: Document analysis models](language-support/ocr.md)
* [Language support: Prebuilt models](language-support/prebuilt.md)
* [Language support: Custom models](language-support/custom.md)

## Regional availability

Document Intelligence is generally available in many of the [60+ Azure global infrastructure regions](https://azure.microsoft.com/global-infrastructure/services/?products=metrics-advisor&regions=all#select-product).

To help choose the region that's best for you and your customers, see [Azure geographies](https://azure.microsoft.com/global-infrastructure/geographies/#overview).

## Model details

This section describes the output that you can expect from each model. You can extend the output of most models with add-on features.

### Read OCR

:::image type="icon" source="media/studio/read-card.png" :::

The Read API uses optical character recognition (OCR) to analyze and extract lines and words, their locations, detected languages, and handwriting style, if detected.

This sample document was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/read).

:::image type="content" source="media/studio/form-recognizer-studio-read-v3p2.png" alt-text="Screenshot that shows a sample document processed by using Document Intelligence Studio Read.":::

> [!div class="nextstepaction"]
> [Learn more: Read model](prebuilt/read.md)

### Layout analysis

:::image type="icon" source="media/studio/layout.png":::

The layout analysis model analyzes and extracts text, tables, selection marks, and other structure elements like titles, section headings, page headers, and page footers.

This sample document was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/layout).

:::image type="content" source="media/studio/form-recognizer-studio-layout-newspaper.png" alt-text="Screenshot that shows a sample newspaper page processed by using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
>
> [Learn more: Layout model](prebuilt/layout.md)

### Health insurance card

:::image type="icon" source="media/studio/health-insurance-logo.png":::

The health insurance card model combines powerful OCR capabilities with deep learning models to analyze and extract key information from US health insurance cards.

This sample US health insurance card was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=healthInsuranceCard.us).

:::image type="content" source="./media/studio/analyze-health-card.png" alt-text="Screenshot that shows a sample US health insurance card analysis in Document Intelligence Studio." lightbox="./media/studio/analyze-health-card.png":::

> [!div class="nextstepaction"]
> [Learn more: Health insurance card model](prebuilt/health-insurance-card.md)

### US tax documents

:::image type="icon" source="media/studio/tax-documents.png":::

The US tax document models analyze and extract key fields and line items from a select group of tax documents. The API supports the analysis of English-language US tax documents of various formats and quality, including phone-captured images, scanned documents, and digital PDFs. The following models are currently supported:

  |Model|Description|Model ID|
  |---|---|---|
  |US tax W-2|Extract taxable compensation details.|`prebuilt-tax.us.w2`|
  |US tax W-4|Extract taxable compensation details.|`prebuilt-tax.us.w4`|
  |US tax 1040|Extract mortgage interest details.|`prebuilt-tax.us.1040` (variations)|
  |US tax 1095|Extract health insurance details.|`prebuilt-tax.us.1095` (variations)|
  |US tax 1098|Extract mortgage interest details.|`prebuilt-tax.us.1098` (variations)|
  |US tax 1099|Extract income received from sources other than employer.|`prebuilt-tax.us.1099` (variations)|

This sample W-2 document was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=tax.us.w2).

:::image type="content" source="./media/studio/w-2.png" alt-text="Screenshot that shows a sample W-2 document.":::

> [!div class="nextstepaction"]
> [Learn more: Tax document models](prebuilt/tax-document.md)
>

### US mortgage documents

:::image type="icon" source="media/studio/mortgage-documents.png":::

The US mortgage document models analyze and extract key fields that include borrower, loan, and property information from a select group of mortgage documents. The API supports the analysis of English-language US mortgage documents of various formats and quality, including phone-captured images, scanned documents, and digital PDFs. The following models are currently supported.

  |Model|Description|Model ID|
  |---|---|---|
  |1003 End-User License Agreement|Extract loan, borrower, property details.|`prebuilt-mortgage.us.1003`|
  |1004 Uniform Residential Appraisal Report (URAR)|Extract loan, borrower, property details.|`prebuilt-mortgage.us.1004`|
  |1005 Verification of employment|Extract loan, borrower, property details.|`prebuilt-mortgage.us.1005`|
  |1008 Summary document|Extract borrower, seller, property, mortgage, and underwriting details.|`prebuilt-mortgage.us.1008`|
  |Closing Disclosure|Extract closing, transaction costs, and loan details.|`prebuilt-mortgage.us.closingDisclosure`|

This sample Closing Disclosure document was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=mortgage.us.closingDisclosure).

:::image type="content" source="./media/studio/closing-disclosure.png" alt-text="Screenshot that shows a sample closing disclosure.":::

> [!div class="nextstepaction"]
> [Learn more: Mortgage document models](concept-mortgage-documents.md)
>
### Contract

:::image type="icon" source="media/overview/icon-contract.png":::

 The contract model analyzes and extracts key fields and line items from contractual agreements, including parties, jurisdictions, contract ID, and title. The model currently supports English-language contract documents.

This sample contract was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=contract).

:::image type="content" source="media/studio/analyze-contract.png" alt-text="Screenshot that shows contract model extraction using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: Contract model](prebuilt/contract.md)

### US bank check

:::image type="icon" source="media/overview/icon-contract.png":::

 The contract model analyzes and extracts key fields from US bank checks, including check details, account details, amount, and memo.

This bank check sample was processed by using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=check.us).

:::image type="content" source="media/studio/analyze-bank-check.png" alt-text="Screenshot that shows bank check model extraction by using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: Contract model](prebuilt/bank-check.md)

### US bank statement

:::image type="icon" source="media/overview/icon-contract.png":::

 The bank statement model analyzes and extracts key fields and line items from US bank statements account number, bank details, statement details, and transaction details.

This sample bank statement was processed by using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=bankStatement.us).

:::image type="content" source="media/studio/analyze-bank-statement.png" alt-text="Screenshot that shows bank statement model extraction by using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: Contract model](prebuilt/bank-statement.md)

### payStub

:::image type="icon" source="media/overview/icon-contract.png":::

 The payStub model analyzes and extracts key fields and line items from documents and files with payroll-related information.

This sample pay stub was processed by using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=payStub.us).

:::image type="content" source="media/studio/analyze-pay-stub.png" alt-text="Screenshot that shows payStub model extraction by using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: Contract model](prebuilt/pay-stub.md)

### Invoice

:::image type="icon" source="media/studio/invoice.png":::

The invoice model automates the processing of invoices to extract the customer name, billing address, due date, amount due, line items, and other key data.

This sample invoice was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice).

:::image type="content" source="./media/studio/analyze-invoice.png" alt-text="Screenshot that shows a sample invoice." lightbox="./media/overview-invoices.jpg":::

> [!div class="nextstepaction"]
> [Learn more: Invoice model](prebuilt/invoice.md)

### Receipt

:::image type="icon" source="media/studio/receipt.png":::

Use the receipt model to scan sales receipts for the merchant name, dates, line items, quantities, and totals from printed and handwritten receipts. Version v3.0 also supports single-page hotel receipt processing.

This sample receipt was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=receipt).

:::image type="content" source="./media/studio/analyze-receipt.png" alt-text="Screenshot that shows a sample receipt." lightbox="./media/overview-receipt.jpg":::

> [!div class="nextstepaction"]
> [Learn more: Receipt model](prebuilt/receipt.md)

### Identity document

:::image type="icon" source="media/studio/id-document.png":::

Use the identity document (ID) model to process US driver's licenses (all 50 states and District of Columbia) and biographical pages from international passports (excluding visa and other travel documents) to extract key fields.

This sample US driver's license was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=idDocument).

:::image type="content" source="./media/studio/analyze-drivers-license.png" alt-text="Screenshot that shows a sample identification card." lightbox="./media/overview-id.jpg":::

> [!div class="nextstepaction"]
> [Learn more: Identity document model](prebuilt/id-document.md)

### Marriage certificate

:::image type="icon" source="media/studio/marriage-certificate-icon.png":::

Use the marriage certificate model to process US marriage certificates to extract key fields, including the individuals, date, and location.

This sample US marriage certificate was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=marriageCertificate.us).

:::image type="content" source="./media/studio/marriage-certificate.png" alt-text="Screenshot that shows a sample marriage certificate." lightbox="./media/studio/marriage-certificate.png":::

> [!div class="nextstepaction"]
> [Learn more: Identity document model](concept-marriage-certificate.md)

### Credit card

:::image type="icon" source="media/studio/credit-card-icon.png":::

Use the credit card model to process credit and debit cards to extract key fields.

This sample credit card was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=creditCard).

:::image type="content" source="./media/studio/credit-card.png" alt-text="Screenshot that shows a sample credit card." lightbox="./media/studio/credit-card.png":::

> [!div class="nextstepaction"]
> [Learn more: Identity document model](concept-credit-card.md)

### Custom models

:::image type="icon" source="media/studio/custom.png":::

Custom models are broadly classified into two types. Custom classification models that support classification of a "document type" and custom extraction models that can extract a defined schema from a specific document type.

:::image type="content" source="media/custom-models.png" alt-text="Diagram that shows types of custom models and associated model build modes.":::

Custom document models analyze and extract data from forms and documents specific to your business. They recognize form fields within your distinct content and extract key/value pairs and table data. You need only one example of the form type to get started.

Version v3.0 and later custom models support signature detection in custom template (form) and cross-page tables in both template and neural models. [Signature detection](train/custom-template.md#model-capabilities) looks for the presence of a signature, not the identity of the person who signs the document. If the model returns **unsigned** for signature detection, the model didn't find a signature in the defined field.

This sample custom template was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects).

:::image type="content" source="media/studio/train-model.png" alt-text="Screenshot that shows Document Intelligence analyzing a custom form.":::

> [!div class="nextstepaction"]
> [Learn more: Custom model](train/custom-model.md)

#### Custom extraction

:::image type="icon" source="media/studio/custom-extraction.png":::

The custom extraction model comes in two types: custom template and custom neural. To create a custom extraction model, label a dataset of documents with the values you want extracted and train the model on the labeled dataset. You need only five examples of the same form or document type to get started.

This sample custom extraction was processed by using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects).

:::image type="content" source="media/studio/custom-extraction-models.png" alt-text="Screenshot that shows custom extraction model analysis in Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: Custom template model](train/custom-template.md)

> [!div class="nextstepaction"]
> [Learn more: Custom neural model](./train/custom-neural.md)

#### Custom classifier

:::image type="icon" source="media/studio/custom-classifier.png":::

With the custom classification model, you can identify the document type before you invoke the extraction model. The classification model is available starting with the 2023-07-31 (GA) API. Training a custom classification model requires at least two distinct classes and a minimum of five samples per class.

> [!div class="nextstepaction"]
> [Learn more: Custom classification model](train/custom-classifier.md)

#### Composed models

A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types. You can assign multiple custom models to a composed model that are called with a single model ID. You can assign up to 200 trained custom models to a single composed model.

This sample composed model is in [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects).

:::image type="content" source="media/studio/composed-model.png" alt-text="Screenshot that shows the Document Intelligence Studio Compose custom model pane.":::

> [!div class="nextstepaction"]
> [Learn more: Custom model](train/custom-model.md)

## Input requirements

[!INCLUDE [input requirements](./includes/input-requirements.md)]

> [!NOTE]
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) doesn't support the BMP file format. The limitation derives from the tool not the Document Intelligence Service.

### Version migration

Learn how to use Document Intelligence v3.0 in your applications by following the steps in the [Document Intelligence v3.1 migration guide](v3-1-migration-guide.md).

::: moniker-end

::: moniker range="doc-intel-2.1.0"

| Model   | Description   |
| --- | --- |
|Document analysis||
| [Layout](#layout)  | Extract text and layout information from documents.|
|Prebuilt||
| [Invoice](#invoice)  | Extract key information from English-language and Spanish-language invoices.  |
| [Receipt](#receipt)  | Extract key information from English-language receipts.  |
| [ID document](#id-document)  | Extract key information from US driver's licenses and international passports.  |
| [Business card](#business-card)  | Extract key information from English-language business cards.  |
|Custom||
| [Custom](#custom) |  Extract data from forms and documents specific to your business. Custom models are trained for your distinct data and use cases. |
| [Composed](#composed-custom-model) | Compose a collection of custom models and assign them to a single model built from your form types.|

### Layout

The Layout API analyzes and extracts text, tables and headers, selection marks, and structure information from documents.

This sample document was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/layout-analyze).

:::image type="content" source="media/overview-layout.png" alt-text="Screenshot that shows layout analysis by using the Sample Labeling tool.":::

> [!div class="nextstepaction"]
>
> [Learn more: Layout model](prebuilt/layout.md)

### Invoice

The invoice model analyzes and extracts key information from sales invoices. The API analyzes invoices in various formats and extracts key information such as customer name, billing address, due date, and amount due.

This sample invoice was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze).

:::image type="content" source="./media/overview-invoices.jpg" alt-text="Screenshot that shows a sample invoice analysis by using the Sample Labeling tool.":::

> [!div class="nextstepaction"]
> [Learn more: Invoice model](prebuilt/invoice.md)

### Receipt

The receipt model analyzes and extracts key information from printed and handwritten sales receipts.

This sample receipt was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze).

:::image type="content" source="./media/receipts-example.jpg" alt-text="Screenshot that shows a sample receipt." lightbox="./media/overview-receipt.jpg":::

> [!div class="nextstepaction"]
> [Learn more: Receipt model](prebuilt/receipt.md)

### ID document

 The ID document model analyzes and extracts key information from the following documents:

* US driver's licenses (all 50 states and District of Columbia)
* Biographical pages from international passports (excluding visa and other travel documents). The API analyzes and extracts identity documents.

This sample US driver's license was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze).

:::image type="content" source="./media/id-example-drivers-license.jpg" alt-text="Screenshot that shows a sample identification card.":::

> [!div class="nextstepaction"]
> [Learn more: Identity document model](prebuilt/id-document.md)

### Business card

The business card model analyzes and extracts key information from business card images.

This sample business card was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze).

:::image type="content" source="./media/business-card-example.jpg" alt-text="Screenshot that shows a sample business card.":::

> [!div class="nextstepaction"]
> [Learn more: Business card model](concept-business-card.md)

### Custom

Custom models analyze and extract data from forms and documents specific to your business. The API is a machine-learning program trained to recognize form fields within your distinct content and extract key/value pairs and table data. You need only five examples of the same form type to get started. You can train your custom model with or without labeled datasets.

This sample custom model was processed by using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/).

:::image type="content" source="media/overview-custom.jpg" alt-text="Screenshot that shows the Document Intelligence tool analyzing a custom form pane.":::

> [!div class="nextstepaction"]
> [Learn more: Custom model](train/custom-model.md)

#### Composed custom model

A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types. You can assign multiple custom models to a composed model that are called with a single model ID. You can assign up to 100 trained custom models to a single composed model.

This composed model pane was processed by using the [Sample Labeling tool](https://formrecognizer.appliedai.azure.com/studio/customform/projects).

:::image type="content" source="media/custom-model-compose.png" alt-text="Screenshot that shows the Document Intelligence Studio Compose custom model pane.":::

> [!div class="nextstepaction"]
> [Learn more: Custom model](train/custom-model.md)

## Model data extraction

| Model | Text extraction | Language detection | Selection marks | Tables | Paragraphs | Paragraph roles | Key/value pairs | Fields |
|:-----|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
| [Layout](prebuilt/layout.md#data-extraction)  | ✓  |   | ✓ | ✓ | ✓  | ✓  |  |  |
| [Invoice](prebuilt/invoice.md#field-extraction)  | ✓ |   | ✓  | ✓ | ✓ |   | ✓ | ✓ |
| [Receipt](prebuilt/receipt.md#field-extraction)  | ✓  |   |  |  | ✓ |   |  | ✓ |
| [ID Document](prebuilt/id-document.md#field-extractions) | ✓ |   |   |  | ✓ |   |  | ✓ |
| [Business Card](concept-business-card.md#field-extractions)  | ✓  |   |   |  | ✓ |   |  | ✓ |
| [Custom Form](train/custom-model.md#compare-model-features) | ✓  ||  ✓ | ✓ | ✓  |   | | ✓ |

## Input requirements

[!INCLUDE [input requirements](./includes/input-requirements.md)]

> [!NOTE]
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) doesn't support the BMP file format. The limitation derives from the tool not Document Intelligence.

### Version migration

 You can learn how to use Document Intelligence v3.0 in your applications by following the steps in the [Document Intelligence v3.1 migration guide](v3-1-migration-guide.md)

::: moniker-end

## Related content

::: moniker range=">=doc-intel-3.0.0"

* Process your own forms and documents with [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).
* Finish a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true), and then create a document processing app in the development language of your choice.

::: moniker-end

::: moniker range="doc-intel-2.1.0"

* Process your own forms and documents with the [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/).
* Finish a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true), and then create a document processing app in the development language of your choice.

::: moniker-end
