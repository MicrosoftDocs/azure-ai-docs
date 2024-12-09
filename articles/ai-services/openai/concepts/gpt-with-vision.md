---
title: GPT-4 Turbo with Vision concepts
titleSuffix: Azure OpenAI
description: Learn concepts related to using images in your AI model chats, enabled through GPT-4 Turbo with Vision and other models.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 09/24/2024
manager: nitinme
---

# GPT-4 Turbo with Vision concepts

GPT-4 Turbo with Vision is a large multimodal model (LMM) developed by OpenAI that can analyze images and provide textual responses to questions about them. It incorporates both natural language processing and visual understanding. This guide provides details on the capabilities and limitations of GPT-4 Turbo with Vision.

To try out GPT-4 Turbo with Vision, see the [quickstart](/azure/ai-services/openai/gpt-v-quickstart).

## Chats with vision

The GPT-4 Turbo with Vision model answers general questions about what's present in the images or videos you upload.


## Special pricing information

> [!IMPORTANT]
> Pricing details are subject to change in the future.

GPT-4 Turbo with Vision accrues charges like other Azure OpenAI chat models. You pay a per-token rate for the prompts and completions, detailed on the [Pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). The base charges and additional features are outlined here:

Base Pricing for GPT-4 Turbo with Vision is:
- Input: $0.01 per 1000 tokens
- Output: $0.03 per 1000 tokens

See the [Tokens section of the overview](/azure/ai-services/openai/overview#tokens) for information on how text and images translate to tokens.


### Example image price calculation

> [!IMPORTANT]
> The following content is an example only, and prices are subject to change in the future.

For a typical use case, take an image with both visible objects and text and a 100-token prompt input. When the service processes the prompt, it generates 100 tokens of output. In the image, both text and objects can be detected. The price of this transaction would be:

| Item        | Detail        |  Cost   |
|-----------------|-----------------|--------------|
| Text prompt input | 100 text tokens | $0.001 |
| Example image input (see [Image tokens](/azure/ai-services/openai/overview#image-tokens-gpt-4-turbo-with-vision)) | 170 + 85 image tokens | $0.00255 |
| Enhanced add-on features for OCR | $1.50 / 1000 transactions | $0.0015 |
| Enhanced add-on features for Object Grounding | $1.50 / 1000 transactions | $0.0015 | 
| Output Tokens      | 100 tokens (assumed)    | $0.003       |
| **Total** |  |**$0.00955** |


### Example video price calculation

> [!IMPORTANT]
> The following content is an example only, and prices are subject to change in the future.

For a typical use case, take a 3-minute video with a 100-token prompt input. The video has a transcript that's 100 tokens long, and when the service processes the prompt, it generates 100 tokens of output. The pricing for this transaction would be:

| Item        | Detail        |  Cost   |
|-----------------|-----------------|--------------|
| GPT-4 Turbo with Vision input tokens      | 100 text tokens    | $0.001     |
| Additional Cost to identify frames        | 100 input tokens + 700 tokens + 1 Video Retrieval transaction         | $0.00825     |
| Image Inputs and Transcript Input         | 20 images (85 tokens each) + 100 transcript tokens            | $0.018       |
| Output Tokens      | 100 tokens (assumed)    | $0.003       |
| **Total**      |      | **$0.03025** |

Additionally, there's a one-time indexing cost of $0.15 to generate the Video Retrieval index for this 3-minute video. This index can be reused across any number of Video Retrieval and GPT-4 Turbo with Vision API calls.

## Input limitations

This section describes the limitations of GPT-4 Turbo with Vision.

### Image support

- **Maximum input image size**: The maximum size for input images is restricted to 20 MB.
- **Low resolution accuracy**: When images are analyzed using the "low resolution" setting, it allows for faster responses and uses fewer input tokens for certain use cases. However, this could impact the accuracy of object and text recognition within the image.
- **Image chat restriction**: When you upload images in Azure AI Foundry portal or the API, there is a limit of 10 images per chat call.

### Video support

- **Low resolution**: Video frames are analyzed using GPT-4 Turbo with Vision's "low resolution" setting, which may affect the accuracy of small object and text recognition in the video.
- **Video file limits**: Both MP4 and MOV file types are supported. In Azure AI Foundry portal, videos must be less than 3 minutes long. When you use the API there is no such limitation.
- **Prompt limits**: Video prompts only contain one video and no images. In Azure AI Foundry portal, you can clear the session to try another video or images.
- **Limited frame selection**: The service selects 20 frames from the entire video, which might not capture all the critical moments or details. Frame selection can be approximately evenly spread through the video or focused by a specific video retrieval query, depending on the prompt.
- **Language support**: The service primarily supports English for grounding with transcripts. Transcripts don't provide accurate information on lyrics in songs.

## Next steps

- Get started using GPT-4 Turbo with Vision by following the [quickstart](/azure/ai-services/openai/gpt-v-quickstart).
- For a more in-depth look at the APIs, and to use video prompts in chat, follow the [how-to guide](../how-to/gpt-with-vision.md).
- See the [completions and embeddings API reference](../reference.md)
