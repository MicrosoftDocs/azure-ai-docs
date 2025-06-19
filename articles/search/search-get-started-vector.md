---
title: 'Quickstart: Vector Search'
titleSuffix: Azure AI Search
description: Learn how to call the Search REST and Azure SDK APIs for vector workloads in Azure AI Search.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 06/19/2025
zone_pivot_groups: search-get-started-vector-search
---

# Quickstart: Vector search

In this quickstart, you use the [Azure AI Search REST APIs](/rest/api/searchservice) to create, load, and query vectors.

In Azure AI Search, a [vector store](vector-store.md) has an index schema that defines vector and nonvector fields, a vector search configuration for algorithms that create the embedding space, and settings on vector field definitions that are evaluated at query time. The [Create Index](/rest/api/searchservice/indexes/create-or-update) REST API creates the vector store.

> [!NOTE]
> This quickstart omits the vectorization step and provides inline embeddings. If you want to add [built-in data chunking and vectorization](vector-search-integrated-vectorization.md) over your own content, try the [**Import and vectorize data wizard**](search-get-started-portal-import-vectors.md) for an end-to-end walkthrough.

## Prerequisites

- An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F).

- An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch) in your current subscription.
    - You can use a free search service for most of this quickstart, but we recommend the Basic tier or higher for larger data files.
    - To run the query example that invokes [semantic reranking](semantic-search-overview.md), your search service must be at the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

- [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).


---


::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/search-get-started-vector-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST quickstart](includes/quickstarts/search-get-started-vector-rest.md)]

::: zone-end


## Next steps

As a next step, we recommend learning how to invoke REST API calls [without API keys](search-get-started-rbac.md).

You might also want to review the demo code for [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python), [C#](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet), or [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript).
