---
title: "Quickstart: Azure AI Content Understanding REST APIs"
titleSuffix: Azure AI services
description: Learn about Content Understanding REST APIs
author: laujan
ms.author: paulhsu
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/19/2025
---

# Quickstart: Azure AI Content Understanding REST APIs

* This quickstart shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) to get structured data from multimodal content in document, image, audio, and video files.

* Try [Content Understanding with no code on Azure AI Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding)

## Prerequisites

To get started, you need **an active Azure subscription**. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/free/).

* Once you have your Azure subscription, create an [Azure AI Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. This multi-service resource enables access to multiple Azure AI services with a single set of credentials.

   * This resource is listed under **AI Foundry** > **AI Foundry** in the portal.

    > [!IMPORTANT]
    > Azure provides more than one resource type for Azure AI services. Make certain that you select the one listed under **AI Foundry** > **AI Foundry** as depicted in the following image. For more information, see [Create an Azure AI Foundry resource](../how-to/create-multi-service-resource.md).

     :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the AI Foundry resource page in the Azure portal.":::

* In this quickstart, we use the cURL command line tool. If it isn't installed, you can download a version for your dev environment: [cURL download page](https://curl.se/download.html).

## Get Started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt document, image, audio, and video analyzers to help you get started.

### Send file for analysis

Before running the following cURL command, make the following changes to the HTTP request:
# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-documentAnalyzer`. This analyzer extracts text and layout elements such as paragraphs, sections, and tables from a document.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-imageAnalyzer`. This analyzer generates a description of the image.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg`.

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-audioAnalyzer`. This analyzer extracts the audio transcript, generates a summary, and performs speaker labeling.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav`.

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-videoAnalyzer`. This analyzer extracts keyframes, transcript, and chapter segments from video.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4`.
---

#### POST request

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"{fileUrl}\"}"
```

#### POST response
The response includes a JSON body containing the `resultId`, which you use to retrieve the results of the asynchronous analysis operation. Additionally, the `Operation-Location` header provides the direct URL to access the analysis result.

```
202 Accepted
Operation-Location: {endpoint}/contentunderstanding/analyzerResults/{resultId}?api-version=2024-12-01-preview
{
  "id": {resultId},
  "status": "Running",
  "result": {
    "analyzerId": {analyzerId},
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": []
  }
}
```

### Get analyze result

Use the `resultId` from the [`POST` response](#post-response) and retrieve the result of the analysis.

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{resultId}` with the `resultId` from the `POST` response.

#### GET request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzerResults/{resultId}?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

#### GET response

The 200 (`OK`) JSON response includes a `status` field indicating the status of the operation. If the operation isn't complete, the value of `status` is `Running` or `NotStarted`. In such cases, you should send the `GET` request again, either manually or through a script. Wait an interval of one second or more between calls.

# [Document](#tab/document)

```json
{
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-documentAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "markdown": "CONTOSO LTD.\n\n\n# INVOICE\n\nContoso Headquarters\n123 456th St...",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "This document is an invoice issued by Contoso Ltd. to Microsoft Corporation for services rendered during the period of 10/14/2019 to 11/14/2019..."
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
                "confidence": 0.998,
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
          },
          {
            "role": "title",
            "content": "INVOICE",
            "source": "D(1,7.0515,0.5614,8.0064,0.5628,8.006,0.791,7.0512,0.7897)",
            "span": { "offset": 15, "length": 9 }
          }, ...
        ],
        "sections": [
          {
            "span": { "offset": 0, "length": 1649 },
            "elements": [ "/sections/1", "/sections/2" ]
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
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-imageAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "markdown": "![image](image)\n",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "The image is a pie chart depicting the distribution of hours worked per week among a group of individuals. The chart is divided into four segments: 60+ hours (37.8%), 50-60 hours (36.6%), 40-50 hours (18.9%), and 1-39 hours (6.7%). Each segment is labeled with its corresponding percentage and color-coded for clarity."
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "pixel",
        "pages": [
          {
            "pageNumber": 1,
            "spans": []
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
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-audioAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Audio: 00:00.000 => 01:54.670\n\nTranscript\n```\nWEBVTT\n\n00:00.080 --> 00:02.160\n<v Speaker 1>Thank you for calling Woodgrove Travel...",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "John Smith contacted Woodgrove Travel to report a negative experience with his flight from New York City to Los Angeles..."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 114670,
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 80,
            "endTimeMs": 2160,
            "text": "Thank you for calling Woodgrove Travel.",
            "words": [
              {
                "startTimeMs": 80,
                "endTimeMs": 280,
                "text": "Thank"
              }, ...
            ]
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
  "id": {resultId},
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-videoAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Video: 00:00.000 => 00:43.866\nWidth: 1080\nHeight: 608\n\n## Segment 1: 00:00.000 => 00:07.367\nThe video begins with a scenic aerial view featuring the Flight Simulator and Microsoft Azure AI logos...\n\nTranscript\n```\nWEBVTT\n\n00:01.400 --> 00:06.560\n<Speaker 1 Speaker>When it comes to the neural TTS, in order to get a good voice, it's better to have good data.\n```\n\nKey Frames\n- 00:00.726 ![](keyFrame.726.jpg)...",
        "fields": {
          "Segments": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "SegmentId": {
                    "type": "string",
                    "valueString": "1"
                  }
                }
              }, ...
            ]
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 43866,
        "width": 1080,
        "height": 608,
        "KeyFrameTimesMs": [ 726, 2046, ... ],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 1400,
            "endTimeMs": 6560,
            "text": "When it comes to the neural TTS, in order to get a good voice, it's better to have good data.",
            "words": []
          }, ...
        ],
        "cameraShotTimesMs": [ 1467, 3233, ... ],
        "segments": [
          {
            "startTimeMs": 0,
            "endTimeMs": 7367,
            "description": "The video begins with a scenic aerial view featuring the Flight Simulator and Microsoft Azure AI logos...",
            "segmentId": "1"
          }, ...
        ]
      }
    ]
  }
}
```

---

## Next steps

Learn more about [analyzers](../concepts/analyzer-templates.md) for your use case.



