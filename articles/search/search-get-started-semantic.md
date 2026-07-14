---
title: 'Quickstart: Semantic Ranking'
description: Learn how to change an existing index to use semantic ranker, which helps rescore search results and promote the most semantically relevant matches.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-python
  - ignite-2023
ms.topic: quickstart
ms.date: 07/14/2026
ai-usage: ai-assisted
zone_pivot_groups: search-sdks-rest
---

# Quickstart: Semantic ranking

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

In this quickstart, you add semantic ranking to an existing Azure AI Search index and run semantic queries to improve result relevance. Use the language tabs to choose your preferred SDK or REST workflow.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
+ An [Azure AI Search service](search-create-service-portal.md).
+ An existing index with descriptive text fields marked as `searchable` and `retrievable`.
+ Permissions to configure and query your search service. For role guidance, see [Role-based access control in Azure AI Search](search-security-rbac.md).

::: zone pivot="csharp"

[!INCLUDE [C#](includes/quickstarts/semantic-ranker-csharp.md)]

::: zone-end

::: zone pivot="java"

[!INCLUDE [Java](includes/quickstarts/semantic-ranker-java.md)]

::: zone-end

::: zone pivot="javascript"

[!INCLUDE [JavaScript](includes/quickstarts/semantic-ranker-javascript.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python](includes/quickstarts/semantic-ranker-python.md)]

::: zone-end

::: zone pivot="typescript"

[!INCLUDE [TypeScript](includes/quickstarts/semantic-ranker-typescript.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST](includes/quickstarts/semantic-ranker-rest.md)]

::: zone-end

## Clean up resources

[!INCLUDE [clean up resources (paid)](includes/resource-cleanup-paid.md)]

## Related content

+ [Semantic ranking in Azure AI Search](semantic-search-overview.md)
+ [Configure semantic ranker](semantic-how-to-configure.md)
+ [Add query rewrite to semantic ranker](semantic-how-to-query-rewrite.md)
+ [Use scoring profiles with semantic ranker](semantic-how-to-enable-scoring-profiles.md)
