---
title: How do Deploy MedImageParse Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use MedImageParse Healthcare AI Model with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: how-to
ms.date: 09/30/2024
ms.reviewer: kritifaujdar
reviewer: fkriti
ms.author: mopeakande
author: msakande
ms.custom: references_regions, generated
zone_pivot_groups: ?????
---

# How to use MedImageParse Healthcare AI Model for Generating Grounded Findings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn about the MedImageParse Foundational Model for Healthcare. 

## MedImageParse - Prompt-based Segmentation of Medical Images
* MedImageParse is a unique model for prompt-based segmentation
* See model catalog entry for model card  

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
MedImageParse is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following: 

* [Using MedImageParse and visualizing results](http://www.github.com)
* [Using MedImageParse to analyze various stains of digital pathology workflow](http://www.github.com)

## Related content

* [CXRReportGen for grounded report generation](../reference/reference-model-inference-api.md)
* [MedImageInsights for embeddings](deploy-models-serverless.md)
