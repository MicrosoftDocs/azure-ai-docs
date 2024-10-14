---
title: How to Deploy MedImageParse Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use MedImageParse Healthcare AI Model with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: fkriti
ms.author: mopeakande
author: msakande
zone_pivot_groups: ?????
---

# How to use MedImageParse Healthcare AI Model for Generating Grounded Findings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy MedImageParse as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive and interpret results


## MedImageParse - Prompt-based Segmentation of Medical Images
Biomedical image analysis is crucial for discovery in fields like cell biology, pathology, and radiology. Traditionally, tasks such as segmentation, detection, and recognition of relevant objects have been addressed separately, which can limit the overall effectiveness of image analysis. MedImageParse unifies these tasks through image parsing, jointly conducting segmentation, detection, and recognition across numerous object types and imaging modalities. By leveraging the interdependencies among these subtasks—such as the semantic labels of segmented objects—the model enhances accuracy and enables novel applications. For instance, it allows users to segment all relevant objects in an image using a simple text prompt, eliminating the need to manually specify bounding boxes for each object. Remarkably, this was achieved using only standard segmentation datasets, augmented by natural-language labels or descriptions harmonized with established biomedical object ontologies. This approach not only improved individual task performance but also offered an all-in-one tool for biomedical image analysis, paving the way for more efficient and accurate image-based biomedical discovery.

## Prerequisites

To use MedImageParse model with Azure AI Studio or Azure Machine Learning Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageParse model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../../concepts/deployments-overview.md)

## Work with an Segmentation Model

### Using REST API to consume the model

MedImageParse segmentation model can be consumed as a REST API using simple GET requests or by creating a client like so:

```python
from azure.ai.ml import MLClient
from azure.identity import DeviceCodeCredential

credential = DeviceCodeCredential()
credential.authenticate()

ml_client_workspace = MLClient.from_config(credential)
```

Note that in the deployment configuration you get to choose authentication method. This example uses Azure ML Token-based authentication. Also note that client is created from configuration file. This file is created automatically for Azure Machine Learning VMs. Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient?view=azure-python#azure-ai-ml-mlclient-from-config).

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

## Reference for MedImageParse REST API
MedImageParse model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"image"`, `"text"` | An object containing the strings mapping data to 
| `index`   | `integer` | Y | 0 - 256 | Count of inputs passed to the model. Note that you are limited by how much data can be passed in a single POST request which will depend on the size of your images, so it is reasonable to keep this number in the dozens. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings, order is defined by the "columns" parameter. The `text` string contains the prompt text, the `image` string are the image bytes encoded using base64 and decoded as utf-8 string |

### Request Example

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

Response payload is a JSON formatted string containing the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_features`       | `binary` |  TODO |
| `text_features`       | `binary` |  TODO |


### Response example
**A simple inference requesting embedding of a single string** 
```JSON
TODO
```

## Explore Quickstarts
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using MedImageParse](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/mip-deploy.ipynb): learn how to deploy the MedImageParse model and integrate it into your workflow.
* [Generating Segmentation for a Variety of Imaging Modalities](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/call-examples.ipynb): understand how to use MedImageParse to segment a wide variety of different medical images and learn some prompting techniques. 

## Related content

* [CXRReportGen for grounded report generation](deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
