---
title: 'Quickstart: Full Text Search Using the Azure SDKs'
titleSuffix: Azure AI Search
description: "Learn how to create, load, and query a search index using the Azure SDKs for .NET, Python, Java, and JavaScript."
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - devx-track-js
  - devx-track-ts
  - devx-track-python
  - ignite-2023
ms.topic: quickstart
zone_pivot_groups: search-quickstart-full-text
ms.date: 03/04/2025
---

# Quickstart: Full text search using the Azure SDKs

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# quickstart](includes/quickstarts/full-text-csharp.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java quickstart](includes/quickstarts/full-text-java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](includes/quickstarts/full-text-javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/quickstarts/full-text-python.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](includes/quickstarts/full-text-typescript.md)]

::: zone-end

## Clean-up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

If you're using a free service, remember that you're limited to three indexes, indexers, and data sources. You can delete individual items in the Azure portal to stay under the limit.

## Next step

In this quickstart, you worked through a set of tasks to create an index, load it with documents, and run queries. At different stages, we took shortcuts to simplify the code for readability and comprehension.

Now that you're familiar with the basic concepts, try a tutorial that calls the Azure AI Search APIs in a web app:

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
