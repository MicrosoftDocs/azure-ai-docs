---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
ms.author: pafarley
---

You can create and run an application to use Voice Live with agents for real-time voice conversations.

Agents offer several advantages over direct API calls:

- Manage prompts and configuration centrally in the agent itself, not in session code.
- Encapsulate complex logic and conversational behaviors for easier updates.
- Reduce manual configuration by using the agent ID to connect automatically.
- Support multiple variations and business logic without changing client code.

To use Voice Live without Foundry agents, see the [Voice Live API quickstart](/azure/ai-services/speech-service/voice-live-quickstart).

> [!TIP]
> You don't need to deploy an audio model with Microsoft Foundry to use Voice Live. Voice Live is fully managed and automatically deploys the model for you. For model availability, see the [Voice Live overview documentation](../../../voice-live.md).
