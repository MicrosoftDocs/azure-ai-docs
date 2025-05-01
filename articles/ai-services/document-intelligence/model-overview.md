---
title: Document processing models - Document Intelligence
titleSuffix: Azure AI services
description: Document processing models for OCR, document layout, invoices, identity, custom  models, and more to extract text, structure, and key-value pairs.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 03/14/2025
ms.author: lajanuar
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
 Azure AI Document Intelligence supports a wide variety of models that enable you to add intelligent document processing to your apps and flows. You can use a prebuilt domain-specific model or train a custom model tailored to your specific business needs and use cases. Document Intelligence can be used with the REST API or Python, C#, Java, and JavaScript client libraries.
::: moniker-end

> [!NOTE]
>
> * Document processing projects that involve financial data, protected health data, personal data, or highly sensitive data require careful attention.
> * Be sure to comply with all [national/regional and industry-specific requirements](https://azure.microsoft.com/resources/microsoft-azure-compliance-offerings/).

## Model overview

The following table shows the available models for each stable API:

|**Model Type**| **Model**|[2024-11-30 (GA)](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-11-30)&preserve-view=true)|[2023-07-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[2022-08-31 (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)|[v2.1 (GA)](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true)|
|----------------|-----------|---|--|---|---|
|Document analysis models|[Read](prebuilt/read.md)                                  | ✔️| ✔️| ✔️| n/a|
|Document analysis models|[Layout](prebuilt/layout.md)                              | ✔️| ✔️| ✔️| ✔️|
|Document analysis models|[** General document](prebuilt/general-document.md)          |**supported in<br>layout model**| ✔️| ✔️| n/a|
|Prebuilt models|[Bank Check](concept-bank-check.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Bank Statement](concept-bank-statement.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Paystub](concept-pay-stub.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Contract](prebuilt/contract.md)                          | ✔️| ✔️| n/a| n/a|
|Prebuilt models|[Health insurance card](prebuilt/health-insurance-card.md)| ✔️| ✔️| ✔️| n/a|
|Prebuilt models|[ID document](prebuilt/id-document.md)                    | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[Invoice](prebuilt/invoice.md)                            | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[Receipt](prebuilt/receipt.md)                            | ✔️| ✔️| ✔️| ✔️|
|Prebuilt models|[US Unified Tax*](prebuilt/tax-document.md)                   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US 1040 Tax*](prebuilt/tax-document.md)                   | ✔️| ✔️| n/a| n/a|
|Prebuilt models|[US 1095 Tax*](prebuilt/tax-document.md)                    | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US 1098 Tax*](prebuilt/tax-document.md)                   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US 1099 Tax*](prebuilt/tax-document.md)                 | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US W2 Tax](prebuilt/tax-document.md)                     | ✔️| ✔️| ✔️| n/a|
|Prebuilt models|[US W4 Tax](prebuilt/tax-document.md)                      | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US Mortgage 1003 URLA](concept-mortgage-documents.md)    | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US Mortgage 1004 URAR](concept-mortgage-documents.md)    | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US Mortgage 1005](concept-mortgage-documents.md)    | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US Mortgage 1008 Summary](concept-mortgage-documents.md)       | ✔️| n/a| n/a| n/a|
|Prebuilt models|[US Mortgage closing disclosure](concept-mortgage-documents.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Marriage certificate](concept-marriage-certificate.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Credit card](concept-credit-card.md)   | ✔️| n/a| n/a| n/a|
|Prebuilt models|[Business card](concept-business-card.md)                | deprecated|✔️|✔️|✔️ |
|Custom classification model|[Custom classifier](train/custom-classifier.md)        | ✔️| ✔️| n/a| n/a|
|Custom extraction model|[Custom neural](train/custom-neural.md)                | ✔️| ✔️| ✔️| n/a|
|Custom extraction model|[Custom template](train/custom-template.md)            | ✔️| ✔️| ✔️| ✔️|
|Custom extraction model|[Custom composed](train/composed-models.md)            | ✔️| ✔️| ✔️| ✔️|
|All models|[Add-on capabilities](concept-add-on-capabilities.md)    | ✔️| ✔️| n/a| n/a|

\* Contains submodels. See the model specific information for supported variations and subtypes.</br>
\** All the General Document model capabilities are available in layout model. General model is no longer supported. 

### Latency

Latency is the amount of time it takes for an API server to handle and process an incoming request and deliver the outgoing response to the client. The time to analyze a document depends on the size (for example, number of pages) and associated content on each page. Document Intelligence is a multitenant service where latency for similar documents is comparable but not always identical. Occasional variability in latency and performance is inherent in any microservice-based, stateless, asynchronous service that processes images and large documents at scale. Although we're continuously scaling up the hardware and capacity and scaling capabilities, you might still have latency issues at runtime.

### Add-on Capability

Following are the add-on capability available in document intelligence. For all models, except Business card model, Document Intelligence now supports add-on capabilities to allow for more sophisticated analysis. These optional capabilities can be enabled and disabled depending on the scenario of the document extraction. There are seven add-on capabilities available for the `2023-07-31` (GA) and later API version:

* [`ocrHighResolution`](concept-add-on-capabilities.md#high-resolution-extraction)
* [`formulas`](concept-add-on-capabilities.md#formula-extraction)
* [`styleFont`](concept-add-on-capabilities.md#font-property-extraction)
* [`barcodes`](concept-add-on-capabilities.md#barcode-property-extraction)
* [`languages`](concept-add-on-capabilities.md#language-detection)
* [`keyValuePairs`](concept-add-on-capabilities.md#key-value-pairs)
* [`queryFields`](concept-add-on-capabilities.md#query-fields)  `Not available with the US.Tax models`
* [`searchablePDF`](prebuilt/read.md#searchable-pdf)  `Only available for Read Model`

|**Add-on Capability**| **Add-On/Free**|&bullet; **2024-11-30 (GA)**|[`2023-07-31` (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)|[`2022-08-31` (GA)](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)|[v2.1 (GA)](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true)|
|----------------|-----------|---|--|---|---|
|Font property extraction|Add-On| ✔️| ✔️| n/a| n/a|
|Formula extraction|Add-On| ✔️| ✔️| n/a| n/a|
|High resolution extraction|Add-On| ✔️| ✔️| n/a| n/a|
|Barcode extraction|Free| ✔️| ✔️| n/a| n/a|
|Language detection|Free| ✔️| ✔️| n/a| n/a|
|Key value pairs|Free| ✔️|n/a|n/a| n/a|
|Query fields|Add-On*| ✔️|n/a|n/a| n/a|
|Searchable pdf|Add-On*| ✔️|n/a|n/a| n/a|

### Model analysis features

[!INCLUDE [model analysis features](includes/model-analysis-features.md)]

Add-On* - Query fields are priced differently than the other add-on features. See [pricing](https://azure.microsoft.com/pricing/details/ai-document-intelligence/) for details.

::: moniker range=">=doc-intel-3.0.0"

### Bounding box and polygon coordinates

A bounding box (`polygon` in v3.0 and later versions) is an abstract rectangle that surrounds text elements in a document used as a reference point for object detection.

* The bounding box specifies position by using an x and y coordinate plane presented in an array of four numerical pairs. Each pair represents a corner of the box in the following order: upper left, upper right, lower right, lower left.

* Image coordinates are presented in pixels. For a PDF, coordinates are presented in inches.

## Language support

The deep-learning-based universal models in Document Intelligence support many languages that can extract multilingual text from your images and documents, including text lines with mixed languages.
Language support varies by Document Intelligence service functionality. For a complete list, see the following articles:

* [Language support: document analysis models](language-support/ocr.md)
* [Language support: prebuilt models](language-support/prebuilt.md)
* [Language support: custom models](language-support/custom.md)

## Regional availability

Document Intelligence is generally available in many of the [60+ Azure global infrastructure regions](https://azure.microsoft.com/global-infrastructure/services/?products=metrics-advisor&regions=all#select-product).

For more information, see our [Azure geographies](https://azure.microsoft.com/global-infrastructure/geographies/#overview) page to help choose the region that's best for you and your customers.

## Model details

This section describes the output you can expect from each model. You can extend the output of most models with add-on features.

### Read OCR

:::image type="icon" source="media/studio/read-card.png" :::

The Read API analyzes and extracts lines, words, their locations, detected languages, and handwritten style if detected.

***Sample document processed using the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/read)***:

:::image type="content" source="media/studio/form-recognizer-studio-read-v3p2.png" alt-text="Screenshot of Screenshot of sample document processed using Document Intelligence Studio Read":::

> [!div class="nextstepaction"]
> [Learn more: read model](prebuilt/read.md)

### Layout analysis

:::image type="icon" source="media/studio/layout.png":::

The Layout analysis model analyzes and extracts text, tables, selection marks, and other structure elements like titles, section headings, page headers, page footers, and more.

***Sample document processed using the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/layout)***:

:::image type="content" source="media/studio/form-recognizer-studio-layout-newspaper.png" alt-text="Screenshot of sample newspaper page processed using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
>
> [Learn more: layout model](prebuilt/layout.md)

### Health insurance card

:::image type="icon" source="media/studio/health-insurance-logo.png":::

The health insurance card model combines powerful Optical Character Recognition (OCR) capabilities with deep learning models to analyze and extract key information from US health insurance cards.

***Sample US health insurance card processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=healthInsuranceCard.us)***:

:::image type="content" source="./media/studio/analyze-health-card.png" alt-text="Screenshot of a sample US health insurance card analysis in Document Intelligence Studio." lightbox="./media/studio/analyze-health-card.png":::

> [!div class="nextstepaction"]
> [Learn more: Health insurance card model](prebuilt/health-insurance-card.md)

### US tax documents

:::image type="icon" source="media/studio/tax-documents.png":::

The US tax document models analyze and extract key fields and line items from a select group of tax documents. The API supports the analysis of English-language US tax documents of various formats and quality including phone-captured images, scanned documents, and digital PDFs. The following models are currently supported:

  |Model|Description|ModelID|
  |---|---|---|
  |US Tax W-2|Extract taxable compensation details.|**prebuilt-tax.us.w2**|
  |US Tax W-4|Extract taxable compensation details.|**prebuilt-tax.us.w4**|
  |US Tax 1040|Extract mortgage interest details.|**prebuilt-tax.us.1040(variations)**|
  |US Tax 1095|Extract health insurance details.|**prebuilt-tax.us.1095(variations)**|
  |US Tax 1098|Extract mortgage interest details.|**prebuilt-tax.us.1098(variations)**|
  |US Tax 1099|Extract income received from sources other than employer.|**prebuilt-tax.us.1099(variations)**|

***Sample W-2 document processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=tax.us.w2)***:

:::image type="content" source="./media/studio/w-2.png" alt-text="Screenshot of a sample W-2.":::

> [!div class="nextstepaction"]
> [Learn more: Tax document models](prebuilt/tax-document.md)
>

### US mortgage documents

:::image type="icon" source="media/studio/mortgage-documents.png":::

The US mortgage document models analyze and extract key fields including borrower, loan, and property information from a select group of mortgage documents. The API supports the analysis of English-language US mortgage documents of various formats and quality including phone-captured images, scanned documents, and digital PDFs. The following models are currently supported:

  |Model|Description|ModelID|
  |---|---|---|
  |1003 End-User License Agreement (EULA)|Extract loan, borrower, property details.|**prebuilt-mortgage.us.1003**|
  |1004 Uniform Residential Appraisal Report (URAR))|Extract loan, borrower, property details.|**prebuilt-mortgage.us.1004**|
  |1005 Verification of Employment|Extract loan, borrower, property details.|**prebuilt-mortgage.us.1005**|
  |1008 Summary document|Extract borrower, seller, property, mortgage, and underwriting details.|**prebuilt-mortgage.us.1008**|
  |Closing disclosure|Extract closing, transaction costs, and loan details.|**prebuilt-mortgage.us.closingDisclosure**|
 

***Sample Closing disclosure document processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=mortgage.us.closingDisclosure)***:

:::image type="content" source="./media/studio/closing-disclosure.png" alt-text="Screenshot of a sample closing disclosure.":::

> [!div class="nextstepaction"]
> [Learn more: Mortgage document models](concept-mortgage-documents.md)
>
### Contract

:::image type="icon" source="media/overview/icon-contract.png":::

 The contract model analyzes and extracts key fields and line items from contractual agreements including parties, jurisdictions, contract ID, and title. The model currently supports English-language contract documents.

***Sample contract processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=contract)***:

:::image type="content" source="media/studio/analyze-contract.png" alt-text="Screenshot of contract model extraction using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: contract model](prebuilt/contract.md)

### US Bank Check

:::image type="icon" source="media/overview/icon-contract.png":::

 The contract model analyzes and extracts key fields from check including check details, account details, amount, memo, is extracted from US bank checks.
 
***A bank check sample processed using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=check.us)***:

:::image type="content" source="media/studio/analyze-bank-check.png" alt-text="Screenshot of bank check model extraction using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: contract model](prebuilt/bank-check.md)

### US Bank Statement

:::image type="icon" source="media/overview/icon-contract.png":::

 The bank statement model analyzes and extracts key fields and line items from US bank statements account number, bank details, statement details, and transaction details.

***Sample bank statement processed using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=bankStatement.us)***:

:::image type="content" source="media/studio/analyze-bank-statement.png" alt-text="Screenshot of bank statement model extraction using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: contract model](prebuilt/bank-statement.md)

### PayStub

:::image type="icon" source="media/overview/icon-contract.png":::

 The paystub model analyzes and extracts key fields and line items from documents and files with payroll related information.

***Sample paystub processed using [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=payStub.us)***:

:::image type="content" source="media/studio/analyze-pay-stub.png" alt-text="Screenshot of pay stub model extraction using Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: contract model](prebuilt/pay-stub.md)

### Invoice

:::image type="icon" source="media/studio/invoice.png":::

The invoice model automates processing of invoices to extracts customer name, billing address, due date, and amount due, line items, and other key data. 

***Sample invoice processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=invoice)***:

:::image type="content" source="./media/studio/analyze-invoice.png" alt-text="Screenshot of a sample invoice." lightbox="./media/overview-invoices.jpg":::

> [!div class="nextstepaction"]
> [Learn more: invoice model](prebuilt/invoice.md)

### Receipt

:::image type="icon" source="media/studio/receipt.png":::

Use the receipt model to scan sales receipts for merchant name, dates, line items, quantities, and totals from printed and handwritten receipts. The version v3.0 also supports single-page hotel receipt processing.

***Sample receipt processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=receipt)***:

:::image type="content" source="./media/studio/analyze-receipt.png" alt-text="Screenshot of a sample receipt." lightbox="./media/overview-receipt.jpg":::

> [!div class="nextstepaction"]
> [Learn more: receipt model](prebuilt/receipt.md)

### Identity document (ID)

:::image type="icon" source="media/studio/id-document.png":::

Use the Identity document (ID) model to process U.S. Driver's Licenses (all 50 states and District of Columbia) and biographical pages from international passports (excluding visa and other travel documents) to extract key fields.

***Sample U.S. Driver's License processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=idDocument)***:

:::image type="content" source="./media/studio/analyze-drivers-license.png" alt-text="Screenshot of a sample identification card." lightbox="./media/overview-id.jpg":::

> [!div class="nextstepaction"]
> [Learn more: identity document model](prebuilt/id-document.md)

### Marriage certificate

:::image type="icon" source="media/studio/marriage-certificate-icon.png":::

Use the marriage certificate model to process U.S. marriage certificates to extract key fields including the individuals, date, and location.

***Sample U.S. marriage certificate processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=marriageCertificate.us)***:

:::image type="content" source="./media/studio/marriage-certificate.png" alt-text="Screenshot of a sample marriage certificate." lightbox="./media/studio/marriage-certificate.png":::

> [!div class="nextstepaction"]
> [Learn more: identity document model](concept-marriage-certificate.md)

### Credit card

:::image type="icon" source="media/studio/credit-card-icon.png":::

Use the credit card model to process credit and debit cards to extract key fields.

***Sample credit card processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=creditCard)***:

:::image type="content" source="./media/studio/credit-card.png" alt-text="Screenshot of a sample credit card." lightbox="./media/studio/credit-card.png":::

> [!div class="nextstepaction"]
> [Learn more: identity document model](concept-credit-card.md)

### Custom models

:::image type="icon" source="media/studio/custom.png":::

Custom models can be broadly classified into two types. Custom classification models that support classification of a "document type" and custom extraction models that can extract a defined schema from a specific document type.

:::image type="content" source="media/custom-models.png" alt-text="Diagram of types of custom models and associated model build modes.":::

Custom document models analyze and extract data from forms and documents specific to your business. They recognize form fields within your distinct content and extract key-value pairs and table data. You only need one example of the form type to get started.

Version v3.0 and later custom models support signature detection in custom template (form) and cross-page tables in both template and neural models. [Signature detection](train/custom-template.md#model-capabilities) looks for the presence of a signature, not the identity of the person who signs the document. If the model returns **unsigned** for signature detection, the model didn't find a signature in the defined field.

***Sample custom template processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects)***:

:::image type="content" source="media/studio/train-model.png" alt-text="Screenshot of Document Intelligence tool analyze-a-custom-form window.":::

> [!div class="nextstepaction"]
> [Learn more: custom model](train/custom-model.md)

#### Custom extraction

:::image type="icon" source="media/studio/custom-extraction.png":::

Custom extraction model can be one of two types, **custom template**, **custom neural**. To create a custom extraction model, label a dataset of documents with the values you want extracted and train the model on the labeled dataset. You only need five examples of the same form or document type to get started.

***Sample custom extraction processed using [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects)***:

:::image type="content" source="media/studio/custom-extraction-models.png" alt-text="Screenshot of custom extraction model analysis in Document Intelligence Studio.":::

> [!div class="nextstepaction"]
> [Learn more: custom template model](train/custom-template.md)

> [!div class="nextstepaction"]
> [Learn more: custom neural model](./train/custom-neural.md)

#### Custom classifier

:::image type="icon" source="media/studio/custom-classifier.png":::

The custom classification model enables you to identify the document type before invoking the extraction model. The classification model is available starting with the `2023-07-31 (GA)` API. Training a custom classification model requires at least two distinct classes and a minimum of five samples per class.

> [!div class="nextstepaction"]
> [Learn more: custom classification model](train/custom-classifier.md)

#### Composed models

A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types. You can assign multiple custom models to a composed model called with a single model ID. You can assign up to 200 trained custom models to a single composed model.

***Composed model dialog window in [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/customform/projects)***:

:::image type="content" source="media/studio/composed-model.png" alt-text="Screenshot of Document Intelligence Studio compose custom model dialog window.":::

> [!div class="nextstepaction"]
> [Learn more: custom model](train/custom-model.md)

## Input requirements

[!INCLUDE [input requirements](./includes/input-requirements.md)]

> [!NOTE]
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) doesn't support the BMP file format. The limitation is derived from the tool not the Document Intelligence Service.

### Version migration

Learn how to use Document Intelligence v3.0 in your applications by following our [**Document Intelligence v3.1 migration guide**](v3-1-migration-guide.md)

::: moniker-end

::: moniker range="doc-intel-2.1.0"

| **Model**   | **Description**   |
| --- | --- |
|**Document analysis**||
| [Layout](#layout)  | Extract text and layout information from documents.|
|**Prebuilt**||
| [Invoice](#invoice)  | Extract key information from English and Spanish invoices.  |
| [Receipt](#receipt)  | Extract key information from English receipts.  |
| [ID document](#id-document)  | Extract key information from US driver licenses and international passports.  |
| [Business card](#business-card)  | Extract key information from English business cards.  |
|**Custom**||
| [Custom](#custom) |  Extract data from forms and documents specific to your business. Custom models are trained for your distinct data and use cases. |
| [Composed](#composed-custom-model) | Compose a collection of custom models and assign them to a single model built from your form types.|

### Layout

The Layout API analyzes and extracts text, tables and headers, selection marks, and structure information from documents.

***Sample document processed using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/layout-analyze)***:

:::image type="content" source="media/overview-layout.png" alt-text="Screenshot of `layout` analysis using the Sample Labeling tool.":::

> [!div class="nextstepaction"]
>
> [Learn more: layout model](prebuilt/layout.md)

### Invoice

The invoice model analyzes and extracts key information from sales invoices. The API analyzes invoices in various formats and extracts key information such as customer name, billing address, due date, and amount due.

***Sample invoice processed using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze)***:

:::image type="content" source="./media/overview-invoices.jpg" alt-text="Screenshot of a sample invoice analysis using the Sample Labeling tool.":::

> [!div class="nextstepaction"]
> [Learn more: invoice model](prebuilt/invoice.md)

### Receipt

* The receipt model analyzes and extracts key information from printed and handwritten sales receipts.

***Sample receipt processed using [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze)***:

:::image type="content" source="./media/receipts-example.jpg" alt-text="Screenshot of a sample receipt." lightbox="./media/overview-receipt.jpg":::

> [!div class="nextstepaction"]
> [Learn more: receipt model](prebuilt/receipt.md)

### ID document

 The ID document model analyzes and extracts key information from the following documents:

* U.S. Driver's Licenses (all 50 states and District of Columbia)

* Biographical pages from international passports (excluding visa and other travel documents). The API analyzes identity documents and extracts

***Sample U.S. Driver's License processed using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze)***:

:::image type="content" source="./media/id-example-drivers-license.jpg" alt-text="Screenshot of a sample identification card.":::

> [!div class="nextstepaction"]
> [Learn more: identity document model](prebuilt/id-document.md)

### Business card

The business card model analyzes and extracts key information from business card images.

***Sample business card processed using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/prebuilts-analyze)***:

:::image type="content" source="./media/business-card-example.jpg" alt-text="Screenshot of a sample business card.":::

> [!div class="nextstepaction"]
> [Learn more: business card model](concept-business-card.md)

### Custom

* Custom models analyze and extract data from forms and documents specific to your business. The API is a machine-learning program trained to recognize form fields within your distinct content and extract key-value pairs and table data. You only need five examples of the same form type to get started and your custom model can be trained with or without labeled datasets.

***Sample custom model processing using the [Sample Labeling tool](https://fott-2-1.azurewebsites.net/)***:

:::image type="content" source="media/overview-custom.jpg" alt-text="Screenshot of Document Intelligence tool analyze-a-custom-form window.":::

> [!div class="nextstepaction"]
> [Learn more: custom model](train/custom-model.md)

#### Composed custom model

A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types. You can assign multiple custom models to a composed model called with a single model ID. You can assign up to 100 trained custom models to a single composed model.

***Composed model dialog window using the [Sample Labeling tool](https://formrecognizer.appliedai.azure.com/studio/customform/projects)***:

:::image type="content" source="media/custom-model-compose.png" alt-text="Screenshot of Document Intelligence Studio compose custom model dialog window.":::

> [!div class="nextstepaction"]
> [Learn more: custom model](train/custom-model.md)

## Model data extraction

| **Model** | **Text extraction** | **Language detection** | **Selection Marks** | **Tables** | **Paragraphs** | **Paragraph roles** | **Key-Value pairs** | **Fields** |
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
> The [Sample Labeling tool](https://fott-2-1.azurewebsites.net/) doesn't support the BMP file format. The limitation is derived from the tool not the Document Intelligence Service.

### Version migration

 You can learn how to use Document Intelligence v3.0 in your applications by following our [**Document Intelligence v3.1 migration guide**](v3-1-migration-guide.md)

::: moniker-end

## Next steps

::: moniker range=">=doc-intel-3.0.0"

* Try processing your own forms and documents with the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).

* Complete a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

::: moniker-end

::: moniker range="doc-intel-2.1.0"

* Try processing your own forms and documents with the [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/).

* Complete a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true) and get started creating a document processing app in the development language of your choice.

::: moniker-end
