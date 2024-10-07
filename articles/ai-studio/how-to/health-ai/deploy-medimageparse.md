---
title: How do Deploy MedImageParse Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use MedImageParse Healthcare AI Model with Azure AI Studio.
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

To use MedImageParse model with Azure AI Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageParse model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](../concepts/deployments-overview.md)

### The inference package installed

You can consume predictions from this model by using the `azure-ai-inference` package with Python. To install this package, you need the following prerequisites:

* Python 3.8 or later installed, including pip.
* The endpoint URL. To construct the client library, you need to pass in the endpoint URL. The endpoint URL has the form `https://your-host-name.your-azure-region.inference.ai.azure.com`, where `your-host-name` is your unique model deployment host name and `your-azure-region` is the Azure region where the model is deployed (for example, eastus2).
* Depending on your model deployment and authentication preference, you need either a key to authenticate against the service, or Microsoft Entra ID credentials. The key is a 32-character string.
  
Once you have these prerequisites, install the Azure AI inference package with the following command:

```bash
pip install azure-ai-inference
```

Read more about the [Azure AI inference package and reference](https://aka.ms/azsdk/azure-ai-inference/python/reference).

## Work with a Prompted Segmentation Model

### Create a client to consume the model

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```python
import os
from azure.core.credentials import AzureKeyCredential

client = TBD(
    endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
)
```

### Make basic calls to the model

Once the model is deployed, use the following code to send data and retrieve embeddings.

```python
print("SAMPLE CODE HERE")
```


## More Examples 
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using MedImageParse](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/deploy.ipynb): learn how to deploy the MedImageParse model and integrate it into your workflow.
* [Generating Segmentation for a Variety of Imaging Modalities](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageparse/call-examples.ipynb): understand how to use MedImageParse to segment a wide variety of different medical images and learn some prompting techniques. 

## Related content

* [CXRReportGen for grounded report generation](./deploy-cxrreportgen.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
