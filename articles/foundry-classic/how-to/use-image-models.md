---
title: How to use image-to-text models in the model catalog
titleSuffix: Microsoft Foundry
description: Learn how to use image-to-text models from the Foundry model catalog.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 08/28/2025
ms.author: mopeakande
author: msakande
ms.reviewer: malpande
reviewer: mpande98
manager: nitinme
ms.custom: references_regions, tool_generated
---

# How to use image-to-text models in the model catalog

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

This article explains how to use _image-to-text_ models in the Foundry model catalog. 

Image-to-text models are designed to analyze images and generate descriptive text based on what they see. Think of them as a combination of a camera and a writer. You provide an image as an input to the model, and the model looks at the image and identifies different elements within it, like objects, people, scenes, and even text. Based on its analysis, the model then generates a written description of the image, summarizing what it sees.

Image-to-text models excel at various use cases such as accessibility features, content organization (tagging), creating product and educational visual descriptions, and digitizing content via Optical Character Recognition (OCR). One might say image-to-text models bridge the gap between visual content and written language, making information more accessible and easier to process in various contexts.

## Prerequisites

To use image models in your application, you need:
 
- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- A [Microsoft Foundry project](create-projects.md).

- An image model deployment on Foundry. 

  - This article uses a __Mistral OCR__ model deployment.

- The endpoint URL and key.

## Use image-to-text model

1. Authenticate using an API key. First, deploy the model to generate the endpoint URL and an API key to authenticate against the service. In this example, the endpoint and key are strings holding the endpoint URL and the API key. The API endpoint URL and API key can be found on the **Deployments + Endpoint** page once the model is deployed.

    If you're using Bash:
  
    ```bash    
    export AZURE_API_KEY="<your-api-key>"
    ```

    If you're in PowerShell:
  
    ```powershell
    $Env:AZURE_API_KEY = "<your-api-key>"
    ```
  
    If you're using Windows command prompt:
    
    ```
    set AZURE_API_KEY=<your-api-key>
    ```

1. Run a basic code sample. Different image models accept different data formats. In this example, _Mistral OCR 25.03_ supports only base64 encoded data; document url or image url isn't supported. Paste the following code into a shell.
  
    ```http
    curl --request POST \
      --url https://<your_serverless_endpoint>/v1/ocr \
      --header 'Authorization: Bearer <your-api-key>' \
      --header 'Content-Type: application/json' \
      --data '{
      "model": "mistral-ocr-2503",
      "document": {
        "type": "document_url",
        "document_name": "test",
        "document_url": "data:application/pdf;base64,JVBER... <replace with your base64 encoded image data>"
      }
    }'
    ```

## More code samples for Mistral OCR 25.03

To process PDF files:

```bash
# Read the pdf file
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

To process an image file:

```bash
# Read the image file
input_file_path="assets/receipt.png"
base64_value=$(base64 "$input_file_path")
input_base64_value="data:application/png;base64,${base64_value}"
# echo $input_base64_value
 
# Prepare JSON data
payload_body=$(cat <<EOF
{
    "model": "mistral-ocr-2503",
    "document": {
        "type": "image_url",
        "image_url": "$input_base64_value"
    },
    "include_image_base64": true
}
EOF
)
 
# Process the base64 data with ocr endpoint
echo "$payload_body" | curl ${AZURE_AI_CHAT_ENDPOINT}/v1/ocr \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AZURE_AI_CHAT_KEY}" \
  -d @- -o ocr_png_output.json
```

## Model-specific parameters

Some image-to-text models only support specific data formats. Mistral OCR 25.03, for example, requires `base64 encoded image data` for their `document_url` parameter. The following table lists the supported and unsupported data formats for image models in the model catalog.

| Model | Supported | Not supported |
| :---- | ----- | ----- |
| Mistral OCR 25.03 | base64 encoded image data  | document url, image url |



## Related content

- [How to use image generation models on Azure OpenAI](../openai/how-to/dall-e.md)

