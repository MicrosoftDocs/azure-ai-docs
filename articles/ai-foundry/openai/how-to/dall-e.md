---
title: How to Use Image Generation Models from OpenAI
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Learn how to generate and edit images using Azure OpenAI image generation models. Discover configuration options and start creating images today.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 09/02/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom:
  - build-2025
# Customer intent: as an engineer or hobbyist, I want to know how to use DALL-E image generation models to their full capability.
---

# How to use Azure OpenAI image generation models

OpenAI's image generation models create images from user-provided text prompts and optional images. This article explains how to use these models, configure options, and benefit from advanced image generation capabilities in Azure.


## Prerequisites


- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=ai-services).
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability).
- Deploy a `dall-e-3` or `gpt-image-1` model with your Azure OpenAI resource. For more information on deployments, see [Create a resource and deploy a model with Azure OpenAI](/azure/ai-foundry/openai/how-to/create-resource).
    - GPT-image-1 is the newer model and features a number of improvements over DALL-E 3. It's available in limited access: apply for access with [this form](https://aka.ms/oai/gptimage1access).


## Call the image generation API


The following command shows the most basic way to use an image model with code. If this is your first time using these models programmatically, start with the [quickstart](/azure/ai-foundry/openai/dall-e-quickstart).


#### [GPT-image-1](#tab/gpt-image-1)

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/generations?api-version=<api_version>
```


**URL**:

Replace the following values:

- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your DALL-E 3 or GPT-image-1 model deployment.
- `<api_version>` is the version of the API you want to use. For example, `2025-04-01-preview`.


**Required headers**:

- `Content-Type`: `application/json`
- `api-key`: `<your_API_key>`


**Body**:

The following is a sample request body. You specify a number of options, defined in later sections.

```json
{
    "prompt": "A multi-colored umbrella on the beach, disposable camera",
    "model": "gpt-image-1",
    "size": "1024x1024", 
    "n": 1,
    "quality": "high"
}
```

#### [DALL-E 3](#tab/dalle-3)

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/generations?api-version=<api_version>
```

**URL**:

Replace the following values:
- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your DALL-E 3 or GPT-image-1 model deployment.
- `<api_version>` is the version of the API you want to use. For example, `2024-02-01`.

**Required headers**:
- `Content-Type`: `application/json`
- `api-key`: `<your_API_key>`

**Body**:

The following is a sample request body. You specify a number of options, defined in later sections.

```json
{
    "prompt": "A multi-colored umbrella on the beach, disposable camera",
    "size": "1024x1024", 
    "n": 1,
    "quality": "hd", 
    "style": "vivid"
}
```

---

> [!TIP]
> For image generation token costs, see [Image tokens](../overview.md#image-generation-tokens).


### Output

#### [GPT-image-1](#tab/gpt-image-1)


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
> [!NOTE]
> The `response_format` parameter isn't supported for GPT-image-1, which always returns base64-encoded images.

#### [DALL-E 3](#tab/dalle-3)

The response from a successful image generation API call looks like the following example. The `url` field contains a URL where you can download the generated image. The URL stays active for 24 hours.

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

---

### Streaming

You can stream image generation requests to `gpt-image-1` by setting the `stream` parameter to `true`, and setting the `partial_images` parameter to a value between 0 and 3.

```python
import base64
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://RESOURCE-NAME-HERE/openai/v1/",  
  api_key=token_provider,
  default_headers={"api_version":"preview"}
)

stream = client.images.generate(
    model="gpt-image-1",
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


### API call rejection

Prompts and images are filtered based on our content policy. The API returns an error when a prompt or image is flagged.

If your prompt is flagged, the `error.code` value in the message is set to `contentFilter`. Here's an example:

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

It's also possible that the generated image itself is filtered. In this case, the error message is set to *Generated image was filtered as a result of our safety system*. Here's an example:

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

### Write effective text-to-image prompts

Your prompts should describe the content you want to see in the image and the visual style of the image.

When you write prompts, consider that the Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../concepts/content-filter.md).

> [!TIP]
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see the [Image prompt engineering guide](/azure/ai-foundry/openai/concepts/gpt-4-v-prompt-engineering).


### Specify API options

The following API body parameters are available for image generation models.


#### [GPT-image-1](#tab/gpt-image-1)


#### Size

Specify the size of the generated images. Must be one of `1024x1024`, `1024x1536`, or `1536x1024` for GPT-image-1 models. Square images are faster to generate.


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
> WEBP images aren't supported in the Azure OpenAI in Azure AI Foundry Models.

#### Compression

Use the *output_compression* parameter to specify the compression level for the generated image. Input an integer between `0` and `100`, where `0` is no compression and `100` is maximum compression. The default is `100`.

#### Streaming 

Use the *stream* parameter to enable streaming responses. When set to `true`, the API returns partial images as they're generated. This feature provides faster visual feedback for users and improves perceived latency. Set the *partial_images* parameter to control how many partial images are generated (1-3).


#### [DALL-E 3](#tab/dalle-3)

<!--
| Parameter Name   | Description       | Values         |
|------------------|-------------|--------------------------|
| Size             | Specifies the size of generated images. Square images generate faster.    | `1024x1024` (default), `1792x1024`, `1024x1792`           |
| Style            | DALL-E 3 offers two style options. The natural style is more similar to the default style of older models, while the vivid style generates more hyper-real and cinematic images. </br></br>The natural style is useful in cases where DALL-E 3 over-exaggerates or confuses a subject that's meant to be more simple, subdued, or realistic.     | `natural`, `vivid` (default)           |
| Quality          | Controls image quality. `hd` has finer details and better consistency; `standard` is faster.    | `hd`, `standard` (default) |
| Number (`n`)     | Must be set to 1 for DALL-E 3. To get multiple images, make parallel requests.        | `1`              |
| Response format  | Format for the returned images. Default is `url`.   | `url`, `b64_json`|
-->

#### Size

Specify the size of the generated images. Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for DALL-E 3 models. Square images are faster to generate.

#### Style

DALL-E 3 offers two style options: `natural` and `vivid`. The natural style is more similar to the default style of older models, while the vivid style generates more hyper-real and cinematic images.

The natural style is useful in cases where DALL-E 3 over-exaggerates or confuses a subject that's meant to be more simple, subdued, or realistic.

The default value is `vivid`.

#### Quality

There are two options for image quality: `hd` and `standard`. The hd option creates images with finer details and greater consistency across the image. Standard images are faster to generate.

The default value is `standard`.

#### Number

With DALL-E 3, you can't generate more than one image in a single API call: the `n` parameter must be set to *1*. To generate multiple images at once, make parallel requests.

#### Response format

The format in which DALL-E 3 returns generated images. Must be one of `url` or `b64_json`. This parameter isn't supported for GPT-image-1, which always returns base64-encoded images.

---

## Call the image edit API

The Image Edit API enables you to modify existing images based on text prompts you provide. The API call is similar to the image generation API call, but you also need to provide an input image.


#### [GPT-image-1](#tab/gpt-image-1)

> [!IMPORTANT]
> The input image must be less than 50 MB in size and must be a PNG or JPG file.

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/edits?api-version=<api_version>
```


**URL**:

Replace the following values:
- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your DALL-E 3 or GPT-image-1 model deployment.
- `<api_version>` is the version of the API you want to use. For example, `2025-04-01-preview`.

**Required headers**:
- `Content-Type`: `multipart/form-data`
- `api-key`: `<your_API_key>`

**Body**:

The following is a sample request body. You specify a number of options, defined in later sections.

> [!IMPORTANT]
> The Image Edit API takes multipart/form data, not JSON data. The example below shows sample form data that would be attached to a cURL request.

```
-F "image[]=@beach.png" \
-F 'prompt=Add a beach ball in the center' \
-F "model=gpt-image-1" \
-F "size=1024x1024" \
-F "n=1" \
-F "quality=high"
```
### API response output

The response from a successful image editing API call looks like the following example. The `b64_json` field contains the output image data.

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

### Specify image edit API options

The following API body parameters are available for image editing models, in addition to the ones available for image generation models.

#### Image

The *image* value indicates the image file you want to edit.

#### Input fidelity 

The *input_fidelity* parameter controls how much effort the model puts into matching the style and features, especially facial features, of input images. 

This parameter lets you make subtle edits to an image without changing unrelated areas. When you use high input fidelity, faces are preserved more accurately than in standard mode. 


#### Mask

The *mask* parameter uses the same type as the main *image* input parameter. It defines the area of the image that you want the model to edit, using fully transparent pixels (alpha of zero) in those areas. The mask must be a PNG file and have the same dimensions as the input image.

#### Streaming 

Use the *stream* parameter to enable streaming responses. When set to `true`, the API returns partial images as they're generated. This feature provides faster visual feedback for users and improves perceived latency. Set the *partial_images* parameter to control how many partial images are generated (1-3).

#### [DALL-E 3](#tab/dalle-3)

DALL-E models don't support the Image Edit API.

---

## Related content

* [What is Azure OpenAI?](../overview.md)
* [Quickstart: Generate images with Azure OpenAI](../dall-e-quickstart.md)
* [Image API reference](/azure/ai-foundry/openai/reference#image-generation)
* [Image API (preview) reference](/azure/ai-foundry/openai/reference-preview)


<!-- OAI HT guide https://platform.openai.com/docs/guides/images/usage
dall-e 3 features here: https://cookbook.openai.com/articles/what_is_new_with_dalle_3 -->

