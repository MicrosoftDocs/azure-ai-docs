---
title: "How to Use Image Generation Models from OpenAI (classic)"
description: "Learn how to generate and edit images using Azure OpenAI image generation models. Discover configuration options and start creating images today. (classic)"
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 11/21/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom:
  - classic-and-new
  - build-2025
# Customer intent: as an engineer or hobbyist, I want to know how to use image generation models to their full capability.
zone_pivot_groups: openai-quickstart-dall-e
ai-usage: ai-assisted

ROBOTS: NOINDEX, NOFOLLOW
---

# Azure OpenAI image generation models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/dall-e.md)

[!INCLUDE [dall-e 1](../../../foundry/openai/includes/how-to-dall-e-1.md)]

## Call the image generation API

The following command shows the most basic way to use an image model with code. If this is your first time using these models programmatically, start with the [quickstart](/azure/ai-foundry/openai/dall-e-quickstart).

> [!TIP]
> Image generation typically takes 10-30 seconds depending on the model, size, and quality settings.

### Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability).
- Deploy a `gpt-image-1`-series model with your Azure OpenAI resource. For more information on deployments, see [Create a resource and deploy a model with Azure OpenAI](/azure/ai-foundry/openai/how-to/create-resource).
    - GPT-image-1 series models are available in limited access: [Apply for GPT-image-1 access](https://aka.ms/oai/gptimage1access); [Apply for GPT-image-1.5 access](https://aka.ms/oai/gptimage1.5access).
- Python 3.8 or later.
    - Install the required packages: `pip install openai azure-identity`

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/generations?api-version=<api_version>
```

**URL**:

Replace the following values:

- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your GPT-image-1 series model deployment.
- `<api_version>` is the version of the API you want to use. For example, `2025-04-01-preview`.

**Required headers**:

- `Content-Type`: `application/json`
- `api-key`: `<your_API_key>`

**Body**:

The following is a sample request body. You specify a number of options, defined in later sections.

```json
{
    "prompt": "A multi-colored umbrella on the beach, disposable camera",
    "model": "gpt-image-1.5",
    "size": "1024x1024", 
    "n": 1,
    "quality": "high"
}
```

> [!TIP]
> For image generation token costs, see [Image tokens](../../foundry-models/concepts/models-sold-directly-by-azure.md).

### Output

The response from a successful image generation API call looks like the following example. The `b64_json` field contains the output image data.

```json
{ 
    "created": 1698116662, 
    "data": [ 
        { 
            "b64_json": "<base64 image data>"
        }
    ]
} 
```

### Streaming

Streaming lets you receive partial images as they're generated, providing faster visual feedback for your users. This is useful for applications where you want to show generation progress. The `partial_images` parameter (1-3) controls how many intermediate images are returned before the final result.

You can stream image generation requests to `gpt-image-1`-series models by setting the `stream` parameter to `true`, and setting the `partial_images` parameter to a value between 0 and 3.

```python
import base64
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://RESOURCE-NAME-HERE/openai/v1/",  
  api_key=token_provider,
  default_headers={"api_version":"preview"}
)

stream = client.images.generate(
    model="gpt-image-1.5",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024",
    stream=True,
    partial_images = 2
)

for event in stream:
    if event.type == "image_generation.partial_image":
        idx = event.partial_image_index
        image_base64 = event.b64_json
        image_bytes = base64.b64decode(image_base64)
        with open(f"river{idx}.png", "wb") as f:
            f.write(image_bytes)
 
```

### Specify API options

The following API body parameters are available for image generation models.

#### [GPT-image-1 series](#tab/gpt-image-1)

#### Size

Specify the size of the generated images. Must be one of `1024x1024`, `1024x1536`, or `1536x1024` for GPT-image-1 series models. Square images are faster to generate.

#### Quality

There are three options for image quality: `low`, `medium`, and `high`. Lower quality images can be generated faster.

The default value is `high`.

#### Number

You can generate between one and 10 images in a single API call. The default value is `1`.

#### User ID

Use the *user* parameter to specify a unique identifier for the user making the request. This identifier is useful for tracking and monitoring usage patterns. The value can be any string, such as a user ID or email address.

#### Output format

Use the *output_format* parameter to specify the format of the generated image. Supported formats are `PNG` and `JPEG`. The default is `PNG`.

> [!NOTE]
> WEBP images aren't supported in the Azure OpenAI in Microsoft Foundry Models.

#### Compression

Use the *output_compression* parameter to specify the compression level for the generated image. Input an integer between `0` and `100`, where `0` is no compression and `100` is maximum compression. The default is `100`.

#### Streaming 

Use the *stream* parameter to enable streaming responses. When set to `true`, the API returns partial images as they're generated. This feature provides faster visual feedback for users and improves perceived latency. Set the *partial_images* parameter to control how many partial images are generated (1-3).

#### Transparency

Set the *background* parameter to `transparent` and *output_format* to `PNG` on an image generate request to get an image with a transparent background.

[!INCLUDE [dall-e 2](../../../foundry/openai/includes/how-to-dall-e-2.md)]

## Related content

* [What is Azure OpenAI?](../../foundry-models/concepts/models-sold-directly-by-azure.md)
* [Image API reference](/azure/ai-foundry/openai/reference#image-generation)
* [Image API (preview) reference](/azure/ai-foundry/openai/reference-preview)
- Learn about [image generation tokens](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#image-generation-models)

<!-- OAI HT guide https://platform.openai.com/docs/guides/images/usage -->
