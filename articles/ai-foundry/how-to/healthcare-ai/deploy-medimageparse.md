---
title: "MedImageParse: Medical Image Segmentation Models"
titleSuffix: Microsoft Foundry
description: Learn how to use MedImageParse and MedImageParse 3D healthcare AI models for medical image segmentation with Microsoft Foundry.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/26/2026
ms.custom: dev-focus
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
manager: nitinme
author: msakande
ai-usage: ai-assisted
#Customer intent: As a Data Scientist I want to learn how to use the MedImageParse and MedImageParse 3D healthcare AI models to segment medical images.

---

# How to use MedImageParse healthcare AI models for segmentation of medical images

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

MedImageParse and MedImageParse 3D are healthcare AI models for medical image segmentation using simple text prompts. In this article, you learn how to deploy these prompt-based segmentation models as online endpoints for real-time inference and issue basic calls to the API. The steps you take are:

1. Deploy the model to a self-hosted managed compute.
1. Grant permissions to the endpoint.
1. Send test data to the model, receive results, and interpret them.


# [MedImageParse](#tab/medimageparse)

## MedImageParse

MedImageParse unifies segmentation, detection, and recognition tasks through image parsing. You can segment medical images by using simple text prompts without manually specifying bounding boxes.

# [MedImageParse 3D](#tab/medimageparse-3d)

## MedImageParse 3D

MedImageParse 3D processes entire 3D medical volumes (such as CT or MRI scans) and generates three-dimensional segmentation masks using text prompts.

---

To learn more about these models, see [Learn more about the models](#learn-more-about-the-models).

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, [create a paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../../includes/hub-project-name.md)]](../hub-create-projects.md)

- Azure role-based access controls (Azure RBAC) grant access to operations in Microsoft Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. Deploying models and invoking endpoints requires this role. For more information, see [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).

- Python 3.8 or later.

- Install the required Python packages:
  ```bash
  pip install azure-ai-ml azure-identity
  ```

- For MedImageParse, images must be resized to `1024x1024` pixels while preserving aspect ratio. Pad non-square images with black pixels. See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) notebook for preprocessing code examples.

## Sample notebooks

For complete working examples, see these interactive Python notebooks:

* [Deploying and Using MedImageParse](https://aka.ms/healthcare-ai-examples-mip-deploy): Learn how to deploy the MedImageParse model and integrate it into your workflow.
* [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples): Learn how to use MedImageParse to segment different medical images and learn prompting techniques.

## Deploy the model to a managed compute

Deployment to a self-hosted managed inference solution lets you customize and control all the details about how the model's served. The deployment process creates an online endpoint with a unique scoring URI and authentication keys. This endpoint lets you send inference requests to your model. You configure the compute resources (such as GPU-enabled VMs) and set deployment parameters like instance count and request timeout values.

To deploy the model programmatically or from its model card in Microsoft Foundry, see [How to deploy and infer with a managed compute deployment](../deploy-models-managed.md). After deployment completes, note your endpoint name and deployment name for use in the inference code.

## Send inference requests to the segmentation model

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

After you deploy the model, use the following code to send data and retrieve segmentation masks.

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

The response contains base64-encoded segmentation masks as NumPy arrays. See the [Response example](#response-example) section for details on decoding and interpreting the results.

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
# Find these values in Foundry portal under Deployments > [your deployment] > Details
url = "<your-endpoint-url>"
api_key = "<your-api-key>"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
}

req = urllib.request.Request(url, body, headers)

# Ensure that helper functions decode_base64_to_nifti() and plot_segmentation_masks() are defined as shown in the [Response example](#response-example) sub-section of the "Reference for REST API" section in the later part of this article.
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

The response contains a base64-encoded NIfTI segmentation mask. The helper functions `decode_base64_to_nifti()` and `plot_segmentation_masks()` shown in the [Response example](#response-example) section decode and visualize the 3D segmentation results.

---

## Reference for REST API

MedImageParse and MedImageParse 3D models assume a simple single-turn interaction where one request produces one response. 

### Request schema

The request payload is a JSON-formatted string containing the following parameters:

# [MedImageParse](#tab/medimageparse)

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Y    | An object containing the input data payload |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Y    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Y | 0 - 256 | Count of inputs passed to the model. You're limited by how much data you can pass in a single POST request, which depends on the size of your images. Therefore, it's reasonable to keep this number in the dozens. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the items you pass to the model, which the `index` parameter defines. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the image bytes encoded by using base64 and decoded as a utf-8 string. <br/>**NOTE**: You should resize the image to `1024x1024` pixels before submitting it to the model, preserving the aspect ratio. Empty space should be padded with black pixels. See the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) sample notebook for an example of resizing and padding code.<br/><br/> The input text is a string containing multiple sentences separated by the special character `&`. For example: `tumor core & enhancing tumor & non-enhancing tumor`. In this case, there are three sentences, so the output consists of three images with segmentation masks. |

# [MedImageParse 3D](#tab/medimageparse-3d)

| Key           | Type           | Required/Default | Description |
| ------------- | -------------- | :-----------------:| ----------------- |
| `input_data`       | `[object]`       | Yes    | An object containing the input data |

The `input_data` object contains the following fields:

| Key           | Type           | Required/Default | Allowed values    | Description |
| ------------- | -------------- | :-----------------:| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `columns`       | `list[string]`       | Yes    |  `"image"`, `"text"` | An object containing the strings mapping data to inputs passed to the model.|
| `index`   | `integer` | Yes | 0 | Use this parameter when you pass multiple inputs to the endpoint in one call. This model's endpoint wrapper doesn't use this parameter, so set it to 0. |
| `data`   | `list[list[string]]` | Yes | Base64 image + text prompt | The list contains the items you pass to the model, defined by the `index` parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the input volume in NIfTI format encoded using base64 and decoded as utf-8 string. The input text is a string containing the target (for example, organ) to be segmented. |

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

The response payload is a list of JSON-formatted strings, each corresponding to a submitted image. Each string contains a `segmentation_object`.

The `segmentation_object` contains the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image_features`       | `segmentation_mask` | An object representing the segmentation masks for a given image |
| `text_features`       | `list[string]` |  List of strings, one per each submitted text string, classifying the segmentation masks into one of 16 biomedical segmentation categories each: `liver`, `lung`, `kidney`, `pancreas`, `heart anatomies`, `brain anatomies`, `eye anatomies`, `vessel`, `other organ`, `tumor`, `infection`, `other lesion`, `fluid disturbance`, `other abnormality`, `histology structure`, `other` |

The `segmentation_mask` contains the following fields:

| Key           | Type           |  Description |
| ------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `data`       | `string` | A base64-encoded NumPy array containing the one-hot encoded segmentation mask. The array can include multiple instances of objects. Use `np.frombuffer` to deserialize after decoding. The array contains a three-dimensional matrix. The array's size is `1024x1024` (matching the input image dimensions), with the third dimension representing the number of input sentences provides. See the provided [sample notebooks](#sample-notebooks) for decoding and usage examples. |
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

The deployed model API supports images encoded in PNG format. For optimal results, we recommend using uncompressed or lossless PNGs with RGB images.

As described in the API specification, the model only accepts images in the resolution of `1024x1024` pixels. You need to resize and pad images if they have a non-square aspect ratio.

For techniques and sample code useful for submitting images of various sizes stored using various biomedical imaging formats, see the [Generating Segmentation for a Variety of Imaging Modalities](https://aka.ms/healthcare-ai-examples-mip-examples) notebook.

# [MedImageParse 3D](#tab/medimageparse-3d)

The deployed model API supports volumes encoded in NIfTI format.

---

## Learn more about the models

# [MedImageParse](#tab/medimageparse)

Biomedical image analysis is crucial for discovery in fields like cell biology, pathology, and radiology. Traditionally, tasks such as segmentation, detection, and recognition of relevant objects are addressed separately, which can limit the overall effectiveness of image analysis. However, MedImageParse unifies these tasks through image parsing by jointly conducting segmentation, detection, and recognition across numerous object types and imaging modalities. By using the interdependencies among these subtasks—such as the semantic labels of segmented objects—the model enhances accuracy and enables novel applications. For example, it lets users segment all relevant objects in an image by using a simple text prompt. This approach eliminates the need to manually specify bounding boxes for each object.

The following image shows the conceptual architecture of the MedImageParse model where an image embedding model is augmented with a task adaptation layer to produce segmentation masks and textual descriptions.

:::image type="content" source="../../media/how-to/healthcare-ai/medimageparse-flow.gif" alt-text="Screenshot of an animated diagram showing a medical image entering the MedImageParse model, flowing through a task adaptation layer, and outputting multiple segmentation masks with corresponding text labels.":::

The segmentation masks and textual descriptions are achieved by using only standard segmentation datasets, augmented by natural-language labels, or descriptions harmonized with established biomedical object ontologies. This approach improves individual task performance and offers an all-in-one tool for biomedical image analysis, paving the way for more efficient and accurate image-based biomedical discovery.

# [MedImageParse 3D](#tab/medimageparse-3d)

Similar to the MedImageParse model, MedImageParse 3D uses a combination of a text prompt and a medical image to create a segmentation mask. However, unlike MedImageParse, MedImageParse 3D takes in an entire 3D volume—a common way of representing the imaged area for cross-sectional imaging modalities like CT or MRI—and generates the three-dimensional segmentation mask.

--- 

## Related content

* [CXRReportGen for grounded report generation](deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
