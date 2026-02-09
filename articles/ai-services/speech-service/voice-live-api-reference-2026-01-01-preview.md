---
title: Voice Live API Reference 2026-01-01-preview
titleSuffix: Foundry Tools
description: Complete reference for the Voice Live API events, models, and configuration options. Version 2026-01-01-preview
manager: nitinme
ms.service: azure-ai-services
ms.topic: reference
ms.date: 1/30/2026
author: PatrickFarley
ms.author: pafarley
---

# Voice Live `2026-01-01-preview` API Reference (preview)

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
| [session.update](#sessionupdate) | Update the session configuration including voice, modalities, turn detection, and other settings |
| [session.avatar.connect](#sessionavatarconnect) | Establish avatar connection by providing client SDP for WebRTC negotiation |
| [input_audio_buffer.append](#input_audio_bufferappend) | Append audio bytes to the input audio buffer |
| [input_audio_buffer.commit](#input_audio_buffercommit) | Commit the input audio buffer for processing |
| [input_audio_buffer.clear](#input_audio_bufferclear) | Clear the input audio buffer |
| [conversation.item.create](#conversationitemcreate) | Add a new item to the conversation context |
| [conversation.item.retrieve](#conversationitemretrieve) | Retrieve a specific item from the conversation |
| [conversation.item.truncate](#conversationitemtruncate) | Truncate an assistant audio message |
| [conversation.item.delete](#conversationitemdelete) | Remove an item from the conversation |
| [response.create](#responsecreate) | Instruct the server to create a response via model inference |
| [response.cancel](#responsecancel) | Cancel an in-progress response |

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
| client_sdp | string | The client's SDP offer for WebRTC connection establishment, encoded with base64 |

### input_audio_buffer.append

Append audio bytes to the input audio buffer.

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

Commit the input audio buffer for processing.

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

Clear the input audio buffer.

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
| item | [RealtimeConversationRequestItem](#realtimeconversationrequestitem) | The item to add to the conversation |

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

#### Example with Function Call output

```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"location\": \"San Francisco\", \"temperature\": \"70\"}"
  }
}
```

#### Example with MCP approval response
```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "mcp_approval_response",
    "approval_request_id": "mcp_approval_req_456",
    "approve": true,
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

### input_audio_buffer.append

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

### input_audio_buffer.clear

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

### input_audio_buffer.commit

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

## Server Events

The Voice Live API sends the following server events to communicate status, responses, and data to the client:

| Event | Description |
|-------|-------------|
| [error](#error) | Indicates an error occurred during processing |
| [warning](#warning) | Indicates a warning occurred that doesn't interrupt the conversation flow |
| [session.created](#sessioncreated) | Sent when a new session is successfully established |
| [session.updated](#sessionupdated) | Sent when session configuration is updated |
| [session.avatar.connecting](#sessionavatarconnecting) | Indicates avatar WebRTC connection is being established |
| [conversation.item.created](#conversationitemcreated) | Sent when a new item is added to the conversation |
| [conversation.item.retrieved](#conversationitemretrieved) | Response to conversation.item.retrieve request |
| [conversation.item.truncated](#conversationitemtruncated) | Confirms item truncation |
| [conversation.item.deleted](#conversationitemdeleted) | Confirms item deletion |
| [conversation.item.input_audio_transcription.completed](#conversationiteminput_audio_transcriptioncompleted) | Input audio transcription is complete |
| [conversation.item.input_audio_transcription.delta](#conversationiteminput_audio_transcriptiondelta) | Streaming input audio transcription |
| [conversation.item.input_audio_transcription.failed](#conversationiteminput_audio_transcriptionfailed) | Input audio transcription failed |
| [input_audio_buffer.committed](#input_audio_buffercommitted) | Input audio buffer was for processing |
| [input_audio_buffer.cleared](#input_audio_buffercleared) | Input audio buffer was cleared |
| [input_audio_buffer.speech_started](#input_audio_bufferspeech_started) | Speech detected in input audio buffer (VAD) |
| [input_audio_buffer.speech_stopped](#input_audio_bufferspeech_stopped) | Speech ended in input audio buffer (VAD) |
| [response.created](#responsecreated) | New response generation started |
| [response.done](#responsedone) | Response generation is complete |
| [response.output_item.added](#responseoutput_itemadded) | New output item added to response |
| [response.output_item.done](#responseoutput_itemdone) | Output item is complete |
| [response.content_part.added](#responsecontent_partadded) | New content part added to output item |
| [response.content_part.done](#responsecontent_partdone) | Content part is complete |
| [response.text.delta](#responsetextdelta) | Streaming text content from the model |
| [response.text.done](#responsetextdone) | Text content is complete |
| [response.audio_transcript.delta](#responseaudio_transcriptdelta) | Streaming audio transcript |
| [response.audio_transcript.done](#responseaudio_transcriptdone) | Audio transcript is complete |
| [response.audio.delta](#responseaudiodelta) | Streaming audio content from the model |
| [response.audio.done](#responseaudiodone) | Audio content is complete |
| [response.animation_blendshapes.delta](#responseanimation_blendshapesdelta) | Streaming animation blendshapes data |
| [response.animation_blendshapes.done](#responseanimation_blendshapesdone) | Animation blendshapes data is complete |
| [response.audio_timestamp.delta](#responseaudio_timestampdelta) | Streaming audio timestamp information |
| [response.audio_timestamp.done](#responseaudio_timestampdone) | Audio timestamp information is complete |
| [response.animation_viseme.delta](#responseanimation_visemedelta) | Streaming animation viseme data |
| [response.animation_viseme.done](#responseanimation_visemedone) | Animation viseme data is complete |
| [response.function_call_arguments.delta](#responsefunction_call_argumentsdelta) | Streaming function call arguments |
| [response.function_call_arguments.done](#responsefunction_call_argumentsdone) | Function call arguments are complete |
| [mcp_list_tools.in_progress](#mcp_list_toolsin_progress) | MCP tool listing is in progress |
| [mcp_list_tools.completed](#mcp_list_toolscompleted) | MCP tool listing is completed |
| [mcp_list_tools.failed](#mcp_list_toolsfailed) | MCP tool listing has failed |
| [response.mcp_call_arguments.delta](#responsemcp_call_argumentsdelta) | Streaming MCP call arguments |
| [response.mcp_call_arguments.done](#responsemcp_call_argumentsdone) | MCP call arguments are complete |
| [response.mcp_call.in_progress](#responsemcp_callin_progress) | MCP call is in progress |
| [response.mcp_call.completed](#responsemcp_callcompleted) | MCP call is completed |
| [response.mcp_call.failed](#responsemcp_callfailed) | MCP call has failed |
| [response.foundry_agent_call_arguments.delta](#responsefoundry_agent_call_argumentsdelta) | Streaming foundry agent call arguments |
| [response.foundry_agent_call_arguments.done](#responsefoundry_agent_call_argumentsdone) | Foundry agent call arguments are complete |
| [response.foundry_agent_call.in_progress](#responsefoundry_agent_callin_progress) | Foundry agent call is in progress |
| [response.foundry_agent_call.completed](#responsefoundry_agent_callcompleted) | Foundry agent call is completed |
| [response.foundry_agent_call.failed](#responsefoundry_agent_callfailed) | Foundry agent call has failed |

### session.created

Sent when a new session is successfully established. This is the first event received after connecting to the API.

#### Event Structure

```json
{
  "type": "session.created",
  "session": {
    "id": "sess_ABC123DEF456",
    "object": "realtime.session",
    "model": "gpt-realtime",
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
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The created conversation item |

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

### conversation.item.retrieved

Sent in response to a `conversation.item.retrieve` client event, providing the requested conversation item.

#### Event Structure

```json
{
  "type": "conversation.item.retrieved",
  "item": {
    "id": "item_ABC123",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "audio",
        "audio": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=",
        "transcript": "Hello! I'm doing well, thank you for asking. How can I help you today?"
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.retrieved"` |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The retrieved conversation item |

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

### conversation.item.deleted

Sent in response to a `conversation.item.delete` client event, confirming that the specified item was removed from the conversation.

#### Event Structure

```json
{
  "type": "conversation.item.deleted",
  "item_id": "item_ABC123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"conversation.item.deleted"` |
| item_id | string | ID of the deleted item |

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
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The output item that was added |

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
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) | The completed output item |

### response.content_part.added

The server `response.content_part.added` event is returned when a new content part is added to an assistant message item during response generation.

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

The server `response.content_part.done` event is returned when a content part is done streaming in an assistant message item.

This event is also returned when a response is interrupted, incomplete, or canceled.

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

### conversation.item.input_audio_transcription.delta

The server `conversation.item.input_audio_transcription.delta` event is returned when input audio transcription is configured, and a transcription request for a user message is in progress. This event provides partial transcription results as they become available.

#### Event structure

```json
{
  "type": "conversation.item.input_audio_transcription.delta",
  "item_id": "<item_id>",
  "content_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.delta`. |
| item_id | string | The ID of the user message item. |
| content_index | integer | The index of the content part containing the audio. |
| delta | string | The incremental transcription text. |

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

### response.animation_blendshapes.delta

The server `response.animation_blendshapes.delta` event is returned when the model generates animation blendshapes data as part of a response. This event provides incremental blendshapes data as it becomes available.

#### Event structure

```json
{
  "type": "response.animation_blendshapes.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "frame_index": 0,
  "frames": [
    [0.0, 0.1, 0.2, ..., 1.0]
    ...
  ]
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.animation_blendshapes.delta`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| frame_index | integer | Index of the first frame in this batch of frames |
| frames | array of array of float | Array of blendshape frames, each frame is an array of blendshape values |

### response.animation_blendshapes.done

The server `response.animation_blendshapes.done` event is returned when the model has finished generating animation blendshapes data as part of a response.

#### Event structure

```json
{
  "type": "response.animation_blendshapes.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.animation_blendshapes.done`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |

### response.audio_timestamp.delta

The server `response.audio_timestamp.delta` event is returned when the model generates audio timestamp data as part of a response. This event provides incremental timestamp data for output audio and text alignment as it becomes available.

#### Event structure

```json
{
  "type": "response.audio_timestamp.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "audio_offset_ms": 0,
  "audio_duration_ms": 500,
  "text": "Hello",
  "timestamp_type": "word"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio_timestamp.delta`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| audio_offset_ms | integer | Audio offset in milliseconds from the start of the audio |
| audio_duration_ms | integer | Duration of the audio segment in milliseconds |
| text | string | The text segment corresponding to this audio timestamp |
| timestamp_type | string | The type of timestamp, currently only "word" is supported |

### response.audio_timestamp.done

Sent when audio timestamp generation is complete.

#### Event Structure

```json
{
  "type": "response.audio_timestamp.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.audio_timestamp.done`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |

### response.animation_viseme.delta

The server `response.animation_viseme.delta` event is returned when the model generates animation viseme data as part of a response. This event provides incremental viseme data as it becomes available.

#### Event Structure

```json
{
  "type": "response.animation_viseme.delta",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0,
  "audio_offset_ms": 0,
  "viseme_id": 1
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.animation_viseme.delta`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |
| audio_offset_ms | integer | Audio offset in milliseconds from the start of the audio |
| viseme_id | integer | The viseme ID corresponding to the mouth shape for animation |

### response.animation_viseme.done

The server `response.animation_viseme.done` event is returned when the model has finished generating animation viseme data as part of a response.

#### Event Structure

```json
{
  "type": "response.animation_viseme.done",
  "response_id": "resp_ABC123",
  "item_id": "item_DEF456",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.animation_viseme.done`. |
| response_id | string | ID of the response |
| item_id | string | ID of the item |
| output_index | integer | Index of the item in the response |
| content_index | integer | Index of the content part |

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

### warning

The server `warning` event is returned when a warning occurs that doesn't interrupt the conversation flow. Warnings are informational and the session continues normally.

#### Event structure

```json
{
  "type": "warning",
  "warning": {
    "code": "<code>",
    "message": "<message>",
    "param": "<param>"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `warning`. |
| warning | object | Details of the warning. See nested properties in the next table. |

#### Warning properties

| Field | Type | Description |
|-------|------|-------------|
| message | string | A human-readable warning message. |
| code | string | Optional. Warning code, if any. |
| param | string | Optional. Parameter related to the warning, if any. |

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

### mcp_list_tools.in_progress

The server `mcp_list_tools.in_progress` event is returned when the service starts listing available tools from a mcp server.

#### Event structure

```json
{
  "type": "mcp_list_tools.in_progress",
  "item_id": "<mcp_list_tools_item_id>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.in_progress`. |
| item_id | string | The ID of the [MCP list tools item](#realtimeconversationmcplisttoolsitem) being processed. |

### mcp_list_tools.completed

The server `mcp_list_tools.completed` event is returned when the service completes listing available tools from a mcp server.

#### Event structure

```json
{
  "type": "mcp_list_tools.completed",
  "item_id": "<mcp_list_tools_item_id>"
}
```

##### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.completed`. |
| item_id | string | The ID of the [MCP list tools item](#realtimeconversationmcplisttoolsitem) being processed. |

### mcp_list_tools.failed

The server `mcp_list_tools.failed` event is returned when the service fails to list available tools from a mcp server.

#### Event structure

```json
{
  "type": "mcp_list_tools.failed",
  "item_id": "<mcp_list_tools_item_id>"
}
```

##### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.failed`. |
| item_id | string | The ID of the [MCP list tools item](#realtimeconversationmcplisttoolsitem) being processed. |

### response.mcp_call_arguments.delta

The server `response.mcp_call_arguments.delta` event is returned when the model-generated mcp tool call arguments are updated.

#### Event structure

```json
{
  "type": "response.mcp_call_arguments.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call_arguments.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the [mcp tool call item](#realtimeconversationmcpcallitem). |
| output_index | integer | The index of the output item in the response. |
| delta | string | The arguments delta as a JSON string. |

### response.mcp_call_arguments.done

The server `response.mcp_call_arguments.done` event is returned when the model-generated mcp tool call arguments are done streaming.

#### Event structure

```json
{
  "type": "response.mcp_call_arguments.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "arguments": "<arguments>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call_arguments.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the [mcp tool call item](#realtimeconversationmcpcallitem). |
| output_index | integer | The index of the output item in the response. |
| arguments | string | The final arguments as a JSON string. |

### response.mcp_call.in_progress

The server `response.mcp_call.in_progress` event is returned when an MCP tool call starts processing.

#### Event structure

```json
{
  "type": "response.mcp_call.in_progress",
  "item_id": "<item_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.in_progress`. |
| item_id | string | The ID of the [mcp tool call item](#realtimeconversationmcpcallitem). |
| output_index | integer | The index of the output item in the response. |

### response.mcp_call.completed

The server `response.mcp_call.completed` event is returned when an MCP tool call completes successfully.

#### Event structure

```json
{
  "type": "response.mcp_call.completed",
  "item_id": "<item_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.completed`. |
| item_id | string | The ID of the [mcp tool call item](#realtimeconversationmcpcallitem). |
| output_index | integer | The index of the output item in the response. |

### response.mcp_call.failed

The server `response.mcp_call.failed` event is returned when an MCP tool call fails.

#### Event structure

```json
{
  "type": "response.mcp_call.failed",
  "item_id": "<item_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.failed`. |
| item_id | string | The ID of the [mcp tool call item](#realtimeconversationmcpcallitem). |
| output_index | integer | The index of the output item in the response. |

### response.foundry_agent_call_arguments.delta

The server `response.foundry_agent_call_arguments.delta` event is returned when the model-generated foundry agent call arguments are updated.

#### Event structure

```json
{
  "type": "response.foundry_agent_call_arguments.delta",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "delta": "<delta>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.foundry_agent_call_arguments.delta`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the [foundry agent call item](#realtimeconversationfoundryagentcallitem). |
| output_index | integer | The index of the output item in the response. |
| delta | string | The arguments delta as a JSON string. |

### response.foundry_agent_call_arguments.done

The server `response.foundry_agent_call_arguments.done` event is returned when the model-generated foundry agent call arguments are done streaming.

#### Event structure

```json
{
  "type": "response.foundry_agent_call_arguments.done",
  "response_id": "<response_id>",
  "item_id": "<item_id>",
  "output_index": 0,
  "arguments": "<arguments>"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.foundry_agent_call_arguments.done`. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the [foundry agent call item](#realtimeconversationfoundryagentcallitem). |
| output_index | integer | The index of the output item in the response. |
| arguments | string | The final arguments as a JSON string. |

### response.foundry_agent_call.in_progress

The server `response.foundry_agent_call.in_progress` event is returned when a foundry agent call starts processing.

#### Event structure

```json
{
  "type": "response.foundry_agent_call.in_progress",
  "item_id": "<item_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.foundry_agent_call.in_progress`. |
| item_id | string | The ID of the [foundry agent call item](#realtimeconversationfoundryagentcallitem). |
| agent_response_id | string | The response ID from the foundry agent. |
| output_index | integer | The index of the output item in the response. |

### response.foundry_agent_call.completed

The server `response.foundry_agent_call.completed` event is returned when a foundry agent call completes successfully.

#### Event structure

```json
{
  "type": "response.foundry_agent_call.completed",
  "item_id": "<item_id>",
  "agent_response_id": "<agent_response_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.foundry_agent_call.completed`. |
| item_id | string | The ID of the [foundry agent call item](#realtimeconversationfoundryagentcallitem). |
| output_index | integer | The index of the output item in the response. |

### response.foundry_agent_call.failed

The server `response.foundry_agent_call.failed` event is returned when a foundry agent call fails.

#### Event structure

```json
{
  "type": "response.foundry_agent_call.failed",
  "item_id": "<item_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.foundry_agent_call.failed`. |
| item_id | string | The ID of the [foundry agent call item](#realtimeconversationfoundryagentcallitem). |
| output_index | integer | The index of the output item in the response. |

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
| model | string | The transcription model.<br>Supported with `gpt-realtime` and `gpt-realtime-mini`:<br>`whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, `gpt-4o-transcribe-diarize`.<br>Supported with **all other models** and **agents**: `azure-speech` |
| language | string | Optional language code in BCP-47 (for example, `en-US`), or ISO-639-1 (for example, `en`), or multi languages with auto detection (for example, `en,zh`).<br><br>See [Azure speech to text supported languages](./voice-live-language-support.md?tabs=speechinput#azure-speech-to-text-supported-languages) for recommended usage of this setting. |
| custom_speech | object | Optional configuration for custom speech models, only valid for `azure-speech` model. |
| phrase_list | string[] | Optional list of phrase hints to bias recognition, only valid for `azure-speech` model. |
| prompt | string | Optional prompt text to guide transcription, only valid for `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe` and `gpt-4o-transcribe-diarize` models. |

#### RealtimeInputAudioNoiseReductionSettings

This can be:

- An [RealtimeOpenAINoiseReduction](#realtimeopenainoisereduction) object
- An [RealtimeAzureDeepNoiseSuppression](#realtimeazuredeepnoisesuppression) object

#### RealtimeOpenAINoiseReduction

OpenAI noise reduction configuration with explicit type field, only available for `gpt-realtime` and `gpt-realtime-mini` models.

| Field | Type | Description |
|-------|------|-------------|
| type | string | `near_field` or `far_field` |

#### RealtimeAzureDeepNoiseSuppression

Configuration for input audio noise reduction.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure_deep_noise_suppression"` |

#### RealtimeInputAudioEchoCancellationSettings

Echo cancellation configuration for server-side audio processing.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"server_echo_cancellation"` |

### Voice Configuration

#### RealtimeVoice

Union of all supported voice configurations.

This can be:

- An [RealtimeOpenAIVoice](#realtimeopenaivoice) object
- An [RealtimeAzureVoice](#realtimeazurevoice) object

#### RealtimeOpenAIVoice

OpenAI voice configuration with explicit type field.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"openai"` |
| name | string | OpenAI voice name: `alloy`, `ash`, `ballad`, `coral`, `echo`, `sage`, `shimmer`, `verse`, `marin`, `cedar` |

#### RealtimeAzureVoice

Base for Azure voice configurations. This is a discriminated union with different types:

##### RealtimeAzureStandardVoice

Azure standard voice configuration.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-standard"` |
| name | string | Voice name (can't be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| custom_lexicon_url | string | Optional. URL to custom lexicon |
| custom_text_normalization_url | string | Optional. URL to custom text normalization |
| prefer_locales | string[] | Optional. Preferred locales<br/> Prefer locales change the accents of languages. If the value isn't set, TTS uses default accent of each language. For example when TTS speaking English, it uses the American English accent. And when speaking Spanish, it uses the Mexican Spanish accent. <br/>If set the prefer_locales to `["en-GB", "es-ES"]`, the English accent is British English and the Spanish accent is European Spanish. And TTS also able to speak other languages like French, Chinese, etc. |
| locale | string | Optional. Locale specification<br/> Enforce The locale for TTS output. If not set, TTS always uses the given locale to speak. For example set locale to `en-US`, TTS always uses American English accent to speak the text content, even the text content is in another language. And TTS will output silence if the text content is in Chinese. |
| style | string | Optional. Voice style |
| pitch | string | Optional. Pitch adjustment |
| rate | string | Optional. Speech rate adjustment |
| volume | string | Optional. Volume adjustment |

##### RealtimeAzureCustomVoice

Azure custom voice configuration (preferred for custom voices).

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-custom"` |
| name | string | Voice name (can't be empty) |
| endpoint_id | string | Endpoint ID (can't be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| custom_lexicon_url | string | Optional. URL to custom lexicon |
| custom_text_normalization_url | string | Optional. URL to custom text normalization |
| prefer_locales | string[] | Optional. Preferred locales<br/> Prefer locales change the accents of languages. If the value isn't set, TTS uses default accent of each language. For example When TTS speaking English, it uses the American English accent. And when speaking Spanish, it uses the Mexican Spanish accent. <br/>If set the prefer_locales to `["en-GB", "es-ES"]`, the English accent is British English and the Spanish accent is European Spanish. And TTS also able to speak other languages like French, Chinese, etc. |
| locale | string | Optional. Locale specification<br/> Enforce The locale for TTS output. If not set, TTS always uses the given locale to speak. For example set locale to `en-US`, TTS always uses American English accent to speak the text content, even the text content is in another language. And TTS will output silence if the text content is in Chinese. |
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

##### RealtimeAzurePersonalVoice

Azure personal voice configuration.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure-personal"` |
| name | string | Voice name (can't be empty) |
| temperature | number | Optional. Temperature between 0.0 and 1.0 |
| model | string | Underlying neural model: `DragonLatestNeural`, `PhoenixLatestNeural`, `PhoenixV2Neural` |
| custom_lexicon_url | string | Optional. URL to custom lexicon |
| custom_text_normalization_url | string | Optional. URL to custom text normalization |
| prefer_locales | string[] | Optional. Preferred locales<br/> Prefer locales change the accents of languages. If the value isn't set, TTS uses default accent of each language. For example when TTS speaking English, it uses the American English accent. And when speaking Spanish, it uses the Mexican Spanish accent. <br/>If set the prefer_locales to `["en-GB", "es-ES"]`, the English accent is British English and the Spanish accent is European Spanish. And TTS also able to speak other languages like French, Chinese, etc. |
| locale | string | Optional. Locale specification<br/> Enforce The locale for TTS output. If not set, TTS always uses the given locale to speak. For example set locale to `en-US`, TTS always uses American English accent to speak the text content, even the text content is in another language. And TTS will output silence if the text content is in Chinese. |
| pitch | string | Optional. Pitch adjustment |
| rate | string | Optional. Speech rate adjustment |
| volume | string | Optional. Volume adjustment |


### Turn Detection

#### RealtimeTurnDetection

Configuration for turn detection. This is a discriminated union supporting multiple VAD types.

##### RealtimeServerVAD

Base VAD-based turn detection.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"server_vad"` |
| threshold | number | Optional. Activation threshold (0.0-1.0) |
| prefix_padding_ms | integer | Optional. Audio padding before speech starts |
| silence_duration_ms | integer | Optional. Silence duration to detect speech end |
| end_of_utterance_detection | [RealtimeEOUDetection](#realtimeeoudetection) | Optional. End-of-utterance detection config |
| create_response | boolean | Optional. Enable or disable whether a response is generated. |
| interrupt_response | boolean | Optional. Enable or disable barge-in interruption (default: false) |
| auto_truncate | boolean | Optional. Auto-truncate on interruption (default: false) |

##### RealtimeOpenAISemanticVAD

OpenAI semantic VAD configuration which uses a model to determine when the user has finished speaking. Only available for `gpt-realtime` and `gpt-realtime-mini` models.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"semantic_vad"` |
| eagerness | string | Optional. This is a way to control how eager the model is to interrupt the user, tuning the maximum wait timeout. In transcription mode, even if the model doesn't reply, it affects how the audio is chunked.<br/>The following values are allowed:<br/>- `auto` (default) is equivalent to `medium`,<br/>- `low` lets the user take their time to speak,<br/>- `high` will chunk the audio as soon as possible.<br/><br/>If you want the model to respond more often in conversation mode, or to return transcription events faster in transcription mode, you can set eagerness to `high`.<br/>On the other hand, if you want to let the user speak uninterrupted in conversation mode, or if you would like larger transcript chunks in transcription mode, you can set eagerness to `low`. |
| create_response | boolean | Optional. Enable or disable whether a response is generated. |
| interrupt_response | boolean | Optional. Enable or disable barge-in interruption (default: false) |

##### RealtimeAzureSemanticVAD

Azure semantic VAD, which determines when the user starts and speaking using a semantic speech model, providing more robust detection in noisy environments.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure_semantic_vad"` |
| threshold | number | Optional. Activation threshold |
| prefix_padding_ms | integer | Optional. Audio padding before speech |
| silence_duration_ms | integer | Optional. Silence duration for speech end |
| end_of_utterance_detection | [RealtimeEOUDetection](#realtimeeoudetection) | Optional. EOU detection config |
| speech_duration_ms | integer | Optional. Minimum speech duration |
| remove_filler_words | boolean | Optional. Remove filler words (default: false) |
| languages | string[] | Optional. Supports English. Other languages are ignored. |
| create_response | boolean | Optional. Enable or disable whether a response is generated. |
| interrupt_response | boolean | Optional. Enable or disable barge-in interruption (default: false) |
| auto_truncate | boolean | Optional. Auto-truncate on interruption (default: false) |

##### RealtimeAzureSemanticVADMultilingual

Azure semantic VAD (default variant).

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"azure_semantic_vad_multilingual"` |
| threshold | number | Optional. Activation threshold |
| prefix_padding_ms | integer | Optional. Audio padding before speech |
| silence_duration_ms | integer | Optional. Silence duration for speech end |
| end_of_utterance_detection | [RealtimeEOUDetection](#realtimeeoudetection) | Optional. EOU detection config |
| speech_duration_ms | integer | Optional. Minimum speech duration |
| remove_filler_words | boolean | Optional. Remove filler words (default: false). |
| languages | string[] | Optional. Supports English, Spanish, French, Italian, German (DE), Japanese, Portuguese, Chinese, Korean, Hindi. Other languages are ignored. |
| create_response | boolean | Optional. Enable or disable whether a response is generated. |
| interrupt_response | boolean | Optional. Enable or disable barge-in interruption (default: false) |
| auto_truncate | boolean | Optional. Auto-truncate on interruption (default: false) |

### RealtimeEOUDetection

Azure End-of-Utterance (EOU) could indicate when the end-user stopped speaking while allowing for natural pauses. End of utterance detection can significantly reduce premature end-of-turn signals without adding user-perceivable latency.

| Field | Type | Description |
|-------|------|-------------|
| model | string | Could be `semantic_detection_v1` supporting English or `semantic_detection_v1_multilingual` supporting English, Spanish, French, Italian, German (DE), Japanese, Portuguese, Chinese, Korean, Hindi |
| threshold_level | string | Optional. Detection threshold level (`low`, `medium`, `high` and `default`), the default equals `medium` setting. With a lower setting the probability the sentence is complete will be higher. |
| timeout_ms | number | Optional. Maximum time in milliseconds to wait for more user speech. Defaults to 1000 ms. |

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
| scene | [RealtimeAvatarScene](#realtimeavatarscene) | Optional. Configuration for the avatar's zoom level, position, rotation and movement amplitude in the video frame |
| output_protocol | string | Optional. Output protocol for avatar streaming. Default is `webrtc` |
| output_audit_audio | boolean | Optional. When enabled, forwards audit audio via WebSocket for review/debugging purposes, even when avatar output is delivered via WebRTC. Default is `false` |

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

#### RealtimeAvatarScene

Configuration for avatar's zoom level, position, rotation and movement amplitude in the video frame.

| Field | Type | Description |
|-------|------|-------------|
| zoom | number | Optional. Zoom level of the avatar. Range is (0, +∞). Values less than 1 zoom out, values greater than 1 zoom in. Default is 0 |
| position_x | number | Optional. Horizontal position of the avatar. Range is [-1, 1], as a proportion of frame width. Negative values move left, positive values move right. Default is 0 |
| position_y | number | Optional. Vertical position of the avatar. Range is [-1, 1], as a proportion of frame height. Negative values move up, positive values move down. Default is 0 |
| rotation_x | number | Optional. Rotation around the X-axis (pitch). Range is [-π, π] in radians. Negative values rotate up, positive values rotate down. Default is 0 |
| rotation_y | number | Optional. Rotation around the Y-axis (yaw). Range is [-π, π] in radians. Negative values rotate left, positive values rotate right. Default is 0 |
| rotation_z | number | Optional. Rotation around the Z-axis (roll). Range is [-π, π] in radians. Negative values rotate anticlockwise, positive values rotate clockwise. Default is 0 |
| amplitude | number | Optional. Amplitude of the avatar movement. Range is (0, 1]. Values in (0, 1) mean reduced amplitude, 1 means full amplitude. Default is 0 |

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
| modalities | [RealtimeModality](#realtimemodality)[] | Optional. The supported modalities for the session. <br><br> For example, "modalities": ["text", "audio"] is the default setting that enables both text and audio modalities. To enable only text, set "modalities": ["text"]. To enable avatar output, set "modalities": ["text", "audio", "avatar"]. You can't enable only audio. |
| animation | [RealtimeAnimation](#realtimeanimation) | Optional. Animation configuration |
| voice | [RealtimeVoice](#realtimevoice) | Optional. Voice configuration |
| instructions | string | Optional. System instructions for the model. The instructions could guide the output audio if OpenAI voices are used but may not apply to Azure voices. |
| input_audio_sampling_rate | integer | Optional. Input audio sampling rate in Hz (default: 24000 for `pcm16`, 8000 for `g711_ulaw` and `g711_alaw`) |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | Optional. Input audio format (default: `pcm16`) |
| output_audio_format | [RealtimeOutputAudioFormat](#realtimeoutputaudioformat) | Optional. Output audio format (default: `pcm16`) |
| input_audio_noise_reduction | [RealtimeInputAudioNoiseReductionSettings](#realtimeinputaudionoisereductionsettings) | Configuration for input audio noise reduction. This can be set to null to turn off. Noise reduction filters audio added to the input audio buffer before it is sent to VAD and the model. Filtering the audio can improve VAD and turn detection accuracy (reducing false positives) and model performance by improving perception of the input audio.<br><br>This property is nullable.|
| input_audio_echo_cancellation | [RealtimeInputAudioEchoCancellationSettings](#realtimeinputaudioechocancellationsettings) | Configuration for input audio echo cancellation. This can be set to null to turn off. This service side echo cancellation can help improve the quality of the input audio by reducing the impact of echo and reverberation.<br><br>This property is nullable. |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) | The configuration for input audio transcription. The configuration is null (off) by default. Input audio transcription isn't native to the model, since the model consumes audio directly. Transcription runs asynchronously through the `/audio/transcriptions` endpoint and should be treated as guidance of input audio content rather than precisely what the model heard. For additional guidance to the transcription service, the client can optionally set the language and prompt for transcription.<br><br>This property is nullable. |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) | The turn detection settings for the session. This can be set to null to turn off. |
| tools | array of [RealtimeTool](#realtimetool) | The tools available to the model for the session. |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | The tool choice for the session.<br><br>Allowed values: `auto`, `none`, and `required`. Otherwise, you can specify the name of the function to use. |
| temperature | number | The sampling temperature for the model. The allowed temperature values are limited to [0.6, 1.2]. Defaults to 0.8. |
| max_response_output_tokens | integer or "inf" | The maximum number of output tokens per assistant response, inclusive of tool calls.<br><br>Specify an integer between 1 and 4096 to limit the output tokens. Otherwise, set the value to "inf" to allow the maximum number of tokens.<br><br>For example, to limit the output tokens to 1000, set `"max_response_output_tokens": 1000`. To allow the maximum number of tokens, set `"max_response_output_tokens": "inf"`.<br><br>Defaults to `"inf"`. |
| filler_response | [FillerResponseConfig](#fillerresponseconfig) | Optional. Configuration for filler response generation during latency or tool calls. |
| reasoning_effort | [ReasoningEffort](#reasoningeffort) | Optional. Constrains effort on reasoning for reasoning models. Check [Azure Foundry doc](../../ai-foundry/openai/how-to/reasoning.md#reasoning-effort) for more details. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.  |
| avatar | [RealtimeAvatarConfig](#realtimeavatarconfig) | Optional. Avatar configuration |
| output_audio_timestamp_types | [RealtimeAudioTimestampType](#realtimeaudiotimestamptype)[] | Optional. Timestamp types for output audio |

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

#### ReasoningEffort

Constrains effort on reasoning for reasoning models. Check model documentation for supported values for each model. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.

**Allowed Values:**
* `none` - No reasoning effort
* `minimal` - Minimal reasoning effort
* `low` - Low reasoning effort - faster responses with less reasoning
* `medium` - Medium reasoning effort - balanced between speed and reasoning depth
* `high` - High reasoning effort - more thorough reasoning, may take longer
* `xhigh` - Extra high reasoning effort - maximum reasoning depth

### Tool Configuration

We support two types of tools: function calling and MCP tools which allow you connect to a mcp server.

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

#### MCPTool
MCP tool configuration.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"mcp"` |
| server_label | string | Required. The label of the MCP server. |
| server_url | string | Required. The server URL of the MCP server. |
| allowed_tools | string[] | Optional. The list of allowed tool names. If not specified, all tools are allowed. |
| headers | object | Optional. Additional headers to include in MCP requests. |
| authorization | string | Optional. Authorization token for MCP requests. |
| require_approval | string or dictionary | Optional. <br/>If set to a string, The value must be `never` or `always`. <br/>If set to a dictionary, it must be in format `{"never": ["<tool_name_1>", "<tool_name_2>"], "always": ["<tool_name_3>"]}`. <br/>Default value is `always`. <br/> When set to `always`, the tool execution requires approval, [mcp_approval_request](#realtimeconversationmcpapprovalrequestitem) will be sent to client when mcp argument done, and will only be executed when [mcp_approval_response](#realtimemcpapprovalresponseitem) with `approve=true` is received. <br/>When set to `never`, the tool will be executed automatically without approval. |

#### FoundryAgentTool

Tool definition for integrating a Foundry agent as a tool. This enables a chat-supervisor pattern where a realtime-based chat agent handles basic interactions while delegating complex tasks to a more intelligent Foundry agent.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"foundry_agent"` |
| agent_name | string | Required. The name of the Foundry agent to call. |
| agent_version | string | Optional. The version of the Foundry agent to call. |
| project_name | string | Required. The name of the Foundry project containing the agent. |
| client_id | string | Optional. The client ID associated with the Foundry agent. |
| description | string | Optional. An optional description for the Foundry agent tool. If provided, it's used instead of the agent's description in Foundry portal. |
| foundry_resource_override | string | Optional. Override for the Foundry resource used to execute the agent. |
| agent_context_type | string | Optional. The context type to use when invoking the Foundry agent. Possible values: `no_context`, `agent_context`. Default is `agent_context`.<br/><br/>`no_context`: Only the current user input is sent, no context maintained.<br/><br/>`agent_context`: Agent maintains its own context (thread), only current input sent per call. |
| return_agent_response_directly | boolean | Optional. Whether to return the agent's response directly in the Voice Live response. Default is `true`. When set to `false`, the response is sent to the chat agent to rephrase. |

Example:
```json
{
  "instructions": "You are a helpful assistant. Please respond with a short message like 'working on this' before calling the agent tool.",
  "tools": [
    {
      "type": "foundry_agent",
      "agent_name": "customer-service-agent",
      "agent_version": "2",
      "project_name": "my-foundry-project",
      "description": "A helpful agent that can search online information and handle complex customer requests"
    }
  ]
}
```

### Filler Response Configuration

Filler responses allow the system to generate placeholder audio responses during latency or while tools are being executed, improving user experience by avoiding silence.

#### FillerResponseConfig

Configuration for filler response generation. This is a union type that can be one of the following:
- [BasicFillerResponseConfig](#basicfillerresponseconfig) - Static filler responses randomly selected from a list
- [LlmFillerResponseConfig](#llmfillerresponseconfig) - LLM-generated context-aware filler responses

#### BasicFillerResponseConfig

Configuration for basic/static filler response generation. Randomly selects from configured texts when any trigger condition is met.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"static_filler"` |
| triggers | [FillerTrigger](#fillertrigger)[] | Optional. List of triggers that can fire the filler. Any trigger can activate the filler (OR logic). Supported values: `latency`, `tool`. Default is `["latency"]`. |
| latency_threshold_ms | integer | Optional. Latency threshold in milliseconds before triggering filler response. Default is 2000ms. Minimum value is 0. |
| texts | string[] | Optional. List of filler text options to randomly select from. |

Example:
```json
{
  "filler_response": {
    "type": "static_filler",
    "triggers": ["latency", "tool"],
    "latency_threshold_ms": 1500,
    "texts": [
      "Let me think about that...",
      "One moment please...",
      "Working on that for you..."
    ]
  }
}
```

#### LlmFillerResponseConfig

Configuration for LLM-based filler response generation. Uses LLM to generate context-aware filler responses when any trigger condition is met.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"llm_filler"` |
| triggers | [FillerTrigger](#fillertrigger)[] | Optional. List of triggers that can fire the filler. Any trigger can activate the filler (OR logic). Supported values: `latency`, `tool`. Default is `["latency"]`. |
| latency_threshold_ms | integer | Optional. Latency threshold in milliseconds before triggering filler response. Default is 2000ms. Minimum value is 0. |
| model | string | Optional. The model to use for LLM-based filler generation. Default is `gpt-4.1-mini`. |
| instructions | string | Optional. Custom instructions for generating filler responses. If not provided, a default prompt is used. |
| max_completion_tokens | integer | Optional. Maximum number of tokens to generate for the filler response. Default is 50. Minimum value is 1. |

Example:
```json
{
  "filler_response": {
    "type": "llm_filler",
    "triggers": ["tool"],
    "latency_threshold_ms": 2000,
    "model": "gpt-4.1-mini",
    "instructions": "Generate a brief, friendly acknowledgment that you're working on the user's request.",
    "max_completion_tokens": 30
  }
}
```

#### FillerTrigger

Triggers that can activate filler response generation.

**Allowed Values:**
* `latency` - Trigger filler when response latency exceeds threshold
* `tool` - Trigger filler when a tool call is being executed

### RealtimeConversationResponseItem

This is a union type that can be one of the following:

#### RealtimeConversationUserMessageItem

User message item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"message"` |
| object | string | Must be `"conversation.item"` |
| role | string | Must be `"user"` |
| content | [RealtimeInputTextContentPart](#realtimeinputtextcontentpart) | The content of the message. |
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

#### RealtimeConversationMCPListToolsItem

MCP list tools response item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"mcp_list_tools"` |
| server_label | string | The label of the MCP server. |

#### RealtimeConversationMCPCallItem

MCP call response item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"mcp_call"` |
| server_label | string | The label of the MCP server. |
| name | string | The name of the tool to call. |
| approval_request_id | string | The approval request ID for the MCP call. |
| arguments | string | The arguments for the MCP call. |
| output | string | The output of the MCP call. |
| error | object | The error details if the MCP call failed. |

#### RealtimeConversationMCPApprovalRequestItem

MCP approval request item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"mcp_approval_request"` |
| server_label | string | The label of the MCP server. |
| name | string | The name of the tool to call. |
| arguments | string | The arguments for the MCP call. |

#### RealtimeConversationFoundryAgentCallItem

Foundry agent call response item.

| Field | Type | Description |
|-------|------|-------------|
| id | string | The unique ID of the item. |
| type | string | Must be `"foundry_agent_call"` |
| name | string | The name of the Foundry agent. |
| call_id | string | The ID of the call. |
| arguments | string | The arguments for the foundry agent call. |
| agent_response_id | string | Optional. The response ID from the foundry agent. |
| output | string | Optional. The output of the foundry agent call. |
| error | object | Optional. The error details if the foundry agent call failed. |

### RealtimeItemStatus

Status of conversation items.

**Allowed Values:**
* `in_progress` - Currently being processed
* `completed` - Successfully completed
* `incomplete` - Incomplete (interrupted or failed)

### RealtimeContentPart

Content part within a message.

#### RealtimeInputTextContentPart

Text content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be  `"input_text"` |
| text | string | The text content |

#### RealtimeOutputTextContentPart

Text content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"text"` |
| text | string | The text content |

#### RealtimeInputAudioContentPart

Audio content part.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Must be `"input_audio"` |
| audio | string | Optional. Base64-encoded audio data |
| transcript | string | Optional. Audio transcript |

#### RealtimeOutputAudioContentPart

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
| output | [RealtimeConversationResponseItem](#realtimeconversationresponseitem)[] | Optional. Output items |
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

#### RealtimeUsage

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

### RealtimeConversationRequestItem

You use the `RealtimeConversationRequestItem` object to create a new item in the conversation via the [conversation.item.create](#conversationitemcreate) event.

This is a union type that can be one of the following:

#### RealtimeSystemMessageItem

A system message item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | string | The role of the message.<br><br>Allowed values: `system` |
| content | array of [RealtimeInputTextContentPart](#realtimeinputtextcontentpart) | The content of the message. |
| id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one. |

#### RealtimeUserMessageItem

A user message item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `message` |
| role | string | The role of the message.<br><br>Allowed values: `user` |
| content | array of [RealtimeInputTextContentPart](#realtimeinputtextcontentpart) or [RealtimeInputAudioContentPart](#realtimeinputaudiocontentpart) | The content of the message. |
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

#### RealtimeMCPApprovalResponseItem

An MCP approval response item.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The type of the item.<br><br>Allowed values: `mcp_approval_response` |
| approve | boolean | Whether the MCP request is approved. |
| approval_request_id | string | The ID of the MCP approval request. |
| id | string | The unique ID of the item. The client can specify the ID to help manage server-side context. If the client doesn't provide an ID, the server generates one. |

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
| filler_response | [FillerResponseConfig](#fillerresponseconfig) | Optional. Configuration for filler response generation during latency or tool calls. |
| reasoning_effort | [ReasoningEffort](#reasoningeffort) | Optional. Constrains effort on reasoning for reasoning models. Check model documentation for supported values for each model. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response. |
| conversation | string | Controls which conversation the response is added to. The supported values are `auto` and `none`.<br><br>The `auto` value (or not setting this property) ensures that the contents of the response are added to the session's default conversation.<br><br>Set this property to `none` to create an out-of-band response where items won't be added to the default conversation. <br><br>Defaults to `"auto"` |
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
| input_audio_sampling_rate | integer | The sampling rate for the input audio. |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the input audio. |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format for the output audio. |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) | The settings for audio input transcription.<br><br>This property is nullable. |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) | The turn detection settings for the session.<br><br>This property is nullable. |
| tools | array of [RealtimeTool](#realtimetool) | The tools available to the model for the session. |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | The tool choice for the session. |
| temperature | number | The sampling temperature for the model. The allowed temperature values are limited to [0.6, 1.2]. Defaults to 0.8. |
| max_response_output_tokens | integer or "inf" | The maximum number of output tokens per assistant response, inclusive of tool calls.<br><br>Specify an integer between 1 and 4096 to limit the output tokens. Otherwise, set the value to "inf" to allow the maximum number of tokens.<br><br>For example, to limit the output tokens to 1000, set `"max_response_output_tokens": 1000`. To allow the maximum number of tokens, set `"max_response_output_tokens": "inf"`. |
| filler_response | [FillerResponseConfig](#fillerresponseconfig) | Configuration for filler response generation during latency or tool calls. |

### RealtimeResponseStatusDetails

| Field | Type | Description |
|-------|------|-------------|
| type | [RealtimeResponseStatus](#realtimeresponsestatus) | The status of the response. |

#### RealtimeRateLimitsItem

| Field | Type | Description |
|-------|------|-------------|
| name | string | The rate limit property name that this item includes information about. |
| limit | integer | The maximum configured limit for this rate limit property. |
| remaining | integer | The remaining quota available against the configured limit for this rate limit property. |
| reset_seconds | number | The remaining time, in seconds, until this rate limit property is reset. |

## Related Resources

- Try the [Voice Live quickstart](./voice-live-quickstart.md)
- Try the [Voice Live agents quickstart](./voice-live-agents-quickstart.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
