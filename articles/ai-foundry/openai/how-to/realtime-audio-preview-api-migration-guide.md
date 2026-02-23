---
title: 'Migration from Preview to GA version of Realtime API'
titleSuffix: Azure OpenAI
description: Step-by-step guide for migrating from Preview (Beta) to Generally Available version of OpenAI GPT Realtime API protocol.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/23/2026
author: alexeyo26
ms.author: alexeyo
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Migration from Preview to GA version of Realtime API

The Azure OpenAI GPT Realtime API has transitioned from Preview to Generally Available (GA). This migration guide helps you update existing applications to use the GA protocol. The GA version introduces changes to SDK usage, endpoint URLs, event names, and session configuration.

**What's changing**: SDK packages, endpoint URL format, event names, and session configuration structure.

**What's not changing**: Core functionality, audio format support, and model capabilities.

**Time to migrate**: Most migrations take 30-60 minutes.

> [!IMPORTANT]
> The Preview version of the API is deprecated starting April 30, 2026. Migrate to the GA version before this date to avoid service disruption.

> [!NOTE]
> If you're building a new application, refer to the [Realtime API quickstart](../realtime-audio-quickstart.md) instead. This guide is only for migrating existing Preview applications to GA.

## Prerequisites

Before you begin the migration, verify you have:

- An existing Azure OpenAI resource with a Realtime API deployment that uses the Preview (Beta) protocol
- Access to the Azure portal with permissions to manage Azure OpenAI resources
- Ability to update SDK dependencies in your development environment
- A test environment where you can validate changes before deploying to production
- Understanding of your current implementation (WebSocket or WebRTC)

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

## Update WebRTC endpoints

If you're using WebRTC for browser-based realtime audio, you need to update two endpoints to the GA versions.

Ephemeral keys for WebRTC requests are now created with a `POST /openai/v1/realtime/client_secrets` request on your Azure OpenAI endpoint (see details in [Step-by-step guide](realtime-audio-webrtc.md#step-1-set-up-service-to-procure-ephemeral-token)).

The URL for initializing the WebRTC connection in the browser is now `/openai/v1/realtime/calls` (see details in [Step-by-step guide](realtime-audio-webrtc.md#step-2-set-up-your-browser-application)).

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

## Troubleshooting

This section covers common issues encountered during migration and their solutions.

### WebSocket connection returns 401 Unauthorized

**Symptom**: Connection fails with authentication error after updating to GA endpoint.

**Cause**: The `api-version` query parameter is no longer supported in GA endpoint URLs.

**Solution**: Remove `api-version` from your endpoint URL. Change from:
```
wss://<resource>.openai.azure.com/openai/realtime?api-version=2025-04-01-preview
```

to:
```
wss://<resource>.openai.azure.com/openai/v1/realtime
```

### Event handlers not triggering

**Symptom**: Audio or text responses aren't being processed after migration.

**Cause**: Event names changed between Preview and GA versions.

**Solution**: Update your event handler names according to the mapping in [Step 3: Update event names](#step-3-update-event-names). Ensure all occurrences are updated, including error handlers.

### Session configuration rejected

**Symptom**: Server returns an error when sending the `session.update` event.

**Cause**: The required `type` field is missing from the session configuration.

**Solution**: Add the `type` field to your session configuration with the value `"realtime"` for speech-to-speech or `"transcription"` for audio transcription. See [Step 4: Update session configuration](#step-4-update-session-configuration) for examples.

### WebRTC connection fails to establish

**Symptom**: Browser-based WebRTC connection doesn't establish after migration.

**Cause**: WebRTC endpoints changed in the GA version.

**Solution**: Update both the ephemeral key endpoint and the connection URL as described in [Update WebRTC endpoints](#update-webrtc-endpoints).

### .NET SDK compatibility error

**Symptom**: .NET application throws errors when attempting to use GA protocol.

**Cause**: GA protocol requires OpenAI .NET SDK version later than 2.8.0.

**Solution**: Update your .NET SDK package to version 2.1.0 or later using:
```bash
dotnet add package OpenAI --version 2.1.0
```

## Verification checklist

Use this checklist to verify your migration is complete:

> [!div class="checklist"]
> * SDK updated to GA-compatible version (Python ≥1.54.0, JavaScript ≥4.77.0, .NET >2.8.0)
> * Endpoint URLs changed to `/openai/v1/realtime` format
> * `api-version` query parameter removed from endpoint URLs
> * Event names updated (`response.text.delta` → `response.output_text.delta`, etc.)
> * `type` field added to `session.update` event configuration
> * `OpenAI-Beta` header removed from custom client implementations
> * WebRTC endpoints updated (if applicable)
> * Application tested successfully in a non-production environment
> * Audio input and output verified to work correctly
> * No deprecation warnings appear in application logs
> * Performance metrics meet or exceed baseline expectations

## Next steps

Now that you've migrated to the GA version of the Realtime API, explore these resources to enhance your implementation:

- [Realtime API reference](https://developers.openai.com/docs/api-reference/realtime) - Complete API documentation
- [WebSocket implementation guide](realtime-audio-websockets.md) - Detailed WebSocket configuration
- [WebRTC implementation guide](realtime-audio-webrtc.md) - Browser-based audio implementation
- [SIP integration](realtime-audio-sip.md) - Enable phone call integration
- [Monitor Azure OpenAI](../how-to/monitoring.md) - Track usage and performance
- [Realtime API quickstart](../realtime-audio-quickstart.md) - Additional implementation examples
- [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) - Cost and billing information
