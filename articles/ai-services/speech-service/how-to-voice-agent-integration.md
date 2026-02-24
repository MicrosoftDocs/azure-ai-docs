---
title: How to build a voice agent
titleSuffix: Foundry Tools
description: Learn how to use Voice Live with Foundry Agent Service to build real-time voice agents.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 02/20/2026
author: PatrickFarley
reviewer: PatrickFarley
ms.author: pafarley
ms.reviewer: pafarley
zone_pivot_groups: voice-live-howto-agents
recommendations: false
---

# How to build a voice agent (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

::: zone pivot="programming-language-python"
[!INCLUDE [Python quickstart](./includes/how-to/voice-live-agents/python.md)]
::: zone-end

::: zone pivot="programming-language-csharp"
<!-- [!INCLUDE [Csharp quickstart](./includes/quickstarts/voice-live-agents/csharp.md)] -->
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [Java how-to](./includes/how-to/voice-live-agents/java.md)]
::: zone-end

## Migration from the previous version

The previous agent integration using Agent Service v1 (preview) used mostly the same integration code. However instead of `agent-name` the `agent-id` was used.

__**TBD, whether old agents can be accessed via the new Agent Service API?**__

__**Do we need to explain how to migrate from query params to strongly typed SDK code?**__

## Related content

- Explore [How to add proactive messages](./how-to-voice-live-proactive-messages.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
- See the [Voice Live API reference](./voice-live-api-reference-2025-10-01.md)
