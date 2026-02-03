---
title: Brand detection - Azure Vision in Foundry Tools
titleSuffix: Foundry Tools
description: Learn about brand and logo detection, a specialized mode of object detection, using Azure Vision in Foundry Tools API.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 09/26/2025
ms.author: pafarley
---

# Brand detection

Brand detection is a specialized mode of [object detection](concept-object-detection.md) that uses a database of thousands of global corporate logos to identify commercial brands in images or video. You can use this feature, for example, to discover which brands are most popular on social media or most prevalent in media product placement.

## How it works

Azure Vision in Foundry Tools service detects whether there are brand logos in a given image. If a brand logo is detected, the service returns the brand name, a confidence score, and the coordinates of a bounding box around the logo.

The built-in logo database covers popular brands in consumer electronics, clothing, and more. If you find that the Vision service doesn't detect the brand you're looking for, you can also try creating and training your own logo detector using the [Custom Vision](../custom-vision-service/index.yml) service.

## Brand detection example

The following JSON responses illustrate what Azure Vision returns when detecting brands in the example images.

:::image type="content" source="images/red-shirt-logo.jpg" alt-text="Photograph of a red shirt with a Microsoft label and logo.":::

```json
"brands":[  
   {  
      "name":"Microsoft",
      "rectangle":{  
         "x":20,
         "y":97,
         "w":62,
         "h":52
      }
   }
]
```

In some cases, the brand detector picks up both the logo image and the stylized brand name as two separate logos.

:::image type="content" source="images/gray-shirt-logo.jpg" alt-text="Photograph of a gray sweatshirt with a Microsoft label and logo.":::

```json
"brands":[  
   {  
      "name":"Microsoft",
      "rectangle":{  
         "x":58,
         "y":106,
         "w":55,
         "h":46
      }
   },
   {  
      "name":"Microsoft",
      "rectangle":{  
         "x":58,
         "y":86,
         "w":202,
         "h":63
      }
   }
]
```

## Use the API

The brand detection feature is part of the [Analyze Image](/rest/api/computervision/analyze-image) API. You can call this API by using a native SDK or through REST calls. Include `Brands` in the `visualFeatures` query parameter. Then, when you get the full JSON response, parse the string for the contents of the `"brands"` section.

## Next step

> [!div class="nextstepaction"]
> [Quickstart: Image Analysis](./quickstarts-sdk/image-analysis-client-library.md?pivots=programming-language-csharp)
