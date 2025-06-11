---
title: 'Quickstart: Generate images with the Python SDK for Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to generate images with Azure OpenAI by using the Python SDK and the endpoint and access keys for your Azure OpenAI resource.
manager: nitinme
ms.service: azure-ai-openai
ms.custom:
  - ignite-2023
ms.topic: include
ms.date: 11/06/2023
---

Use this guide to get started generating images with the Azure OpenAI SDK for Python.

[Library source code](https://github.com/openai/openai-python/tree/main/src/openai) | [Package](https://github.com/openai/openai-python) | [Samples](https://github.com/openai/openai-python/tree/main/examples)

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>.
- An Azure OpenAI resource created in a compatible region. See [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).
- Then, you need to deploy a `gpt-image-1` model or `dalle3` model with your Azure resource. For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

## Setup

### Retrieve key and endpoint

To successfully call the Azure OpenAI APIs, you need the following information about your Azure OpenAI resource:

| Variable | Name | Value |
|---|---|---|
| **Endpoint** | `api_base` | The endpoint value is located under **Keys and Endpoint** for your resource in the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
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

## Generate images

Create a new python file, _quickstart.py_. Open it in your preferred editor or IDE.

#### [GPT-image-1](#tab/gpt-image-1)

Replace the contents of _quickstart.py_ with the following code. 

```python
import os
import requests
import base64
from PIL import Image
from io import BytesIO

# You will need to set these environment variables or edit the following values.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

deployment = "gpt-image-1" # the name of your GPT-image-1 deployment
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

1. Change the value of `prompt` to your preferred text.
1. Change the value of `deployment` to the name of your deployed GPT-image-1 model.

#### [DALL-E](#tab/dall-e-3)

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
    prompt="a close-up of a bear walking throughthe forest",
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

1. Change the value of `prompt` to your preferred text.
1. Change the value of `model` to the name of your deployed DALL-E 3 model.

---

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

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* Try examples in the [Azure OpenAI Samples GitHub repository](https://github.com/Azure/openai-samples).
* See the [API reference](../reference.md#image-generation)
