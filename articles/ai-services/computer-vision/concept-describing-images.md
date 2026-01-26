---
title: Image descriptions - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Concepts related to the image description feature of Azure Vision in Foundry Tools API.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 09/26/2025
ms.author: pafarley
---

# Image descriptions

Azure Vision in Foundry Tools can analyze an image and generate a human-readable phrase that describes its contents. The service returns several descriptions based on different visual features, and each description is given a confidence score. The final output is a list of descriptions ordered from highest to lowest confidence.

English is the only supported language for image descriptions.

Try out the image captioning features quickly and easily in your browser using Vision Studio.

> [!div class="nextstepaction"]
> [Try Vision Studio](https://portal.vision.cognitive.azure.com/)

## Image description example

The following JSON response illustrates what the Analyze Image API returns when describing the example image based on its visual features.

![A black and white picture of buildings in Manhattan](./Images/bw_buildings.png)

```json
{
   "description":{
      "tags":[
         "outdoor",
         "city",
         "white"
      ],
      "captions":[
         {
            "text":"a city with tall buildings",
            "confidence":0.48468858003616333
         }
      ]
   },
   "requestId":"7e5e5cac-ef16-43ca-a0c4-02bd49d379e9",
   "metadata":{
      "height":300,
      "width":239,
      "format":"Png"
   },
   "modelVersion":"2021-05-01"
}
```

## Use the API

The image description feature is part of the [Analyze Image](/rest/api/computervision/analyze-image) API. You can call this API through a native SDK or through REST calls. Include `Description` in the **visualFeatures** query parameter. Then, when you get the full JSON response, parse the string for the contents of the `"description"` section.

* [Quickstart: Image Analysis REST API or client libraries](./quickstarts-sdk/image-analysis-client-library.md?pivots=programming-language-csharp)

## Related content

Learn the related concepts of [tagging images](concept-tagging-images.md) and [categorizing images](concept-categorizing-images.md).
