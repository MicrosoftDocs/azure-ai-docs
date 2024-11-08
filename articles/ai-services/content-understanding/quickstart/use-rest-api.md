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
---

# Quickstart: Azure AI Content Understanding REST APIs

* Start using the latest preview version of the Azure AI Content Understanding REST API (2024-12-01-preview).

* Azure AI Content Understanding is a new generative AI-based [**Azure AI Service**](../what-are-ai-services.md) that analyzes files of any modality (documents, images, videos, and audio) and extracts structured output in user-defined field formats.

* Integrate the Content Understanding service into your workflows and applications easily by calling our REST APIs.

* This quickstart guides you through using the Content Understanding REST API to create a custom analyzer and extract content and fields from your input.

## Prerequisites

To use Content Understanding, you need an Azure AI Services resource. This resource provides access to multiple Azure AI services with a single set of credentials.

1. Get an Azure account:
   - If you don't have an Azure account, you can [create a free subscription](https://azure.microsoft.com/free/).

2. Create an Azure AI Services resource:
   - Once you have an Azure subscription, create an [Azure AI Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. 
   - This resource is listed under Azure AI services → Azure AI services in the portal.

    :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

    > [!IMPORTANT]
    > Azure provides more than one resource type named Azure AI services. Ensure you select the one listed under Azure AI services → Azure AI services with the logo shown above.

   For more information, see [Create an Azure AI Services resource](../how-to/create-multi-service-resource.md).

3. Install [cURL](https://curl.se/) command line tool.

## Create a custom analyzer

To create a custom analyzer, you need to define a field schema that describes the structured data you want to extract. In the following example, we define a schema for extracting basic information from an invoice document.

First, create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample invoice analyzer",
  "scenario": "document",
  "fieldSchema": {
    "fields": {
      "VendorName": {
        "type": "string",
        "kind": "extract",
        "description": "Vendor issuing the invoice"
      },
      "Items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Description": {
              "type": "string",
              "kind": "extract",
              "description": "Description of the item"
            },
            "Amount": {
              "type": "number",
              "kind": "extract",
              "description": "Amount of the item"
            }
          }
        }
      }
    }
  }
}
```

Before running the following `cURL` commands, make the following changes to the HTTP request:

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the new analyzer to create, such as `myInvoice`.

### PUT Request

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```

### PUT Response

You will receive a 201 (Created) response that includes an `Operation-Location` header containing a URL that you can use to track the status of this asynchronous creation operation.

```
201 Created
Operation-Location: {endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2024-12-01-preview
```

Upon completion, performing an HTTP GET on the URL will return `"status": "succeeded"`.

```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{analyzerId}/operations/{operationId}?api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```


## Analyze a file

You can analyze files using the custom analyzer you created to extract the fields defined in the schema.

Before running the cURL command, make the following changes to the HTTP request:

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf`.

### POST request
```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?stringEncoding=codePoint&api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"{fileUrl}\"}"
```

### POST response

You will receive a 202 (Accepted) response that includes an `Operation-Location` header containing a URL that you can use to track the status of this asynchronous analyze operation.

```
202 Accepted
Operation-Location: {endpoint}/contentunderstanding/analyzers/{analyzerId}/results/{resultId}?api-version=2024-12-01-preview
```

## Get analyze result

Use the `resultId` from the `Operation-Location` header returned by the previous POST response to retrieve the result of the analysis.

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{resultId}` with the `resultId` returned from the POST request.

### GET request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{analyzerId}/results/{resultId}?api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

### GET response

You will receive a 200 (OK) JSON response with a `status` field indicating the status of the operation. If the operation isn't complete, the value of `status` will be `running` or `notStarted`. In such cases, you should call the API again, either manually or through a script, with an interval of one second or more between calls.

#### Sample response

```json
{
  "id": "3b31320d-8bab-4f88-b19c-2322a7f11034",
  "status": "Succeeded",
  "result": {
    "analyzerId": "myInvoice",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-10-14T18:46:36Z",
    "stringEncoding": "codePoint",
    "contents": [
      {
        "kind": "document",
        "markdown": "# CONTOSO LTD.\n\n...",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "inch",
        "pages": [
          {
            "pageNumber": 1,
            "width": 8.5,
            "height": 11
          }
        ],
        "fields": {
          "Company": {
            "type": "string",
            "valueString": "CONTOSO",
            "spans": [
              {
                "offset": 7,
                "length": 2
              }
            ],
            "confidence": 0.95,
            "source": "D(1,5,1,7,1,7,1.5,5,1.5)"
          }
        }
      }
    ]
  }
}
```

## Next steps 

* In this quickstart, you learned how to call the REST API to create a custom analyzer. For a user experience, try [**Azure AI Foundry**](). 

* Explore more analyzer templates in our [GitHub repository]().
<!-- For more scenario-based samples/quickstarts, learn about our [**Scenario Guides**]().  -->
