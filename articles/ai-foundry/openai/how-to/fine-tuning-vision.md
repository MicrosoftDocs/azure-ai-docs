---
title: 'Vision customization'
titleSuffix: Azure OpenAI
description: Learn how to fine-tune a model with image inputs.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 11/26/2025
author: mrbullwinkle
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
---

# Vision fine-tuning

Fine-tuning is also possible with images in your JSONL files. Just as you can send one or many image inputs to chat completions, you can include those same message types within your training data. Images can be provided either as publicly accessible URLs or data URIs containing [base64 encoded images](/azure/ai-foundry/openai/how-to/gpt-with-vision?tabs=rest#call-the-chat-completion-apis). 

## Model support

Vision fine-tuning is supported for `gpt-4o` version `2024-08-06` and `gpt-4.1` version `2025-04-14` models only.

## Image dataset requirements

- Your training file can contain a maximum of 50,000 examples that contain images (not including text examples).
- Each example can have at most 64 images.
- Each image can be at most 10 MB.

## Format

Images must be:

- JPEG
- PNG
- WEBP

Images must be in the RGB or RGBA image mode.

You cannot include images as output from messages with the assistant role.

As with all fine-tuning training your example file requires at least 10 examples.

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
    { "role": "assistant", "content": "The image appears to be a watercolor painting of a city skyline, featuring tall buildings and a recognizable structure often associated with Seattle, like the Space Needle. The artwork uses soft colors and brushstrokes to create a somewhat abstract and artistic representation of the cityscape" }
  ]
}
```


## Content moderation policy

We scan your images before training to ensure that they comply with our usage policy [Transparency Note](/azure/ai-foundry/responsible-ai/openai/transparency-note). This may introduce latency in file validation before fine tuning begins.

Images containing the following will be excluded from your dataset and not used for training:

- People
- Faces
- CAPTCHAs

> [!IMPORTANT]
>For vision fine tuning face screening process: We screen for faces/people to skip those images from training the model. The screening capability leverages face detection **WITHOUT** Face identification which means we don't create facial templates or measure specific facial geometry, and the technology used to screen for faces is incapable of uniquely identifying the individuals. To know more about data and Privacy for face refer to - [Data and privacy for Face - Foundry Tools | Microsoft Learn](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security).

## Next steps

- To modify content safety for fine-tuning refer to terms listed in the [form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu)
- [Deploy a fine-tuned model](fine-tuning-deploy.md).
- Review fine-tuning [model regional availability](../concepts/models.md?pivots=azure-openai#fine-tuning-models)
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)
