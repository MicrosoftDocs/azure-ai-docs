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

* This quickstart shows you how to use the [Content Understanding REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) to get structured data from multimodal content in document, image, audio, and video files.

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
This quickstart uses pre-built document, image, audio, and video analyzers to help you get started. 

Before running the cURL command, make the following changes to the HTTP request:
#### POST Request
```bash
curl -i -X POST "{endpoint}/analyzers/{analyzerId}:analyze?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"{fileUrl}\"}"
```

# [Document](#tab/document)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-documentAnalyzer`.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf`.

# [Image](#tab/image)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-imageAnalyzer`.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/pieChart.jpg`.

# [Audio](#tab/audio)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-audioAnalyzer`.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/audio.wav`.

# [Video](#tab/video)

1. Replace `{endpoint}` and `{key}` with the corresponding values from your Azure AI Services instance in the Azure portal.
2. Replace `{analyzerId}` with  `prebuilt-videoAnalyzer`.
3. Replace `{fileUrl}` with a publicly accessible URL of the file to analyze—such as a path to an Azure Storage Blob with a shared access signature (SAS), or use the sample URL: `https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/FlightSimulator.mp4`.
---


#### POST Response

The response returns `resultId` that you can use to track the status of this asynchronous analyze operation.

```
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

### Get Analyze Result

Use the `resultId` from the `POST` response above and retrieve the result of the analysis.

1. Replace `{endpoint}` and `{key}` with the endpoint and key values from your Azure portal Azure AI Services instance.
2. Replace `{resultId}` with the `resultId` from the `POST` response.

#### GET Request
```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzerResults/{resultId}?api-version=2025-05-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

#### GET Response

The 200 (`OK`) JSON response includes a `status` field indicating the status of the operation. If the operation isn't complete, the value of `status` is `running` or `notStarted`. In such cases, you should send the GET request again, either manually or through a script. Wait an interval of one second or more between calls.

# [Document](#tab/document)

```json
{
  "id": "a8ccf3ea-e4ad-4302-9ac5-b40e69768053",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-documentAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-05-05T17:55:35Z",
    "warnings": [],
    "contents": [
      {
        "markdown": "# WEB HOSTING AGREEMENT\n\nThis web Hosting Agreement is entered as of this 15 day of October ..." ,
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "This document is a Web Hosting Agreement between Contoso Corporation and AdventureWorks Cycles, both based in Washington. It outlines the terms of their agreement, including payment terms for software and bandwidth usage, technical support requirements, and governing laws. The agreement nullifies any previous agreements between the parties and is signed by representatives of both companies."
          }
        },
        "kind": "document",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "unit": "inch",
        "pages": [
          {
            "pageNumber": 1,
            "angle": -0.0052,
            "width": 8.2639,
            "height": 11.6806
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
  "id": "2e77aecc-b5f0-4652-b91c-4790b655ce01",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-audioAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-05-05T18:06:24Z",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Audio: 00:00.000 => 01:54.670\n\nTranscript\n```\nWEBVTT\n\n00:00.080 --> 00:02.160\n<v Speaker 1>Thank you for calling Woodgrove Travel.\n\n00:02.960 --> 00:04.560\n<v Speaker 1>My name is Isabella Taylor ...",
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 114670
      }
    ]
  }
}
```

# [Video](#tab/video)

```json
{
  "id": "3fb3cca1-4cf1-4f2f-9155-8d1db4ef9541",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-videoAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-05-05T18:24:03Z",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Video: 00:00.000 => 00:43.866\nWidth: 1080\nHeight: 608\n\nTranscript\n```\nWEBVTT\n\n00:01.400 --> 00:06.560\n<Speaker 1 Speaker>When it comes to the neural TTS, in order to get a good voice, it's better to have good data ..."
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 43866,
        "width": 1080,
        "height": 608
      }
    ]
  }
}
```

---

## Next steps

* In this quickstart, you learned how to call the [REST API](REFERENCE LINK) using a pre-built analyzer. See how you can [customize pre-built analyzers](LINK TO CUSTOMIZATION) to better fit your use case.


