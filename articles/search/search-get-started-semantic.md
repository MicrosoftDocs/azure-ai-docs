---
title: 'Quickstart: semantic ranking'
titleSuffix: Azure AI Search
description: Change an existing index to use semantic ranker to rescore search results and promote the most semantically relevant matches.
author: HeidiSteen
manager: nitinme
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-python
  - ignite-2023
ms.topic: quickstart
ms.date: 10/22/2024
---

# Quickstart: Semantic ranking with .NET or Python

In Azure AI Search, [semantic ranking](semantic-search-overview.md) is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and the query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167), with minimal work for the developer.

This quickstart walks you through the index and query modifications that invoke semantic ranker.

> [!NOTE]
> For an Azure AI Search solution example with ChatGPT interaction, see [this demo](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md) or [this accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator).

## Prerequisites

+ An Azure account with an active subscription. You can [create an account for free](https://azure.microsoft.com/free/).

+ An Azure AI Search resource, at Basic tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An API key and search service endpoint. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices).

  In **Overview**, copy the URL and save it for a later step. An example endpoint might look like `https://mydemo.search.windows.net`.

  In **Keys**, copy and save an admin key for full rights to create and delete objects. There are two interchangeable primary and secondary keys. Choose either one.

  :::image type="content" source="media/search-get-started-rest/get-url-key.png" alt-text="Screenshot showing where to find your search service's HTTP endpoint and access key.":::

## Add semantic ranking

To use semantic ranker, add a *semantic configuration* to a search index, and add parameters to a query. If you have an existing index, you can make these changes without having to reindex your content because there's no impact on the structure of your searchable content.

+ A semantic configuration sets a priority order for fields that contribute a title, keywords, and content used in semantic reranking. Field prioritization allows for faster processing.

+ Queries that invoke semantic ranker include parameters for query type and whether captions and answers are returned. You can add these parameters to your existing query logic. There's no conflict with other parameters.

### [**.NET**](#tab/dotnet)

[!INCLUDE [dotnet-sdk-semantic-quickstart](includes/quickstarts/dotnet-semantic.md)]

### [**Python**](#tab/python)

[!INCLUDE [python-sdk-semantic-quickstart](includes/quickstarts/python-semantic.md)]

---

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

## Next steps

In this quickstart, you learned how to invoke semantic ranking on an existing index. We recommend trying semantic ranking on your own indexes as a next step. However, if you want to continue with demos, visit the following link.

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
