---
title: How to invoke a proactive greeting and pregenerated messages
titleSuffix: Azure AI services
description: Learn how to invoke a proactive greeting or generate pregenerated messages with the Voice live API.
manager: nitinme
author: goergenj
ms.author: jagoerge
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 11/05/2025
ms.custom: references_regions
zone_pivot_groups: voice-live-how-to-proactive-and-pregenerated-messages
# Customer intent: As a developer, I want to learn invoke a proactive greeting or generate pre-generated messages with the Voice live API.
---

# How to invoke a proactive greeting and pregenerated messages

The voice agent user experience build with the Voice live API can be enhanced for advanced use cases by adding proactive greeting messages or pregenerated messages.

Common use-cases are:
* Call center voice agents proactively greeting customers when answering calls
* Voice agents and avatars proactively greeting users to provide guidance at the start of the conversation on the available use cases
* Pregenerated phrases for legal or compliance sensitive responses

## Proactive greetings

Voice live provides two options to initialize a pro-active greeting:
1. Option 1: Requesting a LLM-generated greeting by sending a basic `response.create` event triggering the LLM to generate a first message.
1. Option 2: Requesting a pregenerated assistant greeting using a `response.create` event including the `pre_generated_assistant_message` configuration.

### Option 1 Requesting a LLM-generated greeting

Option 1 applies the LLMs instructions to generate an appropriate response. To ensure the response is generated in the default language of your voice agent, you need to include a specific instruction as part of the session's `instructions` configuration. Example: `Always start the conversation in English.`

::: zone pivot="programming-language-python"
[!INCLUDE [Python quickstart](./includes/how-to/voice-live-how-to-proactive-and-pregenerated-messages/python1.md)]
::: zone-end

### Option 2 Requesting a pregenerated assistant greeting

Option 2 uses a pregenerated greeting message to generate the greeting response. This option applies the same feature used for other pregenerated messages too.

::: zone pivot="programming-language-python"
[!INCLUDE [Python quickstart](./includes/how-to/voice-live-how-to-proactive-and-pregenerated-messages/python2.md)]
::: zone-end

### General advice

While there are multiple places where you could place the invocation for the greeting message, we recommend the following as shown in the above samples:
  - Send the proactive event immediately after `SESSION_UPDATED` and before starting microphone capture to avoid overlap if the user speaks early.
  - If you might repeat the greeting (for example, reconnect), guard with a flag like `self.conversation_started` as shown in the above samples.

## Pregenerated messages

The source for pregenerated messages in voice agents can be manifold. Reasons for using this feature could be that you want to use the exact answers provided from knowledge database queries, function calls, or mcp tools or it could be that there are hardcoded legal disclaimers within your application.

To request a Voice live output based on a pregenerated message, you need to send a `response.create` event including the `pre_generated_assistant_message` configuration.

::: zone pivot="programming-language-python"

The following example shows the required code for sending the correct event using the python SDK.

```python
pre_generated_message = "This is a pregenerated message text."
logger.info("Sending proactive greeting via response.create: %s", proactive_greeting)
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
    logger.exception("Failed to send proactive greeting event")
```
::: zone-end

## Related content

- Try out the [Voice live API quickstart](./voice-live-quickstart.md)
- Learn more about [How to use the Voice live API](./voice-live-how-to.md)
- See the [Voice live API reference](./voice-live-api-reference.md)
