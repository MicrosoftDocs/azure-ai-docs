---
title: People detection - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Learn concepts related to the people detection feature of Azure Vision in Foundry Tools API - usage and limits.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 09/26/2025
ms.author: pafarley
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"

---

# People detection (version 4.0)

Version 4.0 of Image Analysis offers the ability to detect people appearing in images. The bounding box coordinates of each detected person are returned, along with a confidence score. 

> [!IMPORTANT]
> We built this model by enhancing our object detection model for person detection scenarios. People detection doesn't involve distinguishing one face from another face, predicting or classifying facial attributes, or creating a facial template (a unique set of numbers generated from an image that represents the distinctive features of a face).

## People detection example

The following JSON response illustrates what the Analysis 4.0 API returns when describing the example image based on its visual features.

![Photo of four people.](./Images/family_photo.png)

```json
{
  "modelVersion": "2024-02-01",
  "metadata": {
    "width": 300,
    "height": 231
  },
  "peopleResult": {
    "values": [
      {
        "boundingBox": {
          "x": 0,
          "y": 41,
          "w": 95,
          "h": 189
        },
        "confidence": 0.9474349617958069
      },
      {
        "boundingBox": {
          "x": 204,
          "y": 96,
          "w": 95,
          "h": 134
        },
        "confidence": 0.9470965266227722
      },
      {
        "boundingBox": {
          "x": 53,
          "y": 20,
          "w": 136,
          "h": 210
        },
        "confidence": 0.8943784832954407
      },
      {
        "boundingBox": {
          "x": 170,
          "y": 31,
          "w": 91,
          "h": 199
        },
        "confidence": 0.2713555097579956
      }
    ]
  }
}
```

## Use the API

The people detection feature is part of the [Analyze Image 4.0 API](https://aka.ms/vision-4-0-ref). Include `People` in the **features** query parameter. Then, when you get the full JSON response, parse the string for the contents of the `"people"` section.

## Next step

> [!div class="nextstepaction"]
> [Call the Analyze Image API](./how-to/call-analyze-image-40.md)
