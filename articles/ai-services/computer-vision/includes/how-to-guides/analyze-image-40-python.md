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

This guide assumes you've followed the steps of the [quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40). This means:

* You've <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesComputerVision"  title="Created a Computer Vision resource"  target="_blank">created a Computer Vision resource </a> and obtained a key and endpoint URL.
* You've installed the appropriate SDK package and have a working [quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40) application. You can modify this quickstart application based on the code examples here.

## Create and authenticate the client

To authenticate against the Image Analysis service, you need a Computer Vision key and endpoint URL. This guide assumes that you've defined the environment variables `VISION_KEY` and `VISION_ENDPOINT` with your key and endpoint.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

Start by creating an [ImageAnalysisClient](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.imageanalysisclient) object using one of the constructors. For example:

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_client)]


## Select the image to analyze

You can select an image by providing a publicly accessible image URL, or by reading image data into the SDK's input buffer. See [Image requirements](../../overview-image-analysis.md?tabs=4-0#input-requirements) for supported image formats.

### Image URL

You can use the following sample image URL.

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_url)]


### Image buffer

Alternatively, you can pass in the image as [bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects) object. For example, read from a local image file you want to analyze.

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_file)]

## Select visual features

The Analysis 4.0 API gives you access to all of the service's image analysis features. Choose which operations to do based on your own use case. See the [overview](/azure/ai-services/computer-vision/overview-image-analysis) for a description of each feature. The example in this section adds all of the [available visual features](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.models.visualfeatures), but for practical usage you likely need fewer.

> [!IMPORTANT]
> The visual features [Captions](/java/api/com.azure.ai.vision.imageanalysis.models.visualfeatures#com-azure-ai-vision-imageanalysis-models-visualfeatures-caption) and [DenseCaptions](/java/api/com.azure.ai.vision.imageanalysis.models.visualfeatures#com-azure-ai-vision-imageanalysis-models-visualfeatures-dense-captions) are only supported in certain Azure regions. See [Region availability](./../../overview-image-analysis.md#region-availability).

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_features)]

<!--
### Set model name when using a custom model

You can also do image analysis with a custom trained model. To create and train a model, see [Create a custom Image Analysis model](/azure/ai-services/computer-vision/how-to/model-customization). Once your model is trained, all you need is the model's name. You don't need to specify visual features if you use a custom model.

To use a custom model, create the [ImageAnalysisOptions](/python/api/azure-ai-vision/azure.ai.vision.imageanalysisoptions) object and set the [model_name](/python/api/azure-ai-vision/azure.ai.vision.imageanalysisoptions#azure-ai-vision-imageanalysisoptions-model-name) property. You don't need to set any other properties on **ImageAnalysisOptions**. There's no need to set the [features](/python/api/azure-ai-vision/azure.ai.vision.imageanalysisoptions#azure-ai-vision-imageanalysisoptions-features) property, as you do with the standard model, since your custom model already implies the visual features the service extracts.

[!code-python[](~/azure-ai-vision-sdk/docs/learn.microsoft.com/python/image-analysis/custom-model/main.py?name=model_name)]
-->

## Call the analyze_from_url method with options

The following code calls the [analyze_from_url](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.imageanalysisclient#azure-ai-vision-imageanalysis-imageanalysisclient-analyzefromurl) method on the client with the features you selected above and other options, defined below. To analyze from an image buffer instead of URL, call the method [analyze](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.imageanalysisclient#azure-ai-vision-imageanalysis-imageanalysisclient-analyze) instead, with `image_data=image_data` as the first argument.

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_call)]

### Select smart cropping aspect ratios

An aspect ratio is calculated by dividing the target crop width by the height. Supported values are from 0.75 to 1.8 (inclusive). Setting this property is only relevant when [VisualFeatures.SMART_CROPS](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.models.visualfeatures) was selected as part the visual feature list. If you select [VisualFeatures.SMART_CROPS](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.models.visualfeatures) but don't specify aspect ratios, the service returns one crop suggestion with an aspect ratio it sees fit. In this case, the aspect ratio is between 0.5 and 2.0 (inclusive).


### Select gender neutral captions

If you're extracting captions or dense captions (using [VisualFeatures.CAPTION](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.models.visualfeatures) or [VisualFeatures.DENSE_CAPTIONS](/python/api/azure-ai-vision-imageanalysis/azure.ai.vision.imageanalysis.models.visualfeatures)), you can ask for gender neutral captions. Gender neutral captions are optional, with the default being gendered captions. For example, in English, when you select gender neutral captions, terms like **woman** or **man** are replaced with **person**, and **boy** or **girl** are replaced with **child**.

### Specify languages

You can specify the language of the returned data. The language is optional, with the default being English. See [Language support](https://aka.ms/cv-languages) for a list of supported language codes and which visual features are supported for each language.


## Get results from the service

The following code shows you how to parse the results from the **analyze_from_url** or **analyze** operations.

[!Code-python[](~/cognitive-services-quickstart-code/python/ComputerVision/4-0/how-to.py?name=snippet_result)]


<!--
### Get results using custom model

This section shows you how to make an analysis call to the service, when using a custom model. 


The code is similar to the standard model case. The only difference is that results from the custom model are available on the **custom_tags** and/or **custom_objects** properties of the [ImageAnalysisResult](/python/api/azure-ai-vision/azure.ai.vision.imageanalysisresult) object.

[!code-python[](~/azure-ai-vision-sdk/docs/learn.microsoft.com/python/image-analysis/custom-model/main.py?name=analyze)]
-->


## Troubleshooting

### Exceptions

The `analyze` methods raise an [HttpResponseError](/python/api/azure-core/azure.core.exceptions.httpresponseerror) exception for a non-success HTTP status code response from the service. The exception's `status_code` is the HTTP response status code. The exception's `error.message` contains a detailed message that allows you to diagnose the issue:

```python
try:
    result = client.analyze( ... )
except HttpResponseError as e:
    print(f"Status code: {e.status_code}")
    print(f"Reason: {e.reason}")
    print(f"Message: {e.error.message}")
```

For example, when you provide a wrong authentication key:
```
Status code: 401
Reason: PermissionDenied
Message: Access denied due to invalid subscription key or wrong API endpoint. Make sure to provide a valid key for an active subscription and use a correct regional API endpoint for your resource.
```

Or when you provide an image URL that doesn't exist or is not accessible:
```
Status code: 400
Reason: Bad Request
Message: The provided image url is not accessible.
```

### Logging

The client uses the standard [Python logging library](https://docs.python.org/3/library/logging.html). The SDK logs HTTP request and response details, which may be useful in troubleshooting. To log to stdout, add the following:

<!-- SNIPPET:sample_analyze_all_image_file.logging -->

```python
import sys
import logging

# Acquire the logger for this client library. Use 'azure' to affect both
# 'azure.core` and `azure.ai.vision.imageanalysis' libraries.
logger = logging.getLogger("azure")

# Set the desired logging level. logging.INFO or logging.DEBUG are good options.
logger.setLevel(logging.INFO)

# Direct logging output to stdout (the default):
handler = logging.StreamHandler(stream=sys.stdout)
# Or direct logging output to a file:
# handler = logging.FileHandler(filename = 'sample.log')
logger.addHandler(handler)

# Optional: change the default logging format. Here we add a timestamp.
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
handler.setFormatter(formatter)
```

<!-- END SNIPPET -->

By default logs redact the values of URL query strings, the values of some HTTP request and response headers (including `Ocp-Apim-Subscription-Key`, which holds the key), and the request and response payloads. To create logs without redaction, set the method argument `logging_enable = True` when you create `ImageAnalysisClient`, or when you call `analyze` on the client. 

<!-- SNIPPET:sample_analyze_all_image_file.create_client_with_logging -->

```python
# Create an Image Analysis client with none redacted log
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    logging_enable=True
)
```

<!-- END SNIPPET -->

None redacted logs are generated for log level `logging.DEBUG` only. Be sure to protect none redacted logs to avoid compromising security. For more information, see [Configure logging in the Azure libraries for Python](https://aka.ms/azsdk/python/logging)
