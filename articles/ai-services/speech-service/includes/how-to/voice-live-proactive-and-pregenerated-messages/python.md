---
title: include file for Voice Live proactive and pregenerated messages with python SDK how to
description: Learn how to invoke a proactive greeting or generate pregenerated messages with the Voice Live API
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/09/2025
ms.subservice: azure-ai-foundry-openai
---

[!INCLUDE [Header](../../common/voice-live-python.md)]

In this article, you learn how to set up Voice Live with proactive greetings and how to use pregenerated messages.

## Proactive greetings

Voice Live provides two options to initialize a pro-active greeting:
1. Option 1: Requesting a LLM-generated greeting by sending a basic `response.create` event triggering the LLM to generate a first message.
1. Option 2: Requesting a pregenerated assistant greeting using a `response.create` event including the `pre_generated_assistant_message` configuration.

### Option 1 Requesting a LLM-generated greeting

Option 1 applies the LLMs instructions to generate an appropriate response. To ensure the response is generated in the default language of your voice agent, you need to include a specific instruction as part of the session's `instructions` configuration. Example: `Always start the conversation in English.`

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

1. Find the class 'BasicVoiceAssistant' and add the following variable declaration:

    ```python
    self.conversation_started = False
    ```

1. Find the '_handle_event_' function in class 'BasicVoiceAssistant'.
1. Find the `SESSSION_UPDATED` event.
1. Replace the existing code handling the `SESSSION_UPDATED` event:

    ```python
    if event.type == ServerEventType.SESSION_UPDATED:
        logger.info("Session ready: %s", event.session.id)
        self.session_ready = True
    
        # Proactive greeting
        if not self.conversation_started:
            self.conversation_started = True
            logger.info("Sending proactive greeting request")
            try:
                await conn.response.create()
    
            except Exception:
                logger.exception("Failed to send proactive greeting request")
    
        # Start audio capture once session is ready
        ap.start_capture()
    ```

### Option 2 Requesting a pregenerated assistant greeting

Option 2 uses a pregenerated greeting message to generate the greeting response. This option applies the same feature used for other pregenerated messages too.

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

1. Find the class 'BasicVoiceAssistant' and add the following variable declaration:

    ```python
    self.conversation_started = False
    ```
    
1. Find the '_handle_event_' function in class 'BasicVoiceAssistant'.
1. Find the `SESSSION_UPDATED` event.
1. Replace the existing code handling the `SESSSION_UPDATED` event:

    ```python
    if event.type == ServerEventType.SESSION_UPDATED:
        logger.info("Session ready: %s", event.session.id)
        self.session_ready = True
    
        # Proactive greeting with pre-generated message
        if not self.conversation_started:
            self.conversation_started = True
            proactive_greeting = "Welcome to Contoso Insurance. You are now connected to our AI assistant. How can I help you today?"
            logger.info("Sending proactive greeting via response.create: %s", proactive_greeting)
            try:
                await conn.send({
                    "type": "response.create",
                    "response": {
                        "pre_generated_assistant_message": {
                            "type": "message",
                            "role": "assistant",
                            "content": [
                                {"type": "text", "text": proactive_greeting}
                            ],
                        }
                    }
                })
            except Exception:
                logger.exception("Failed to send proactive greeting event")
    
        # Start audio capture once session is ready
        ap.start_capture()
    ```

### General advice

While there are multiple places where you could place the invocation for the greeting message, we recommend the following as shown in the above samples:
  - Send the proactive event immediately after `session.update` and before starting microphone capture to avoid overlap if the user speaks early.
  - If you might repeat the greeting (for example, reconnect), guard with a flag like `self.conversation_started` as shown in the above samples.

## Pregenerated messages

The source for pregenerated messages in voice agents can be manifold. Reasons for using this feature could be that you want to use the exact answers provided from knowledge database queries, function calls, or mcp tools. It could also be due to a need for hardcoded legal disclaimers within your application.

To request a Voice Live output based on a pregenerated message, you need to send a `response.create` event including the `pre_generated_assistant_message` configuration.

The following example shows the required code for sending the correct event using the python SDK.

```python
pre_generated_message = "This is a pregenerated message text."
logger.info("Sending pregenerated message text via response.create: %s", proactive_greeting)
try:
    await conn.send({
        "type": "response.create",
        "response": {
            "pre_generated_assistant_message": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {"type": "text", "text": pre_generated_message}
                ],
            }
        }
    })
except Exception:
    logger.exception("Failed to send pregenerated message event")
```