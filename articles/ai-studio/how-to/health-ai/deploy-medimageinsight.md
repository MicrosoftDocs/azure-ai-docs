---
title: How do Deploy MedImageInsight Health AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use MedImageInsight Health AI Model with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande
zone_pivot_groups: ?????
---

# How to use MedImageInsight Health AI Model for Generating Image Embeddings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy MedImageInsight as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive and interpret results

## MedImageInsight - the Medical Imaging Embedding model
MedImageInsight Foundational Model for Health is a powerful model that can process a wide variety of medical images including X-Ray, CT, MRI, clinical photography, dermoscopy, histopathology, ultrasound, and mammography. Rigorous evaluations demonstrate MedImageInsight's ability to achieve state-of-the-art (SOTA) or human expert level performance across classification, image-image search, and fine-tuning tasks.  Specifically, on public datasets, MedImageInsight achieves or exceeds SOTA in chest X-ray disease classification and search, dermatology classification and search, OCT classification and search, 3D medical image retrieval, and near SOTA for histopathology classification and search.  

## Prerequisites

To use MedImageInsight models with Azure AI Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

MedImageInsight model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

For deployment to a self-hosted managed compute, you must have enough quota in your subscription. If you don't have enough quota available, you can use our temporary quota access by selecting the option **I want to use shared quota and I acknowledge that this endpoint will be deleted in 168 hours.**

> [!div class="nextstepaction"]
> [Deploy the model to managed compute](https://portal.azure.com)

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

## Work with an Embedding Model

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
MedImageInsight is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more specific examples of solving a variety of tasks with MedImageInsight see the following interactive Python Notebooks: 

### Getting Started
* [Deploying and Using MedImageInsight](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/deploy.ipynb): learn how to deploy the MedImageInsight model and integrate it into your workflow.

### Classification Techniques
* [Building a Zero-Shot Classifier](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/zero-shot.ipynb): discover how to create a classifier without the need training or large amount of labeled training data using MedImageInsight.

* [Enhancing Classification with Adapter Networks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/adapter.ipynb): improve classification performance by incorporating a small adapter network with MedImageInsight.

### Advanced Applications
* [Inferring MRI Acquisition Parameters from Pixel Data](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/exam-parameter.ipynb): understand how to extract MRI exam acquisition parameters directly from imaging data.

* [Detecting Outliers in Medical Image Series](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/medimageinsight/outlier.ipynb): learn methods to identify anomalies in full series of medical images using MedImageInsight.


## Related content

* [MedImageParse for medical image segmentation](./deploy-medimageparse)
* [CXRReportGen for grounded report generation](./deploy-cxrreportgen.md)
