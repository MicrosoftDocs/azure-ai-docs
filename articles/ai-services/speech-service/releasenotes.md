---
title: What's new - Speech service
titleSuffix: Foundry Tools
description: Discover the latest updates, features, and improvements in Azure Speech in Foundry Tools, including SDK, CLI, and service releases.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: release-notes
ms.date: 11/21/2025
ms.custom: references_regions
# Customer intent: As a developer, I want to learn about new releases and features for Azure Speech in Foundry Tools.
---

# What's new in Azure Speech in Foundry Tools?

Azure Speech is updated on an ongoing basis. To stay up-to-date with recent developments, this article provides you with information about new releases and features.

## Recent highlights

* LLM speech API is public preview now. It uses a large-language-model-enhanced speech model that delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It currently supports the following speech tasks:
   - `transcribe`: Convert pre-recorded audio into text.
   - `translate`: Convert pre-recorded audio into text in a specified target language.

  For more information, see [LLM speech](./llm-speech.md). 

* Voice live API is generally available. Transform conversations into seamless experiences with Voice live API—the all-in-one solution that combines speech recognition, generative AI, and text-to-speech into a single low-latency interface for building intelligent voice agents. For more information, see [Voice live](./voice-live.md).
* To transcribe multi-lingual contents continuously and accurately in an audio file, you can now use the latest multi-lingual model without specifying the locale codes via fast transcription API. For more information, see [multi-lingual transcription in fast transcription](fast-transcription-create.md?tabs=multilingual-transcription-on).
* Fast transcription is generally available. It can transcribe audio much faster than the actual audio duration. For more information, see the [fast transcription API guide](fast-transcription-create.md).
* Azure Speech Toolkit extension is now available for Visual Studio Code users. It contains a list of speech quick-starts and scenario samples that can be easily built and run with simple clicks. For more information, see [Azure Speech Toolkit in Visual Studio Code Marketplace](https://aka.ms/speech-toolkit-vscode).
* Azure speech high definition (HD) voices are available in public preview. The HD voices can understand the content, automatically detect emotions in the input text, and adjust the speaking tone in real-time to match the sentiment. For more information, see [What are Azure Speech high definition (HD) voices?](high-definition-voices.md).
* Video translation is now available in the Azure Speech service. For more information, see [What is video translation?](./video-translation-overview.md).
* Speech services are now available in three new regions: *Canada East*, *Italy North* and *UK West*. For more information, see [Speech service supported regions](./regions.md).

## Release notes

**Choose a service or resource**

# [SDK](#tab/speech-sdk)

[!INCLUDE [speech-sdk](./includes/release-notes/release-notes-sdk.md)]

# [CLI](#tab/speech-cli)

[!INCLUDE [speech-cli](./includes/release-notes/release-notes-cli.md)]

# [Text to speech service](#tab/text-to-speech)

[!INCLUDE [text to speech](./includes/release-notes/release-notes-tts.md)]

# [Speech to text service](#tab/speech-to-text)

[!INCLUDE [speech to text](./includes/release-notes/release-notes-stt.md)]

# [Containers](#tab/containers)

[!INCLUDE [containers](./includes/release-notes/release-notes-containers.md)]

***
