---
title: Domain-specific content - Azure AI Vision
titleSuffix: Azure AI services
description: Learn how to specify an image categorization domain to return more detailed information about an image.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: conceptual
ms.date: 02/21/2025
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
---

# Domain-specific content detection

In addition to tagging and high-level categorization, Azure AI Vision also supports further domain-specific analysis using models that are trained on specialized data.

There are two ways to use the domain-specific models: by themselves (scoped analysis) or as an enhancement to the image [categorization](./concept-categorizing-images.md) feature.

### Scoped analysis

You can analyze an image using only the chosen domain-specific model by calling the [Models/\<model\>/Analyze](/rest/api/computervision/analyze-image) API.

The following is a sample JSON response returned by the `models/celebrities/analyze` API for the given image:

![Satya Nadella standing, smiling](./images/satya.jpeg)

```json
{
  "result": {
    "celebrities": [{
      "faceRectangle": {
        "top": 391,
        "left": 318,
        "width": 184,
        "height": 184
      },
      "name": "Satya Nadella",
      "confidence": 0.99999856948852539
    }]
  },
  "requestId": "8217262a-1a90-4498-a242-68376a4b956b",
  "metadata": {
    "width": 800,
    "height": 1200,
    "format": "Jpeg"
  }
}
```

### Enhanced categorization analysis

You can also use domain-specific models to supplement general image analysis. You do this as part of [high-level categorization](concept-categorizing-images.md) by specifying domain-specific models in the *details* parameter of the [Analyze Image](/rest/api/computervision/analyze-image) API call.

In this case, the 86-category taxonomy classifier is called first. If any of the detected categories have a matching domain-specific model, the image is passed through that model as well and the results are added.

The following JSON response shows how domain-specific analysis can be included as the `detail` node in a broader categorization analysis.

```json
"categories":[
  {
    "name":"abstract_",
    "score":0.00390625
  },
  {
    "name":"people_",
    "score":0.83984375,
    "detail":{
      "celebrities":[
        {
          "name":"Satya Nadella",
          "faceRectangle":{
            "left":597,
            "top":162,
            "width":248,
            "height":248
          },
          "confidence":0.999028444
        }
      ],
      "landmarks":[
        {
          "name":"Forbidden City",
          "confidence":0.9978346
        }
      ]
    }
  }
]
```

## List the domain-specific models

Currently, Azure AI Vision supports the following domain-specific models:

| Name | Description |
|------|-------------|
| celebrities | Celebrity recognition, supported for images classified in the `people_` category |
| landmarks | Landmark recognition, supported for images classified in the `outdoor_` or `building_` categories |

Calling the [Models](/rest/api/computervision/list-models/list-models) API returns this information along with the categories to which each model can apply:

```json
{
  "models":[
    {
      "name":"celebrities",
      "categories":[
        "people_",
        "人_",
        "pessoas_",
        "gente_"
      ]
    },
    {
      "name":"landmarks",
      "categories":[
        "outdoor_",
        "户外_",
        "屋外_",
        "aoarlivre_",
        "alairelibre_",
        "building_",
        "建筑_",
        "建物_",
        "edifício_"
      ]
    }
  ]
}
```

## Use the API

This feature is available through the [Analyze Image 3.2 API](/rest/api/computervision/analyze-image/analyze-image). You can call this API through a native SDK or through REST calls. Include `Celebrities` or `Landmarks` in the **details** query parameter. Then, when you get the full JSON response, parse the string for the contents of the `"details"` section.

* [Quickstart: Vision REST API or client libraries](./quickstarts-sdk/image-analysis-client-library.md?pivots=programming-language-csharp)
