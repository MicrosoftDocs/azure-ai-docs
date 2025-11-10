---
title: "Quickstart: Azure AI Content Understanding REST APIs"
titleSuffix: Azure AI services
description: Learn about Content Understanding REST APIs
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 07/15/2025
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.custom:
  - build-2025
---

# Quickstart: Use Azure AI Content Understanding REST API

* This quickstart shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-11-01&preserve-view=true) to get structured data from multimodal content in document, image, audio, and video files.

## Prerequisites

* To get started, you need **an active Azure subscription**. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* Once you have your Azure subscription, create an [Azure AI Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. Be sure to create it in a [supported region](/azure/ai-services/content-understanding/language-region-support).
   * This resource is listed under **AI Foundry** > **AI Foundry** in the portal.
     :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the AI Foundry resource page in the Azure portal.":::
* In this guide, we use the cURL command line tool. If it isn't installed, you can [download](https://everything.curl.dev/install/index.html) the appropriate version for your dev environment.

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt document, image, audio, and video analyzers to help you get started.

### Send file for analysis

Before running the following cURL command, make the following changes to the HTTP request:
# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Foundry instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-document`. This analyzer extracts text and layout elements such as paragraphs, sections, and tables from a document.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Foundry instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-image`. This analyzer generates a description of the image.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg`.

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Foundry instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-audio`. This analyzer extracts the audio transcript, generates a summary, and performs speaker labeling.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav`.

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Foundry instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-video`. This analyzer extracts keyframes, transcript, and chapter segments from video.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4`.
---

#### POST request

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "{fileUrl}"
          }
        ]
      }'  
```

#### POST response
The response `header` includes a ```Operation-Location```, which you use to retrieve the results of the asynchronous analysis operation. 

```
HTTP/1.1 202 Accepted
Transfer-Encoding: chunked
Content-Type: application/json
request-id: aaa-bbb-ccc-ddd
x-ms-request-id: aaa-bbb-ccc-ddd
Operation-Location: {endpoint}/contentunderstanding/analyzerResults/{request-id}?api-version=2025-11-01
api-supported-versions: 2024-12-01-preview,2025-05-01-preview,2025-11-01
x-envoy-upstream-service-time: 800
apim-request-id: {request-id}
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
x-content-type-options: nosniff
x-ms-region: West US
Date: Fri, 31 Oct 2025 05:30:17 GMT
Connection: close
```

### Get analyze result

Use the `Operation-Location` from the [`POST` response](#post-response) and retrieve the result of the analysis.

#### GET request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzerResults/{request-id}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

#### GET response

The 200 (`OK`) JSON response includes a `status` field indicating the status of the operation. If the operation isn't complete, the value of `status` is `Running` or `NotStarted`. In such cases, you should send the `GET` request again, either manually or through a script. Wait an interval of one second or more between calls.

# [Document](#tab/document)

```json
{
  "id": "<request-id>",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-document",
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "path": "input1",
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
            "angle": 0,
            "width": 8.5,
            "height": 11,
          }
        ],
        "analyzerId": "prebuilt-document",
        "mimeType": "application/pdf"
      }
    ]
  },
  "usage": {
		"documentPages": 1,
		"tokens": {
			"contextualization": 1000,
		}
	}
}
```

# [Image](#tab/image)

```json
{
  "id": "<request-id>",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-image",
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "warnings": [],
    "contents": [
      {
        "path": "input1",
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
  },
  "usage": {
		"tokens": {
			"contextualization": 1000,
			"input": 1866,
			"output": 87
		}
	}
}
```

# [Audio](#tab/audio)

```json
{
  "id": "<request-id>",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-audio",
    "apiVersion": "2025-11-01",
    "createdAt": "YYYY-MM-DDTHH:MM:SSZ",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "path": "input1",
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
        "analyzerId": "prebuilt-audio",
        "mimeType": "audio/wav"
      }
    ]
  },
  "usage": {
		"audioHours": 0.032,
    "tokens": {
      "contextualization": 3194.445
		}
	}
}
```

# [Video](#tab/video)

```json
{
  "id": "<request-id>",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-video",
    "apiVersion": "2025-11-01",
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
        "mimeType": "video/x-m4v"
      }
    ]
  },
  "usage": {
		"videoHours": 0.013,
    "tokens": {
      "contextualization": 12222.223
	}
}
```

---

## Next step

Now that you know how to invoke the analysis operation, learn more about building [custom analyzers](../tutorial/create-custom-analyzer.md) for your use case.
