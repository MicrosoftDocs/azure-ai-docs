---
title: Voice Live API overview
titleSuffix: Azure AI services
description: Learn about the Voice Live API for real-time voice agents.
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 7/1/2025
ms.custom: references_regions
# Customer intent: As a developer, I want to learn about the Voice Live API for real-time voice agents.
---

# Voice Live API for real-time voice agents (Preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

## What is the Voice Live API?

The Voice Live API is a solution enabling low-latency, high-quality speech to speech interactions for voice agents. The API is designed for developers seeking scalable and efficient voice-driven experiences as it eliminates the need to manually orchestrate multiple components. By integrating speech recognition, generative AI, and text to speech functionalities into a single, unified interface, it provides an end-to-end solution for creating seamless experiences.

## Understanding speech to speech experiences

Speech to speech technology is revolutionizing how humans interact with systems, offering intuitive voice-based solutions. Traditional implementations involved combining disparate modules such as speech to text, intent recognition, dialog management, text to speech, and more. Such chaining can lead to increased engineering complexity and end-user perceived latency.

With advancements in Large Language Models (LLMs) and multimodal AI, the Voice Live API consolidates these functionalities, simplifying workflows for developers. This approach enhances real-time interactions and ensures high-quality, natural communication, making it suitable for industries requiring instant, voice-enabled solutions.

## Key Scenarios for Voice Live API

Azure AI Voice Live API is ideal for scenarios where voice-driven interactions improve user experience. Examples include:

- **Contact centers**: Develop interactive voice bots for customer support, product catalog navigation, and self-service solutions.
- **Automotive assistants**: Enable hands-free, in-car voice assistants for command execution, navigation, and general inquiries.
- **Education**: Create voice-enabled learning companions and virtual tutors for interactive training and education.
- **Public services**: Build voice agents to assist citizens with administrative queries and public service information.
- **Human resources**: Enhance HR processes with voice-enabled tools for employee support, career development, and training.

## Features of the Voice Live API

The Voice Live API includes a comprehensive set of features to support diverse use cases and ensure superior voice interactions:

- **Broad locale coverage**: Supports over 15 locales for speech to text and offers over 600 standard voices across 140+ locales for text to speech, ensuring global accessibility.
- **Customizable input and output**: Use phrase list for lightweight just-in-time customization on audio input. Use custom voice to create unique, brand-aligned voices for audio output.
- **Flexible generative AI model options**: [Choose from multiple models](#supported-models-and-regions), including GPT-4o, GPT-4o-mini, and Phi, tailored to conversational requirements.
- **Advanced conversational features**:
    - Noise suppression: Reduces environmental noise for clearer communication.
    - Echo cancellation: Prevents the agent from picking up its own responses.
    - Robust interruption detection: Ensures accurate recognition of interruptions during conversations.
    - Advanced end-of-turn detection: Allows natural pauses without prematurely concluding interactions.
- **Avatar integration**: Provides standard or customizable avatars synchronized with audio output, offering a visual identity for voice agents.
- **Function calling**: Enables external actions, use of tools, and grounded responses using the VoiceRAG pattern.

## How it works

The Voice Live API is fully managed, eliminating the need for customers to handle backend orchestration or component integration. Developers provide audio input and receive audio output, avatar visuals, and action triggers—all with minimal latency. You don't need to deploy or manage any generative AI models, as the API handles all the underlying infrastructure.

## API design and compatibility

The Azure AI Voice Live API is designed for compatibility with the Azure OpenAI Realtime API. The supported real-time events are mostly in parity with the [Azure OpenAI Realtime API events](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context), with some exceptions as described in the [Voice Live API how to guide](./voice-live-how-to.md).

Features that are unique to the Voice Live API are designed to be optional and additive. You can add Azure AI Speech capabilities such as noise suppression, echo cancellation, and advanced end-of-turn detection to your existing applications without needing to change your existing architecture. 

The API is supported through WebSocket events, allowing for an easy server-to-server integration. Your backend or middle-tier service connects to the Voice Live API via WebSockets. You can use the WebSocket messages directly to interact with the API.

## Supported models and regions

To power the intelligence of your voice agent, you have flexibility and choice in the generative AI model between GPT-4o, GPT-4o-mini, and Phi. Different generative AI models provide different types of capabilities, levels of intelligence, speed/latency of inferencing, and cost. Depending on what matters most for your business and use case, you can choose the model that best suits your needs.

All natively supported models – GPT-4o, GPT-4o-mini, and Phi – are fully managed, meaning you don’t have to deploy models, worry about capacity planning, or provisioning throughputs. You can use the model you need, and the Voice Live API takes care of the rest.

The Voice Live API supports the following models. For supported regions, see the [Azure AI Speech service regions](./regions.md?tabs=voice-live#regions).

| Model | Description |
| ------------------------------ | ----------- |
| `gpt-4o-realtime-preview`      | GPT-4o real-time + option to use Azure text to speech voices including custom voice for audio. |
| `gpt-4o-mini-realtime-preview` | GPT-4o mini real-time + option to use Azure text to speech voices including custom voice for audio. |
| `gpt-4o` | GPT-4o + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4o-mini` | GPT-4o mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4.1` | GPT-4.1 + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4.1-mini` | GPT-4.1 mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4.1-nano` | GPT-4.1 nano + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `phi4-mm-realtime` | Phi4-mm + audio output through Azure text to speech voices including custom voice. |
| `phi4-mini` | Phi4-mm + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |


## Comparing Voice Live API with other speech to speech solutions

The Voice Live API is an alternative to orchestrating multiple components such as speech recognition, generative AI, and text to speech. This orchestration can be complex and time-consuming, requiring significant engineering effort to integrate and maintain. The Voice Live API simplifies this process by providing a single interface for all these components, allowing developers to focus on building their applications rather than managing the underlying infrastructure.

To meet your requirements, you can either build your own solution or use the Voice Live API. This table compares the approaches:

| Application requirement | Do it yourself | Voice Live API |
|-----|-----|-----|
| Broad locale coverage with high accuracy (audio input) | ✅ | ✅ |
| Maintain brand and character personality (audio output) | ✅ | ✅ |
| Conversational enhancements | ❌ | ✅ |
| Choice of generative AI models | ✅ | ✅ |
| Visual output with text to speech avatar | ✅ | ✅ |
| Low engineering cost | ❌ | ✅ |
| Low latency perceived by end user | ❌ | ✅ |

## Pricing

Pricing for the Voice Live API is in effect from July 1, 2025. 

Pricing for the Voice Live API is tiered (**Pro**, **Basic**, and **Lite**) based on the generative AI model used.

You don't select a tier. You choose a generative AI model and the corresponding pricing applies.

| Pricing category | Models |
| ----- | ------ |
| Voice Live Pro | `gpt-4o-realtime-preview`, `gpt-4o`, `gpt-4.1` |
| Voice Live Basic | `gpt-4o-mini-realtime-preview`, `gpt-4o-mini`, `gpt-4.1-mini` |
| Voice Live Lite | `gpt-4.1-nano`, `phi4-mm-realtime`, `phi4-mini` |

If you choose to use custom voice for your speech output, you are charged separately for custom voice model training and hosting. Refer to the [Text to Speech – Custom Voice – Professional](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services) pricing for details. Custom voice is a limited access feature. [Learn more about how to create custom voices.](https://aka.ms/CNVPro)

Avatars are charged separately with [the interactive avatar pricing published here.](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services)  

For more details regarding how custom voice and avatar training charges, [refer to this pricing note.](/azure/ai-services/speech-service/text-to-speech#model-training-and-hosting-time-for-custom-voice) 

### Example pricing scenarios

Here are some example pricing scenarios to help you understand how the Voice Live API is charged:

#### Scenario 1

A customer service agent built with standard Azure AI Speech input, GPT-4.1, custom Azure AI Speech output, and a custom avatar.  

You're charged at the Voice Live Pro rate for:
- Text
- Audio with Azure AI Speech - Standard 
- Audio with Azure AI Speech - Custom

You're charged separately for the training and model hosting of:
- Custom voice – professional
- Custom avatar

#### Scenario 2

A learning agent built with `gpt-4o-realtime-preview` native audio input and standard Azure AI Speech output. 

You're charged at the Voice Live Pro rate for:
- Text
- Native audio with `gpt-4o-realtime-preview`
- Audio with Azure AI Speech - Standard

#### Scenario 3

A talent interview agent built with `gpt-4o-mini-realtime-preview` native audio input, and standard Azure AI Speech output and standard avatar. 

You're charged at the Voice Live Basic rate for:
- Text
- Native audio with `gpt-4o-mini-realtime-preview`
- Audio with Azure AI Speech - Standard

You're charged separately for:
- Text to speech avatar (standard)

#### Scenario 4

An in-car assistant built with `phi4-mm-realtime` and Azure custom voice.  

You're charged at the Voice Live Lite rate for:
- Text
- Native audio with `phi4-mm-realtime`

You're charged at the Voice Live Pro rate for:
- Audio with Azure AI Speech - Custom

You're charged separately for the training and model hosting of:
- Custom voice – professional

### Token usage and cost estimation

Tokens are the units that generative AI models use to process input and generate output. 

You can estimate token usage for different model families with the Voice Live API based on audio length. The following token calculations apply to each model family:

| Model family | Input audio (tokens per second) | Output audio (tokens per second) |
| ----- | ----- | ----- |
| Azure OpenAI models | ~10 tokens | ~20 tokens |
| Phi models | ~12.5 tokens | ~20 tokens |

You're also charged for cached audio and text inputs, including the prompt and the context of the conversations. 

## Related content

- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- Try out the [Voice Live API quickstart](./voice-live-quickstart.md)
- See the [audio events reference](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context)
