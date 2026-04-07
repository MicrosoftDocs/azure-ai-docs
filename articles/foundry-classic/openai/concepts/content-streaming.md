---
title: "Content Streaming in Azure OpenAI (classic)"
description: "Learn about content streaming options in Azure OpenAI, including default and asynchronous filtering modes, and their impact on latency and performance. (classic)"
author: ssalgadodev
ms.author: ssalgado
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 01/15/2026
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
ROBOTS: NOINDEX, NOFOLLOW
---

# Content streaming (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/content-streaming.md)

[!INCLUDE [content-streaming 1](../../../foundry/openai/includes/concepts-content-streaming-1.md)]

## Default filtering behavior

The content filtering system is integrated and enabled by default for all customers. In the default streaming scenario, completion content buffers, the content filtering system runs on the buffered content, and – depending on the content filtering configuration – content is returned to the user if it doesn't violate the content filtering policy (Microsoft's default or a custom user configuration), or it is immediately blocked and a content filtering error is returned instead. This process repeats until the end of the stream. Content is fully vetted according to the content filtering policy before it's returned to the user. Content isn't returned token-by-token in this case, but in "content chunks" of the respective buffer size.

[!INCLUDE [content-streaming 2](../../../foundry/openai/includes/concepts-content-streaming-2.md)]
