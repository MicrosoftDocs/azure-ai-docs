---
title: How do Deploy MedImageInsight Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use MedImageInsight Healthcare AI Model with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
zone_pivot_groups: ?????
---

# How to use MedImageInsight Healthcare AI Model for Generating Image Embeddings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy MedImageInsight as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive and interpret results

## MedImageInsight - the Medical Imaging Embedding model
MedImageInsight Foundational Model for Health is a powerful model that can process a wide variety of medical images including X-Ray, CT, MRI, clinical photography, dermoscopy, histopathology, ultrasound, and mammography. Rigorous evaluations demonstrate MedImageInsight's ability to achieve state-of-the-art (SOTA) or human expert level performance across classification, image-image search, and fine-tuning tasks.  Specifically, on public datasets, MedImageInsight achieves or exceeds SOTA in chest X-ray disease classification and search, dermatology classification and search, OCT classification and search, 3D medical image retrieval, and near SOTA for histopathology classification and search.  

Embedding model is the "swiss army knife" of foundational models since it is capable of serving as the basis of many different solutions - from classification to more complex scenarios like group matching or outlier detection. 

:::image type="content" source="../../media/how-to/healthcare-ai/healthcare-embedding-capabilities.gif" alt-text="Embedding model capable of supporting similarity search and quality control scenarios":::

Here we will explain how to deploy MedImageInsight using Azure AI Model Catalog using Azure AI Studio or Azure Machine Learning Studio and provide links to more in-depth tutorials and samples.

## Prerequisites

To use MedImageInsight models with Azure AI Studio or Azure Machine Learning Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageInsight model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../../concepts/deployments-overview.md)

## Work with an Embedding Model

### Using REST API to consume the model

MedImageInsight embedding model can be consumed as a REST API using simple GET requests or by creating a client like so:

```python
TODO: Client code
```

Note that in the deployment configuration you get to choose authentication method. This example uses Azure ML Token-based authentication.

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve embeddings.

```python
import base64
import json
import os

sample_image_xray = os.path.join(image_path)

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

data = {
    "input_data": {
        "columns": ["image", "text"],
        #  IMPORTANT: Modify the index as needed
        "index": [0],
        "data": [
            [
                base64.encodebytes(read_image(sample_image_xray)).decode("utf-8"),
                "x-ray chest anteroposterior Pneumonia",
            ]
        ],
    },
    "params": {"get_scaling_factor": True},
}

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

## Reference for MedImageInsight REST API
MedImageInsight model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload | |
| `params`   | `[object]` | N<br/>`null` | An object containing parameters passed to the model| |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"text"`, `"image"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 1024| Count of inputs passed to the model. Note that you are limited by how much data can be passed in a single POST request which will depend on the size of your images, so it is reasonable to keep this number in the dozens |
| `data`   | `list[list[string]]` | Y | "" | The list contains the number of items passed to the model which is defined by the index parameter. Each item is a list of two strings, order is defined by the "columns" parameter. The `text` string contains text to embed, the `image` string are the image bytes encoded using base64 and decoded as utf-8 string |

The `params` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_standardization_jpeg_compression_ratio`       | `integer`       | N<br/>`75`    |  0 - 100 | What compression rate to apply to the input images. 75 yields best results. |
| `image_standardization_image_size`   | `integer` | N<br/>`512` | TODO | TODO |
| `get_scaling_factor`   | `boolean` | N<br/>`True` | `"True"` OR `"False"` | Whether the model should return "temperature" scaling factor. This factor is useful when you are planning to compare multiple cosine similarity values in application like classification. For usage refer to the zero-shot classification example. |

### Request Example

**A simple inference requesting embedding of a single string** 
```JSON
{
  "input_data": {
    "columns": [
      "image",
      "text"
    ],
    "index":[0],
    "data": [
      ["", "a quick brown fox jumps over the lazy dog"]
    ]
  },
  "params": {}
}
```

**Request for embedding of an image and a string, requesting for return of the scaling factor** 
```JSON
{
  "input_data": {
    "columns": [
      "image",
      "text"
    ],
    "index":[0],
    "data": [
      ["4oCwUE5HDQoaCgAAAA1JSERSAAAAAgAAAAIIBgAAAHLCtg0kAAAAAXNSR0IAwq7DjhzDqQAAAARnQU1BAADCscKPC8O8YQUAAAAJcEhZcwAAFiUAABYlAUlSJMOwAAAAG0lEQVQYV2PDuBTCoMO0wr9+F8ODfwbigKAlw6/Dv8O/w5/DicOwHwBUbAnDpVDDrz3DpgAAAABJRU5Ewq5CYOKAmg==",
       "Microsoft Products are Generally Bug Free"]
    ]
  },
  "params": {
    "get_scaling_factor": True
  }
}
```

### Response schema

Response payload is a JSON formatted string containing the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_features`       | `list[list[float]]` |  If requested, list of vectors, one per each submitted image. |
| `text_features`   | `list[list[float]]` |  If requested, list of vectors, one per each submitted text string. |
| `scaling_factor`   | `float` |  If requested, the scaling factor |

### Response example
**A simple inference requesting embedding of a single string** 
```JSON
{
  "image_features": [[0.029661938548088074, -0.027228673920035362, ... , -0.0328846238553524]],
  "text_features": [[0.0028937323950231075, 0.004354152828454971, -0.0227945726364851, ..., 0.002080598147585988]],
  "scaling_factor": 4.516357
}
```

## More Examples 
MedImageInsight is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more specific examples of solving a variety of tasks with MedImageInsight see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using MedImageInsight](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/deploy.ipynb): learn how to deploy the MedImageInsight model programmatically and issue an API call to it.

### Classification Techniques
* [Building a Zero-Shot Classifier](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/zero-shot-classification.ipynb): discover how to create a classifier without the need training or large amount of labeled training data using MedImageInsight.

* [Enhancing Classification with Adapter Networks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/adapter-training.ipynb): improve classification performance by building a small adapter network on top of MedImageInsight.

### Advanced Applications
* [Inferring MRI Acquisition Parameters from Pixel Data](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/exam-parameter-demo/exam-parameter-detection.ipynb): understand how to extract MRI exam acquisition parameters directly from imaging data.

* [Detecting Outliers in Medical Image Series](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/outlier.ipynb): learn methods to identify anomalies in full series of medical images using MedImageInsight.


## Related content

* [MedImageParse for medical image segmentation](./deploy-medimageparse.md)
* [CXRReportGen for grounded report generation](./deploy-cxrreportgen.md)
