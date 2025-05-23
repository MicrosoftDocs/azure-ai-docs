---
title: How to deploy and use CXRReportGen healthcare AI model with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to use CXRReportGen Healthcare AI Model with Azure AI Foundry.
ms.service: azure-ai-foundry
manager: scottpolly
ms.topic: how-to
ms.date: 04/24/2025
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
#Customer intent: As a Data Scientist I want to learn how to use the CXRReportGen healthcare AI model to generate grounded findings.

---

# How to use CXRReportGen Healthcare AI model to generate grounded findings

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy CXRReportGen as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive, and interpret results

## CXRReportGen - grounded report generation model for chest X-rays
Radiology reporting demands detailed image understanding, integration of multiple inputs (including comparisons with prior imaging), and precise language generation, making it an ideal candidate for generative multimodal models. CXRReportGen generates a list of findings from a chest X-ray study and also perform a _grounded report generation_ or _grounding_ task. That is, the CXRReportGen model also incorporates the localization of individual findings on the image. Grounding enhances the clarity of image interpretation and the transparency of AI-generated text, which end up improving the utility of automated report drafting.

The following animation demonstrates the conceptual architecture of the CXRReportGen model, which consists of an embedding model paired with a general reasoner large language model (LLM). 

:::image type="content" source="../../media/how-to/healthcare-ai/healthcare-reportgen.gif" alt-text="Animation of CXRReportGen architecture and data flow.":::

The CXRReportGen model combines a radiology-specific image encoder with a large language model and takes as inputs a more comprehensive set of data than many traditional approaches. The input data includes the current frontal image, the current lateral image, the prior frontal image, the prior report, and the indication, technique, and comparison sections of the current report. These additions significantly enhance report quality and reduce incorrect information, ultimately demonstrating the feasibility of grounded reporting as a novel and richer task in automated radiology.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](hub-project-name.md)]](../create-projects.md?pivots=hub-project).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../../concepts/rbac-ai-foundry.md).

## Deploy the model to a managed compute

Deployment to a self-hosted managed inference solution allows you to customize and control all the details about how the model is served. You can deploy the model from its model card in the catalog UI of [Azure AI Foundry](https://aka.ms/healthcaremodelstudio) or [Azure Machine Learning studio](https://ml.azure.com/model/catalog) or [deploy it programmatically](../deploy-models-managed.md).

To __deploy the model through the UI__:

1. Go to the model catalog.
1. Search for the _CxrReportGen_ model and select its model card.
1. On the model's overview page, select __Deploy__.
1. If given the option to choose between standard deployment and deployment using a managed compute, select **Managed Compute**.
1. Fill out the details in the deployment window.

    > [!NOTE]
    > For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**
1. Select __Deploy__.

To __deploy the model programmatically__, see [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md).


## Work with a grounded report generation model for chest X-ray analysis

In this section, you consume the model and make basic calls to it.

### Use REST API to consume the model

Consume the CXRReportGen report generation model as a REST API, using simple GET requests or by creating a client as follows:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

ml_client_workspace = MLClient.from_config(credential)
```

In the deployment configuration, you get to choose an authentication method. This example uses Azure Machine Learning token-based authentication. For more authentication options, see the [corresponding documentation page](../../../machine-learning/how-to-setup-authentication.md). Also, the client is created from a configuration file that is created automatically for Azure Machine Learning virtual machines (VMs). Learn more on the [corresponding API documentation page](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-from-config).

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve a list of findings and corresponding bounding boxes.

```python
input_data = {
        "frontal_image": base64.encodebytes(read_image(frontal_path)).decode("utf-8"),
        "lateral_image": base64.encodebytes(read_image(lateral_path)).decode("utf-8"),
        "indication": indication,
        "technique": technique,
        "comparison": comparison,
    }

    data = {
        "input_data": {
            "columns": list(input_data.keys()),
            #  IMPORANT: Modify the index as needed
            "index": [0],  # 1, 2],
            "data": [
                list(input_data.values()),
            ],
        }
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

## Use CXRReportGen REST API
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
| `index`   | `integer` | Y | 0 - 10 | Count of inputs passed to the model. You're limited by how much GPU RAM you have on the VM where CxrReportGen is hosted, and by how much data can be passed in a single POST request—which depends on the size of your images. Therefore, it's reasonable to keep this number under 10. Check model logs if you're getting errors when passing multiple inputs. |
| `data`   | `list[list[string]]` | Y | "" | The list contains the list of items passed to the model. The length of the list is defined by the index parameter. Each item is a list of several strings. The order and meaning are defined by the `columns` parameter. The text strings contain text. The image strings are the image bytes encoded using base64 and decoded as utf-8 string |


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

### Supported image formats

The deployed model API supports images encoded in PNG or JPEG formats. For optimal results, we recommend using uncompressed/lossless PNGs with 8-bit monochromatic images.

## Learn more from samples

CXRReportGen is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python notebook: 

* [Deploying and Using CXRReportGen](https://aka.ms/healthcare-ai-examples-cxr-deploy): Learn how to deploy the CXRReportGen model and integrate it into your workflow. This notebook also covers bounding-box parsing and visualization techniques.

## Related content

* [MedImageParse models for medical image segmentation](deploy-medimageparse.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)