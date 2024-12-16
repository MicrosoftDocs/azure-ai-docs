---
title: Azure OpenAI Service Realtime API Reference
titleSuffix: Azure OpenAI
description: Learn how to use the Realtime API to interact with the Azure OpenAI service in real-time.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 12/12/2024
author: eric-urban
ms.author: eur
recommendations: false
---

# Realtime API (Preview) reference

[!INCLUDE [Feature preview](includes/preview-feature.md)]

The Realtime API is a WebSocket-based API that allows you to interact with the Azure OpenAI service in real-time. 

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. Device details like capturing and rendering audio data are outside the scope of the Realtime API. It should be used in the context of a trusted, intermediate service that manages both connections to end users and model endpoint connections. Don't use it directly from untrusted end user devices.

> [!TIP]
> To get started with the Realtime API, see the [quickstart](realtime-audio-quickstart.md) and [how-to guide](./how-to/realtime-audio.md).

## Connection

The Realtime API requires an existing Azure OpenAI resource endpoint in a supported region. The API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

You can construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol
- Your Azure OpenAI resource endpoint hostname, for example, `my-aoai-resource.openai.azure.com`
- The `openai/realtime` API path
- An `api-version` query string parameter for a supported API version such as `2024-10-01-preview`
- A `deployment` query string parameter with the name of your `gpt-4o-realtime-preview` model deployment

The following example is a well-constructed `/realtime` request URI:

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/realtime?api-version=2024-10-01-preview&deployment=gpt-4o-realtime-preview-1001
```

## Authentication

To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI Service resource with managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the prehandshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.

## Client events

There are nine client events that can be sent from the client to the server:

| Event | Description |
|-------|-------------|
| [RealtimeClientEventConversationItemCreate](#realtimeclienteventconversationitemcreate) | Send this client event when adding an item to the conversation. |
| [RealtimeClientEventConversationItemDelete](#realtimeclienteventconversationitemdelete) | Send this client event when you want to remove any item from the conversation history. |
| [RealtimeClientEventConversationItemTruncate](#realtimeclienteventconversationitemtruncate) | Send this client event when you want to truncate a previous assistant message's audio. |
| [RealtimeClientEventInputAudioBufferAppend](#realtimeclienteventinputaudiobufferappend) | Send this client event to append audio bytes to the input audio buffer. |
| [RealtimeClientEventInputAudioBufferClear](#realtimeclienteventinputaudiobufferclear) | Send this client event to clear the audio bytes in the buffer. |
| [RealtimeClientEventInputAudioBufferCommit](#realtimeclienteventinputaudiobuffercommit) | Send this client event to commit audio bytes to a user message. |
| [RealtimeClientEventResponseCancel](#realtimeclienteventresponsecancel) | Send this client event to cancel an in-progress response. |
| [RealtimeClientEventResponseCreate](#realtimeclienteventresponsecreate) | Send this client event to trigger a response generation. |
| [RealtimeClientEventSessionUpdate](#realtimeclienteventsessionupdate) | Send this client event to update the session's default configuration. |

### RealtimeClientEventConversationItemCreate

Add a new item to the conversation's context, including messages, function calls, and function call responses. This event can be used to populate a history of the conversation and to add new items mid-stream. Currently this event can't populate assistant audio messages.

If successful, the server responds with a `conversation.item.created` event, otherwise an `error` event is sent.

#### Event structure

```json
{
  "type": "conversation.item.create",
  "previous_item_id": "<previous_item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.create`. | **Required**<br>Allowed values: `conversation.item.create` |
| previous_item_id | string | The ID of the preceding item after which the new item is inserted. If not set, the new item is appended to the end of the conversation. If set, it allows an item to be inserted mid-conversation. If the ID can't be found, then an error is returned and the item isn't added. |  |
| item | [RealtimeConversationRequestItem](#realtimeconversationrequestitem) |  | **Required** |

### RealtimeClientEventConversationItemDelete

Send this client event when you want to remove any item from the conversation history. The server responds with a `conversation.item.deleted` event, unless the item doesn't exist in the conversation history, in which case the server responds with an error.

#### Event structure

```json
{
  "type": "conversation.item.delete",
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.delete`. | **Required**<br>Allowed values: `conversation.item.delete` |
| item_id | string | The ID of the item to delete. | **Required** |

### RealtimeClientEventConversationItemTruncate

Send this client event to truncate a previous assistant message's audio. The server produces audio faster than realtime, so this event is useful when the user interrupts to truncate audio that was sent to the client but not yet played. The server's understanding of the audio with the client's playback is synchronized.

Truncating audio deletes the server-side text transcript to ensure there isn't text in the context that the user doesn't know about.

If successful, the server responds with a `conversation.item.truncated` event.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.truncate`. | **Required**<br>Allowed values: `conversation.item.truncate` |
| item_id | string | The ID of the assistant message item to truncate. Only assistant message items can be truncated. | **Required** |
| content_index | integer | The index of the content part to truncate. Set this property to "0". | **Required** |
| audio_end_ms | integer | Inclusive duration up to which audio is truncated, in milliseconds. If the audio_end_ms is greater than the actual audio duration, the server responds with an error. | **Required** |

### RealtimeClientEventInputAudioBufferAppend

Send this client event to append audio bytes to the input audio buffer. The audio buffer is temporary storage you can write to and later commit. In Server VAD (Voice Activity Detection) mode, the audio buffer is used to detect speech and the server decides when to commit. When Server VAD is disabled, you must commit the audio buffer manually.

The client can choose how much audio to place in each event up to a maximum of 15 MiB, for example streaming smaller chunks from the client can allow the VAD to be more responsive. Unlike made other client events, the server doesn't send a confirmation response to this event.

#### Event structure

```json
{
  "type": "input_audio_buffer.append",
  "audio": "<audio>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.append`. | **Required**<br>Allowed values: `input_audio_buffer.append` |
| audio | string | Base64-encoded audio bytes. This value must be in the format specified by the `input_audio_format` field in the session configuration. | **Required** |

### RealtimeClientEventInputAudioBufferClear

Send this client event to clear the audio bytes in the buffer. The server responds with an `input_audio_buffer.cleared` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.clear"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.clear`. | **Required**<br>Allowed values: `input_audio_buffer.clear` |

### RealtimeClientEventInputAudioBufferCommit

Send this client event to commit the user input audio buffer, which creates a new user message item in the conversation. This event produces an error if the input audio buffer is empty. When in server VAD mode, the client doesn't need to send this event, the server commits the audio buffer automatically.

Committing the input audio buffer triggers input audio transcription (if enabled in session configuration), but it doesn't create a response from the model. The server responds with an `input_audio_buffer.committed` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.commit"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.commit`. | **Required**<br>Allowed values: `input_audio_buffer.commit` |

### RealtimeClientEventResponseCancel

Send this client event to cancel an in-progress response. The server responds with a `response.cancelled` event or an error if there's no response to cancel.

#### Event structure

```json
{
  "type": "response.cancel"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.cancel`. | **Required**<br>Allowed values: `response.cancel` |

### RealtimeClientEventResponseCreate

This event instructs the server to create a response, which means triggering model inference. When in server VAD mode, the server creates responses automatically.

A response includes at least one item, and can have two, in which case the second is a function call. These items are appended to the conversation history.

The server responds with a `response.created` event, events for items and content created, and finally a `response.done` event to indicate the response is complete.

The `response.create` event includes inference configuration like 
`instructions`, and `temperature`. These fields override the session's configuration for this response only.

#### Event structure

```json
{
  "type": "response.create"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.create`. | **Required**<br>Allowed values: `response.create` |
| response | [RealtimeResponseOptions](#realtimeresponseoptions) |  | **Required** |

### RealtimeClientEventSessionUpdate

Send this client event to update the session's default configuration. The client can send this event at any time to update the session configuration, and any field can be updated at any time, except for voice. The server responds with a `session.updated` event that shows the full effective configuration. 

Only fields that are present are updated, thus the correct way to clear a field like "instructions" is to pass an empty string.

#### Event structure

```json
{
  "type": "session.update"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `session.update`. | **Required**<br>Allowed values: `session.update` |
| session | [RealtimeRequestSession](#realtimerequestsession) |  | **Required** |

## Server events

There are 28 server events that can be received from the server:

| Event | Description |
|-------|-------------|
| [RealtimeServerEventConversationCreated](#realtimeservereventconversationcreated) | Server event when a conversation is created. Emitted right after session creation. |
| [RealtimeServerEventConversationItemCreated](#realtimeservereventconversationitemcreated) | Server event when a conversation item is created. |
| [RealtimeServerEventConversationItemDeleted](#realtimeservereventconversationitemdeleted) | Server event when an item in the conversation is deleted. |
| [RealtimeServerEventConversationItemInputAudioTranscriptionCompleted](#realtimeservereventconversationiteminputaudiotranscriptioncompleted) | Server event when input audio transcription is enabled and a transcription succeeds. |
| [RealtimeServerEventConversationItemInputAudioTranscriptionFailed](#realtimeservereventconversationiteminputaudiotranscriptionfailed) | Server event when input audio transcription is configured, and a transcription request for a user message failed. |
| [RealtimeServerEventConversationItemTruncated](#realtimeservereventconversationitemtruncated) | Server event when the client truncates an earlier assistant audio message item. |
| [RealtimeServerEventError](#realtimeservereventerror) | Server event when an error occurs. |
| [RealtimeServerEventInputAudioBufferCleared](#realtimeservereventinputaudiobuffercleared) | Server event when the client clears the input audio buffer. |
| [RealtimeServerEventInputAudioBufferCommitted](#realtimeservereventinputaudiobuffercommitted) | Server event when an input audio buffer is committed, either by the client or automatically in server VAD mode. |
| [RealtimeServerEventInputAudioBufferSpeechStarted](#realtimeservereventinputaudiobufferspeechstarted) | Server event in server turn detection mode when speech is detected. |
| [RealtimeServerEventInputAudioBufferSpeechStopped](#realtimeservereventinputaudiobufferspeechstopped) | Server event in server turn detection mode when speech stops. |
| [RealtimeServerEventRateLimitsUpdated](#realtimeservereventratelimitsupdated) | Emitted after every "response.done" event to indicate the updated rate limits. |
| [RealtimeServerEventResponseAudioDelta](#realtimeservereventresponseaudiodelta) | Server event when the model-generated audio is updated. |
| [RealtimeServerEventResponseAudioDone](#realtimeservereventresponseaudiodone) | Server event when the model-generated audio is done. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventResponseAudioTranscriptDelta](#realtimeservereventresponseaudiotranscriptdelta) | Server event when the model-generated transcription of audio output is updated. |
| [RealtimeServerEventResponseAudioTranscriptDone](#realtimeservereventresponseaudiotranscriptdone) | Server event when the model-generated transcription of audio output is done streaming. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventResponseContentPartAdded](#realtimeservereventresponsecontentpartadded) | Server event when a new content part is added to an assistant message item during response generation. |
| [RealtimeServerEventResponseContentPartDone](#realtimeservereventresponsecontentpartdone) | Server event when a content part is done streaming in an assistant message item. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventResponseCreated](#realtimeservereventresponsecreated) | Server event when a new Response is created. The first event of response creation, where the response is in an initial state of "in_progress". |
| [RealtimeServerEventResponseDone](#realtimeservereventresponsedone) | Server event when a response is done streaming. Always emitted, no matter the final state. |
| [RealtimeServerEventResponseFunctionCallArgumentsDelta](#realtimeservereventresponsefunctioncallargumentsdelta) | Server event when the model-generated function call arguments are updated. |
| [RealtimeServerEventResponseFunctionCallArgumentsDone](#realtimeservereventresponsefunctioncallargumentsdone) | Server event when the model-generated function call arguments are done streaming. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventResponseOutputItemAdded](#realtimeservereventresponseoutputitemadded) | Server event when a new output item is added to a response. |
| [RealtimeServerEventResponseOutputItemDone](#realtimeservereventresponseoutputitemdone) | Server event when an output item is done streaming. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventResponseTextDelta](#realtimeservereventresponsetextdelta) | Server event when the model-generated text is updated. |
| [RealtimeServerEventResponseTextDone](#realtimeservereventresponsetextdone) | Server event when the model-generated text is done. Also emitted when a response is interrupted, incomplete, or cancelled. |
| [RealtimeServerEventSessionCreated](#realtimeservereventsessioncreated) | Server event when a session is created. |
| [RealtimeServerEventSessionUpdated](#realtimeservereventsessionupdated) | Server event when a session is updated. |

### RealtimeServerEventConversationCreated

Server event when a conversation is created. Emitted right after session creation.

#### Event structure

```json
{
  "type": "conversation.created",
  "conversation": {
    "id": "<id>",
    "object": "<object>"
  }
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.created`. | **Required**<br>Allowed values: `conversation.created` |
| conversation | object | The conversation resource. | **Required**<br>See nested properties next.|

#### Conversation properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| id | string | The unique ID of the conversation. |  |
| object | string | The object type must be `realtime.conversation`. |  |

### RealtimeServerEventConversationItemCreated

Server event when a conversation item is created. There are several scenarios that produce this event:
  - The server is generating a response, which if successful produces either one or two items, which is of type `message` (role `assistant`) or type `function_call`.
  - The input audio buffer is committed, either by the client or the server (in `server_vad` mode). The server takes the content of the input audio buffer and adds it to a new user message item.
  - The client sent a `conversation.item.create` event to add a new item to the conversation.

#### Event structure

```json
{
  "type": "conversation.item.created",
  "previous_item_id": "<previous_item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.created`. | **Required**<br>Allowed values: `conversation.item.created` |
| previous_item_id | string | The ID of the preceding item in the conversation context, allows the client to understand the order of the conversation. | **Required** |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) |  | **Required** |

### RealtimeServerEventConversationItemDeleted

Server event when the client deleted an item in the conversation with a `conversation.item.delete` event. This event is used to synchronize the server's understanding of the conversation history with the client's view.

#### Event structure

```json
{
  "type": "conversation.item.deleted",
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.deleted`. | **Required**<br>Allowed values: `conversation.item.deleted` |
| item_id | string | The ID of the item that was deleted. | **Required** |

### RealtimeServerEventConversationItemInputAudioTranscriptionCompleted

This server event is the output of audio transcription for user audio written to the user audio buffer. Transcription begins when the input audio buffer is committed by the client or server (in `server_vad` mode). Transcription runs asynchronously with response creation, so this event can come before or after the response events.

Realtime API models accept audio natively, and thus input transcription is a separate process run on a separate Automatic Speech Recognition (ASR) model, currently always `whisper-1`. Thus the transcript can diverge somewhat from the model's interpretation, and should be treated as a rough guide.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.completed`. | **Required**<br>Allowed values: `conversation.item.input_audio_transcription.completed` |
| item_id | string | The ID of the user message item containing the audio. | **Required** |
| content_index | integer | The index of the content part containing the audio. | **Required** |
| transcript | string | The transcribed text. | **Required** |

### RealtimeServerEventConversationItemInputAudioTranscriptionFailed

Server event when input audio transcription is configured, and a transcription request for a user message failed. These events are separate from other `error` events so that the client can identify the related item.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.failed`. | **Required**<br>Allowed values: `conversation.item.input_audio_transcription.failed` |
| item_id | string | The ID of the user message item. | **Required** |
| content_index | integer | The index of the content part containing the audio. | **Required** |
| error | object | Details of the transcription error. | **Required**<br>See nested properties next.|

#### Error properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The type of error. |  |
| code | string | Error code, if any. |  |
| message | string | A human-readable error message. |  |
| param | string | Parameter related to the error, if any. |  |

### RealtimeServerEventConversationItemTruncated

Server event when the client truncates an earlier assistant audio message item with a `conversation.item.truncate` event. This event is used to synchronize the server's understanding of the audio with the client's playback.

This action truncates the audio and removes the server-side text transcript to ensure there's no text in the context that the user doesn't know about.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `conversation.item.truncated`. | **Required**<br>Allowed values: `conversation.item.truncated` |
| item_id | string | The ID of the assistant message item that was truncated. | **Required** |
| content_index | integer | The index of the content part that was truncated. | **Required** |
| audio_end_ms | integer | The duration up to which the audio was truncated, in milliseconds. | **Required** |

### RealtimeServerEventError

Server event when an error occurs, which could be a client problem or a server problem. Most errors are recoverable and the session stays open. 

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `error`. | **Required**<br>Allowed values: `error` |
| error | object | Details of the error. | **Required**<br>See nested properties next.|

#### Error properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The type of error (for example, "invalid_request_error", "server_error"). |  |
| code | string | Error code, if any. |  |
| message | string | A human-readable error message. |  |
| param | string | Parameter related to the error, if any. |  |
| event_id | string | The ID of the client event that caused the error, if applicable. |  |

### RealtimeServerEventInputAudioBufferCleared

Server event when the client clears the input audio buffer with a `input_audio_buffer.clear` event.

#### Event structure

```json
{
  "type": "input_audio_buffer.cleared"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.cleared`. | **Required**<br>Allowed values: `input_audio_buffer.cleared` |

### RealtimeServerEventInputAudioBufferCommitted

Server event when an input audio buffer is committed, either by the client or automatically in server VAD mode. The `item_id` property is the ID of the user message item created. Thus a `conversation.item.created` event is also sent to the client.

#### Event structure

```json
{
  "type": "input_audio_buffer.committed",
  "previous_item_id": "<previous_item_id>",
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.committed`. | **Required**<br>Allowed values: `input_audio_buffer.committed` |
| previous_item_id | string | The ID of the preceding item after which the new item is inserted. | **Required** |
| item_id | string | The ID of the user message item created. | **Required** |

### RealtimeServerEventInputAudioBufferSpeechStarted

Server event when in `server_vad` mode to indicate that speech is detected in the audio buffer. This event can happen any time audio is added to the buffer (unless speech is already detected). The client can want to use this event to interrupt audio playback or provide visual feedback to the user. 

The client should expect to receive a `input_audio_buffer.speech_stopped` event when speech stops. The `item_id` property is the ID of the user message item created when speech stops and is also included in the `input_audio_buffer.speech_stopped` event (unless the client manually commits the audio buffer during VAD activation).

#### Event structure

```json
{
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 0,
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.speech_started`. | **Required**<br>Allowed values: `input_audio_buffer.speech_started` |
| audio_start_ms | integer | Milliseconds from the start of all audio written to the buffer during the session when speech was first detected. This property corresponds to the beginning of audio sent to the model, and thus includes the `prefix_padding_ms` configured in the session. | **Required** |
| item_id | string | The ID of the user message item created when speech stops. | **Required** | 

### RealtimeServerEventInputAudioBufferSpeechStopped

Server event in `server_vad` mode when the server detects the end of speech in 
the audio buffer. The server also sends an `conversation.item.created` 
event with the user message item created from the audio buffer.

#### Event structure

```json
{
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 0,
  "item_id": "<item_id>"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `input_audio_buffer.speech_stopped`. | **Required**<br>Allowed values: `input_audio_buffer.speech_stopped` |
| audio_end_ms | integer | Milliseconds since the session started when speech stopped. This property corresponds to the end of audio sent to the model, and thus includes the `min_silence_duration_ms` configured in the session. | **Required** |
| item_id | string | The ID of the user message item created. | **Required** |

### RealtimeServerEventRateLimitsUpdated

Server event emitted at the beginning of a response to indicate the updated rate limits. 

When a response is created some tokens are "reserved" for the output tokens, the rate limits shown here reflect that reservation, which is then adjusted accordingly once the response is completed.

#### Event structure

```json
{
  "type": "rate_limits.updated"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `rate_limits.updated`. | **Required**<br>Allowed values: `rate_limits.updated` |
| rate_limits | array | List of rate limit information. | **Required**<br>Array items: [RealtimeServerEventRateLimitsUpdatedRateLimitsItem](#realtimeservereventratelimitsupdatedratelimitsitem) |

### RealtimeServerEventRateLimitsUpdatedRateLimitsItem

#### Event structure

```json
{
  "name": "<name>",
  "limit": 0,
  "remaining": 0
}
```

#### Properties

| Field | Type | Description | 
|------|------|-------------| 
| name | string | The rate limit property name that this item includes information about. | 
| limit | integer | The maximum configured limit for this rate limit property. | 
| remaining | integer | The remaining quota available against the configured limit for this rate limit property. | 
| reset_seconds | number | The remaining time, in seconds, until this rate limit property is reset. | 

### RealtimeServerEventResponseAudioDelta

Returned when the model-generated audio is updated.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.audio.delta`. | **Required**<br>Allowed values: `response.audio.delta` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| delta | string | Base64-encoded audio data delta. | **Required** |

### RealtimeServerEventResponseAudioDone

Server event when the model-generated audio is done. Also emitted when a response is interrupted, incomplete, or cancelled.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.audio.done`. | **Required**<br>Allowed values: `response.audio.done` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |

### RealtimeServerEventResponseAudioTranscriptDelta

Server event when the model-generated transcription of audio output is updated.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.audio_transcript.delta`. | **Required**<br>Allowed values: `response.audio_transcript.delta` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| delta | string | The transcript delta. | **Required** |

### RealtimeServerEventResponseAudioTranscriptDone

Server event when the model-generated transcription of audio output is done streaming. Also emitted when a response is interrupted, incomplete, or cancelled.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.audio_transcript.done`. | **Required**<br>Allowed values: `response.audio_transcript.done` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| transcript | string | The final transcript of the audio. | **Required** |

### RealtimeServerEventResponseContentPartAdded

Server event when a new content part is added to an assistant message item during response generation.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.content_part.added`. | **Required**<br>Allowed values: `response.content_part.added` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item to which the content part was added. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| part | [RealtimeContentPart](#realtimecontentpart) | The content part that was added. | **Required** |

#### Part properties

| Field | Type | Description | 
|------|------|-------------| 
| type | [RealtimeContentPartType](#realtimecontentparttype) |  | 

### RealtimeServerEventResponseContentPartDone

Server event when a content part is done streaming in an assistant message item. Also emitted when a response is interrupted, incomplete, or cancelled.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.content_part.done`. | **Required**<br>Allowed values: `response.content_part.done` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| part | [RealtimeContentPart](#realtimecontentpart) | The content part that is done. | **Required** | 

#### Part properties

| Field | Type | Description | 
|------|------|-------------| 
| type | [RealtimeContentPartType](#realtimecontentparttype) |  | 

### RealtimeServerEventResponseCreated

Server event when a new response is created. The first event of response creation,where  the response is in an initial state of `in_progress`.

#### Event structure

```json
{
  "type": "response.created"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.created`. | **Required**<br>Allowed values: `response.created` |
| response | [RealtimeResponse](#realtimeresponse) |  | **Required** |

### RealtimeServerEventResponseDone

Server event when a response is done streaming. Always emitted, no matter the final state. The response object included in the `response.done` event includes all output items in the response but omits the raw audio data.

#### Event structure

```json
{
  "type": "response.done"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.done`. | **Required**<br>Allowed values: `response.done` |
| response | [RealtimeResponse](#realtimeresponse) |  | **Required** |

### RealtimeServerEventResponseFunctionCallArgumentsDelta

Server event when the model-generated function call arguments are updated.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.function_call_arguments.delta`. | **Required**<br>Allowed values: `response.function_call_arguments.delta` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the function call item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| call_id | string | The ID of the function call. | **Required** |
| delta | string | The arguments delta as a JSON string. | **Required** |

### RealtimeServerEventResponseFunctionCallArgumentsDone

Server event when the model-generated function call arguments are done streaming.

Also emitted when a response is interrupted, incomplete, or cancelled.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.function_call_arguments.done`. | **Required**<br>Allowed values: `response.function_call_arguments.done` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the function call item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| call_id | string | The ID of the function call. | **Required** |
| arguments | string | The final arguments as a JSON string. | **Required** |

### RealtimeServerEventResponseOutputItemAdded

Server event when a new item is created during response generation.

#### Event structure

```json
{
  "type": "response.output_item.added",
  "response_id": "<response_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.output_item.added`. | **Required**<br>Allowed values: `response.output_item.added` |
| response_id | string | The ID of the response to which the item belongs. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) |  | **Required** | 

### RealtimeServerEventResponseOutputItemDone

Server event when an item is done streaming. Also emitted when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "type": "response.output_item.done",
  "response_id": "<response_id>",
  "output_index": 0
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.output_item.done`. | **Required**<br>Allowed values: `response.output_item.done` |
| response_id | string | The ID of the response to which the item belongs. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| item | [RealtimeConversationResponseItem](#realtimeconversationresponseitem) |  | **Required** |

### RealtimeServerEventResponseTextDelta

Server event event when the text value of a "text" content part is updated.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.text.delta`. | **Required**<br>Allowed values: `response.text.delta` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| delta | string | The text delta. | **Required** |

### RealtimeServerEventResponseTextDone

Server event when the text value of a "text" content part is done streaming. Also
emitted when a response is interrupted, incomplete, or cancelled.

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

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `response.text.done`. | **Required**<br>Allowed values: `response.text.done` |
| response_id | string | The ID of the response. | **Required** |
| item_id | string | The ID of the item. | **Required** |
| output_index | integer | The index of the output item in the response. | **Required** |
| content_index | integer | The index of the content part in the item's content array. | **Required** |
| text | string | The final text content. | **Required** |

### RealtimeServerEventSessionCreated

Server event when a session is created. Emitted automatically when a new 
connection is established as the first server event. This event contains 
the default session configuration.

#### Event structure

```json
{
  "type": "session.created"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `session.created`. | **Required**<br>Allowed values: `session.created` |
| session | [RealtimeResponseSession](#realtimeresponsesession) |  | **Required** |

### RealtimeServerEventSessionUpdated

Server event when a session is updated with a `session.update` event, unless 
there's an error.

#### Event structure

```json
{
  "type": "session.updated"
}
```

#### Properties

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string | The event type must be `session.updated`. | **Required**<br>Allowed values: `session.updated` |
| session | [RealtimeResponseSession](#realtimeresponsesession) |  | **Required** |

## Components

### RealtimeAudioFormat

**Allowed Values:**

* `pcm16` 
* `g711_ulaw` 
* `g711_alaw` 

### RealtimeAudioInputTranscriptionModel

**Allowed Values:**

* `whisper-1` 

### RealtimeAudioInputTranscriptionSettings

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| model | [RealtimeAudioInputTranscriptionModel](#realtimeaudioinputtranscriptionmodel) |  | Default: `whisper-1` |


### RealtimeClientEvent

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeClientEventType](#realtimeclienteventtype) |  | **Required** |
| event_id | string |  |  |

### RealtimeClientEventType

**Allowed Values:**

* `session.update` 
* `input_audio_buffer.append` 
* `input_audio_buffer.commit` 
* `input_audio_buffer.clear` 
* `conversation.item.create` 
* `conversation.item.delete` 
* `conversation.item.truncate` 
* `response.create` 
* `response.cancel` 

### RealtimeContentPart

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeContentPartType](#realtimecontentparttype) |  | **Required** |

### RealtimeContentPartType

**Allowed Values:**

* `input_text` 
* `input_audio` 
* `text` 
* `audio` 

### RealtimeConversationItemBase

The item to add to the conversation.

### RealtimeConversationRequestItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeItemType](#realtimeitemtype) |  | **Required** |
| id | string |  |  |

### RealtimeConversationResponseItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| object | string |  | **Required**<br>Allowed values: `realtime.item` |
| type | [RealtimeItemType](#realtimeitemtype) |  | **Required** |
| id | string |  | **Required**<br>This property is nullable. |

### RealtimeFunctionTool

The definition of a function tool as used by the realtime endpoint.

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function` |
| name | string |  | **Required** |
| description | string |  |  |
| parameters |  |  |  |

### RealtimeItemStatus

**Allowed Values:**

* `in_progress` 
* `completed` 
* `incomplete` 

### RealtimeItemType

**Allowed Values:**

* `message` 
* `function_call` 
* `function_call_output` 

### RealtimeMessageRole

**Allowed Values:**

* `system` 
* `user` 
* `assistant` 

### RealtimeRequestAssistantMessageItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| role | string |  | **Required**<br>Allowed values: `assistant` |
| content | array |  | **Required**<br>Array items: [RealtimeRequestTextContentPart](#realtimerequesttextcontentpart) |

### RealtimeRequestAudioContentPart

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `input_audio` |
| transcript | string |  |  |

### RealtimeRequestFunctionCallItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function_call` |
| name | string |  | **Required** |
| call_id | string |  | **Required** |
| arguments | string |  | **Required** |
| status | [RealtimeItemStatus](#realtimeitemstatus) |  |  |

### RealtimeRequestFunctionCallOutputItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function_call_output` |
| call_id | string |  | **Required** |
| output | string |  | **Required** |

### RealtimeRequestMessageItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `message` |
| role | [RealtimeMessageRole](#realtimemessagerole) |  | **Required** |
| status | [RealtimeItemStatus](#realtimeitemstatus) |  |  |

### RealtimeRequestMessageReferenceItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `message` |
| id | string |  | **Required** |

### RealtimeRequestSession

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| modalities | array |  |  |
| instructions | string |  |  |
| voice | [RealtimeVoice](#realtimevoice) |  |  |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) |  |  |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) |  |  |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) |  | Nullable |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) |  | Nullable |
| tools | array |  | Array items: [RealtimeTool](#realtimetool) |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) |  |  |
| temperature | number |  |  |
| max_response_output_tokens |  |  |  |

### RealtimeRequestSystemMessageItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| role | string |  | **Required**<br>Allowed values: `system` |
| content | array |  | **Required**<br>Array items: [RealtimeRequestTextContentPart](#realtimerequesttextcontentpart) |

### RealtimeRequestTextContentPart

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `input_text` |
| text | string |  | **Required** |

### RealtimeRequestUserMessageItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| role | string |  | **Required**<br>Allowed values: `user` |
| content | array |  | **Required**<br>Array items can be: [RealtimeRequestTextContentPart](#realtimerequesttextcontentpart) or [RealtimeRequestAudioContentPart](#realtimerequestaudiocontentpart) |

### RealtimeResponse

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| object | string |  | **Required**<br>Allowed values: `realtime.response` |
| id | string |  | **Required** |
| status | [RealtimeResponseStatus](#realtimeresponsestatus) |  | **Required**<br>Default: `in_progress` |
| status_details | [RealtimeResponseStatusDetails](#realtimeresponsestatusdetails) |  | **Required**<br>This property is nullable. |
| output | array |  | **Required**<br>Array items: [RealtimeConversationResponseItem](#realtimeconversationresponseitem) |
| usage | object |  | **Required**<br>See nested properties next.|
| + total_tokens | integer | A property of the `usage` object. | **Required** |
| + input_tokens | integer | A property of the `usage` object. | **Required** |
| + output_tokens | integer | A property of the `usage` object. | **Required** |
| + input_token_details | object | A property of the `usage` object. | **Required**<br>See nested properties next.|
| + cached_tokens | integer | A property of the `input_token_details` object. | **Required** |
| + text_tokens | integer | A property of the `input_token_details` object. | **Required** |
| + audio_tokens | integer | A property of the `input_token_details` object. | **Required** |
| + output_token_details | object | A property of the `usage` object. | **Required**<br>See nested properties next.|
| + text_tokens | integer | A property of the `output_token_details` object. | **Required** |
| + audio_tokens | integer | A property of the `output_token_details` object. | **Required** |

### RealtimeResponseAudioContentPart

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `audio` |
| transcript | string |  | **Required**<br>This property is nullable. |

### RealtimeResponseBase

The response resource.

### RealtimeResponseFunctionCallItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function_call` |
| name | string |  | **Required** |
| call_id | string |  | **Required** |
| arguments | string |  | **Required** |
| status | [RealtimeItemStatus](#realtimeitemstatus) |  | **Required** |

### RealtimeResponseFunctionCallOutputItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function_call_output` |
| call_id | string |  | **Required** |
| output | string |  | **Required** |

### RealtimeResponseMessageItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `message` |
| role | [RealtimeMessageRole](#realtimemessagerole) |  | **Required** |
| content | array |  | **Required**<br>Array items: [RealtimeContentPart](#realtimecontentpart) |
| status | [RealtimeItemStatus](#realtimeitemstatus) |  | **Required** |

### RealtimeResponseOptions

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| modalities | array | The modalities for the response. |  |
| instructions | string | Instructions for the model. |  |
| voice | [RealtimeVoice](#realtimevoice) | The voice the model uses to respond - one of `alloy`, `echo`, or `shimmer`. |  |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) | The format of output audio. |  |
| tools | array | Tools (functions) available to the model. | Array items: [RealtimeTool](#realtimetool) |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) | How the model chooses tools. |  |
| temperature | number | Sampling temperature. |  |
| max_output_tokens |  | Maximum number of output tokens for a single assistant response, inclusive of tool calls. Provide an integer between 1 and 4096 to limit output tokens, or "inf" for the maximum available tokens for a given model. Defaults to "inf". |  |

### RealtimeResponseSession

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| object | string |  | **Required**<br>Allowed values: `realtime.session` |
| id | string |  | **Required** |
| model | string |  | **Required** |
| modalities | array |  | **Required** |
| instructions | string |  | **Required** |
| voice | [RealtimeVoice](#realtimevoice) |  | **Required** |
| input_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) |  | **Required** |
| output_audio_format | [RealtimeAudioFormat](#realtimeaudioformat) |  | **Required** |
| input_audio_transcription | [RealtimeAudioInputTranscriptionSettings](#realtimeaudioinputtranscriptionsettings) |  | **Required**<br>This property is nullable. |
| turn_detection | [RealtimeTurnDetection](#realtimeturndetection) |  | **Required** |
| tools | array |  | **Required**<br>Array items: [RealtimeTool](#realtimetool) |
| tool_choice | [RealtimeToolChoice](#realtimetoolchoice) |  | **Required** |
| temperature | number |  | **Required** |
| max_response_output_tokens |  |  | **Required**<br>This property is nullable. |

### RealtimeResponseStatus

**Allowed Values:**

* `in_progress` 
* `completed` 
* `cancelled` 
* `incomplete` 
* `failed` 

### RealtimeResponseStatusDetails

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeResponseStatus](#realtimeresponsestatus) |  | **Required** |

### RealtimeResponseTextContentPart

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `text` |
| text | string |  | **Required** |

### RealtimeServerEvent

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeServerEventType](#realtimeservereventtype) |  | **Required** |
| event_id | string |  | **Required** |

### RealtimeServerEventRateLimitsUpdatedRateLimitsItem

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| name | string | The rate limit property name that this item includes information about. | **Required** |
| limit | integer | The maximum configured limit for this rate limit property. | **Required** |
| remaining | integer | The remaining quota available against the configured limit for this rate limit property. | **Required** |
| reset_seconds | number | The remaining time, in seconds, until this rate limit property is reset. | **Required** |

### RealtimeServerEventType

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

### RealtimeServerVadTurnDetection

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `server_vad` |
| threshold | number |  | Default: `0.5` |
| prefix_padding_ms | string |  |  |
| silence_duration_ms | string |  |  |

### RealtimeSessionBase

Realtime session object configuration.

### RealtimeTool

The base representation of a realtime tool definition.

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeToolType](#realtimetooltype) |  | **Required** |

### RealtimeToolChoice

The combined set of available representations for a realtime tool_choice parameter, encompassing both string literal options like 'auto' and structured references to defined tools.

### RealtimeToolChoiceFunctionObject

The representation of a realtime tool_choice selecting a named function tool.

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | string |  | **Required**<br>Allowed values: `function` |
| function | object |  | **Required**<br>See nested properties next.|
| + name | string | A property of the `function` object. | **Required** |

### RealtimeToolChoiceLiteral

The available set of mode-level, string literal tool_choice options for the realtime endpoint.

**Allowed Values:**

* `auto` 
* `none` 
* `required` 

### RealtimeToolChoiceObject

A base representation for a realtime tool_choice selecting a named tool.

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeToolType](#realtimetooltype) |  | **Required** |

### RealtimeToolType

The supported tool type discriminators for realtime tools.
Currently, only 'function' tools are supported.

**Allowed Values:**

* `function` 

### RealtimeTurnDetection

| Field | Type | Description | More Info |
|-------|------|-------------|----------------|
| type | [RealtimeTurnDetectionType](#realtimeturndetectiontype) |  | **Required** |

### RealtimeTurnDetectionType

**Allowed Values:**

* `server_vad` 

### RealtimeVoice

**Allowed Values:**

* `alloy` 
* `shimmer` 
* `echo` 

## Related content

* Get started with the [Realtime API quickstart](./realtime-audio-quickstart.md).
* Learn more about [How to use the Realtime API](./how-to/realtime-audio.md).
