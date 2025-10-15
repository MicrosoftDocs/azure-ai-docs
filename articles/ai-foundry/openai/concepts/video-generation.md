---
title: Sora video generation overview (preview)
description: Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: conceptual
ms.date: 09/16/2025
---

# Video generation with Sora (preview)

Sora is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions and/or input images or video. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations.
Azure OpenAI supports two versions of Sora:
- Sora (or Sora 1): Azure OpenAI–specific implementation released as an API in early preview.
- Sora 2: The latest OpenAI-based API, now being adapted for Azure OpenAI
## Overview
- Modalities: text → video, image → video, video (generated) → video
- Audio: Sora 2 supports audio generation in output videos (similar to the Sora app).
- Remix: Sora 2 introduces the ability to remix existing videos by making targeted adjustments instead of regenerating from scratch.

## Sora 1 vs. Sora 2

| Aspect | **Sora 1 (Azure OpenAI)** | **Sora 2 (OpenAI-based API)** |
|--------|-----------------------------|-------------------------------|
| **Model type** | Azure-specific API implementation | Adapts OpenAI’s latest Sora API |
| **Availability** | Available exclusively on Azure OpenAI (Preview) | Rolling out on Azure; **Sora 2 Pro** coming later |
| **Modalities supported** | text → video, image → video, video → video | text → video, image → video, **video (generated) → video** |
| **Audio generation** | ❌ Not supported | ✅ Supported in outputs |
| **Remix capability** | ❌ Not supported | ✅ Supported — make targeted edits to existing videos |
| **API behavior** | Uses Azure-specific API schema | Aligns with OpenAI’s native Sora 2 schema |
| **Performance & fidelity** | Early preview; limited realism and motion range | Enhanced realism, physics, and temporal consistency |
| **Intended use** | Enterprise preview deployments | Broader developer availability with improved API parity |


## Sora 2 API 
Provides 5 endpoints, each with distinct capabilities. 
- Create Video: Start a new render job from a prompt, with optional reference inputs or a remix id.
- Get Video Status: Retrieve the current state of a render job and monitor its progress
- Download Video: Fetch the finished MP4 once the job is completed.
- List Videos: Enumerate your videos with pagination for history, dashboards, or housekeeping. 
- Delete Videos: Delete an individual video id from Azure OpenAI’s storage

### API Parameters

| Parameter | Type | **Sora 2** | 
|------------|------|------------|
| **Prompt** | String (required) | Natural-language description of the shot. Include shot type, subject, action, setting, lighting, and any desired camera motion to reduce ambiguity. Keep it *single-purpose* for best adherence. | 
| **Model** | String (optional) | `Sora-2` (default) |
| **Size (Output resolution in width × height)** | String (optional) | Portrait: `720×1280`  <br> Landscape: `1280×720`  <br> **Default:** 720×1280 |
| **Seconds** | String (optional) | `4 / 8 / 12`  <br> **Default:** 4 | 
| **Input reference** | File (optional) | Single reference image used as a visual anchor for the first frame. <br> Accepted MIME types: `image/jpeg`, `image/png`, `image/webp`. Must match size exactly. | 
| **Remix_video_id** | String (optional) | ID of a previously completed video (e.g., `video_...`) to reuse structure, motion, and framing. | Same as Sora 2 |

The API is the same as the [OAI API]([url](https://platform.openai.com/docs/guides/video-generation)) , minus the following two things:
- In AOAI API, you have to replace the model's name, by the name of the deployment. For example, "sora2-
test"


## How it works

Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You can check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL.

## Best practices for prompts

Write text prompts in English or other Latin script languages for the best video generation performance.  


## Limitations

### Content quality limitations

Sora might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Sora 2 Technical Limitations 

- Please see Sora 2 API details above 
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.

### Sora 1 Technical limitations

- Sora supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.
- Sora can produce videos between 1 and 20 seconds long.
- You can request multiple video variants in a single job: for 1080p resolutions, this feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.
- You can use up to two images as input (the generated video interpolates content between them).
- You can use one video up to five seconds as input.

## Responsible AI

Sora has a robust safety stack that includes content filtering, abuse monitoring, sensitive content blocking, and safety classifiers.

Sora doesn't generate scenes with acts of violence but can generate adjacent content, such as realistic war-like footage.

## Related content
- [Video generation quickstart](../video-generation-quickstart.md)
- [Image generation quickstart](../dall-e-quickstart.md)
