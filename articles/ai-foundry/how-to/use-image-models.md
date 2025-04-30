---
title: How to use image models in the model catalog
titleSuffix: Azure AI Foundry
description: Learn how to use image models from the AI Foundry model catalog.
manager: scottpolly
author: msakande
reviewer: frogglew
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 04/30/2025
ms.author: mopeakande
ms.reviewer: frogglew
ms.custom: references_regions, tool_generated
---

# How to use image models in the model catalog

This article explains how to use _image_ models in the AI Foundry model catalog. Some models have unique parameters or data format requirements.

## Prerequisites

To use image models in your application, you need:
 
- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry project](create-projects.md).

- An image model deployment on Azure AI Foundry. 

  - This article uses a __Mistral OCR__ model deployment.

- The endpoint URL and key.

## Use image model

1. Authenticate using an API key. First, deploy the model to generate the endpoint URL and an API key to authenticate against the service. In this example, the endpoint and key are strings holding the endpoint URL and the API key. The API endpoint URL and API key can be found on the **Deployments + Endpoint** page once the model is deployed.

    If you're using Bash:
  
    ```bash    
    export AZURE_API_KEY = "<your-api-key>"
    ```

    If you're in PowerShell:
  
    ```powershell
    $Env:AZURE_API_KEY = "<your-api-key>"
    ```
  
    If you're using Windows command prompt:
    
    ```
    export AZURE_API_KEY = "<your-api-key>"
    ```

1. Run a basic code sample. Different image models accept different data formats. In this example, _Mistral OCR 25.03_ supports only base64 encoded data; document url or image url isn't supported. Paste the following code into a shell.
  
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

**More code samples for Mistral OCR 25.03**

```bash
input_file_path="assets/2201.04234v3.pdf"
base64_value=$(base64 "$input_file_path")
input_base64_value="data:application/pdf;base64,${base64_value}"
# echo $input_base64_value
 
# Prepare JSON data
payload_body=$(cat <<EOF
{
    "model": "mistral-ocr-2503",
    "document": {
        "type": "document_url",
        "document_url": "$input_base64_value"
    },
    "include_image_base64": true
}
EOF
)

echo "$payload_body" | curl ${AZURE_AI_CHAT_ENDPOINT}/v1/ocr \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AZURE_AI_CHAT_KEY}" \
  -d @- -o ocr_pdf_output.json
```


## Model-specific parameters

Some image models only support specific data formats. Mistral OCR 25.03, for example, requires `base64 encoded image data` for their `document_url` parameter. The following table lists the supported and unsupported data formats for image models in the model catalog.

| Model | Supported | Not supported |
| :---- | ----- | ----- |
| Mistral OCR 25.03 | base64 encoded image data  | document url, image url |
| dall-e-3 | document url, image url, b64_json | base64 encoded image data |
| gpt-image-1 | base64 encoded image data, image url | document url  |


## Related content

- [How to use image generation models on Azure OpenAI](../../ai-services/openai/how-to/dall-e.md)

