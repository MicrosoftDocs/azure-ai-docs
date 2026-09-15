---
title: Explore Azure AI Search query integration in a C# app
description: Learn how C# query integration works in an Azure AI Search app, including managed identity, search requests, suggestions, and document lookup.
ms.reviewer: diberry
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 08/07/2026
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
ms.devlang: csharp
ai-usage: ai-assisted
---

# Explore Azure AI Search query integration in a C# app

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

In the previous step, you deployed the search-enabled website to Azure Container Apps. This article highlights the essential steps that establish search integration. Think of it as a cheat sheet for integrating search into your web app.

## Azure SDK Azure.Search.Documents

The API uses the Azure SDK for Azure AI Search:

- NuGet: [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/)
- Reference documentation: [Client Library](/dotnet/api/overview/azure/search)

The API authenticates through the SDK to the cloud-based Azure AI Search API by using the search service name and index name. In Azure Container Apps, the container environment provides the configuration values. Managed identity is the default credential path.

## Managed identity authentication

Each Azure function in the API creates its `SearchClient` through a shared `SearchClientFactory` class, so every function authenticates the same way. By default, the factory builds a `DefaultAzureCredential` and uses it to request tokens for Azure AI Search. In Azure Container Apps, `DefaultAzureCredential` resolves to the managed identity assigned to the container app.

The following method from `SearchClientFactory.cs` creates that credential. When the container app has a user-assigned managed identity, the client ID from the `AZURE_CLIENT_ID` environment variable is passed to `DefaultAzureCredentialOptions` so token acquisition isn't ambiguous.

```csharp
private static DefaultAzureCredential CreateManagedIdentityCredential()
{
    var options = new DefaultAzureCredentialOptions();

    if (!string.IsNullOrWhiteSpace(ManagedIdentityClientId))
    {
        options.ManagedIdentityClientId = ManagedIdentityClientId;
    }

    return new DefaultAzureCredential(options);
}
```

The Bicep infrastructure assigns the managed identity access to the Azure AI Search data plane during `azd up`. This role assignment lets the API query the `good-books` index without storing a query key in the container environment.

### Local vs. deployed credential resolution

Locally, if `AZURE_CLIENT_ID` is unset, `DefaultAzureCredential` falls back through its standard credential chain and resolves to your signed-in developer credential, such as the Azure CLI or Visual Studio Code account you used to sign in. When deployed to Azure Container Apps, the Bicep infrastructure sets `AZURE_CLIENT_ID` to the user-assigned managed identity's client ID, so `DefaultAzureCredential` targets that identity specifically instead of resolving ambiguously among multiple identities that a host can expose.

To use API keys instead, set `USE_KEYLESS_AUTH` to `false` before deployment:

```bash
azd env set USE_KEYLESS_AUTH false
azd up
```

Use key authentication only when your environment requires it.

## Local development settings

For local development, the sample `sample.local.settings.json` file shows the values the API expects. Use local settings for development only. In Azure Container Apps, deployment configuration provides the equivalent container environment values.

| Setting | Purpose | Required when |
|--|--|--|
| `SearchServiceName` | Name of the Azure AI Search service. Combines with `.search.windows.net` to build the service endpoint URI. | Always |
| `SearchIndexName` | Name of the search index to query. Defaults to `good-books` if unset. | Optional |
| `SEARCH_USE_KEY_AUTH` | Default is false, uses managed identity. Set to `true` to use an API key instead of managed identity. | Optional key authentication |
| `SearchApiKey` | Admin key for Azure AI Search. | Required when `SEARCH_USE_KEY_AUTH` is `true` |

:::code language="json" source="~/azure-search-static-web-app/api/sample.local.settings.json" :::

## Function: Search the catalog

The [Search API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Search.cs) takes a search term and searches across the documents in the search index, returning a list of matches. Through the Suggest API, partial strings are sent to the search engine as the user types. The API suggests search terms, such as book titles and authors, based on documents in the search index and returns a small list of matches.

The Azure function pulls in the search configuration information from the container environment, creates the Azure AI Search client, and fulfills the query.

The search suggester, `sg`, is defined in the [schema file](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/bulk-insert/BookSearchIndex.cs) used during bulk upload.

:::code language="csharp" source="~/azure-search-static-web-app/api/Search.cs" :::

To verify the function independently, call `/api/search` with a search term in the request body and confirm the response includes matching book documents, a total count, and facet values.

## Client: Search the catalog

The React client's Search page calls the `search` Azure function whenever the user enters a query, changes a facet filter, or moves to a new page of results. The client sends the search text, the current page's `skip` and `top` values, and any selected author or language filters in the POST body to `/api/search`. The function returns a list of matching book documents, a total count, and facet values, which the page uses to render the result list, pager, and facet filters. The following code in `\client\src\pages\Search\Search.jsx` builds that request and stores the response in component state:

:::code language="jsx" source="~/azure-search-static-web-app/client/src/pages/Search/Search.jsx" :::

To verify this integration, enter a search term in the website's search bar and confirm that the result list, result count, and facets all update.

## Client: Suggestions from the catalog

The Suggest function API is called in the React app at `\client\src\components\SearchBar\SearchBar.jsx` as part of the [Material UI Autocomplete component](https://mui.com/material-ui/react-autocomplete/). This component uses the input text to search for authors and books that match. It then displays those possible matches as selectable items in the dropdown list.

:::code language="jsx" source="~/azure-search-static-web-app/client/src/components/SearchBar/SearchBar.jsx" :::

To verify this integration, enter text in the website's search bar and confirm that matching book titles and authors appear in the autocomplete dropdown.

## Function: Get specific document

The [Document Lookup API](https://github.com/Azure-Samples/azure-search-static-web-app/blob/main/api/Lookup.cs) retrieves the full document for a single book after a user selects it from the search results. The function reads a book `id` from the request's query string, uses `SearchClientFactory` to create an authenticated `SearchClient`, and calls `GetDocumentAsync` to look up that key in the `good-books` index. It returns the resulting document wrapped in a `LookupOutput` object.

:::code language="csharp" source="~/azure-search-static-web-app/api/Lookup.cs" :::

To verify the Lookup function independently, call `/api/lookup` with a valid book `id` and confirm the response returns that book's full document.

## Client: Get specific document

When a user selects a book from the search results, the Details page needs the complete document for that book, including fields not shown in the summary list. The Details page reads the book `id` from the route parameters and calls the Document Lookup API through `/api/lookup` when the component mounts. It stores the returned document in component state and renders it in the **Result** and **Raw Data** tabs. The following code in `\client\src\pages\Details\Details.jsx` performs this lookup during component initialization:

:::code language="jsx" source="~/azure-search-static-web-app/client/src/pages/Details/Details.jsx" :::

To verify this integration, select a book from the search results and confirm that its details, including cover image, authors, and rating, appear on the Details page.

## C# models that support the API

The Azure Functions API and the bulk import project share a set of C# model classes. These classes define the request bodies the client sends, such as search text, paging values, and filters. They also define the response shapes the client expects, such as search results, facet values, and a single looked-up document. Keeping these models in one file ensures the search, suggest, and document lookup endpoints stay consistent with the React client's expectations. The following models, defined in `Models.cs`, support the functions in this app:

:::code language="csharp" source="~/azure-search-static-web-app/api/Models.cs" :::

## Next step

To continue learning about Azure AI Search development, try this next tutorial about indexing:

> [!div class="nextstepaction"]
> [Tutorial: Index Azure SQL data using the .NET SDK](search-indexer-tutorial.md)
