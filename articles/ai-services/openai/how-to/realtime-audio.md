---
title: 'How to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to use the GPT-4o Realtime API for speech and audio with Azure OpenAI Service.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 12/6/2024
author: eric-urban
ms.author: eur
ms.custom: references_regions
recommendations: false
---

# How to use the GPT-4o Realtime API for speech and audio (Preview)

Azure OpenAI GPT-4o Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o Realtime API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

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
- You need a deployment of the `gpt-4o-realtime-preview` model in a supported region as described in the [supported models](#supported-models) section. You can deploy the model from the [Azure AI Studio model catalog](../../ai-studio/how-to/model-catalog-overview.md) or from your project in AI Studio. 

For steps to deploy and use the `gpt-4o-realtime-preview` model, see [the real-time audio quickstart](../realtime-audio-quickstart.md).

For more information about the API and architecture, see the remaining sections in this guide.


## Architecture

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. Device details like capturing and rendering audio data are outside the scope of the Realtime API. It should be used in the context of a trusted, intermediate service that manages both connections to end users and model endpoint connections. Don't use it directly from untrusted end user devices.

### Connection and authentication with the Realtime API

The Realtime API requires an existing Azure OpenAI resource endpoint in a supported region. The API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

A full request URI can be constructed by concatenating:

- The secure WebSocket (`wss://`) protocol
- Your Azure OpenAI resource endpoint hostname, e.g. `my-aoai-resource.openai.azure.com`
- The `openai/realtime` API path
- An `api-version` query string parameter for a supported API version -- initially, `2024-10-01-preview`
- A `deployment` query string parameter with the name of your `gpt-4o-realtime-preview` model deployment

Combining into a full example, the following could be a well-constructed `/realtime` request URI:

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/realtime?api-version=2024-10-01-preview&deployment=gpt-4o-realtime-preview-1001
```

To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI Service resource that has managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  1. Using an `api-key` connection header on the pre-handshake connection. This option isn't available in a browser environment.
  2. Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using https/wss.


### API concepts

- A caller establishes a connection to `/realtime`, which starts a new `session`.
- A `session` automatically creates a default `conversation`. Multiple concurrent conversations aren't supported.
- The `conversation` accumulates input signals until a `response` is started, either via a direct command by the caller or automatically by voice-activity-based (VAD) turn detection.
- Each `response` consists of one or more `items`, which can encapsulate messages, function calls, and other information.
- Each message `item` has `content_part`, allowing multiple modalities (text and audio) to be represented across a single item.
- The `session` manages configuration of caller input handling (for example, user audio) and common output generation handling.
- Each caller-initiated `response.create` can override some of the output `response` behavior, if desired.
- Server-created `item` and the `content_part` in messages can be populated asynchronously and in parallel. For example, receiving audio, text, and function information concurrently in a round robin fashion.

## API details

Once the WebSocket connection session to `/realtime` is established and authenticated, the functional interaction takes place via sending and receiving WebSocket messages, herein referred to as "commands" to avoid ambiguity with the content-bearing "message" concept already present for inference. These commands each take the form of a JSON object. Commands can be sent and received in parallel and applications should generally handle them both concurrently and asynchronously.

### Session configuration and turn handling mode

Often, the first command sent by the caller on a newly established `/realtime` session will be a `session.update` payload. This command controls a wide set of input and output behavior, with output and response generation portions then later overridable via `update_conversation_config` or other properties in `response.create`.

One of the key session-wide settings is `turn_detection`, which controls how data flow is handled between the caller and model:

- `server_vad` evaluates incoming user audio (as sent via `add_user_audio`) using a voice activity detector (VAD) component and automatically use that audio to initiate response generation on applicable conversations when an end of speech is detected. Silence detection for the VAD can be configured when specifying `server_vad` detection mode.
- `none` relies on caller-initiated `input_audio_buffer.commit` and `response.create` commands to progress conversations and produce output. This setting is useful for push-to-talk applications or situations that have external audio flow control (such as caller-side VAD component). These manual signals can still be used in `server_vad` mode to supplement VAD-initiated response generation.

Transcription of user input audio is opted into via the `input_audio_transcription` property. Specifying a transcription model (`whisper-1`) in this configuration enables the delivery of `conversation.item.audio_transcription.completed` events.

## Summary of commands

### Requests

The following table describes commands sent from the caller to the `/realtime` endpoint.

| `type` | Description |
|---|---|
| **Session Configuration** | |
| `session.update` | Configures the connection-wide behavior of the conversation session such as shared audio input handling and common response generation characteristics. This is typically sent immediately after connecting, but can also be sent at any point during a session to reconfigure behavior after the current response (if in progress) is complete. |
| **Input Audio** | |
| `input_audio_buffer_append` | Appends audio data to the shared user input buffer. This audio won't be processed until an end of speech is detected in the `server_vad` `turn_detection` mode or until a manual `response.create` is sent (in either `turn_detection` configuration). |
| `input_audio_buffer_clear` | Clears the current audio input buffer. This doesn't affect responses already in progress. |
| `input_audio_buffer_commit` | Commits the current state of the user input buffer to subscribed conversations, including it as information for the next response. |
| **Item Management** | For establishing history or including non-audio item information. |
| `item_create` | Inserts a new item into the conversation, optionally positioned according to `previous_item_id`. This property can provide new, non-audio input from the user (such as a text message), tool responses, or historical information from another interaction to form a conversation history before generation. |
| `item_delete` | Removes an item from an existing conversation. |
| `item_truncate` | Manually shortens text and audio content in a message. This property can be useful in situations where faster-than-realtime model generation produced more data that's later skipped by an interruption. |
| **Response Management** |
| `response.create` | Initiates model processing of unprocessed conversation input, signifying the end of the caller's logical turn. `server_vad` `turn_detection` mode automatically triggers generation at end of speech, but `response.create` must be called in other circumstances (such as text input, tool responses, and `none` mode) to signal that the conversation should continue. The `response.create` should be invoked after the `response.done` command from the model that confirms all tool calls and other messages are provided. |
| `response.cancel` | Cancels an in-progress response. |


### Responses

The following table describes commands sent by the `/realtime` endpoint to the caller.

| `type` | Description |
|---|---|
| **Session** | |
| `session_created` | Sent as soon as the connection is successfully established. Provides a connection-specific ID that might be useful for debugging or logging. |
| **Caller Item Acknowledgement** | |
| `item_created` | Provides acknowledgment that a new conversation item is inserted into a conversation. |
| `item_deleted` | Provides acknowledgment that an existing conversation item is removed from a conversation. |
| `item_truncated` | Provides acknowledgment that an existing item in a conversation is truncated. |
| **Response Flow** | |
| `response_created` | Notifies that a new response is started for a conversation. This snapshots input state and begins generation of new items. Until `response_done` signifies the end of the response, a response can create items via `response_output_item_added` that are then populated via `delta` commands. |
| `response_done` | Notifies that a response generation is complete for a conversation. |
| `response_cancelled` | Confirms that a response was canceled in response to a caller-initiated or internal signal. |
| `rate_limits_updated` | This response is sent immediately after `response.done`, this property provides the current rate limit information reflecting updated status after the consumption of the just-finished response. |
| **Item Flow in a Response** | |
| `response_output_item_added` | Notifies that a new, server-generated conversation item *is being created*; content will then be populated via incremental `add_content` messages with a final `response_output_item_done` command signifying the item creation has completed. |
| `response_output_item_done` | Notifies that a new conversation item is added to a conversation. For model-generated messages, this property is preceded by `response_output_item_added` and `delta` commands which begin and populate the new item, respectively. |
| **Content Flow within Response Items** | |
| `response_content_part_added` | Notifies that a new content part is being created within a conversation item in an ongoing response. Until `response_content_part_done` arrives, content is then incrementally provided via the appropriate `delta` commands. |
| `response_content_part_done` | Signals that a newly created content part is complete and receives no further incremental updates. |
| `response_audio_delta` | Provides an incremental update to a binary audio data content part generated by the model. |
| `response_audio_done` | Signals that an audio content part's incremental updates are complete. |
| `response_audio_transcript_delta` | Provides an incremental update to the audio transcription associated with the output audio content generated by the model. |
| `response_audio_transcript_done` | Signals that the incremental updates to audio transcription of output audio are complete. |
| `response_text_delta` | Provides an incremental update to a text content part within a conversation message item. |
| `response_text_done` | Signals that the incremental updates to a text content part are complete. |
| `response_function_call_arguments_delta` | Provides an incremental update to the arguments of a function call, as represented within an item in a conversation. |
| `response_function_call_arguments_done` | Signals that incremental function call arguments are complete and that accumulated arguments can now be used in their entirety. |
| **User Input Audio** | |
| `input_audio_buffer_speech_started` | When you use configured voice activity detection, this command notifies that a start of user speech is detected within the input audio buffer at a specific audio sample index. |
| `input_audio_buffer_speech_stopped` | When you use configured voice activity detection, this command notifies that an end of user speech is detected within the input audio buffer at a specific audio sample index. This setting automatically triggers response generation when configured. |
| `item_input_audio_transcription_completed` | Notifies that a supplementary transcription of the user's input audio buffer is available. This behavior must be opted into via the `input_audio_transcription` property in `session.update`. |
| `item_input_audio_transcription_failed` | Notifies that input audio transcription failed. |
| `input_audio_buffer_committed` | Provides acknowledgment that the current state of the user audio input buffer is submitted to subscribed conversations. |
| `input_audio_buffer_cleared` | Provides acknowledgment that the pending user audio input buffer is cleared. |
| **Other** | |
| `error` | Indicates that something went wrong while processing data on the session. Includes an `error` message that provides more detail. |

## Related content

* Learn more about Azure OpenAI [deployment types](deployment-types.md)
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md)
