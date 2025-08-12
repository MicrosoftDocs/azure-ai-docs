---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/31/2025
ms.author: eur
---

You create and run an application to use voice live directly with generative AI models for real-time voice agents.

- Using models directly allows specifying custom instructions (prompts) for each session, offering more flexibility for dynamic or experimental use cases.

- Models may be preferable when you want fine-grained control over session parameters or need to frequently adjust the prompt or configuration without updating an agent in the portal.

- The code for model-based sessions is simpler in some respects, as it does not require managing agent IDs or agent-specific setup.

- Direct model use is suitable for scenarios where agent-level abstraction or built-in logic is unnecessary.

To instead use the voice live API with agents, see the [voice live agents quickstart](/azure/ai-services/speech-service/voice-live-agents-quickstart).
