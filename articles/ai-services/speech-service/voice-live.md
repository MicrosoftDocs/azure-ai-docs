---
title: Voice Live API Overview
titleSuffix: Foundry Tools
description: Learn about the Voice Live API for real-time voice agents, key scenarios, and pricing so you can choose the right model and start building voice apps.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 01/16/2026
ms.custom: references_regions
# Customer intent: As a developer, I want to learn about the Voice Live API for real-time voice agents.
---

# Voice Live API for real-time voice agents

## What is the Voice Live API?

The Voice Live API is a solution that enables low-latency, high-quality speech-to-speech interactions for voice agents. The API is designed for developers seeking scalable and efficient voice-driven experiences as it eliminates the need to manually orchestrate multiple components. By integrating speech recognition, generative AI, and text-to-speech functionalities into a single, unified interface, it provides an end-to-end solution for creating seamless experiences.

The Voice Live API is fully managed, so you don't need to handle backend orchestration or component integration. Developers provide audio input and receive audio output, avatar visuals, and action triggers—all with minimal latency. You don't need to deploy or manage any generative AI models, as the API handles the underlying infrastructure.


## Understand speech-to-speech experiences

Speech-to-speech technology is revolutionizing how humans interact with systems, offering intuitive voice-based solutions. Traditional implementations involved combining disparate modules such as speech-to-text, dialog management, text-to-speech, and more. Such chaining can lead to increased engineering complexity and end-user perceived latency.

With advancements in large language models (LLMs) and multimodal AI, the Voice Live API consolidates these functionalities, simplifying workflows for developers. This approach enhances real-time interactions and ensures high-quality, natural communication, making it suitable for industries requiring instant, voice-enabled solutions.

## Key scenarios for Voice Live API

Azure AI Voice Live API is ideal for scenarios where voice-driven interactions improve user experience. Examples include:

- **Contact centers**: Develop interactive voice bots for customer support, product catalog navigation, and self-service solutions.
- **Automotive assistants**: Enable hands-free, in-car voice assistants for command execution, navigation, and general inquiries.
- **Education**: Create voice-enabled learning companions and virtual tutors for interactive training and education.
- **Public services**: Build voice agents to assist citizens with administrative queries and public service information.
- **Human resources**: Enhance HR processes with voice-enabled tools for employee support, career development, and training.

## Features of the Voice Live API

The Voice Live API includes a comprehensive set of features to support diverse use cases and ensure superior voice interactions:

- **Broad locale coverage**: Supports over 140 locales for speech to text and offers over 600 standard voices across 150+ locales for text to speech, ensuring global accessibility.
- **Customizable input and output**: Use phrase list for lightweight just-in-time customization on audio input or custom speech models for advanced speech recognition fine-tuning. Use custom voice to create unique, brand-aligned voices for audio output. See [How to customize Voice Live input and output](./voice-live-how-to-customize.md) to learn more.
- **Flexible generative AI model options**: [Choose from multiple models](#supported-models-and-regions), including GPT-5, GPT-4.1, GPT-4o, Phi, and more tailored to conversational requirements.
- **Advanced conversational features**:
    - Noise suppression: Reduces environmental noise for clearer communication.
    - Echo cancellation: Prevents the agent from picking up its own responses.
    - Robust interruption detection: Ensures accurate recognition of interruptions during conversations.
    - Advanced end-of-turn detection: Allows natural pauses without prematurely concluding interactions.
- **Avatar integration**: Provides standard or customizable avatars synchronized with audio output, offering a visual identity for voice agents.
- **Function calling**: Enables external actions, use of tools, and grounded responses using the VoiceRAG pattern.

## API design and compatibility

The Voice Live API is designed for compatibility with the Azure OpenAI Realtime API. The supported real-time events mostly match the [Azure OpenAI Realtime API events](/azure/ai-foundry/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context), with some exceptions described in the [Voice Live API how to guide](./voice-live-how-to.md).

Features that are unique to the Voice Live API are optional and additive. You can add Azure Speech in Foundry Tools capabilities such as noise suppression, echo cancellation, and advanced end-of-turn detection to your existing applications without changing your existing architecture.

The API is supported through WebSocket events, allowing for an easy server-to-server integration. Your backend or middle-tier service connects to the Voice Live API via WebSockets. You can use the WebSocket messages directly to interact with the API.

## Supported models and regions

To power the intelligence of your voice agent, you have flexibility and choice in the generative AI model between GPT-Realtime, GPT-5, GPT-4.1, Phi, and more options. Different generative AI models provide different types of capabilities, levels of intelligence, speed and latency of inferencing, and cost. Depending on what matters most for your business and use case, choose the model that best suits your needs.

All natively supported models are fully managed, so you don't need to deploy models, worry about capacity planning, or provision throughput. Use the model you need, and the Voice Live API takes care of the rest.

The Voice Live API supports the following models. For supported regions, see the [Azure Speech service regions](./regions.md?tabs=voice-live#regions).

| Model | Description |
| ------------------------------ | ----------- |
| `gpt-realtime`      | GPT real-time + option to use Azure text to speech voices including custom voice for audio. |
| `gpt-realtime-mini` | GPT mini real-time + option to use Azure text to speech voices including custom voice for audio. |
| `gpt-4o` | GPT-4o + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4o-mini` | GPT-4o mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4.1` | GPT-4.1 + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-4.1-mini` | GPT-4.1 mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-5` | GPT-5 + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-5-mini` | GPT-5 mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-5-nano` | GPT-5 nano + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `gpt-5-chat` | GPT-5 chat + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |
| `phi4-mm-realtime` | Phi4-mm + audio output through Azure text to speech voices including custom voice. |
| `phi4-mini` | Phi4-mm + audio input through Azure speech to text + audio output through Azure text to speech voices including custom voice. |

## Compare Voice Live API with other speech-to-speech solutions

The Voice Live API is an alternative to orchestrating multiple components such as speech recognition, generative AI, and text to speech. This orchestration can be complex and time-consuming, requiring significant engineering effort to integrate and maintain. The Voice Live API simplifies this process by providing a single interface for all these components. Developers can focus on building their applications rather than managing the underlying infrastructure.

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

Pricing for the Voice Live API takes effect on July 1, 2025.

Pricing for the Voice Live API is tiered (**Pro**, **Basic**, and **Lite**) based on the generative AI model used. You don't select a tier. You choose a generative AI model and the corresponding pricing applies:

| Pricing category | Models |
| ----- | ------ |
| Voice Live pro | `gpt-realtime`, `gpt-4o`, `gpt-4.1`, `gpt-5`, `gpt-5-chat` |
| Voice Live basic | `gpt-realtime-mini`, `gpt-4o-mini`, `gpt-4.1-mini`, `gpt-5-mini` |
| Voice Live lite | `gpt-5-nano`,`phi4-mm-realtime`, `phi4-mini` |

If you choose to use custom speech, custom voice, or custom avatar for your speech input or output, you're charged separately for model training and hosting. Refer to the [Speech Services Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services) for details.

> [!IMPORTANT]
> Custom voice access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

> [!IMPORTANT]
> Custom text to speech avatar access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

### Example pricing scenarios

Here are some example pricing scenarios to help you understand how the Voice Live API is charged:

#### Scenario 1

A customer service agent built with standard Azure Speech input, GPT-4.1, custom Azure Speech output, and a custom avatar.

You're charged at the Voice Live pro rate for:
- Text
- Audio with Azure Speech - Standard
- Audio with Azure Speech - Custom

You're charged separately for the training and model hosting of:
- Custom voice – professional
- Custom avatar

#### Scenario 2

A learning agent built with `gpt-realtime` native audio input and standard Azure Speech output.

You're charged at the Voice Live pro rate for:
- Text
- Native audio with `gpt-realtime`
- Audio with Azure Speech - Standard

#### Scenario 3

A talent interview agent built with `gpt-realtime-mini` native audio input, and standard Azure Speech output and standard avatar.

You're charged at the Voice Live basic rate for:
- Text
- Native audio with `gpt-realtime-mini`
- Audio with Azure Speech - Standard

You're charged separately for:
- Text to speech avatar (standard)

#### Scenario 4

An in-car assistant built with `phi4-mm-realtime` and Azure custom voice.

You're charged at the Voice Live lite rate for:
- Text
- Native audio with `phi4-mm-realtime`

You're charged at the Voice Live pro rate for:
- Audio with Azure Speech - Custom

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
- See the [Voice Live API reference](./voice-live-api-reference-2025-10-01.md)
