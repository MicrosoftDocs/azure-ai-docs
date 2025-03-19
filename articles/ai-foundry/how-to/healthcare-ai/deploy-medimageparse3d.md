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
Similar to our [MedImageParse model](deploy-medimageparse.md) model, MedImageParse 3D uses a combination of a text prompt and medical image to create a segmentation mask. However, unlike MedImageParse, the MedImageParse 3D model takes in an entire 3D volume - which is a common way of representing the imaged area for cross-sectional imaging modalities like CT or MRI - and generates the 3-dimensional segmenatation mask. 

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
from azure.identity import DeviceCodeCredential

credential = DefaultAzureCredential()

ml_client_workspace = MLClient.from_config(credential)
```

In the deployment configuration, you get to choose authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see the [corresponding documentation page](../../../machine-learning/how-to-setup-authentication.md). Also, note that the client is created from a configuration file that is created automatically for Azure Machine Learning virtual machines (VMs). Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve segmentation masks.

TODO: the example here follows MedImageParse (2D) where it uses `ml_client_workspace.online_endpoints.invoke` instead of `urllib.request.urlopen` as in this [notebook](https://dev.azure.com/msazuredev/HLS%20AI%20Platform/_git/3dMedImageParseDeployment?path=/notebooks/03.model.endpoint.api.call.ipynb&version=GBmain&line=192&lineEnd=193&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents). Verify the correct call pattern.

```python
import base64
import json
import os

sample_image = "example.nii.gz"
with open(sample_image, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

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

## Use MedImageParse 3D REST API
TODO: verify all contents in this section

MedImageParse 3D model assumes a simple single-turn interaction where one request produces one response. 

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
| `data`   | `list[list[string]]` | Y | "" | The list contains the items passed to the model which is defined by the index parameter. Each item is a list of two strings. The order is defined by the `columns` parameter. The `text` string contains the prompt text. The `image` string is the input volume in NIfTI format encoded using base64 and decoded as utf-8 string. The input text is a string containing the target (e.g., organ) to be segmented. |

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
      ["iVBORw0KGgoAAAAN...",
      "pancreas"]
    ]
  }
}
```

### Response schema

Response payload is a list of JSON-formatted strings, each corresponding to a submitted volume. Each string contains a `segmentation_object` object.

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
The requested segmentation mask is stored in NIfTI, represented by an encoded string.

TODO: verify the value of nifti_file is a string or a json object (without the quote).
```JSON
[
  {
    "nifti_file": "{'data': 'H4sIAAAAAAAE...'}"
  }
]
```

TODO: In an [example notebook](https://dev.azure.com/msazuredev/HLS%20AI%20Platform/_git/3dMedImageParseDeployment?path=/notebooks/01.model.packaging.ipynb&version=GBmain&line=314&lineEnd=315&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents), `temp_file.flush()` and `os.unlink(temp_file.name)` are commented out. Are these lines needed?

The NIfTI file can be obtained by decoding the returned string using a code like
```python
def decode_base64_to_nifti(base64_string: str) -> nib.Nifti1Image:
    """
    Decode a Base64 string back to a NIfTI image.
    
    Args:
        base64_string (str): Base64 encoded string of NIfTI image
    
    Returns:
        nib.Nifti1Image: Decoded NIfTI image object
    """
    base64_string = json.loads(base64_string)["data"]
    # Decode Base64 string to bytes
    byte_data = base64.b64decode(base64_string)
    
    # Create a temporary file to load the NIfTI image
    with tempfile.NamedTemporaryFile(suffix='.nii.gz', delete=False) as temp_file:
        temp_file.write(byte_data)
        temp_file.flush()
        # Load NIfTI image from the temporary file
        nifti_image = nib.load(temp_file.name)
    
    # Remove temporary file
    os.unlink(temp_file.name)
    
    return nifti_image.get_fdata()
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
