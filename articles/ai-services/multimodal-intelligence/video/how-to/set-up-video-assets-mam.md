---
title: Azure AI Multimodal Intelligence set up a Video Metadata for Media Asset Management workflow
titleSuffix: Azure AI services
description: Learn how to set up a post-call analytics workflow
author: laujan
ms.author: jfilcik
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/24/2024
---
# Set up a Video Metadata for Media Asset Management 

Media asset management (`MAM`) is essential for organizations that handle and process large volumes of video content. Although it can be challenging to implement, `MAM` is an effective tool for organizing and storing digital assets. Multimodal Intelligence enables you to automatically generate specific metadata for your video assets, such as descriptions of each shot, shot types, brands seen, and more. This metadata can be customized to your specific needs by defining the schema. 

In this article, you learn how to create a media asset management workflow with Multimodal Intelligence service. You'll call the analyze API with a specific prebuilt model and retrieve the generated metadata and customize the output by defining custom fields.

## Prerequisites
* [**Azure subscription**](https://azure.microsoft.com/free/)
* Azure AI services resource: To access the Video Description API
* Video file: A video file stored in Azure Blob Storage or accessible via URL

## Setup
1. Get your Azure AI services endpoint and key:
* Navigate to your Azure AI services resource in the Azure portal.
* Copy the Endpoint and Key from the Keys and Endpoint section.
2. Prepare your video file:
* Ensure your video file is accessible via a URL. If it's stored in Azure Blob Storage, you can generate a shared access signature (SAS) URL.
3. Set up authentication headers:
* For API calls, you'll need to include the Ocp-Apim-Subscription-Key header with your resource key.

### 1. Analyze a Video
To analyze a video and generate metadata, you'll call the analyze API with the prebuilt video-descriptor model.

#### Request
#### HTTP Method: POST

#### URL:
```bash
{Endpoint}/multimodalintelligence/analyzers/prebuilt-video-descriptor:analyze?api-version=2024-12-01-preview
```

Replace {Endpoint} with your Azure AI services endpoint.

#### Headers:
```bash
Ocp-Apim-Subscription-Key: YOUR_RESOURCE_KEY
Content-Type: application/json
```

#### Request Body:
``` json
{
  "input": {
    "kind": "url",
    "url": "YOUR_VIDEO_URL"
  },
  "features": [
    "transcription",
    "sceneDetection",
    "faceDetection"
  ],
  "properties": {
    "schema": {
      "fields": {
        "VideoDescription": {
          "description": "Provide a high-level summary of the content in the video, including themes, subjects, and any key visuals."
        },
        "GeographicLocation": {
          "description": "Specify the physical location depicted in the video, such as city or region."
        },
        "ShotSetting": {
          "description": "Classify the scene setting, including options such as indoor, outdoor, urban, rural, underwater, or aerial."
        },
        "ShotType": {
          "description": "Classify the shot, such as close-up, wide-angle, or medium shot."
        },
        "ShotMovement": {
          "description": "Describe the movement of the camera in the shot, such as panning left to right or zooming in/out."
        }
      }
    }
  }
}
```

**Note**: Replace YOUR_VIDEO_URL with the URL of your video file.

#### Sample curl Command
``` bash
curl -X POST "{Endpoint}/multimodalintelligence/analyzers/prebuilt-video-descriptor:analyze?api-version=2024-12-01-preview" \
  -H "Ocp-Apim-Subscription-Key: YOUR_RESOURCE_KEY" \
  -H "Content-Type: application/json" \
  -d @request_body.json
```
### 2. Retrieve the Analysis Results
The analyze API is an asynchronous operation. The response will include an operation-location header that you can use to check the status and retrieve the results.

#### Check Operation Status
#### HTTP Method: GET

#### URL:
``` bash
{operation-location}
```
Replace {operation-location} with the value from the operation-location header in the response.

#### Headers:

``` bash
Ocp-Apim-Subscription-Key: YOUR_RESOURCE_KEY
```
Repeat this request until the status field in the response is succeeded.

#### Sample Response
``` json
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
          "VideoDescription": {
            "type": "string",
            "content": "A promotional video showcasing the features of Contoso's new electric car model.",
            "confidence": 0.95
          },
          "GeographicLocation": {
            "type": "string",
            "content": "Seattle, Washington",
            "confidence": 0.90
          },
          "ShotSetting": {
            "type": "string",
            "content": "Outdoor, Urban",
            "confidence": 0.92
          },
          "ShotType": {
            "type": "string",
            "content": "Wide-angle, Close-up",
            "confidence": 0.88
          },
          "ShotMovement": {
            "type": "string",
            "content": "Panning left to right, Zooming in",
            "confidence": 0.87
          }
        }
      }
    ]
  }
}
```
### 3. Customize the Metadata Schema
You can customize the metadata fields by modifying the schema in the request body. For example, if you want to extract information about the emotions displayed in the video, you can add a new field:
``` json
"EmotionAnalysis": {
  "description": "Analyze the emotions displayed by individuals in the video, such as happiness, sadness, or surprise."
}
```
Include this field in the fields section of the schema:
``` json
"properties": {
  "schema": {
    "fields": {
      // existing fields
      "EmotionAnalysis": {
        "description": "Analyze the emotions displayed by individuals in the video, such as happiness, sadness, or surprise."
      }
    }
  }
}
```

### Next steps
* **Explore Advanced Features**: Learn how to use additional features like face recognition, object detection, and more.
* **Integrate into Applications**: Use the API in your applications to automate video metadata generation.
* **Provide Feedback**: Share your experience and suggestions to improve the Azure AI services.

**Note**: This quickstart provides a basic implementation. For production scenarios, implement proper error handling, secure your API keys, and follow best practices for API usage.

By following this quickstart, you've learned how to use the Video Description API to generate metadata for your video assets. You can now enhance your media asset management workflows with rich, customizable metadata.