---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 3/10/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/swift.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Create a keyword in Speech Studio

[!INCLUDE [Create a keyword](use-speech-studio.md)]

## Use a keyword model with the Speech SDK

See the [sample on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/b4257370e1d799f0b8b64be9bf2a34cad8b1a251/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L585) for a complete Objective-C example that demonstrates how to load a custom keyword model (`.table` file) and start keyword recognition on iOS. Although a Swift-specific sample is not currently available, the same workflow and Speech SDK concepts apply when using Swift.

> [!NOTE]
> If you use keyword recognition in an iOS application, newly created keyword models require either the Speech SDK xcframework bundle from [https://aka.ms/csspeech/iosbinaryembedded](https://aka.ms/csspeech/iosbinaryembedded) or the `MicrosoftCognitiveServicesSpeechEmbedded-iOS` pod in your project.