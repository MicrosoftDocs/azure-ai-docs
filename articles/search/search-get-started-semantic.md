---
title: 'Quickstart: Semantic Ranking'
titleSuffix: Azure AI Search
description: Learn how to change an existing index to use semantic ranker, which helps rescore search results and promote the most semantically relevant matches.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-python
  - ignite-2023
ms.topic: quickstart
ms.date: 07/09/2025
zone_pivot_groups: search-get-started-semantic
---

# Quickstart: Semantic ranking

::: zone pivot="csharp"

[!INCLUDE [C# quickstart](includes/quickstarts/semantic-ranker-csharp.md)]

::: zone-end

::: zone pivot="javascript"

[!INCLUDE [JavaScript quickstart](includes/quickstarts/semantic-ranker-javascript.md)]

::: zone-end

::: zone pivot="java"

[!INCLUDE [Java quickstart](includes/quickstarts/semantic-ranker-java.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/semantic-ranker-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST quickstart](includes/quickstarts/semantic-ranker-rest.md)]

::: zone-end

::: zone pivot="typescript"

[!INCLUDE [TypeScript quickstart](includes/quickstarts/semantic-ranker-typescript.md)]

::: zone-end

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

## Related content

In this quickstart, you learned how to invoke semantic ranking on an existing index. We recommend trying semantic ranking on your own indexes as a next step. The following articles can help you get started.

+ [Semantic ranking overview](semantic-search-overview.md)
+ [Configure semantic ranker ](semantic-how-to-configure.md)
+ [Add query rewrite to semantic ranking](semantic-how-to-query-rewrite.md)
+ [Use scoring profiles and semantic ranking together](semantic-how-to-enable-scoring-profiles.md)
