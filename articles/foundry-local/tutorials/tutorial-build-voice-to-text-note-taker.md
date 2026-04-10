---
title: "Tutorial: Build a voice-to-text note taker"
titleSuffix: Foundry Local
description: Build a note-taking application that transcribes audio files and summarizes them using the Foundry Local SDK. Combines speech-to-text and chat models in one app.
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.topic: tutorial
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 03/29/2026
author: jonburchel
reviewer: samuel100
zone_pivot_groups: foundry-local-sdk
ai-usage: ai-assisted
# CustomerIntent: As a developer, I want to build a note-taking app that transcribes audio and summarizes it so that I can quickly capture and organize spoken content locally.
---

# Tutorial: Build a voice-to-text note taker

Build an application that converts spoken audio into organized notes — entirely on your device. The app first transcribes an audio file using a speech-to-text model, then uses a chat model to summarize and organize the transcription into clean notes.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Set up a project and install the Foundry Local SDK
> * Load a speech-to-text model and transcribe an audio file
> * Load a chat model and summarize the transcription
> * Combine transcription and summarization into a complete app
> * Clean up resources

## Prerequisites

- A Windows, macOS, or Linux computer with at least 8 GB of RAM.
- A `.wav` audio file to transcribe (the tutorial uses a sample file).

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/tutorial-voice-to-text/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/tutorial-voice-to-text/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/tutorial-voice-to-text/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/tutorial-voice-to-text/rust.md)]
::: zone-end

## Clean up resources

The model weights remain in your local cache after you unload a model. This means the next time you run the application, the download step is skipped and the model loads faster. No extra cleanup is needed unless you want to reclaim disk space.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Transcribe audio (speech-to-text)](../how-to/how-to-transcribe-audio.md)
- [Tutorial: Build a multi-turn chat assistant](tutorial-build-chat-assistant.md)
