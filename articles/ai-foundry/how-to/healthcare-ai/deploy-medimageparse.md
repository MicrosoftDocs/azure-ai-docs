---
title: MedImageParse and MedImageParse 3D healthcare AI models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use MedImageParse and MedImageParse 3D Healthcare AI models with Azure AI Foundry.
ms.service: azure-ai-foundry
manager: scottpolly
ms.topic: how-to
ms.date: 04/24/2025
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
#Customer intent: As a Data Scientist I want to learn how to use the MedImageParse and MedImageParse 3D healthcare AI models to segment medical images.

---

# How to use MedImageParse healthcare AI models for segmentation of medical images

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy prompt-based image segmentation models, MedImageParse and MedImageParse 3D, as online endpoints for real-time inference. You also see how to issue basic calls to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive, and interpret results.

# [MedImageParse](#tab/medimageparse)

## MedImageParse

Biomedical image analysis is crucial for discovery in fields like cell biology, pathology, and radiology. Traditionally, tasks such as segmentation, detection, and recognition of relevant objects are addressed separately, which can limit the overall effectiveness of image analysis. However, MedImageParse unifies these tasks through image parsing, by jointly conducting segmentation, detection, and recognition across numerous object types and imaging modalities. By applying the interdependencies among these subtasks—such as the semantic labels of segmented objects—the model enhances accuracy and enables novel applications. For example, it allows users to segment all relevant objects in an image, by using a simple text prompt. This approach eliminates the need to manually specify bounding boxes for each object.  

The following image shows the conceptual architecture of the MedImageParse model where an image embedding model is augmented with a task adaptation layer to produce segmentation masks and textual descriptions.

:::image type="content" source="../../media/how-to/healthcare-ai/medimageparse-flow.gif" alt-text="Animation of data flow through MedImageParse model showing image coming through the model paired with a task adaptor and turning into a set of segmentation masks.":::

Remarkably, the segmentation masks and textual descriptions were achieved by using only standard segmentation datasets, augmented by natural-language labels, or descriptions harmonized with established biomedical object ontologies. This approach not only improved individual task performance but also offered an all-in-one tool for biomedical image analysis, paving the way for more efficient and accurate image-based biomedical discovery.

# [MedImageParse 3D](#tab/medimageparse-3d)

## MedImageParse 3D
Similar to the MedImageParse model, MedImageParse 3D uses a combination of a text prompt and a medical image to create a segmentation mask. However, unlike MedImageParse, the MedImageParse 3D model takes in an entire 3D volume—a common way of representing the imaged area for cross-sectional imaging modalities like CT or MRI—and generates the 3-dimensional segmentation mask.

---

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../../includes/hub-project-name.md)]](../create-projects.md?pivots=hub-project).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../../concepts/rbac-ai-foundry.md).

## Deploy the model to a managed compute

Deployment to a self-hosted managed inference solution allows you to customize and control all the details about how the model is served. You can deploy the model from its model card in the catalog UI of [Azure AI Foundry](https://aka.ms/healthcaremodelstudio) or [Azure Machine Learning studio](https://ml.azure.com/model/catalog) or [deploy it programmatically](../deploy-models-managed.md).

To __deploy the model through the UI__:

1. Go to the model catalog.
1. Search for the model and select its model card.
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

Consume the model as a REST API, using simple GET requests or by creating a client as follows:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

ml_client_workspace = MLClient.from_config(credential)
```

In the deployment configuration, you get to choose an authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see the [corresponding documentation page](../../../machine-learning/how-to-setup-authentication.md). Also, the client is created from a configuration file that is created automatically for Azure Machine Learning virtual machines (VMs). Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve segmentation masks.

# [MedImageParse](#tab/medimageparse)

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

# [MedImageParse 3D](#tab/medimageparse-3d)

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

---

## Reference for REST API

MedImageParse and MedImageParse 3D models assume a simple single-turn interaction where one request produces one response. 

### Request schema



Request payload is a JSON formatted string containing the following parameters:

# [MedImageParse](#tab/medimageparse)

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 256 | Count of inputs passed to the model. You're limited by how much data can be passed in a single POST request, which depends on the size of your images. Therefore, it's reasonable to keep this number in the dozens. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the image bytes encoded using base64 and decoded as utf-8 string. <br/>**NOTE**: The image should be resized to `1024x1024` pixels before submitting to the model, preserving the aspect ratio. Empty space should be padded with black pixels. See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) sample notebook for an example of resizing and padding code.<br/><br/> The input text is a string containing multiple sentences separated by the special character `&`. For example: `tumor core & enhancing tumor & non-enhancing tumor`. In this case, there are three sentences, so the output consists of three images with segmentation masks. |

# [MedImageParse 3D](#tab/medimageparse-3d)

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Yes    | An object containing the input data |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Yes    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Yes | 0 | This parameter is used when multiple inputs are passed to the endpoint in one call. This model's endpoint wrapper doesn't use this parameter, so it should be set to 0. |
| `data`   | `list[list[string]]` | Yes | Base64 image + text prompt | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the input volume in NIfTI format encoded using base64 and decoded as utf-8 string. The input text is a string containing the target (for example, organ) to be segmented. |

---

### Request example

# [MedImageParse](#tab/medimageparse)

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

# [MedImageParse 3D](#tab/medimageparse-3d)

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

---

### Response schema

# [MedImageParse](#tab/medimageparse)

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

# [MedImageParse 3D](#tab/medimageparse-3d)

The response is a list of objects. Each object contains the segmentation result for one input. The segmentation mask is encoded as a Base64 string inside a serialized JSON object under the key `nifti_file`.

| Key            | Type   | Description                                                                 |
| -------------- | ------ | --------------------------------------------------------------------------- |
| `nifti_file` | string | JSON-formatted string containing the base64-encoded NIfTI segmentation mask |


---

### Response example

# [MedImageParse](#tab/medimageparse)

**Response to a simple inference requesting segmentation of two objects** 

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

# [MedImageParse 3D](#tab/medimageparse-3d)


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

---

### Supported input formats

# [MedImageParse](#tab/medimageparse)

The deployed model API supports images encoded in PNG format. For optimal results, we recommend using uncompressed/lossless PNGs with RGB images.

As described in the API specification, the model only accepts images in the resolution of `1024x1024` pixels. Images need to be resized and padded (if they have a non-square aspect ratio).

See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) notebook for techniques and sample code useful for submitting images of various sizes stored using various biomedical imaging formats.

# [MedImageParse 3D](#tab/medimageparse-3d)

The deployed model API supports volumes encoded in NIfTI format.

---

## Learn more from samples
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

* [Deploying and Using MedImageParse](https://aka.ms/healthcare-ai-examples-mip-deploy): Learn how to deploy the MedImageParse model and integrate it into your workflow.
* [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples): Understand how to use MedImageParse to segment a wide variety of different medical images and learn some prompting techniques. 

## Related content

* [CXRReportGen for grounded report generation](deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)