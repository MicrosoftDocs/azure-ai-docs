---
title: include file for Voice Live proactive and pregenerated messages with csharp SDK how to
description: Learn how to invoke a proactive greeting or generate pregenerated messages with the Voice Live API
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/05/2025
ms.subservice: azure-ai-foundry-openai
---

[!INCLUDE [Header](../../common/voice-live-csharp.md)]

In this article, you learn how to set up Voice Live with proactive greetings and how to use pregenerated messages.

## Proactive greetings

Voice Live provides two options to initialize a pro-active greeting:
1. Option 1: Requesting a LLM-generated greeting by sending a basic `response.create` event triggering the LLM to generate a first message.
1. Option 2: Requesting a pregenerated assistant greeting using a `response.create` event including the `pre_generated_assistant_message` configuration.

### Option 1 Requesting a LLM-generated greeting

Option 1 applies the LLMs instructions to generate an appropriate response. To ensure the response is generated in the default language of your voice agent, you need to include a specific instruction as part of the session's `instructions` configuration. Example: `Always start the conversation in English.`

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

1. Find the class 'BasicVoiceAssistant' and add the following variable declaration:

    ```csharp
    private bool _conversationStarted;
    // Tracks whether the assistant can still cancel the current response (between ResponseCreated and ResponseDone)
    ```
    
1. Find the 'HandleSessionUpdateAsync' function in class 'BasicVoiceAssistant'.
1. Find the `sessionUpdated` event.
1. Replace the existing code handling the `sessionUpdated` event:

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

### Option 2 Requesting a pregenerated assistant greeting

Option 2 uses a pregenerated greeting message to generate the greeting response. This option applies the same feature used for other pregenerated messages too.

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

1. Find the class 'BasicVoiceAssistant' and add the following variable declaration:

    ```csharp
    private bool _conversationStarted;
    // Tracks whether the assistant can still cancel the current response (between ResponseCreated and ResponseDone)
    ```

1. Find the 'HandleSessionUpdateAsync' function in class 'BasicVoiceAssistant'.
1. Find the `sessionUpdated` event.
1. Replace the existing code handling the `sessionUpdated` event:

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
                    var proactiveGreeting = "Welcome to Contoso Insurance. You are now connected to our AI assistant. How can I help you today?";
                    var responseCreateEventPreGeneratedGreetingPayload = new
                    {
                        type = "response.create",
                        response = new
                        {
                            pre_generated_assistant_message = new
                            {
                                type = "message",
                                role = "assistant",
                                content = new[]
                                {
                                    new { type = "text", text = proactiveGreeting }
                                }
                            }
                        }
                    };
                    BinaryData responseCreateEventPreGeneratedGreeting = BinaryData.FromObjectAsJson(responseCreateEventPreGeneratedGreetingPayload);
                    await _session!.SendCommandAsync(responseCreateEventPreGeneratedGreeting, cancellationToken).ConfigureAwait(false);
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

### General advice

While there are multiple places where you could place the invocation for the greeting message, we recommend the following as shown in the above samples:
  - Send the proactive event immediately after `session.update` and before starting microphone capture to avoid overlap if the user speaks early.
  - If you might repeat the greeting (for example, reconnect), guard with a flag like `_conversationStarted` as shown in the above samples.

## Pregenerated messages

The source for pregenerated messages in voice agents can be manifold. Reasons for using this feature could be that you want to use the exact answers provided from knowledge database queries, function calls, or mcp tools. It could also be due to a need for hardcoded legal disclaimers within your application.

To request a Voice Live output based on a pregenerated message, you need to send a `response.create` event including the `pre_generated_assistant_message` configuration.

The following example shows the required code for sending the correct event using the python SDK.

```csharp
var preGeneratedMessage = "This is a pregenerated message text.";
_logger.LogInformation("Sending pregenerated message text via response.create");
try
{
    var responseCreateEventPreGeneratedMessagePayload = new
    {
        type = "response.create",
        response = new
        {
            pre_generated_assistant_message = new
            {
                type = "message",
                role = "assistant",
                content = new[]
                {
                    new { type = "text", text = preGeneratedMessage }
                }
            }
        }
    };
    BinaryData responseCreateEventPreGeneratedMessage = BinaryData.FromObjectAsJson(responseCreateEventPreGeneratedMessagePayload);
    await _session!.SendCommandAsync(responseCreateEventPreGeneratedMessage, cancellationToken).ConfigureAwait(false);
}
catch (Exception ex)
{
    _logger.LogError(ex, "Failed to send pregenerated message event");
}
```
