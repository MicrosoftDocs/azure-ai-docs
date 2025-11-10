---
title: 'Quickstart: Generative Search (RAG)'
titleSuffix: Azure AI Search
description: Learn how to use grounding data from Azure AI Search with a chat model on Azure OpenAI.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: quickstart
ms.date: 10/15/2025
zone_pivot_groups: programming-languages-ai-search-rag-qs
---

# Quickstart: Classic generative search (RAG) using grounding data from Azure AI Search

In this quickstart, you send queries to a chat completion model for a conversational search experience over your indexed content on Azure AI Search. After setting up Azure OpenAI and Azure AI Search resources in the Azure portal, you run code to call the APIs.

> [!NOTE]
> We now recommend [agentic retrieval](search-get-started-agentic-retrieval.md) for RAG workflows, but classic RAG is simpler. If it meets your application requirements, it's still a good choice.

::: zone pivot="csharp"

[!INCLUDE [.NET quickstart](includes/quickstarts/search-get-started-rag-dotnet.md)]

::: zone-end

::: zone pivot="java"

[!INCLUDE [Java quickstart](includes/quickstarts/search-get-started-rag-java.md)]

::: zone-end

::: zone pivot="javascript"

[!INCLUDE [JavaScript quickstart](includes/quickstarts/search-get-started-rag-javascript.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/search-get-started-rag-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [Rest quickstart](includes/quickstarts/search-get-started-rag-rest.md)]

::: zone-end

::: zone pivot="typescript"

[!INCLUDE [TypeScript quickstart](includes/quickstarts/search-get-started-rag-typescript.md)]

::: zone-end

## Related content

- [Tutorial: Build a RAG solution in Azure AI Search](tutorial-rag-build-solution.md)