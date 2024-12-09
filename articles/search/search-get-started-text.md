---
title: 'Quickstart: Full text search using the Azure SDKs'
titleSuffix: Azure AI Search
description: "Learn how to create, load, and query a search index using the Azure SDKs for .NET, Python, Java, and JavaScript."
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - devx-track-js
  - devx-track-ts
  - devx-track-python
  - ignite-2023
ms.topic: quickstart
ms.date: 11/01/2024
---

# Quickstart: Full text search using the Azure SDKs

Learn how to use the *Azure.Search.Documents* client library in an Azure SDK to create, load, and query a search index using sample data for [full text search](search-lucene-query-architecture.md). Full text search uses Apache Lucene for indexing and queries, and a BM25 ranking algorithm for scoring results.

This quickstart has steps for the following SDKs:

+ [Azure SDK for .NET](?tabs=dotnet#create-load-and-query-an-index)
+ [Azure SDK for Python](?tabs=python#create-load-and-query-an-index)
+ [Azure SDK for Java](?tabs=java#create-load-and-query-an-index)
+ [Azure SDK for JavaScript/Typescript](?tabs=javascript#create-load-and-query-an-index)

## Prerequisites

+ An Azure account with an active subscription. You can [create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?icid=azurefreeaccount).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) if you don't have one. You can use a free tier for this quickstart.

+ An API key and service endpoint for your service. Sign in to the [Azure portal](https://portal.azure.com) and [find your search service](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/CognitiveSearch).

  In the **Overview** section, copy the URL and save it to a text editor for a later step. An example endpoint might look like `https://mydemo.search.windows.net`.

  In the **Settings** > **Keys** section, copy and save an admin key for full rights to create and delete objects. There are two interchangeable primary and secondary keys. Choose either one.

  :::image type="content" source="media/search-get-started-rest/get-url-key.png" alt-text="Screenshot that shows the HTTP endpoint and the primary and secondary API key locations.":::

## Create, load, and query an index

Choose a programming language for the next step. The **Azure.Search.Documents** client libraries are available in Azure SDKs for .NET, Python, Java, and JavaScript/Typescript.

## [**.NET**](#tab/dotnet)

[!INCLUDE [dotnet-sdk-quickstart](includes/quickstarts/dotnet.md)]

## [**Python**](#tab/python)

[!INCLUDE [python-sdk-quickstart](includes/quickstarts/python.md)]

## [**Java**](#tab/java)

[!INCLUDE [java-sdk-quickstart](includes/quickstarts/java.md)]

## [**JavaScript**](#tab/javascript)

[!INCLUDE [javascript-sdk-quickstart](includes/quickstarts/javascript.md)]

## [**TypeScript**](#tab/typescript)

[!INCLUDE [typescript-sdk-quickstart](includes/quickstarts/typescript.md)]

---

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal, using the **All resources** or **Resource groups** link in the left-navigation pane.

If you're using a free service, remember that you're limited to three indexes, indexers, and data sources. You can delete individual items in the Azure portal to stay under the limit.

## Next step

In this quickstart, you worked through a set of tasks to create an index, load it with documents, and run queries. At different stages, we took shortcuts to simplify the code for readability and comprehension. Now that you're familiar with the basic concepts, try a tutorial that calls the Azure AI Search APIs in a web app.

> [!div class="nextstepaction"]
> [Tutorial: Add search to web apps](tutorial-csharp-overview.md)
