---
title: "Quickstart: Create a Skillset in the Azure Portal"
titleSuffix: Azure AI Search
description: Learn how to use an import wizard to generate searchable text from images and unstructured documents. Skills in this quickstart include optical character recognition (OCR), image analysis, and natural-language processing.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 03/04/2025
zone_pivot_groups: search-get-started-skillset
---

# Quickstart: Create a skillset in the Azure portal

::: zone pivot="import-and-vectorize-data"
[!INCLUDE [Import and vectorize data instructions](includes/quickstarts/search-get-started-skillset-import-vectorize.md)]
::: zone-end

::: zone pivot="import-data"
[!INCLUDE [Import data instructions](includes/quickstarts/search-get-started-skillset-import.md)]
::: zone-end

## Monitor status

You can monitor the creation of the indexer in the Azure portal. Skills-based indexing takes longer than text-based indexing, especially OCR and image analysis.

To monitor the progress of the indexer:

1. From the left pane, select **Indexers**.

1. Select your indexer from the list.

1. Select **Success** (or **Failed**) to view execution details.

   :::image type="content" source="media/search-get-started-skillset/indexer-notification.png" alt-text="Screenshot of the indexer status page." border="true" lightbox="media/search-get-started-skillset/indexer-notification.png":::

In this quickstart, there are a few warnings, including `Could not execute skill because one or more skill input was invalid.` This warning tells you that a PNG file in the data source doesn't provide a text input to Entity Recognition. It occurs because the upstream OCR skill didn't recognize any text in the image and couldn't provide a text input to the downstream Entity Recognition skill.

Warnings are common in skillset execution. As you become familiar with how skills iterate over your data, you might begin to notice patterns and learn which warnings are safe to ignore.

## Query in Search explorer

Now that your index is created, use **Search explorer** to send queries and return results.

To query your index:

1. From the left pane, select **Indexes**.

1. Select your index from the list. If the index has zero documents or storage, wait for the Azure portal to refresh.

   :::image type="content" source="media/search-get-started-portal/indexes-list.png" alt-text="Screenshot of the Indexes list on the Azure AI Search service dashboard in the Azure portal." lightbox="media/search-get-started-portal/indexes-list.png":::

1. On the **Search explorer** tab, enter a search string, such as `satya nadella`.

    The search bar accepts keywords, quote-enclosed phrases, and operators. For example: `"Satya Nadella" +"Bill Gates" +"Steve Ballmer"`

Results are returned as verbose JSON, which can be hard to read, especially in large documents. Here are tips for searching in this tool:

+ Switch to the JSON view to specify parameters that shape results.
+ Add `select` to limit the fields in results.
+ Add `count` to show the number of matches.
+ Use CTRL-F to search within the JSON for specific properties or terms.

:::image type="content" source="media/search-get-started-skillset/search-explorer.png" alt-text="Screenshot of the Search explorer page." border="true" lightbox="media/search-get-started-skillset/search-explorer.png":::

Here's some JSON you can paste into the view:

  ```json
  {
  "search": "\"Satya Nadella\" +\"Bill Gates\" +\"Steve Ballmer\"",
  "count": true,
  "select": "content, people"
  }
  ```

> [!TIP]
> Query strings are case-sensitive, so if you get an "unknown field" message, check **Fields** or **Index Definition (JSON)** to verify the name and case.

## Takeaways

You've created your first skillset and learned the basic steps of skills-based indexing.

Some key concepts that we hope you picked up include the dependencies. A skillset is bound to an indexer, and indexers are Azure and source-specific. Although this quickstart uses Azure Blob Storage, other Azure data sources are available. For more information, see [Indexers in Azure AI Search](search-indexer-overview.md). 

Another important concept is that skills operate over content types, and when you use heterogeneous content, some inputs are skipped. Also, large files or fields might exceed the indexer limits of your service tier. It's normal to see warnings when these events occur. 

The output is routed to a search index, and there's a mapping between name-value pairs created during indexing and individual fields in your index. Internally, the wizard sets up [an enrichment tree](cognitive-search-concept-annotations-syntax.md) and defines a [skillset](cognitive-search-defining-skillset.md), establishing the order of operations and general flow. These steps are hidden in the wizard, but when you start writing code, these concepts become important.

Finally, you learned that you can verify content by querying the index. Ultimiately, Azure AI Search provides a searchable index that you can query using either [simple](/rest/api/searchservice/simple-query-syntax-in-azure-search) or [fully extended query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search). An index containing enriched fields is like any other. You can incorporate standard or [custom analyzers](search-analyzers.md), [scoring profiles](/rest/api/searchservice/add-scoring-profiles-to-a-search-index), [synonyms](search-synonyms.md), [faceted navigation](search-faceted-navigation.md), geo-search, and other Azure AI Search features.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by selecting **All resources** or **Resource groups** from the left pane.

If you used a free service, remember that you're limited to three indexes, indexers, and data sources. You can delete individual items in the Azure portal to stay under the limit. 

## Next step

You can use the Azure portal, REST APIs, or an Azure SDK to create skillsets. Try the REST APIs by using a REST client and more sample data:

> [!div class="nextstepaction"]
> [Tutorial: Use skillsets to generate searchable content in Azure AI Search](tutorial-skillset.md)
