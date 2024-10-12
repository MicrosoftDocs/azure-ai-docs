---
title: How do Deploy CXRReportGen Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use CXRReportGen Healthcare AI Model with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 09/30/2024
ms.reviewer: itarapov
reviewer: fkriti
ms.author: mopeakande
author: msakande
ms.custom: references_regions, generated
zone_pivot_groups: ?????
---

# How to use CXRReportGen Healthcare AI Model for Generating Grounded Findings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy CXRReportGen as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive and interpret results

## CXRReportGen - Grounded Report Generation Model for Chest X-rays
Radiology reporting demands detailed image understanding, integration of multiple inputs (including comparisons with prior imaging), and precise language generation, making it an ideal candidate for generative multimodal models. CXRReportGen not only performs the task of generating a list of findings from a chest Xray study, but also extends it by incorporating the localization of individual findings on the image—a task we refer to as grounded report generation. Grounding enhances the clarity of image interpretation and the transparency of AI-generated text, thereby improving the utility of automated report drafting. The model combines a radiology-specific image encoder with a large language model and it takes as inputs a more comprehensive set of data than many traditional approaches: the current frontal image, the current lateral image, the prior frontal image, the prior report, and the Indication, Technique, and Comparison sections of the current report. These additions significantly enhance report quality and reduce hallucinations, demonstrating the feasibility of grounded reporting as a novel and richer task in automated radiology.

## Prerequisites

To use CXRReportGen model with Azure AI Studio or Azure Machine Learning Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

CXRReportGen model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../../concepts/deployments-overview.md)

## Work with a Grounded Report Generation Model for Chest X-rays

### Using REST API to consume the model

CXRReportGen report generation model can be consumed as a REST API using simple GET requests or by creating a client like so:

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

## Reference for CXRReportGen REST API
CXRReportGen model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload | 

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"frontal_image"`, `"lateral_image"`, `"prior_image"`,`"indication"`, `"technique"`,  `"comparison"`, `"prior_report"`  | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 1024| Count of inputs passed to the model. Note that you are limited by how much data can be passed in a single POST request which will depend on the size of your images, so it is reasonable to keep this number in the dozens |
| `data`   | `list[list[string]]` | Y | "" | The list contains the list of items passed to the model. Length of the list is defined by the index parameter. Each item is a list of several strings, order and meaning is defined by the "columns" parameter. The text strings contains text, the image strings are the image bytes encoded using base64 and decoded as utf-8 string |


### Request Example

**A simple inference requesting list of findings for a single frontal image with no indication provided** 
```JSON
{
  "input_data": {
    "columns": [
      "frontal_image"
    ],
    "index":[0],
    "data": [
      ["iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAbSURBVBhXY/gUoPS/fhfDfwaGJe///9/J8B8A\nVGwJ5VDvPeYAAAAASUVORK5CYII=\n"]
    ]
  }
}
```

**More complex request passing frontal, lateral, indication and technique** 
```JSON
{
  "input_data": {
    "columns": [
      "frontal_image",
      "lateral_image",
      "indication",
      "technique"
    ],
    "index":[0],
    "data": [
      ["iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAbSURBVBhXY/gUoPS/fhfDfwaGJe///9/J8B8A\nVGwJ5VDvPeYAAAAASUVORK5CYII=\n",
        "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAbSURBVBhXY/gUoPS/fhfDfwaGJe///9/J8B8A\nVGwJ5VDvPeYAAAAASUVORK5CYII=\n",
       "Cough and wheezing for 5 months",
       "PA and lateral views of the chest were obtained"]
    ]
  }
}
```

### Response schema

Response payload is a JSON formatted string containing the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output`       | `list[list[string, list[list[float]]]]` | The list of findings. Each finding is an item in a list represented by a list that contains a string with the text of finding and a list that contains bounding boxes. Each bounding box is represented by a list of four coordinates of the bounding box related to the finding in the following order: `x_min`, `y_min`, `x_max`, `y_max`. Each coordinate value is between 0 and 1, thus to obtain coordinates in the space of the image for rendering or processing these values need to be multiplied by image width or height accordingly|

### Response example
**A simple inference requesting embedding of a single string** 
```JSON
{
    "output": [
        ["The heart size is normal.", null],
        ["Lungs demonstrate blunting of both costophrenic angles.", [[0.005, 0.555, 0.965, 0.865]]],
        ["There is an area of increased radiodensity overlying the left lower lung.", [[0.555, 0.405, 0.885, 0.745]]],
        ["Healed fractures of the left fourth, fifth, sixth, seventh, and eighth posterior ribs are noted.", [[0.585, 0.135, 0.925, 0.725]]]
    ]
}
```

## More Examples 
CXRReportGen is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using CXRReportGen](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/cxrreportgen/deploy.ipynb): learn how to deploy the CXRReportGen model and integrate it into your workflow.
* [Calling CXRReportGen and Visualizing Results](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/cxrreportgen/examples.ipynb): understand how to submit various types of Chest X-Ray studies to CXRReportGen, interpret the results and apply some visualization techniques. 

## Related content

* [MedImageParse for medical image segmentation](deploy-medimageparse.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
