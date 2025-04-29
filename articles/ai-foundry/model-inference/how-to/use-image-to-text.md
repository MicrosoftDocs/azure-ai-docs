---
title: How to use image models with Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to generate images with image models with Azure AI model inference
manager: scottpolly
author: msakande
reviewer: Frogglew
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 04/29/2025
ms.author: mopeakande
ms.reviewer: saoh
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

# How to generate images with Azure AI model inference

This article explains how to generate images with _image_ models deployed to Azure AI model inference in Azure AI services. Some models have unique parameters or data format requirements.

## Prerequisites

To use image models in your application, you need:

[!INCLUDE [how-to-prerequisites](../includes/how-to-prerequisites.md)]

* An image model deployment. If you don't have one, see [Add and configure models to Azure AI model inference](create-model-deployments.md) to add an image model to your resource. This article uses the Mistral OCR model.

## Use image model

1. Authenticate using API key. For serverless API endpoints, deploy the model to generate the endpoint URL and an API key to authenticate against the service. In this example, the endpoint and key are strings holding the endpoint URL and the API key. The API endpoint URL and API key can be found on the **Deployments + Endpoint** page once the model is deployed.

    If you're using bash:
  
    ```
    export AZURE_API_KEY = "<your-api-key>"
    ```
  
    If you're in powershell:
  
    ```
    $Env:AZURE_API_KEY = "<your-api-key>"
    ```
  
    If you're using Windows command prompt:
    
    ```
    export AZURE_API_KEY = "<your-api-key>"
    ```

1. Run a basic code sample. Different image models accept different data formats. In this example, `Mistral OCR 25.03` supports only base64 data; document url or image url isn't supported. Paste the following code into a shell.
  
    ```http
    curl --request POST \
      --url https://<your_serverless_endpoint>/v1/ocr \
      --header 'Authorization: <api_key>' \
      --header 'Content-Type: Application/json' \
      --data '{
      "model": "mistral-ocr-2503",
      "document": {
        "type": "document_url",
        "document_name": "test",
        "document_url": "data:application/pdf;base64,JVBER..."
      }
    }'
    ```

## Model specific requirements

Some models only support specific data format. The following table list the supported and unsupported data formats for models.

| Model | Supported | Not supported |
| :---- | ----- | ----- |
| Mistral OCR 25.03 | base64 only  | document url or image url |
| dall-e-3 | Must be one of url or b64_json | base64 |
| gpt-image-1 | base64 only | document url or image url  |


## Related content

* [Use embeddings models](use-embeddings.md)
* [Azure AI Model Inference API](.././reference/reference-model-inference-api.md)