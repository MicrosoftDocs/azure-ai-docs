---
title: Deploy CXRReportGen Healthcare AI Model in Foundry
titleSuffix: Microsoft Foundry
description: Learn how to deploy and use the CXRReportGen healthcare AI model with Microsoft Foundry to generate grounded findings from chest X-ray studies. Follow step-by-step instructions to deploy, configure, and invoke the model endpoint.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/26/2026
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
manager: nitinme
author: msakande
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a data scientist, I want to deploy the CXRReportGen healthcare AI model so that I can generate grounded findings from chest X-ray studies.

---

# How to use CXRReportGen healthcare AI model to generate grounded findings

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

CXRReportGen is a multimodal model that generates grounded findings from chest X-ray studies. In this article, you learn how to deploy CXRReportGen as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

1. Deploy the model to a self-hosted managed compute.
1. Grant permissions to the endpoint.
1. Send test data to the model, receive results, and interpret them.

CXRReportGen generates a list of findings from a chest X-ray study and also performs a *grounded report generation or grounding task*. That task incorporates the localization of individual findings on the image. The model combines a radiology-specific image encoder with a large language model and takes as inputs a more comprehensive set of data than many traditional approaches to enhance report quality and reduce incorrect information. To learn more about the model, see [Learn more about the model](#learn-more-about-the-model).

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../../includes/hub-project-name.md)]](../hub-create-projects.md)

- Azure role-based access controls (Azure RBAC) grant access to operations in Microsoft Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. Deploying models and invoking endpoints requires this role. For more information, see [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).

- Python 3.8 or later.

- Install the required Python packages:
  ```bash
  pip install azure-ai-ml azure-identity
  ```

## Sample notebook

For a complete working example, see this interactive Python notebook:

* [Deploying and Using CXRReportGen](https://aka.ms/healthcare-ai-examples-cxr-deploy): Learn how to deploy the CXRReportGen model and integrate it into your workflow. This notebook also covers bounding-box parsing and visualization techniques.


## Deploy the model to a managed compute

Deployment to a self-hosted managed inference solution lets you customize and control all the details about how the model's served. The deployment process creates an online endpoint with a unique scoring URI and authentication keys. This endpoint lets you send inference requests to your model. You configure the compute resources (such as GPU-enabled VMs) and set deployment parameters like instance count and request timeout values.

To deploy the model programmatically or from its model card in Microsoft Foundry, see [How to deploy and infer with a managed compute deployment](../deploy-models-managed.md). After deployment completes, note your endpoint name and deployment name for use in the inference code.

## Send inference requests to the grounded report generation model

In this section, you consume the model and make basic calls to it.

### Use REST API to consume the model

Use the model as a REST API, by using simple GET requests or by creating a client as follows:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Authenticate using Azure credentials
credential = DefaultAzureCredential()

# Create ML client from workspace configuration file (config.json)
# The config file is automatically created on Azure ML compute instances
ml_client_workspace = MLClient.from_config(credential)
```

This code authenticates your session and creates a workspace client that you use to invoke the deployed endpoint. The `DefaultAzureCredential` automatically uses available authentication methods in your environment (managed identity, Azure CLI, and environment variables).

Reference: [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

In the deployment configuration, you select an authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see [Set up authentication](../../../machine-learning/how-to-setup-authentication.md). The client is created from a configuration file that's created automatically for Azure Machine Learning virtual machines (VMs). Learn more in the [MLClient.from_config API reference](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

After you deploy the model, use the following code to send data and get a list of findings and the corresponding bounding boxes.

```python
import base64
import json
import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Helper function to read image as bytes
def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

# Set your endpoint and deployment names from the deployment step
endpoint_name = "your-endpoint-name"  # Replace with your endpoint name
deployment_name = "your-deployment-name"  # Replace with your deployment name

# Set paths to your chest X-ray images
frontal_path = "path/to/frontal_image.png"  # Replace with your frontal image path
lateral_path = "path/to/lateral_image.png"  # Replace with your lateral image path (optional)

# Set clinical context
indication = "Cough and wheezing for 5 months"
technique = "PA and lateral views of the chest were obtained"
comparison = "None"

# Encode images to base64 and prepare input data
input_data = {
    "frontal_image": base64.encodebytes(read_image(frontal_path)).decode("utf-8"),
    "lateral_image": base64.encodebytes(read_image(lateral_path)).decode("utf-8"),
    "indication": indication,
    "technique": technique,
    "comparison": comparison,
}

# Structure data according to the model's expected schema
data = {
    "input_data": {
        "columns": list(input_data.keys()),
        "index": [0],  # Set to number of concurrent requests (keep under 10)
        "data": [
            list(input_data.values()),
        ],
    }
}

# Create request JSON file
request_file_name = "sample_request_data.json"
with open(request_file_name, "w") as request_file:
    json.dump(data, request_file)

# Authenticate and create workspace client
credential = DefaultAzureCredential()
ml_client_workspace = MLClient.from_config(credential)

# Invoke the endpoint
response = ml_client_workspace.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    deployment_name=deployment_name,
    request_file=request_file_name,
)

# Parse and display the response
result = json.loads(response)
print("Generated Findings:")
for finding_text, bounding_boxes in result["output"]:
    print(f"- {finding_text}")
    if bounding_boxes:
        print(f"  Bounding boxes: {bounding_boxes}")
```

This code prepares a request with chest X-ray images and clinical context, sends it to your deployed endpoint, and receives a structured response. The model returns a list of clinical findings, each with optional bounding box coordinates indicating where on the image the finding is located. Bounding box coordinates are normalized (0-1 range), so multiply by image dimensions to get pixel coordinates.

Reference: [MLClient.online_endpoints](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations), [base64 module](https://docs.python.org/3/library/base64.html)

## Reference for REST API

The CXRReportGen model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

The request payload is a JSON-formatted string with the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload | 

The `input_data` object has the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"frontal_image"`, `"lateral_image"`, `"prior_image"`,`"indication"`, `"technique"`,  `"comparison"`, `"prior_report"`  | An object with strings mapping data to inputs you pass to the model.|
| `index`   | `integer` | Y | 0 - 10 | Count of inputs you pass to the model. You're limited by how much GPU RAM you have on the VM where CxrReportGen is hosted, and by how much data you can pass in a single POST request—which depends on the size of your images. Therefore, keep this number under 10. Check model logs if you're getting errors when passing multiple inputs. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the list of items you pass to the model. The length of the list is defined by the index parameter. Each item is a list of several strings. The order and meaning are defined by the `columns` parameter. The text strings contain text. The image strings are the image bytes encoded using base64 and decoded as utf-8 string |


### Request example

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

**More complex request passing frontal, lateral, indication, and technique** 
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

The response payload is a JSON-formatted string containing the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output`       | `list[list[string, list[list[float]]]]` | The list of findings. Each finding is an item in a list represented by a list that contains a string with the text of finding and a list that contains bounding boxes. Each bounding box is represented by a list of four coordinates of the bounding box related to the finding in the following order: `x_min`, `y_min`, `x_max`, `y_max`. Each coordinate value is between 0 and 1, so to get coordinates in the space of the image for rendering or processing, multiply these values by image width or height accordingly. |

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

### Supported image formats

The deployed model API supports images encoded in PNG or JPEG formats. For optimal results, we recommend using uncompressed or lossless PNGs with 8-bit monochromatic images.

## Learn more about the model

Radiology reporting demands detailed image understanding, integration of multiple inputs (including comparisons with prior imaging), and precise language generation. These requirements make it an ideal candidate for generative multimodal models. CXRReportGen generates a list of findings from a chest X-ray study and also performs a _grounded report generation_ or _grounding_ task. That task incorporates the localization of individual findings on the image. Grounding enhances the clarity of image interpretation and the transparency of AI-generated text, which ends up improving the utility of automated report drafting.

The following animation demonstrates the conceptual architecture of the CXRReportGen model, which consists of an embedding model paired with a general reasoner large language model (LLM). 

:::image type="content" source="../../media/how-to/healthcare-ai/healthcare-reportgen.gif" alt-text="Screenshot of an animated diagram showing the CXRReportGen model architecture with a radiology-specific image encoder processing chest X-ray inputs, followed by a large language model that generates findings with bounding box coordinates for grounded report generation.":::

The CXRReportGen model combines a radiology-specific image encoder with a large language model and takes as inputs a more comprehensive set of data than many traditional approaches. The input data includes the current frontal image, the current lateral image, the prior frontal image, the prior report, and the indication, technique, and comparison sections of the current report. These additions significantly enhance report quality and reduce incorrect information. They ultimately demonstrate the feasibility of grounded reporting as a novel and richer task in automated radiology.

## Related content

* [MedImageParse models for medical image segmentation](deploy-medimageparse.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)