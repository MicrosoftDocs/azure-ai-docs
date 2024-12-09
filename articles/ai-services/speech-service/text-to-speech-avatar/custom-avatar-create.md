---
title: How to create a custom text to speech avatar - Speech service
titleSuffix: Azure AI services
description: Learn how to create a custom text to speech avatar.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/11/2024
ms.reviewer: v-baolianzou
ms.author: eur
author: eric-urban
---

# How to create a custom text to speech avatar

Getting started with a custom text to speech avatar is a straightforward process. All it takes are a few of video files. If you'd like to train a [custom neural voice](../custom-neural-voice.md) for the same actor, you can do so separately.

## Get consent file from the avatar talent

An avatar talent is an individual or target actor whose video of speaking is recorded and used to create neural avatar models. You must obtain sufficient consent under all relevant laws and regulations from the avatar talent to use their video to create the custom text to speech avatar.

You must provide a video file with a recorded statement from your avatar talent, acknowledging the use of their image and voice. Microsoft verifies that the content in the recording matches the predefined script provided by Microsoft. Microsoft compares the face of the avatar talent in the recorded video statement file with randomized videos from the training datasets to ensure that the avatar talent in video recordings and the avatar talent in the statement video file are from the same person.

You can find the verbal consent statement in multiple languages on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/customavatar/verbal-statement-all-locales.txt). The language of the verbal statement must be the same as your recording. See also the disclosure for voice talent.

For more information about recording the consent video, see [How to record video samples](custom-avatar-record-video-samples.md).

## Prepare training data for custom text to speech avatar

You're required to provide video recordings of the avatar talent speaking in a language of your choice. The video recordings should contain high signal-to-noise ratio voice. The voice in the video recording isn't used as training data for a custom neural voice; its purpose is to train the custom text to speech avatar model.

For more information about preparing the training data, see [How to record video samples](custom-avatar-record-video-samples.md).

## Next steps

* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
* [How to record video samples](custom-avatar-record-video-samples.md)
