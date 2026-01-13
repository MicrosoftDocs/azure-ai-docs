---
title: "Quickstart: Image Analysis REST API"
titleSuffix: "Foundry Tools"
description: In this quickstart, get started with the Image Analysis REST API.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: include
ms.date: 09/30/2024
ms.author: pafarley
---

Use the Image Analysis REST API to analyze an image for tags.

> [!TIP]
> The Analyze Image API can do many different operations other than generate image tags. See the [Image Analysis how-to guide](../how-to/call-analyze-image.md) for examples that showcase all of the available features.

> [!NOTE]
> This quickstart uses cURL commands to call the REST API. You can also call the REST API using a programming language. See the GitHub samples for examples in [C#](https://github.com/Azure-Samples/cognitive-services-quickstart-code/tree/master/dotnet/ComputerVision/REST), [Python](https://github.com/Azure-Samples/cognitive-services-quickstart-code/tree/master/python/ComputerVision/REST), [Java](https://github.com/Azure-Samples/cognitive-services-quickstart-code/tree/master/java/ComputerVision/REST), and [JavaScript](https://github.com/Azure-Samples/cognitive-services-quickstart-code/tree/master/javascript/ComputerVision/REST).

## Prerequisites

* An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* Once you have your Azure subscription, create a [Computer Vision resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision) in the Azure portal to get your key and endpoint. After it deploys, select **Go to resource**.
  * You need the key and endpoint from the resource you create to connect your application to Azure Vision in Foundry Tools.
  * You can use the free pricing tier (`F0`) to try the service, and upgrade later to a paid tier for production.
* [cURL](https://curl.se) installed.

## Analyze an image

To analyze an image for various visual features, do the following steps:

1. Copy the following command into a text editor.

    ```bash
    curl.exe -H "Ocp-Apim-Subscription-Key: <yourKey>" -H "Content-Type: application/json" "https://westcentralus.api.cognitive.microsoft.com/vision/v3.2/analyze?visualFeatures=Tags" -d "{'url':'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png'}"
    ```

1. Make the following changes in the command where needed:
    1. Replace the value of `<yourKey>` with the key from your Computer Vision resource.
    1. Replace the first part of the request URL (`westcentralus.api.cognitive.microsoft.com`) with your own endpoint URL.
        [!INCLUDE [Custom subdomains notice](../../includes/cognitive-services-custom-subdomains-note.md)]
    1. Optionally, change the image URL in the request body (`https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png`) to the URL of a different image to be analyzed.
1. Open a command prompt window.
1. Paste your edited `curl` command from the text editor into the command prompt window, and then run the command.

### Examine the response

A successful response is returned in JSON format. The sample application parses and displays a successful response in the command prompt window, similar to the following example:

```json
{
   "tags":[
      {
         "name":"text",
         "confidence":0.9992657899856567
      },
      {
         "name":"post-it note",
         "confidence":0.9879657626152039
      },
      {
         "name":"handwriting",
         "confidence":0.9730165004730225
      },
      {
         "name":"rectangle",
         "confidence":0.8658561706542969
      },
      {
         "name":"paper product",
         "confidence":0.8561884760856628
      },
      {
         "name":"purple",
         "confidence":0.5961999297142029
      }
   ],
   "requestId":"2788adfc-8cfb-43a5-8fd6-b3a9ced35db2",
   "metadata":{
      "height":945,
      "width":1000,
      "format":"Jpeg"
   },
   "modelVersion":"2021-05-01"
}
```

## Next step

In this quickstart, you learned how to make basic image analysis calls using the REST API. Next, learn more about the Analyze Image API features.

> [!div class="nextstepaction"]
>[Call the Analyze Image API](../how-to/call-analyze-image.md)

* [What is Image Analysis?](../overview-image-analysis.md)
