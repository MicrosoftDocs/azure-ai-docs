---
title: 'Vision customization'
titleSuffix: Azure OpenAI
description: Learn how to fine-tune a model with image inputs.
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 02/24/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
---

# Vision fine-tuning

Fine-tuning is also possible with images in your JSONL files. Just as you can send one or many image inputs to chat completions, you can include those same message types within your training data. Images can be provided either as publicly accessible URLs or data URIs containing [base64 encoded images](/azure/ai-services/openai/how-to/gpt-with-vision?tabs=rest#call-the-chat-completion-apis). 

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
    { "role": "system", "content": "You are an assistant that identifies uncommon cheeses." },
    { "role": "user", "content": "What is this cheese?" },
    { "role": "user", "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Danbo_Cheese.jpg"
          }
        }
      ]
    },
    { "role": "assistant", "content": "Danbo" }
  ]
}
```


## Content moderation policy

We scan your images before training to ensure that they comply with our usage policy [Transparency Note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text). This may introduce latency in file validation before fine tuning begins.

Images containing the following will be excluded from your dataset and not used for training:

- People
- Faces
- CAPTCHAs

> [!IMPORTANT]
>For  vision fine tuning face screening process: We screen for faces/people to skip those images from training the model. The screening capability leverages face detection **WITHOUT** Face identification which means we don't create facial templates or measure specific facial geometry, and the technology used to screen for faces is incapable of uniquely identifying the individuals. To know more about data and Privacy for face refer to - [Data and privacy for Face - Azure AI services | Microsoft Learn](/legal/cognitive-services/computer-vision/imageanalysis-data-privacy-security?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext).

## Next steps

- [Deploy a finetuned model](fine-tuning-deploy.md).
- Review fine-tuning [model regional availability](../concepts/models.md#fine-tuning-models)
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)