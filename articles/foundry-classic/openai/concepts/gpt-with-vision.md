---
title: "Vision-enabled chat model concepts (classic)"
description: "Learn concepts for using images in your AI model chats, with GPT-4 Turbo with Vision and other models. (classic)"
author: PatrickFarley
ms.author: pafarley
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: concept-article 
ms.date: 01/30/2026
manager: nitinme
ai-usage: ai-assisted

---

# Vision-enabled chat model concepts (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Vision-enabled chat models are large multimodal models (LMM) developed by OpenAI that analyze images and provide textual responses to questions about them. They incorporate both natural language processing and visual understanding. This guide provides details on their capabilities and limitations. To see which models support image input, see the [Models page](../../foundry-models/concepts/models-sold-directly-by-azure.md).

To try out vision-enabled chat models, see the [quickstart](/azure/ai-foundry/openai/gpt-v-quickstart).

## Vision-enabled chats

The vision-enabled models answer general questions about what's present in the images you upload.

[!INCLUDE [input limitations](../../../foundry/openai/includes/gpt-with-vision-input-limitations.md)]


<!--
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
-->

<!--
### Video support

- **Low resolution**: Video frames are analyzed using GPT-4 Turbo with Vision's "low resolution" setting, which may affect the accuracy of small object and text recognition in the video.
- **Video file limits**: Both MP4 and MOV file types are supported. In [Foundry portal](https://ai.azure.com/?cid=learnDocs), videos must be less than 3 minutes long. When you use the API there is no such limitation.
- **Prompt limits**: Video prompts only contain one video and no images. In [Foundry portal](https://ai.azure.com/?cid=learnDocs), you can clear the session to try another video or images.
- **Limited frame selection**: The service selects 20 frames from the entire video, which might not capture all the critical moments or details. Frame selection can be approximately evenly spread through the video or focused by a specific video retrieval query, depending on the prompt.
- **Language support**: The service primarily supports English for grounding with transcripts. Transcripts don't provide accurate information on lyrics in songs.
-->

## Related content

- Get started using vision-enabled models by following the [quickstart](/azure/ai-foundry/openai/gpt-v-quickstart).
- For a more in-depth look at the APIs, follow the [how-to guide](../how-to/gpt-with-vision.md).
- See the [completions and embeddings API reference](../reference.md)
