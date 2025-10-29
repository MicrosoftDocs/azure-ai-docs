---
title: "Explore code (.NET tutorial)"
titleSuffix: Azure AI Search
description: Understand the .NET SDK Search integration queries used in the Search-enabled website with this cheat sheet.
manager: nitinme
author: diberry
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 09/23/2025
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
ms.devlang: csharp
---

# Step 4 - Explore the .NET search code

In the previous lessons, you added search to a static web app. This lesson highlights the essential steps that establish integration. If you're looking for a cheat sheet on how to integrate search into your web app, this article explains what you need to know.

## Azure SDK Azure.Search.Documents

The Function app uses the Azure SDK for Azure AI Search:

* NuGet: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
* Reference Documentation: [Client Library](/dotnet/api/overview/azure/search)

The function app authenticates through the SDK to the cloud-based Azure AI Search API using your resource name, resource key, and index name. The secrets are stored in the static web app settings and pulled in to the function as environment variables. 

## Configure secrets in a local.settings.json file

:::code language="json" source="~/azure-search-static-web-app/api/sample.local.settings.json":::

## Azure Function: Search the catalog

The [Search API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Search.cs) takes a search term and searches across the documents in the search index, returning a list of matches. Through the Suggest API, partial strings are sent to the search engine as the user types, suggesting search terms such as book titles and authors across the documents in the search index, and returning a small list of matches. 

The Azure function pulls in the search configuration information, and fulfills the query. 

The search suggester, `sg`, is defined in the [schema file](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/bulk-insert/BookSearchIndex.cs) used during bulk upload.

:::code language="csharp" source="~/azure-search-static-web-app/api/Search.cs" :::

## Client: Search from the catalog

Call the Azure Function in the React client at `\client\src\pages\Search\Search.jsx` with the following code to search for books. 

:::code language="csharp" source="~/azure-search-static-web-app/client/src/pages/Search/Search.jsx" :::

## Client: Suggestions from the catalog

The Suggest function API is called in the React app at `\client\src\components\SearchBar\SearchBar.jsx` as part of the [Material UI's Autocomplete component](https://mui.com/material-ui/react-autocomplete/). This component uses the input text to search for authors and books that match the input text then displays those possible matches at selectable items in the drop-down list. 

:::code language="csharp" source="~/azure-search-static-web-app/client/src/components/SearchBar/SearchBar.jsx" :::

## Azure Function: Get specific document 

The [Document Lookup API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Lookup.cs) takes an ID and returns the document object from the Search Index. 

:::code language="csharp" source="~/azure-search-static-web-app/api/Lookup.cs"  :::

## Client: Get specific document 

This function API is called in the React app at `\client\src\pages\Details\Details.jsx` as part of component initialization:

:::code language="csharp" source="~/azure-search-static-web-app/client/src/pages/Details/Details.jsx"  :::

## C# models to support function app

The following models are used to support the functions in this app.

:::code language="csharp" source="~/azure-search-static-web-app/api/Models.cs" :::

## Next steps

To continue learning more about Azure AI Search development, try this next tutorial about indexing:

* [Index Azure SQL data](search-indexer-tutorial.md)
