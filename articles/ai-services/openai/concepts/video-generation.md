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



## Responsible AI

Sora has a robust safety stack including a moderation stack with prompt rewrites, content filtering, abuse monitoring, sensitive content blocking, and safety classifiers.

Sora does not generate scenes with acts of violence but can demonstrate realistic war-like footage  

Commonly filtered names such as Emma Watson, Obama, Biden, etc. are not filtered.

## Limitations

### Content quality limitations

Sora may have difficulty with complex physics, causal relationships (for example, bite marks on a cookie), spatial reasoning (for example, knowing left vs. right), and precise time-base event sequencing such as camera movement.

### Technical limitations

Sora supports the following output resolution dimensions: 480x480, 480x854, 720x720, 720x1280, 1080x1080, 1920x1080. 

Sora supports the following video durations: 5, 10, 15, and 20 seconds. The maximum duration for 1080x videos is 10 seconds.


Max variants on 1080p =1; 720 =2; otherwise 4  

Limiting 2 pending tasks per customer  