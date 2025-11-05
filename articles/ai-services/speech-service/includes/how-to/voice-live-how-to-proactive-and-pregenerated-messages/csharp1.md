---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/05/2025
---

In this article, you learn how to use Azure AI Speech voice live with Azure AI Foundry models using the VoiceLive SDK for C#.

[!INCLUDE [Header](../../common/voice-live-csharp.md)]

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

1. Find the 'HandleSessionUpdateAsync' function in class 'BasicVoiceAssistant'.
1. Find the `sessionUpdated` event.
1. Replace the existing code handling the `SESSSION_UPDATED` event:

```csharp
case SessionUpdateSessionUpdated sessionUpdated:
    _logger.LogInformation("Session updated successfully");

    // Start audio capture once session is ready
    if (_audioProcessor != null)
    {
        // Proactive greeting
        if (!_conversationStarted)
        {
            _conversationStarted = true;
            _logger.LogInformation("Sending proactive greeting request");
            try
            {
                await _session!.StartResponseAsync().ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to send proactive greeting request");
            }
        }
        await _audioProcessor!.StartCaptureAsync().ConfigureAwait(false);
    }
    break;
```
