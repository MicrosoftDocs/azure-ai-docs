---
title: "Quickstart: Azure AI Multimodal Intelligence REST APIs"
titleSuffix: Azure AI services
description: Learn about Multimodal Intelligence REST APIs
author: laujan
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure
ms.topic: quickstart
ms.date: 10/22/2024
---

# Quickstart: Multimodal Intelligence REST APIs

* Get started with the Azure AI Multimodal Intelligence latest preview version REST API (2024-12-01-preview).

* Azure AI Multimodal Intelligence is a cloud-based solution within [**Azure AI services**](../../what-are-ai-services.md), designed to process varied data modalities such as documents, images, videos, and audio within a unified workflow.

* The Multimodal Intelligence API provides you with AI algorithms for extracting data modalities and returns a structured JSON representation. Follow these steps to install a package to your application and try out the sample code.

 * In this quickstart, learn to use the Multimodal Intelligence REST API to analyze and extract data and values from  your schema input.

## Prerequisites

To use Multimodal Intelligence, you need an Azure AI services multi-service resource. The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

* To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).

* Once you have your Azure subscription, create an [**Azure AI services multi-services resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal as shown here:

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource types named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.

    For more information, *see* [Create an Azure AI services multi-services resource](../how-to-guide/create-multi-service-resource.md)

* * curl command line tool installed.

  * [Windows](https://curl.haxx.se/windows/)
  * [Mac or Linux](https://learn2torials.com/thread/how-to-install-curl-on-mac-or-linux-(ubuntu)-or-windows)

## Analyze a document

* A `POST` request is used to analyze all document types.

* A `GET` request is used to retrieve the result of a data analysis request.

* The `analyzerId` is used with `POST` requests.

* The  `resultId`  is used with `GET` operations.


##  Analyze document (POST)

Before you run the cURL command, make the following changes to the [POST request](#analyze-document-post):

1. Replace {endpoint} with the endpoint value from your Azure portal AI service resource instance.

1. Replace {key} with the key value from your Azure portal AI Service resource instance.

1. You need a document file at a URL. For this quickstart, you can use the sample forms provided in the following table for each feature.

1. Using the following table as a reference, replace `{analyzerID}` and `{your-document-url}` with your desired values.

    |Feature|{analyzerID}| {document-url}|
    |--------|-------|-------|
    |Audio|||
    |Video|||
    |Document|||
    |Image|||

1. Open a command prompt window.

1. Copy and Past your edited curl command from the text editor into the command prompt window, and then run the command.

  ```bash
  curl -v -i POST "{endpoint}/multimodalintelligence/analyzers/{analyzerId}:analyze?api-version=2024-12-01-preview" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: {key}" --data-ascii "{'urlSource': '{your-document-url}'}"
  ```

## Get analyze results (GET Request)

Call the Get analyze result API to get the status of the operation and the extracted data.

### GET Request

```bash
    curl -v -X GET "{endpoint}/multimodalintelligence/analyzers/{analyzerId}/results/{resultId}api-version=2024-12-01-preview" -H "Ocp-Apim-Subscription-Key: {key}"

```


### Examine the response
A successful response is 200 with JSON output. The first field, `status`, indicates the status of the operation. If the operation isn't complete, the value of `status` is `running` or `notStarted`; you should call the API again, either manually or through a script. We recommend an interval of one second or more between calls.

### Sample response

```json
{
  "fileType": "pdf",
  "documents": [
    {
      // Generic properties
      "documentId": "myFile.pdf",
      "kind": "visualDocument",

      // Content representation
      "content": "{markdown representation of document}",

      // Semantic field extraction
      "type": "invoice",
      "confidence": 0.95,
      "fields": {
        "VendorName": {
          "type": "string",
          "content": "Contoso",
          "value": "Contoso",
          "spans": [{ "offset": 10, "length", 7 }],
          "confidence": 0.98,
          "groundings": [ "VD({pageNumber}:{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4})" ]
        }
      }
    }
  ]
}

```
