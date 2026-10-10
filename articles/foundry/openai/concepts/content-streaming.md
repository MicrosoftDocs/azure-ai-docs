---
title: "Content Streaming in Azure OpenAI"
description: "Learn about content streaming options in Azure OpenAI, including default and asynchronous filtering modes, and their impact on latency and performance."
author: ssalgadodev
ms.author: ssalgado
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: concept-article
ms.date: 09/08/2026
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Content streaming

[!INCLUDE [content-streaming 1](../includes/concepts-content-streaming-1.md)]

## Default filtering behavior

The content guardrails system is integrated and enabled by default for all customers. In the default streaming scenario, completion content buffers, the content guardrail system runs on the buffered content, and – depending on the guardrail configuration – content is returned to the user if it doesn't violate the guardrail policy (Microsoft's default or a custom user configuration), or it is immediately blocked and a guardrail error is returned instead. This process repeats until the end of the stream. Content is fully vetted according to the guardrail policy before it's returned to the user. Content isn't returned token-by-token in this case, but in "content chunks" of the respective buffer size.

> [!NOTE]
> The last segment of a streamed response might be returned before the guardrail policy is applied to it. In tests with a custom blocklist (blocking, applied to completions) on a `gpt-4o` deployment, a blocklisted term in roughly the last 15 to 30 words of a streamed response was returned to the client with `finish_reason: "stop"`. The same response was blocked when `stream` was `false`, and blocked mid-stream when more text followed the term. If your application can't tolerate policy-violating content reaching the client, use non-streaming requests or apply your own filtering to the final segment of the stream.

[!INCLUDE [content-streaming 2](../includes/concepts-content-streaming-2.md)]
