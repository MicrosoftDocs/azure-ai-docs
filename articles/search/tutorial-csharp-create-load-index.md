---
title: Load an Index (.NET Tutorial)
description: Create index and import CSV data into Search index with .NET.
ms.reviewer: diberry
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 07/24/2026
ai-usage: ai-assisted
ms.custom:
  - devx-track-csharp
  - devx-track-azurecli
  - devx-track-dotnet
  - devx-track-azurepowershell
  - ignite-2023
ms.devlang: csharp
---

# Step 2 - Create and load the search index

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Continue to build your search-enabled website for Azure Container Apps by following these steps:

- Create a new index.
- Load data.

The program uses [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/) in the Azure SDK for .NET:

- [NuGet package Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents/).
- [Reference documentation](/dotnet/api/overview/azure/search).

Before you start, make sure you have room on your search service for a new index. The free tier limit is three indexes. The Basic tier limit is 15.

## Prepare the bulk import script for Search

The bulk import project reads its configuration from environment variables. Managed identity is the default credential path. If `SEARCH_API_KEY` is empty, the code uses `DefaultAzureCredential` for Azure AI Search. Use an API key only as an explicit fallback.

1. In Visual Studio Code, open an integrated terminal for the `azure-search-static-web-app/bulk-insert` directory.

1. Set the search service name. Replace `YOUR-SEARCH-SERVICE-NAME` with the name of your search service, not the full URL.

    ```bash
    export SEARCH_SERVICE_NAME="YOUR-SEARCH-SERVICE-NAME"
    ```

1. If you need key authentication, set `SEARCH_API_KEY` to an admin key for your search service. To find keys, see [Find API keys](search-security-api-keys.md#find-existing-keys).

    ```bash
    export SEARCH_API_KEY="YOUR-SEARCH-ADMIN-API-KEY"
    ```

    If you use managed identity or another credential supported by `DefaultAzureCredential`, omit `SEARCH_API_KEY`. Make sure your signed-in identity has access to create and load the search index.

1. Review the current `Program.cs` configuration. It uses `SEARCH_SERVICE_NAME`, optional `SEARCH_API_KEY`, and `SEARCH_INDEX_NAME`, which defaults to `good-books`.

    :::code language="csharp" source="~/azure-search-static-web-app/bulk-insert/Program.cs" :::

1. Run the following command to install the dependencies.

    ```bash
    dotnet restore
    ```

## Run the bulk import script for Search

1. Still in the same subdirectory (`azure-search-static-web-app/bulk-insert`), run the program:

    ```bash
    dotnet run
    ```

1. As the code runs, the console displays progress. You should see the following output.

   ```bash
    Creating (or updating) search index
    Status: 201, Value: Azure.Search.Documents.Indexes.Models.SearchIndex
    Download data file
    Reading and parsing raw CSV data
    Uploading bulk book data
    Finished bulk inserting book data
    ```

## Review the new search index

Once the upload completes, the search index is ready to use. Review your new index in Azure portal.

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. On the left, select **Search Management > Indexes**, and then select the `good-books` index.

    :::image type="content" source="media/tutorial-csharp-create-load-index/azure-portal-indexes-page.png" lightbox="media/tutorial-csharp-create-load-index/azure-portal-indexes-page.png" alt-text="Expandable screenshot of Azure portal showing the index." border="true":::

1. By default, the index opens in the **Search Explorer** tab. Select **Search** to return documents from the index.

    :::image type="content" source="media/tutorial-csharp-create-load-index/azure-portal-search-explorer.png" lightbox="media/tutorial-csharp-create-load-index/azure-portal-search-explorer.png" alt-text="Expandable screenshot of Azure portal showing search results." border="true":::

## Clear local environment variables

If you set `SEARCH_API_KEY` in your terminal, clear it after the import finishes. Don't save or commit API keys to your repository.

```bash
unset SEARCH_API_KEY
```

## Next steps

[Deploy the app to Azure Container Apps](tutorial-csharp-deploy-static-web-app.md)
