---
title: 'How to use GPT-4o Realtime API for speech and audio with Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to use GPT-4o Realtime API for speech and audio with Azure OpenAI.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 3/20/2025
author: eric-urban
ms.author: eur
ms.custom: references_regions, ignite-2024
zone_pivot_groups: openai-portal-js-python-ts
recommendations: false
---

# GPT-4o Realtime API for speech and audio (Preview)

[!INCLUDE [Feature preview](includes/preview-feature.md)]

Azure OpenAI GPT-4o Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. The GPT-4o audio `realtime` API is designed to handle real-time, low-latency conversational interactions, making it a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of the Realtime API need to deliver and receive audio from an end-user in real time, including applications that use WebRTC or a telephony system. The Realtime API isn't designed to connect directly to end user devices and relies on client integrations to terminate end user audio streams. 

## Supported models

The GPT 4o real-time models are available for global deployments.
- `gpt-4o-realtime-preview` (version `2024-12-17`)
- `gpt-4o-mini-realtime-preview` (version `2024-12-17`)

See the [models and versions documentation](./concepts/models.md#audio-models) for more information.

## API support

Support for the Realtime API was first added in API version `2024-10-01-preview` (retired). Use version `2025-04-01-preview` to access the latest Realtime API features. 

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
