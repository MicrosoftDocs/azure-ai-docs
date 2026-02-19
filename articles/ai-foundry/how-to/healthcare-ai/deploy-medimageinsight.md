---
title: Deploy MedImageInsight for Medical Image Embeddings
titleSuffix: Microsoft Foundry
description: Deploy MedImageInsight to generate medical image embeddings for X-Ray, CT, MRI, and more. Get step-by-step deployment guidance and API examples.
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

#customer intent: As a data scientist, I want to deploy the MedImageInsight healthcare AI model so that I can generate embeddings for medical images.
---

# How to use MedImageInsight healthcare AI model for medical image embedding generation

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

MedImageInsight is a healthcare AI model that generates embeddings for medical images including X-Ray, CT, MRI, clinical photography, dermoscopy, histopathology, ultrasound, and mammography. This article shows you how to deploy MedImageInsight as an online endpoint for real-time inference and send API requests to generate medical image embeddings. The steps you take are:

1. Deploy the model to a self-hosted managed compute.
1. Grant permissions to the endpoint.
1. Send test data to the model, receive results, and interpret them.

To learn more about MedImageInsight, see [Learn more about the model](#learn-more-about-the-model).

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../../includes/hub-project-name.md)]](../hub-create-projects.md)

- Azure role-based access controls (Azure RBAC) grant access to operations in Microsoft Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. Deploying models and invoking endpoints requires this role. For more information, see [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).

- Python 3.8 or later

- Install the required Python packages:
   ```bash
   pip install azure-ai-ml azure-identity
   ```

## Sample notebooks

For complete working examples, see these interactive Python notebooks:

* **Getting started**

    * [Deploying and Using MedImageInsight](https://aka.ms/healthcare-ai-examples-mi2-deploy): Deploy the MedImageInsight model programmatically and issue an API call to it.

* **Classification techniques**

    * [Building a Zero-Shot Classifier](https://aka.ms/healthcare-ai-examples-mi2-zero-shot): Use MedImageInsight to create a classifier without the need for training or large amounts of labeled ground truth data.
    
    * [Enhancing Classification with Adapter Networks](https://aka.ms/healthcare-ai-examples-mi2-adapter): Improve classification performance by building a small adapter network on top of MedImageInsight.

* **Advanced applications**

    * [Inferring MRI Acquisition Parameters from Pixel Data](https://aka.ms/healthcare-ai-examples-mi2-exam-parameter): Extract MRI exam acquisition parameters directly from imaging data.
    
    * [Scalable MedImageInsight Endpoint Usage](https://aka.ms/healthcare-ai-examples-mi2-advanced-call): Generate embeddings of medical images at scale using the MedImageInsight API while handling potential network issues gracefully.


## Deploy the model to a managed compute

Deployment to a self-hosted managed inference solution lets you customize and control all the details about how the model's served. The deployment process creates an online endpoint with a unique scoring URI and authentication keys. This endpoint lets you send inference requests to your model. You configure the compute resources (such as GPU-enabled VMs) and set deployment parameters like instance count and request timeout values.

To deploy the model programmatically or from its model card in Microsoft Foundry, see [How to deploy and infer with a managed compute deployment](../deploy-models-managed.md). After deployment's complete, note your endpoint name and deployment name for use in the inference code.


## Send inference requests to the embedding model

In this section, you consume the model and make basic calls to it.

### Use REST API to consume the model

Use the model as a REST API by using simple GET requests or by creating a client as follows:

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

**References**: [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient) | [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

In the deployment configuration, you select an authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see [Set up authentication](../../../machine-learning/how-to-setup-authentication.md). The client is created from a configuration file that's created automatically for Azure Machine Learning virtual machines (VMs). Learn more in the [MLClient.from_config API reference](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

After you deploy the model, use the following code to send data and get embeddings.

```python
import base64
import json
import os

# Configure your endpoint details
endpoint_name = "medimageinsight"
deployment_name = "medimageinsight-v1"

sample_image_xray = os.path.join(image_path)

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()

# Prepare the request payload
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

This code reads an X-ray image, encodes it as base64, and sends it with descriptive text to the embedding endpoint. The response contains `image_features` (a 1,024-dimensional vector representing the image), `text_features` (vector for the text), and an optional `scaling_factor` used for classification tasks.

**References**: [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient) | [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) | [online_endpoints.invoke](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-invoke)

## Reference for REST API

The MedImageInsight model works with a simple single-turn interaction. One request gets one response. 

### Request schema

The request payload is a JSON-formatted string that contains the following parameters:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload | |
| `params`   | `[object]` | N<br/>`null` | An object containing parameters passed to the model| |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"text"`, `"image"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 1024| Count of inputs passed to the model. You're limited by how much data you can pass in a single POST request, which depends on the size of your images. Therefore, keep this number in the dozens |
| `data`   | `list[list[string]]` | Y | "" | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains text to embed. The `image` strings are the image bytes encoded using base64 and decoded as utf-8 string |

The `params` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `get_scaling_factor`   | `boolean` | N<br/>`True` | `"True"` or `"False"` | Whether the model should return "temperature" scaling factor. This factor is useful when you're planning to compare multiple cosine similarity values in an application like classification. It's essential for correct implementation of "zero-shot" type of scenarios. For usage, refer to the zero-shot classification example linked in the "Classification techniques" section of [Sample notebooks](#sample-notebooks). |

### Request example

**A simple inference that requests embedding of a single string** 
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
        "columns": ["image", "text"],
        "index": [0],
        "data": [
            [
                "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAAbSURBVBhXY/gUoPS/fhfDfwaGJe///9/J8B8A\nVGwJ5VDvPeYAAAAASUVORK5CYII=\n",
                "x-ray chest anteroposterior Pleural Effusion"
            ]
        ]
    },
    "params": {
        "get_scaling_factor": "true"
    }
}
```

### Response schema

The response payload is a JSON-formatted string that contains the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_features`       | `list[list[float]]` |  If requested, a list of vectors, one for each submitted image. |
| `text_features`   | `list[list[float]]` |  If requested, a list of vectors, one for each submitted text string. |
| `scaling_factor`   | `float` |  If requested, the scaling factor |

### Response example
**A simple inference that requests embedding of a single string** 
```JSON
{
  "image_features": [[0.029661938548088074, -0.027228673920035362, ... , -0.0328846238553524]],
  "text_features": [[0.0028937323950231075, 0.004354152828454971, -0.0227945726364851, ..., 0.002080598147585988]],
  "scaling_factor": 4.516357
}
```

### Other implementation considerations
The maximum number of tokens processed in the input string is 77. The system removes any tokens beyond 77 before it passes the input to the model. The model uses a Contrastive Language-Image Pre-Training (CLIP) tokenizer, which uses about three Latin characters per token.

The model embeds the submitted text into the same latent space as the image. As a result, strings describing medical images of certain body parts obtained with certain imaging modalities are embedded close to such images. Also, when you build systems on top of a MedImageInsight model, make sure that all your embedding strings are consistent with one another (word order and punctuation). For best results with the base model, strings should follow the pattern `<image modality> <anatomy> <exam parameters> <condition/pathology>.`, for example: `x-ray chest anteroposterior Atelectasis.`. 

If you fine-tune the model, you can change these parameters to better suit your application needs.

### Supported image formats
The deployed model API supports images encoded in PNG format. 

When the model receives the images, it preprocesses them by compressing and resizing them to `512x512` pixels.

The preferred compression format is lossless PNG that contains either an 8-bit monochromatic or RGB image. For optimization purposes, you can perform resizing on the client side to reduce network traffic.


## Learn more about the model

The MedImageInsight foundation model for health is a powerful model that can process a wide variety of medical images. These images include X-Ray, CT, MRI, clinical photography, dermoscopy, histopathology, ultrasound, and mammography images. Rigorous evaluations demonstrate MedImageInsight's ability to achieve state-of-the-art (SOTA) or human expert-level performance across classification, image-to-image search, and fine-tuning tasks. Specifically, on public datasets, MedImageInsight achieves or exceeds SOTA performance in chest X-ray disease classification and search, dermatology classification and search, optical coherence tomography (OCT) classification and search, and 3D medical image retrieval. The model also achieves near-SOTA performance for histopathology classification and search.  

An embedding model can serve as the basis of many different solutions—from classification to more complex scenarios like group matching or outlier detection. The following animation shows an embedding model being used for image similarity search and to detect images that are outliers.

:::image type="content" source="../../media/how-to/healthcare-ai/healthcare-embedding-capabilities.gif" alt-text="Screenshot of an animated diagram that shows an embedding model capable of supporting similarity search and quality control scenarios.":::

## Related content

* [MedImageParse models for medical image segmentation](deploy-medimageparse.md)
* [CXRReportGen for grounded report generation](./deploy-cxrreportgen.md)