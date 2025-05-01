---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images with the Azure OpenAI REST API'
titleSuffix: Azure OpenAI
description: Get started using the Azure OpenAI REST APIs to deploy and use the GPT-4 Turbo with Vision model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions
ms.date: 11/02/2023
---

Use this article to get started using the Azure OpenAI REST APIs to deploy and use the GPT-4 Turbo with Vision model. 

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- The following Python libraries: `requests`, `json`.
- An Azure OpenAI Service resource with a GPT-4 Turbo with Vision model deployed. See [GPT-4 and GPT-4 Turbo Preview model availability](../concepts/models.md#gpt-4-and-gpt-4-turbo-model-availability) for available regions. For more information about resource creation, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).

> [!NOTE]
> It is currently not supported to turn off content filtering for the GPT-4 Turbo with Vision model.

## Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="../media/quickstarts/endpoint.png":::

## Create a new Python application

Create a new Python file named _quickstart.py_. Open the new file in your preferred editor or IDE.


1. Replace the contents of _quickstart.py_ with the following code. 
    
    ```python
    # Packages required:
    import requests 
    import json 
    
    api_base = '<your_azure_openai_endpoint>' 
    deployment_name = '<your_deployment_name>'
    API_KEY = '<your_azure_openai_key>'
    
    base_url = f"{api_base}openai/deployments/{deployment_name}" 
    headers = {   
        "Content-Type": "application/json",   
        "api-key": API_KEY 
    } 
    
    # Prepare endpoint, headers, and request body 
    endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview" 
    data = { 
        "messages": [ 
            { "role": "system", "content": "You are a helpful assistant." }, 
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture:" 
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": "<image URL>"
                    }
                }
            ] } 
        ], 
        "max_tokens": 2000 
    }   
    
    # Make the API call   
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))   
    
    print(f"Status Code: {response.status_code}")   
    print(response.text)
    ```

1. Make the following changes:
    1. Enter your endpoint URL and key in the appropriate fields.
    1. Enter your GPT-4 Turbo with Vision deployment name in the appropriate field. 
    1. Change the value of the `"image"` field to the URL of your image.
        > [!TIP]
        > You can also use a base 64 encoded image data instead of a URL. For more information, see the [GPT-4 Turbo with Vision how-to guide](../how-to/gpt-with-vision.md#use-a-local-image).
1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ```


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)


