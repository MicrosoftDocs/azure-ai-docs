---
title: "Tutorial: Add Search to a C# Web App"
description: Learn how to add Azure AI Search to a C# web app, deploy it to Azure Container Apps, and use managed identity for search access.
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

# Tutorial: Add Azure AI Search to a C# web app on Azure Container Apps

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

This tutorial builds a website that searches through a catalog of books and deploys the website to Azure Container Apps. The deployment uses the Azure Developer CLI (`azd`) and managed identity as the default authentication method for Azure AI Search.

In this tutorial, you:

> [!div class="checklist"]
> - Deploy Azure AI Search and auto-seed an index with the Azure Developer CLI.
> - Integrate search queries, suggestions, facets, pagination, and document lookup in the C# app.
> - Deploy the app to Azure Container Apps with managed identity as the default authentication method.

## What does the sample do?

This sample website provides access to a catalog of 10,000 books. You can search the catalog by entering text in the search bar. While you enter text, the website uses the search index's suggestion feature to autocomplete the text.

When the query finishes, the website displays the list of books with a portion of their details. You can select a book to see its complete details, which are stored in the search index.

:::image type="content" source="media/tutorial-csharp-overview/cognitive-search-enabled-book-website-2.png" alt-text="Screenshot of the sample app in a browser window.":::

The search experience includes:

- [Search](search-query-create.md) - Provides search functionality for the application.
- [Suggest](search-add-autocomplete-suggestions.md) - Provides suggestions as the user types in the search bar.
- [Facets and filters](search-faceted-navigation.md) - Provides a faceted navigation structure that filters by author or language.
- [Paginated results](search-pagination-page-layout.md) - Provides paging controls for scrolling through results.
- [Document lookup](search-query-overview.md#document-look-up) - Looks up a document by ID to retrieve all of its contents for the details page.

## How is the sample organized?

The [sample code](https://github.com/Azure-Samples/azure-search-static-web-app) includes the following components:

| App | Purpose | GitHub repository location |
|--|--|--|
| `client` | React app (presentation layer) to display books with search. It calls the API. | [/azure-search-static-web-app/client](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/client) |
| `api` | C# Azure Functions API (business layer), hosted in a container on Azure Container Apps, that calls the Azure AI Search API with the .NET SDK. | [/azure-search-static-web-app/api](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/api) |
| `bulk-insert` | .NET project that creates the index and loads documents. The `azd` deployment runs this automatically through the `postprovision` hook. | [/azure-search-static-web-app/bulk-insert](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/bulk-insert) |
| `infra` | Bicep infrastructure used by `azd` to deploy Azure AI Search, Azure Container Apps, and supporting resources. | [Azure-Samples/azure-search-static-web-app](https://github.com/Azure-Samples/azure-search-static-web-app) |

## Set up your development environment

Install the following software for your local development environment. The `azd up` command provisions all Azure resources, including Azure AI Search, so you don't need to create them beforehand.

- [.NET 9](https://dotnet.microsoft.com/download/dotnet) or later
- [Git](https://git-scm.com/downloads)
- [Visual Studio Code](https://code.visualstudio.com/)
- [C# Dev Tools extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or another Docker-compatible container runtime

This tutorial doesn't run the Azure Functions API locally. If you want to run it locally, install [Azure Functions Core Tools](/azure/azure-functions/functions-run-local?tabs=linux%2ccsharp%2cbash#install-the-azure-functions-core-tools).

## Clone the search sample with Git

You can deploy the sample from a local clone. The `azd up` command reads the application and infrastructure files from your local repository, builds the containers, provisions Azure resources, and deploys the client and API to Azure Container Apps.

1. In a Bash terminal, clone the sample application to your local computer.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-static-web-app.git
    ```

1. In the same Bash terminal, go to the repository directory for this search example.

    ```bash
    cd azure-search-static-web-app
    ```

1. Use the Visual Studio Code command, `code .`, to open the repository. Unless otherwise specified, you complete the remaining tasks in Visual Studio Code.

    ```bash
    code .
    ```

## Next step

> [!div class="nextstepaction"]
> [Deploy the app to Azure Container Apps](tutorial-csharp-deploy-web-search.md)
