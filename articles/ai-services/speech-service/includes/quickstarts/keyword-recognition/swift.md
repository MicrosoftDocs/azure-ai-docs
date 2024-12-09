---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 9/12/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/swift.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Create a keyword in Speech Studio

[!INCLUDE [Create a keyword](use-speech-studio.md)]

## Use a keyword model with the Speech SDK

See the [sample on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/b4257370e1d799f0b8b64be9bf2a34cad8b1a251/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L585) for using your Custom Keyword model with the Objective C SDK. Although we don't currently have a Swift sample for parity, the concepts are similar.

> [!NOTE]
> If you are going to use keyword recognition in your Swift application on iOS, note that new keyword models created in Speech Studio will require using either the Speech SDK xcframework bundle from [https://aka.ms/csspeech/iosbinaryembedded](https://aka.ms/csspeech/iosbinaryembedded) or the `MicrosoftCognitiveServicesSpeechEmbedded-iOS` pod in your project.
