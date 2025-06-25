---
title: 'Quickstart: Add Semantic Ranking to an Index Using .NET or Python'
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
ms.date: 06/13/2025
zone_pivot_groups: search-get-started-semantic
---

# Quickstart: Semantic ranking using .NET or Python

In this quickstart, you learn about the index and query modifications that invoke semantic ranker.

In Azure AI Search, [semantic ranking](semantic-search-overview.md) is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and the query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort. Semantic ranking is also required for [agentic retrieval (preview)](search-agentic-retrieval-concept.md).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md), at Basic tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ A new or existing index with descriptive or verbose text fields, attributed as retrievable in your index. You can add a semantic configuration to an existing index with no rebuild requirement. Semantic ranking is effective on content that's informational or descriptive.

## How to add a semantic ranker

To use semantic ranker, add a *semantic configuration* to a search index, and add parameters to a query. If you have an existing index, you can make these changes without having to reindex your content because there's no impact on the structure of your searchable content.

+ A semantic configuration sets a priority order for fields that contribute a title, keywords, and content used in semantic reranking. Field prioritization allows for faster processing.

+ Queries that invoke semantic ranker include parameters for query type and whether captions and answers are returned. You can add these parameters to your existing query logic. There's no conflict with other parameters.

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# quickstart](includes/quickstarts/semantic-ranker-csharp.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](includes/quickstarts/semantic-ranker-python.md)]

::: zone-end

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

## Next step

In this quickstart, you learned how to invoke semantic ranking on an existing index. We recommend trying semantic ranking on your own indexes as a next step. However, if you want to continue with demos, try the following tutorial:

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
