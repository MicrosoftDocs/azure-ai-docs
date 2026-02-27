---
title: 'Troubleshooting for Azure OpenAI fine-tuning'
titleSuffix: Azure OpenAI
description: Learn how to troubleshoot Azure OpenAI in Microsoft Foundry Models fine-tuning.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 11/26/2025
author: ssalgadodev
ms.author: ssalgado
---

# Troubleshooting for Azure OpenAI fine-tuning

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

## How do I enable fine-tuning?

In order to successfully access fine-tuning, you need **Azure AI User** role assigned. Even someone with high-level Service Administrator permissions would still need this account explicitly set in order to access fine-tuning. For more information, please review the [role-based access control guidance](../../../ai-foundry/concepts/rbac-foundry.md).

## Why did my upload fail?

If your file upload fails in Microsoft Foundry portal, you can view the error message under **Data files** in Foundry portal. Hover your mouse over where it says **error** (under the status column) and an explanation of the failure will be displayed.

:::image type="content" source="../media/fine-tuning/error.png" alt-text="Screenshot of fine-tuning error message." lightbox="../media/fine-tuning/error.png":::

## My fine-tuned model doesn't seem to have improved

- **Missing system message:** You need to provide a system message when you fine tune; you'll want to provide that same system message when you use the fine-tuned model. If you provide a different system message, you may see different results than what you fine-tuned for.

- **Not enough data:** while 10 is the minimum for the pipeline to run, you need hundreds to thousands of data points to teach the model a new skill. Too few data points risks overfitting and poor generalization. Your fine-tuned model may perform well on the training data, but poorly on other data because it has memorized the training examples instead of learning patterns. For best results, plan to prepare a data set with hundreds or thousands of data points.

- **Bad data:** A poorly curated or unrepresentative dataset will produce a low-quality model. Your model may learn inaccurate or biased patterns from your dataset. For example, if you're training a chatbot for customer service, but only provide training data for one scenario (e.g. item returns) it will not know how to respond to other scenarios. Or, if your training data is bad (contains incorrect responses), your model will learn to provide incorrect results.

## Fine-tuning with vision

**What to do if your images get skipped**

Your images can get skipped for the following reasons:

- contains CAPTCHAs
- contains people
- contains faces

Remove the image. For now, we can't fine-tune models with images containing these entities.

**Common issues**

|Issue| Reason/Solution|
|:----|:-----|
|**Images skipped**| Images can get skipped for the following reasons: contains CAPTCHAs, people, or faces.<br><br> Remove the image. For now, we can't fine-tune models with images containing these entities.|
|**Inaccessible URL**| Check that the image URL is publicly accessible.|
|**Image too large**| Check that your images fall within our dataset size limits.|
|**Invalid image format**| Check that your images fall within our dataset format.|

**How to upload large files**

Your training files might get quite large. You can upload files up to 8 GB in multiple parts using the [Uploads API](/rest/api/azureopenai/upload-file?view=rest-azureopenai-2024-10-21&preserve-view=true) as opposed to the Files API, which only allows file uploads of up to 512 MB.

**Reducing training cost**

If you set the detail parameter for an image to low, the image is resized to 512 by 512 pixels and is only represented by 85 tokens regardless of its size. This will reduce the cost of training.

```json
{ 
    "type": "image_url", 

    "image_url": { 

        "url": "https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png", 

        "detail": "low" 

    } 
} 
```

**Other considerations for vision fine-tuning**

To control the fidelity of image understanding, set the detail parameter of `image_url` to `low`, `high`, or `auto` for each image. This will also affect the number of tokens per image that the model sees during training time and will affect the cost of training.
