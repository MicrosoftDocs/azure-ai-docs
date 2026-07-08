---
title: Tips for AI Enrichment Design
description: Tips and troubleshooting for setting up AI enrichment pipelines in Azure AI Search.
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: best-practice
ms.date: 07/07/2026
ms.update-cycle: 365-days
---

# Tips for AI enrichment in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

This article provides tips to help you get started with AI enrichment and skillsets used during indexing.

## Tip 1: Start simple and start small

The [**Import data** wizard](search-get-started-skillset.md) in the Azure portal supports AI enrichment. Without writing any code, you can create and examine all of the objects used in an enrichment pipeline: an index, indexer, data source, and skillset.

Another way to start simply is by creating a data source with just a handful of documents or rows in a table that are representative of the documents you want to index. A small data set is the best way to increase the speed of finding and fixing problems. Run your sample through the end-to-end pipeline and check that the results meet your needs. When you're satisfied with the results, you're ready to add more files to your data source.

## Tip 2: See what works even if there are some failures

Sometimes a small failure stops an indexer in its tracks. That condition is fine if you plan to fix problems one by one. However, you might want to ignore a particular type of error, so the indexer can continue and you can see what flows are actually working.

To ignore errors during development, set `maxFailedItems` and `maxFailedItemsPerBatch` to -1 as part of the indexer definition.

```json
{
  // rest of your indexer definition
   "parameters":
   {
      "maxFailedItems":-1,
      "maxFailedItemsPerBatch":-1
   }
}
```

> [!NOTE]
> As a best practice, set the `maxFailedItems` and `maxFailedItemsPerBatch` to 0 for production workloads.

## Tip 3: Use Debug session to troubleshoot problems

[**Debug session**](./cognitive-search-debug-session.md) is a visual editor that shows a skillset's dependency graph, inputs and outputs, and definitions. It works by loading a single document from your search index, with the current indexer and skillset configuration. You can then run the entire skillset, scoped to a single document. Within a debug session, you can identify and resolve errors, validate changes, and commit changes to a parent skillset. For a walkthrough, see [Tutorial: debug sessions](./cognitive-search-tutorial-debug-sessions.md).

## Tip 4: Expected content doesn't appear

If content is missing, check for dropped documents in the Azure portal. In the search service page, open **Indexers** and look at the **Docs succeeded** column. Select it to view indexer execution history and review specific errors. 

If the problem is related to file size, you might see an error like this: "The blob \<file-name>" has the size of \<file-size> bytes, which exceeds the maximum size for document extraction for your current service tier." For more information on indexer limits, see [Service limits](search-limits-quotas-capacity.md).

A second reason for content failing to appear might be related to input/output mapping errors. For example, an output target name is "People" but the index field name is lower-case "people". The system returns 201 success messages for the entire pipeline so you think indexing succeeded, when in fact a field is empty. 

## Tip 5: Extend processing beyond maximum run time

Image analysis is computationally intensive for even simple cases, so when images are especially large or complex, processing times can exceed the maximum time allowed.

For indexers that have skillsets, skillset execution is [capped at 2 hours for most tiers](search-limits-quotas-capacity.md#indexer-limits). If skillset processing fails to complete within that period, you can put your indexer on a 2-hour recurring schedule to have the indexer pick up processing where it left off. 

Scheduled indexing resumes at the last known good document. On a recurring schedule, the indexer can work its way through the image backlog over a series of hours or days, until all unprocessed images are processed. For more information on schedule syntax, see [Schedule an indexer](search-howto-schedule-indexers.md).

> [!NOTE]
> If a scheduled indexer repeatedly fails on the same document, the service reduces its run frequency (up to once every 24 hours) until it makes progress. After fixing the underlying issue, run the indexer on demand. If it makes progress, the indexer returns to its configured interval. If the indexer doesn't return to its configured schedule after a successful run, see [Scheduling behavior FAQ](search-howto-schedule-indexers.md#scheduling-behavior-faq).

## Tip 6: Increase indexing throughput

For [parallel indexing](search-howto-large-index.md), distribute your data into multiple containers or multiple virtual folders inside the same container. Then create multiple data source and indexer pairs. All indexers can use the same skillset and write into the same target search index, so your search app doesn’t need to be aware of this partitioning.

## See also

+ [Quickstart: Create an AI enrichment pipeline in the Azure portal](search-get-started-skillset.md)
+ [Tutorial: Learn AI enrichment REST APIs](tutorial-skillset.md)
+ [How to configure blob indexers](search-how-to-index-azure-blob-storage.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [How to map enriched fields to an index](cognitive-search-output-field-mapping.md)
