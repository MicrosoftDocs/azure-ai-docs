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
---

# Quickstart: Semantic ranking using .NET or Python

In this quickstart, you learn about the index and query modifications that invoke semantic ranker.

In Azure AI Search, [semantic ranking](semantic-search-overview.md) is query-side functionality that uses machine reading comprehension from Microsoft to rescore search results, promoting the most semantically relevant matches to the top of the list. Depending on the content and the query, semantic ranking can [significantly improve search relevance](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167) with minimal developer effort.

> [!NOTE]
> For an example of an Azure AI Search solution with ChatGPT interaction, see [this demo](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/README.md) or [this accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

+ An [Azure AI Search service](search-create-service-portal.md), at Basic tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ An API key and a search service endpoint. To obtain them:

  1. Sign in to the [Azure portal](https://portal.azure.com) and find your search service.

  1. On **Overview**, copy the URL and save it for a later step. An example endpoint might look like `https://mydemo.search.windows.net`.

  1. On **Keys**, copy and save an admin key for full rights to create and delete objects. There are two interchangeable primary and secondary keys. Choose either one.

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

## Next step

In this quickstart, you learned how to invoke semantic ranking on an existing index. We recommend trying semantic ranking on your own indexes as a next step. However, if you want to continue with demos, try the following tutorial:

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
