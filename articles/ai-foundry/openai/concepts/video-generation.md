---
title: Sora video generation overview (preview)
description: Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 5/29/2025
---

# Sora video generation (preview)

Sora is an AI model from OpenAI that can create realistic and imaginative video scenes from text instructions. The model is capable of generating a wide range of video content, including realistic scenes, animations, and special effects. Several video resolutions and durations are supported.

## Supported features

Sora can generate complex scenes with multiple characters, diverse motions, and detailed backgrounds. The model interprets prompts with contextual and physical world understanding, enabling accurate scene composition and character persistence across multiple shots. Sora demonstrates strong language comprehension for prompt interpretation and emotional character generation. 

## How it works

Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You can check the status of the video generation job and, once it finishes, retrieve the generated video via a download URL.

## Best practices for prompts

Users should write text prompts in English or Latin script languages for the best video generation performance.  


## Limitations

### Content quality limitations

Sora might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Technical limitations

Sora has some technical limitations to be aware of:

- Sora supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.
- Sora supports video durations between 1 and 20 seconds.
- You can request multiple video variants in a single job: for 1080p resolutions, this feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.
- You can have two video creation jobs running at the same time. You must wait for one of the jobs to finish before you can create another.
- Jobs are available for up to 24 hours after they're created. After that, you must create a new job to generate the video again.

## Responsible AI

Sora has a robust safety stack including content filtering, abuse monitoring, sensitive content blocking, and safety classifiers.

Sora doesn't generate scenes with acts of violence but can generate adjacent content, such as realistic war-like footage.

## Related content
- [Video generation quickstart](../video-generation-quickstart.md)
- [Image generation quickstart](../dall-e-quickstart.md)
