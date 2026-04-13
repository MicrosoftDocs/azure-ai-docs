---
title: Include file
description: Include file
author: alexeyo26
ms.reviewer: sgilley
ms.author: alexeyo
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Update WebRTC endpoints

If you're using WebRTC for browser-based realtime audio, you need to update two endpoints to the GA versions.

Ephemeral keys for WebRTC requests are now created with a `POST /openai/v1/realtime/client_secrets` request on your Azure OpenAI endpoint (see details in [Step-by-step guide](../how-to/realtime-audio-webrtc.md#step-1-set-up-service-to-procure-ephemeral-token)).

The URL for initializing the WebRTC connection in the browser is now `/openai/v1/realtime/calls` (see details in [Step-by-step guide](../how-to/realtime-audio-webrtc.md#step-2-set-up-your-browser-application)).

## Protocol changes for custom clients

If you implement the Realtime API protocol in your own client instead of using the official SDKs, review these detailed protocol changes.

### OpenAI-Beta header

Don't include the `OpenAI-Beta:` header in any of the requests.

### Modified events

Both realtime speech-to-speech and transcription sessions now use the same `session.update` event. This event has new `type` field with the following possible values:

- `realtime` for speech-to-speech
- `transcription` for realtime audio transcription

See the following code snippet example:

```javascript
ws.on("open", function open() {
    ws.send(
        JSON.stringify({
            type: "session.update",
            session: {
                type: "realtime",
                model: "gpt-realtime",
                // ... additional configuration
```
The `session.update` event changed format, and some properties are now in different locations. See the [API reference](https://platform.openai.com/docs/api-reference/realtime) for details.

The following event names changed:

- From `response.text.delta` to `response.output_text.delta`
- From `response.audio.delta` to `response.output_audio.delta`
- From `response.audio_transcript.delta` to `response.output_audio_transcript.delta`

All conversation item events now have `object=realtime.item` field.

A status field can be added to the function call output item. This field has no effect on the conversation.

The types of the message content for assistant responses changed like this:

- From `type=text` to `type=output_text`
- From `type=audio` to `type=output_audio`

### New events

The `conversation.item.added` and `conversation.item.done` events were added to better handle long-running operations such as MCP tool listing.
