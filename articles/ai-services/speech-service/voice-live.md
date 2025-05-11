---
title: Voice Live API overview
titleSuffix: Azure AI services
description: Learn about the Voice Live API and how to use it for real-time voice conversation.
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 5/19/2025
# Customer intent: As a developer, I want to learn about the Voice Live API and how to use it for real-time voice conversation.
---

# Voice Live API for real-time voice conversation (Preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

## What is the Voice Live API?

The Voice Live API is a solution enabling low-latency, high-quality speech to speech interactions for voice agents. The API is designed for developers seeking scalable and efficient voice-driven experiences as it eliminates the need to manually orchestrate multiple components. By integrating speech recognition, generative AI, and text to speech functionalities into a single, unified interface, it provides an end-to-end solution for creating seamless experiences.

## Understanding speech to speech Experiences

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

- **Broad locale coverage**: Supports over 15 locales for speech to text and offers over 600 prebuilt voices across 140+ locales for text to speech, ensuring global accessibility.
- **Customizable input and output**: Use customized speech recognition models for domain-specific recognition and phrase list for lightweight just-in-time customization on audio input, and Custom Neural Voice to create unique, brand-aligned voices for audio output.
- **Flexible generative AI model options**: Choose from multiple models, including GPT-4o, GPT-4o-mini, and Phi, tailored to conversational requirements.
- **Advanced conversational features**:
    - Noise suppression: Reduces environmental noise for clearer communication.
    - Echo cancellation: Prevents the agent from picking up its own responses.
    - Robust interruption detection: Ensures accurate recognition of interruptions during conversations.
    - Advanced end-of-turn detection: Allows natural pauses without prematurely concluding interactions.
- **Avatar integration**: Provides prebuilt or customizable avatars synchronized with audio output, offering a visual identity for voice agents.
- **Function calling**: Enables external actions, use of tools, and grounded responses using the VoiceRAG pattern.

## How it works

The Voice Live API is fully managed, eliminating the need for customers to handle backend orchestration or component integration. Developers provide audio input and receive audio output, avatar visuals, and action triggers—all with minimal latency. You don't need to deploy or manage any generative AI models, as the API handles all the underlying infrastructure.

## API design and compatibility

The Azure AI Voice Live API is designed for compatibility with the Azure OpenAI Realtime API. The supported real-time events are mostly in parity with the [Azure OpenAI Realtime API events](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context), with some exceptions. See the [Voice Live API how to guide](./voice-live-how-to.md) for more details.

Features that are unique to the Voice Live API are designed to be optional and additive. You can add Azure AI Speech capabilities such as noise suppression, echo cancellation, and advanced end-of-turn detection to your existing applications without needing to change your existing architecture. 

The API is supported through WebSocket events, allowing for an easy server-to-server integration. Your backend or middle-tier service connects to the Voice Live API via WebSockets. You can use the WebSocket messages directly to interact with the API.

## Models supported natively

To power the intelligence of your voice agent, you have flexibility and choice in the generative AI model between GPT-4o, GPT-4o-mini, and Phi. Different generative AI models provide different types of capabilities, levels of intelligence, speed/latency of inferencing, and cost. Depending on what matters most for your business and use case, you can choose the model that best suits your needs.

All natively supported models – GPT-4o, GPT-4o-mini, and Phi – are fully managed, meaning you don’t have to deploy models, worry about capacity planning, or provisioning throughputs. You can simply use the model you need, and the Voice Live API takes care of the rest.

## Comparing Voice Live API with other speech to speech solutions

| Application requirement | Do it yourself | Speech real-time | Voice Live API |
|-----|-----|-----|-----|
| Broad locale coverage with high accuracy (audio input) | ✅ | ❌ | ✅ |
| Maintain brand and character personality (audio output) | ✅ | ❌ | ✅ |
| Conversational enhancements | ❌ | ✅ | ✅ |
| Choice of generative AI models | ✅ | ❌ | ✅ |
| Visual output with text to speech avatar | ✅ | ❌ | ✅ |
| Low engineering cost | ❌ | ✅ | ✅ |
| Low latency perceived by end user | ❌ | ✅ | ✅ |

## Related content

- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- Try out the [Voice Live API quickstart](./voice-live-quickstart.md)
- See the [Azure OpenAI Realtime API reference](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context)
