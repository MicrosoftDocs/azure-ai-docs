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

## Supported features

Sora can generate complex scenes with multiple characters, diverse motions, and detailed backgrounds. 

**Text to video**: The model interprets prompts with contextual and physical world understanding, enabling accurate scene composition and character persistence across multiple shots. Sora demonstrates strong language comprehension for prompt interpretation and emotional character generation. 

**Image to video**: Sora generates video content from a still image. You can specify where in the generated video the image appears (it doesn't need to be the first frame) and which region of the image to use.

**Video to video**: Sora generates new video content from an existing video clip. You can specify where in the generated video the input video appears (it doesn't need to be the beginning).

## How it works

Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You can check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL.

## Best practices for prompts

Write text prompts in English or other Latin script languages for the best video generation performance.  


## Limitations

### Content quality limitations

Sora might have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Technical limitations

Sora has some technical limitations to be aware of:

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
