---
title: "Quickstart: Create a Demo App in the Azure portal"
titleSuffix: Azure AI Search
description: Run the Create demo app wizard to generate HTML pages and script for an operational web app. The page includes a search box, results area, sidebar, and typeahead support.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 12/05/2025
ms.update-cycle: 180-days
ms.custom:
  - mode-ui
  - ignite-2023
---

# Quickstart: Create a demo search app in the Azure portal

In this quickstart, you use the **Create demo app** wizard in the Azure portal to generate a downloadable, "localhost"-style web app that runs in a browser. Depending on how you configure it, the generated app is operational on first use, with a live read-only connection to an index on your search service. A default app can include a search box, results area, sidebar filters, and typeahead support.

A demo app can help you visualize how an index functions in a client app, but it isn't intended for production scenarios. Production apps should include security, error handling, and hosting logic that the demo app doesn't provide.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. For this quickstart, you can use a free service.

+ A [search index](search-what-is-an-index.md) to use as the basis of your generated application.

  This quickstart uses the hotels-sample index. Follow the instructions in [this quickstart](search-import-data-portal.md) to create the index.

  :::image type="content" source="media/search-create-app-portal/import-data-hotels.png" alt-text="Screenshot of the data source page for sample data.":::

## Start the wizard

To start the wizard for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Search management** > **Indexes**.

1. Select **hotels-sample-index** from the list.

1. At the top of the index page, select **Create demo app**.

1. Select **Enable CORS and continue** to add CORS support to your index definition.

    :::image type="content" source="media/search-create-app-portal/enable-cors.png" alt-text="Screenshot of the enable CORS action.":::

## Configure search results

The wizard provides a basic layout for the rendered search results, including space for a thumbnail image, title, and description. Each element is backed by a field in your index that provides the necessary data.

To configure the search results:

1. Skip **Thumbnail** because the index doesn't have image URLs.

    However, if your index contains a field populated with URLs that resolve to publicly available images, you should specify that field for the thumbnail.

1. For **Title**, choose a field that conveys the uniqueness of each document. Our example uses **HotelName**.

1. For **Description**, choose a field that might help someone decide whether to drill down to that particular document. Our example uses **Description**.

1. Select **Next**.

   :::image type="content" source="media/search-create-app-portal/configure-results.png" lightbox="media/search-create-app-portal/configure-results.png" alt-text="Screenshot of the search results configuration page." :::

## Add a sidebar

The search service supports faceted navigation, which is often rendered as a sidebar. Facets are based on fields attributed as filterable and facetable in your index schema.

> [!TIP]
> To view field attributes, select the **Fields** tab on the index page in the Azure portal. Only fields marked as filterable and facetable can be used in the sidebar.

In Azure AI Search, faceted navigation is a cumulative filtering experience. Within a category, selecting multiple filters expands the results, such as selecting both `Seattle` and `Bellevue` within the `City` filter. Across categories, selecting multiple filters narrows the results.

To customize the sidebar:

1. Review the list of filterable and facetable fields in the index.

1. To shorten the sidebar and prevent scrolling in the finished app, delete some fields.

1. Select **Next**.

   :::image type="content" source="media/search-create-app-portal/customize-sidebar.png" lightbox="media/search-create-app-portal/customize-sidebar.png" alt-text="Screenshot of the sidebar customization page." :::

## Add suggestions

Suggestions are automated query prompts that appear in the search box. The demo app supports suggestions that provide a dropdown list of potential matching documents based on partial text inputs.

To customize the suggestions:

1. Choose the fields you want to display as suggested queries. Use shorter string fields instead of verbose fields, such as descriptions.

1. Use the **Show Field Name** checkbox to include or exclude labels for the suggestions.

    :::image type="content" source="media/search-create-app-portal/suggestions.png" lightbox="media/search-create-app-portal/suggestions.png" alt-text="Screenshot of the suggestion configuration page.":::

## Create, download, and execute

To finish the wizard and use the demo app:

1. Select **Create demo app** to generate the HTML file.

1. When prompted, select **Download** to download the file.

1. Open the file in a browser.

1. Select the search button to run an empty query (`*`) that returns an arbitrary result set.

1. Enter a term in the search box and use the sidebar filters to narrow the results.

    :::image type="content" source="media/search-create-app-portal/run-app.png" lightbox="media/search-create-app-portal/run-app.png" alt-text="Screenshot of the search application in a browser window.":::

    > [!TIP]
    > If you don't see suggested queries, check your browser settings or try a different browser.

## Clean up resources

[!INCLUDE [clean up resources (free)](includes/resource-cleanup-free.md)]

## Next step

The demo app is useful for prototyping because it simulates the end-user experience without requiring JavaScript or front-end code. As you approach the proof-of-concept stage of your own project, review the end-to-end code samples that more closely resemble a real-world app:

> [!div class="nextstepaction"]
> [Add search to web apps](tutorial-csharp-overview.md)
