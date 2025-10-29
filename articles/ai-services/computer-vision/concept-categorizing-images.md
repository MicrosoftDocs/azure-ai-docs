---
title: Image categorization - Azure AI Vision
titleSuffix: Azure AI services
description: Learn concepts related to the image categorization feature of the Image Analysis API.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: conceptual
ms.date: 02/21/2025
ms.author: pafarley
---

# Image categorization

In addition to tags and a description, Image Analysis 3.2 can return the taxonomy-based categories detected in an image. Unlike tags, categories are organized in a parent/child hierarchy, and there are fewer of them (86, as opposed to thousands of tags). All category names are in English. Categorization can be done by itself or in the same API call as the newer tags model.

## The 86-category taxonomy

Azure AI Vision can categorize an image broadly or specifically, using the list of 86 categories in the following diagram. For the full taxonomy in text format, see [Category Taxonomy](category-taxonomy.md).

![Grouped lists of all the categories in the category taxonomy](./Images/analyze_categories-v2.png)

## Image categorization examples

The following JSON response illustrates what Azure AI Vision returns when categorizing the example image based on its visual features.

![A woman on the roof of an apartment building](./Images/woman_roof.png)

```json
{
    "categories": [
        {
            "name": "people_",
            "score": 0.81640625
        }
    ],
    "requestId": "bae7f76a-1cc7-4479-8d29-48a694974705",
    "metadata": {
        "height": 200,
        "width": 300,
        "format": "Jpeg"
    }
}
```

The following table illustrates a typical image set and the category returned by Azure AI Vision for each image.

| Image | Category |
|-------|----------|
| ![Four people posed together as a family](./Images/family_photo.png) | people_group |
| ![A puppy sitting in a grassy field](./Images/cute_dog.png) | animal_dog |
| ![A person standing on a mountain rock at sunset](./Images/mountain_vista.png) | outdoor_mountain |
| ![A pile of bread roles on a table](./Images/bread.png) | food_bread |

## Use the API

The categorization feature is part of the [Analyze Image 3.2](/rest/api/computervision/analyze-image?view=rest-computervision-v3.2&preserve-view=true) API. You can call this API through a native SDK or through REST calls. Include `Categories` in the **visualFeatures** query parameter. Then, when you get the full JSON response, simply parse the string for the contents of the `"categories"` section.

* [Quickstart: Vision REST API or client libraries](./quickstarts-sdk/image-analysis-client-library.md?pivots=programming-language-csharp)

## Related content

Learn the related concepts of [tagging images](concept-tagging-images.md) and [describing images](concept-describing-images.md).
