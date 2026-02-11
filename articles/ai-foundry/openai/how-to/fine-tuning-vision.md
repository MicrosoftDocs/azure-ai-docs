---
title: 'Vision fine-tuning'
titleSuffix: Azure OpenAI
description: Learn how to fine-tune Azure OpenAI GPT-4o and GPT-4.1 models with image inputs, including dataset requirements, image formats, and best practices.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
monikerRange: 'foundry-classic || foundry'
---

# Vision fine-tuning

Learn how to fine-tune Azure OpenAI models with image data to customize visual understanding for your use case. Vision fine-tuning lets you include image inputs in your training examples, following the same chat completions format used for text fine-tuning.

Images can be provided either as publicly accessible URLs or data URIs containing [base64 encoded images](/azure/ai-foundry/openai/how-to/gpt-with-vision?tabs=rest#call-the-chat-completion-apis).

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- An Microsoft Foundry resource. See [Create an Azure AI Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource).
- Familiarity with the [fine-tuning workflow](fine-tuning.md). Vision fine-tuning follows the same process with image-specific data formatting.
- Fine-tuning access for the supported models in a [supported region](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).

## Model support

Vision fine-tuning is supported for the following models only:

| Model | Version | Region availability |
|-------|--------|--------|
| `gpt-4o` | `2024-08-06` | [Supported regions](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models). |
| `gpt-4.1` | `2025-04-14` | [Supported regions](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models). |

## Image dataset requirements

| Constraint | Limit |
|------------|-------|
| Max examples with images per training file | 50,000 |
| Max images per example | 64 |
| Max image file size | 10 MB |

## Format

Images must be:

- JPEG
- PNG
- WEBP

Images must be in the RGB or RGBA image mode.

You cannot include images as output from messages with the assistant role.

Your example file requires at least 10 examples.

### Image detail control

You can control the fidelity of image processing using the `detail` parameter in the `image_url` object. Note that the detail parameter will impact the cost of your training job; Low will be lower cost but may lose fine visual details.

- `low` — Downscales images to 512×512 pixels. Uses fewer tokens and reduces training cost.
- `high` — Processes images at full resolution. Provides more visual detail but increases token usage.
- `auto` — Lets the model decide based on image size (default).

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/image.png",
    "detail": "low"
  }
}
```

## Best practices

- **Diverse examples**: Include variety in image content, angles, and lighting conditions.
- **Consistent annotations**: Ensure assistant responses are consistent in style and detail level across examples.

### Example file format

```json
{
  "messages": [
    { "role": "system", "content": "You are a helpful AI assistant." },
    { "role": "user", "content": "Describe the image?" },
    { "role": "user", "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png"
          }
        }
      ]
    },
    { "role": "assistant", "content": "The image appears to be a watercolor painting of a city skyline, featuring tall buildings and a recognizable structure often associated with Seattle, like the Space Needle. The artwork uses soft colors and brushstrokes to create a somewhat abstract and artistic representation of the cityscape." }
  ]
}
```

## Create a vision fine-tuning job

After preparing your dataset with image examples, follow the standard fine-tuning workflow to submit your job:

1. Upload your training file using the Files API or the Microsoft Foundry portal. Image validation may take longer than text-only uploads due to [content moderation screening](#content-moderation-policy).
2. Create a fine-tuning job specifying your uploaded file and a [supported vision model](#model-support).
3. Monitor the job until completion.

For detailed steps, see [Fine-tune an Azure OpenAI model](fine-tuning.md).

## Content moderation policy

We scan your images before training to ensure that they comply with our usage policy. For details, see the [Transparency Note](/azure/ai-foundry/responsible-ai/openai/transparency-note). This may introduce latency in file validation before fine-tuning begins.

Images containing the following will be excluded from your dataset and not used for training:

- People
- Faces
- Children
- CAPTCHAs

> [!IMPORTANT]
> **Face screening process for vision fine-tuning:**
>
> - Images are screened for faces/people and skipped from training.
> - The screening uses face **detection** only, not face identification.
> - No facial templates are created, and no specific facial geometry is measured.
> - The technology cannot uniquely identify individuals.
>
> For more information about data privacy, see [Data and privacy for Face - Foundry Tools](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security).

## Troubleshooting

### Images skipped during training

Images can be excluded from training for several reasons:

| Reason | Resolution |
|--------|------------|
| Image URL not accessible | Ensure URLs are publicly accessible or use base64 data URIs |
| Image exceeds 10 MB | Resize or compress the image |
| Unsupported format | Convert to JPEG, PNG, or WEBP |
| Not RGB/RGBA mode | Convert image color mode |
| Content policy violation | Images with people, faces, children, or CAPTCHAs are automatically excluded |
| Too many images in example | Reduce to 10 or fewer images per example |

## Next steps

- [Fine-tune a model](fine-tuning.md) — Complete fine-tuning workflow including upload, training, and monitoring.
- [Deploy a fine-tuned model](fine-tuning-deploy.md) — Deploy your customized model for inference.
- [Fine-tuning model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models) — Check which regions support vision fine-tuning.
- [Model quotas and limits](../quotas-limits.md) — Review rate limits and quotas for fine-tuned models.
