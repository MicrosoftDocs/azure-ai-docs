---
title: 'Quickstart: Generate images with the REST APIs for Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to generate images with Azure OpenAI by using the REST APIs and the endpoint and access keys for your Azure OpenAI resource.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 02/20/2025
---

Use this guide to get started calling the Azure OpenAI in Microsoft Foundry Models image generation REST APIs by using Python.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- The following Python libraries installed: `os`, `requests`, `json`.
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability).
- Then, you need to deploy a `gpt-image-1`-series or `dalle3` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Setup 

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](environment-variables.md)]

## Create a new Python application

Create a new Python file named _quickstart.py_. Open the new file in your preferred editor or IDE.

#### [GPT-image-1 series](#tab/gpt-image-1)

1. Replace the contents of _quickstart.py_ with the following code. Change the value of `prompt` to your preferred text. Also set `deployment` to the deployment name you chose when you deployed the GPT-image-1 series model.
    
    ```python
    import os
    import requests
    import base64
    from PIL import Image
    from io import BytesIO
    
    # set environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
    
    deployment = "gpt-image-1.5" # the name of your GPT-image-1 series deployment
    api_version = "2025-04-01-preview" # or later version
    
    def decode_and_save_image(b64_data, output_filename):
      image = Image.open(BytesIO(base64.b64decode(b64_data)))
      image.show()
      image.save(output_filename)
    
    def save_all_images_from_response(response_data, filename_prefix):
      for idx, item in enumerate(response_data['data']):
        b64_img = item['b64_json']
        filename = f"{filename_prefix}_{idx+1}.png"
        decode_and_save_image(b64_img, filename)
        print(f"Image saved to: '{filename}'")
    
    base_path = f'openai/deployments/{deployment}/images'
    params = f'?api-version={api_version}'
    
    generation_url = f"{endpoint}{base_path}/generations{params}"
    generation_body = {
      "prompt": "girl falling asleep",
      "n": 1,
      "size": "1024x1024",
      "quality": "medium",
      "output_format": "png"
    }
    generation_response = requests.post(
      generation_url,
      headers={
        'Api-Key': subscription_key,
        'Content-Type': 'application/json',
      },
      json=generation_body
    ).json()
    save_all_images_from_response(generation_response, "generated_image")
    
    # In addition to generating images, you can edit them.
    edit_url = f"{endpoint}{base_path}/edits{params}"
    edit_body = {
      "prompt": "girl falling asleep",
      "n": 1,
      "size": "1024x1024",
      "quality": "medium"
    }
    files = {
      "image": ("generated_image_1.png", open("generated_image_1.png", "rb"), "image/png"),
      # You can use a mask to specify which parts of the image you want to edit.
      # The mask must be the same size as the input image.
      # "mask": ("mask.png", open("mask.png", "rb"), "image/png"),
    }
    edit_response = requests.post(
      edit_url,
      headers={'Api-Key': subscription_key},
      data=edit_body,
      files=files
    ).json()
    save_all_images_from_response(edit_response, "edited_image")
    ```

    The script makes a synchronous image generation API call.

    > [!IMPORTANT]
    > Remember to remove the key from your code when you're done, and never post your key publicly. For production, use a secure way of storing and accessing your credentials. For more information, see [Azure Key Vault](/azure/key-vault/general/overview).

1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ```

    Wait a few moments to get the response.

<!--
#### [Black Forest Labs](#tab/bfl)
tbd
-->

#### [DALL-E](#tab/dall-e-3)


1. Replace the contents of _quickstart.py_ with the following code. Change the value of `prompt` to your preferred text.

    You also need to replace `<dalle3>` in the URL with the deployment name you chose when you deployed the DALL-E 3 model. Entering the model name will result in an error unless you chose a deployment name that is identical to the underlying model name. If you encounter an error, double check to make sure that you don't have a doubling of the `/` at the separation between your endpoint and `/openai/deployments`.
    
    ```python
    import requests
    import time
    import os
    api_base = os.environ['AZURE_OPENAI_ENDPOINT']  # Enter your endpoint here
    api_key = os.environ['AZURE_OPENAI_API_KEY']         # Enter your API key here

    api_version = '2024-02-01'
    url = f"{api_base}/openai/deployments/<dalle3>/images/generations?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
        # Enter your prompt text here
        "prompt": "A multi-colored umbrella on the beach, disposable camera",
        "size": "1024x1024", # supported values are “1792x1024”, “1024x1024” and “1024x1792” 
        "n": 1, #The number of images to generate. Only n=1 is supported for DALL-E 3.
        "quality": "hd", # Options are “hd” and “standard”; defaults to standard 
        "style": "vivid" # Options are “natural” and “vivid”; defaults to “vivid”
    }
    submission = requests.post(url, headers=headers, json=body)
    
    image_url = submission.json()['data'][0]['url']
    
    print(image_url)
    ```

    The script makes a synchronous image generation API call.

    > [!IMPORTANT]
    > Remember to remove the key from your code when you're done, and never post your key publicly. For production, use a secure way of storing and accessing your credentials. For more information, see [Azure Key Vault](/azure/key-vault/general/overview).

1. Run the application with the `python` command:

    ```console
    python quickstart.py
    ```

    Wait a few moments to get the response.

---

## Output

The output from a successful image generation API call looks like the following example. The `url` field contains a URL where you can download the generated image. The URL stays active for 24 hours.

```json
{ 
    "created": 1698116662, 
    "data": [ 
        { 
            "url": "<URL_to_generated_image>",
            "revised_prompt": "<prompt_that_was_used>" 
        }
    ]
} 
```

A successful response includes:
- A `created` timestamp (Unix epoch time)
- A `data` array with at least one image object
- Either a `url` (temporary link valid for 24 hours) or `b64_json` (base64-encoded image data)

### Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `DeploymentNotFound` | The deployment name doesn't exist or is misspelled | Verify the deployment name in the Azure portal or Foundry portal |
| `401 Unauthorized` | Invalid or missing API key | Check that your `AZURE_OPENAI_API_KEY` environment variable is set correctly |
| `429 Too Many Requests` | Rate limit exceeded | Implement retry logic with exponential backoff |
| `content_policy_violation` | Prompt or generated output blocked by content filter | Modify the prompt to comply with the content policy |
| `InvalidPayload` | Missing required parameters or invalid values | Check that `prompt`, `size`, and `n` are correctly specified |

The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../concepts/content-filter.md). For examples of error responses, see the [Image generation how-to guide](../how-to/dall-e.md).

The system returns an operation status of `Failed` and the `error.code` value in the message is set to `contentFilter`. Here's an example:

```json
{
    "created": 1698435368,
    "error":
    {
        "code": "contentFilter",
        "message": "Your task failed as a result of our safety system."
    }
}
```

It's also possible that the generated image itself is filtered. In this case, the error message is set to `Generated image was filtered as a result of our safety system.`. Here's an example:


```json
{
    "created": 1698435368,
    "error":
    {
        "code": "contentFilter",
        "message": "Generated image was filtered as a result of our safety system."
    }
}
```

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* Try examples in the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
* See the [API reference](../reference.md#image-generation)
