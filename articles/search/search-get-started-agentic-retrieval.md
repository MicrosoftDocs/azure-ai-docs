---
title: "Quickstart: Agentic Retrieval"
description: Learn how to use agentic retrieval to create a knowledge base that processes multi-turn conversations.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 02/23/2026
ms.custom: dev-focus
ai-usage: ai-assisted
zone_pivot_groups: search-sdks-rest
# Customer intent: I want to learn how to use agentic retrieval to create a knowledge base that processes multi-turn conversations. The knowledge base should retrieve relevant information from a knowledge source that points to an Azure AI Search index and use an Azure OpenAI LLM to synthesize answers.

<!-- build26-sdk-migration-note -->
> [!NOTE]
> For 2026-05-01-preview SDK migration work, align code samples with the current preview SDK surface before publishing. Python and .NET support the message-based retrieve path used for answer synthesis. The tested Java, JavaScript, and TypeScript alpha packages currently use semantic intents for retrieve until their public models expose the full message-based REST contract. For the detailed migration checklist, see [Migrate agentic retrieval code](agentic-retrieval-how-to-migrate.md).
---

# Quickstart: Agentic retrieval

<!-- build26-sdk-migration-note -->
> [!NOTE]
> For 2026-05-01-preview SDK migration work, align code samples with the current preview SDK surface before publishing. Python and .NET support the message-based retrieve path used for answer synthesis. The tested Java, JavaScript, and TypeScript alpha packages currently use semantic intents for retrieve until their public models expose the full message-based REST contract. For the detailed migration checklist, see [Migrate agentic retrieval code](agentic-retrieval-how-to-migrate.md).

::: zone pivot="csharp"
[!INCLUDE [C#](includes/quickstarts/agentic-retrieval-csharp.md)]
::: zone-end

::: zone pivot="java"
[!INCLUDE [Java](includes/quickstarts/agentic-retrieval-java.md)]
::: zone-end

::: zone pivot="javascript"
[!INCLUDE [JavaScript](includes/quickstarts/agentic-retrieval-javascript.md)]
::: zone-end

::: zone pivot="python"
[!INCLUDE [Python](includes/quickstarts/agentic-retrieval-python.md)]
::: zone-end

::: zone pivot="typescript"
[!INCLUDE [TypeScript](includes/quickstarts/agentic-retrieval-typescript.md)]
::: zone-end

::: zone pivot="rest"
[!INCLUDE [REST](includes/quickstarts/agentic-retrieval-rest.md)]
::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base using the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md)
+ [Tutorial: Build an end-to-end agentic retrieval solution](agentic-retrieval-how-to-create-pipeline.md)
