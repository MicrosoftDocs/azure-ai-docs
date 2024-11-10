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

* Azure AI Content Understanding is a new generative AI-based [**Azure AI Service**](../../what-are-ai-services.md) that analyzes files of any modality (documents, images, videos, and audio) and extracts structured output in user-defined field formats.

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

# [Document](#tab/document)

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
        "method": "extract",
        "description": "Vendor issuing the invoice"
      },
      "Items": {
        "type": "array",
        "method": "extract",
        "items": {
          "type": "object",
          "properties": {
            "Description": {
              "type": "string",
              "method": "extract",
              "description": "Description of the item"
            },
            "Amount": {
              "type": "number",
              "method": "extract",
              "description": "Amount of the item"
            }
          }
        }
      }
    }
  }
}
```

# [Image](#tab/image)

To create a custom analyzer, you need to define a field schema that describes the structured data you want to extract. In the following example, we define a schema for identifying detects in images of metal plates.

First, create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample chart analyzer",
  "scenario": "image",
  "fieldSchema": {
    "fields": {
      "Title": {
        "type": "string"
      },
      "ChartType": {
        "type": "string",
        "method": "classify",
        "enum": [ "bar", "line", "pie" ]
      }
    }
  }
}
```

# [Audio](#tab/audio)

To create a custom analyzer, you need to define a field schema that describes the structured data you want to extract. In the following example, we define a schema for extracting basic information from call transcripts.

First, create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample call transcript analyzer",
  "scenario": "callCenter",
  "config": {
    "returnDetails": true,
    "locales": ["en-US"]
  },
  "fieldSchema": {
    "fields": {
      "Summary": {
        "type": "string",
        "method": "generate"
      },
      "Sentiment": {
        "type": "string",
        "method": "classify",
        "enum": [ "Positive", "Neutral", "Negative" ]
      },
      "People": {
        "type": "array",
        "description": "List of people mentioned",
        "items": {
          "type": "object",
          "properties": {
            "Name": { "type": "string" },
            "Role": { "type": "string" }
          }
        }
      }
    }
  }
}
```

# [Video](#tab/video)

To create a custom analyzer, you need to define a field schema that describes the structured data you want to extract. In the following example, we define a schema for extracting basic information from marketing videos.

First, create a JSON file named `request_body.json` with the following content:
```json
{
  "description": "Sample marketing video analyzer",
  "scenario": "videoShot",
  "config": {
    "returnDetails": true
  },
  "fieldSchema": {
    "fields": {
      "Description": {
        "type": "string",
        "description": "Detailed summary of the video segment, focusing on product characteristics, lighting, and color palette."
      },
      "Sentiment": {
        "type": "string",
        "method": "classify",
        "enum": [ "Positive", "Neutral", "Negative" ]
      }
    }
  }
}
```

---

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

# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS) or the sample URL `https://github.com/Azure-Samples/cognitive-services-REST-api-samples/raw/master/curl/form-recognizer/rest-api/invoice.pdf`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS).

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS).

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze, such as a path to an Azure Storage Blob with a shared access signature (SAS).

---

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

# [Document](#tab/document)

```json
{
  "id": "f87e468b-d96b-488c-a646-33cc5823972f",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_invoice_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:36:31Z",
    "contents": [
      {
        "markdown": "CONTOSO LTD.\n\n\n# INVOICE\n\nContoso Headquarters...",
        "fields": {
          "VendorName": {
            "type": "string",
            "valueString": "CONTOSO LTD.",
            "spans": [ { "offset": 0, "length": 12 } ],
            "confidence": 0.941,
            "source": "D(1,0.5729,0.6582,2.3353,0.6582,2.3353,0.8957,0.5729,0.8957)"
          },
          "Items": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Description": {
                    "type": "string",
                    "valueString": "Consulting Services",
                    "spans": [ { "offset": 909, "length": 19 } ],
                    "confidence": 0.971,
                    "source": "D(1,2.3264,5.673,3.6413,5.673,3.6413,5.8402,2.3264,5.8402)"
                  },
                  "Amount": {
                    "type": "number",
                    "valueNumber": 60,
                    "spans": [ { "offset": 995, "length": 6 }
                    ],
                    "confidence": 0.988,
                    "source": "D(1,7.4507,5.6684,7.9245,5.6684,7.9245,5.8323,7.4507,5.8323)"
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "inch",
        "pages": [
          {
            "pageNumber": 1,
            "angle": -0.0039,
            "width": 8.5,
            "height": 11
          }
        ]
      }
    ]
  }
}
```

# [Image](#tab/image)

```json
{
  "id": "12fd421b-b545-4d63-93a5-01284081bbe1",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_chart_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:41:00Z",
    "contents": [
      {
        "markdown": "![image](image)\n",
        "fields": {
          "Title": {
            "type": "string",
            "valueString": "Weekly Work Hours Distribution"
          },
          "ChartType": {
            "type": "string",
            "valueString": "pie"
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "pixel",
        "pages": [
          {
            "pageNumber": 1,
            "width": 1283,
            "height": 617
          }
        ]
      }
    ]
  }
}
```

# [Audio](#tab/audio)

```json
{
  "id": "247c369c-1aa5-4f92-b033-a8e4318e1c02",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_chart_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:42:58Z",
    "contents": [
      {
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 32182,
        "markdown": "```WEBVTT\n\n00:00.080 --> 00:00.640\n<v Agent>Good day...",
        "fields": {
          "Sentiment": {
            "type": "string",
            "valueString": "Positive"
          },
          "Summary": {
            "type": "string",
            "valueString": "Maria Smith contacted Contoso to inquire about her current point balance. Agent John Doe confirmed her identity and informed her that she has 599 points. Maria did not require any further information and the call ended on a positive note."
          },
          "People": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Name": {
                    "type": "string",
                    "valueString": "Maria Smith"
                  },
                  "Role": {
                    "type": "string",
                    "valueString": "Customer"
                  }
                }
              }, ...
            ]
          }
        },
        "transcriptPhrases": [
          {
            "speaker": "Agent 1",
            "startTimeMs": 80,
            "endTimeMs": 640,
            "text": "Good day.",
            "confidence": 0.932,
            "words": [
              {
                "startTimeMs": 80,
                "endTimeMs": 280,
                "text": "Good"
              }, ...
            ],
            "locale": "en-US"
          }, ...
        ]
      }
    ]
  }
}
```

# [Video](#tab/video)

```json
{
  "id": "204fb777-e961-4d6d-a6b1-6e02c773d72c",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_marketing_video_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-09T08:57:21Z",
    "warnings": [],
    "contents": [
      {
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 2800,
        "width": 540,
        "height": 960,
        "markdown": "# Shot 0:0.0 => 0:2.800\n\n## Transcript\n\n```\n\nWEBVTT\n\n0:0.80 --> 0:10.560\n<v Speaker>When I was planning my trip...",
        "fields": {
          "sentiment": {
            "type": "string",
            "valueString": "Neutral"
          },
          "description": {
            "type": "string",
            "valueString": "The video begins with a view from a glass floor, showing a person's feet in white sneakers standing on it. The scene captures a downward view of a structure, possibly a tower, with a grid pattern on the floor and a clear view of the ground below. The lighting is bright, suggesting a sunny day, and the colors are dominated by the orange of the structure and the gray of the floor."
          }
        }
      },
      ...
    ]
  }
}```

---

## Next steps 

* In this quickstart, you learned how to call the REST API to create a custom analyzer. For a user experience, try [**Azure AI Foundry**](). 
* Explore more analyzer templates in our [GitHub repository]().

