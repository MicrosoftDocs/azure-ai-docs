---
title: How do Deploy CXRReportGen Healthcare AI Model with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use CXRReportGen Healthcare AI Model with Azure AI Studio.
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

# How to use CXRReportGen Healthcare AI Model for Generating Grounded Findings

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn how to deploy CXRReportGen as an online endpoint for real-time inference and issue a basic call to the API. The steps you take are:

* Deploy the model to a self-hosted managed compute.
* Grant permissions to the endpoint.
* Send test data to the model, receive and interpret results

## CXRReportGen - Grounded Report Generation Model for Chest X-rays
Radiology reporting demands detailed image understanding, integration of multiple inputs (including comparisons with prior imaging), and precise language generation, making it an ideal candidate for generative multimodal models. CXRReportGen not only performs the task of generating a list of findings from a chest Xray study, but also extends it by incorporating the localization of individual findings on the image—a task we refer to as grounded report generation. Grounding enhances the clarity of image interpretation and the transparency of AI-generated text, thereby improving the utility of automated report drafting. The model combines a radiology-specific image encoder with a large language model and it takes as inputs a more comprehensive set of data than many traditional approaches: the current frontal image, the current lateral image, the prior frontal image, the prior report, and the Indication, Technique, and Comparison sections of the current report. These additions significantly enhance report quality and reduce hallucinations, demonstrating the feasibility of grounded reporting as a novel and richer task in automated radiology.

## Prerequisites

To use CXRReportGen model with Azure AI Studio, you need the following prerequisites:

### A model deployment

**Deployment to a self-hosted managed compute**

CXRReportGen model can be deployed to our self-hosted managed inference solution, which allows you to customize and control all the details about how the model is served.

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

## Work with a Grounded Report Generation Model

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
CXRReportGen is a versatile model that can be applied to a wide range of tasks and imaging modalities. For more examples see the following interactive Python Notebooks: 


### Getting Started
* [Deploying and Using CXRReportGen](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/cxrreportgen/deploy.ipynb): learn how to deploy the CXRReportGen model and integrate it into your workflow.
* [Calling CXRReportGen and Visualizing Results](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/healthcare-ai/cxrreportgen/examples.ipynb): understand how to submit various types of Chest X-Ray studies to CXRReportGen, interpret the results and apply some visualization techniques. 

## Related content

* [MedImageParse for medical image segmentation](deploy-medimageparse.md)
* [MedImageInsight for grounded report generation](deploy-medimageinsight.md)
