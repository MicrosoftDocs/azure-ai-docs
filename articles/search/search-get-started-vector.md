---
title: 'Quickstart: Vector Search'
description: Learn how to call the Search REST and Azure SDK APIs for vector workloads in Azure AI Search.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - dev-focus
ms.topic: quickstart
ms.date: 07/21/2026
ai-usage: ai-assisted
zone_pivot_groups: search-sdks-rest
---

# Quickstart: Vector search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!NOTE]
> For embedding models in vector search workflows, Azure AI Search supports `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large` from Azure OpenAI. For AI-enriched workflows using chat completion models, see [Model retirement schedules](/azure/foundry/openai/concepts/model-retirement-schedule) to check deprecation status of GPT-4 family models.

::: zone pivot="csharp"

[!INCLUDE [C#](includes/quickstarts/search-get-started-vector-csharp.md)]

::: zone-end

::: zone pivot="java"

[!INCLUDE [Java](includes/quickstarts/search-get-started-vector-java.md)]

::: zone-end

::: zone pivot="javascript"

[!INCLUDE [JavaScript](includes/quickstarts/search-get-started-vector-javascript.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python](includes/quickstarts/search-get-started-vector-python.md)]

::: zone-end

::: zone pivot="typescript"

[!INCLUDE [TypeScript](includes/quickstarts/search-get-started-vector-typescript.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST](includes/quickstarts/search-get-started-vector-rest.md)]

::: zone-end

## Related content

+ [Vector search in Azure AI Search](vector-search-overview.md)
+ [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) GitHub repository
