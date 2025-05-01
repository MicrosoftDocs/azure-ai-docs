---
author: PatrickFarley
manager: nitinme
ms.service: ai-services
ms.subservice: computer-vision
ms.topic: include
ms.date: 01/15/2024
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.author: pafarley
ms.custom: references_regions
---

## Prerequisites

This guide assumes you followed the steps mentioned in the [quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40). This means:

* You have <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision"  title="Created a Computer Vision resource"  target="_blank">created a Computer Vision resource </a> and obtained a key and endpoint URL.
* You have the appropriate SDK package installed and you have a running [quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40) application. You can modify this quickstart application based on the code examples here.

## Create and authenticate the client

To authenticate against the Image Analysis service, you need a Computer Vision key and endpoint URL. This guide assumes that you defined the environment variables `VISION_KEY` and `VISION_ENDPOINT` with your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

Start by creating a **ImageAnalysisClient** object. For example:

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_client)]

## Select the image to analyze

You can select an image by providing a publicly accessible image URL, or by reading image data into the SDK's input buffer. See [Image requirements](../../overview-image-analysis.md?tabs=4-0#input-requirements) for supported image formats.

### Image URL

You can use the following sample image URL.

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_url)]

### Image buffer

Alternatively, you can pass in the image as a data array. For example, read from a local image file you want to analyze.

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_file)]


## Select visual features

The Analysis 4.0 API gives you access to all of the service's image analysis features. Choose which operations to do based on your own use case. See the [Overview](/azure/ai-services/computer-vision/overview-image-analysis) for a description of each feature. The example in this section adds all of the available visual features, but for practical usage you likely need fewer. 

> [!IMPORTANT]
> The visual features [Captions](/java/api/com.azure.ai.vision.imageanalysis.models.visualfeatures#com-azure-ai-vision-imageanalysis-models-visualfeatures-caption) and [DenseCaptions](/java/api/com.azure.ai.vision.imageanalysis.models.visualfeatures#com-azure-ai-vision-imageanalysis-models-visualfeatures-dense-captions) are only supported in certain Azure regions. See .

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_features)]

## Call the Analyze API with options

The following code calls the Analyze Image API with the features you selected above and other options, defined next. To analyze from an image buffer instead of URL, replace `imageURL` in the method call with `imageData`.

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_call)]


### Select smart cropping aspect ratios

An aspect ratio is calculated by dividing the target crop width by the height. Supported values are from 0.75 to 1.8 (inclusive). Setting this property is only relevant when **VisualFeatures.SmartCrops** was selected as part the visual feature list. If you select **VisualFeatures.SmartCrops** but don't specify aspect ratios, the service returns one crop suggestion with an aspect ratio it sees fit. In this case, the aspect ratio is between 0.5 and 2.0 (inclusive).

### Select gender neutral captions

If you're extracting captions or dense captions (using **VisualFeatures.Caption** or **VisualFeatures.DenseCaptions**), you can ask for gender neutral captions. Gender neutral captions are optional, with the default being gendered captions. For example, in English, when you select gender neutral captions, terms like **woman** or **man** are replaced with **person**, and **boy** or **girl** are replaced with **child**. 

### Specify languages

You can specify the language of the returned data. The language is optional, with the default being English. See [Language support](https://aka.ms/cv-languages) for a list of supported language codes and which visual features are supported for each language.

## Get results from the service

The following code shows you how to parse the results of the various **analyze** operations.

[!Code-javascript[](~/cognitive-services-quickstart-code/javascript/ComputerVision/4-0/how-to.js?name=snippet_results)]


## Troubleshooting

### Logging

Enabling logging may help uncover useful information about failures. In order to see a log of HTTP requests and responses, set the `AZURE_LOG_LEVEL` environment variable to `info`. Alternatively, logging can be enabled at runtime by calling `setLogLevel` in the `@azure/logger`:

```javascript
const { setLogLevel } = require("@azure/logger");

setLogLevel("info");
```

For more detailed instructions on how to enable logs, you can look at the [@azure/logger package docs](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/core/logger).
