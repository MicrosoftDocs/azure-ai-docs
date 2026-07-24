---
title: Explore Code (.NET Tutorial)
description: Understand the .NET SDK Search integration queries used in the Search-enabled website with this cheat sheet.
ms.reviewer: diberry
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 07/24/2026
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
ms.devlang: csharp
ai-usage: ai-assisted
---

# Step 4 - Explore the .NET search code

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

In the previous lessons, you added search to a website that runs on Azure Container Apps. This lesson highlights the essential steps that establish integration. If you're looking for a cheat sheet on how to integrate search into your web app, this article explains what you need to know.

## Azure SDK Azure.Search.Documents

The Function app uses the Azure SDK for Azure AI Search:

* NuGet: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
* Reference documentation: [Client Library](/dotnet/api/overview/azure/search)

The function app authenticates through the SDK to the cloud-based Azure AI Search API using the search service name and index name. In Azure Container Apps, the container environment provides the configuration values. Managed identity is the default credential path.

## Managed identity authentication

The deployed API uses `DefaultAzureCredential` in `Search.cs` when key authentication isn't explicitly enabled. In Azure Container Apps, `DefaultAzureCredential` uses the managed identity assigned to the container app to request tokens for Azure AI Search.

The Bicep infrastructure assigns the managed identity access to the Azure AI Search data plane during `azd up`. This role assignment lets the API query the `good-books` index without storing a query key in the container environment.

To use API keys instead, set `SEARCH_USE_KEY_AUTH` before deployment:

```bash
azd env set SEARCH_USE_KEY_AUTH true
azd up
```

Use key authentication only when your environment requires it. Keep keys out of source control and rotate them according to your organization's security policy.

## Configure local settings

For local development, the sample `local.settings.json` file shows the values the function app expects. Use local settings for development only. In Azure Container Apps, deployment configuration provides the equivalent container environment values.

:::code language="json" source="~/azure-search-static-web-app/api/sample.local.settings.json":::

## Azure Function: Search the catalog

The [Search API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Search.cs) takes a search term and searches across the documents in the search index, returning a list of matches. Through the Suggest API, partial strings are sent to the search engine as the user types. The API suggests search terms such as book titles and authors across the documents in the search index, and returns a small list of matches.

The Azure function pulls in the search configuration information from the container environment, creates the Azure AI Search client, and fulfills the query.

The search suggester, `sg`, is defined in the [schema file](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/bulk-insert/BookSearchIndex.cs) used during bulk upload.

:::code language="csharp" source="~/azure-search-static-web-app/api/Search.cs" :::

## Client: Search from the catalog

Call the Azure Function in the React client at `\client\src\pages\Search\Search.jsx` with the following code to search for books.

:::code language="csharp" source="~/azure-search-static-web-app/client/src/pages/Search/Search.jsx" :::

## Client: Suggestions from the catalog

The Suggest function API is called in the React app at `\client\src\components\SearchBar\SearchBar.jsx` as part of the [Material UI Autocomplete component](https://mui.com/material-ui/react-autocomplete/). This component uses the input text to search for authors and books that match the input text. It then displays those possible matches as selectable items in the drop-down list.

:::code language="csharp" source="~/azure-search-static-web-app/client/src/components/SearchBar/SearchBar.jsx" :::

## Azure Function: Get specific document

The [Document Lookup API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Lookup.cs) takes an ID and returns the document object from the search index.

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
