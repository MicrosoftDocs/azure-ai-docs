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

::: zone pivot="csharp"

[!INCLUDE [C# quickstart](includes/quickstarts/dotnet-semantic.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/python-semantic.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST quickstart](includes/quickstarts/semantic-ranker-rest.md)]

::: zone-end

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

## Next step

In this quickstart, you learned how to invoke semantic ranking on an existing index. We recommend trying semantic ranking on your own indexes as a next step. However, if you want to continue with demos, try the following tutorial:

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
