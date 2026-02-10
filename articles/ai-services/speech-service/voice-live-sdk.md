---
title: About the Voice Live SDK - Speech service
titleSuffix: Foundry Tools
description: The Voice Live software development kit (SDK) exposes Azure Voice Live capabilities, making it easier to build low-latency speech-to-speech voice agents.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 01/26/2026
ms.author: pafarley
ai-usage: ai-assisted
#Customer intent: As a developer, I want to learn about the Voice Live SDK.
---

# What is the Voice Live SDK?

The Voice Live software development kit (SDK) exposes [Azure Voice Live](/azure/ai-services/speech-service/voice-live), a managed service that enables low-latency, high-quality speech-to-speech interactions for voice agents. Voice Live consolidates speech recognition, generative AI, and text-to-speech into a single, unified interface, so you can build end-to-end voice experiences with less integration work.

Use the Voice Live SDK to:

- Create real-time voice assistants and conversational agents.
- Build speech-to-speech applications with minimal latency.
- Integrate advanced conversational features like noise suppression and echo cancellation.
- Choose from multiple AI models (for example, GPT-4o, GPT-4o-mini, and Phi) for different use cases.
- Implement function calling and tool integration for dynamic responses.
- Create avatar-enabled voice interactions with visual components.

## Supported languages

The Voice Live SDK supports the following languages and platforms:

| Programming language | Reference | Platform support |
|----------------------|-----------|------------------|
| C# | [C#](/dotnet/api/overview/azure/ai.voicelive-readme?view=foundry) | Windows, Linux, macOS |
| Python | [Python](/python/api/overview/azure/ai-voicelive-readme?view=foundry) | Windows, Linux, macOS|
| Java (preview) | [Java](/java/api/overview/azure/ai-voicelive-readme?view=foundry) | Android, Windows, Linux, macOS |
| JavaScript/TypeScript (preview) | [JavaScript/TypeScript](/javascript/api/overview/azure/ai-voicelive-readme?view=foundry) | Windows, Linux, macOS |

## Code samples

Voice Live SDK code samples are available in the documentation and GitHub.

### Docs samples

At the top of [documentation pages](/azure/ai-services/speech-service/voice-live-quickstart) that contain samples, use the options to select your programming language.

:::image type="content" source="./media/sdk/pivot-programming-languages-speech-sdk.png" alt-text="Screenshot showing how to select a programming language in the documentation.":::

If a sample isn't available in your preferred programming language, select another programming language to get started and learn the concepts, or use the reference and samples linked from the beginning of the article.

### GitHub samples

You can find samples for each programming language in the respective GitHub
repositories.

| Programming language | Samples repository |
|----------------------|--------------------|
| Java | [Java samples](https://aka.ms/voicelive/github-java) |
| Python | [Python samples](https://aka.ms/voicelive/github-python) |
| JavaScript/TypeScript | [JavaScript/TypeScript samples](https://aka.ms/voicelive/github-javascript) |
| C# | [C# samples](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp) |

## Help options

The developer community can use the [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-speech) forums to ask and answer questions about Azure Cognitive Speech and other services. Microsoft monitors the forums and replies to questions that the community didn't yet answer. To make sure that Microsoft sees your question, tag it with `azure-speech`.

You can suggest an idea or report a bug by creating an issue on GitHub.

See also [Foundry Tools support and help options](../cognitive-services-support-options.md?context=/azure/ai-services/speech-service/context/context) to get support, stay up-to-date, give feedback, and report bugs for Foundry Tools.

## Next steps

- [Voice Live overview](/azure/ai-services/speech-service/voice-live?view=foundry)
- [Try the Voice Live API quickstart](./voice-live-quickstart.md)
