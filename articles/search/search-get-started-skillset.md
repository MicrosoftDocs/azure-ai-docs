---
title: "Quickstart: Create a Skillset in the Azure portal"
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
ms.date: 09/16/2025
zone_pivot_groups: azure-portal-wizards
---

# Quickstart: Create a skillset in the Azure portal

::: zone pivot="import-data-new"
[!INCLUDE [Import data (new) instructions](includes/quickstarts/search-get-started-skillset-new-wizard.md)]
::: zone-end

::: zone pivot="import-data"
[!INCLUDE [Import data instructions](includes/quickstarts/search-get-started-skillset-old-wizard.md)]
::: zone-end

## Takeaways

You've created your first skillset and learned the basic steps of skills-based indexing.

Some key concepts that we hope you picked up include the dependencies. A skillset is bound to an indexer, and indexers are Azure and source-specific. Although this quickstart uses Azure Blob Storage, other Azure data sources are available. For more information, see [Indexers in Azure AI Search](search-indexer-overview.md). 

Another important concept is that skills operate over content types, and when you use heterogeneous content, some inputs are skipped. Also, large files or fields might exceed the indexer limits of your service tier. It's normal to see warnings when these events occur. 

The output is routed to a search index, and there's a mapping between name-value pairs created during indexing and individual fields in your index. Internally, the wizard sets up [an enrichment tree](cognitive-search-concept-annotations-syntax.md) and defines a [skillset](cognitive-search-defining-skillset.md), establishing the order of operations and general flow. These steps are hidden in the wizard, but when you start writing code, these concepts become important.

Finally, you learned that you can verify content by querying the index. Ultimately, Azure AI Search provides a searchable index that you can query using either [simple](/rest/api/searchservice/simple-query-syntax-in-azure-search) or [fully extended query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search). An index containing enriched fields is like any other. You can incorporate standard or [custom analyzers](search-analyzers.md), [scoring profiles](/rest/api/searchservice/add-scoring-profiles-to-a-search-index), [synonyms](search-synonyms.md), [faceted navigation](search-faceted-navigation.md), geo-search, and other Azure AI Search features.

## Clean up resources

When you're working in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

You can find and manage resources in the Azure portal by selecting **All resources** or **Resource groups** from the left pane.

If you used a free service, remember that you're limited to three indexes, indexers, and data sources. You can delete individual items in the Azure portal to stay under the limit. 

## Next step

You can use the Azure portal, REST APIs, or an Azure SDK to create skillsets. Try the REST APIs by using a REST client and more sample data:

> [!div class="nextstepaction"]
> [Tutorial: Use skillsets to generate searchable content in Azure AI Search](tutorial-skillset.md)
