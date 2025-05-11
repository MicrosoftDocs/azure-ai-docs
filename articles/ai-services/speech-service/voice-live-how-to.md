---
title: How to use the Voice Live API (Preview)
titleSuffix: Azure AI services
description: Learn how to use the Voice Live API for real-time voice conversation.
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 5/19/2025
ms.custom: references_regions
# Customer intent: As a developer, I want to learn how to use the Voice Live API for real-time voice conversation.
---

# How to use the Voice Live API (Preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The Voice Live API provides a capable WebSocket interface compared to the [Azure OpenAI Realtime API](../openai/how-to/realtime-audio.md). 

Unless otherwise noted, the Voice Live API uses the same events as the [Azure OpenAI Realtime API](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context). This document provides a reference for the event message properties that are specific to the Voice Live API.

## Supported models and regions

The Voice Live API supports the following models and regions:

| Model | Description | Supported regions |
| ------------------------------ | ----------- | ----------- |
| `gpt-4o-realtime-preview`      | GPT-4o realtime + option to use Azure text to speech voices including custom neural voice for audio. | `eastus2`<br/>`swedencentral` |
| `gpt-4o-mini-realtime-preview` | GPT-4o mini realtime + option to use Azure text to speech voices including custom neural voice for audio. | `eastus2`<br/>`swedencentral` |
| `gpt-4o` | GPT-4o + audio input through Azure speech to text + audio output through Azure text to speech voices including custom neural voice. | `centralindia`<br/>`eastus2`<br/>`swedencentral`<br/>`westus2` |
| `gpt-4o-mini` | GPT-4o mini + audio input through Azure speech to text + audio output through Azure text to speech voices including custom neural voice. | `centralindia`<br/>`eastus2`<br/>`swedencentral`<br/>`westus2` |
| `phi4-mm-realtime` | Phi4-mm + audio output through Azure text to speech voices including custom neural voice. | `centralindia`<br/>`eastus2`<br/>`swedencentral`<br/>`westus2` |
| `phi4` | Phi4-mm + audio input through Azure speech to text + audio output through Azure text to speech voices including custom neural voice. | `centralindia`<br/>`eastus2`<br/>`swedencentral`<br/>`westus2` |

## Authentication

An [Azure AI Foundry resource](../multi-service-resource.md) is required to access the Voice Live API. 

### WebSocket endpoint

The WebSocket endpoint for the Voice Live API is `wss://<your-ai-foundry-resource-name>.cognitiveservices.azure.com/voice-agent/realtime?api-version=2025-05-01-preview`.
The endpoint is the same for all models. The only difference is the required `model` query parameter.

For example, an endpoint for a resource with a custom domain would be `wss://<your-ai-foundry-resource-name>.cognitiveservices.azure.com/voice-agent/realtime?api-version=2025-05-01-preview&model=gpt-4o-mini-realtime-preview`

### Credentials

The Voice Live API supports two authentication methods:

- **Microsoft Entra** (recommended): Use token-based authentication for an Azure AI Foundry resource. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the prehandshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.

For the recommended keyless authentication with Microsoft Entra ID, you need to:

- Assign the `Cognitive Services User` role to your user account or a managed identity. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.
- Generate a token using the Azure CLI or Azure SDKs. The token must be generated with the `https://cognitiveservices.azure.com/.default` scope.
- Use the token in the `Authorization` header of the WebSocket connection request, with the format `Bearer <token>`.

## Session configuration

Often, the first event sent by the caller on a newly established Voice Live API session is the [`session.update`](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context#realtimeclienteventsessionupdate) event. This event controls a wide set of input and output behavior, with output and response generation properties then later overridable using the [`response.create`](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context#realtimeclienteventresponsecreate) event.

Here's an example `session.update` message that configures several aspects of the session, including turn detection, input audio processing, and voice output. Most session parameters are optional and can be omitted if not needed.

```json
{
    "turn_detection": {
        "type": "azure_semantic_vad",
        "threshold": 0.3,
        "prefix_padding_ms": 200,
        "silence_duration_ms": 200,
        "remove_filler_words": false,
        "end_of_utterance_detection": {
            "model": "semantic_detection_v1",
            "threshold": 0.1,
            "timeout": 4,
        },
    },
    "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
    "input_audio_echo_cancellation": {"type": "server_echo_cancellation"},
    "voice": {
        "name": "en-US-Aria:DragonHDLatestNeural",
        "type": "azure-standard",
        "temperature": 0.8,
    },
}
```

The server responds with a [`session.updated`](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context#realtimeservereventsessionupdated) event to confirm the session configuration.

## Session Properties

The following sections describe the properties of the `session` object that can be configured in the `session.update` message. 

> [!TIP]
> For comprehensive descriptions of supported events and properties, see the [Azure OpenAI Realtime API events reference documentation](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context). This document provides a reference for the event message properties that are enhancements via the Voice Live API. 

### Input audio properties

You can use input audio properties to configure the input audio stream.

| Property | Type | Required or optional | Description |
|----------|----------|----------|------------|
| `input_audio_sampling_rate` | integer  | Optional | The sampling rate of the input audio.<br/><br/>The supported values are `16000` and `24000`. The default value is `24000`. |
| `input_audio_echo_cancellation` | object   | Optional | Enhances the input audio quality by removing the echo from the model's own voice without requiring any client-side echo cancellation.<br/><br/>Set the `type` property of `input_audio_echo_cancellation` to enable echo cancellation.<br/><br/>The supported value for `type` is `server_echo_cancellation` which is used when the model's voice is played back to the end-user through a speaker, and the microphone picks up the model's own voice.  |
| `input_audio_noise_reduction`   | object   | Optional | Enhances the input audio quality by suppressing or removing environmental background noise.<br/><br/>Set the `type` property of `input_audio_noise_reduction` to enable noise suppression.<br/><br/>The supported value for `type` is `azure_deep_noise_suppression` which optimizes for speakers closest to the microphone. |

Here's an example of input audio properties is a session object: 

```json
{
    "input_audio_sampling_rate": 24000,
    "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
    "input_audio_echo_cancellation": {"type": "server_echo_cancellation"},
}
```

#### Noise suppression and echo cancellation

Noise suppression enhances the input audio quality by suppressing or removing environmental background noise. Noise suppression helps the model understand the end-user with higher accuracy and improves accuracy of signals like interruption detection and end-of-turn detection.

Server echo cancellation enhances the input audio quality by removing the echo from the model's own voice without requiring any client-side echo cancellation. Server echo cancellation is useful when the model's voice is played back to the end-user through a speaker, and the microphone picks up the model's own voice.

> [!NOTE]
> The service assumes the client plays response audio as soon as it receives them. If playback is delayed for more than 3 seconds, echo cancellation quality is impacted.

```json
{
    "session": {
        "input_audio_noise_reduction": {
            "type": "azure_deep_noise_suppression"
        },
        "input_audio_echo_cancellation": {
            "type": "server_echo_cancellation"
        }
    }
}
```

### Turn Detection Parameters

Turn detection is the process of detecting when the end-user started or stopped speaking. The Voice Live API provides a `turn_detection` property to configure turn detection. The `azure_semantic_vad` type is one differentiator between the Voice Live API and the Azure OpenAI Realtime API. 

| Property | Type | Required or optional | Description |
|----------|----------|----------|------------|
| `type` | string   | Optional | The type of turn detection system to use. Type `server_vad` detects start and end of speech based on audio volume.<br/><br/>Type `azure_semantic_vad` detects start and end of speech based on semantic meaning. The `azure_semantic_vad` type is only available when using the `gpt-4o` model. Azure semantic voice activity detection (VAD) improves turn detection by removing filler words to reduce the false alarm rate. The current list of filler words are `['ah', 'umm', 'mm', 'uh', 'huh', 'oh', 'yeah', 'hmm']`. The service ignores these words when there's an ongoing response. Remove feature words feature assumes the client plays response audio as soon as it receives them.<br/><br/>The default value is `server_vad`. |
| `threshold` | number | Optional | A higher threshold requires a higher confidence signal of the user trying to speak. |
| `prefix_padding_ms` | integer | Optional  | The amount of audio, measured in milliseconds, to include before the start of speech detection signal. |
| `silence_duration_ms` | integer  | Optional | The duration of user's silence, measured in milliseconds, to detect the end of speech. |
| `end_of_utterance_detection` | object | Optional | Configuration for end of utterance detection. The Voice Live API offers advanced end-of-turn detection to indicate when the end-user stopped speaking while allowing for natural pauses. End of utterance detection can significantly reduce premature end-of-turn signals without adding user-perceivable latency. End of utterance detection is only available when using `azure_semantic_vad`.<br/><br/>Properties of `end_of_utterance_detection` include:<br/>-`model`: The model to use for end of utterance detection. The supported value is `semantic_detection_v1`.<br/>- `threshold`: Threshold to determine the end of utterance (0.0 to 1.0). The default value is 0.1.<br/>- `timeout`: Timeout in seconds. The default value is 4 seconds.|

Here's an example of end of utterance detection in a session object:

```json
{
    "session": {
        "turn_detection": {
            "type": "azure_semantic_vad",
            "threshold": 0.3,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 500,
            "remove_filler_words": false,
            "end_of_utterance_detection": {
                "model": "semantic_detection_v1",
                "threshold": 0.1,
                "timeout": 4
            }
        }
    }
}
```

### Audio output through Azure text to speech

You can use the `voice` parameter to specify a prebuilt or custom voice. The voice is used for audio output. 

The `voice` object has the following properties:

| Property | Type | Required or optional | Description |
|----------|----------|----------|------------|
| `name` | string   | Required | Specifies the name of the voice. For example, `en-US-AriaNeural`. |
| `type` | string   | Required | Configuration of the type of Azure voice between `azure-standard` and `azure-custom`. |
| `temperature` | number   | Optional | Specifies temperature applicable to Azure HD voices. Higher values provide higher levels of variability in intonation, prosody, etc. |

#### Azure standard voices

Here's a partial message example for a prebuilt (`azure-standard`) neural voice:

```json
{
  "voice": {
    "name": "en-US-AriaNeural",
    "type": "azure-standard"
  }
}
```

For the full list of prebuilt neural voices, see [Language and voice support for the Speech service](language-support.md?tabs=tts).

#### Azure high definition voices

Here's an example `session.update` message for a neural high definition voice:

```json
{
  "voice": {
    "name": "en-US-Aria:DragonHDLatestNeural",
    "type": "azure-standard",
    "temperature": 0.8 // optional
  }
}
```

For the full list of neural high definition voices, see [high definition voices documentation](high-definition-voices.md#supported-azure-ai-speech-hd-voices).

#### Azure custom neural voices

```json
{
  "voice": {
    "name": "en-US-CustomNeural",
    "type": "azure-custom",
    "endpoint_id": "your-endpoint-id", // a guid string
    "temperature": 0.8 // optional, value range 0.0-1.0, only take effect when using HD voices
  }
}
```

### Azure text to speech avatar

You can use the `avatar` parameter to specify a prebuilt or custom avatar. The avatar is synchronized with the audio output.

An `avatar` parameter can be specified to enable avatar output that is synchronized with the audio output:

```json
{
  "session": {
    "avatar": {
      "character": "lisa",
      "style": "casual-sitting",
      "customized": false,
      "ice_servers": [
        {
          "urls": ["REDACTED"],
          "username": "",
          "credential": ""
        }
      ],
      "video": {
        "bitrate": 2000000,
        "codec": "h264",
        "crop": {
          "top_left": [560, 0],
          "bottom_right": [1360, 1080],
        },
        "resolution": {
          "width": 1080,
          "height": 1920,
        },
        "background": {
          "color": "#00FF00FF"
          // "image_url": "https://example.com/example.jpg"
        }
      }
    }
  }
}
```

The `ice_servers` field is optional. If you don't specify it, the service returns the server-specific ICE servers in `session.updated` response. And you need to use the server-specific ICE servers to generate the local ICE candidates.

Send the client SDP after ICE candidates are gathered.

```json
{
    "type": "session.avatar.connect",
    "client_sdp": "your-client-sdp"
}
```

And the service responds with the server SDP.

```json
{
    "type": "session.avatar.connecting",
    "server_sdp": "your-server-sdp"
}
```

Then you can connect the avatar with the server SDP.

## Conversational enhancements

The Voice Live API offers several conversational enhancements to provide robustness to the natural end-user conversation flow.

### Audio timestamps

When you use Azure voices, and `output_audio_timestamp_types` is configured, the service returns the `response.audio_timestamp.delta` in the response, and `response.audio_timestamp.done` when the all timestamps message are returned.

To configure the audio timestamps, you can set the `output_audio_timestamp_types` in the session.update message.

```json
{
    "session": {
        "output_audio_timestamp_types": ["word"]
    }
}
```

Service returns the audio timestamps in the response when the audio is generated.

```json
{
    "event_id": "<event_id>",
    "type": "response.audio_timestamp.delta",
    "response_id": "<response_id>",
    "item_id": "<item_id>",
    "output_index": 0,
    "content_index": 0,
    "audio_offset_ms": 490,
    "audio_duration_ms": 387,
    "text": "end",
    "timestamp_type": "word"
}
```

And a `response.audio_timestamp.done` message is sent when all timestamps are returned.

```json
{
    "event_id": "<event_id>",
    "type": "response.audio_timestamp.done",
    "response_id": "<response_id>",
    "item_id": "<item_id>",
}
```

### Viseme

You can use Azure standard voice or Azure custom voice with `animation.outputs` set to `{"viseme_id"}`. The service returns the `response.animation_viseme.delta` in the response and `response.animation_viseme.done` when all viseme messages are returned.

To configure the viseme, you can set the `animation.outputs` in the `session.update` message. The `animation.outputs` parameter is optional. It configures which animation outputs should be returned. Currently, it only supports `viseme_id`.

```json
{
  "type": "session.update",
  "event_id": "your-session-id",
  "session": {
    "voice": {
      "name": "en-US-AriaNeural",
      "type": "azure-standard",
    },
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful assistant.",
    "turn_detection": {
        "type": "server_vad"
    },
    "output_audio_timestamp_types": ["word"], // optional
    "animation": {
        "outputs": ["viseme_id"], // optional
    },
  }
}
```

The `output_audio_timestamp_types` parameter is optional. It configures which audio timestamps should be returned for generated audio. Currently, it only supports `word`. 

The service returns the viseme alignment in the response when the audio is generated.

```json
{
    "event_id": "<event_id>",
    "type": "response.animation_viseme.delta",
    "response_id": "<response_id>",
    "item_id": "<item_id>",
    "output_index": 0,
    "content_index": 0,
    "audio_offset_ms": 455,
    "viseme_id": 20
}
```

And a `response.animation_viseme.done` message is sent when all viseme messages are returned.

```json
{
    "event_id": "<event_id>",
    "type": "response.animation_viseme.done",
    "response_id": "<response_id>",
    "item_id": "<item_id>",
}
```

## Related content

- Try out the [Voice Live API quickstart](./voice-live-quickstart.md)
- See the [Azure OpenAI Realtime API reference](/azure/ai-services/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context)
