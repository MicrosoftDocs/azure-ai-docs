---
title: Voice Live API
titleSuffix: Azure AI services
description: Learn how to use the Voice Live API for real-time voice conversation.
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 5/19/2025
# Customer intent: 
---

# Voice Live API for real-time voice conversation

## What is the Voice Live API?

The Voice Live API is a solution enabling low-latency, high-quality speech-to-speech interactions for voice agents. It's designed for developers seeking scalable and efficient voice-driven experiences as it eliminates the need to manually orchestrate multiple components. By integrating speech recognition, generative AI, and text to speech functionalities into a single, unified interface, it provides an end-to-end solution for creating seamless experiences.

## Understanding Speech-to-Speech Experiences

Speech-to-speech technology is revolutionizing how humans interact with systems, offering intuitive voice-based solutions. Traditional implementations involved combining disparate modules such as speech to text, intent recognition, dialog management, text to speech, and more. Such chaining can lead to increased engineering complexity and end-user perceived latency.

With advancements in Large Language Models (LLMs) and multimodal AI, the Voice Live API consolidates these functionalities, simplifying workflows for developers. This approach enhances real-time interactions and ensures high-quality, natural communication, making it suitable for industries requiring instant, voice-enabled solutions.

## Key Scenarios for Voice Live API

Azure AI Voice Live API is ideal for scenarios where voice-driven interactions improve user experience. Examples include:

- **Contact Centers**: Develop interactive voice bots for customer support, product catalog navigation, and self-service solutions.
- **Automotive Assistants**: Enable hands-free, in-car voice assistants for command execution, navigation, and general inquiries.
- **Education**: Create voice-enabled learning companions and virtual tutors for interactive training and education.
- **Public Services**: Build voice agents to assist citizens with administrative queries and public service information.
- **Human Resources**: Enhance HR processes with voice-enabled tools for employee support, career development, and training.

## Features of the Voice Live API

The Voice Live API includes a comprehensive set of features to support diverse use cases and ensure superior voice interactions:

- **Broad Locale Coverage**: Supports over 15 locales for speech to text and offers over 600 prebuilt voices across 140+ locales for text to speech, ensuring global accessibility.
- **Customizable Input and Output**: Use customized speech recognition models for domain-specific recognition and phrase list for lightweight just-in-time customization on audio input, and Custom Neural Voice to create unique, brand-aligned voices for audio output.
- **Flexible Generative AI Model Options**: Choose from multiple models, including GPT-4o, GPT-4o-mini, and Phi, tailored to conversational requirements.
- **Advanced Conversational Features**:
  - Noise Suppression: Reduces environmental noise for clearer communication.
  - Echo Cancellation: Prevents the agent from picking up its own responses.
  - Robust Interruption Detection: Ensures accurate recognition of interruptions during conversations.
  - Advanced End-of-Turn Detection: Allows natural pauses without prematurely concluding interactions.
- **Avatar Integration**: Provides prebuilt or customizable avatars synchronized with audio output, offering a visual identity for voice agents.
- **Function Calling**: Enables external actions, use of tools, and grounded responses using the VoiceRAG pattern.

## How It Works

The Voice Live API is fully managed, eliminating the need for customers to handle backend orchestration or component integration. Developers provide audio input and receive audio output, avatar visuals, and action triggers—all with minimal latency.

## API Design & Compatibility

The Azure AI Voice Live API is designed with seamless integration in mind, ensuring full compatibility with the Azure OpenAI Realtime API. This unified interface allows developers to effortlessly onboard and use the enhanced features of the Voice Live API. By adding a few more configuration parameters, developers can unlock its advanced capabilities, such as text to speech avatar, without overhauling their existing systems.

## WebSocket Interface

The API is supported through WebSocket events, allowing for an easy server-to-server integration. Your backend or middle-tier service connects to the Voice Live API via WebSockets. You can either use the WebSocket event messages directly to interact with the API, or use our lightweight SDK which is available in JavaScript and Python.

The supported real-time events are mostly in parity with the Azure OpenAI Realtime API, with a few exceptions. See the [Realtime events reference documentation](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context) for more details.

## Models Supported Natively

To power the intelligence of your voice agent, you have flexibility and choice in the GenAI model between GPT-4o, GPT-4o-mini, and Phi. Different GenAI models provide different types of capabilities, levels of intelligence, speed/latency of inferencing, and cost. Depending on what matters most for your business and use case, you can choose the model that best suits your needs.

All natively supported models – GPT-4o, GPT-4o-mini, and Phi – are fully managed, meaning you don’t have to worry about capacity planning, provisioning throughputs, etc.

## Comparing Voice Live API with other Speech Services

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

- [Azure OpenAI Realtime API](../openai/realtime-audio-reference.md)
- [Whisper model](./whisper-overview.md)
