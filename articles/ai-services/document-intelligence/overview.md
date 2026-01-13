---
title: What Is Azure Document Intelligence in Foundry Tools?
titleSuffix: Foundry Tools
description: Azure Document Intelligence in Foundry Tools is a machine-learning based OCR and intelligent document processing service to automate extraction of key data from forms and documents.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: '<=doc-intel-4.0.0'
---


<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD001 -->

# What is Azure Document Intelligence in Foundry Tools?

 :::moniker range="doc-intel-4.0.0"


[!INCLUDE [applies to v4.0](includes/applies-to-v40.md)]

:::moniker-end

 :::moniker range="doc-intel-3.1.0"
[!INCLUDE [applies to v3.1](includes/applies-to-v31.md)]

:::moniker-end

 :::moniker range="doc-intel-3.0.0"
[!INCLUDE [applies to v3.0](includes/applies-to-v30.md)]

:::moniker-end

 :::moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](includes/applies-to-v21.md)]

:::moniker-end

Azure Document Intelligence in Foundry Tools is a cloud-based [Foundry Tools](../../ai-services/index.yml) service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation. For information on region access, see [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).</br></br>

| ✔️ [Document analysis models](#document-analysis-models) | ✔️ [Prebuilt models](#prebuilt-models) | ✔️ [Custom models](#custom-model-overview) |

## Document analysis models

Document analysis (general extraction) models enable text extraction from forms and documents and return structured business-ready content for your organization's action, use, or development.

:::moniker range="doc-intel-4.0.0"

 :::row:::
    :::column:::
    [Read](#read) | Extract printed and handwritten text.
    :::column-end:::
    :::column span="":::
     [Layout](#layout) | Extract text, tables, and document structure.
    :::column-end:::
   :::row-end:::

:::moniker-end
 
:::moniker range="<=doc-intel-3.1.0"

 :::row:::
    :::column:::
    [Read](#read) | Extract printed </br>and handwritten text.
    :::column-end:::
    :::column span="":::
     [Layout](#layout) | Extract text, tables, </br>and document structure.
    :::column-end:::
    :::column span="":::
     [General document](#general-document-deprecated-in-2023-10-31-preview) | Extract text, structure, and </br>key-value pairs.
    :::column-end:::
 :::row-end:::

:::moniker-end

## Prebuilt models

You can use prebuilt models to add intelligent document processing to your apps and flows without having to train and build your own models.

:::moniker range="doc-intel-4.0.0"

### Financial services and legal

 :::row:::
    :::column span="":::
     [Bank statement](#bank-statement) | Extract account information and details from bank statements.
    :::column-end:::
    :::column span="":::
     [Check](#check) | Extract relevant information from checks.
    :::column-end:::
    :::column span="":::
     [Contract](#contract-model) | Extract agreement and party details.
    :::column-end:::
 :::row-end:::
 :::row:::
     :::column span="":::
     [Credit card](#credit-card-model) | Extract payment card information.
     :::column-end:::
     :::column span="":::
     [Invoice](#invoice) | Extract customer and vendor details.
    :::column-end:::
    :::column span="":::
     [Pay stub](#pay-stub) | Extract pay stub details.
    :::column-end:::
    :::column span="":::
     [Receipt](#receipt) | Extract sales transaction details.
    :::column-end:::
 :::row-end:::

### US tax

 :::row:::
    :::column span="":::
     [Unified US tax](#unified-us-tax-forms) | Extract from any US tax forms supported.
    :::column-end:::
    :::column span="":::
     [US tax W-2](#us-tax-w-2-model) | Extract taxable compensation details.
    :::column-end:::
    :::column span="":::
     [US tax 1098](#us-tax-1098-and-variations-forms) | Extract 1098 variation details.
    :::column-end:::
    :::column span="":::
     [US tax 1099](#us-tax-1099-and-variations-forms) | Extract 1099 variation details.
    :::column-end:::
    :::column span="":::
     [US tax 1040](#us-tax-1040-and-variations-forms) |  Extract 1040 variation details.
    :::column-end:::
 :::row-end:::

### US mortgage

 :::row:::
    :::column span="":::
     [US mortgage 1003](#us-mortgage-1003-form) | Extract loan application details.
    :::column-end:::
    :::column span="":::
     [US mortgage 1004](#us-mortgage-1004-form) | Extract information from appraisal.
    :::column-end:::
    :::column span="":::
     [US mortgage 1005](#us-mortgage-1005-form) | Extract information from validation of employment.
    :::column-end:::
    :::column span="":::
     [US mortgage 1008](#us-mortgage-1008-form) | Extract loan transmittal details.
    :::column-end:::
    :::column span="":::
     [US mortgage disclosure](#us-mortgage-disclosure-form) | Extract final closing loan terms.
    :::column-end:::
 :::row-end:::

### Personal identification

 :::row:::
    :::column span="":::
     [Health insurance card](#health-insurance-card) | Extract insurance coverage details.
    :::column-end:::
     :::column span="":::
     [Identity](#identity-id) | Extract verification details.
    :::column-end:::
        :::column span="":::
     [Marriage certificate](#marriage-certificate-model) | Extract certified marriage information.
    :::column-end:::
 :::row-end:::

:::moniker-end

:::moniker range="<=doc-intel-3.1.0"

:::row:::
   :::column span="":::
    [Invoice](#invoice) | Extract customer </br>and vendor details.
   :::column-end:::
   :::column span="":::
    [Receipt](#receipt) | Extract sales </br>transaction details.
   :::column-end:::
   :::column span="":::
    [Identity](#identity-id) | Extract identification </br>and verification details.
   :::column-end:::
:::row-end:::
:::row:::
   :::column span="":::
    [Health insurance card](#health-insurance-card) | Extract health insurance details.
   :::column-end:::
   :::column span="":::
    [Business card](#business-card) | Extract business contact details.
   :::column-end:::
   :::column span="":::
    [Contract](#contract-model) | Extract agreement</br> and party details.
   :::column-end:::
:::row-end:::
:::row:::
   :::column span="":::
    [US tax W-2](#us-tax-w-2-model) | Extract taxable </br>compensation details.
   :::column-end:::
   :::column span="":::
    [US tax 1098](#us-tax-1098-and-variations-forms) | Extract 1098 variation details.
   :::column-end:::
:::row-end:::

:::moniker-end

## Custom models

Custom models are trained by using your labeled datasets to extract distinct data from forms and documents that are specific to your use cases. You can combine standalone custom models to create composed models.

### Document field extraction models

✔️ Document field extraction models are trained to extract labeled fields from documents.

:::row:::
   :::column span="":::
    [Custom neural](#custom-neural) | Extract data from mixed-type documents.
   :::column-end:::
   :::column span="":::
    [Custom template](#custom-template) | Extract data from static layouts.
   :::column-end:::
   :::column span="":::
    [Custom composed](#custom-composed) | Extract data by using a collection of models.
   :::column-end:::
:::row-end:::

### Custom classification models

✔️ Custom classifiers identify document types before invoking an extraction model.

:::row:::
   :::column span="":::
    [Custom classifier](#custom-classification-model) | Identify designated document types (classes) before invoking an extraction model.
   :::column-end:::
:::row-end:::

## Add-on capabilities

Document Intelligence supports optional features that you can enable or disable depending on the document extraction scenario:

* [`ocr.highResolution`](concept-add-on-capabilities.md#high-resolution-extraction)

* [`ocr.formula`](concept-add-on-capabilities.md#formula-extraction)

* [`ocr.font`](concept-add-on-capabilities.md#font-property-extraction)

* [`ocr.barcode`](concept-add-on-capabilities.md#barcode-property-extraction)

* [`Read model support for searchable PDF`](prebuilt/read.md#searchable-pdf)

* [`Searchable PDF`](concept-add-on-capabilities.md#searchable-pdf)

* [`queryFields`](concept-add-on-capabilities.md#query-fields)

* [`keyValuePairs`](concept-add-on-capabilities.md#key-value-pairs)

## Analysis features

[!INCLUDE [model analysis features](includes/model-analysis-features.md)]

## Models and development options

Use Document Intelligence to automate document processing in applications and workflows, enhance data-driven strategies, and enrich document search capabilities. Use the links in the table to learn more about each model and browse development options.

### Read

:::image type="content" source="media/overview/analyze-read.png" alt-text="Screenshot that shows Read model analysis by using Document Intelligence Studio.":::

|Model ID| Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-read](prebuilt/read.md)|&#9679; Extract text from documents.</br>&#9679; [Extract data](prebuilt/read.md#data-extraction).| &#9679; Digitizing any document </br>&#9679; Compliance and auditing</br>&#9679; Processing handwritten notes before translation|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/read)</br>&#9679; [REST API](how-to-guides/use-sdk-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api)</br>&#9679; [C# SDK](how-to-guides/use-sdk-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-csharp)</br>&#9679; [Python SDK](how-to-guides/use-sdk-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-python)</br>&#9679; [Java SDK](how-to-guides/use-sdk-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-java)</br>&#9679; [JavaScript](how-to-guides/use-sdk-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-javascript) |

> [!div class="nextstepaction"]
> [Return to model types](#document-analysis-models)

### Layout

:::image type="content" source="media/overview/analyze-layout.png" alt-text="Screenshot that shows the layout model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-layout](prebuilt/layout.md) |&#9679; Extract text and layout information from documents.</br>&#9679; [Extract data](prebuilt/layout.md#data-extraction). |&#9679; Document indexing and retrieval by structure</br>&#9679; Financial and medical report analysis |&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/layout)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#layout-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#layout-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#layout-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#layout-model)|

> [!div class="nextstepaction"]
> [Return to model types](#document-analysis-models)

 :::moniker range="doc-intel-3.1.0 || doc-intel-3.0.0"

### General document (deprecated in 2023-10-31-preview)

:::image type="content" source="media/overview/analyze-general-document.png" alt-text="Screenshot that shows General document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-document](prebuilt/general-document.md)|&#9679; Extract text, layout, and key/value pairs from documents.</br>&#9679; [Extract data and fields](prebuilt/general-document.md#data-extraction).|&#9679; Key/value pair extraction</br>&#9679; Form processing</br>&#9679; Survey data collection and analysis|&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/document)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)|

> [!div class="nextstepaction"]
> [Return to model types](#document-analysis-models)

:::moniker-end

### Invoice

:::image type="content" source="media/overview/analyze-invoice.png" alt-text="Screenshot that shows Invoice model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-invoice](prebuilt/invoice.md) |&#9679; Extract key information from invoices.</br>&#9679; [Extract data and fields](prebuilt/invoice.md#field-extraction). |&#9679; Accounts payable processing</br>&#9679; Automated tax recording and reporting |&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=invoice&formType=invoice)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Receipt

:::image type="content" source="media/overview/analyze-receipt.png" alt-text="Screenshot that shows Receipt model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-receipt](prebuilt/receipt.md) |&#9679; Extract key information from receipts.</br>&#9679; [Extract data and fields](prebuilt/receipt.md#field-extraction).</br>&#9679; Receipt model v3.0 supports processing of single-page hotel receipts.|&#9679; Expense management</br>&#9679; Consumer behavior data analysis</br>&#9679; Customer loyalty program</br>&#9679; Merchandise return processing</br>&#9679; Automated tax recording and reporting |&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=receipt&formType=receipt)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Identity (ID)

:::image type="content" source="media/overview/analyze-id-document.png" alt-text="Screenshot that shows Identity (ID) document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-idDocument](prebuilt/id-document.md) |&#9679; Extract key information from passports and ID cards.</br>&#9679; [Document types](prebuilt/id-document.md#supported-document-types).</br>&#9679; Extract  endorsements, restrictions, and vehicle classifications from US driver's licenses. |&#9679; Know your customer (KYC) financial services guidelines compliance</br>&#9679; Medical account management</br>&#9679; Identity checkpoints and gateways</br>&#9679; Hotel registration |&#9679;  [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=idDocument&formType=idDocument)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Check

:::image type="content" source="media/studio/overview-check.png" alt-text="Screenshot that shows Check model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-check](concept-bank-check.md) |&#9679; Extract key information from checks.</br>&#9679; [Extract data and fields](concept-bank-check.md#field-extractions). |&#9679; Credit management</br>&#9679; Automated lender management |&#9679;  [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=check.us&formType=check.us)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Pay stub

:::image type="content" source="media/studio/overview-pay-stub.png" alt-text="Screenshot that shows pay stub model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-paystub](concept-pay-stub.md) |&#9679; Extract key information from pay stubs.</br>&#9679; [Extract data and fields](concept-pay-stub.md#field-extractions). |&#9679; Employee payroll detail verification</br>&#9679; Fraud detection for employment</br>&#9679; Automated tax processing |&#9679;  [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=payStub.us&formType=payStub.us)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Bank statement

:::image type="content" source="media/studio/overview-bank-statement.png" alt-text="Screenshot that shows Bank statement model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-bankStatement](concept-bank-statement.md) |&#9679; Extract key information from bank statements.</br>&#9679; [Extract data and fields](concept-bank-statement.md#field-extractions). |&#9679; Tax processing use cases</br>&#9679; Automated accounting management</br>&#9679; Credit-debit management</br>&#9679; Loan documentation processing |&#9679;  [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=bankStatement.us&formSubcategory=bankStatement.us&formType=bankStatement.us)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Health insurance card

:::image type="content" source="media/overview/analyze-health-insurance.png" alt-text="Screenshot that shows Health insurance card model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
| [prebuilt-healthInsuranceCard.us](prebuilt/health-insurance-card.md)|&#9679; Extract key information from US health insurance cards.</br>&#9679; [Extract data and fields](prebuilt/health-insurance-card.md#field-extraction).|&#9679; Coverage and eligibility verification </br>&#9679; Predictive modeling</br>&#9679; Value-based analytics|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=healthInsuranceCard.us&formType=healthInsuranceCard.us)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Contract model

:::image type="content" source="media/overview/analyze-contract.png" alt-text="Screenshot that shows Contract model extraction by using Document Intelligence Studio.":::

| Model ID | Description| Development options |
|----------|--------------|-------------------|
|[prebuilt-contract](prebuilt/contract.md)|&#9679; Extract contract agreement and party details.</br>&#9679; [Extract data and fields](prebuilt/contract.md#field-extraction).|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=contract&formType=contract)</br>&#9679; [REST API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Credit card model

:::image type="content" source="media/overview/analyze-credit-debit.png" alt-text="Screenshot that shows Credit card image model analysis by using Document Intelligence Studio.":::

| Model ID | Description| Development options |
|----------|--------------|-------------------|
|[prebuilt-creditCard](concept-credit-card.md)|&#9679; Extract contract agreement and party details. </br>&#9679; [Extract data and fields](concept-credit-card.md#field-extraction).|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=contract&formType=contract)</br>&#9679; [REST API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### Marriage certificate model

:::image type="content" source="media/overview/analyze-marriage-certificate.png" alt-text="Screenshot that shows Marriage certificate document model analysis by using Document Intelligence Studio.":::

| Model ID | Description| Development options |
|----------|--------------|-------------------|
|[prebuilt-marriageCertificate.us](concept-marriage-certificate.md)|&#9679; Extract contract agreement and party details. </br>&#9679; [Extract data and fields](concept-marriage-certificate.md#field-extraction).|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=marriageCertificate.us&formType=marriageCertificate.us)</br>&#9679; [REST API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

### US mortgage 1003 form

:::image type="content" source="media/overview/analyze-1003.png" alt-text="Screenshot that shows US Mortgage 1003 document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-mortgage.us.1003](concept-mortgage-documents.md)|&#9679; Extract key information from 1003 loan applications. </br>&#9679; [Extract data and fields](concept-mortgage-documents.md#field-extraction-1003-uniform-residential-loan-application-urla).| Fannie Mae and Freddie Mac documentation requirements| &#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=mortgage.us.1003&formType=mortgage.us.1003)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US mortgage 1004 form

:::image type="content" source="media/studio/overview-mortgage-1004.png" alt-text="Screenshot that shows US Mortgage 1004 document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-mortgage.us.1004](concept-mortgage-documents.md)|&#9679; Extract key information from 1004 appraisals. </br>&#9679; [Extract data and fields](concept-mortgage-documents.md#field-extraction-1004-uniform-residential-appraisal-report-urar).|&#9679; Fannie Mae and Freddie Mac documentation requirements </br>&#9679; Uniform Residential Appraisal report to help lender/client with the market value of the subject property| &#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=mortgage.us.1004&formType=mortgage.us.1004)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US mortgage 1005 form

:::image type="content" source="media/studio/overview-mortgage-1005.png" alt-text="Screenshot that shows US Mortgage 1005 document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-mortgage.us.1005](concept-mortgage-documents.md)|&#9679; Extract key information from 1005 validation of employment. </br>&#9679; [Extract data and fields](concept-mortgage-documents.md#field-extraction-1005-verification-of-employment-form).|&#9679; Fannie Mae and Freddie Mac documentation requirements </br>&#9679; Verification of employment document to determine the qualification as a prospective mortgagor| &#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=mortgage.us.1005&formType=mortgage.us.1005)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US mortgage 1008 form

:::image type="content" source="media/overview/analyze-1008.png" alt-text="Screenshot that shows US Mortgage 1008 document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-mortgage.us.1008](concept-mortgage-documents.md)|&#9679; Extract key information from Uniform Underwriting and Transmittal Summary. </br>&#9679; [Extract data and fields](concept-mortgage-documents.md#field-extraction-1008-uniform-underwriting-and-transmittal-summary). Loan underwriting processing by using summary data| &#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=mortgage.us.1008&formType=mortgage.us.1008)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US mortgage disclosure form

:::image type="content" source="media/overview/analyze-closing-disclosure.png" alt-text="Screenshot that shows US Mortgage closing disclosure document model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-mortgage.us.closingDisclosure](concept-mortgage-documents.md)|&#9679; Extract key information from Uniform Underwriting and Transmittal Summary. </br>&#9679; [Extract data and fields](concept-mortgage-documents.md#field-extraction-mortgage-closing-disclosure).| Mortgage loan final details requirements| &#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=mortgage.us.closingDisclosure&formType=mortgage.us.closingDisclosure)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US tax W-2 model

:::image type="content" source="media/overview/analyze-w2.png" alt-text="Screenshot that shows W-2 model analysis by using Document Intelligence Studio.":::

| Model ID| Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-tax.us.w2](prebuilt/tax-document.md) | Extract key information from IRS US W2 tax forms (years 2018-2021).</br>|&#9679; Automated tax document management</br>&#9679; Mortgage loan application processing |&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=tax.us.w2&formType=tax.us.w2)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model) |

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US tax 1098 (and variations) forms

:::image type="content" source="media/overview/analyze-1098.png" alt-text="Screenshot that shows US 1098 tax form analyzed in the Document Intelligence Studio.":::

| Model ID | Description| Development options |
|----------|--------------|-------------------|
|[prebuilt-tax.us.1098{`variation`}](prebuilt/tax-document.md)| Extract key information from 1098-form variations.</br>|&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=tax.us.1098)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US tax 1099 (and variations) forms

:::image type="content" source="media/overview/analyze-1099.png" alt-text="Screenshot that shows US 1099 tax form analyzed in the Document Intelligence Studio." lightbox="media/overview/analyze-1099.png":::

| Model ID |Description|Development options |
|----------|--------------|-----------------|
|[prebuilt-tax.us.1099{`variation`}](prebuilt/tax-document.md)| Extract information from 1099-form variations.</br>|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=tax.us.1099)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

### US tax 1040 (and variations) forms

:::image type="content" source="media/overview/analyze-1040.png" alt-text="Screenshot that shows US tax 1040 tax form model analysis by using Document Intelligence Studio.":::

| Model ID |Description|Development options |
|----------|--------------|-----------------|
|[prebuilt-tax.us.1040{`variation`}](prebuilt/tax-document.md)| Extract information from 1040-form variations.</br>|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=tax.us.1040)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

:::moniker range=">=doc-intel-4.0.0"

### Unified US tax forms

| Model ID |Description|Development options |
|----------|--------------|-----------------|
|[prebuilt-tax.us](prebuilt/tax-document.md)|Extract information from any of the supported US tax forms.|&#9679; [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio/prebuilt?formCategory=tax.us.1040)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

:::moniker-end

 :::moniker range="<=doc-intel-3.1.0"

### Business card

  :::image type="content" source="media/overview/analyze-business-card.png" alt-text="Screenshot that shows Business card model analysis by using Document Intelligence Studio.":::

| Model ID | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[prebuilt-businessCard](concept-business-card.md) |&#9679; Extract key information from business cards.</br>&#9679; [Extract data and fields](concept-business-card.md#field-extractions). | Sales lead and marketing management |&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/prebuilt?formType=businessCard)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-rest-api#analyze-document-post-request)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)</br>&#9679; [JavaScript](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true#prebuilt-model)|

> [!div class="nextstepaction"]
> [Return to model types](#prebuilt-models)

:::moniker-end

### Custom model overview

:::image type="content" source="media/overview/custom-train.png" alt-text="Screenshot that shows Custom model training by using Document Intelligence Studio.":::

| About | Description |Automation use cases |Development options |
|----------|--------------|-----------|--------------------------|
|[Custom model](train/custom-model.md) | Extract information from forms and documents into structured data based on a model created from a set of representative training document sets.|Extract distinct data from forms and documents specific to your business and use cases.|&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/custommodel/projects)</br>&#9679; [REST API](/rest/api/aiservices/document-models/build-model?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [JavaScript SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|

> [!div class="nextstepaction"]
> [Return to custom model types](#custom-models)

#### Custom neural

:::image type="content" source="media/overview/analyze-custom-neural.png" alt-text="Screenshot that shows Custom Neural model analysis by using Document Intelligence Studio.":::

  > [!NOTE]
  > To train a custom neural model, set the `buildMode` property to `neural`. For more information, see [Training a neural model](train/custom-neural.md#training-a-model).

| About | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[Custom Neural model](train/custom-neural.md)| Extract labeled data from structured (surveys, questionnaires), semistructured (invoices, purchase orders), and unstructured documents (contracts, letters).|Extract text data, checkboxes, and tabular fields from structured and unstructured documents.|[Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/custommodel/projects)</br>&#9679; [REST API](/rest/api/aiservices/document-models/build-model?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [JavaScript SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|

> [!div class="nextstepaction"]
> [Return to custom model types](#custom-models)

#### Custom template

:::image type="content" source="media/overview/analyze-custom-template.png" alt-text="Screenshot that shows Custom Template model analysis by using Document Intelligence Studio.":::

  > [!NOTE]
  > To train a custom template model, set the `buildMode` property to `template`. For more information, see [Training a template model](train/custom-template.md#training-a-model).

| About | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[Custom Template model](train/custom-template.md) | Extract labeled values and fields from structured and semistructured documents.</br> | Extract key data from highly structured documents with defined visual templates or common visual layouts and forms.| &#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/custommodel/projects)</br>&#9679; [REST API](/rest/api/aiservices/document-models/build-model?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [C# SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [Java SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)</br>&#9679; [JavaScript SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true)|

> [!div class="nextstepaction"]
> [Return to custom model types](#custom-models)

#### Custom composed

| About | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[Composed custom models](train/composed-models.md)| A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types.| Useful when you train several models and want to group them to analyze similar form types, like purchase orders|&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/custommodel/projects)</br>&#9679; [REST API](/rest/api/aiservices/document-models/compose-model?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>&#9679; [C# SDK](/dotnet/api/azure.ai.formrecognizer.training.formtrainingclient.startcreatecomposedmodel)</br>&#9679; [Java SDK](/java/api/com.azure.ai.formrecognizer.training.formtrainingclient.begincreatecomposedmodel)</br>&#9679; [JavaScript SDK](/javascript/api/@azure/ai-form-recognizer/documentmodeladministrationclient?view=azure-node-latest#@azure-ai-form-recognizer-documentmodeladministrationclient-begincomposemodel&preserve-view=true)</br>&#9679; [Python SDK](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)|

> [!div class="nextstepaction"]
> [Return to custom model types](#custom-models)

:::moniker range=">=doc-intel-3.1.0"

#### Custom classification model

:::image type="content" source="media/overview/custom-classifier-labeling.png" alt-text="Screenshot that shows Custom classification model labeling in Document Intelligence Studio.":::

| About | Description |Automation use cases | Development options |
|----------|--------------|-------------------------|-----------|
|[Composed classification model](train/custom-classifier.md)| Custom classification models combine layout and language features to detect, identify, and classify documents within an input file.|&#9679; A loan application package that contains application forms, pay slips, and bank statements</br>&#9679; A collection of scanned invoices |&#9679; [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio/custommodel/projects)</br>&#9679; [REST API](/rest/api/aiservices/document-classifiers/build-classifier?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)</br>|

> [!div class="nextstepaction"]
> [Return to custom model types](#custom-models)

:::moniker-end

 :::moniker range="doc-intel-2.1.0"

Azure Document Intelligence is a cloud-based [Foundry Tools](../../ai-services/index.yml) for developers to build intelligent document processing solutions. Azure Document Intelligence applies optical character recognition (OCR) based on machine learning along with document understanding technologies to extract text, tables, structure, and key/value pairs from documents. You can also label and train custom models to automate data extraction from structured, semistructured, and unstructured documents. To learn more about each model, see the concepts articles.

| Model type | Model name |
|------------|-----------|
|Document analysis model| &#9679; [Layout analysis model](prebuilt/layout.md?view=doc-intel-2.1.0&preserve-view=true) </br>  |
| Prebuilt models | &#9679; [Invoice model](prebuilt/invoice.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Receipt model](prebuilt/receipt.md?view=doc-intel-2.1.0&preserve-view=true) </br>&#9679; [Identity document (ID) model](prebuilt/id-document.md?view=doc-intel-2.1.0&preserve-view=true) </br>&#9679; [Business card model](concept-business-card.md?view=doc-intel-2.1.0&preserve-view=true) </br>|
| Custom models | &#9679; [Custom model](train/custom-model.md) </br>&#9679; [Composed model](model-overview.md?view=doc-intel-2.1.0&preserve-view=true)|

:::moniker-end

 :::moniker range="doc-intel-2.1.0"

[!INCLUDE [applies to v2.1](includes/applies-to-v21.md)]

## Document Intelligence models and development options

 >[!TIP]
 >
 > For an enhanced experience and advanced model quality, try the [Document Intelligence v3.0 Studio](https://formrecognizer.appliedai.azure.com/studio):

 >   * The v3.0 Studio supports any model trained with v2.1 labeled data.
 >   * For more information about migrating from v2.1 to v3.0, see the API migration guide.

To learn more about each model and browse the API references, use the links in the following table.

| Model| Description | Development options |
|----------|--------------|-------------------------|
|[Layout analysis](prebuilt/layout.md?view=doc-intel-2.1.0&preserve-view=true) | Extraction and analysis of text, selection marks, tables, and bounding box coordinates, from forms and documents | &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#analyze-layout)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Client-library SDK](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?branch=main&tabs=layout#run-the-container-with-the-docker-compose-up-command)|
|[Custom model](train/custom-model.md?view=doc-intel-2.1.0&preserve-view=true) | Extraction and analysis of data from forms and documents specific to distinct business data and use cases| &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#train-a-custom-form-model)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Sample Labeling Tool](train/custom-model.md?view=doc-intel-2.1.0&preserve-view=true#build-a-custom-model)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?tabs=custom#run-the-container-with-the-docker-compose-up-command)|
|[Invoice model](prebuilt/invoice.md?view=doc-intel-2.1.0&preserve-view=true) | Automated data processing and extraction of key information from sales invoices | &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#analyze-using-a-prebuilt-model)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Client-library SDK](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?tabs=invoice#run-the-container-with-the-docker-compose-up-command)|
|[Receipt model](prebuilt/receipt.md?view=doc-intel-2.1.0&preserve-view=true) | Automated data processing and extraction of key information from sales receipts.| &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#analyze-using-a-prebuilt-model)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Client-library SDK](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?tabs=receipt#run-the-container-with-the-docker-compose-up-command)|
|[Identity document (ID) model](prebuilt/id-document.md?view=doc-intel-2.1.0&preserve-view=true) | Automated data processing and extraction of key information from US driver's licenses and international passports| &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#analyze-using-a-prebuilt-model)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Client-library SDK](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?tabs=id-document#run-the-container-with-the-docker-compose-up-command)|
|[Business card model](concept-business-card.md?view=doc-intel-2.1.0&preserve-view=true) | Automated data processing and extraction of key information from business cards| &#9679; [Document Intelligence labeling tool](quickstarts/try-sample-label-tool.md#analyze-using-a-prebuilt-model)</br>&#9679; [REST API](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true)</br>&#9679; [Client-library SDK](quickstarts/get-started-sdks-rest-api.md)</br>&#9679; [Document Intelligence Docker container](containers/install-run.md?tabs=business-card#run-the-container-with-the-docker-compose-up-command)|

:::moniker-end

## Data privacy and security

 As with all Foundry Tools, developers who use Document Intelligence should be aware of Microsoft policies on customer data. For more information, see [Data, privacy, and security for Document Intelligence](/azure/ai-foundry/responsible-ai/document-intelligence/data-privacy-security).

## Related content

:::moniker range=">=doc-intel-3.0.0"

* [Choose a Document Intelligence model]().
* Process your own forms and documents with [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).
* Finish a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), and then create a document processing app in the development language of your choice.

:::moniker-end

:::moniker range="doc-intel-2.1.0"

* Process your own forms and documents with the [Document Intelligence Sample Labeling tool](https://fott-2-1.azurewebsites.net/).
* Finish a [Document Intelligence quickstart](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true), and then create a document processing app in the development language of your choice.

:::moniker-end
