---
title: Schedule indexer execution
titleSuffix: Azure AI Search
description: Learn how to schedule Azure AI Search indexers to index content at specific intervals, or at specific dates and times.
author: HeidiSteen
manager: nitinme
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 09/24/2025
ms.update-cycle: 365-days
---

# Schedule an indexer in Azure AI Search

Indexers can be configured to run on a schedule when you set the `schedule` property. Some situations where indexer scheduling is useful include:

+ Source data is changing over time, and you want the indexer to automatically process the difference.
+ Source data is very large, and you need a recurring schedule to index all of the content.
+ An index is populated from multiple sources, using multiple indexers, and you want to stagger the jobs to reduce conflicts.

When indexing can't complete within the [typical 2-hour processing window](search-howto-run-reset-indexers.md#indexer-execution), you can schedule the indexer to run on a 2-hour cadence to work through a large volume of data. As long as your data source supports [change detection logic](search-howto-create-indexers.md#change-detection-and-internal-state), indexers can automatically pick up where they left off on each run.

Once an indexer is on a schedule, it remains on the schedule until you clear the interval or start time, or set `disabled` to true. Leaving the indexer on a schedule when there's nothing to process won't impact system performance. Checking for changed content is a relatively fast operation.

## Prerequisites

+ A valid indexer configured with a data source and index.

+ [Change detection](search-howto-create-indexers.md#change-detection-and-internal-state) in the data source. Azure Storage and SharePoint have built-in change detection. Other data sources, such as [Azure SQL](search-how-to-index-sql-database.md) and [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md) must be enabled manually.

## Schedule definition

A schedule is part of the indexer definition. If the `schedule` property is omitted, the indexer will only run on demand. The property has two parts.

| Property | Description |
|----------|-------------|
| "interval" | (required) The amount of time between the start of two consecutive indexer executions. The smallest interval allowed is 5 minutes, and the longest is 1440 minutes (24 hours). It must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value). </br></br>The pattern for this is: `P(nD)(T(nH)(nM))`. </br></br>Examples: `PT15M` for every 15 minutes, `PT2H` for every two hours.|
| "startTime" | (optional) Start time is specified in coordinated universal time (UTC). If omitted, the current time is used. This time can be in the past, in which case the first execution is scheduled as if the indexer has been running continuously since the original start time.|

The following example is a schedule that starts on January 1 at midnight and runs every two hours.

```json
{
    "dataSourceName" : "hotels-ds",
    "targetIndexName" : "hotels-idx",
    "schedule" : { "interval" : "PT2H", "startTime" : "2024-01-01T00:00:00Z" }
}
```

## Configure a schedule

Schedules are specified in an indexer definition. To set up a schedule, you can use Azure portal, REST APIs, or an Azure SDK.

### [**Azure portal**](#tab/portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and open the search service page.
1. On the left pane, select **Indexers**.
1. Open an indexer.
1. Select **Settings**.
1. Scroll down to **Schedule**, and then choose Hourly, Daily, or Custom to set a specific date, time, or custom interval.

Switch to the **Indexer Definition (JSON)** tab at the top of the index to view the schedule definition in XSD format.

### [**REST**](#tab/rest)

1. Call [Create Indexer](/rest/api/searchservice/indexers/create) or [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update).

1. Set the schedule property in the body of the request:

    ```http
    PUT /indexers/<indexer-name>?api-version=2025-09-01
    {
        "dataSourceName" : "myazuresqldatasource",
        "targetIndexName" : "my-target-index-name",
        "schedule" : { "interval" : "PT10M", "startTime" : "2024-01-01T00:00:00Z" }
    }
    ```

### [**.NET SDK**](#tab/csharp)

Call the [IndexingSchedule](/dotnet/api/azure.search.documents.indexes.models.indexingschedule) class when creating or updating an indexer using the [SearchIndexerClient](/dotnet/api/azure.search.documents.indexes.searchindexerclient). 

The IndexingSchedule constructor requires an interval parameter specified using a TimeSpan object. Recall that the smallest interval value allowed is 5 minutes, and the largest is 24 hours. The second StartTime parameter, specified as a DateTimeOffset object, is optional.

The following C# example creates an indexer, using a predefined data source and index, and sets its schedule to run once every day, starting now:

```csharp
var schedule = new IndexingSchedule(TimeSpan.FromDays(1))
{
    StartTime = DateTimeOffset.Now
};

var indexer = new SearchIndexer("demo-idxr", dataSource.Name, searchIndex.Name)
{
    Description = "Demo data indexer",
    Schedule = schedule
};

await indexerClient.CreateOrUpdateIndexerAsync(indexer);
```

---

## Scheduling behavior FAQ

**Can I run multiple indexer jobs in parallel?**

You can run multiple indexers simultaneously, but each indexer is single instance. You can't run two copies of the same indexer concurrently. 

For text-based indexing, the scheduler can kick off as many indexer jobs as the search service supports, which is determined by the number of [search units](search-capacity-planning.md#concepts-search-units-replicas-partitions). For example, if the service has three replicas and four partitions, you can have 12 indexer jobs in active execution, whether initiated on demand or on a schedule.

For skills-based indexing, indexers run in a specific [execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). For this reason, the number of service units has no bearing on the number of skills-based indexer jobs you can run. Multiple skills-based indexers can run in parallel, but doing so depends on content processor availability within the execution environment.

**Do scheduled jobs always start at the designated time?**

Indexer processes can be queued up and might not start exactly at the time posted, depending on the processing workload and other factors. For example, if an indexer happens to still be running when its next scheduled execution is set to start, the pending execution is postponed until the next scheduled occurrence, allowing the current job to finish.

Let’s consider an example to make this more concrete. Suppose we configure an indexer schedule with an interval of hourly and a start time of January 1, 2024 at 8:00:00 AM UTC. Here's what could happen when an indexer run takes longer than an hour:

1. The first indexer execution starts at or around January 1, 2024 at 8:00 AM UTC. Assume this execution takes 20 minutes (or any amount of time that's less than 1 hour).

1. The second execution starts at or around January 1, 2024 9:00 AM UTC. Suppose that this execution takes 70 minutes - more than an hour – and it will not complete until 10:10 AM UTC.

1. The third execution is scheduled to start at 10:00 AM UTC, but at that time the previous execution is still running. This scheduled execution is then skipped. The next execution of the indexer won't start until 11:00 AM UTC.

In rare cases, such as during maintenance or when recovering from transient conditions, multiple indexer runs are queued up. When this occurs, the indexer executes pending workloads sequentially within the scheduled window. For example, if an indexer is scheduled to run hourly and several runs were delayed or triggered on-demand, those queued up jobs will execute back-to-back until the queue is drained. These are not additional runs, but represent previously scheduled or requested executions. While this behavior is uncommon in most scenarios, the indexer is designed to eventually process all queued tasks to maintain consistency and data freshness.

> [!NOTE]
> If you have strict indexer execution requirements that are time-sensitive, you should consider using the [push API model](search-what-is-data-import.md#pushing-data-to-an-index) so you can control the indexing pipeline directly.

<!-- + Although multiple indexers can run simultaneously, a given indexer is single instance. You can't run two copies of the same indexer concurrently. If an indexer happens to still be running when its next scheduled execution is set to start, the pending execution is postponed until the next scheduled occurrence, allowing the current job to finish. -->

**What happens if indexing fails repeatedly on the same document?**

If an indexer is set to a certain schedule but repeatedly fails on the same document each time, the indexer will begin running on a less frequent interval (up to the maximum interval of at least once every 2 hours or 24 hours, depending on different implementation factors) until it successfully makes progress again. If you believe you have fixed the underlying issue, you can [run the indexer manually](search-howto-run-reset-indexers.md), and if indexing succeeds, the indexer will return to its regular schedule.

## Next steps

For indexers that run on a schedule, you can monitor operations by retrieving status from the search service, or obtain detailed information by enabling resource logging.

+ [Monitor search indexer status](search-monitor-indexers.md)
+ [Collect and analyze log data](monitor-azure-cognitive-search.md)
+ [Index large data sets](search-howto-large-index.md)
