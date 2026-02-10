---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 3/10/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/objectivec.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Create a keyword in Speech Studio

[!INCLUDE [Create a keyword](use-speech-studio.md)]

## Use a keyword model with the Speech SDK

See the [sample on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/b4257370e1d799f0b8b64be9bf2a34cad8b1a251/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L585) for a complete Objective-C example that demonstrates how to load a custom keyword model (`.table` file), configure the Speech SDK, and start keyword recognition using the device microphone in an iOS app.
