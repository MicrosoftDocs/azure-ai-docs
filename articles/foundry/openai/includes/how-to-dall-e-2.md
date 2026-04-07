---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Call the image edit API

The Image Edit API enables you to modify existing images based on text prompts you provide. The API call is similar to the image generation API call, but you also need to provide an input image.

> [!IMPORTANT]
> The input image must be less than 50 MB in size and must be a PNG or JPG file.

Send a POST request to:

```
https://<your_resource_name>.openai.azure.com/openai/deployments/<your_deployment_name>/images/edits?api-version=<api_version>
```

**URL**:

Replace the following values:
- `<your_resource_name>` is the name of your Azure OpenAI resource.
- `<your_deployment_name>` is the name of your GPT-image-1 series model deployment.
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

> [!IMPORTANT]
> Input fidelity is not supported by the `gpt-image-1-mini` model.

#### Mask

The *mask* parameter uses the same type as the main *image* input parameter. It defines the area of the image that you want the model to edit, using fully transparent pixels (alpha of zero) in those areas. The mask must be a PNG file and have the same dimensions as the input image.

#### Streaming 

Use the *stream* parameter to enable streaming responses. When set to `true`, the API returns partial images as they're generated. This feature provides faster visual feedback for users and improves perceived latency. Set the *partial_images* parameter to control how many partial images are generated (1-3).

#### Transparency

Set the *background* parameter to `transparent` and *output_format* to `PNG` on an image generate request to get an image with a transparent background.

## Write effective text-to-image prompts

Your prompts should describe the content you want to see in the image and the visual style of the image.

When you write prompts, consider that the Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it doesn't generate an image. For more information, see [Content filtering](../../../foundry-classic/foundry-models/concepts/content-filter.md).

> [!TIP]
> For a thorough look at how you can tweak your text prompts to generate different kinds of images, see the [Image prompt engineering guide](/azure/ai-foundry/openai/concepts/gpt-4-v-prompt-engineering).

## Responsible AI and Image Generation

Azure OpenAI's image generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use.

In addition, Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

Customers can learn more about these safeguards and how to customize them here:
- Learn more: Explore [content filtering](/azure/ai-foundry/openai/concepts/content-filter)
- Request customization: Apply to [opt out of content filtering](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu)

### Special considerations for generating images of minors

Photorealistic images of minors are blocked by default. Customers can [request access](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUQVFQRDhQRjVPNllLMVZCSVNYVUs4MzhNMyQlQCN0PWcu) to this model capability. Enterprise-tier customers are automatically approved.

## Troubleshooting

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

### Rate limit errors

If you receive a 429 error, you've exceeded your rate limit. Wait before retrying or request a quota increase in the Azure portal.

### Authentication errors

If you receive a 401 error:
- **API key auth**: Verify your API key is correct and not expired.
- **Managed identity**: Ensure your identity has the **Cognitive Services OpenAI User** role on the resource.

### Timeout errors

Image generation can take up to 60 seconds for complex prompts. If you experience timeouts:
- Use streaming to get partial results sooner.
- Simplify your prompt.
- Try a smaller image size.
