---
title: "Quickstart: Azure AI Content Understanding REST APIs"
titleSuffix: Azure AI services
description: Learn about Content Understanding REST APIs
author: laujan
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure
ms.topic: quickstart
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# Quickstart: Azure AI Content Understanding REST APIs

* Get started with the Azure AI Content Understanding latest preview version REST API (2024-12-01-preview).

* Azure AI Content Understanding is a new Generative AI based Azure AI Service, designed to process/ingest content of any modality - documents, images, videos, and audio into a user-defined output format. 

* You can easily integrate the Content Understanding service into your workflows and applications by calling our REST APIs.

* This quickstart guides you on using the Content Understanding REST API to use a custom or prebuilt analyzer (available for some file formats) to analyze and extract data and values from your input. 

* For instructions on using our prebuilt analyzer with the REST API, refer to this [**quickstart**]() guide.

## Prerequisites

To use Content Understanding, you need an Azure AI services multi-service resource. The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

* To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).

* Once you have your Azure subscription, create an [**Azure AI services multi-services resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal as shown here:

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource types named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.

    For more information, *see* [Create an Azure AI services multi-services resource](../how-to/create-multi-service-resource.md)

* curl command line tool installed.

  * [Windows](https://curl.haxx.se/windows/)
  * [Mac or Linux](https://learn2torials.com/thread/how-to-install-curl-on-mac-or-linux-(ubuntu)-or-windows)

## Create an analyzer (PUT request)

To create custom analyzer, a schema definition input is required. The following steps show you how to use a sample schema to create a custom analyzer. 

To utilize any of our prebuilt analyzers(currently available for documents), skip this step and call the POST request to analyze with our prebuilt analyzers.

Before you run the cURL command and call the PUT request to create an analyzer and view the status of the operation, make the following changes to the HTTP request:

1. Replace {endpoint} with the endpoint value from your Azure portal AI service resource instance.

1. Replace {key} with the key value from your Azure portal AI Service resource instance.

1. Replace `{analyzerID}` with the name you wish to name your analyzer.

1. Open a command prompt window.

1. Copy and Past your edited curl command from the text editor into the command prompt window, and then run the command.

### PUT Request

  ```bash
  curl -v -i PUT "{endpoint}/multimodalintelligence/analyzers/{analyzerId}:analyze?api-version=2024-12-01-preview" "Ocp-Apim-Subscription-Key: {key}" -H "Content-Type: application/json" -d @request_body.json
  ```
 
 The following code a sample template schema definition in a `request_body.json` file:

```json
{
    "description": "Analyzer to extract content from video ",
    "scenario": "Video",
    "fieldSchema": {
        "fields": {
           "Brand": {
                "type": "string",
                "kind": "generate",
                "description": "Identify the brand being promoted in the video."
            },
            "Topics": {
                "type": "string",
                "kind": "generate",
                "description": "Top 5 topics mentioned in the video"
            }
        },
        "trainingData": {
        "containerUrl": "{container SAS URL}",
        "kind": "blob",
        "prefix": "blobprefix"
    }
    }
}

```
> [!NOTE]
> The `trainingData` section is optional and only required when a schema has been generated from training data via Azure AI Studio. 
> The value is limited to document file format. 
> If you use `trainingData` replace the `containerUrl` with the SAS URL to your training data storage.

## Analyze a file (POST Request)
Call the POST Request to analyze and extract data from a file. 

Before you run the cURL command, make the following changes to the HTTP request:

1. Replace {endpoint} with the endpoint value from your Azure portal AI service resource instance.

1. Replace {key} with the key value from your Azure portal AI Service resource instance.

1. Replace `{analyzerID}` with the name of a custom or an analyzer from the [**prebuilt analyzers table**](#prebuilt-analyzers).

1. Replace `{image SAS URL}` with your generated shared access signature (SAS) URL from your Azure Blob Storage.

1. Open a command prompt window.

1. Copy and Past your edited curl command from the text editor into the command prompt window, and then run the command.

```bash
  curl -v -i PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2024-12-01-preview" "Ocp-Apim-Subscription-Key: {key}" -H "Content-Type: application/json" -d {"url":"{image SAS URL}"}
  ```

After the POST request is successful, grab the resultId (needed for the `GET` request) from the response header values.

#### Prebuilt Analyzers

Prebuilt Analyzers are available for document files. To use any of these prebuilt analyzers, replace the `{analyzerID}` with the name of the prebuilt analyzer.

|Prebuilt Analyzer Name| Description|
|--------|-------|
|prebuilt-read| Extracts data from documents and scanned images.|
|prebuilt-layout|  Extracts regions of interest including text, tables, table headers, selection marks, and structure information from documents and scanned images.|


## Get analyze results (GET Request)

Call the Get analyze result API to retrieve the extracted data.

1. Replace {endpoint} with the endpoint value from your Azure portal AI service resource instance.

1. Replace {key} with the key value from your Azure portal AI Service resource instance.

1. Replace `{analyzerID}` with the name of a custom or prebuilt analyzer.
1. Replace `{resultID}` with the resultId returned from the POST request.
1. Open a command prompt window.

1. Copy and Past your edited curl command from the text editor into the command prompt window, and then run the command.

```bash
    curl -v -X GET "{endpoint}/multimodalintelligence/analyzers/{analyzerId}/results/{resultId}api-version=2024-12-01-preview" -H "Ocp-Apim-Subscription-Key: {key}"

```

### Examine the response
A successful response is 200 with JSON output. The first field, `status`, indicates the status of the operation. If the operation isn't complete, the value of `status` is `running` or `notStarted`; you should call the API again, either manually or through a script. We recommend an interval of one second or more between calls.

### Sample response

```json
{
  "status": "succeeded",
  "createdDateTime": "2024-09-12T12:34:56Z",
  "lastUpdatedDateTime": "2024-09-12T12:35:56Z",
  "analyzeResult": {
    "metadata": {
      "width": 1920,
      "height": 1080,
      "duration": "00:05:00"
    },
    "documents": [
      {
        "fields": {
          "Brand": {
            "type": "string",
            "content": "A promotional video showcasing the features of Contoso's new electric car model.",
            "confidence": 0.95
          },
          "Topics": {
            "type": "string",
            "content": "Car, Eletric, Automobile, Transportation, Insurance",
            "confidence": 0.90
          },
        }
      }
    ]
  }
}


```
## Next steps 

In this quickstart, you learned how to call the REST API. For a user experience, try [**Azure AI Studio**](). 

For more scenario-based samples/quickstarts, learn about our [**Scenario Guides**](). 
