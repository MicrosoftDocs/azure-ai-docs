---
title: How to deploy and use MedImageParse 3D healthcare AI model with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use MedImageParse 3D Healthcare AI Model with Azure AI Foundry.
ms.service: azure-ai-foundry
manager: scottpolly
ms.topic: how-to
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
#Customer intent: As a Data Scientist I want to learn how to use the MedImageParse 3D healthcare AI model to segment medical images.

---

# How to use MedImageParse 3D healthcare AI model for segmentation of medical images

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy MedImageParse 3D as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive, and interpret results.


## MedImageParse 3D - prompt-based segmentation of medical images
Similar to our [MedImageParse model](deploy-medimageparse.md) model, MedImageParse 3D uses a combination of a text prompt and a medical image to create a segmentation mask. However, unlike MedImageParse, the MedImageParse 3D model takes in an entire 3D volume - which is a common way of representing the imaged area for cross-sectional imaging modalities like CT or MRI - and generates the 3-dimensional segmentation mask. 

## Prerequisites

To use the MedImageParse 3D model, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageParse 3D model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served. You can deploy the model through the catalog UI (in [Azure AI Foundry](https://aka.ms/healthcaremodelstudio) or [Azure Machine Learning studio](https://ml.azure.com/model/catalog)) or deploy programmatically.

To __deploy the model through the UI__:

1. Go to the catalog.
1. Search for _MedImageParse3D_ and select the model card.
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

Consume the MedImageParse 3D segmentation model as a REST API, using simple GET requests or by creating a client as follows:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

ml_client_workspace = MLClient.from_config(credential)
```

In the deployment configuration, you get to choose authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see the [corresponding documentation page](../../../machine-learning/how-to-setup-authentication.md). Also, note that the client is created from a configuration file that is created automatically for Azure Machine Learning virtual machines (VMs). Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve segmentation masks.

```python
import base64
import json
import urllib.request
import matplotlib.pyplot as plt
import nibabel as nib
import tempfile
import os

# Replace with the path to your NIfTI input file
sample_image = "./examples/amos_0308.nii.gz"
with open(sample_image, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Prepare data payload
data = {
    "input_data": {
        "columns": [ "image", "text" ],
        "index": [ 0 ],
        "data": [
            [
                base64_image,
                "pancreas"
            ]
        ]
    }
}
data_json = json.dumps(data)
body = str.encode(data_json)

# Add your endpoint URL and API key
url = "<your-endpoint-url>"
api_key = "<your-api-key>"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
}

req = urllib.request.Request(url, body, headers)

# Make sure decode_base64_to_nifti() and plot_segmentation_masks() are defined above
try:
    response = urllib.request.urlopen(req)
    result = response.read()
    result_list = json.loads(result)

    # Extract and decode NIfTI segmentation output
    nifti_file_str = result_list[0]["nifti_file"]
    nifti_file_data = decode_base64_to_nifti(nifti_file_str)

    print(nifti_file_data.shape)
    plot_segmentation_masks(nifti_file_data)

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
```

## Use MedImageParse 3D REST API

MedImageParse 3D model assumes a simple single-turn interaction where one request produces one response. 

### Request schema

Request payload is a JSON formatted string containing the following parameters:

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Yes    | An object containing the input data |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Yes    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Yes | 0 | This parameter is used when multiple inputs are passed to the endpoint in one call. This model's endpoint wrapper does not use this parameter, so it should be set to 0. |
| `data`   | `list[list[string]]` | Yes | Base64 image + text prompt | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the input volume in NIfTI format encoded using base64 and decoded as utf-8 string. The input text is a string containing the target (e.g., organ) to be segmented. |

### Request example

**Requesting segmentation of pancreas**
```JSON
{
  "input_data": {
    "columns": [
      "image",
      "text"
    ],
    "index":[0],
    "data": [
      ["iVBORw0KGgoAAAAN...",
      "pancreas"]
    ]
  }
}
```

### Response schema

The response is a list of objects. Each object contains the segmentation result for one input. The segmentation mask is encoded as a Base64 string inside a serialized JSON object under the key `nifti_file`.

| Key            | Type   | Description                                                                 |
| -------------- | ------ | --------------------------------------------------------------------------- |
| `nifti_file` | string | JSON-formatted string containing the base64-encoded NIfTI segmentation mask |

### Response example

```json
[
  {
    "nifti_file": "{\"data\": \"H4sIAAAAAAAE...\"}"
  }
]
```

The `nifti_file` field is a **stringified JSON object**. To decode:

```python
import json
import base64
import tempfile
import nibabel as nib
import os

def decode_base64_to_nifti(base64_string: str):
    """
    Decode a Base64 string back to a NIfTI image.

    Args:
        base64_string (str): Base64 encoded string of NIfTI image, wrapped in a JSON string

    Returns:
        np.ndarray: Decoded NIfTI image data as a NumPy array
    """
    # Parse the inner JSON object to extract the 'data' field
    base64_string = json.loads(base64_string)["data"]

    # Decode the Base64 string to raw bytes
    byte_data = base64.b64decode(base64_string)

    # Write the decoded bytes to a temporary .nii.gz file
    with tempfile.NamedTemporaryFile(suffix='.nii.gz', delete=False) as temp_file:
        temp_file.write(byte_data)     # Write bytes to file
        temp_file.flush()              # Ensure it's fully written to disk
        nifti_image = nib.load(temp_file.name)  # Load the image with nibabel

    # Clean up the temporary file to avoid clutter
    os.unlink(temp_file.name)

    # Return the image as a NumPy array
    return nifti_image.get_fdata()
```
To plot segmentation mask
```python
import matplotlib.pyplot as plt

def plot_segmentation_masks(segmentation_masks):
    """
    Plot a series of 2D slices from a 3D segmentation mask volume.
    Only slices with non-zero masks are displayed.

    Args:
        segmentation_masks (np.ndarray): A 3D NumPy array of shape (H, W, D),
                                         where D is the number of slices.
    """
    index = 1
    plt.figure(figsize=(15, 15))

    # Loop through each slice (along the depth axis)
    for i in range(segmentation_masks.shape[2]):
        # Only show slices that contain non-zero segmentation
        if segmentation_masks[:, :, i].sum() > 0:
            plt.subplot(4, 4, index)  # Adjust grid size if needed
            plt.imshow(segmentation_masks[:, :, i], cmap='gray')
            plt.axis('off')
            index += 1

    plt.tight_layout()
    plt.show()
```
### Supported input formats

The deployed model API supports volumes encoded in NIfTI format.

<!-- 
See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) notebook for techniques and sample code useful for submitting images of various sizes stored using various biomedical imaging formats.

## Learn more from samples
For more MedImageParse 3D examples see the following interactive Python Notebooks: 

#### Getting started
* [Deploying and Using MedImageParse 3D](https://aka.ms/healthcare-ai-examples-mip-deploy): Learn how to deploy the MedImageParse 3D model and integrate it into your workflow.

#### Advanced inferencing techniques and samples
* [Segmentation examples](https://aka.ms/healthcare-ai-examples-mip-examples): Understand how to use MedImageParse 3D to segment images in DICOM and NIfTI formats.  -->

## Related content

* [CXRReportGen for grounded report generation](deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
