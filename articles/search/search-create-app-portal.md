---
title: Create a Demo App in the Azure Portal
titleSuffix: Azure AI Search
description: Run the Create demo app wizard to generate HTML pages and script for a local web app. The page includes a search box, results area, sidebar, and typeahead support.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 03/05/2026
ms.update-cycle: 180-days
ms.custom:
  - mode-ui
  - ignite-2023
---

# Create a demo search app in the Azure portal

Use the **Create demo app** wizard in the Azure portal to generate a downloadable, "localhost"-style web app that runs in a browser. Depending on how you configure it, the generated app is operational on first use, with a live read-only connection to an index on your search service. A default app can include a search box, results area, sidebar filters, and typeahead support.

A demo app can help you visualize how an index functions in a client app, but it isn't intended for production scenarios. Production apps should include security, error handling, and hosting logic that the demo app doesn't provide.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. For this example, you can use a free service.

+ A [search index](search-what-is-an-index.md) to use as the basis of your generated application. We use the [hotels-sample index](search-get-started-portal.md) to illustrate the demo app.

## Start the wizard

The **Create demo app** wizard is available for existing indexes. Choose an index that includes retrievable, filterable, and facetable fields.

To start the wizard:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. From the left pane, select **Search management** > **Indexes**.

1. Select **hotels-sample** from the list.

1. At the top of the index page, select **Create demo app**.

1. Select **Enable CORS and continue** to add CORS support to your index definition.

    :::image type="content" source="media/search-create-app-portal/enable-cors-continue.png" alt-text="Screenshot of the button for enabling CORS and continuing." lightbox="media/search-create-app-portal/enable-cors-continue.png":::

## Configure search results

You can configure a basic layout for the rendered search results, including space for a thumbnail image, title, and description. Each element is backed by a field in your index that provides the necessary data.

To configure the search results:

1. Skip **Thumbnail** because the hotels-sample index doesn't have image URLs. If your index contains a field populated with URLs that resolve to publicly available images, you should specify that field for the thumbnail.

1. For **Title**, choose a field that conveys the uniqueness of each document. Our example uses **HotelName**.

1. For **Description**, choose a field that might help someone decide whether to drill down to that particular document. Our example uses **Description**.

1. Select **Next**.

    :::image type="content" source="media/search-create-app-portal/customize-results.png" alt-text="Screenshot of the page for customizing individual results." lightbox="media/search-create-app-portal/customize-results.png":::

## Add a sidebar

The search service supports filters and faceted navigation, which is often rendered as a sidebar. Facets are based on fields attributed as filterable and facetable in your index schema.

> [!TIP]
> To view field attributes, select the **Fields** tab on the index page in the Azure portal. Only fields marked as filterable can be used in the sidebar.

Filters can be cumulative or subtractive. For multiple filters of the same field, such as multiple cities, expand search results to include all cities. Across fields, multiple filters add more criteria that must be met by each document, narrowing the results.

To customize the sidebar:

1. Review the list of filterable and facetable fields in the index.

1. To shorten the sidebar and prevent scrolling in the finished app, delete some fields.

1. Select **Next**.

    :::image type="content" source="media/search-create-app-portal/customize-sidebar.png" alt-text="Screenshot of the page for customizing the sidebar." lightbox="media/search-create-app-portal/customize-sidebar.png":::

## Add suggestions

[Suggestions](search-add-autocomplete-suggestions.md) are automated query prompts that appear in the search box. The demo app supports suggestions that provide a dropdown list of potential matching documents based on partial text inputs.

To customize the suggestions:

1. Choose the fields you want to display as suggested queries. Use shorter string fields instead of verbose fields, such as descriptions.

1. Use the **Show Field Name** checkbox to include or exclude labels for the suggestions.

    :::image type="content" source="media/search-create-app-portal/add-suggestions.png" lightbox="media/search-create-app-portal/add-suggestions.png" alt-text="Screenshot of the page for adding suggestions.":::

## Create, download, and execute

To finish the wizard and use the demo app:

1. Select **Create demo app** to generate the HTML file.

1. When prompted, select **Download** to download the file.

1. Open the file in a browser.

1. Select the search button to run an empty query (`*`) that returns an arbitrary result set.

1. Enter a term in the search box and use the sidebar filters to narrow the results. Select filters to narrow results.

    :::image type="content" source="media/search-create-app-portal/app.png" lightbox="media/search-create-app-portal/app.png" alt-text="Screenshot of the search application in a browser window.":::

1. Test suggestions by typing in part of a search term. If you don't see suggested results, check your browser settings or try a different browser. Notice that suggested results are different from autocompletion of a search term. The demo app supports suggested results only.

   :::image type="content" source="media/search-create-app-portal/app-suggestions.png" alt-text="Screenshot of suggested results." lightbox="media/search-create-app-portal/app-suggestions.png":::

## Clean up resources

[!INCLUDE [clean up resources (free)](includes/resource-cleanup-free.md)]

## Next step

The demo app is useful for prototyping because it simulates the end-user experience without requiring JavaScript or front-end code. As you approach the proof-of-concept stage of your own project, review the end-to-end code samples that more closely resemble a real-world app:

> [!div class="nextstepaction"]
> [Add search to web apps](tutorial-csharp-overview.md)
