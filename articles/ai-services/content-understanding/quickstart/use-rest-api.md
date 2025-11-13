---
title: "Quickstart: Azure Content Understanding in Foundry Tools REST APIs"
titleSuffix: Foundry Tools
description: Learn about Content Understanding REST APIs
author: PatrickFarley 
ms.author: paulhsu
manager: nitinme
ms.date: 07/15/2025
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Quickstart: Use Azure Content Understanding in Foundry Tools REST API

This quickstart shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-11-01&preserve-view=true) to get structured data from multimodal content in document, image, audio, and video files.

## Prerequisites

* To get started, you need **an active Azure subscription**. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* Once you have your Azure subscription, create an [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. Be sure to create it in a [supported region](/azure/ai-services/content-understanding/language-region-support).
   * This resource is listed under **AI Foundry** > **AI Foundry** in the portal.
     :::image type="content" source="../media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the AI Foundry resource page in the Azure portal.":::
* Once you have a Foundry resource, create a Foundry Model deployment of GPT-4.1 completion model and a text-embedding-3-large embedding model in your Foundry resource. For details on how to deploy these models, see [Create model deployments in Azure AI Foundry portal](/articles/ai-foundry/foundry-models/how-to/create-model-deployments.md?pivots=ai-foundry-portal).
* In this guide, we use the cURL command line tool. If it isn't installed, you can [download](https://everything.curl.dev/install/index.html) the appropriate version for your dev environment.

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.

### Send file for analysis

Before running the following cURL command, make the following changes to the HTTP request:

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Foundry instance in the Azure portal.
2. Replace `{CompletionDeploymentName}` with the name of your GPT-4.1 completion model deployment name.
3. Replace `{embeddingDeploymentName}` with the name of your text-embedding-3-large embedding model deployment name.

---

#### POST request

# [Document](#tab/document)

This example uses the `prebuilt-document` analyzer to extract structured data from an invoice document.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/prebuilt-document:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[{"url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"}],
        "modelDeployments": {
          "gpt-4.1": "{CompletionDeploymentName}",
          "text-embedding-3-large": "{embeddingDeploymentName}"
        }
      }'  
```

# [Image](#tab/image)

This example uses the `prebuilt-image` analyzer to generate a description of the image.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/prebuilt-image:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg"
          }          
        ],
        "modelDeployments": {
          "gpt-4.1": "{CompletionDeploymentName}",
          "text-embedding-3-large": "{embeddingDeploymentName}"
        }
      }'  
```

# [Audio](#tab/audio)

This example uses the `prebuilt-audio` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/prebuilt-audio:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav"
          }          
        ],
        "modelDeployments": {
          "gpt-4.1": "{CompletionDeploymentName}",
          "text-embedding-3-large": "{embeddingDeploymentName}"
        }
      }'  
```

# [Video](#tab/video)

This example uses the `prebuilt-video` analyzer to extract keyframes, transcript, and chapter segments from video.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/prebuilt-video:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4"
          }          
        ],
        "modelDeployments": {
          "gpt-4.1": "{CompletionDeploymentName}",
          "text-embedding-3-large": "{embeddingDeploymentName}"
        }
      }'  
```

---

#### POST response
The response header includes an `Operation-Location` field, which you use to retrieve the results of the asynchronous analysis operation. 

```
HTTP/1.1 202 Accepted
Transfer-Encoding: chunked
Content-Type: application/json
request-id: aaa-bbb-ccc-ddd
x-ms-request-id: aaa-bbb-ccc-ddd
Operation-Location: {endpoint}/contentunderstanding/analyzerResults/{request-id}?api-version=2025-11-01  // <--- Use this URL to check the analysis status
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
		"documentStandardPages": 1,
    "contextualizationToken": 1000,
    "tokens": {
      "gpt-4.1-input": 1234, 
      "gpt-4.1-output": 2345,
      "text-embedding-3-large": 3456 
    }
  }
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
		"contextualization": 1000,
    "tokens": {
      "gpt-4.1-input": 1234, 
      "gpt-4.1-output": 2345,
      "text-embedding-3-large": 3456 
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
    "analyzerId": "prebuilt-audioAnalyzer",
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
        "analyzerId": "prebuilt-audioAnalyzer",
        "mimeType": "audio/wav"
      }
    ]
  },
  "usage": {
		"audioHours": 0.032,
    "contextualization": 3194.445
    "tokens": {
      "gpt-4.1-input": 1234, 
      "gpt-4.1-output": 2345,
      "text-embedding-3-large": 3456 
    }
 
	}
}
```

# [Video](#tab/video)

```json
{
  "id": "2689a699-fa3a-4ddf-9a27-c34ceaa6c597",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-videoAnalyzer",
    "apiVersion": "2025-11-01",
    "createdAt": "2025-11-13T16:11:17Z",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Video: 00:00.733 => 00:15.467\nWidth: 1080\nHeight: 608\n\nTranscript\n```\nWEBVTT\n\n00:01.360 --> 00:06.640\n<Speaker 1>When it comes to the neural TTS, in order to get a good voice, it's better to have good data.\n\n00:07.120 --> 00:13.320\n<Speaker 2>To achieve that, we build a universal TTS model based on 3,000 hours of data.\n\n00:13.440 --> 00:23.680\n<Speaker 1>We actually accumulated tons of the data so that this universal model is able to capture the nuance of the audio and generate a more natural voice for the algorithm.\n```\n\nKey Frames\n- 00:00.733 ![](keyFrame.733.jpg)\n- 00:02.067 ![](keyFrame.2067.jpg)\n...\n- 00:14.833 ![](keyFrame.14833.jpg)\n- 00:15.467 ![](keyFrame.15467.jpg)",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "The video opens with a Flight Simulator logo alongside Microsoft Azure AI branding, followed by an interview with a man discussing the importance of good data for neural text-to-speech (TTS) technology. He explains the creation of a universal TTS model trained on 3,000 hours of data to capture audio nuances and produce natural-sounding voices. Visuals include audio waveform displays and shots of data centers and server rooms, emphasizing the technological infrastructure behind the TTS model."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 733,
        "endTimeMs": 15467,
        "width": 1080,
        "height": 608,
        "KeyFrameTimesMs": [
          733,
          2067
          /*... (14 additional keyframes)*/
        ],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 1360,
            "endTimeMs": 6640,
            "text": "When it comes to the neural TTS, in order to get a good voice, it's better to have good data.",
            "confidence": 0.937,
            "words": [
              {
                "startTimeMs": 1360,
                "endTimeMs": 1600,
                "text": "When"
              },
              {
                "startTimeMs": 1600,
                "endTimeMs": 1760,
                "text": "it"
              }
              /*... (18 additional words)*/
            ],
            "locale": "en-US"
          },
          {
            "speaker": "Speaker 2",
            "startTimeMs": 7120,
            "endTimeMs": 13320,
            "text": "To achieve that, we build a universal TTS model based on 3,000 hours of data.",
            "confidence": 0.937,
            "words": [
              {
                "startTimeMs": 7120,
                "endTimeMs": 7360,
                "text": "To"
              },
              {
                "startTimeMs": 7560,
                "endTimeMs": 7880,
                "text": "achieve"
              }
              /*... (13 additional words)*/
            ],
            "locale": "en-US"
          },
          {
            "speaker": "Speaker 1",
            "startTimeMs": 13440,
            "endTimeMs": 23680,
            "text": "We actually accumulated tons of the data so that this universal model is able to capture the nuance of the audio and generate a more natural voice for the algorithm.",
            "confidence": 0.937,
            "words": [
              {
                "startTimeMs": 13440,
                "endTimeMs": 13600,
                "text": "We"
              },
              {
                "startTimeMs": 13600,
                "endTimeMs": 14000,
                "text": "actually"
              }
              /*... (28 additional words)*/
            ],
            "locale": "en-US"
          }
        ],
        "cameraShotTimesMs": [
          1467,
          3233
          /*... (13 additional camera shots)*/
        ],
        "mimeType": "video/x-m4v"
      },
      {
        "markdown": "# Video: 00:15.467 => 00:23.100\nWidth: 1080\nHeight: 608\n\n\n\nKey Frames\n- 00:15.467 ![](keyFrame.15467.jpg)\n- 00:16.933 ![](keyFrame.16933.jpg)\n...\n- 00:22.367 ![](keyFrame.22367.jpg)\n- 00:23.100 ![](keyFrame.23100.jpg)",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "The video transitions to scenic aerial views from the Flight Simulator, showcasing detailed landscapes including coastlines, mountains, and castles. This segment highlights the realistic graphics and immersive experience of the Flight Simulator, demonstrating the integration of advanced AI technologies to enhance the simulation."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 15467,
        "endTimeMs": 23100,
        "width": 1080,
        "height": 608,
        "KeyFrameTimesMs": [
          15467,
          16933
          /*... (7 additional keyframes)*/
        ],
        "transcriptPhrases": [],
        "cameraShotTimesMs": [
          1467,
          3233
          /*... (13 additional camera shots)*/
        ]
      },
      {
        "markdown": "# Video: 00:23.100 => 00:43.233\nWidth: 1080\nHeight: 608\n\nTranscript\n```\nWEBVTT\n\n00:24.040 --> 00:29.120\n<Speaker 3>What we liked about cognitive services offerings were that they had a much higher fidelity.\n\n00:29.600 --> 00:32.880\n<Speaker 3>And they sounded a lot more like an actual human voice.\n\n00:33.680 --> 00:37.200\n<Speaker 4>Orlando ground 9555 requesting the end of pushback.\n\n00:38.680 --> 00:41.280\n<Speaker 4>9555 request to end pushback received.\n```\n\nKey Frames\n- 00:23.100 ![](keyFrame.23100.jpg)\n- 00:24.833 ![](keyFrame.24833.jpg)\n...\n- 00:42.633 ![](keyFrame.42633.jpg)\n- 00:43.233 ![](keyFrame.43233.jpg)",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "The focus shifts back to an interview with another man discussing the high fidelity and human-like quality of voices produced by cognitive services offerings. The segment concludes with visuals of an airplane on the tarmac, ground crew directing the plane, and the plane preparing for pushback, accompanied by realistic audio communications between ground control and the aircraft."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 23100,
        "endTimeMs": 43233,
        "width": 1080,
        "height": 608,
        "KeyFrameTimesMs": [
          23100,
          24833
          /*... (19 additional keyframes)*/
        ],
        "transcriptPhrases": [
          {
            "speaker": "Speaker 3",
            "startTimeMs": 24040,
            "endTimeMs": 29120,
            "text": "What we liked about cognitive services offerings were that they had a much higher fidelity.",
            "confidence": 0.937,
            "words": [
              {
                "startTimeMs": 24040,
                "endTimeMs": 24240,
                "text": "What"
              },
              {
                "startTimeMs": 24240,
                "endTimeMs": 24320,
                "text": "we"
              }
              /*... (13 additional words)*/
            ],
            "locale": "en-US"
          },
          {
            "speaker": "Speaker 3",
            "startTimeMs": 29600,
            "endTimeMs": 32880,
            "text": "And they sounded a lot more like an actual human voice.",
            "confidence": 0.823,
            "words": [
              {
                "startTimeMs": 29600,
                "endTimeMs": 30080,
                "text": "And"
              },
              {
                "startTimeMs": 30080,
                "endTimeMs": 30160,
                "text": "they"
              }
              /*... (9 additional words)*/
            ],
            "locale": "en-US"
          },
          {
            "speaker": "Speaker 4",
            "startTimeMs": 33680,
            "endTimeMs": 37200,
            "text": "Orlando ground 9555 requesting the end of pushback.",
            "confidence": 0.823,
            "words": [
              {
                "startTimeMs": 33680,
                "endTimeMs": 34160,
                "text": "Orlando"
              },
              {
                "startTimeMs": 34160,
                "endTimeMs": 34600,
                "text": "ground"
              }
              /*... (6 additional words)*/
            ],
            "locale": "en-US"
          },
          {
            "speaker": "Speaker 4",
            "startTimeMs": 38680,
            "endTimeMs": 41280,
            "text": "9555 request to end pushback received.",
            "confidence": 0.823,
            "words": [
              {
                "startTimeMs": 38680,
                "endTimeMs": 39600,
                "text": "9555"
              },
              {
                "startTimeMs": 39600,
                "endTimeMs": 40080,
                "text": "request"
              }
              /*... (4 additional words)*/
            ],
            "locale": "en-US"
          }
        ],
        "cameraShotTimesMs": [
          1467,
          3233
          /*... (13 additional camera shots)*/
        ]
      }
    ]
  },
  "usage": {
    "videoHours": 0.013,
    "contextualizationTokens": 12222,
    "tokens": {
      "gpt-4.1-mini-input": 8976,
      "gpt-4.1-mini-output": 439
    }
  }
}
```

---

## Next step

Now that you know how to invoke the analysis operation, learn more about building [custom analyzers](../tutorial/create-custom-analyzer.md) for your use case.
