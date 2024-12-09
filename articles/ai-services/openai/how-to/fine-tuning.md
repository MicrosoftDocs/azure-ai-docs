---
title: 'Customize a model with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to create your own customized model with Azure OpenAI Service by using Python, the REST APIs, or Azure OpenAI Studio.
#services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python
ms.topic: how-to
ms.date: 11/11/2024
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
---

# Customize a model with fine-tuning

Azure OpenAI Service lets you tailor our models to your personal datasets by using a process known as *fine-tuning*. This customization step lets you get more out of the service by providing:

- Higher quality results than what you can get just from [prompt engineering](../concepts/prompt-engineering.md)
- The ability to train on more examples than can fit into a model's max request context limit.
- Token savings due to shorter prompts
- Lower-latency requests, particularly when using smaller models.

In contrast to few-shot learning, fine tuning improves the model by training on many more examples than can fit in a prompt, letting you achieve better results on a wide number of tasks. Because fine tuning adjusts the base model’s weights to improve performance on the specific task, you won’t have to include as many examples or instructions in your prompt. This means less text sent and fewer tokens processed on every API call, potentially saving cost, and improving request latency.

We use LoRA, or low rank approximation, to fine-tune models in a way that reduces their complexity without significantly affecting their performance. This method works by approximating the original high-rank matrix with a lower rank one, thus only fine-tuning a smaller subset of *important* parameters during the supervised training phase, making the model more manageable and efficient. For users, this makes training faster and more affordable than other techniques.

> [!NOTE]
> Azure OpenAI currently only supports text-to-text fine-tuning for all supported models including GPT-4o mini.

::: zone pivot="programming-language-studio"

[!INCLUDE [Azure OpenAI Studio fine-tuning](../includes/fine-tuning-unified.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/fine-tuning-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

## Vision fine-tuning

Fine-tuning is also possible with images in your JSONL files. Just as you can send one or many image inputs to chat completions, you can include those same message types within your training data. Images can be provided either as publicly accessible URLs or data URIs containing [base64 encoded images](/azure/ai-services/openai/how-to/gpt-with-vision?tabs=rest#call-the-chat-completion-apis). 

### Image dataset requirements

- Your training file can contain a maximum of 50,000 examples that contain images (not including text examples).
- Each example can have at most 64 images.
- Each image can be at most 10 MB.

### Format

Images must be:

- JPEG
- PNG
- WEBP

Images must be in the RGB or RGBA image mode.

You cannot include images as output from messages with the assistant role.

### Content moderation policy

We scan your images before training to ensure that they comply with our usage policy [Transparency Note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text). This may introduce latency in file validation before fine tuning begins.

Images containing the following will be excluded from your dataset and not used for training:

- People
- Faces
- CAPTCHAs

> [!IMPORTANT]
>For  vision fine tuning face screening process: We screen for faces/people to skip those images from training the model. The screening capability leverages face detection **WITHOUT** Face identification which means we don't create facial templates or measure specific facial geometry, and the technology used to screen for faces is incapable of uniquely identifying the individuals. To know more about data and Privacy for face refer to - [Data and privacy for Face - Azure AI services | Microsoft Learn](/legal/cognitive-services/computer-vision/imageanalysis-data-privacy-security?context=%2Fazure%2Fai-services%2Fcomputer-vision%2Fcontext%2Fcontext).

## Troubleshooting

### How do I enable fine-tuning?

In order to successfully access fine-tuning, you need **Cognitive Services OpenAI Contributor assigned**. Even someone with high-level Service Administrator permissions would still need this account explicitly set in order to access fine-tuning. For more information, please review the [role-based access control guidance](/azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-openai-contributor).

### Why did my upload fail?

If your file upload fails in Azure OpenAI Studio, you can view the error message under “data files” in Azure OpenAI Studio. Hover your mouse over where it says “error” (under the status column) and an explanation of the failure will be displayed.

:::image type="content" source="../media/fine-tuning/error.png" alt-text="Screenshot of fine-tuning error message." lightbox="../media/fine-tuning/error.png":::

### My fine-tuned model does not seem to have improved

- **Missing system message:** You need to provide a system message when you fine tune; you will want to provide that same system message when you use the fine-tuned model. If you provide a different system message, you may see different results than what you fine-tuned for.

- **Not enough data:** while 10 is the minimum for the pipeline to run, you need hundreds to thousands of data points to teach the model a new skill. Too few data points risks overfitting and poor generalization. Your fine-tuned model may perform well on the training data, but poorly on other data because it has memorized the training examples instead of learning patterns. For best results, plan to prepare a data set with hundreds or thousands of data points.

- **Bad data:** A poorly curated or unrepresentative dataset will produce a low-quality model. Your model may learn inaccurate or biased patterns from your dataset. For example, if you are training a chatbot for customer service, but only provide training data for one scenario (e.g. item returns) it will not know how to respond to other scenarios. Or, if your training data is bad (contains incorrect responses), your model will learn to provide incorrect results.

### Fine-tuning with vision

**What to do if your images get skipped**

Your images can get skipped for the following reasons:

- contains CAPTCHAs
- contains people
- contains faces

Remove the image. For now, we cannot fine-tune models with images containing these entities.

**Common issues**

|Issue| Reason/Solution|
|:----|:-----|
|**Images skipped**| Images can get skipped for the following reasons: contains CAPTCHAs, people, or faces.<br><br> Remove the image. For now, we cannot fine-tune models with images containing these entities.|
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

## Next steps

- Explore the fine-tuning capabilities in the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../concepts/models.md#fine-tuning-models)
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)
