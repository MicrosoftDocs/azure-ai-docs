---
title: 'Migration from Beta to GA version of Realtime API protocol'
titleSuffix: Azure OpenAI
description: Migration Guide from Beta to GA version of OpenAI GPT Realtime API protocol.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 09/16/2025
author: alexeyo26
ms.author: alexeyo
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Migration from Preview to GA version of Realtime API

You need to use Generally Available (GA) version of Azure OpenAI GPT Realtime API in your applications. The Beta version of the API used during the Preview phase of the Service is deprecated starting April 30, 2026.

## SDK Support

For Realtime GA API protocol, you need to use a supported SDK and the right API version.

> [!CAUTION]
> The Realtime GA API protocol and message format are only supported in the SDKs provided by OpenAI. Realtime Preview SDKs previously released by Microsoft don't support GA API protocol.

**List of SDKs**:

- TypeScript/JavaScript: https://github.com/openai/openai-node
- Python: https://github.com/openai/openai-python
- Java (only message format): https://github.com/openai/openai-java
- Go (only message format): https://github.com/openai/openai-go
- .NET: https://github.com/openai/openai-dotnet 

> [!IMPORTANT]
> Realtime GA API protocol isn't supported in OpenAI .NET v.2.8.0 or earlier. You need to use later versions for GA protocol.

**API version / Base URL**.

Use GA endpoint URL format in your applications. This URL should contain `/openai/v1` and shouldn't contain any API version like `2025-04-01-preview`.

Example of GA endpoint format:
```http
https://<your-resource>.openai.azure.com/openai/v1/
```

See detailed information on the endpoint format in [this article](realtime-audio-websockets.md#connection-and-authentication). See example of GA endpoint format usage in [Quick start on GPT Realtime API for speech and audio](../realtime-audio-quickstart.md).

## Ephemeral Keys and WebRTC URLs

Ephemeral keys for WebRTC requests are now created with a `POST /openai/v1/realtime/client_secrets` request on your Azure OpenAI endpoint (see details in [Step-by-step guide](realtime-audio-webrtc.md#step-1-set-up-service-to-procure-ephemeral-token)).

The URL for initializing the WebRTC connection in the browser is now `/openai/v1/realtime/calls` (see details in [Step-by-step guide](realtime-audio-webrtc.md#step-2-set-up-your-browser-application)).

## Custom Clients

If you implement the protocol in your own client, this section shows the detailed changes of the protocol.

### OpenAI-Beta header

Don't include the `OpenAI-Beta:` header in any of the requests.

### Modified events

Both realtime speech-to-speech and transcription sessions now use the same `session.update` event. This event has new `type` field with the following possible values:

- `realtime` for speech-to-speech
- `transcription` for realtime audio transcription

See the following code snippet example:

```python
ws.on("open", function open() {
    ws.send(
        JSON.stringify({
            type: "session.update",
            session: {
                type: "realtime",
                model: "gpt-realtime",
                <...>
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
