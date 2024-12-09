---
title: How to deploy and use MedImageParse healthcare AI model with AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use MedImageParse Healthcare AI Model with Azure AI Foundry.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
#Customer intent: As a Data Scientist I want to learn how to use the MedImageParse healthcare AI model to segment medical images.

---

# How to use MedImageParse healthcare AI model for segmentation of medical images

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy MedImageParse as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive, and interpret results.


## MedImageParse - prompt-based segmentation of medical images
Biomedical image analysis is crucial for discovery in fields like cell biology, pathology, and radiology. Traditionally, tasks such as segmentation, detection, and recognition of relevant objects are addressed separately, which can limit the overall effectiveness of image analysis. However, MedImageParse unifies these tasks through image parsing, by jointly conducting segmentation, detection, and recognition across numerous object types and imaging modalities. By applying the interdependencies among these subtasks—such as the semantic labels of segmented objects—the model enhances accuracy and enables novel applications. For example, it allows users to segment all relevant objects in an image, by using a simple text prompt. This approach eliminates the need to manually specify bounding boxes for each object.  

The following image shows the conceptual architecture of the MedImageParse model where an image embedding model is augmented with a task adaptation layer to produce segmentation masks and textual descriptions.

:::image type="content" source="../../media/how-to/healthcare-ai/medimageparse-flow.gif" alt-text="Animation of data flow through MedImageParse model showing image coming through the model paired with a task adaptor and turning into a set of segmentation masks.":::

Remarkably, the segmentation masks and textual descriptions were achieved by using only standard segmentation datasets, augmented by natural-language labels, or descriptions harmonized with established biomedical object ontologies. This approach not only improved individual task performance but also offered an all-in-one tool for biomedical image analysis, paving the way for more efficient and accurate image-based biomedical discovery.

## Prerequisites

To use the MedImageParse model, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageParse model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served. You can deploy the model through the catalog UI (in [Azure AI Foundry](https://aka.ms/healthcaremodelstudio) or [Azure Machine Learning studio](https://ml.azure.com/model/catalog)) or deploy programmatically.

To __deploy the model through the UI__:

1. Go to the catalog.
1. Search for _MedImageParse_ and select the model card.
1. On the model's overview page, select __Deploy__.
1. If given the option to choose between serverless API deployment and deployment using a managed compute, select **Managed Compute**.
1. Fill out the details in the deployment window.

    > [!NOTE]
    > For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**
1. Select __Deploy__.

To __deploy the model programmatically__, see [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md).

## Work with a segmentation model

In this section, you consume the model and make basic calls to it.

### Use REST API to consume the model

Consume the MedImageParse segmentation model as a REST API, using simple GET requests or by creating a client as follows:

```python
from azure.ai.ml import MLClient
from azure.identity import DeviceCodeCredential

credential = DefaultAzureCredential()

ml_client_workspace = MLClient.from_config(credential)
```

In the deployment configuration, you get to choose authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see the [corresponding documentation page](../../../machine-learning/how-to-setup-authentication.md). Also, note that the client is created from a configuration file that is created automatically for Azure Machine Learning virtual machines (VMs). Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve segmentation masks.

```python
import base64
import json
import os

sample_image_xray = os.path.join(image_path)

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

sample_image =  "sample_image.png"
data = {
    "input_data": {
        "columns": [ "image", "text" ],
        "index": [ 0 ],
        "data": [
            [
                base64.encodebytes(read_image(sample_image)).decode("utf-8"),
                "neoplastic cells in breast pathology & inflammatory cells"
            ]
        ]
    }
}
data_json = json.dumps(data)

# Create request json
request_file_name = "sample_request_data.json"
with open(request_file_name, "w") as request_file:
    json.dump(data, request_file)

response = ml_client_workspace.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    deployment_name=deployment_name,
    request_file=request_file_name,
)
```

## Use MedImageParse REST API
MedImageParse model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 256 | Count of inputs passed to the model. You're limited by how much data can be passed in a single POST request, which depends on the size of your images. Therefore, it's reasonable to keep this number in the dozens. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the image bytes encoded using base64 and decoded as utf-8 string. <br/>**NOTE**: The image should be resized to `1024x1024` pixels before submitting to the model, preserving the aspect ratio. Empty space should be padded with black pixels. See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) sample notebook for an example of resizing and padding code.<br/><br/> The input text is a string containing multiple sentences separated by the special character `&`. For example: `tumor core & enhancing tumor & non-enhancing tumor`. In this case, there are three sentences, so the output consists of three images with segmentation masks. |

### Request example

**Requesting segmentation of all cells in a pathology image** 
```JSON
{
  "input_data": {
    "columns": [
      "image",
      "text"
    ],
    "index":[0],
    "data": [
      ["iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAbSURBVBhXY/gUoPS/fhfDfwaGJe///9/J8B8A\nVGwJ5VDvPeYAAAAASUVORK5CYII=\n",
      "neoplastic & inflammatory cells "]
    ]
  }
}
```

### Response schema

Response payload is a list of JSON-formatted strings, each corresponding to a submitted image. Each string contains a `segmentation_object` object.

`segmentation_object` contains the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_features`       | `segmentation_mask` | An object representing the segmentation masks for a given image |
| `text_features`       | `list[string]` |  List of strings, one per each submitted text string, classifying the segmentation masks into one of 16 biomedical segmentation categories each: `liver`, `lung`, `kidney`, `pancreas`, `heart anatomies`, `brain anatomies`, `eye anatomies`, `vessel`, `other organ`, `tumor`, `infection`, `other lesion`, `fluid disturbance`, `other abnormality`, `histology structure`, `other` |

`segmentation_mask` contains the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`       | `string` | A base64-encoded NumPy array containing the one-hot encoded segmentation mask. There could be multiple instances of objects in the returned array. Decode and use `np.frombuffer` to deserialize. The array contains a three-dimensional matrix. The array's size is `1024x1024` (matching the input image dimensions), with the third dimension representing the number of input sentences provided. See the provided [sample notebooks](#learn-more-from-samples) for decoding and usage examples. |
| `shape`       | `list[int]` | A list representing the shape of the array (typically `[NUM_PROMPTS, 1024, 1024]`) |
| `dtype`       | `string` | An instance of the [NumPy dtype class](https://numpy.org/doc/stable/reference/arrays.dtypes.html) serialized to a string. Describes the data packing in the data array. |

### Response example
**A simple inference requesting segmentation of two objects** 
```JSON
[
  {
    "image_features": "{ 
    'data': '4oCwUE5HDQoa...',
    'shape': [2, 1024, 1024], 
    'dtype': 'uint8'}",
    "text_features": ['liver', 'pancreas']
  }
]
```

### Supported image formats

The deployed model API supports images encoded in PNG format. For optimal results, we recommend using uncompressed/lossless PNGs with RGB images.

As described in the API specification, the model only accepts images in the resolution of `1024x1024`pixels. Images need to be resized and padded (in the case of non-square aspect ratio).

See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) notebook for techniques and sample code useful for submitting images of various sizes stored using various biomedical imaging formats.

## Learn more from samples
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

#### Getting started
* [Deploying and Using MedImageParse](https://aka.ms/healthcare-ai-examples-mip-deploy): Learn how to deploy the MedImageParse model and integrate it into your workflow.

#### Advanced inferencing techniques and samples
* [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples): Understand how to use MedImageParse to segment a wide variety of different medical images and learn some prompting techniques. 

## Related content

* [CXRReportGen for grounded report generation](deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
