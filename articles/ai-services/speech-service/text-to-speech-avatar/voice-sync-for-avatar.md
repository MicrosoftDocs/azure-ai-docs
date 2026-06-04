---
title: Voice sync for avatar - Speech service
titleSuffix: Azure AI services
description: Introduction to voice sync for avatar
manager: nitinme
ms.service: azure-speech-foundry-tools
ms.topic: overview
ms.date: 4/29/2026
ms.author: melindam
author: melindam
reviewer: patrickfarley
ms.reviewer: pafarley
---

# Voice sync for avatar

Voice sync for avatar is a synthetic voice that resembles the avatar talent's voice. It's trained together with the custom video avatar by using audio from the training video, making it the most efficient custom voice option for a custom video avatar.

- No need to apply for additional limited access. If you've been granted limited access to the custom video avatar, you can also train a voice sync for avatar.
- It doesn't require additional audio training data.
- It's trained together with the custom video avatar model.

## Features and limitations

Voice sync for avatar offers the same voice quality as personal voice, and it also supports multiple languages. However, you can't use voice sync for avatar independently—it must be used together with the custom video avatar.

Custom photo avatar doesn't currently support voice sync for avatar.

## How to create a voice sync for avatar

A voice sync for avatar is created during custom video avatar fine-tuning. When you upload the consent video for the avatar talent, you can choose the avatar type: either *Avatar with a voice sync for avatar* or *Avatar only*. If you choose to create an avatar with a voice sync for avatar, the verbal statement in the consent video must include consent for synthetic voice creation and use.

For more details, see [Create a custom video avatar](/azure/ai-services/speech-service/text-to-speech-avatar/custom-avatar-create?pivots=ai-foundry-portal).


## Supported regions and languages

Voice sync for avatar supports the same languages as [personal voice](../language-support.md#personal-voice)

The regions that support voice sync for avatar use and creation are listed in [Speech service regions table](../regions.md?tabs=ttsavatar).

> [!NOTE]
> When you copy a custom video avatar model to another resource, the voice sync for avatar is lost if the destination resource is in a region that doesn't support voice sync for avatar.

## Pricing

Voice sync for avatar is charged at the same rate as personal voice for both voice creation and synthesis. Voice storage is free.

## Other voice options for custom avatar

- **Standard voice** – A rich selection of out-of-the-box voices, including HD voices and neural voices. See [Text to speech supported languages](../language-support.md).
- **Professional voice** – A premium custom voice that sounds highly natural for your characters. It requires a relatively large amount of training data. See [Custom voice](../custom-neural-voice.md)
- **Personal voice** – A custom voice trained from a short audio recording that supports multiple languages. See [Personal voice](../personal-voice-overview.md).

Both professional voice and personal voice require limited access and are trained through a separate process. These voices can be used independently of the custom video avatar.
