---
title: "Migration from Preview to GA version of Realtime API (classic)"
description: "Step-by-step guide for migrating from Preview (Beta) to Generally Available version of OpenAI GPT Realtime API protocol. (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/23/2026
author: alexeyo26
ms.author: alexeyo
recommendations: false
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Migration from Preview to GA version of Realtime API (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/realtime-audio-preview-api-migration-guide.md)

[!INCLUDE [realtime-audio-preview-api-migration-guide 1](../../../foundry/openai/includes/how-to-realtime-audio-preview-api-migration-guide-1.md)]

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

See detailed information on the endpoint format in [this article](realtime-audio-websockets.md#connection-and-authentication). See example of GA endpoint format usage in [Quick start on GPT Realtime API for speech and audio](../how-to/realtime-audio.md#quickstart).

[!INCLUDE [realtime-audio-preview-api-migration-guide 2](../../../foundry/openai/includes/how-to-realtime-audio-preview-api-migration-guide-2.md)]

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

**Solution**: Update your event handler names according to the new event names. Ensure all occurrences are updated, including error handlers.

### Session configuration rejected

**Symptom**: Server returns an error when sending the `session.update` event.

**Cause**: The required `type` field is missing from the session configuration.

**Solution**: Add the `type` field to your session configuration with the value `"realtime"` for speech-to-speech or `"transcription"` for audio transcription.

### WebRTC connection fails to establish

**Symptom**: Browser-based WebRTC connection doesn't establish after migration.

**Cause**: WebRTC endpoints changed in the GA version.

**Solution**: Update both the ephemeral key endpoint and the connection URL.

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

[!INCLUDE [realtime-audio-preview-api-migration-guide 3](../../../foundry/openai/includes/how-to-realtime-audio-preview-api-migration-guide-3.md)]
