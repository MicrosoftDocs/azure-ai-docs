---
title: Add search to web apps with .NET
description: Add search to a .NET website and deploy it to Azure Container Apps with Azure Developer CLI and managed identity.
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

# Step 1 - Overview of adding search to a Container Apps web app with .NET

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

This tutorial builds a website that searches through a catalog of books and deploys the website to Azure Container Apps. The deployment uses the Azure Developer CLI (`azd`) and managed identity as the default authentication method for Azure AI Search.

## What does the sample do?

This sample website provides access to a catalog of 10,000 books. You can search the catalog by entering text in the search bar. While you enter text, the website uses the search index's suggestion feature to autocomplete the text.

When the query finishes, the website displays the list of books with a portion of the details. You can select a book to see all the details, stored in the search index, for the book.

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
| `client` | React app (presentation layer) to display books with search. It calls the Azure Function app. | [/azure-search-static-web-app/client](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/client) |
| `api` | Azure .NET Function app (business layer) that calls the Azure AI Search API with the .NET SDK. | [/azure-search-static-web-app/api](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/api) |
| `bulk-insert` | .NET project to create the index and add documents to it. | [/azure-search-static-web-app/bulk-insert](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/bulk-insert) |
| `infra` | Bicep infrastructure used by `azd` to deploy Azure AI Search, Azure Container Apps, and supporting resources. | [/azure-search-static-web-app/infra](https://github.com/Azure-Samples/azure-search-static-web-app/tree/main/infra) |

## Set up your development environment

Create services and install the following software for your local development environment.

- [Azure AI Search](search-create-service-portal.md), any region or tier.
- [.NET 9](https://dotnet.microsoft.com/download/dotnet) or later.
- [Git](https://git-scm.com/downloads).
- [Visual Studio Code](https://code.visualstudio.com/).
- [C# Dev Tools extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit).
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`).
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or another Docker-compatible container runtime.

This tutorial doesn't run the Azure Function API locally. If you want to run it locally, install [Azure Functions Core Tools](/azure/azure-functions/functions-run-local?tabs=linux%2ccsharp%2cbash#install-the-azure-functions-core-tools).

## Clone the search sample with git

You can deploy the sample from a local clone. The `azd up` command reads the application and infrastructure files from your local repository, builds the containers, provisions Azure resources, and deploys the client and API to Azure Container Apps.

1. At a Bash terminal, clone the sample application to your local computer.

    ```bash
    git clone https://github.com/Azure-Samples/azure-search-static-web-app.git
    ```

1. At the same Bash terminal, go into the repository for this website search example:

    ```bash
    cd azure-search-static-web-app
    ```

1. Use the Visual Studio Code command, `code .`, to open the repository. You accomplish the remaining tasks from Visual Studio Code, unless specified.

    ```bash
    code .
    ```

## Next steps

- [Create an index and load it with documents](tutorial-csharp-create-load-index.md)
- [Deploy the app to Azure Container Apps](tutorial-csharp-deploy-static-web-app.md)
