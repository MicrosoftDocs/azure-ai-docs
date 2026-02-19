---
title: Audio content creation tool
titleSuffix: Foundry Tools
description: Audio content creation is an online tool that allows you to run text to speech synthesis without writing any code.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 8/5/2025
ms.author: pafarley
zone_pivot_groups: foundry-speech-studio
---

# Text to speech with the audio content creation tool

You can use the audio content creation tool in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) or [Speech Studio](https://speech.microsoft.com/portal/audiocontentcreation) for text to speech without writing any code. 

> [!TIP]
> Select **Foundry portal** or **Speech Studio** at the top of this article. 

Build highly natural audio content for various scenarios, such as audiobooks, news broadcasts, video narrations, and chat bots. With audio content creation, you can efficiently fine-tune text to speech voices and design customized audio experiences. 

The tool is based on [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup.md). It allows you to adjust text to speech output attributes in real-time or batch synthesis, such as voice characters, voice styles, speaking speed, pronunciation, and prosody.

- No-code approach: You can use the audio content creation tool for text to speech synthesis without writing any code. The output audio might be the final deliverable that you want. For example, you can use the output audio for a podcast or a video narration. 
- Developer-friendly: You can listen to the output audio and adjust the SSML to improve speech synthesis. Then you can use the [Speech SDK](speech-sdk.md) or [Speech CLI](spx-basics.md) to integrate the SSML into your applications. 

You have easy access to a broad portfolio of [languages and voices](language-support.md?tabs=tts). These voices include state-of-the-art standard voices and your custom voice, if you built one.

The audio content creation tool is free to access; you pay only for Speech service usage.

::: zone pivot="ai-foundry-portal"
[!INCLUDE [Foundry include](includes/how-to/audio-content-creation/ai-foundry.md)]
::: zone-end

::: zone pivot="speech-studio"
[!INCLUDE [Speech Studio include](includes/how-to/audio-content-creation/speech-studio.md)]
::: zone-end

## Related content

- [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup.md)
- [Batch synthesis](batch-synthesis.md)
