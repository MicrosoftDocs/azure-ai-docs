---
title: Analyze a shelf image using pretrained models
titleSuffix: Azure AI services
description: Use the Product Recognition API to analyze a shelf image and receive rich product data.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: how-to
ms.date: 02/14/2024
ms.author: pafarley
ms.custom: build-2023, build-2023-dataai
---

# Shelf Product Recognition (preview): Analyze shelf images using pretrained model

[!INCLUDE [model-customization-deprecation](../includes/model-customization-deprecation.md)]

The fastest way to start using Product Recognition is to use the built-in pretrained AI models. With the Product Recognition API, you can upload a shelf image and get the locations of products and gaps.

:::image type="content" source="../media/shelf/shelf-analysis-pretrained.png" alt-text="Photo of a retail shelf with products and gaps highlighted with rectangles.":::

> [!NOTE]
> The brands shown in the images are not affiliated with Microsoft and do not indicate any form of endorsement of Microsoft or Microsoft products by the brand owners, or an endorsement of the brand owners or their products by Microsoft.

## Prerequisites
* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/) 
* Once you have your Azure subscription, <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision"  title="create a Vision resource"  target="_blank">create a Vision resource</a> in the Azure portal. It must be deployed in a supported Azure region (see [Region availability](./../overview-image-analysis.md#region-availability)). After it deploys, select **Go to resource**.
  * You'll need the key and endpoint from the resource you create to connect your application to the Azure AI Vision service. You'll paste your key and endpoint into the code below later in the guide.
* An Azure Storage resource with a blob storage container. [Create one](/azure/storage/common/storage-account-create?tabs=azure-portal)
* [cURL](https://curl.haxx.se/) installed. Or, you can use a different REST platform, like Swagger or the [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension for VS Code.
* A shelf image. You can download our [sample image](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/ComputerVision/shelf-analysis/shelf.png) or bring your own images. The maximum file size per image is 20 MB.

## Analyze shelf images

To analyze a shelf image, do the following steps:

1. Upload the images you'd like to analyze to your blob storage container, and get the absolute URL.
1. Copy the following `curl` command into a text editor.

    ```bash
    curl -X PUT -H "Ocp-Apim-Subscription-Key: <subscriptionKey>" -H "Content-Type: application/json" "<endpoint>/computervision/productrecognition/ms-pretrained-product-detection/runs/<your_run_name>?api-version=2023-04-01-preview" -d "{
        'url':'<your_url_string>'
    }"
    ```
1. Make the following changes in the command where needed:
    1. Replace the `<subscriptionKey>` with your Vision resource key.
    1. Replace the `<endpoint>` with your Vision resource endpoint. For example: `https://YourResourceName.cognitiveservices.azure.com`.
    2. Replace the `<your_run_name>` with your unique test run name for the task queue. It is an async API task queue name for you to be able retrieve the API response later. For example, `.../runs/test1?api-version...`
    1. Replace the `<your_url_string>` contents with the blob URL of the image
1. Open a command prompt window.
1. Paste your edited `curl` command from the text editor into the command prompt window, and then run the command.


## Examine the response

A successful response is returned in JSON. The product recognition API results are returned in a `ProductRecognitionResultApiModel` JSON field:

```json
"ProductRecognitionResultApiModel": {
  "description": "Results from the product understanding operation.",
  "required": [
    "gaps",
    "imageMetadata",
    "products"
  ],
  "type": "object",
  "properties": {
    "imageMetadata": {
      "$ref": "#/definitions/ImageMetadataApiModel"
    },
    "products": {
      "description": "Products detected in the image.",
      "type": "array",
      "items": {
        "$ref": "#/definitions/DetectedObject"
      }
    },
    "gaps": {
      "description": "Gaps detected in the image.",
      "type": "array",
      "items": {
        "$ref": "#/definitions/DetectedObject"
      }
    }
  }
}
```

See the following sections for definitions of each JSON field.

### Product Recognition Result API model

Results from the product recognition operation.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `imageMetadata` | [ImageMetadataApiModel](#image-metadata-api-model) | The image metadata information such as height, width and format. | Yes |
| `products` |[DetectedObject](#detected-object-api-model) | Products detected in the image. | Yes |
| `gaps` | [DetectedObject](#detected-object-api-model) | Gaps detected in the image. | Yes |

### Image Metadata API model

The image metadata information such as height, width and format.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `width` | integer | The width of the image in pixels. | Yes |
| `height` | integer | The height of the image in pixels. | Yes |

### Detected Object API model

Describes a detected object in an image.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `id` | string | ID of the detected object. | No |
| `boundingBox` | [BoundingBox](#bounding-box-api-model) | A bounding box for an area inside an image. | Yes |
| `tags` | [TagsApiModel](#image-tags-api-model) | Classification confidences of the detected object. | Yes |

### Bounding Box API model

A bounding box for an area inside an image.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `x` | integer | Left-coordinate of the top left point of the area, in pixels. | Yes |
| `y` | integer | Top-coordinate of the top left point of the area, in pixels. | Yes |
| `w` | integer | Width measured from the top-left point of the area, in pixels. | Yes |
| `h` | integer | Height measured from the top-left point of the area, in pixels. | Yes |

### Image Tags API model

Describes the image classification confidence of a label.

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| `confidence` | float | Confidence of the classification prediction. | Yes |
| `name` | string | Label of the classification prediction. | Yes |

## Next steps

In this guide, you learned how to make a basic analysis call using the pretrained Product Recognition REST API. Next, learn how to use a custom Product Recognition model to better meet your business needs.

> [!div class="nextstepaction"]
> [Train a custom model for Product Recognition](../how-to/shelf-model-customization.md)

* [Image Analysis overview](../overview-image-analysis.md)
* [API reference](/rest/api/computervision/operation-groups?view=rest-computervision-2023-04-01-preview)
