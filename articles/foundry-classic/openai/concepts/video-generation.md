---
title: "Sora video generation overview (preview) (classic)"
description: "Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features. (classic)"
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
zone_pivot_groups: openai-video-generation
ms.date: 12/1/2025
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Video generation with Sora (preview) (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/video-generation.md)

Sora is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions and/or input images or video. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations.

[!INCLUDE [video-generation 1](../../../foundry/openai/includes/concepts-video-generation-1.md)]

## Model comparison

Azure OpenAI supports two versions of Sora:
- Sora (or Sora 1): Azure OpenAI–specific implementation released as an API in early preview.
- Sora 2: The latest OpenAI-based API, now available with the Azure OpenAI [v1 API](../api-version-lifecycle.md).

| Aspect | **Sora 1 (Azure OpenAI)** | **Sora 2 (OpenAI-based API)** |
|--------|-----------------------------|-------------------------------|
| **Model type** | Azure-specific API implementation | Adapts OpenAI’s latest Sora API using [v1 API](../api-version-lifecycle.md)|
| **Availability** | Available exclusively on Azure OpenAI (Preview) | Rolling out on Azure; **Sora 2 Pro** coming later |
| **Modalities supported** | text → video, image → video, video → video | text → video, image → video, **video (generated) → video** |
| **Audio generation** | ❌ Not supported | ✅ Supported in outputs |
| **Remix capability** | ❌ Not supported | ✅ Supported — make targeted edits to existing videos |
| **API behavior** | Uses Azure-specific API schema | Aligns with OpenAI’s native Sora 2 schema |
| **Performance & fidelity** | Early preview; limited realism and motion range | Enhanced realism, physics, and temporal consistency |
| **Intended use** | Enterprise preview deployments | Broader developer availability with improved API parity |
| **Billing** | Billed differently across duration and resolutions | [Per second billing information](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)

## Quickstart

Generate video clips using the Azure OpenAI service. Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL. The example uses the Sora model.

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

[!INCLUDE [video-generation 2](../../../foundry/openai/includes/concepts-video-generation-2.md)]

## Limitations

### Content quality limitations

Sora might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Technical Limitations

Sora video generation is currently in preview. Keep the following limitations in mind:

#### [Sora 1](#tab/sora-1) 

- Please see Sora 2 API details above 
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can create two video job requests per minute. The Sora 2 quota only counts video job requests: other types of requests are not rate-limited.

#### [Sora 2](#tab/sora-2) 

- Sora supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.
- Sora can produce videos between 1 and 20 seconds long.
- You can request multiple video variants in a single job: for 1080p resolutions, this feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can use up to two images as input (the generated video interpolates content between them).
- You can use one video up to five seconds as input.

---

[!INCLUDE [video-generation 3](../../../foundry/openai/includes/concepts-video-generation-3.md)]
