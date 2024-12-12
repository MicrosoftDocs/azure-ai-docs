---
title: 'How to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 12/11/2024
author: eric-urban
ms.author: eur
ms.custom: references_regions
recommendations: false
---

# How to use the GPT-4o Realtime API for speech and audio (Preview)

[!INCLUDE [Feature preview](../includes/preview-feature.md)]

Azure OpenAI GPT-4o Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o Realtime API is designed to handle real-time, low-latency conversational interactions. Realtime API is a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of the Realtime API need to deliver and receive audio from an end-user in real time, including applications that use WebRTC or a telephony system. The Realtime API isn't designed to connect directly to end user devices and relies on client integrations to terminate end user audio streams. 

## Supported models

Currently only `gpt-4o-realtime-preview` version: `2024-10-01-preview` supports real-time audio.

The `gpt-4o-realtime-preview` model is available for global deployments in [East US 2 and Sweden Central regions](../concepts/models.md#global-standard-model-availability).

> [!IMPORTANT]
> The system stores your prompts and completions as described in the "Data Use and Access for Abuse Monitoring" section of the service-specific Product Terms for Azure OpenAI Service, except that the Limited Exception does not apply. Abuse monitoring will be turned on for use of the `gpt-4o-realtime-preview` API even for customers who otherwise are approved for modified abuse monitoring.

## API support

Support for the Realtime API was first added in API version `2024-10-01-preview`. 

> [!NOTE]
> For more information about the API and architecture, see the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

## Get started

Before you can use GPT-4o real-time audio, you need:

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>.
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- You need a deployment of the `gpt-4o-realtime-preview` model in a supported region as described in the [supported models](#supported-models) section. You can deploy the model from the [Azure AI Foundry portal model catalog](../../../ai-studio/how-to/model-catalog-overview.md) or from your project in AI Foundry portal. 

For steps to deploy and use the `gpt-4o-realtime-preview` model, see [the real-time audio quickstart](../realtime-audio-quickstart.md).

For more information about the API and architecture, see the remaining sections in this guide.

## Sample code

Right now, the fastest way to get started development with the GPT-4o Realtime API is to download the sample code from the [Azure OpenAI GPT-4o real-time audio repository on GitHub](https://github.com/azure-samples/aoai-realtime-audio-sdk).

[The Azure-Samples/aisearch-openai-rag-audio repo](https://github.com/Azure-Samples/aisearch-openai-rag-audio) contains an example of how to implement RAG support in applications that use voice as their user interface, powered by the GPT-4o realtime API for audio.

## Connection and authentication

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. 

> [!IMPORTANT]
> Device details like capturing and rendering audio data are outside the scope of the Realtime API. It should be used in the context of a trusted, intermediate service that manages both connections to end users and model endpoint connections. Don't use it directly from untrusted end user devices.

The Realtime API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

You can construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol
- Your Azure OpenAI resource endpoint hostname, for example, `my-aoai-resource.openai.azure.com`
- The `openai/realtime` API path
- An `api-version` query string parameter for a supported API version such as `2024-10-01-preview`
- A `deployment` query string parameter with the name of your `gpt-4o-realtime-preview` model deployment

The following example is a well-constructed `/realtime` request URI:

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/realtime?api-version=2024-10-01-preview&deployment=gpt-4o-realtime-preview-deployment-name
```

To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI Service resource with managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the prehandshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.

## Realtime API architecture

Once the WebSocket connection session to `/realtime` is established and authenticated, the functional interaction takes place via events for sending and receiving WebSocket messages. These events each take the form of a JSON object. Events can be sent and received in parallel and applications should generally handle them both concurrently and asynchronously.

- A caller establishes a connection to `/realtime`, which starts a new `session`.
- A `session` automatically creates a default `conversation`. Multiple concurrent conversations aren't supported.
- The `conversation` accumulates input signals until a `response` is started, either via a direct event by the caller or automatically by voice-activity-based (VAD) turn detection.
- Each `response` consists of one or more `items`, which can encapsulate messages, function calls, and other information.
- Each message `item` has `content_part`, allowing multiple modalities (text and audio) to be represented across a single item.
- The `session` manages configuration of caller input handling (for example, user audio) and common output generation handling.
- Each caller-initiated `response.create` can override some of the output `response` behavior, if desired.
- Server-created `item` and the `content_part` in messages can be populated asynchronously and in parallel. For example, receiving audio, text, and function information concurrently in a round robin fashion.

## Session configuration and turn handling mode

Often, the first event sent by the caller on a newly established `/realtime` session is a `session.update` payload. This event controls a wide set of input and output behavior, with output and response generation portions then later overridable via `response.create` properties.

One of the key session-wide settings is `turn_detection`, which controls how data flow is handled between the caller and model:

- `server_vad` evaluates incoming user audio (as sent via `input_audio_buffer.append`) using a voice activity detector (VAD) component and automatically use that audio to initiate response generation on applicable conversations when an end of speech is detected. Silence detection for the VAD can be configured when specifying `server_vad` detection mode.
- `none` relies on caller-initiated `input_audio_buffer.commit` and `response.create` events to progress conversations and produce output. This setting is useful for push-to-talk applications or situations that have external audio flow control (such as caller-side VAD component). These manual signals can still be used in `server_vad` mode to supplement VAD-initiated response generation.

Transcription of user input audio is opted into via the `input_audio_transcription` property. Specifying a transcription model (`whisper-1`) in this configuration enables the delivery of `conversation.item.audio_transcription.completed` events.

### Session update example

An example `session.update` that configures several aspects of the session, including tools, follows. All session parameters are optional; not everything needs to be configured!

```json
{
  "type": "session.update",
  "session": {
    "voice": "alloy",
    "instructions": "Call provided tools if appropriate for the user's input.",
    "input_audio_format": "pcm16",
    "input_audio_transcription": {
      "model": "whisper-1"
    },
    "turn_detection": {
      "threshold": 0.4,
      "silence_duration_ms": 600,
      "type": "server_vad"
    },
    "tools": [
      {
        "type": "function",
        "name": "get_weather_for_location",
        "description": "gets the weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state e.g. San Francisco, CA"
            },
            "unit": {
              "type": "string",
              "enum": [
                "c",
                "f"
              ]
            }
          },
          "required": [
            "location",
            "unit"
          ]
        }
      }
    ]
  }
}
```


## Related content

* Try the [real-time audio quickstart](../realtime-audio-quickstart.md)
* See the [Realtime API reference](../realtime-audio-reference.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
