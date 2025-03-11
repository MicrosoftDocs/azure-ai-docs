---
title: How to use DALL-E models 
titleSuffix: Azure OpenAI Service
description: Learn how to generate images with the DALL-E models, and learn about the configuration options that are available.
author: PatrickFarley
ms.author: pafarley 
ms.service: azure-ai-openai
ms.custom: 
ms.topic: how-to
ms.date: 02/20/2025
manager: nitinme
keywords: 
zone_pivot_groups: 
# Customer intent: as an engineer or hobbyist, I want to know how to use DALL-E image generation models to their full capability.
---

# How to use the DALL-E models

OpenAI's DALL-E models generate images based on user-provided text prompts. This guide demonstrates how to use the DALL-E models and configure their options through REST API calls.


## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=ai-services).
- An Azure OpenAI resource created in a supported region. See [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).
- - Deploy a *dall-e-3* model with your Azure OpenAI resource.

## Call the Image Generation APIs

The following command shows the most basic way to use DALL-E with code. If this is your first time using these models programmatically, we recommend starting with the [DALL-E quickstart](/azure/ai-services/openai/dall-e-quickstart).

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/generations?api-version=<api_version>
```

**Replace the following placeholders**:
- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your DALL-E 3 model deployment.
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

### API call rejection

Prompts and images are filtered based on our content policy, returning an error when a prompt or image is flagged.

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

## Write image prompts

Your image prompts should describe the content you want to see in the image, and the visual style of image.

When writing prompts, consider that the image generation APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../concepts/content-filter.md).

> [!TIP]
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see the [Image prompt engineering guide](/azure/ai-services/openai/concepts/gpt-4-v-prompt-engineering).


## Specify API options

The following API body parameters are available for DALL-E image generation.

### Size

Specify the size of the generated images. Must be one of `1024x1024`, `1792x1024`, or `1024x1792` for DALL-E 3 models. Square images are faster to generate.

### Style

DALL-E 3 offers two style options: `natural` and `vivid`. The natural style is more similar to the default style of older models, while the vivid style generates more hyper-real and cinematic images.

The natural style is useful in cases where DALL-E 3 over-exaggerates or confuses a subject that's meant to be more simple, subdued, or realistic.

The default value is `vivid`.

### Quality

There are two options for image quality: `hd` and `standard`. The hd option creates images with finer details and greater consistency across the image. Standard images can be generated faster.

The default value is `standard`.

### Number

With DALL-E 3, you can't generate more than one image in a single API call: the `n` parameter must be set to *1*. If you need to generate multiple images at once, make parallel requests.

### Response format

The format in which the generated images are returned. Must be one of `url` (a URL pointing to the image) or `b64_json` (the base 64-byte code in JSON format). The default is `url`.

## Related content

* [What is Azure OpenAI Service?](../overview.md)
* [Quickstart: Generate images with Azure OpenAI Service](../dall-e-quickstart.md)
* [Image generation API reference](/azure/ai-services/openai/reference#image-generation)


<!-- OAI HT guide https://platform.openai.com/docs/guides/images/usage
dall-e 3 features here: https://cookbook.openai.com/articles/what_is_new_with_dalle_3 -->

