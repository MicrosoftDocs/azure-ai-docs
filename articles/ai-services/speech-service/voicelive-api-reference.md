---
title: Voice Live API Reference
titleSuffix: Azure AI Services
description: Complete reference for the Voice Live API events, models, and configuration options.
manager: nitinme
ms.service: azure-ai-services
ms.topic: reference
ms.date: 9/22/2025
author: goergenj
ms.author: jagoerge
---

# Voice Live API Reference

The Voice Live API provides real-time, bidirectional communication for voice-enabled applications using WebSocket connections. This API supports advanced features including speech recognition, text-to-speech synthesis, avatar streaming, animation data, and comprehensive audio processing capabilities.

The API uses JSON-formatted events sent over WebSocket connections to manage conversations, audio streams, avatar interactions, and real-time responses. Events are categorized into client events (sent from client to server) and server events (sent from server to client).

## Key Features

- **Real-time Audio Processing**: Support for multiple audio formats including PCM16 at various sample rates and G.711 codecs
- **Advanced Voice Options**: OpenAI voices, Azure custom voices, Azure standard voices, and Azure personal voices
- **Avatar Integration**: WebRTC-based avatar streaming with video, animation, and blendshapes
- **Intelligent Turn Detection**: Multiple VAD options including Azure semantic VAD and server-side detection
- **Audio Enhancement**: Built-in noise reduction and echo cancellation
- **Function Calling**: Tool integration for enhanced conversational capabilities
- **Flexible Session Management**: Configurable modalities, instructions, and response parameters

## Client Events

The Voice Live API supports the following client events that can be sent from the client to the server:

| Event | Description |
|-------|-------------|
| [session.update](#realtimeclienteventsessionupdate) | Update the session configuration including voice, modalities, turn detection, and other settings |
| [session.avatar.connect](#sessionavatarconnect) | Establish avatar connection by providing client SDP for WebRTC negotiation |
| [input_audio_buffer.append](#realtimeclienteventinputaudiobufferappend) | Append audio bytes to the input audio buffer |
| [input_audio_buffer.commit](#realtimeclienteventinputaudiobuffercommit) | Commit the input audio buffer for processing |
| [input_audio_buffer.clear](#realtimeclienteventinputaudiobufferclear) | Clear the input audio buffer |
| [conversation.item.create](#conversationitemcreate) | Add a new item to the conversation context |
| [conversation.item.retrieve](#conversationitemretrieve) | Retrieve a specific item from the conversation |
| [conversation.item.truncate](#realtimeclienteventconversationitemtruncate) | Truncate an assistant audio message |
| [conversation.item.delete](#conversationitemdelete) | Remove an item from the conversation |
| [response.create](#realtimeclienteventresponsecreate) | Instruct the server to create a response via model inference |
| [response.cancel](#realtimeclienteventresponsecancel) | Cancel an in-progress response |

### session.update

Update the session's configuration. This event can be sent at any time to modify settings such as voice, modalities, turn detection, tools, and other session parameters. Note that once a session is initialized with a particular model, it can't be changed to another model.

#### Event Structure

```json
{
  "type": "session.update",
  "session": {
    "modalities": ["text", "audio"],
    "voice": {
      "type": "openai",
      "name": "alloy"
    },
    "instructions": "You are a helpful assistant. Be concise and friendly.",
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "input_audio_sampling_rate": 24000,
    "turn_detection": {
      "type": "azure_semantic_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "temperature": 0.8,
    "max_response_output_tokens": "inf"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"session.update"` |
| session | [RealtimeRequestSession](#realtimerequestsession) | Session configuration object with fields to update |

#### Example with Azure Custom Voice

```json
{
  "type": "session.update",
  "session": {
    "voice": {
      "type": "azure-custom",
      "name": "my-custom-voice",
      "endpoint_id": "12345678-1234-1234-1234-123456789012",
      "temperature": 0.7,
      "style": "cheerful"
    },
    "input_audio_noise_reduction": {
      "type": "azure_deep_noise_suppression"
    },
    "avatar": {
      "character": "lisa",
      "customized": false,
      "video": {
        "resolution": {
          "width": 1920,
          "height": 1080
        },
        "bitrate": 2000000
      }
    }
  }
}
```

### session.avatar.connect

Establish an avatar connection by providing the client's SDP (Session Description Protocol) offer for WebRTC media negotiation. This event is required when using avatar features.

#### Event Structure

```json
{
  "type": "session.avatar.connect",
  "client_sdp": "<client_sdp>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"session.avatar.connect"` |
| client_sdp | string | The client's SDP offer for WebRTC connection establishment |

### input_audio_buffer.append

* support event* - Append audio bytes to the input audio buffer. This is maintained for compatibility with OpenAI Realtime API clients. New integrations should use the `input_audio.turn.*` events instead.

#### Event Structure

```json
{
  "type": "input_audio_buffer.append",
  "audio": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"input_audio_buffer.append"` |
| audio | string | Base64-encoded audio data |

### input_audio_buffer.commit

Commit the input audio buffer for processing. This is maintained for compatibility with OpenAI Realtime API clients.

#### Event Structure

```json
{
  "type": "input_audio_buffer.commit"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"input_audio_buffer.commit"` |

### input_audio_buffer.clear

Clear the input audio buffer. This is maintained for compatibility with OpenAI Realtime API clients.

#### Event Structure

```json
{
  "type": "input_audio_buffer.clear"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"input_audio_buffer.clear"` |

### conversation.item.create

Add a new item to the conversation context. This can include messages, function calls, and function call responses. Items can be inserted at specific positions in the conversation history.

#### Event Structure

```json
{
  "type": "conversation.item.create",
  "previous_item_id": "item_ABC123",
  "item": {
    "id": "item_DEF456",
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "Hello, how are you?"
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.create"` |
| previous_item_id | string | Optional. ID of the item after which to insert this item. If not provided, appends to end |
| item | [RealtimeConversationItem](#realtimeconversationitem) | The item to add to the conversation |

#### Example with Audio Content

```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_audio",
        "audio": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=",
        "transcript": "Hello there"
      }
    ]
  }
}
```

#### Example with Function Call

```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "function_call",
    "name": "get_weather",
    "call_id": "call_123",
    "arguments": "{\"location\": \"San Francisco\", \"unit\": \"celsius\"}"
  }
}
```

### conversation.item.retrieve

Retrieve a specific item from the conversation history. This is useful for inspecting processed audio after noise cancellation and VAD.

#### Event Structure

```json
{
  "type": "conversation.item.retrieve",
  "item_id": "item_ABC123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.retrieve"` |
| item_id | string | The ID of the item to retrieve |

### conversation.item.truncate

Truncate an assistant message's audio content. This is useful for stopping playback at a specific point and synchronizing the server's understanding with the client's state.

#### Event Structure

```json
{
  "type": "conversation.item.truncate",
  "item_id": "item_ABC123",
  "content_index": 0,
  "audio_end_ms": 5000
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.truncate"` |
| item_id | string | The ID of the assistant message item to truncate |
| content_index | integer | The index of the content part to truncate |
| audio_end_ms | integer | The duration up to which to truncate the audio, in milliseconds |

### conversation.item.delete

Remove an item from the conversation history.

#### Event Structure

```json
{
  "type": "conversation.item.delete",
  "item_id": "item_ABC123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.delete"` |
| item_id | string | The ID of the item to delete |

### response.create

Instruct the server to create a response via model inference. This event can specify response-specific configuration that overrides session defaults.

#### Event Structure

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["text", "audio"],
    "instructions": "Be extra helpful and detailed.",
    "voice": {
      "type": "openai",
      "name": "alloy"
    },
    "output_audio_format": "pcm16",
    "temperature": 0.7,
    "max_response_output_tokens": 1000
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.create"` |
| response | [RealtimeResponseOptions](#realtimeresponseoptions) | Optional response configuration that overrides session defaults |

#### Example with Tool Choice

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["text"],
    "tools": [
      {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {
          "type": "object",
          "properties": {}
        }
      }
    ],
    "tool_choice": "get_current_time",
    "temperature": 0.3
  }
}
```

#### Example with Animation

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["audio", "animation"],
    "animation": {
      "model_name": "default",
      "outputs": ["blendshapes", "viseme_id"]
    },
    "voice": {
      "type": "azure-custom",
      "name": "my-expressive-voice",
      "endpoint_id": "12345678-1234-1234-1234-123456789012",
      "style": "excited"
    }
  }
}
```

### response.cancel

Cancel an in-progress response. This immediately stops response generation and related audio output.

#### Event Structure

```json
{
  "type": "response.cancel"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.cancel"` |

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.retrieve`. |
| item_id | string | The ID of the item to retrieve. |
| event_id | string | The ID of the event. |

### RealtimeClientEventConversationItemTruncate

The client `conversation.item.truncate` event is used to truncate a previous assistant message's audio. The server produces audio faster than realtime, so this event is useful when the user interrupts to truncate audio that was sent to the client but not yet played. The server's understanding of the audio with the client's playback is synchronized.

Truncating audio deletes the server-side text transcript to ensure there isn't text in the context that the user doesn't know about.

If the client event is successful, the server responds with a `conversation.item.truncated` event.

#### Event structure

```json
{
  "type": "conversation.item.truncate",
  "item_id": "<item_id>",
  "content_index": 0,
  "audio_end_ms": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.truncate`. |
| item_id | string | The ID of the assistant message item to truncate. Only assistant message items can be truncated. |
| content_index | integer | The index of the content part to truncate. Set this property to "0". |
| audio_end_ms | integer | Inclusive duration up to which audio is truncated, in milliseconds. If the audio_end_ms is greater than the actual audio duration, the server responds with an error. |

### RealtimeClientEventInputAudioBufferAppend

The client `input_audio_buffer.append` event is used to append audio bytes to the input audio buffer. The audio buffer is temporary storage you can write to and later commit.

In Server VAD (Voice Activity Detection) mode, the audio buffer is used to detect speech and the server decides when to commit. When server VAD is disabled, the client can choose how much audio to place in each event up to a maximum of 15 MiB. For example, streaming smaller chunks from the client can allow the VAD to be more responsive.

Unlike most other client events, the server doesn't send a confirmation response to client `input_audio_buffer.append` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.append",
  "audio": "<audio>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.append`. |
| audio | string | Base64-encoded audio bytes. This value must be in the format specified by the `input_audio_format` field in the session configuration. |

### RealtimeClientEventInputAudioBufferClear

The client `input_audio_buffer.clear` event is used to clear the audio bytes in the buffer.

The server responds with an `input_audio_buffer.cleared` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.clear"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.clear`. |

### RealtimeClientEventInputAudioBufferCommit

The client `input_audio_buffer.commit` event is used to commit the user input audio buffer, which creates a new user message item in the conversation. Audio is transcribed if `input_audio_transcription` is configured for the session.

When in server VAD mode, the client doesn't need to send this event, the server commits the audio buffer automatically. Without server VAD, the client must commit the audio buffer to create a user message item. This client event produces an error if the input audio buffer is empty.

Committing the input audio buffer doesn't create a response from the model.

The server responds with an `input_audio_buffer.committed` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.commit"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.commit`. |

### RealtimeClientEventResponseCancel

The client `response.cancel` event is used to cancel an in-progress response.

The server will respond with a `response.done` event with a status of `response.status=cancelled`.

#### Event structure

```json
{
  "type": "response.cancel"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.cancel`. |

### RealtimeClientEventResponseCreate

The client `response.create` event is used to instruct the server to create a response via model inference. When the session is configured in server VAD mode, the server creates responses automatically.

A response includes at least one `item`, and can have two, in which case the second is a function call. These items are appended to the conversation history.

The server responds with a [`response.created`](#responsecreated) event, one or more item and content events (such as `conversation.item.created` and `response.content_part.added`), and finally a [`response.done`](#responsedone) event to indicate the response is complete.


#### Event structure

```json
{
  "type": "response.create"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.create`. |
| response | [RealtimeResponseOptions](#realtimeresponseoptions) | The response options. |

### RealtimeClientEventSessionUpdate

The client `session.update` event is used to update the session's default configuration. The client can send this event at any time to update the session configuration, and any field can be updated at any time, except for voice.

Only fields that are present are updated. To clear a field (such as `instructions`), pass an empty string.

The server responds with a `session.updated` event that contains the full effective configuration.

#### Event structure

```json
{
  "type": "session.update"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `session.update`. |
| session | [RealtimeRequestSession](#realtimerequestsession) | The session configuration. |

## Server Events

The Voice Live API sends the following server events to communicate status, responses, and data to the client:

| Event | Description |
|-------|-------------|
| [error](#error) | Indicates an error occurred during processing |
| [session.created](#sessioncreated) | Sent when a new session is successfully established |
| [session.updated](#sessionupdated) | Sent when session configuration is updated |
| [session.avatar.connecting](#sessionavatarconnecting) | Indicates avatar WebRTC connection is being established |
| [conversation.item.created](#conversationitemcreated) | Sent when a new item is added to the conversation |
| [conversation.item.retrieved](#conversationitemretrieved) | Response to conversation.item.retrieve request |
| [conversation.item.truncated](#conversationitemtruncated) | Confirms item truncation |
| [conversation.item.deleted](#conversationitemdeleted) | Confirms item deletion |
| [conversation.item.input_audio_transcription.completed](#conversationiteminputaudiotranscriptioncompleted) | Input audio transcription is complete |
| [conversation.item.input_audio_transcription.delta](#conversationiteminputaudiotranscriptiondelta) | Streaming input audio transcription |
| [conversation.item.input_audio_transcription.failed](#conversationiteminputaudiotranscriptionfailed) | Input audio transcription failed |
| [input_audio_buffer.committed](#inputaudiobuffercommitted) | Input audio buffer has been committed for processing |
| [input_audio_buffer.cleared](#inputaudiobuffercleared) | Input audio buffer has been cleared |
| [input_audio_buffer.speech_started](#inputaudiobufferspeechstarted) | Speech detected in input audio buffer (VAD) |
| [input_audio_buffer.speech_stopped](#inputaudiobufferspeechstopped) | Speech ended in input audio buffer (VAD) |
| [response.created](#responsecreated) | New response generation has started |
| [response.done](#responsedone) | Response generation is complete |
| [response.output_item.added](#responseoutputitemadded) | New output item added to response |
| [response.output_item.done](#responseoutputitemdone) | Output item is complete |
| [response.content_part.added](#responsecontentpartadded) | New content part added to output item |
| [response.content_part.done](#responsecontentpartdone) | Content part is complete |
| [response.text.delta](#responsetextdelta) | Streaming text content from the model |
| [response.text.done](#responsetextdone) | Text content is complete |
| [response.audio_transcript.delta](#responseaudiotranscriptdelta) | Streaming audio transcript |
| [response.audio_transcript.done](#responseaudiotranscriptdone) | Audio transcript is complete |
| [response.audio.delta](#responseaudiodelta) | Streaming audio content from the model |
| [response.audio.done](#responseaudiodone) | Audio content is complete |
| [response.animation_blendshapes.delta](#responseanimationblendshapesdelta) | Streaming animation blendshapes data |
| [response.animation_blendshapes.done](#responseanimationblendshapesdone) | Animation blendshapes data is complete |
| [response.audio_timestamp.delta](#responseaudiotimestampdelta) | Streaming audio timestamp information |
| [response.audio_timestamp.done](#responseaudiotimestampdone) | Audio timestamp information is complete |
| [response.animation_viseme.delta](#responseanimationvisemedelta) | Streaming animation viseme data |
| [response.animation_viseme.done](#responseanimationvisemedone) | Animation viseme data is complete |
| [response.function_call_arguments.delta](#responsefunctioncallargumentsdelta) | Streaming function call arguments |
| [response.function_call_arguments.done](#responsefunctioncallargumentsdone) | Function call arguments are complete |

### error

Indicates that an error occurred during processing. Most errors are recoverable and the session remains open.

#### Event Structure

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_event_type",
    "message": "Unknown event type 'invalid.event'",
    "param": "type",
    "event_id": "event_ABC123"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"error"` |
| error | [RealtimeErrorDetails](#realtimeerrordetails) | Error information object |

#### Error Details Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The error type (e.g., "invalid_request_error", "server_error") |
| code | string | Specific error code |
| message | string | Human-readable error description |
| param | string | Parameter related to the error, if applicable |
| event_id | string | ID of the client event that caused the error, if applicable |

### session.created

Sent when a new session is successfully established. This is the first event received after connecting to the API.

#### Event Structure

```json
{
  "type": "session.created",
  "session": {
    "id": "sess_ABC123DEF456",
    "object": "realtime.session",
    "model": "gpt-4o-realtime-preview",
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful assistant.",
    "voice": {
      "type": "openai",
      "name": "alloy"
    },
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "input_audio_sampling_rate": 24000,
    "turn_detection": {
      "type": "azure_semantic_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "temperature": 0.8,
    "max_response_output_tokens": "inf"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"session.created"` |
| session | [RealtimeResponseSession](#realtimeresponsesession) | The created session object |

### session.updated

Sent when session configuration is successfully updated in response to a `session.update` client event.

#### Event Structure

```json
{
  "type": "session.updated",
  "session": {
    "id": "sess_ABC123DEF456",
    "voice": {
      "type": "azure-custom",
      "name": "my-voice",
      "endpoint_id": "12345678-1234-1234-1234-123456789012"
    },
    "temperature": 0.7,
    "avatar": {
      "character": "lisa",
      "customized": false
    }
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"session.updated"` |
| session | [RealtimeResponseSession](#realtimeresponsesession) | The updated session object |

### session.avatar.connecting

Indicates that an avatar WebRTC connection is being established. This event is sent in response to a `session.avatar.connect` client event.

#### Event Structure

```json
{
  "type": "session.avatar.connecting",
  "server_sdp": "<server_sdp>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"session.avatar.connecting"` |

### conversation.item.created

Sent when a new item is added to the conversation, either through a client `conversation.item.create` event or automatically during response generation.

#### Event Structure

```json
{
  "type": "conversation.item.created",
  "previous_item_id": "item_ABC123",
  "item": {
    "id": "item_DEF456",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "Hello, how are you?"
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.created"` |
| previous_item_id | string | ID of the item after which this item was inserted |
| item | [RealtimeConversationItem](#realtimeconversationitem) | The created conversation item |

#### Example with Audio Item

```json
{
  "type": "conversation.item.created",
  "item": {
    "id": "item_GHI789",
    "type": "message",
    "status": "completed",
    "role": "user",
    "content": [
      {
        "type": "input_audio",
        "audio": null,
        "transcript": "What's the weather like today?"
      }
    ]
  }
}
```

### response.created

Sent when a new response generation begins. This is the first event in a response sequence.

#### Event Structure

```json
{
  "type": "response.created",
  "response": {
    "id": "resp_ABC123",
    "object": "realtime.response",
    "status": "in_progress",
    "status_details": null,
    "output": [],
    "usage": {
      "total_tokens": 0,
      "input_tokens": 0,
      "output_tokens": 0
    }
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.created"` |
| response | [RealtimeResponse](#realtimeresponse) | The response object that was created |

### response.done

Sent when response generation is complete. This event contains the final response with all output items and usage statistics.

#### Event Structure

```json
{
  "type": "response.done",
  "response": {
    "id": "resp_ABC123",
    "object": "realtime.response",
    "status": "completed",
    "status_details": null,
    "output": [
      {
        "id": "item_DEF456",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "Hello! I'm doing well, thank you for asking. How can I help you today?"
          }
        ]
      }
    ],
    "usage": {
      "total_tokens": 87,
      "input_tokens": 52,
      "output_tokens": 35,
      "input_token_details": {
        "cached_tokens": 0,
        "text_tokens": 45,
        "audio_tokens": 7
      },
      "output_token_details": {
        "text_tokens": 15,
        "audio_tokens": 20
      }
    }
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.done"` |
| response | [RealtimeResponse](#realtimeresponse) | The completed response object |

### response.output_item.added

Sent when a new output item is added to the response during generation.

#### Event Structure

```json
{
  "type": "response.output_item.added",
  "response_id": "resp_ABC123",
  "output_index": 0,
  "item": {
    "id": "item_DEF456",
    "object": "realtime.item",
    "type": "message",
    "status": "in_progress",
    "role": "assistant",
    "content": []
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.output_item.added"` |
| response_id | string | ID of the response this item belongs to |
| output_index | integer | Index of the item in the response's output array |
| item | [RealtimeConversationItem](#realtimeconversationitem) | The output item that was added |

### response.output_item.done

Sent when an output item is complete.

#### Event Structure

```json
{
  "type": "response.output_item.done",
  "response_id": "resp_ABC123",
  "output_index": 0,
  "item": {
    "id": "item_DEF456",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "Hello! I'm doing well, thank you for asking."
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.output_item.done"` |
| response_id | string | ID of the response this item belongs to |
| output_index | integer | Index of the item in the response's output array |
| item | [RealtimeConversationItem](#realtimeconversationitem) | The completed output item |

### response.content_part.added

Sent when a new content part is added to an output item.

#### Event Structure

```json
{
  "type": "response.content_part.added",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "text",
    "text": ""
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.content_part.added"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item this content part belongs to |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of this content part in the item |
| part | [RealtimeContentPart](#realtimecontentpart) | The content part that was added |

### response.content_part.done

Sent when a content part is complete.

#### Event Structure

```json
{
  "type": "response.content_part.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "text",
    "text": "Hello! I'm doing well, thank you for asking."
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.content_part.done"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item this content part belongs to |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of this content part in the item |
| part | [RealtimeContentPart](#realtimecontentpart) | The completed content part |

### response.text.delta

Streaming text content from the model. Sent incrementally as the model generates text.

#### Event Structure

```json
{
  "type": "response.text.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "delta": "Hello! I'm"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.text.delta"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| delta | string | Incremental text content |

### response.text.done

Sent when text content generation is complete.

#### Event Structure

```json
{
  "type": "response.text.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "text": "Hello! I'm doing well, thank you for asking. How can I help you today?"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.text.done"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| text | string | The complete text content |

### response.audio.delta

Streaming audio content from the model. Audio is provided as base64-encoded data.

#### Event Structure

```json
{
  "type": "response.audio.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "delta": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA="
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.audio.delta"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| delta | string | Base64-encoded audio data chunk |

### response.audio.done

Sent when audio content generation is complete.

#### Event Structure

```json
{
  "type": "response.audio.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.audio.done"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |

### response.audio_transcript.delta

Streaming transcript of the generated audio content.

#### Event Structure

```json
{
  "type": "response.audio_transcript.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "delta": "Hello! I'm doing"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.audio_transcript.delta"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| delta | string | Incremental transcript text |

### response.audio_transcript.done

Sent when audio transcript generation is complete.

#### Event Structure

```json
{
  "type": "response.audio_transcript.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "transcript": "Hello! I'm doing well, thank you for asking. How can I help you today?"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"response.audio_transcript.done"` |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| transcript | string | The complete transcript text |

### conversation.item.input_audio_transcription.completed

The server `conversation.item.input_audio_transcription.completed` event is the result of audio transcription for speech written to the audio buffer.

Transcription begins when the input audio buffer is committed by the client or server (in `server_vad` mode). Transcription runs asynchronously with response creation, so this event can come before or after the response events.

Realtime API models accept audio natively, and thus input transcription is a separate process run on a separate speech recognition model such as `whisper-1`. Thus the transcript can diverge somewhat from the model's interpretation, and should be treated as a rough guide.

#### Event structure

```json
{
  "type": "conversation.item.input_audio_transcription.completed",
  "item_id": "<item_id>",
  "content_index": 0,
  "transcript": "<transcript>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.completed`. |
| item_id | string | The ID of the user message item containing the audio. |
| content_index | integer | The index of the content part containing the audio. |
| transcript | string | The transcribed text. |

### conversation.item.input_audio_transcription.failed

The server `conversation.item.input_audio_transcription.failed` event is returned when input audio transcription is configured, and a transcription request for a user message failed. This event is separate from other `error` events so that the client can identify the related item.

#### Event structure

```json
{
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "<item_id>",
  "content_index": 0,
  "error": {
    "code": "<code>",
    "message": "<message>",
    "param": "<param>"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.failed`. |
| item_id | string | The ID of the user message item. |
| content_index | integer | The index of the content part containing the audio. |
| error | object | Details of the transcription error.<br><br>See nested properties in the next table.|

#### Error properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of error. |
| code | string | Error code, if any. |
| message | string | A human-readable error message. |
| param | string | Parameter related to the error, if any. |

### conversation.item.truncated

The server `conversation.item.truncated` event is returned when the client truncates an earlier assistant audio message item with a `conversation.item.truncate` event. This event is used to synchronize the server's understanding of the audio with the client's playback.

This event truncates the audio and removes the server-side text transcript to ensure there's no text in the context that the user doesn't know about.

#### Event structure

```json
{
  "type": "conversation.item.truncated",
  "item_id": "<item_id>",
  "content_index": 0,
  "audio_end_ms": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.truncated`. |
| item_id | string | The ID of the assistant message item that was truncated. |
| content_index | integer | The index of the content part that was truncated. |
| audio_end_ms | integer | The duration up to which the audio was truncated, in milliseconds. |

### error

The server `error` event is returned when an error occurs, which could be a client problem or a server problem. Most errors are recoverable and the session stays open.

#### Event structure

```json
{
  "type": "error",
  "error": {
    "code": "<code>",
    "message": "<message>",
    "param": "<param>",
    "event_id": "<event_id>"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `error`. |
| error | object | Details of the error.<br><br>See nested properties in the next table.|

#### Error properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of error. For example, "invalid_request_error" and "server_error" are error types. |
| code | string | Error code, if any. |
| message | string | A human-readable error message. |
| param | string | Parameter related to the error, if any. |
| event_id | string | The ID of the client event that caused the error, if applicable. |

### input_audio_buffer.cleared

The server `input_audio_buffer.cleared` event is returned when the client clears the input audio buffer with a `input_audio_buffer.clear` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.cleared"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.cleared`. |

### input_audio_buffer.committed

The server `input_audio_buffer.committed` event is returned when an input audio buffer is committed, either by the client or automatically in server VAD mode. The `item_id` property is the ID of the user message item created. Thus a `conversation.item.created` event is also sent to the client.

#### Event structure

```json
{
  "type": "input_audio_buffer.committed",
  "previous_item_id": "<previous_item_id>",
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.committed`. |
| previous_item_id | string | The ID of the preceding item after which the new item is inserted. |
| item_id | string | The ID of the user message item created. |

### input_audio_buffer.speech_started

The server `input_audio_buffer.speech_started` event is returned in `server_vad` mode when speech is detected in the audio buffer. This event can happen any time audio is added to the buffer (unless speech is already detected).

> [!NOTE]
> The client might want to use this event to interrupt audio playback or provide visual feedback to the user.

The client should expect to receive a `input_audio_buffer.speech_stopped` event when speech stops. The `item_id` property is the ID of the user message item created when speech stops. The `item_id` is also included in the `input_audio_buffer.speech_stopped` event unless the client manually commits the audio buffer during VAD activation.

#### Event structure

```json
{
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 0,
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.speech_started`. |
| audio_start_ms | integer | Milliseconds from the start of all audio written to the buffer during the session when speech was first detected. This property corresponds to the beginning of audio sent to the model, and thus includes the `prefix_padding_ms` configured in the session. |
| item_id | string | The ID of the user message item created when speech stops. |

### input_audio_buffer.speech_stopped

The server `input_audio_buffer.speech_stopped` event is returned in `server_vad` mode when the server detects the end of speech in the audio buffer.

The server also sends a `conversation.item.created` event with the user message item created from the audio buffer.

#### Event structure

```json
{
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 0,
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.speech_stopped`. |
| audio_end_ms | integer | Milliseconds since the session started when speech stopped. This property corresponds to the end of audio sent to the model, and thus includes the `min_silence_duration_ms` configured in the session. |
| item_id | string | The ID of the user message item created. |

### rate_limits.updated

The server `rate_limits.updated` event is emitted at the beginning of a response to indicate the updated rate limits.

When a response is created, some tokens are reserved for the output tokens. The rate limits shown here reflect that reservation, which is then adjusted accordingly once the response is completed.

#### Event structure

```json
{
  "type": "rate_limits.updated",
  "rate_limits": [
    {
      "name": "<name>",
      "limit": 0,
      "remaining": 0,
      "reset_seconds": 0
    }
  ]
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `rate_limits.updated`. |
| rate_limits | array of [RealtimeRateLimitsItem](#realtimeratelimitsitem) | The list of rate limit information. |

### response.audio.delta

The server `response.audio.delta` event is returned when the model-generated audio is updated.

#### Event structure

```json
{
  "type": "response.audio.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| delta | string | Base64-encoded audio data delta. |

### response.audio.done

The server `response.audio.done` event is returned when the model-generated audio is done.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.audio.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |

### response.audio_transcript.delta

The server `response.audio_transcript.delta` event is returned when the model-generated transcription of audio output is updated.

#### Event structure

```json
{
  "type": "response.audio_transcript.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio_transcript.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| delta | string | The transcript delta. |

### response.audio_transcript.done

The server `response.audio_transcript.done` event is returned when the model-generated transcription of audio output is done streaming.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.audio_transcript.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0,
  "transcript": "<transcript>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio_transcript.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| transcript | string | The final transcript of the audio. |

### response.content_part.added

The server `response.content_part.added` event is returned when a new content part is added to an assistant message item during response generation.

#### Event structure

```json
{
  "type": "response.content_part.added",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.content_part.added`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item to which the content part was added. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| part | [RealtimeContentPart](#realtimecontentpart) | The content part that was added. |

#### Part properties

| Field | Type | Description |
|------|------|-------------|
| type | [RealtimeContentPartType](#realtimecontentparttype) |  |

### response.content_part.done

The server `response.content_part.done` event is returned when a content part is done streaming in an assistant message item.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.content_part.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.content_part.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| part | [RealtimeContentPart](#realtimecontentpart) | The content part that is done. |

#### Part properties

| Field | Type | Description |
|------|------|-------------|
| type | [RealtimeContentPartType](#realtimecontentparttype) |  |

### response.created

The server `response.created` event is returned when a new response is created. This is the first event of response creation, where the response is in an initial state of `in_progress`.

#### Event structure

```json
{
  "type": "response.created"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.created`. |
| response | [RealtimeResponse](#realtimeresponse) | The response object. |

### response.done

The server `response.done` event is returned when a response is done streaming. This event is always emitted, no matter the final state. The response object included in the `response.done` event includes all output items in the response, but omits the raw audio data.

#### Event structure

```json
{
  "type": "response.done"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.done`. |
| response | [RealtimeResponse](#realtimeresponse) | The response object. |

### response.function_call_arguments.delta

The server `response.function_call_arguments.delta` event is returned when the model-generated function call arguments are updated.

#### Event structure

```json
{
  "type": "response.function_call_arguments.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "call_id": "<call_id>",
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.function_call_arguments.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the function call item. |
| output_index | integer | The index of the output item in the response. |
| call_id | string | The ID of the function call. |
| delta | string | The arguments delta as a JSON string. |

### response.function_call_arguments.done

The server `response.function_call_arguments.done` event is returned when the model-generated function call arguments are done streaming.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.function_call_arguments.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "call_id": "<call_id>",
  "arguments": "<arguments>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.function_call_arguments.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the function call item. |
| output_index | integer | The index of the output item in the response. |
| call_id | string | The ID of the function call. |
| arguments | string | The final arguments as a JSON string. |

### response.output_item.added

The server `response.output_item.added` event is returned when a new item is created during response generation.

#### Event structure

```json
{
  "type": "response.output_item.added",
  "response_id": "<response_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_item.added`. |
| response_id | string | The ID of the response to which the item belongs. |
| output_index | integer | The index of the output item in the response. |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The item that was added. |

### response.output_item.done

The server `response.output_item.done` event is returned when an item is done streaming.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.output_item.done",
  "response_id": "<response_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_item.done`. |
| response_id | string | The ID of the response to which the item belongs. |
| output_index | integer | The index of the output item in the response. |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The item that is done streaming. |

### response.text.delta

The server `response.text.delta` event is returned when the model-generated text is updated. The text corresponds to the `text` content part of an assistant message item.

#### Event structure

```json
{
  "type": "response.text.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.text.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| delta | string | The text delta. |

### response.text.done

The server `response.text.done` event is returned when the model-generated text is done streaming. The text corresponds to the `text` content part of an assistant message item.

This event is also returned when a response is interrupted, incomplete, or canceled.

#### Event structure

```json
{
  "type": "response.text.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "content_index": 0,
  "text": "<text>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.text.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's content array. |
| text | string | The final text content. |

### session.created

The server `session.created` event is the first server event when you establish a new connection to the Realtime API. This event creates and returns a new session with the default session configuration.

#### Event structure

```json
{
  "type": "session.created"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `session.created`. |
| session | [RealtimeResponseSession](#realtimeresponsesession) | The session object. |

### session.updated

The server `session.updated` event is returned when a session is updated by the client. If there's an error, the server sends an `error` event instead.

#### Event structure

```json
{
  "type": "session.updated"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `session.updated`. |
| session | [RealtimeResponseSession](#realtimeresponsesession) | The session object. |

## Components

### Audio Formats

#### RealtimeAudioFormat

Base audio format used for input audio.

**Allowed Values:**
* `pcm16` - 16-bit PCM audio format
* `g711_ulaw` - G.711 μ-law audio format
* `g711_alaw` - G.711 A-law audio format

#### RealtimeOutputAudioFormat

Audio format used for output audio with specific sampling rates.

**Allowed Values:**
* `pcm16` - 16-bit PCM audio format at default sampling rate (24kHz)
* `pcm16_8000hz` - 16-bit PCM audio format at 8kHz sampling rate
* `pcm16_16000hz` - 16-bit PCM audio format at 16kHz sampling rate
* `g711_ulaw` - G.711 μ-law (mu-law) audio format at 8kHz sampling rate
* `g711_alaw` - G.711 A-law audio format at 8kHz sampling rate

#### RealtimeAudioInputTranscriptionSettings

Configuration for input audio transcription.

| Field | Type | Description |
|-------|------|-------------|
| model | string | The transcription model. Supported: `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `azure-speech` |
| language | string | Optional language code in BCP-47 (e.g., `en-US`), or ISO-639-1 (e.g., `en`), or multi languages with auto detection, (e.g., `en,zh`). |
| custom_speech | object | Optional configuration for custom speech models |
| phrase_list | string[] | Optional list of phrase hints to bias recognition |

#### RealtimeAudioNoiseReduction

Configuration for input audio noise reduction.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure_deep_noise_suppression"` |

#### RealtimeAudioEchoCancellation

Echo cancellation configuration for server-side audio processing.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"server_echo_cancellation"` |

### Voice Configuration

#### RealtimeVoice

Union of all supported voice configurations.

This can be:
- A simple string (OpenAI voice name)
- An [RealtimeOpenAIVoice](#realtimeopenaivoice) object
- An [RealtimeAzureVoice](#realtimeazurevoice) object

#### RealtimeOpenAIVoice

OpenAI voice configuration with explicit type field.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"openai"` |
| name | string | OpenAI voice name: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse` |

#### RealtimeAzureVoice

Base for Azure voice configurations. This is a discriminated union with different types:

##### RealtimeAzureCustomVoice

Azure custom voice configuration (preferred for custom voices).

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-custom"` |
| name | string | Voice name (cannot be empty) |
| endpoint_id | string | Endpoint ID (cannot be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| custom_lexicon_url | string | Optional. URL to custom lexicon |
| prefer_locales | string[] | Optional. Preferred locales |
| locale | string | Optional. Locale specification |
| style | string | Optional. Voice style |
| pitch | string | Optional. Pitch adjustment |
| rate | string | Optional. Speech rate adjustment |
| volume | string | Optional. Volume adjustment |

Example:
```json
{
  "type": "azure-custom",
  "name": "my-custom-voice",
  "endpoint_id": "12345678-1234-1234-1234-123456789012",
  "temperature": 0.7,
  "style": "cheerful",
  "locale": "en-US"
}
```

##### RealtimeAzureStandardVoice

Azure standard voice configuration.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-standard"` |
| name | string | Voice name (cannot be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| custom_lexicon_url | string | Optional. URL to custom lexicon |
| prefer_locales | string[] | Optional. Preferred locales |
| locale | string | Optional. Locale specification |
| style | string | Optional. Voice style |
| pitch | string | Optional. Pitch adjustment |
| rate | string | Optional. Speech rate adjustment |
| volume | string | Optional. Volume adjustment |

##### RealtimeAzurePersonalVoice

Azure personal voice configuration.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-personal"` |
| name | string | Voice name (cannot be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| model | string | Underlying neural model: `DragonLatestNeural`, `PhoenixLatestNeural`, `PhoenixV2Neural` |

### Turn Detection

#### RealtimeTurnDetection

Configuration for turn detection. This is a discriminated union supporting multiple VAD types.

##### RealtimeServerVad

Base VAD-based turn detection.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"server_vad"` |
| threshold | number | Optional. Activation threshold (0.0-1.0) |
| prefix_padding_ms | integer | Optional. Audio padding before speech starts |
| silence_duration_ms | integer | Optional. Silence duration to detect speech end |
| end_of_utterance_detection | [RealtimeEOUDetection](#realtimeeoudetection) | Optional. End-of-utterance detection config |
| auto_truncate | boolean | Optional. Auto-truncate on interruption (default: false) |

##### RealtimeAzureSemanticVad

Azure semantic VAD (default variant).

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure_semantic_vad"` |
| threshold | number | Optional. Activation threshold |
| prefix_padding_ms | integer | Optional. Audio padding before speech |
| silence_duration_ms | integer | Optional. Silence duration for speech end |
| end_of_utterance_detection | [RealtimeEOUDetection](#realtimeeoudetection) | Optional. EOU detection config |
| neg_threshold | number | Optional. Negative threshold |
| speech_duration_ms | integer | Optional. Minimum speech duration |
| window_size | integer | Optional. Analysis window size |
| distinct_ci_phones | integer | Optional. Distinct CI phones requirement |
| require_vowel | boolean | Optional. Require vowel in speech |
| remove_filler_words | boolean | Optional. Remove filler words (default: false) |
| languages | string[] | Optional. Supported languages |
| auto_truncate | boolean | Optional. Auto-truncate on interruption (default: false) |

#### RealtimeEOUDetection

End-of-utterance semantic detection configuration.

##### RealtimeAzureSemanticDetection

Azure semantic end-of-utterance detection (default).

| Field | Type | Description |
|-------|------|-------------|
| model | string | Must be `"semantic_detection_v1"` |
| threshold | number | Optional. Detection threshold |
| timeout | number | Optional. Detection timeout |

### Avatar Configuration

#### RealtimeAvatarConfig

Configuration for avatar streaming and behavior.

| Field | Type | Description |
|-------|------|-------------|
| ice_servers | [RealtimeIceServer](#realtimeiceserver)[] | Optional. ICE servers for WebRTC |
| character | string | Character name or ID for the avatar |
| style | string | Optional. Avatar style (emotional tone, speaking style) |
| customized | boolean | Whether the avatar is customized |
| video | [RealtimeVideoParams](#realtimevideoparams) | Optional. Video configuration |

#### RealtimeIceServer

ICE server configuration for WebRTC connection negotiation.

| Field | Type | Description |
|-------|------|-------------|
| urls | string[] | ICE server URLs (TURN or STUN endpoints) |
| username | string | Optional. Username for authentication |
| credential | string | Optional. Credential for authentication |

#### RealtimeVideoParams

Video streaming parameters for avatar.

| Field | Type | Description |
|-------|------|-------------|
| bitrate | integer | Optional. Bitrate in bits per second (default: 2000000) |
| codec | string | Optional. Video codec, currently only `h264` (default: `h264`) |
| crop | [RealtimeVideoCrop](#realtimevideocrop) | Optional. Cropping settings |
| resolution | [RealtimeVideoResolution](#realtimevideoresolution) | Optional. Resolution settings |

#### RealtimeVideoCrop

Video crop rectangle definition.

| Field | Type | Description |
|-------|------|-------------|
| top_left | integer[] | Top-left corner [x, y], non-negative integers |
| bottom_right | integer[] | Bottom-right corner [x, y], non-negative integers |

#### RealtimeVideoResolution

Video resolution specification.

| Field | Type | Description |
|-------|------|-------------|
| width | integer | Width in pixels (must be > 0) |
| height | integer | Height in pixels (must be > 0) |

### Animation Configuration

#### RealtimeAnimation

Configuration for animation outputs including blendshapes and visemes.

| Field | Type | Description |
|-------|------|-------------|
| model_name | string | Optional. Animation model name (default: `"default"`) |
| outputs | [RealtimeAnimationOutputType](#realtimeanimationoutputtype)[] | Optional. Output types (default: `["blendshapes"]`) |

#### RealtimeAnimationOutputType

Types of animation data to output.

**Allowed Values:**
* `blendshapes` - Facial blendshapes data
* `viseme_id` - Viseme identifier data

### Session Configuration

#### RealtimeRequestSession

Session configuration object used in `session.update` events.

| Field | Type | Description |
|-------|------|-------------|
| model | string | Optional. Model name to use |
| modalities | [RealtimeModality](#realtimemodality)[] | Optional. Supported modalities |
| animation | [RealtimeAnimation](#realtimeanimation) | Optional. Animation configuration |
| voice | [RealtimeVoice](#realtimevoice) | Optional. Voice configuration |
| instructions | string | Optional. System instructions for the model |
| input_audio_sampling_rate | integer | Optional. Input audio sampling rate in Hz (default: 24000) |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | Optional. Input audio format (default: `pcm16`) |
| output_audio_format | [RealtimeOutputAudioFormat](#realtimeoutputaudioformat) | Optional. Output audio format (default: `pcm16`) |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) | Optional. Turn detection configuration |
| input_audio_noise_reduction | [RealtimeAudioNoiseReduction](#realtimeaudionoisereduction) | Optional. Noise reduction settings |
| input_audio_echo_cancellation | [RealtimeAudioEchoCancellation](#realtimeaudioechocancellation) | Optional. Echo cancellation settings |
| avatar | [RealtimeAvatarConfig](#realtimeavatarconfig) | Optional. Avatar configuration |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) | Optional. Transcription settings |
| output_audio_timestamp_types | [RealtimeAudioTimestampType](#realtimeaudiotimestamptype)[] | Optional. Timestamp types for output audio |
| tools | [RealtimeTool](#realtimetool)[] | Optional. Available tools |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | Optional. Tool selection strategy |
| temperature | number | Optional. Sampling temperature |
| max_response_output_tokens | integer or "inf" | Optional. Maximum output tokens |

#### RealtimeResponseSession

Session object returned in server events, extends RequestSession.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Optional. Session ID |
| agent | [RealtimeAgentConfig](#realtimeagentconfig) | Optional. Agent configuration |
| ...RealtimeRequestSession | | All fields from RealtimeRequestSession |

#### RealtimeModality

Supported session modalities.

**Allowed Values:**
* `text` - Text input/output
* `audio` - Audio input/output
* `animation` - Animation output
* `avatar` - Avatar video output

#### RealtimeAudioTimestampType

Output timestamp types supported in audio response content.

**Allowed Values:**
* `word` - Timestamps per word in the output audio

### Tool Configuration

#### RealtimeTool

Tool definition for function calling.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"function"` |
| name | string | Function name |
| description | string | Function description and usage guidelines |
| parameters | object | Function parameters as JSON schema object |

#### RealtimeToolChoice

Tool selection strategy.

This can be:
- `"auto"` - Let the model choose
- `"none"` - Don't use tools
- `"required"` - Must use a tool
- `{ "type": "function", "name": "function_name" }` - Use specific function

### Conversation Items

#### RealtimeConversationItem

This is a union type that can be one of the following:

#### RealtimeConversationUserMessageItem

User message item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"message"` |
| object | string | Must be `"conversation.item"` |
| role | string | Must be `"user"` |
| content | [RealtimeInputTextContentPart](#realtimeinputtextcontentpart)[] | The content of the message. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

#### RealtimeConversationAssistantMessageItem

Assistant message item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"message"` |
| object | string | Must be `"conversation.item"` |
| role | string | Must be `"assistant"` |
| content | [RealtimeOutputTextContentPart](#realtimeoutputtextcontentpart)[] or [RealtimeOutputAudioContentPart](#realtimeoutputaudiocontentpart)[] | The content of the message. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

#### RealtimeConversationSystemMessageItem

System message item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"message"` |
| object | string | Must be `"conversation.item"` |
| role | string | Must be `"system"` |
| content | [RealtimeInputTextContentPart](#realtimeinputtextcontentpart)[] | The content of the message. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

#### RealtimeConversationFunctionCallItem

Function call request item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"function_call"` |
| object | string | Must be `"conversation.item"` |
| name | string | The name of the function to call. |
| arguments | string | The arguments for the function call as a JSON string. |
| call_id | string | The unique ID of the function call. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

#### RealtimeConversationFunctionCallOutputItem

Function call response item.
| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"function_call_output"` |
| object | string | Must be `"conversation.item"` |
| name | string | The name of the function that was called. |
| output | string | The output of the function call. |
| call_id | string | The unique ID of the function call. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

#### RealtimeItemStatus

Status of conversation items.

**Allowed Values:**
* `in_progress` - Currently being processed
* `completed` - Successfully completed
* `incomplete` - Incomplete (interrupted or failed)

#### RealtimeContentPart

Content part within a message.

##### RealtimeInputTextContentPart

Text content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be  `"input_text"` |
| text | string | The text content |

##### RealtimeOutputTextContentPart

Text content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"text"` |
| text | string | The text content |

##### RealtimeInputAudioContentPart

Audio content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"input_audio"` |
| audio | string | Optional. Base64-encoded audio data |
| transcript | string | Optional. Audio transcript |

##### RealtimeOutputAudioContentPart

Audio content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"audio"` |
| audio | string | Base64-encoded audio data |
| transcript | string | Optional. Audio transcript |


### Response Objects

#### RealtimeResponse

Response object representing a model inference response.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Optional. Response ID |
| object | string | Optional. Always `"realtime.response"` |
| status | [RealtimeResponseStatus](#realtimeresponsestatus) | Optional. Response status |
| status_details | [RealtimeResponseStatusDetails](#realtimeresponsestatusdetails) | Optional. Status details |
| output | [RealtimeConversationItem](#realtimeconversationitem)[] | Optional. Output items |
| usage | [RealtimeUsage](#realtimeusage) | Optional. Token usage statistics |
| conversation_id | string | Optional. Associated conversation ID |
| voice | [RealtimeVoice](#realtimevoice) | Optional. Voice used for response |
| modalities | string[] | Optional. Modalities used |
| output_audio_format | [RealtimeOutputAudioFormat](#realtimeoutputaudioformat) | Optional. Audio format used |
| temperature | number | Optional. Temperature used |
| max_response_output_tokens | integer or "inf" | Optional. Max tokens used |

#### RealtimeResponseStatus

Response status values.

**Allowed Values:**
* `in_progress` - Response is being generated
* `completed` - Response completed successfully
* `cancelled` - Response was cancelled
* `incomplete` - Response incomplete (interrupted)
* `failed` - Response failed with error

#### Usage

Token usage statistics.

| Field | Type | Description |
|-------|------|-------------|
| total_tokens | integer | Total tokens used |
| input_tokens | integer | Input tokens used |
| output_tokens | integer | Output tokens generated |
| input_token_details | [TokenDetails](#tokendetails) | Breakdown of input tokens |
| output_token_details | [TokenDetails](#tokendetails) | Breakdown of output tokens |

#### TokenDetails

Detailed token usage breakdown.

| Field | Type | Description |
|-------|------|-------------|
| cached_tokens | integer | Optional. Cached tokens used |
| text_tokens | integer | Optional. Text tokens used |
| audio_tokens | integer | Optional. Audio tokens used |

### Error Handling

#### RealtimeErrorDetails

Error information object.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Error type (e.g., `"invalid_request_error"`, `"server_error"`) |
| code | string | Optional. Specific error code |
| message | string | Human-readable error description |
| param | string | Optional. Parameter related to the error |
| event_id | string | Optional. ID of the client event that caused the error |

|-------|------|-------------|
| type | [RealtimeContentPartType](#realtimecontentparttype) | The content type.<br><br>A property of the `function` object.<br/><br>Allowed values: `input_text`, `input_audio`, `item_reference`, `text`. |
| text | string | The text content. This property is applicable for the `input_text` and `text` content types. |
| id | string | ID of a previous conversation item to reference in both client and server created items. This property is applicable for the `item_reference` content type in `response.create` events. |
| audio | string | The base64-encoded audio bytes. This property is applicable for the `input_audio` content type. |
| transcript | string | The transcript of the audio. This property is applicable for the `input_audio` content type. |

### RealtimeConversationRequestItem

You use the `RealtimeConversationRequestItem` object to create a new item in the conversation via the [conversation.item.create](#realtimeclienteventconversationitemcreate) event.

This is a union type that can be one of the following:

#### RealtimeSystemMessageItem

A system message item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | string | The role of the message.<br><br>Allowed values: `system` |
| content | array of [RealtimeRequestTextContentPart](#realtimerequesttextcontentpart) | The content of the message. |
｜ id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one. |

#### RealtimeUserMessageItem

A user message item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | string | The role of the message.<br><br>Allowed values: `user` |
| content | array of [RealtimeRequestTextContentPart](#realtimerequesttextcontentpart) or [RealtimeRequestAudioContentPart](#realtimerequestaudiocontentpart) | The content of the message. |
| id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one. |

#### RealtimeAssistantMessageItem

An assistant message item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | string | The role of the message.<br><br>Allowed values: `assistant` |
| content | array of [RealtimeOutputTextContentPart](#realtimeoutputtextcontentpart) | The content of the message. |

#### RealtimeFunctionCallItem

A function call item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `function_call` |
| name | string | The name of the function to call. |
| arguments | string | The arguments of the function call as a JSON string. |
| call_id | string | The ID of the function call item. |
| id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one. |

#### RealtimeFunctionCallOutputItem

A function call output item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `function_call_output` |
| call_id | string | The ID of the function call item. |
| output | string | The output of the function call, this is a free-form string with the function result, also could be empty. |
| id | string | The unique ID of the item. If the client doesn't provide an ID, the server generates one. |


### RealtimeConversationResponseItem

The `RealtimeConversationResponseItem` object represents an item in the conversation. It's used in some of the server events, such as:

- [conversation.item.created](#conversationitemcreated)
- [response.output_item.added](#responseoutputitemadded)
- [response.output_item.done](#responseoutputitemdone)
- [`response.created`](#responsecreated) (via the `response` property type [`RealtimeResponse`](#realtimeresponse))
- [`response.done`](#responsedone) (via the `response` property type [`RealtimeResponse`](#realtimeresponse))

| Field | Type | Description |
|-------|------|-------------|
| object | string | The identifier for the returned API object.<br><br>Allowed values: `realtime.item` |
| type | [RealtimeItemType](#realtimeitemtype) | The type of the item.<br><br>Allowed values: `message`, `function_call`, `function_call_output` |
| id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one.<br><br>This property is nullable. |

### RealtimeFunctionTool

The definition of a function tool as used by the realtime endpoint.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the tool.<br><br>Allowed values: `function` |
| name | string | The name of the function. |
| description | string | The description of the function, including usage guidelines. For example, "Use this function to get the current time." |
| parameters | object | The parameters of the function in the form of a JSON object. |

### RealtimeItemStatus

**Allowed Values:**

* `in_progress`
* `completed`
* `incomplete`

### RealtimeRequestSession

You use the `RealtimeRequestSession` object when you want to update the session configuration via the [session.update](#realtimeclienteventsessionupdate) event.

| Field | Type | Description |
|-------|------|-------------|
| modalities | array | The modalities that the session supports.<br><br>Allowed values: `text`, `audio`<br/><br/>For example, `"modalities": ["text", "audio"]` is the default setting that enables both text and audio modalities. To enable only text, set `"modalities": ["text"]`. You can't enable only audio. |
| instructions | string | The instructions (the system message) to guide the model's text and audio responses.<br><br>Here are some example instructions to help guide content and format of text and audio responses:<br>`"instructions": "be succinct"`<br>`"instructions": "act friendly"`<br>`"instructions": "here are examples of good responses"`<br><br>Here are some example instructions to help guide audio behavior:<br>`"instructions": "talk quickly"`<br>`"instructions": "inject emotion into your voice"`<br>`"instructions": "laugh frequently"`<br><br>While the model might not always follow these instructions, they provide guidance on the desired behavior. |
| voice | [RealtimeVoice](#realtimevoice) | The voice used for the model response for the session.<br><br>Once the voice is used in the session for the model's audio response, it can't be changed. |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the input audio. |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the output audio. |
| input_audio_noise_reduction | [RealtimeAudioInputAudioNoiseReductionSettings](#realtimeaudioinputaudionoisereductionsettings) | Configuration for input audio noise reduction. This can be set to null to turn off. Noise reduction filters audio added to the input audio buffer before it is sent to VAD and the model. Filtering the audio can improve VAD and turn detection accuracy (reducing false positives) and model performance by improving perception of the input audio.<br><br>This property is nullable.|
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) | The configuration for input audio transcription. The configuration is null (off) by default. Input audio transcription isn't native to the model, since the model consumes audio directly. Transcription runs asynchronously through the `/audio/transcriptions` endpoint and should be treated as guidance of input audio content rather than precisely what the model heard. For additional guidance to the transcription service, the client can optionally set the language and prompt for transcription.<br><br>This property is nullable. |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) | The turn detection settings for the session. This can be set to null to turn off. <br><br>This property is nullable. |
| tools | array of [RealtimeTool](#realtimetool) | The tools available to the model for the session. |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | The tool choice for the session.<br><br>Allowed values: `auto`, `none`, and `required`. Otherwise, you can specify the name of the function to use. |
| temperature | number | The sampling temperature for the model. The allowed temperature values are limited to [0.6, 1.2]. Defaults to 0.8. |
| max_response_output_tokens | integer or "inf" | The maximum number of output tokens per assistant response, inclusive of tool calls.<br><br>Specify an integer between 1 and 4096 to limit the output tokens. Otherwise, set the value to "inf" to allow the maximum number of tokens.<br><br>For example, to limit the output tokens to 1000, set `"max_response_output_tokens": 1000`. To allow the maximum number of tokens, set `"max_response_output_tokens": "inf"`.<br><br>Defaults to `"inf"`. |

### RealtimeRequestSystemMessageItem

| Field | Type | Description |
|-------|------|-------------|
| role | string | The role of the message.<br><br>Allowed values: `system` |
| content | array of [RealtimeInputTextContentPart](#realtimeinputtextcontentpart) | The content of the message. |


### RealtimeRequestUserMessageItem

| Field | Type | Description |
|-------|------|-------------|
| role | string | The role of the message.<br><br>Allowed values: `user` |
| content | array of [RealtimeInputTextContentPart](#realtimeinputtextcontentpart) or [RealtimeRequestAudioContentPart](#realtimerequestaudiocontentpart) | The content of the message. |

### RealtimeResponse

| Field | Type | Description |
|-------|------|-------------|
| object | string | The response object.<br><br>Allowed values: `realtime.response` |
| id | string | The unique ID of the response. |
| status | [RealtimeResponseStatus](#realtimeresponsestatus) | The status of the response.<br><br>The default status value is `in_progress`. |
| status_details | [RealtimeResponseStatusDetails](#realtimeresponsestatusdetails) | The details of the response status.<br><br>This property is nullable. |
| output | array of [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The output items of the response. |
| usage | object | Usage statistics for the response. Each Realtime API session maintains a conversation context and appends new items to the conversation. Output from previous turns (text and audio tokens) is input for later turns.<br><br>See nested properties next.|
| + total_tokens | integer | The total number of tokens in the Response including input and output text and audio tokens.<br><br>A property of the `usage` object. |
| + input_tokens | integer | The number of input tokens used in the response, including text and audio tokens.<br><br>A property of the `usage` object. |
| + output_tokens | integer | The number of output tokens sent in the response, including text and audio tokens.<br><br>A property of the `usage` object. |
| + input_token_details | object | Details about the input tokens used in the response.<br><br>A property of the `usage` object.<br><br>See nested properties next.|
| + cached_tokens | integer | The number of cached tokens used in the response.<br><br>A property of the `input_token_details` object. |
| + text_tokens | integer | The number of text tokens used in the response.<br><br>A property of the `input_token_details` object. |
| + audio_tokens | integer | The number of audio tokens used in the response.<br><br>A property of the `input_token_details` object. |
| + output_token_details | object | Details about the output tokens used in the response.<br><br>A property of the `usage` object.<br><br>See nested properties next.|
| + text_tokens | integer | The number of text tokens used in the response.<br><br>A property of the `output_token_details` object. |
| + audio_tokens | integer | The number of audio tokens used in the response.<br><br>A property of the `output_token_details` object. |


### RealtimeResponseAudioContentPart

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the content part.<br><br>Allowed values: `audio` |
| transcript | string | The transcript of the audio.<br><br>This property is nullable. |


### RealtimeResponseFunctionCallItem

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `function_call` |
| name | string | The name of the function call item. |
| call_id | string | The ID of the function call item. |
| arguments | string | The arguments of the function call item. |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

### RealtimeResponseFunctionCallOutputItem

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `function_call_output` |
| call_id | string | The ID of the function call item. |
| output | string | The output of the function call item. |

### RealtimeResponseMessageItem

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | [RealtimeMessageRole](#realtimemessagerole) | The role of the message. |
| content | array | The content of the message.<br><br>Array items: [RealtimeResponseTextContentPart](#realtimeresponsetextcontentpart) |
| status | [RealtimeItemStatus](#realtimeitemstatus) | The status of the item. |

### RealtimeResponseOptions

| Field | Type | Description |
|-------|------|-------------|
| modalities | array | The modalities that the session supports.<br><br>Allowed values: `text`, `audio`<br/><br/>For example, `"modalities": ["text", "audio"]` is the default setting that enables both text and audio modalities. To enable only text, set `"modalities": ["text"]`. You can't enable only audio. |
| instructions | string | The instructions (the system message) to guide the model's responses.|
| voice | [RealtimeVoice](#realtimevoice) | The voice used for the model response for the session.<br><br>Once the voice is used in the session for the model's audio response, it can't be changed. |
| tools | array of [RealtimeTool](#realtimetool) | The tools available to the model for the session. |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | The tool choice for the session. |
| temperature | number | The sampling temperature for the model. The allowed temperature values are limited to [0.6, 1.2]. Defaults to 0.8. |
| max_response_output_tokens | integer or "inf" | The maximum number of output tokens per assistant response, inclusive of tool calls.<br><br>Specify an integer between 1 and 4096 to limit the output tokens. Otherwise, set the value to "inf" to allow the maximum number of tokens.<br><br>For example, to limit the output tokens to 1000, set `"max_response_output_tokens": 1000`. To allow the maximum number of tokens, set `"max_response_output_tokens": "inf"`.<br><br>Defaults to `"inf"`. |
| conversation | string | Controls which conversation the response is added to. The supported values are `auto` and `none`.<br><br>The `auto` value (or not setting this property) ensures that the contents of the response are added to the session's default conversation.<br><br>Set this property to `none` to create an out-of-band response where items won't be added to the default conversation. For more information, see the [how-to guide](./how-to/realtime-audio.md#out-of-band-responses).<br><br>Defaults to `"auto"` |
| metadata | map | Set of up to 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maximum of 512 characters long.<br/><br/>For example: `metadata: { topic: "classification" }` |


### RealtimeResponseSession

The `RealtimeResponseSession` object represents a session in the Realtime API. It's used in some of the server events, such as:
- [`session.created`](#sessioncreated)
- [`session.updated`](#sessionupdated)

| Field | Type | Description |
|-------|------|-------------|
| object | string | The session object.<br><br>Allowed values: `realtime.session` |
| id | string | The unique ID of the session. |
| model | string | The model used for the session. |
| modalities | array | The modalities that the session supports.<br><br>Allowed values: `text`, `audio`<br/><br/>For example, `"modalities": ["text", "audio"]` is the default setting that enables both text and audio modalities. To enable only text, set `"modalities": ["text"]`. You can't enable only audio. |
| instructions | string | The instructions (the system message) to guide the model's text and audio responses.<br><br>Here are some example instructions to help guide content and format of text and audio responses:<br>`"instructions": "be succinct"`<br>`"instructions": "act friendly"`<br>`"instructions": "here are examples of good responses"`<br><br>Here are some example instructions to help guide audio behavior:<br>`"instructions": "talk quickly"`<br>`"instructions": "inject emotion into your voice"`<br>`"instructions": "laugh frequently"`<br><br>While the model might not always follow these instructions, they provide guidance on the desired behavior. |
| voice | [RealtimeVoice](#realtimevoice) | The voice used for the model response for the session.<br><br>Once the voice is used in the session for the model's audio response, it can't be changed. |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the input audio. |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the output audio. |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) | The settings for audio input transcription.<br><br>This property is nullable. |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) | The turn detection settings for the session.<br><br>This property is nullable. |
| tools | array of [RealtimeTool](#realtimetool) | The tools available to the model for the session. |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | The tool choice for the session. |
| temperature | number | The sampling temperature for the model. The allowed temperature values are limited to [0.6, 1.2]. Defaults to 0.8. |
| max_response_output_tokens | integer or "inf" | The maximum number of output tokens per assistant response, inclusive of tool calls.<br><br>Specify an integer between 1 and 4096 to limit the output tokens. Otherwise, set the value to "inf" to allow the maximum number of tokens.<br><br>For example, to limit the output tokens to 1000, set `"max_response_output_tokens": 1000`. To allow the maximum number of tokens, set `"max_response_output_tokens": "inf"`. |

### RealtimeResponseStatus

**Allowed Values:**

* `in_progress`
* `completed`
* `cancelled`
* `incomplete`
* `failed`

### RealtimeResponseStatusDetails

| Field | Type | Description |
|-------|------|-------------|
| type | [RealtimeResponseStatus](#realtimeresponsestatus) | The status of the response. |

#### RealtimeServerEvent

| Field | Type | Description |
|-------|------|-------------|
| type | [RealtimeServerEventType](#realtimeservereventtype) | The type of the server event. |
| event_id | string | The unique ID of the server event. |

#### RealtimeRateLimitsItem

| Field | Type | Description |
|-------|------|-------------|
| name | string | The rate limit property name that this item includes information about. |
| limit | integer | The maximum configured limit for this rate limit property. |
| remaining | integer | The remaining quota available against the configured limit for this rate limit property. |
| reset_seconds | number | The remaining time, in seconds, until this rate limit property is reset. |

#### RealtimeServerEventType

**Allowed Values:**

* `session.created`
* `session.updated`
* `conversation.created`
* `conversation.item.created`
* `conversation.item.deleted`
* `conversation.item.truncated`
* `response.created`
* `response.done`
* `rate_limits.updated`
* `response.output_item.added`
* `response.output_item.done`
* `response.content_part.added`
* `response.content_part.done`
* `response.audio.delta`
* `response.audio.done`
* `response.audio_transcript.delta`
* `response.audio_transcript.done`
* `response.text.delta`
* `response.text.done`
* `response.function_call_arguments.delta`
* `response.function_call_arguments.done`
* `input_audio_buffer.speech_started`
* `input_audio_buffer.speech_stopped`
* `conversation.item.input_audio_transcription.completed`
* `conversation.item.input_audio_transcription.failed`
* `input_audio_buffer.committed`
* `input_audio_buffer.cleared`
* `error`



## Related Resources

- [Voice Live API Quickstart Guide](./quickstart.md)
- [Audio Processing Best Practices](./audio-processing.md)
- [Avatar Integration Guide](./avatar-integration.md)
- [Function Calling Tutorial](./function-calling.md)
- [WebRTC Setup Guide](./webrtc-setup.md)
