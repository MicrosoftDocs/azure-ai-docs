---
title: How do Deploy MedImageParse Healthcare AI Model with AI Studio
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

## Reference for MedImageParse REST API
MedImageParse model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload |
| `params`   | `[object]` | Y    | An object containing parameters passed to the model|

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|


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
| `segmentation_mask`       | `binary` |  If requested, list of vectors, one per each submitted image. |


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
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using MedImageParse](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/deploy.ipynb): learn how to deploy the MedImageParse model and integrate it into your workflow.
* [Generating Segmentation for a Variety of Imaging Modalities](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/call-examples.ipynb): understand how to use MedImageParse to segment a wide variety of different medical images and learn some prompting techniques. 

## Related content

* [CXRReportGen for grounded report generation](./deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
