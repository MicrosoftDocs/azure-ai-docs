---
title: How to use the Voice Live API
titleSuffix: Foundry Tools
description: Learn how to use the Voice Live API for real-time voice agents.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 11/05/2025
ms.custom: references_regions
# Customer intent: As a developer, I want to learn how to use the Voice Live API for real-time voice agents.
---

# How to use the Voice Live API 

The Voice Live API provides a capable WebSocket interface compared to the [Azure OpenAI Realtime API](../../ai-foundry/openai/how-to/realtime-audio.md).

Unless otherwise noted, the Voice Live API uses the [same events](/azure/ai-foundry/openai/realtime-audio-reference?context=/azure/ai-services/speech-service/context/context) as the Azure OpenAI Realtime API. This document provides a reference for the event message properties that are specific to the Voice Live API.

## Supported models and regions

For a table of supported models and regions, see the [Voice Live API overview](./voice-live.md#supported-models-and-regions).

## Authentication

A [Microsoft Foundry resource](../multi-service-resource.md) or a [Azure Speech in Foundry Tools Services resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices) is required to use the Voice Live API.

> [!NOTE]
> Using Voice Live API is optimized for Microsoft Foundry resources. We recommend using Microsoft Foundry resources for full feature availability and best Microsoft Foundry integration experience.        
> **Azure Speech Services resources** don't support Microsoft Foundry Agent Service integration and bring-your-own-model (BYOM).

### WebSocket endpoint

The WebSocket endpoint for the Voice Live API is `wss://<your-ai-foundry-resource-name>.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01` or, for older resources, `wss://<your-ai-foundry-resource-name>.cognitiveservices.azure.com/voice-live/realtime?api-version=2025-10-01`.
The endpoint is the same for all models. The only difference is the required `model` query parameter, or, when using the Agent service, the `agent_id` and `project_id` parameters.

For example, an endpoint for a resource with a custom domain would be `wss://<your-ai-foundry-resource-name>.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01&model=gpt-realtime`

### Credentials

The Voice Live API supports two authentication methods:

- **Microsoft Entra** (recommended): Use token-based authentication for a Microsoft Foundry resource. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the prehandshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.

For the recommended keyless authentication with Microsoft Entra ID, you need to:

- Assign the `Cognitive Services User` and `Azure AI User` role to your user account or a managed identity. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.
- Generate a token using the Azure CLI or Azure SDKs. The token must be generated with the `https://ai.azure.com/.default` scope, or the legacy `https://cognitiveservices.azure.com/.default` scope.
- Use the token in the `Authorization` header of the WebSocket connection request, with the format `Bearer <token>`.

## Session configuration

Often, the first event sent by the caller on a newly established Voice Live API session is the [`session.update`](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context#realtimeclienteventsessionupdate) event. This event controls a wide set of input and output behavior, with output and response generation properties then later overridable using the [`response.create`](../openai/realtime-audio-reference.md?context=/azure/ai-services/speech-service/context/context#realtimeclienteventresponsecreate) event.

Here's an example `session.update` message that configures several aspects of the session, including turn detection, input audio processing, and voice output. Most session parameters are optional and can be omitted if not needed.

```json
{
    "instructions": "You are a helpful AI assistant responding in natural, engaging language.",
    "turn_detection": {
        "type": "azure_semantic_vad",
        "silence_duration_ms": 500,
    },
    "input_audio_noise_reduction": {"type": "azure_deep_noise_suppression"},
    "input_audio_echo_cancellation": {"type": "server_echo_cancellation"},
    "voice": {
        "name": "en-US-Ava:DragonHDLatestNeural",
        "type": "azure-standard",
        "temperature": 0.8,
    },
}
```

> [!IMPORTANT]
> The `"instructions"` property isn't supported when you're using a custom agent.

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
| `input_audio_echo_cancellation` | object   | Optional | Enhances the input audio quality by removing the echo from the model's own voice without requiring any client-side echo cancellation.<br/><br/>Set the `type` property of `input_audio_echo_cancellation` to enable echo cancellation.<br/><br/>The supported value for `type` is `server_echo_cancellation`, which is used when the model's voice is played back to the end-user through a speaker, and the microphone picks up the model's own voice.  |
| `input_audio_noise_reduction`   | object   | Optional | Enhances the input audio quality by suppressing or removing environmental background noise.<br/><br/>Set the `type` property of `input_audio_noise_reduction` to enable noise suppression.<br/><br/>The supported value for `type` is `azure_deep_noise_suppression`, which optimizes for speakers closest to the microphone.<br/><br/>You can set this property to `near_field` or `far_field` if you're using the [Azure OpenAI Realtime API](../../ai-foundry/openai/realtime-audio-reference.md#realtimeaudioinputaudionoisereductionsettings). |

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

Server echo cancellation enhances the input audio quality by removing the echo from the model's own voice. In this way, client-side echo cancellation isn't required. Server echo cancellation is useful when the model's voice is played back to the end-user through a speaker. This helps avoiding the microphone picking up the model's own voice.

> [!NOTE]
> The service assumes the client plays response audio as soon as it receives them. If playback is delayed for more than two seconds, echo cancellation quality is impacted.


## Conversational enhancements

The Voice Live API offers conversational enhancements to provide robustness to the natural end-user conversation flow.

### Turn Detection Parameters

Turn detection is the process of detecting when the end-user started or stopped speaking. The Voice Live API builds on the Azure OpenAI Realtime API `turn_detection` property to configure turn detection. The `azure_semantic_vad` and `azure_multilingual_semantic_vad` types are key differentiators between the Voice Live API and the Azure OpenAI Realtime API.

| Property | Type | Required or optional | Description |
|----------|----------|----------|------------|
| `type` | string   | Optional | The type of turn detection system to use. Type `server_vad` detects start and end of speech based on audio volume.<br/><br/>Type `semantic_vad` uses a semantic classifier to detect when the user has finished speaking, based on the words they have uttered. This type can only be used with the *gpt-realtime* and *gpt-realtime-mini* models.<br/><br/>Type `azure_semantic_vad` and `azure_semantic_vad_multilingual` also detects start and end of speech based on semantic meaning and can be used with *all models*. Further Azure semantic voice activity detection (VAD) can also improve turn detection by removing filler words to reduce the false alarm rate of barge-in.<br/><br/>The default value is `server_vad`. |
| `threshold` | number | Optional | A higher threshold requires a higher confidence signal of the user trying to speak. |
| `prefix_padding_ms` | integer | Optional  | The amount of audio, measured in milliseconds, to include before the start of speech detection signal. |
| `speech_duration_ms` | integer | Optional | The duration of user's speech audio required to start detection. If not set or under 80 ms, the detector uses a default value of 80 ms. |
| `silence_duration_ms` | integer  | Optional | The duration of user's silence, measured in milliseconds, to detect the end of speech. |
| `remove_filler_words` | boolean | Optional | Determines whether to remove filler words to reduce the false alarm rate of barge-in.<br/>To enable it the property must be set to `true`. The detected filler words in English are `['ah', 'umm', 'mm', 'uh', 'huh', 'oh', 'yeah', 'hmm']`. The service ignores these words when there's an ongoing response. Remove filler words feature assumes the client plays response audio as soon as it receives them.<br/>The default value is `false`. |
| `languages` | string[] | Optional | Language will be used to improve the `remove_filler_words` accuracy by reducing the applied languages. The type `azure_semantic_vad` primarily supports English. Type `azure_semantic_vad_multilingual` is also available to support a wider variety of languages: English, Spanish, French, Italian, German (DE), Japanese, Portuguese, Chinese, Korean, Hindi. Other languages will be ignored. |
| `create_response` | boolean | Optional | Enable or disable whether a response is generated. |
| `eagerness` | string | Optional | This is a way to control how eager the model is to interrupt the user, tuning the maximum wait timeout. Only available with type `semantic_vad`. In transcription mode, even if the model doesn't reply, it affects how the audio is chunked.<br/>The following values are allowed:<br/>- `auto` (default) is equivalent to `medium`,<br/>- `low` will let the user take their time to speak,<br/>- `high` will chunk the audio as soon as possible.<br/><br/>If you want the model to respond more often in conversation mode, or to return transcription events faster in transcription mode, you can set eagerness to `high`.<br/>On the other hand, if you want to let the user speak uninterrupted in conversation mode, or if you would like larger transcript chunks in transcription mode, you can set eagerness to `low`. |
| `interrupt_response` | boolean | Optional | Enable or disable barge-in interruption (default: false). Only available with type `azure_semantic_vad` and `azure_semantic_vad_multilingual`. |
| `auto_truncate` | boolean | Optional | Auto-truncate on interruption (default: false). |

## Audio input through Azure speech to text

Azure speech to text is automatically active when you're using a non-multimodal model like gpt-4o.

In order to explicitly configure it, you can set the `model` to `azure-speech` in `input_audio_transcription`. This can be useful to improve the recognition quality for specific language situations. See [How to customize Voice Live input and output](./voice-live-how-to-customize.md) learn more about speech input customization configuration.

```json
{
    "session": {
        "input_audio_transcription": {
            "model": "azure-speech",
            "language": "en"
        }
    }
}
```

## Audio output through Azure text to speech

You can use the `voice` parameter to specify a standard or custom voice. The voice is used for audio output.

The `voice` object has the following properties:

| Property | Type | Required or optional | Description |
|----------|----------|----------|------------|
| `name` | string   | Required | Specifies the name of the voice. For example, `en-US-AvaNeural`. |
| `type` | string   | Required | Configuration of the type of Azure voice between `azure-standard` and `azure-custom`. |
| `temperature` | number   | Optional | Specifies temperature applicable to Azure HD voices. Higher values provide higher levels of variability in intonation, prosody, etc. |

See [How to customize Voice Live input and output](./voice-live-how-to-customize.md) learn more about speech output customization configuration.

### Azure standard voices

Here's a partial message example for a standard (`azure-standard`) voice:

```json
{
  "voice": {
    "name": "en-US-AvaNeural",
    "type": "azure-standard"
  }
}
```

For the full list of standard voices, see [Language and voice support for the Speech service](language-support.md?tabs=tts).

### Azure high definition voices

Here's an example `session.update` message for a standard high definition voice:

```json
{
  "voice": {
    "name": "en-US-Ava:DragonHDLatestNeural",
    "type": "azure-standard",
    "temperature": 0.8 // optional
  }
}
```

For the full list of standard high definition voices, see [high definition voices documentation](high-definition-voices.md#supported-azure-speech-hd-voices).

> [!NOTE]
> High definition voices are currently supported in the following regions only: southeastasia, centralindia, swedencentral, westeurope, eastus, eastus2, westus2

### Speaking rate

Use the `rate` string property to adjust the speaking speed for any standard Azure text to speech voices and custom voices.

The rate value should range from 0.5 to 1.5, with higher values indicating faster speeds.

```json
{
  "voice": {
    "name": "en-US-Ava:DragonHDLatestNeural",
    "type": "azure-standard",
    "temperature": 0.8, // optional
    "rate": "1.2"
  }
}
```

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

A viseme is the visual description of a phoneme in spoken language. It defines the position of the face and mouth while a person is speaking.

You can use Azure standard voice or Azure custom voice with `animation.outputs` set to `{"viseme_id"}`. The service returns the `response.animation_viseme.delta` in the response and `response.animation_viseme.done` when all viseme messages are returned.

> [!TIP]
> For more information about viseme via Speech Synthesis Markup Language (SSML), see [viseme element documentation](speech-synthesis-markup-voice.md#viseme-element).

To configure the viseme, you can set the `animation.outputs` in the `session.update` message. The `animation.outputs` parameter is optional. It configures which animation outputs should be returned. Currently, it only supports `viseme_id`.

```json
{
  "type": "session.update",
  "event_id": "your-session-id",
  "session": {
    "voice": {
      "name": "en-US-AvaNeural",
      "type": "azure-standard",
    },
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful AI assistant responding in natural, engaging language.",
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

## Azure text to speech avatar

[Text to speech avatar](./text-to-speech-avatar/what-is-text-to-speech-avatar.md) converts text into a digital video of a photorealistic human (either a standard avatar or a [custom text to speech avatar](./text-to-speech-avatar/what-is-custom-text-to-speech-avatar.md)) speaking with a natural-sounding voice.

You can use the `avatar` parameter to specify a standard or custom avatar. The avatar is synchronized with the audio output.

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

> [!NOTE]
> Azure text to speech avatar is currently supported in limited regions. For the current list of supported regions, see the [Speech service regions table](./regions.md?tabs=ttsavatar).

## Related content

- Try out the [Voice Live API quickstart](./voice-live-quickstart.md)
- See the [Voice Live API reference](./voice-live-api-reference-2025-10-01.md)
