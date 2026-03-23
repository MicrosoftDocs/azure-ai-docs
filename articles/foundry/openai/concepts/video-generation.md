---
title: "Sora 2 video generation overview (preview)"
description: "Learn about Sora 2, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features."
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
zone_pivot_groups: openai-video-generation
ms.date: 03/18/2026
ms.custom:
  - classic-and-new
ai-usage: ai-assisted
---

# Video generation with Sora 2 (preview)

Sora 2 is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions and/or input images or video. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations.

[!INCLUDE [video-generation 1](../includes/concepts-video-generation-1.md)]

## Model details

Sora 2 uses the Azure OpenAI [v1 API](../api-version-lifecycle.md), aligning with OpenAI's native Sora 2 schema.

| Aspect | **Sora 2** |
|--------|------------|
| **Model type** | Adapts OpenAI's latest Sora 2 API using [v1 API](../api-version-lifecycle.md)|
| **Modalities supported** | text → video, image → video, video (generated) → video |
| **Audio generation** | ✅ Supported in outputs |
| **Remix capability** | ✅ Supported — make targeted edits to existing videos |
| **Performance & fidelity** | Enhanced realism, physics, and temporal consistency |
| **Billing** | [Per second billing information](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)

## Quickstart

Generate video clips using the Azure OpenAI service. Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL. The example uses the Sora 2 model.

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](../includes/video-generation-rest.md)]

::: zone-end

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Portal quickstart](../includes/video-generation-studio.md)]

::: zone-end

### Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli)

[!INCLUDE [video-generation 2](../includes/concepts-video-generation-2.md)]

## Limitations

### Content quality limitations

Sora 2 might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Technical limitations

Sora 2 video generation is currently in preview. Keep the following limitations in mind:

- Sora 2 supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.
- Sora 2 can produce videos between 1 and 20 seconds long.
- You can request multiple video variants in a single job: for 1080p resolutions, this feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can use up to two images as input (the generated video interpolates content between them).
- You can use one video up to five seconds as input.

[!INCLUDE [video-generation 3](../includes/concepts-video-generation-3.md)]
