---
title: "Quickstart: Azure AI Content Understanding REST APIs"
titleSuffix: Azure AI services
description: Learn about Content Understanding REST APIs
author: laujan
ms.author: tonyeiyalla
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 04/14/2025
---

# Quickstart: Azure AI Content Understanding REST APIs

* This quickstart shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) to get structured data from multimodal content in documents, videos, images, and audio files.

* Try the [Content Understanding API with no code on Azure AI Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding)

## Prerequisites

To get started, you need **An Active Azure Subscription**. If you don't have an Azure Account, [create one for free](https://azure.microsoft.com/free/).

* Once you have your Azure subscription, create an [Azure AI Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) in the Azure portal. This multi-service resource enables access to multiple Azure AI services with a single set of credentials.

   * This resource is listed under Azure AI services → Azure AI services in the portal.

    > [!IMPORTANT]
    > Azure provides more than one resource type named Azure AI services. Make certain that you select the one listed under Azure AI services → Azure AI services as depicted in the following image. For more information, see [Create an Azure AI Services resource](../how-to/create-multi-service-resource.md).

     :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

* In this quickstart, we use the cURL command line tool. If it isn't installed, you can download a version for your dev environment:

  * [Windows](https://curl.haxx.se/windows/)
  * [Mac or Linux](https://learn2torials.com/thread/how-to-install-curl-on-mac-or-linux-(ubuntu)-or-windows)


## Get Started with a Prebuilt Analyzer
Analyzers define how your content will be processed and the insights that will be extracted. We offer [pre-built analyzers](link to pre-built analyzer page) for common use cases. You can [customize pre-built analyzers](link to learn how to customize analyzers) to better fit your specific needs and use cases. 
This quickstart uses pre-built analyzers to help you get started. 

Before running the cURL command, make the following changes to the HTTP request:
### POST request
```bash
curl -i -X POST "{endpoint}/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"{fileUrl}\"}"
```

# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal
2. Replace `{analyzerId}` with  `prebuilt-documentAnalyzer`.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/data/invoice.pdf`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal
2. Replace `{analyzerId}` with  `prebuilt-imageAnalyzer`
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/data/pieChart.jpg`

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal
2. Replace `{analyzerId}` with  `prebuilt-audioAnalyzer`
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/data/audio.wav`

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal
2. Replace `{analyzerId}` with  `prebuilt-videoAnalyzer`
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/data/FlightSimulator.mp4`
---


### POST response

The 202 (`Accepted`) response includes an `Operation-Location` header containing a URL that you can use to track the status of this asynchronous analyze operation.

```
202 Accepted
Operation-Location: {endpoint}/contentunderstanding/analyzers/{analyzerId}/results/{resultId}?api-version=2024-12-01-preview
```

## Get analyze result

Use the `resultId` from the `Operation-Location` header returned by the previous `POST` response and retrieve the result of the analysis.

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
1. Replace `{analyzerId}` with the name of the custom analyzer created earlier.
1. Replace `{resultId}` with the `resultId` returned from the `POST` request.

### GET request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{analyzerId}/results/{resultId}?api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

### GET response

The 200 (`OK`) JSON response includes a `status` field indicating the status of the operation. If the operation isn't complete, the value of `status` is `running` or `notStarted`. In such cases, you should call the API again, either manually or through a script. Wait an interval of one second or more between calls.

#### Sample response

# [Document](#tab/document)

```json
{
  "id": "bcf8c7c7-03ab-4204-b22c-2b34203ef5db",
  "status": "Succeeded",
  "result": {
    "analyzerId": "sample_invoice_analyzer",
    "apiVersion": "2024-12-01-preview",
    "createdAt": "2024-11-13T07:15:46Z",
    "warnings": [],
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
                    "spans": [ { "offset": 995, "length": 6 } ],
                    "confidence": 0.989,
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
            "height": 11,
            "spans": [ { "offset": 0, "length": 1650 } ],
            "words": [
              {
                "content": "CONTOSO",
                "span": { "offset": 0, "length": 7 },
                "confidence": 0.997,
                "source": "D(1,0.5739,0.6582,1.7446,0.6595,1.7434,0.8952,0.5729,0.8915)"
              }, ...
            ],
            "lines": [
              {
                "content": "CONTOSO LTD.",
                "source": "D(1,0.5734,0.6563,2.335,0.6601,2.3345,0.8933,0.5729,0.8895)",
                "span": { "offset": 0, "length": 12 }
              }, ...
            ]
          }
        ],
        "paragraphs": [
          {
            "content": "CONTOSO LTD.",
            "source": "D(1,0.5734,0.6563,2.335,0.6601,2.3345,0.8933,0.5729,0.8895)",
            "span": { "offset": 0, "length": 12 }
          }, ...
        ],
        "sections": [
          {
            "span": { "offset": 0, "length": 1649 },
            "elements": [ "/sections/1", "/sections/2" ]
          },
          {
            "span": { "offset": 0, "length": 12 },
            "elements": [ "/paragraphs/0" ]
          }, ...
        ],
        "tables": [
          {
            "rowCount": 2,
            "columnCount": 6,
            "cells": [
              {
                "kind": "columnHeader",
                "rowIndex": 0,
                "columnIndex": 0,
                "rowSpan": 1,
                "columnSpan": 1,
                "content": "SALESPERSON",
                "source": "D(1,0.5389,4.5514,1.7505,4.5514,1.7505,4.8364,0.5389,4.8364)",
                "span": { "offset": 512, "length": 11 },
                "elements": [ "/paragraphs/19" ]
              }, ...
            ],
            "source": "D(1,0.4885,4.5543,8.0163,4.5539,8.015,5.1207,0.4879,5.1209)",
            "span": { "offset": 495, "length": 228 }
          }, ...
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
    "warnings": [],
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
    "warnings": [],
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
        "markdown": "# Shot 0:0.0 => 0:1.800\n\n## Transcript\n\n```\n\nWEBVTT\n\n0:0.80 --> 0:10.560\n<v Speaker>When I was planning my trip...",
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
}
```

---

## Next steps

* In this quickstart, you learned how to call the [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true) to create a custom analyzer. For a user experience, try [**Azure AI Foundry portal**](https://ai.azure.com/).


