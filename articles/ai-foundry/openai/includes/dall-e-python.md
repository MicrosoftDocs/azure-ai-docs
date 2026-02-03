---
title: 'Quickstart: Generate images with the Python SDK for Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to generate images with Azure OpenAI by using the Python SDK and the endpoint and access keys for your Azure OpenAI resource.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this guide to get started generating images with the Azure OpenAI SDK for Python.

[Library source code](https://github.com/openai/openai-python/tree/main/src/openai) | [Package](https://github.com/openai/openai-python) | [Samples](https://github.com/openai/openai-python/tree/main/examples)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- An Azure OpenAI resource created in a compatible region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability).
    - Access the Azure OpenAI resource endpoint and keys in the Azure portal.
- Then, you need to deploy a `dalle3` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Setup

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Microsoft Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| **Key** | `api_key` | The key value is also located under **Keys and Endpoint** for your resource in the Azure portal. Azure generates two keys for your resource. You can use either value. |

Go to your resource in the Azure portal. On the navigation pane, select **Keys and Endpoint** under **Resource Management**. Copy the **Endpoint** value and an access key value. You can use either the **KEY 1** or **KEY 2** value. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot that shows the Keys and Endpoint page for an Azure OpenAI resource in the Azure portal." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](environment-variables.md)]

## Install the Python SDK


Open a command prompt and browse to your project folder. Install the OpenAI Python SDK by using the following command:

```bash
pip install openai
```

Install the following libraries as well:
```bash
pip install requests
pip install pillow 
```

## Generate images with DALL-E

Create a new python file, _quickstart.py_. Open it in your preferred editor or IDE.

Replace the contents of _quickstart.py_ with the following code. 

```python
from openai import AzureOpenAI
import os
import requests
from PIL import Image
import json

client = AzureOpenAI(
    api_version="2024-02-01",  
    api_key=os.environ["AZURE_OPENAI_API_KEY"],  
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
)

result = client.images.generate(
    model="dalle3", # the name of your DALL-E 3 deployment
    prompt="a close-up of a bear walking through the forest",
    n=1
)

json_response = json.loads(result.model_dump_json())

# Set the directory for the stored image
image_dir = os.path.join(os.curdir, 'images')

# If the directory doesn't exist, create it
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Initialize the image path (note the filetype should be png)
image_path = os.path.join(image_dir, 'generated_image.png')

# Retrieve the generated image
image_url = json_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(image_url).content  # download the image
with open(image_path, "wb") as image_file:
    image_file.write(generated_image)

# Display the image in the default image viewer
image = Image.open(image_path)
image.show()
```

1. Make sure the `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` environment variables are set.
1. Change the value of `prompt` to your preferred text.
1. Change the value of `model` to the name of your deployed DALL-E 3 model.

> [!IMPORTANT]
> Remember to remove the key from your code when you're done, and never post your key publicly. For production, use a secure way of storing and accessing your credentials. For more information, see [Azure Key Vault](/azure/key-vault/general/overview).

Run the application with the `python` command:

```console
python quickstart.py
```

Wait a few moments to get the response.

## Output

Azure OpenAI stores the output image in the _generated_image.png_ file in your specified directory. The script also displays the image in your default image viewer.

The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../concepts/content-filter.md).

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* Try examples in the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
* See the [API reference](../reference.md#image-generation)
