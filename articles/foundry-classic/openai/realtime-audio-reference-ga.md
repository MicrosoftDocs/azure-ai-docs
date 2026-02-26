---
title: "Audio events reference GA (classic)"
description: "Learn how to use events with the Realtime API and Voice Live API (GA version). (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: article
ms.date: 01/26/2026
author: PatrickFarley
ms.author: pafarley
recommendations: false
---

# Realtime client events reference (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Realtime events are used to communicate between the client and server in real-time audio applications. The events are sent as JSON objects over various endpoints, such as WebSockets or WebRTC. The events are used to manage the conversation, audio buffers, and responses in real-time.

You send Realtime client events to update session configuration, stream and manage input audio, manage conversation history items, and create or cancel model responses.

## Client events

There are 11 client events that you can send from the client to the server:

| Event | Description |
|-------|-------------|
| [`session.update`](#sessionupdate) | Send `session.update` to update the session configuration. |
| [`input_audio_buffer.append`](#input_audio_bufferappend) | Send `input_audio_buffer.append` to append base64 audio bytes to the input audio buffer. |
| [`input_audio_buffer.commit`](#input_audio_buffercommit) | Send `input_audio_buffer.commit` to commit the input audio buffer and create a new user message item. |
| [`input_audio_buffer.clear`](#input_audio_bufferclear) | Send `input_audio_buffer.clear` to clear the audio bytes in the input buffer. |
| [`conversation.item.create`](#conversationitemcreate) | Send `conversation.item.create` to add a new item to the conversation context (messages, function calls, and function call responses). |
| [`conversation.item.retrieve`](#conversationitemretrieve) | Send `conversation.item.retrieve` to retrieve the server representation of an item in the conversation history. |
| [`conversation.item.truncate`](#conversationitemtruncate) | Send `conversation.item.truncate` to truncate a previous assistant message’s audio and synchronize playback state. |
| [`conversation.item.delete`](#conversationitemdelete) | Send `conversation.item.delete` to remove an item from the conversation history. |
| [`response.create`](#responsecreate) | Send `response.create` to trigger model inference and create a response. |
| [`response.cancel`](#responsecancel) | Send `response.cancel` to cancel an in-progress response. |
| [`output_audio_buffer.clear`](#output_audio_bufferclear) | Send `output_audio_buffer.clear` to cut off the current audio response. This event is only applicable to WebRTC/SIP. |

### session.update

Send the client `session.update` event to update the session’s configuration. You can send this event at any time to update any field **except** `voice` and `model`. You can update `voice` only if there have been no other audio outputs yet.

When the server receives a `session.update`, it responds with a `session.updated` event that shows the full, effective configuration. Only fields present in the `session.update` are updated.

To clear fields:
- To clear `instructions`, pass an empty string.
- To clear `tools`, pass an empty array.
- To clear `turn_detection`, pass `null`.

#### Event structure

```json
{
  "type": "session.update",
  "session": {
    "type": "realtime",
    "instructions": "You are a creative assistant that helps with design tasks.",
    "tools": [
      {
        "type": "function",
        "name": "display_color_palette",
        "description": "Call this function when a user asks for a color palette.",
        "parameters": {
          "type": "object",
          "properties": {
            "theme": {
              "type": "string",
              "description": "Description of the theme for the color scheme."
            },
            "colors": {
              "type": "array",
              "description": "Array of five hex color codes based on the theme.",
              "items": {
                "type": "string",
                "description": "Hex color code"
              }
            }
          },
          "required": [
            "theme",
            "colors"
          ]
        }
      }
    ],
    "tool_choice": "auto"
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `session.update`. |
| event_id | string | Optional client-generated ID used to identify this event. This is an arbitrary string you can assign. It is passed back if there is an error with the event, but the corresponding `session.updated` event doesn't include it. |
| session | object | Update the Realtime session. Choose either a realtime session or a transcription session. |

### input_audio_buffer.append

Send the client `input_audio_buffer.append` event to append audio bytes to the input audio buffer. The audio buffer is temporary storage you can write to and later commit.

A commit creates a new user message item in the conversation history from the buffer content and clears the buffer. Input audio transcription (if enabled) is generated when you commit the buffer.

If VAD is enabled, the audio buffer is used to detect speech and the server decides when to commit. When Server VAD is disabled, you must commit the audio buffer manually. Input audio noise reduction operates on writes to the audio buffer.

You can choose how much audio to place in each event up to a maximum of 15 MiB. For example, streaming smaller chunks might allow the VAD to be more responsive.

Unlike most other client events, the server doesn't send a confirmation response to this event.

#### Event structure

```json
{
  "event_id": "event_456",
  "type": "input_audio_buffer.append",
  "audio": "Base64EncodedAudioData"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.append`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| audio | string | Base64-encoded audio bytes. This must be in the format specified by the `input_audio_format` field in the session configuration. |

### input_audio_buffer.commit

Send the client `input_audio_buffer.commit` event to commit the user input audio buffer. This creates a new user message item in the conversation.

This event produces an error if the input audio buffer is empty. When you're in Server VAD mode, you don't need to send this event because the server commits the audio buffer automatically.

Committing the input audio buffer triggers input audio transcription (if enabled in the session configuration), but it doesn't create a response from the model. The server responds with an `input_audio_buffer.committed` event.

#### Event structure

```json
{
  "event_id": "event_789",
  "type": "input_audio_buffer.commit"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.commit`. |
| event_id | string | Optional client-generated ID used to identify this event. |

### input_audio_buffer.clear

Send the client `input_audio_buffer.clear` event to clear the audio bytes in the buffer. The server responds with an `input_audio_buffer.cleared` event.

#### Event structure

```json
{
  "event_id": "event_012",
  "type": "input_audio_buffer.clear"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.clear`. |
| event_id | string | Optional client-generated ID used to identify this event. |

### conversation.item.create

Send the client `conversation.item.create` event to add a new item to the conversation's context, including messages, function calls, and function call responses.

You can use this event to populate a history of the conversation and to add new items mid-stream. This event can't populate assistant audio messages.

If successful, the server responds with a `conversation.item.created` event. Otherwise, the server sends an `error` event.

#### Event structure

```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "hi"
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.create`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| previous_item_id | string | The ID of the preceding item after which the new item is inserted. If not set, the new item is appended to the end of the conversation. If set to `root`, the new item is added to the beginning of the conversation. If set to an existing ID, it allows an item to be inserted mid-conversation. If the ID can't be found, the server returns an error and doesn't add the item. |
| item | object | A single item within a Realtime conversation. |

### conversation.item.retrieve

Send the client `conversation.item.retrieve` event to retrieve the server's representation of a specific item in the conversation history. This is useful, for example, when you want to inspect user audio after noise cancellation and VAD.

The server responds with a `conversation.item.retrieved` event unless the item doesn't exist in the conversation history. If the item doesn't exist, the server responds with an `error`.

#### Event structure

```json
{
  "event_id": "event_901",
  "type": "conversation.item.retrieve",
  "item_id": "item_003"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.retrieve`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| item_id | string | The ID of the item to retrieve. |

### conversation.item.truncate

Send the client `conversation.item.truncate` event to truncate a previous assistant message’s audio. The server produces audio faster than realtime, so this event is useful when the user interrupts to truncate audio that has already been sent to the client but not yet played. This synchronizes the server's understanding of the audio with the client's playback.

Truncating audio deletes the server-side text transcript to ensure there isn't text in the context that hasn't been heard by the user.

If successful, the server responds with a `conversation.item.truncated` event.

#### Event structure

```json
{
  "event_id": "event_678",
  "type": "conversation.item.truncate",
  "item_id": "item_002",
  "content_index": 0,
  "audio_end_ms": 1500
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.truncate`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| item_id | string | The ID of the assistant message item to truncate. Only assistant message items can be truncated. |
| content_index | integer | The index of the content part to truncate. Set this to `0`. |
| audio_end_ms | integer | Inclusive duration up to which audio is truncated, in milliseconds. If `audio_end_ms` is greater than the actual audio duration, the server responds with an error. |

### conversation.item.delete

Send the client `conversation.item.delete` event to remove an item from the conversation history.

The server responds with a `conversation.item.deleted` event unless the item doesn't exist in the conversation history. If the item doesn't exist, the server responds with an `error`.

#### Event structure

```json
{
  "event_id": "event_901",
  "type": "conversation.item.delete",
  "item_id": "item_003"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.delete`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| item_id | string | The ID of the item to delete. |

### response.create

Send the client `response.create` event to instruct the server to create a response, which triggers model inference. When you're in Server VAD mode, the server creates responses automatically.

A response includes at least one item and might include two items. If it includes two, the second item is a function call. By default, these items are appended to the conversation history.

The server responds with:
- A `response.created` event.
- Events for items and content created.
- A `response.done` event to indicate the response is complete.

The `response.create` event includes inference configuration such as `instructions` and `tools`. If you set these fields, they override the session configuration for this response only.

You can create responses out-of-band of the default conversation. That means your response can have arbitrary input, and you can disable writing the output to the conversation. Only one response can write to the default conversation at a time, but you can create multiple responses in parallel. The `metadata` field is a useful way to disambiguate multiple simultaneous responses.

To create a response that doesn't write to the default conversation, set `conversation` to `none`. You can provide arbitrary input with the `input` field, which is an array that accepts raw items and references to existing items.

#### Event structure

Trigger a response with the default conversation and no special parameters:

```json
{
  "type": "response.create"
}
```

Trigger an out-of-band response that doesn't write to the default conversation:

```json
{
  "type": "response.create",
  "response": {
    "instructions": "Provide a concise answer.",
    "tools": [],
    "conversation": "none",
    "output_modalities": [
      "text"
    ],
    "metadata": {
      "response_purpose": "summarization"
    },
    "input": [
      {
        "type": "item_reference",
        "id": "item_12345"
      },
      {
        "type": "message",
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "Summarize the above message in one sentence."
          }
        ]
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.create`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| response | object | Create a new Realtime response with these parameters. |

### response.cancel

Send the client `response.cancel` event to cancel an in-progress response.

The server responds with a `response.done` event with a status of `response.status=cancelled`. If there is no response to cancel, the server responds with an error.

It's safe to call `response.cancel` even if no response is in progress. An error is returned, and the session remains unaffected.

#### Event structure

```json
{
  "type": "response.cancel",
  "response_id": "resp_12345"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.cancel`. |
| event_id | string | Optional client-generated ID used to identify this event. |
| response_id | string | A specific response ID to cancel. If you don't provide it, the server cancels an in-progress response in the default conversation. |

### output_audio_buffer.clear

Send the client `output_audio_buffer.clear` event to cut off the current audio response. This triggers the server to stop generating audio and emit an `output_audio_buffer.cleared` event.

This event is only applicable for WebRTC/SIP.

This event should be preceded by a `response.cancel` client event to stop generation of the current response. Learn more.

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `output_audio_buffer.clear`. |
| event_id | string | The unique ID of the client event used for error handling. |

## Server events

Realtime server events are JSON objects the server emits to report updates in real time. These events help you track input audio buffering and transcription, conversation history changes, response generation progress, and output audio streaming.

This reference covers the server events listed in the **Server events** section.

There are 38 server events that you can receive from the server:

| Event | Description |
|-------|-------------|
| [`conversation.item.input_audio_transcription.completed`](#conversationiteminput_audio_transcriptioncompleted) | Returned when transcription completes for user audio written to the input audio buffer. |
| [`conversation.item.input_audio_transcription.delta`](#conversationiteminput_audio_transcriptiondelta) | Returned when incremental transcription results update the text value of an input audio transcription content part. |
| [`conversation.item.input_audio_transcription.segment`](#conversationiteminput_audio_transcriptionsegment) | Returned when the server identifies an input audio transcription segment for an item. |
| [`conversation.item.input_audio_transcription.failed`](#conversationiteminput_audio_transcriptionfailed) | Returned when a transcription request for a user message fails. |
| [`conversation.item.truncated`](#conversationitemtruncated) | Returned when the client truncates an earlier assistant audio message item. |
| [`conversation.item.deleted`](#conversationitemdeleted) | Returned when the client deletes an item from the conversation history. |
| [`input_audio_buffer.committed`](#input_audio_buffercommitted) | Returned when the input audio buffer is committed (by the client or automatically in server VAD mode). |
| [`input_audio_buffer.dtmf_event_received`](#input_audio_bufferdtmf_event_received) | Returned when the server receives a DTMF keypad event. This event is only applicable for SIP. |
| [`input_audio_buffer.cleared`](#input_audio_buffercleared) | Returned when the client clears the input audio buffer. |
| [`input_audio_buffer.speech_started`](#input_audio_bufferspeech_started) | Returned when the server detects speech in the input audio buffer (server VAD mode). |
| [`input_audio_buffer.speech_stopped`](#input_audio_bufferspeech_stopped) | Returned when the server detects the end of speech in the input audio buffer (server VAD mode). |
| [`input_audio_buffer.timeout_triggered`](#input_audio_buffertimeout_triggered) | Returned when the server VAD idle timeout triggers for the input audio buffer. |
| [`output_audio_buffer.started`](#output_audio_bufferstarted) | Emitted when the server begins streaming audio to the client. This event is only applicable for WebRTC/SIP. |
| [`output_audio_buffer.stopped`](#output_audio_bufferstopped) | Emitted when the output audio buffer drains on the server and no more audio is forthcoming. This event is only applicable for WebRTC/SIP. |
| [`output_audio_buffer.cleared`](#output_audio_buffercleared) | Emitted when the output audio buffer clears. This event is only applicable for WebRTC/SIP. |
| [`response.created`](#responsecreated) | Returned when a new response is created and enters the `in_progress` state. |
| [`response.done`](#responsedone) | Returned when a response finishes streaming, regardless of final state. |
| [`response.output_item.added`](#responseoutput_itemadded) | Returned when the server creates a new output item during response generation. |
| [`response.output_item.done`](#responseoutput_itemdone) | Returned when an output item finishes streaming. |
| [`response.content_part.added`](#responsecontent_partadded) | Returned when a new content part is added to an assistant message item during response generation. |
| [`response.content_part.done`](#responsecontent_partdone) | Returned when a content part finishes streaming. |
| [`response.output_text.delta`](#responseoutput_textdelta) | Returned when the text value of an `output_text` content part updates. |
| [`response.output_text.done`](#responseoutput_textdone) | Returned when the text value of an `output_text` content part finishes streaming. |
| [`response.output_audio_transcript.delta`](#responseoutput_audio_transcriptdelta) | Returned when the model-generated transcription of audio output updates. |
| [`response.output_audio_transcript.done`](#responseoutput_audio_transcriptdone) | Returned when the model-generated transcription of audio output finishes streaming. |
| [`response.output_audio.delta`](#responseoutput_audiodelta) | Returned when the model-generated audio updates. |
| [`response.output_audio.done`](#responseoutput_audiodone) | Returned when the model-generated audio finishes streaming. |
| [`response.function_call_arguments.delta`](#responsefunction_call_argumentsdelta) | Returned when the model-generated function call arguments update. |
| [`response.function_call_arguments.done`](#responsefunction_call_argumentsdone) | Returned when the model-generated function call arguments finish streaming. |
| [`response.mcp_call_arguments.delta`](#responsemcp_call_argumentsdelta) | Returned when MCP tool call arguments update during response generation. |
| [`response.mcp_call_arguments.done`](#responsemcp_call_argumentsdone) | Returned when MCP tool call arguments finalize during response generation. |
| [`response.mcp_call.in_progress`](#responsemcp_callin_progress) | Returned when an MCP tool call starts and is in progress. |
| [`response.mcp_call.completed`](#responsemcp_callcompleted) | Returned when an MCP tool call completes successfully. |
| [`response.mcp_call.failed`](#responsemcp_callfailed) | Returned when an MCP tool call fails. |
| [`mcp_list_tools.in_progress`](#mcp_list_toolsin_progress) | Returned when listing MCP tools is in progress for an item. |
| [`mcp_list_tools.completed`](#mcp_list_toolscompleted) | Returned when listing MCP tools completes for an item. |
| [`mcp_list_tools.failed`](#mcp_list_toolsfailed) | Returned when listing MCP tools fails for an item. |
| [`rate_limits.updated`](#rate_limitsupdated) | Emitted at the beginning of a response to indicate updated rate limits and output-token reservation. |

### conversation.item.input_audio_transcription.completed

The server `conversation.item.input_audio_transcription.completed` event is the output of audio transcription for user audio written to the input audio buffer.

Transcription begins when the input audio buffer is committed by the client or server (when VAD is enabled). Transcription runs asynchronously with response creation, so this event might come before or after the response events.

Realtime models accept audio natively, so input transcription runs as a separate process on a separate ASR (Automatic Speech Recognition) model. The transcript might diverge from the model's interpretation, so treat it as a rough guide.

#### Event structure

```json
{
  "type": "conversation.item.input_audio_transcription.completed",
  "event_id": "event_CCXGRvtUVrax5SJAnNOWZ",
  "item_id": "item_CCXGQ4e1ht4cOraEYcuR2",
  "content_index": 0,
  "transcript": "Hey, can you hear me?",
  "usage": {
    "type": "tokens",
    "total_tokens": 22,
    "input_tokens": 13,
    "input_token_details": {
      "text_tokens": 0,
      "audio_tokens": 13
    },
    "output_tokens": 9
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.completed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the item containing the audio that is being transcribed. |
| content_index | integer | The index of the content part containing the audio. |
| transcript | string | The transcribed text. |
| logprobs | array | The log probabilities of the transcription. [TO VERIFY: `logprobs` schema.] |
| usage | object | Usage statistics for the transcription. Billing uses the ASR model's pricing rather than the realtime model's pricing. |

### conversation.item.input_audio_transcription.delta

The server `conversation.item.input_audio_transcription.delta` event is returned when the text value of an input audio transcription content part updates with incremental transcription results.

#### Event structure

```json
{
  "type": "conversation.item.input_audio_transcription.delta",
  "event_id": "event_CCXGRxsAimPAs8kS2Wc7Z",
  "item_id": "item_CCXGQ4e1ht4cOraEYcuR2",
  "content_index": 0,
  "delta": "Hey",
  "obfuscation": "aLxx0jTEciOGe"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.delta`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the item containing the audio that is being transcribed. |
| content_index | integer | The index of the content part in the item's `content` array. |
| delta | string | The text delta. |
| logprobs | array | The log probabilities of the transcription. Enable these by configuring the session with `"include": ["item.input_audio_transcription.logprobs"]`. Each entry corresponds to a log probability for token selection for this chunk. This can help identify when multiple valid options exist. [TO VERIFY: `logprobs` schema.] |

### conversation.item.input_audio_transcription.segment

The server `conversation.item.input_audio_transcription.segment` event is returned when the server identifies an input audio transcription segment for an item.

#### Event structure

```json
{
  "event_id": "event_6501",
  "type": "conversation.item.input_audio_transcription.segment",
  "item_id": "msg_011",
  "content_index": 0,
  "text": "hello",
  "id": "seg_0001",
  "speaker": "spk_1",
  "start": 0.0,
  "end": 0.4
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.segment`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the item containing the input audio content. |
| content_index | integer | The index of the input audio content part within the item. |
| id | string | The segment identifier. |
| speaker | string | The detected speaker label for this segment. |
| start | number | Start time of the segment in seconds. |
| end | number | End time of the segment in seconds. |
| text | string | The text for this segment. |

### conversation.item.input_audio_transcription.failed

The server `conversation.item.input_audio_transcription.failed` event is returned when input audio transcription is configured and a transcription request for a user message fails.

These events are separate from other error events so you can identify the related item.

#### Event structure

```json
{
  "event_id": "event_2324",
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "msg_003",
  "content_index": 0,
  "error": {
    "type": "transcription_error",
    "code": "audio_unintelligible",
    "message": "The audio could not be transcribed.",
    "param": null
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.input_audio_transcription.failed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the user message item. |
| content_index | integer | The index of the content part containing the audio. |
| error | object | Details of the transcription error. |

### conversation.item.truncated

The server `conversation.item.truncated` event is returned when the client truncates an earlier assistant audio message item by sending `conversation.item.truncate`.

This event synchronizes the server's understanding of the audio with the client's playback. Truncation removes the server-side text transcript to ensure there is no text in context that the user hasn't heard.

#### Event structure

```json
{
  "event_id": "event_2526",
  "type": "conversation.item.truncated",
  "item_id": "msg_004",
  "content_index": 0,
  "audio_end_ms": 1500
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.truncated`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the assistant message item that was truncated. |
| content_index | integer | The index of the content part that was truncated. |
| audio_end_ms | integer | The duration up to which the audio was truncated, in milliseconds. |

### conversation.item.deleted

The server `conversation.item.deleted` event is returned when the client deletes an item from the conversation history by sending `conversation.item.delete`.

This event synchronizes the server's understanding of conversation history with the client's view.

#### Event structure

```json
{
  "event_id": "event_2728",
  "type": "conversation.item.deleted",
  "item_id": "msg_005"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `conversation.item.deleted`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the item that was deleted. |

### input_audio_buffer.committed

The server `input_audio_buffer.committed` event is returned when the input audio buffer is committed, either by the client or automatically in server VAD mode.

The `item_id` value is the ID of the user message item that is created, so the server also sends a `conversation.item.created` event to the client.

#### Event structure

```json
{
  "event_id": "event_1121",
  "type": "input_audio_buffer.committed",
  "previous_item_id": "msg_001",
  "item_id": "msg_002"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.committed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the user message item that is created. |
| previous_item_id | string | The ID of the preceding item after which the new item is inserted. This can be `null` if the item has no predecessor. |

### input_audio_buffer.dtmf_event_received

The server `input_audio_buffer.dtmf_event_received` event is returned when the server receives a DTMF event. A DTMF event represents a telephone keypad press (`0–9`, `*`, `#`, `A–D`).

The `event` property is the keypad the user presses. The `received_at` value is the UTC Unix timestamp when the server receives the event.

> [!NOTE]
> This event is only applicable for SIP.

#### Event structure

```json
{
  "type": "input_audio_buffer.dtmf_event_received",
  "event": "9",
  "received_at": 1763605109
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.dtmf_event_received`. |
| event | string | The telephone keypad key pressed by the user. |
| received_at | integer | UTC Unix timestamp when the server receives the DTMF event. |

### input_audio_buffer.cleared

The server `input_audio_buffer.cleared` event is returned when the client clears the input audio buffer by sending `input_audio_buffer.clear`.

#### Event structure

```json
{
  "event_id": "event_1314",
  "type": "input_audio_buffer.cleared"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.cleared`. |
| event_id | string | The unique ID of the server event. |

### input_audio_buffer.speech_started

The server `input_audio_buffer.speech_started` event is sent in `server_vad` mode to indicate the server detects speech in the input audio buffer. This can happen any time audio is added to the buffer (unless speech is already detected).

Use this event to interrupt audio playback or provide visual feedback to the user.

The server also sends `input_audio_buffer.speech_stopped` when speech stops. The `item_id` is the ID of the user message item created when speech stops and is also included in `input_audio_buffer.speech_stopped` (unless you manually commit the audio buffer during VAD activation).

#### Event structure

```json
{
  "event_id": "event_1516",
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 1000,
  "item_id": "msg_003"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.speech_started`. |
| event_id | string | The unique ID of the server event. |
| audio_start_ms | integer | Milliseconds from the start of all audio written to the buffer during the session when speech is first detected. This corresponds to the beginning of audio sent to the model and includes `prefix_padding_ms` configured in the session. |
| item_id | string | The ID of the user message item created when speech stops. |

### input_audio_buffer.speech_stopped

The server `input_audio_buffer.speech_stopped` event is returned in `server_vad` mode when the server detects the end of speech in the input audio buffer.

The server also sends `conversation.item.created` with the user message item created from the audio buffer.

#### Event structure

```json
{
  "event_id": "event_1718",
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 2000,
  "item_id": "msg_003"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.speech_stopped`. |
| event_id | string | The unique ID of the server event. |
| audio_end_ms | integer | Milliseconds since the session started when speech stops. This corresponds to the end of audio sent to the model and includes `min_silence_duration_ms` configured in the session. |
| item_id | string | The ID of the user message item that is created. |

### input_audio_buffer.timeout_triggered

The server `input_audio_buffer.timeout_triggered` event is returned when the server VAD timeout triggers for the input audio buffer. Configure this with `idle_timeout_ms` in the `turn_detection` settings of the session.

This event indicates there hasn't been any speech detected for the configured duration.

The `audio_start_ms` and `audio_end_ms` fields indicate the segment of audio after the last model response up to the triggering time, as an offset from the beginning of audio written to the input audio buffer. This demarcates silent audio, and the difference between `start` and `end` roughly matches the configured timeout.

The server commits the empty audio to the conversation as an `input_audio` item (so you receive `input_audio_buffer.committed`) and generates a model response. There might be speech that doesn't trigger VAD but is still detected by the model, so the model might respond with something relevant or a prompt to continue speaking.

#### Event structure

```json
{
  "type": "input_audio_buffer.timeout_triggered",
  "event_id": "event_CEKKrf1KTGvemCPyiJTJ2",
  "audio_start_ms": 13216,
  "audio_end_ms": 19232,
  "item_id": "item_CEKKrWH0GiwN0ET97NUZc"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `input_audio_buffer.timeout_triggered`. |
| event_id | string | The unique ID of the server event. |
| audio_start_ms | integer | Millisecond offset of audio written to the input audio buffer that was after the playback time of the last model response. |
| audio_end_ms | integer | Millisecond offset of audio written to the input audio buffer at the time the timeout triggers. |
| item_id | string | The ID of the item associated with this segment. |

### output_audio_buffer.started

The server `output_audio_buffer.started` event is emitted when the server begins streaming audio to the client. The server emits this event after an audio content part is added (`response.content_part.added`) to the response.

> [!NOTE]
> This event is only applicable for WebRTC/SIP.

#### Event structure

```json
{
  "event_id": "event_abc123",
  "type": "output_audio_buffer.started",
  "response_id": "resp_abc123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `output_audio_buffer.started`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The unique ID of the response that produces the audio. |

### output_audio_buffer.stopped

The server `output_audio_buffer.stopped` event is emitted when the output audio buffer drains on the server and no more audio is forthcoming. The server emits this event after the full response data is sent (`response.done`).

> [!NOTE]
> This event is only applicable for WebRTC/SIP.

#### Event structure

```json
{
  "event_id": "event_abc123",
  "type": "output_audio_buffer.stopped",
  "response_id": "resp_abc123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `output_audio_buffer.stopped`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The unique ID of the response that produces the audio. |

### output_audio_buffer.cleared

The server `output_audio_buffer.cleared` event is emitted when the output audio buffer clears. This happens either in VAD mode when the user interrupts (`input_audio_buffer.speech_started`), or when the client sends `output_audio_buffer.clear` to manually cut off the current audio response.

> [!NOTE]
> This event is only applicable for WebRTC/SIP.

#### Event structure

```json
{
  "event_id": "event_abc123",
  "type": "output_audio_buffer.cleared",
  "response_id": "resp_abc123"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `output_audio_buffer.cleared`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The unique ID of the response that produces the audio. |

### response.created

The server `response.created` event is returned when a new response is created. This is the first event of response creation, where the response is in an initial state of `in_progress`.

#### Event structure

```json
{
  "type": "response.created",
  "event_id": "event_C9G8pqbTEddBSIxbBN6Os",
  "response": {
    "object": "realtime.response",
    "id": "resp_C9G8p7IH2WxLbkgPNouYL",
    "status": "in_progress",
    "status_details": null,
    "output": [],
    "conversation_id": "conv_C9G8mmBkLhQJwCon3hoJN",
    "output_modalities": [
      "audio"
    ],
    "max_output_tokens": "inf",
    "audio": {
      "output": {
        "format": {
          "type": "audio/pcm",
          "rate": 24000
        },
        "voice": "marin"
      }
    },
    "usage": null,
    "metadata": null
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.created`. |
| event_id | string | The unique ID of the server event. |
| response | object | The response resource. |

### response.done

The server `response.done` event is returned when a response is done streaming. The server emits this event regardless of final state.

The response object included in `response.done` includes all output items in the response but omits the raw audio data.

Check `response.status` to determine whether the response completes successfully (`completed`) or has another outcome: `cancelled`, `failed`, or `incomplete`.

A response contains all output items generated during the response, excluding any audio content.

#### Event structure

```json
{
  "type": "response.done",
  "event_id": "event_CCXHxcMy86rrKhBLDdqCh",
  "response": {
    "object": "realtime.response",
    "id": "resp_CCXHw0UJld10EzIUXQCNh",
    "status": "completed",
    "status_details": null,
    "output": [
      {
        "id": "item_CCXHwGjjDUfOXbiySlK7i",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
          {
            "type": "output_audio",
            "transcript": "Loud and clear! I can hear you perfectly. How can I help you today?"
          }
        ]
      }
    ],
    "conversation_id": "conv_CCXHsurMKcaVxIZvaCI5m",
    "output_modalities": [
      "audio"
    ],
    "max_output_tokens": "inf",
    "audio": {
      "output": {
        "format": {
          "type": "audio/pcm",
          "rate": 24000
        },
        "voice": "alloy"
      }
    },
    "usage": {
      "total_tokens": 253,
      "input_tokens": 132,
      "output_tokens": 121,
      "input_token_details": {
        "text_tokens": 119,
        "audio_tokens": 13,
        "image_tokens": 0,
        "cached_tokens": 64,
        "cached_tokens_details": {
          "text_tokens": 64,
          "audio_tokens": 0,
          "image_tokens": 0
        }
      },
      "output_token_details": {
        "text_tokens": 30,
        "audio_tokens": 91
      }
    },
    "metadata": null
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.done`. |
| event_id | string | The unique ID of the server event. |
| response | object | The response resource. |

### response.output_item.added

The server `response.output_item.added` event is returned when the server creates a new output item during response generation.

#### Event structure

```json
{
  "event_id": "event_3334",
  "type": "response.output_item.added",
  "response_id": "resp_001",
  "output_index": 0,
  "item": {
    "id": "msg_007",
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
| type | string | The event type must be `response.output_item.added`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response to which the item belongs. |
| output_index | integer | The index of the output item in the response. |
| item | object | A single item within a realtime conversation. |

### response.output_item.done

The server `response.output_item.done` event is returned when an output item is done streaming. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_3536",
  "type": "response.output_item.done",
  "response_id": "resp_001",
  "output_index": 0,
  "item": {
    "id": "msg_007",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "Sure, I can help with that."
      }
    ]
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_item.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response to which the item belongs. |
| output_index | integer | The index of the output item in the response. |
| item | object | A single item within a realtime conversation. |

### response.content_part.added

The server `response.content_part.added` event is returned when a new content part is added to an assistant message item during response generation.

#### Event structure

```json
{
  "event_id": "event_3738",
  "type": "response.content_part.added",
  "response_id": "resp_001",
  "item_id": "msg_007",
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
| type | string | The event type must be `response.content_part.added`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item to which the content part is added. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| part | object | The content part that is added. |

### response.content_part.done

The server `response.content_part.done` event is returned when a content part is done streaming in an assistant message item. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_3940",
  "type": "response.content_part.done",
  "response_id": "resp_001",
  "item_id": "msg_007",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "text",
    "text": "Sure, I can help with that."
  }
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.content_part.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| part | object | The content part that is done. |

### response.output_text.delta

The server `response.output_text.delta` event is returned when the text value of an `output_text` content part updates.

#### Event structure

```json
{
  "event_id": "event_4142",
  "type": "response.output_text.delta",
  "response_id": "resp_001",
  "item_id": "msg_007",
  "output_index": 0,
  "content_index": 0,
  "delta": "Sure, I can h"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_text.delta`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| delta | string | The text delta. |

### response.output_text.done

The server `response.output_text.done` event is returned when the text value of an `output_text` content part is done streaming. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_4344",
  "type": "response.output_text.done",
  "response_id": "resp_001",
  "item_id": "msg_007",
  "output_index": 0,
  "content_index": 0,
  "text": "Sure, I can help with that."
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_text.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| text | string | The final text content. |

### response.output_audio_transcript.delta

The server `response.output_audio_transcript.delta` event is returned when the model-generated transcription of audio output updates.

#### Event structure

```json
{
  "event_id": "event_4546",
  "type": "response.output_audio_transcript.delta",
  "response_id": "resp_001",
  "item_id": "msg_008",
  "output_index": 0,
  "content_index": 0,
  "delta": "Hello, how can I a"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_audio_transcript.delta`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| delta | string | The transcript delta. |

### response.output_audio_transcript.done

The server `response.output_audio_transcript.done` event is returned when the model-generated transcription of audio output is done streaming. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_4748",
  "type": "response.output_audio_transcript.done",
  "response_id": "resp_001",
  "item_id": "msg_008",
  "output_index": 0,
  "content_index": 0,
  "transcript": "Hello, how can I assist you today?"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_audio_transcript.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| transcript | string | The final transcript of the audio. |

### response.output_audio.delta

The server `response.output_audio.delta` event is returned when the model-generated audio updates.

#### Event structure

```json
{
  "event_id": "event_4950",
  "type": "response.output_audio.delta",
  "response_id": "resp_001",
  "item_id": "msg_008",
  "output_index": 0,
  "content_index": 0,
  "delta": "Base64EncodedAudioDelta"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_audio.delta`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |
| delta | string | Base64-encoded audio data delta. |

### response.output_audio.done

The server `response.output_audio.done` event is returned when the model-generated audio is done. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_5152",
  "type": "response.output_audio.done",
  "response_id": "resp_001",
  "item_id": "msg_008",
  "output_index": 0,
  "content_index": 0
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.output_audio.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the item. |
| output_index | integer | The index of the output item in the response. |
| content_index | integer | The index of the content part in the item's `content` array. |

### response.function_call_arguments.delta

The server `response.function_call_arguments.delta` event is returned when the model-generated function call arguments update.

#### Event structure

```json
{
  "event_id": "event_5354",
  "type": "response.function_call_arguments.delta",
  "response_id": "resp_002",
  "item_id": "fc_001",
  "output_index": 0,
  "call_id": "call_001",
  "delta": "{\"location\": \"San\""
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.function_call_arguments.delta`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the function call item. |
| output_index | integer | The index of the output item in the response. |
| call_id | string | The ID of the function call. |
| delta | string | The arguments delta as a JSON string. |

### response.function_call_arguments.done

The server `response.function_call_arguments.done` event is returned when the model-generated function call arguments are done streaming. The server also emits this event when a response is interrupted, incomplete, or cancelled.

#### Event structure

```json
{
  "event_id": "event_5556",
  "type": "response.function_call_arguments.done",
  "response_id": "resp_002",
  "item_id": "fc_001",
  "output_index": 0,
  "call_id": "call_001",
  "arguments": "{\"location\": \"San Francisco\"}"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.function_call_arguments.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the function call item. |
| output_index | integer | The index of the output item in the response. |
| call_id | string | The ID of the function call. |
| arguments | string | The final arguments as a JSON string. |

### response.mcp_call_arguments.delta

The server `response.mcp_call_arguments.delta` event is returned when MCP tool call arguments update during response generation.

#### Event structure

```json
{
  "event_id": "event_6201",
  "type": "response.mcp_call_arguments.delta",
  "response_id": "resp_001",
  "item_id": "mcp_call_001",
  "output_index": 0,
  "delta": "{\"partial\":true}"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call_arguments.delta`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the MCP tool call item. |
| output_index | integer | The index of the output item in the response. |
| delta | string | The JSON-encoded arguments delta. |
| obfuscation | string | If present, indicates the delta text is obfuscated. |

### response.mcp_call_arguments.done

The server `response.mcp_call_arguments.done` event is returned when MCP tool call arguments finalize during response generation.

#### Event structure

```json
{
  "event_id": "event_6202",
  "type": "response.mcp_call_arguments.done",
  "response_id": "resp_001",
  "item_id": "mcp_call_001",
  "output_index": 0,
  "arguments": "{\"q\":\"docs\"}"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call_arguments.done`. |
| event_id | string | The unique ID of the server event. |
| response_id | string | The ID of the response. |
| item_id | string | The ID of the MCP tool call item. |
| output_index | integer | The index of the output item in the response. |
| arguments | string | The final JSON-encoded arguments string. |

### response.mcp_call.in_progress

The server `response.mcp_call.in_progress` event is returned when an MCP tool call starts and is in progress.

#### Event structure

```json
{
  "event_id": "event_6301",
  "type": "response.mcp_call.in_progress",
  "output_index": 0,
  "item_id": "mcp_call_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.in_progress`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP tool call item. |
| output_index | integer | The index of the output item in the response. |

### response.mcp_call.completed

The server `response.mcp_call.completed` event is returned when an MCP tool call completes successfully.

#### Event structure

```json
{
  "event_id": "event_6302",
  "type": "response.mcp_call.completed",
  "output_index": 0,
  "item_id": "mcp_call_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.completed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP tool call item. |
| output_index | integer | The index of the output item in the response. |

### response.mcp_call.failed

The server `response.mcp_call.failed` event is returned when an MCP tool call fails.

#### Event structure

```json
{
  "event_id": "event_6303",
  "type": "response.mcp_call.failed",
  "output_index": 0,
  "item_id": "mcp_call_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `response.mcp_call.failed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP tool call item. |
| output_index | integer | The index of the output item in the response. |

### mcp_list_tools.in_progress

The server `mcp_list_tools.in_progress` event is returned when listing MCP tools is in progress for an item.

#### Event structure

```json
{
  "event_id": "event_6101",
  "type": "mcp_list_tools.in_progress",
  "item_id": "mcp_list_tools_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.in_progress`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP list tools item. |

### mcp_list_tools.completed

The server `mcp_list_tools.completed` event is returned when listing MCP tools completes for an item.

#### Event structure

```json
{
  "event_id": "event_6102",
  "type": "mcp_list_tools.completed",
  "item_id": "mcp_list_tools_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.completed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP list tools item. |

### mcp_list_tools.failed

The server `mcp_list_tools.failed` event is returned when listing MCP tools fails for an item.

#### Event structure

```json
{
  "event_id": "event_6103",
  "type": "mcp_list_tools.failed",
  "item_id": "mcp_list_tools_001"
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `mcp_list_tools.failed`. |
| event_id | string | The unique ID of the server event. |
| item_id | string | The ID of the MCP list tools item. |

### rate_limits.updated

The server `rate_limits.updated` event is emitted at the beginning of a response to indicate updated rate limits.

When a response is created, the server reserves some tokens for output tokens. The rate limits shown here reflect that reservation, which is adjusted once the response completes.

#### Event structure

```json
{
  "event_id": "event_5758",
  "type": "rate_limits.updated",
  "rate_limits": [
    {
      "name": "requests",
      "limit": 1000,
      "remaining": 999,
      "reset_seconds": 60
    },
    {
      "name": "tokens",
      "limit": 50000,
      "remaining": 49950,
      "reset_seconds": 60
    }
  ]
}
```

#### Properties

| Field | Type | Description |
|-------|------|-------------|
| type | string | The event type must be `rate_limits.updated`. |
| event_id | string | The unique ID of the server event. |
| rate_limits | array | List of rate limit information. |

## Components

Use this section to document objects referenced by the events.

### Session object

A session object specifies the configuration for a Realtime session or a transcription session.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The session type (for example, `realtime`). Choose either a realtime session or a transcription session. |
| instructions | string | Instructions used to guide behavior. You can clear this by sending an empty string in `session.update`. |
| tools | array | Tools available to the model. You can clear this by sending an empty array in `session.update`. |
| tool_choice | string | Tool selection behavior (for example, `auto`). |

### Function tool object

A function tool provides a callable function definition.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The tool type (for example, `function`). |
| name | string | The function name. |
| description | string | A description of when to call the function. |
| parameters | object | JSON Schema-like object describing parameters (as shown in the example). |

### Conversation item object

A conversation item represents a single item within a Realtime conversation.

| Field | Type | Description |
|-------|------|-------------|
| type | string | The item type (for example, `message`). |
| role | string | The role for the item (for example, `user`). |
| content | array | Content parts for the item (for example, `input_text`). |

### Response object

A response object specifies per-response parameters for model inference and output handling.

| Field | Type | Description |
|-------|------|-------------|
| instructions | string | Instructions that override session instructions for this response only. |
| tools | array | Tools that override session tools for this response only. |
| conversation | string | Conversation handling (for example, `none` to avoid writing to the default conversation). |
| output_modalities | array | Output modalities (for example, `["text"]`). |
| metadata | object | Metadata you can use to disambiguate multiple simultaneous responses. |
| input | array | Input items, including raw items and references to existing items. |

### Transcription error object

Details of an input audio transcription failure.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Error type (for example, `transcription_error`). |
| code | string | Error code (for example, `audio_unintelligible`). |
| message | string | Human-readable error message. |
| param | object | Parameter associated with the error. This can be `null`. |

### Transcription usage (tokens) object

Usage statistics emitted with transcription completion. Billing uses the ASR model's pricing rather than the realtime model's pricing.

| Field | Type | Description |
|-------|------|-------------|
| type | string | Usage type (for example, `tokens`). |
| total_tokens | integer | Total token count. |
| input_tokens | integer | Input token count. |
| input_token_details | object | Token details for input. |
| output_tokens | integer | Output token count. |

#### input_token_details properties

| Field | Type | Description |
|-------|------|-------------|
| text_tokens | integer | Text token count. |
| audio_tokens | integer | Audio token count. |

### Rate limit object

A single rate limit entry emitted in `rate_limits.updated`.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Rate limit name (for example, `requests` or `tokens`). |
| limit | integer | Limit per window. |
| remaining | integer | Remaining capacity in the current window. |
| reset_seconds | integer | Seconds until reset. |

## Notes and constraints

Client:
- Input audio transcription starts when the input audio buffer is committed by the client or server (when VAD is enabled).
- Input audio transcription runs asynchronously with response creation, so transcription events might arrive before or after response events.
- Input transcription runs on a separate ASR model, and the transcript might diverge from the realtime model’s interpretation.
- Enable transcription `logprobs` by configuring the session with `"include": ["item.input_audio_transcription.logprobs"]`. [TO VERIFY: Full include configuration context.]
- `input_audio_buffer.speech_started`, `input_audio_buffer.speech_stopped`, and `input_audio_buffer.timeout_triggered` apply to server VAD mode (`server_vad`).
- `output_audio_buffer.started`, `output_audio_buffer.stopped`, and `output_audio_buffer.cleared` are only applicable for WebRTC/SIP.
- The response object in `response.done` omits raw audio data.

Server:
- For `session.update`, you can update any field except `voice` and `model`. You can update `voice` only if there have been no other audio outputs yet.
- For `session.update`, clear fields by sending an empty string (`instructions`), an empty array (`tools`), or `null` (`turn_detection`).
- For `input_audio_buffer.append`, you can send up to 15 MiB of audio per event.
- For `input_audio_buffer.append`, the server doesn't send a confirmation response.
- For `output_audio_buffer.clear`, the event is only applicable for WebRTC/SIP, and you should send `response.cancel` first to stop generating the current response.

## Related content

* Get started with the [Realtime API quickstart](./how-to/realtime-audio.md#quickstart).
* Learn more about [How to use the Realtime API](./how-to/realtime-audio.md).