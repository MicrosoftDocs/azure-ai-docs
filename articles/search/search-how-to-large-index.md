---
title: Index large data sets for full text search
titleSuffix: Azure AI Search
description: Learn about strategies for large data indexing or computationally intensive indexing through batch mode, resourcing, and scheduled, parallel, and distributed indexing.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 10/06/2025
ms.update-cycle: 180-days
---

# Index large data sets in Azure AI Search

If you need to index large or complex data sets in your search solution, this article explores strategies to accommodate long-running processes on Azure AI Search.

These strategies assume familiarity with the [two basic approaches for importing data](search-what-is-data-import.md): *pushing* data into an index, or *pulling* in data from a supported data source using a [search indexer](search-indexer-overview.md). If your scenario involves computationally intensive [AI enrichment](cognitive-search-concept-intro.md), then indexers are required, given the skillset dependency on indexers.

This article complements [Tips for better performance](search-performance-tips.md), which offers best practices on index and query design. A well-designed index that includes only the fields and attributes you need is an important prerequisite for large-scale indexing.

We recommend using a search service created after April 3, 2024 for [higher storage per partition](search-limits-quotas-capacity.md#service-limits). Older services can also be [upgraded to benefit from higher partition storage](search-how-to-upgrade.md).

> [!NOTE]
> The strategies described in this article assume a single large data source. If your solution requires indexing from multiple data sources, see [Index multiple data sources in Azure AI Search](/samples/azure-samples/azure-search-dotnet-scale/multiple-data-sources/) for a recommended approach.

## Index data using the push APIs

*Push* APIs, such as the [Documents Index REST API](/rest/api/searchservice/documents) or the [IndexDocuments method (Azure SDK for .NET)](/dotnet/api/azure.search.documents.searchclient.indexdocuments), are the most prevalent form of indexing in Azure AI Search. For solutions that use a push API, the strategy for long-running indexing has one or both of the following components:

+ Batching documents
+ Managing threads

### Batch multiple documents per request

A simple mechanism for indexing a large quantity of data is to submit multiple documents or records in a single request. As long as the entire payload is under 16 MB, a request can handle up to 1,000 documents in a bulk upload operation. These limits apply whether you're using the [Documents Index REST API](/rest/api/searchservice/documents) or the [IndexDocuments method](/dotnet/api/azure.search.documents.searchclient.indexdocuments) in the .NET SDK. Using either API, you can package 1,000 documents in the body of each request.

Batching documents significantly shortens the amount of time it takes to work through a large data volume. Determining the optimal batch size for your data is a key component of optimizing indexing speeds. The two primary factors influencing the optimal batch size are:

+ The schema of your index
+ The size of your data

Because the optimal batch size depends on your index and your data, the best approach is to test different batch sizes to determine which one results in the fastest indexing speeds for your scenario. For sample code to test batch sizes using the .NET SDK, see [Tutorial: Optimize indexing with the push API](tutorial-optimize-indexing-push-api.md).

### Manage threads and a retry strategy

Indexers have built-in thread management, but when you're using the push APIs, your application code needs to manage threads. Make sure there are sufficient threads to make full use of the available capacity, especially if you recently [upgraded your service](search-how-to-upgrade.md), [switched to a higher pricing tier](search-capacity-planning.md#change-your-pricing-tier), or [increased partitions](search-capacity-planning.md#add-or-remove-partitions-and-replicas).

1. [Increase the number of concurrent threads](tutorial-optimize-indexing-push-api.md#use-multiple-threadsworkers) in your client code.

1. As you ramp up the requests hitting the search service, you might encounter [HTTP status codes](/rest/api/searchservice/http-status-codes) indicating the request didn't fully succeed. During indexing, two common HTTP status codes are:

   + **503 Service Unavailable**: This error means that the system is under heavy load and your request can't be processed at this time.

   + **207 Multi-Status**: This error means that some documents succeeded, but at least one failed.

1. To handle failures, requests should be retried using an [exponential backoff retry strategy](/dotnet/architecture/microservices/implement-resilient-applications/implement-retries-exponential-backoff).

The Azure .NET SDK automatically retries 503s and other failed requests, but you need to implement your own logic to retry 207s. Open-source tools such as [Polly](https://github.com/App-vNext/Polly) can also be used to implement a retry strategy.

## Use indexers and the pull APIs

[Indexers](search-indexer-overview.md) have several capabilities that are useful for long-running processes:

+ Batching documents
+ Parallel indexing over partitioned data
+ Scheduling and change detection for indexing only new and changed documents over time

Indexer schedules can resume processing at the last known stopping point. If data isn't fully indexed within the processing window, the indexer picks up wherever it left off on the next run, assuming you're using a data source that provides change detection.

Partitioning data into smaller individual data sources enables parallel processing. You can break up source data, such as into multiple containers in Azure Blob Storage, [create a data source](/rest/api/searchservice/data-sources/create) for each partition, and then [run the indexers in parallel](search-howto-run-reset-indexers.md), subject to the number of search units of your search service.

### Check indexer batch size

As with the push API, indexers allow you to configure the number of items per batch. For indexers based on the [Create Indexer REST API](/rest/api/searchservice/indexers/create), you can set the `batchSize` argument to customize this setting to better match the characteristics of your data. 

Default batch sizes are data-source specific. Azure SQL Database and Azure Cosmos DB have a default batch size of 1,000. In contrast, Azure Blob and SharePoint (Preview) indexing sets batch size at 10 documents in recognition of the larger average document size. 

### Schedule indexers for long-running processes

Indexer scheduling is an important mechanism for processing large data sets and for accommodating slow-running processes like image analysis in an enrichment pipeline. 

Typically, indexer processing runs within a two-hour window. If the indexing workload takes days rather than hours to complete, you can put the indexer on a consecutive, recurring schedule that starts every two hours. Assuming the data source has [change tracking enabled](search-howto-create-indexers.md#change-detection-and-internal-state), the indexer resumes processing where it last left off. At this cadence, an indexer can work its way through a document backlog over a series of days until all unprocessed documents are processed. This pattern is especially important during the initial run or when indexing large blob containers, where the blob listing phase alone can take multiple hours or days. During this time, the indexer would show no blobs being processed, but unless an error is reported, it is likely still iterating through the blob list. Document processing and enrichment begin only after this phase completes, and this behavior is expected.


```json
{
    "dataSourceName" : "hotels-ds",
    "targetIndexName" : "hotels-idx",
    "schedule" : { "interval" : "PT2H", "startTime" : "2024-01-01T00:00:00Z" }
}
```

When there are no longer any new or updated documents in the data source, indexer execution history reports `0/0` documents processed, and no processing occurs.

For more information about setting schedules, see [Create Indexer REST API](/rest/api/searchservice/indexers/create) or see [Schedule indexers for Azure AI Search](search-howto-schedule-indexers.md).

> [!NOTE]
> Some indexers that run on an older runtime architecture have a 24-hour rather than 2-hour maximum processing window. The two-hour limit is for newer content processors that run in an [internally managed multitenant environment](search-howto-run-reset-indexers.md#indexer-execution-environment). Whenever possible, Azure AI Search tries to offload indexer and skillset processing to the multitenant environment. If the indexer can't be migrated, it runs in the private environment and it can run for as long as 24 hours. If you're scheduling an indexer that exhibits these characteristics, assume a 24-hour processing window.

<a name="parallel-indexing"></a>

### Run indexers in parallel

If you partition your data, you can create multiple indexer-data-source combinations that pull from each data source and write to the same search index. Because each indexer is distinct, you can run them at the same time, populating a search index more quickly than if you ran them sequentially. 

Make sure you have sufficient capacity. One search unit in your service can run one indexer at any given time. Creating multiple indexers is only useful if they can run in parallel.

The number of indexing jobs that can run simultaneously varies for text-based and skills-based indexing. For more information, see [Indexer execution](search-howto-run-reset-indexers.md#indexer-execution).

If your data source is an [Azure Blob Storage container](/azure/storage/blobs/storage-blobs-introduction#containers) or [Azure Data Lake Storage Gen 2](/azure/storage/blobs/storage-blobs-introduction#about-azure-data-lake-storage-gen2), enumerating a large number of blobs can take a long time (even hours) until this operation is completed. As a result, your indexer's *documents succeeded* count doesn't appear to increase during that time and it might seem it's not making any progress, when it is. If you would like document processing to go faster for a large number of blobs, consider partitioning your data into multiple containers and create parallel indexers pointing to a single index.

1. Sign in to the [Azure portal](https://portal.azure.com) and check the number of search units used by your search service. Select **Settings** > **Scale** to view the number at the top of the page. The number of indexers that run in parallel is approximately equal to the number of search units. 

1. Partition source data among multiple containers or multiple virtual folders inside the same container.

1. Create multiple [data sources](/rest/api/searchservice/data-sources/create), one for each partition, paired to its own [indexer](/rest/api/searchservice/indexers/create).

1. Specify the same target search index in each indexer.

1. Schedule the indexers.

1. Review indexer status and execution history for confirmation.

There are some risks associated with parallel indexing. First, recall that indexing doesn't run in the background, increasing the likelihood that queries are throttled or dropped. 

Second, Azure AI Search doesn't lock the index for updates. Concurrent writes are managed, invoking a retry if a particular write doesn't succeed on first attempt, but you might notice an increase in indexing failures.

Although multiple indexer-data-source sets can target the same index, be careful of indexer runs that can overwrite existing values in the index. If a second indexer-data-source targets the same documents and fields, any values from the first run are overwritten. Field values are replaced in full; an indexer can't merge values from multiple runs into the same field.

## Index big data on Spark

If you have a big data architecture and your data is on a Spark cluster, we recommend [SynapseML for loading and indexing data](search-synapseml-cognitive-services.md). The tutorial includes steps for calling Foundry Tools for AI enrichment, but you can also use the AzureSearchWriter API for text indexing.

## Related content

+ [Tutorial: Optimize indexing by using the push API](tutorial-optimize-indexing-push-api.md)
+ [Tutorial: Index large data from Apache Spark using SynapseML and Azure AI Search](search-synapseml-cognitive-services.md)
+ [Tips for better performance in Azure AI Search](search-performance-tips.md)
+ [Analyze performance in Azure AI Search](search-performance-analysis.md)
+ [Indexers in Azure AI Search](search-indexer-overview.md)
+ [Monitor indexer status and results in Azure AI Search](search-monitor-indexers.md)
