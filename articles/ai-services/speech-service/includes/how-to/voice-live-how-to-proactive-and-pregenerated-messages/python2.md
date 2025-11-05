---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-openai
ms.topic: include
ms.date: 11/05/2025
---

[!INCLUDE [Header](../../common/voice-live-python.md)]

To get started with the pro-active greeting, start with one of our [quickstart samples](../../../voice-live-quickstart.md).

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
