---
title: Voice assistants overview - Speech service
titleSuffix: Azure AI services
description: An overview of the features, capabilities, and restrictions for voice assistants with the Speech SDK.
author: eric-urban
ms.author: eur
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 3/10/2025
ms.reviewer: travisw
ms.custom: cogserv-non-critical-speech
# Customer intent: As a developer, I want to learn about voice assistants and how to create them by using the Speech SDK.
---

# What is a voice assistant?

By using voice assistants with the Speech service, developers can create natural, human-like, conversational interfaces for their applications and experiences. The voice assistant service provides fast, reliable interaction between a device and an assistant implementation.

## Choose an assistant solution

The first step in creating a voice assistant is to decide what you want it to do. Speech service provides multiple, complementary solutions for crafting assistant interactions. You might want your application to support an open-ended conversation with phrases such as "I need to go to Seattle" or "What kind of pizza can I order?" 

## Reference architecture for building a voice assistant by using the Speech SDK

   ![Conceptual diagram of the voice assistant orchestration service flow.](media/voice-assistants/overview.png)

## Core features

Whether you choose custom keyword or another solution to create your assistant interactions, you can use a rich set of customization features to customize your assistant to your brand, product, and personality.

| Category | Features |
|----------|----------|
|[Custom keyword](./custom-keyword-basics.md) | Users can start conversations with assistants by using a custom keyword such as "Hey Contoso." An app does this with a custom keyword engine in the Speech SDK, which you can configure by going to [Get started with custom keywords](./custom-keyword-basics.md). Voice assistants can use service-side keyword verification to improve the accuracy of the keyword activation (versus using the device alone).
|[Speech to text](speech-to-text.md) | Voice assistants convert real-time audio into recognized text by using [speech to text](speech-to-text.md) from the Speech service. This text is available, as it's transcribed, to both your assistant implementation and your client application.
|[Text to speech](text-to-speech.md) | Textual responses from your assistant are synthesized through [text to speech](text-to-speech.md) from the Speech service. This synthesis is then made available to your client application as an audio stream. Microsoft offers the ability to build your own custom, high-quality Neural Text to speech (Neural TTS) voice that gives a voice to your brand.

## Sample code and tutorials

Sample code for creating a voice assistant is available on [GitHub at Azure-Samples/Cognitive-Services-Voice-Assistant](https://github.com/Azure-Samples/Cognitive-Services-Voice-Assistant). 

## Customization

Voice assistants that you build by using Speech service can use a full range of customization options.

* [Custom speech](./custom-speech-overview.md)
* [Custom voice](professional-voice-create-project.md)
* [Custom Keyword](keyword-recognition-overview.md)

> [!NOTE]
> Customization options vary by language and locale. To learn more, see [Supported languages](language-support.md).

## Related content

* [Learn more about custom keyword](./keyword-recognition-overview.md)
* [Get the Speech SDK](speech-sdk.md)
