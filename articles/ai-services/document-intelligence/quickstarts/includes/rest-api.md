---
title: "Quickstart: Document Intelligence REST API"
titleSuffix: Azure AI services
description: Form and document processing, data extraction, and analysis using Document Intelligence REST API v3.0
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: include
ms.date: 09/09/2024
ms.author: lajanuar
---

<!-- markdownlint-disable MD036 -->

:::moniker range="doc-intel-4.0.0"
| [Document Intelligence REST API](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true) | [Supported Azure SDKS](../../sdk-overview-v4-0.md)
:::moniker-end

:::moniker range="doc-intel-3.1.0"
| [Document Intelligence REST API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP) | [Supported Azure SDKS](../../sdk-overview-v3-1.md) |
:::moniker-end

:::moniker range="doc-intel-3.0.0"
| [Document Intelligence REST API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP) | [Supported Azure SDKS](../../sdk-overview-v3-0.md) |
:::moniker-end

In this quickstart, learn to use the Document Intelligence REST API to analyze and extract data and values from documents:

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services)

* curl command line tool installed.

  * [Windows](https://curl.haxx.se/windows/)
  * [Mac or Linux](https://learn2torials.com/thread/how-to-install-curl-on-mac-or-linux-(ubuntu)-or-windows)

* **PowerShell version 7.*+** (or a similar command-line application.):
  * [Windows](/powershell/scripting/install/installing-powershell-on-windows)
  * [macOS](/powershell/scripting/install/installing-powershell-on-macos)
  * [Linux](/powershell/scripting/install/installing-powershell-on-linux)

* To check your PowerShell version, type the following command relative to your operating system:
  * Windows: `Get-Host | Select-Object Version`
  * macOS or Linux: `$PSVersionTable`

* A Document Intelligence (single-service) or Azure AI services (multi-service) resource. Once you have your Azure subscription, create a [single-service](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) or [multi-service](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) Document Intelligence resource, in the Azure portal, to get your key and endpoint. You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.

> [!TIP]
> Create an Azure AI services resource if you plan to access multiple Azure AI services under a single endpoint/key. For Document Intelligence access only, create a Document Intelligence resource. Please note that you'll  need a single-service resource if you intend to use [Microsoft Entra authentication](/azure/active-directory/authentication/overview-authentication).

* After your resource deploys, select **Go to resource**. You need the key and endpoint from the resource you create to connect your application to the Document Intelligence API. You paste your key and endpoint into the code later in the quickstart:

  :::image type="content" source="../../media/containers/keys-and-endpoint.png" alt-text="Screenshot of keys and endpoint location in the Azure portal.":::

## Analyze documents and get results

 A POST request is used to analyze documents with a prebuilt or custom model. A GET request is used to retrieve the result of a document analysis call. The `modelId` is used with POST and `resultId` with GET operations.

### Analyze document (POST Request)

Before you run the cURL command, make the following changes to the [post request](#post-request):

1. Replace `{endpoint}` with the endpoint value from your Azure portal Document Intelligence instance.

1. Replace `{key}` with the key value from your Azure portal Document Intelligence instance.

1. Using the following table as a reference, replace `{modelID}` and `{your-document-url}` with your desired values.

1. You need a document file at a URL. For this quickstart, you can use the sample forms provided in the following table for each feature:

:::moniker range="doc-intel-4.0.0"

**Sample documents**

| **Feature**   | **{modelID}**   | **{your-document-url}** |
| --- | --- |--|
| **Read** | prebuilt-read | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png` |
| **Layout** | prebuilt-layout | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/layout.png` |
| **Health insurance card** | prebuilt-healthInsuranceCard.us | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/insurance-card.png` |
| **W-2**  | prebuilt-tax.us.w2 | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/w2.png` |
| **Invoice**  | prebuilt-invoice | `https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf` |
| **Receipt**  | prebuilt-receipt | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png` |
| **ID document**  | prebuilt-idDocument | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png` |
:::moniker-end

:::moniker range="doc-intel-3.1.0 || doc-intel-3.0.0"

**Sample documents**

| **Feature**   | **{modelID}**   | **{your-document-url}** |
| --- | --- |--|
| **General Document** | prebuilt-document | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf` |
| **Read** | prebuilt-read | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png` |
| **Layout** | prebuilt-layout | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/layout.png` |
| **Health insurance card** | prebuilt-healthInsuranceCard.us | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/insurance-card.png` |
| **W-2**  | prebuilt-tax.us.w2 | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/w2.png` |
| **Invoice**  | prebuilt-invoice | `https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf` |
| **Receipt**  | prebuilt-receipt | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png` |
| **ID document**  | prebuilt-idDocument | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png` |
| **Business card**  | prebuilt-businessCard | `https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/de5e0d8982ab754823c54de47a47e8e499351523/curl/form-recognizer/rest-api/business_card.jpg` |
:::moniker-end

> [!IMPORTANT]
> Remember to remove the key from your code when you're done, and never post it publicly. For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information, *see* Azure AI services [security](../../../../ai-services/security-features.md).

#### POST request

:::moniker range="doc-intel-4.0.0"

```bash
curl -v -i POST "{endpoint}/documentintelligence/documentModels/{modelId}:analyze?api-version=2024-07-31-preview" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {key}" --data-ascii "{'urlSource': '{your-document-url}'}"
```

:::moniker-end

:::moniker range="doc-intel-3.1.0"

```bash
curl -v -i POST "{endpoint}/formrecognizer/documentModels/{modelID}:analyze?api-version=2023-07-31" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {key}" --data-ascii "{'urlSource': '{your-document-url}'}"
```

:::moniker-end

:::moniker range="doc-intel-3.0.0"

```bash
curl -v -i POST "{endpoint}/formrecognizer/documentModels/{modelId}:analyze?api-version=2022-08-31" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {key}" --data-ascii "{'urlSource': '{your-document-url}'}"
```

:::moniker-end

#### POST response (resultID)

You receive a `202 (Success)` response that includes a read-only **Operation-Location** header. The value of this header contains a `resultID` that can be queried to get the status of the asynchronous operation and retrieve the results using a GET request with your same resource subscription key:

:::image type="content" source="../../media/quickstarts/operation-location-result-id.png" alt-text="{alt-text}":::

### Get analyze results (GET Request)

:::moniker range="doc-intel-4.0.0"

After you call the [`Analyze document`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true&tabs=HTTP) API, call the [**Get analyze result**](/rest/api/aiservices/document-models/get-analyze-result?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true&tabs=HTTP) API to get the status of the operation and the extracted data. Before you run the command, make these changes:
:::moniker-end

:::moniker range="doc-intel-3.1.0"

After you call the [`Analyze document`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP) API, call the [**Get analyze result**](/rest/api/aiservices/document-models/get-analyze-result?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP) API to get the status of the operation and the extracted data. Before you run the command, make these changes:

:::moniker-end

:::moniker range="doc-intel-3.0.0"

After you call the [`Analyze document`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP) API, call the [**Get analyze result**](/rest/api/aiservices/document-models/get-analyze-result?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP) API to get the status of the operation and the extracted data. Before you run the command, make these changes:
:::moniker-end

1. Replace `{resultID}` Operation-Location header from the [POST response](#post-response-resultid).

1. Replace `{key}` with the key value from your Document Intelligence instance in the Azure portal.

<!-- markdownlint-disable MD024 -->

#### GET request

:::moniker range="doc-intel-4.0.0"

```bash
curl -v -X GET "{endpoint}/documentintelligence/documentModels/{modelId}/analyzeResults/{resultId}?api-version=2024-07-31-preview" -H "Ocp-Apim-Subscription-Key: {key}"
```

:::moniker-end

:::moniker range="doc-intel-3.1.0"

```bash
curl -v -X GET "{endpoint}/formrecognizer/documentModels/{modelId}/analyzeResults/{resultId}?api-version=2023-07-31" -H "Ocp-Apim-Subscription-Key: {key}"

```

:::moniker-end

:::moniker range="doc-intel-3.0.0"

```bash
curl -v -X GET "{endpoint}/formrecognizer/documentModels/{modelId}/analyzeResults/{resultId}?api-version=2022-08-31" -H "Ocp-Apim-Subscription-Key: {key}"

```

:::moniker-end

#### Examine the response

You receive a `200 (Success)` response with JSON output. The first field, `"status"`, indicates the status of the operation. If the operation isn't complete, the value of `"status"` is `"running"` or `"notStarted"`, and you should call the API again, either manually or through a script. We recommend an interval of one second or more between calls.

#### Sample response for prebuilt-invoice

:::moniker range="doc-intel-4.0.0"

```json
{
    "status": "succeeded",
    "createdDateTime": "2024-03-25T19:31:37Z",
    "lastUpdatedDateTime": "2024-03-25T19:31:43Z",
    "analyzeResult": {
        "apiVersion": "2024-07-31-preview",
        "modelId": "prebuilt-invoice",
        "stringIndexType": "textElements"...
    ..."pages": [
            {
                "pageNumber": 1,
                "angle": 0,
                "width": 8.5,
                "height": 11,
                "unit": "inch",
                "words": [
                    {
                        "content": "CONTOSO",
                        "boundingBox": [
                            0.5911,
                            0.6857,
                            1.7451,
                            0.6857,
                            1.7451,
                            0.8664,
                            0.5911,
                            0.8664
                        ],
                        "confidence": 1,
                        "span": {
                            "offset": 0,
                            "length": 7
                                }
                      }],
              }]
      }
}
```

:::moniker-end

:::moniker range="doc-intel-3.1.0"

```json
{
    "status": "succeeded",
    "createdDateTime": "2023-08-25T19:31:37Z",
    "lastUpdatedDateTime": "2023-08-25T19:31:43Z",
    "analyzeResult": {
        "apiVersion": "2023-07-31",
        "modelId": "prebuilt-invoice",
        "stringIndexType": "textElements"...
    ..."pages": [
            {
                "pageNumber": 1,
                "angle": 0,
                "width": 8.5,
                "height": 11,
                "unit": "inch",
                "words": [
                    {
                        "content": "CONTOSO",
                        "boundingBox": [
                            0.5911,
                            0.6857,
                            1.7451,
                            0.6857,
                            1.7451,
                            0.8664,
                            0.5911,
                            0.8664
                        ],
                        "confidence": 1,
                        "span": {
                            "offset": 0,
                            "length": 7
                                }
                      }],
              }]
      }
}
```

:::moniker-end

:::moniker range="doc-intel-3.0.0"

```json
{
    "status": "succeeded",
    "createdDateTime": "2022-09-25T19:31:37Z",
    "lastUpdatedDateTime": "2022-09-25T19:31:43Z",
    "analyzeResult": {
        "apiVersion": "2022-08-31",
        "modelId": "prebuilt-invoice",
        "stringIndexType": "textElements"...
    ..."pages": [
            {
                "pageNumber": 1,
                "angle": 0,
                "width": 8.5,
                "height": 11,
                "unit": "inch",
                "words": [
                    {
                        "content": "CONTOSO",
                        "boundingBox": [
                            0.5911,
                            0.6857,
                            1.7451,
                            0.6857,
                            1.7451,
                            0.8664,
                            0.5911,
                            0.8664
                        ],
                        "confidence": 1,
                        "span": {
                            "offset": 0,
                            "length": 7
                                }
                      }],
              }]
      }
}
```

:::moniker-end

#### Supported document fields

The prebuilt models extract predefined sets of document fields. See [Model data extraction](../../model-overview.md#model-data-extraction) for extracted field names, types, descriptions, and examples.
