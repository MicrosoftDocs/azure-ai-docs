---
title: 'How to use GPT Realtime API for speech and audio with Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to use GPT Realtime API for speech and audio with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 09/16/2025
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions, ignite-2024
zone_pivot_groups: openai-portal-js-python-ts
recommendations: false
---

# GPT Realtime API for speech and audio


Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC or WebSocket to send audio input to the model and receive audio responses in real time. 

Follow the instructions in this article to get started with the Realtime API via WebSockets. Use the Realtime API via WebSockets in server-to-server scenarios where low latency isn't a requirement.

> [!TIP] 
> In most cases, we recommend using the [Realtime API via WebRTC](./how-to/realtime-audio-webrtc.md) for real-time audio streaming in client-side applications such as a web application or mobile app. WebRTC is designed for low-latency, real-time audio streaming and is the best choice for most use cases.

## Supported models

The GPT real-time models are available for global deployments.
- `gpt-4o-realtime-preview` (version `2024-12-17`)
- `gpt-4o-mini-realtime-preview` (version `2024-12-17`)
- `gpt-realtime` (version `2025-08-28`)
- `gpt-realtime-mini` (version `2025-10-06`)

For more information, see the [models and versions documentation](./concepts/models.md#audio-models).

## API support

Support for the Realtime API was first added in API version `2024-10-01-preview` (retired). Use version `2025-08-28` to access the latest Realtime API features. We recommend you select the generally available API version (without '-preview' suffix) when possible.

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Azure AI Foundry portal quickstart](includes/realtime-portal.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/realtime-javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](includes/realtime-python.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](includes/realtime-typescript.md)]

::: zone-end

## Related content

* Learn more about [How to use the Realtime API](./how-to/realtime-audio.md)
* See the [Realtime API reference](./realtime-audio-reference.md)
* Learn more about Azure OpenAI [quotas and limits](quotas-limits.md)
* Learn more about [Language and voice support for the Speech service](../../ai-services/speech-service/language-support.md)
