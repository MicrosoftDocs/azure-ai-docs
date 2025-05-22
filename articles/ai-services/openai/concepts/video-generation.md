---
title: Sora video generation overview
description: Learn about Sora, an AI model for generating realistic and imaginative video scenes from text instructions, including safety, limitations, and supported features.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 05/22/2025
---

# Sora video generation

Sora is an AI model from OpenAI that can create realistic and imaginative video scenes from text instructions. The model is capable of generating a wide range of video content, including realistic scenes, animations, and special effects. A variety of video resolutions and durations are supported.

## Supported features

Sora can generate complex scenes with multiple characters, diverse motions, and detailed backgrounds. The model interprets prompts with contextual and physical world understanding, enabling accurate scene composition and character persistence across multiple shots. Sora demonstrates strong language comprehension for prompt interpretation and emotional character generation. 





## Best practices for prompts

Users should write text prompts in English or Latin script languages for the best video generation performance.  





## Limitations

### Content quality limitations

Sora may have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left from right), and precise time-based event sequencing such as camera movement.

### Technical limitations

Sora supports the following output resolution dimensions: 
480x480, 480x854, 854x480, 720x720, 720x1280, 1280x720, 1080x1080, 1080x1920, 1920x1080.

Sora supports the following video durations: 5, 10, 15, and 20 seconds.

Multiple video variants can be requested in the same job: for 1080p resolutions, is feature is disabled; for 720p, the maximum is two variants; for other resolutions, the maximum is four variants.

A user can create two video creation jobs at a time. Then you must wait for one of the jobs to finish before you create another.

## Responsible AI

Sora has a robust safety stack including content filtering, abuse monitoring, sensitive content blocking, and safety classifiers.

Sora does not generate scenes with acts of violence but can generate adjacent content, such as realistic war-like footage.

