---
title: Schedule Indexer Execution
description: Learn how to schedule Azure AI Search indexers to index content at specific intervals, or at specific dates and times.
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 07/07/2026
ms.update-cycle: 365-days
---

# Schedule an indexer in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Set the `schedule` property to configure indexers to run on a schedule. Indexer scheduling is useful in situations such as:

+ Source data changes over time, and you want the indexer to automatically process the difference.
+ Source data is very large, and you need a recurring schedule to index all of the content.
+ An index is populated from multiple sources using multiple indexers, and you want to stagger the jobs to reduce conflicts.

When indexing can't complete within the [typical 2-hour processing window](search-howto-run-reset-indexers.md#indexer-execution), schedule the indexer to run on a 2-hour cadence to work through a large volume of data. As long as your data source supports [change detection logic](search-howto-create-indexers.md#change-detection-and-internal-state), indexers can automatically pick up where they left off on each run.

Once you put an indexer on a schedule, it stays on the schedule until you clear the interval or start time, or set `disabled` to true. If a scheduled indexer stops triggering unexpectedly, see [Scheduling behavior FAQ](#scheduling-behavior-faq) for recovery steps. Leaving the indexer on a schedule when there's nothing to process doesn't impact system performance. Checking for changed content is a relatively fast operation.

## Prerequisites

+ A valid indexer configured with a data source and index.

+ [Change detection](search-howto-create-indexers.md#change-detection-and-internal-state) in the data source. Azure Storage and SharePoint have built-in change detection. For other data sources, such as [Azure SQL](search-how-to-index-sql-database.md) and [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md), you must enable change detection manually.

## Schedule definition

A schedule is part of the indexer definition. If you omit the `schedule` property, the indexer only runs on demand. The property has two parts.

| Property | Description |
|----------|-------------|
| "interval" | (required) The amount of time between the start of two consecutive indexer executions. The smallest interval allowed is 5 minutes, and the longest is 1,440 minutes (24 hours). Format it as an XSD "dayTimeDuration" value (a restricted subset of an [ISO 8601 duration](https://www.w3.org/TR/xmlschema11-2/#dayTimeDuration) value). </br></br>The pattern for this value is: `P(nD)(T(nH)(nM))`. </br></br>Examples: `PT15M` for every 15 minutes, `PT2H` for every two hours.|
| "startTime" | (optional) Specify the start time in coordinated universal time (UTC). If you omit this value, the current time is used. This time can be in the past, in which case the first execution is scheduled as if the indexer has been running continuously since the original start time.|

The following example is a schedule that starts on January 1 at midnight and runs every two hours.

```json
{
    "dataSourceName" : "hotels-ds",
    "targetIndexName" : "hotels-idx",
    "schedule" : { "interval" : "PT2H", "startTime" : "2024-01-01T00:00:00Z" }
}
```

## Configure a schedule

Specify schedules in an indexer definition. To set up a schedule, use the Azure portal, REST APIs, or an Azure SDK.

### [**Azure portal**](#tab/portal)

1. Go to your search service in the [Azure portal](https://portal.azure.com).
1. On the left pane, select **Indexers**.
1. Open an indexer.
1. Select **Settings**.
1. Scroll down to **Schedule**, and then choose **Hourly**, **Daily**, or **Custom** to set a specific date, time, or custom interval.

Switch to the **Indexer Definition (JSON)** tab at the top of the index to view the schedule definition in XSD format.

### [**REST**](#tab/rest)

1. Call [Create Indexer](/rest/api/searchservice/indexers/create) or [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update).

1. Set the schedule property in the body of the request:

    ```http
    PUT /indexers/<indexer-name>?api-version=2026-04-01
    {
        "dataSourceName" : "myazuresqldatasource",
        "targetIndexName" : "my-target-index-name",
        "schedule" : { "interval" : "PT10M", "startTime" : "2024-01-01T00:00:00Z" }
    }
    ```

### [**.NET SDK**](#tab/csharp)

Call the [IndexingSchedule](/dotnet/api/azure.search.documents.indexes.models.indexingschedule) class when creating or updating an indexer by using the [SearchIndexerClient](/dotnet/api/azure.search.documents.indexes.searchindexerclient). 

The IndexingSchedule constructor requires an interval parameter specified as a TimeSpan object. The smallest interval value allowed is 5 minutes, and the largest is 24 hours. The second StartTime parameter, specified as a DateTimeOffset object, is optional.

The following C# example creates an indexer by using a predefined data source and index, and sets its schedule to run once every day, starting now:

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

You can run multiple indexers simultaneously, but each indexer is a single instance. You can't run two copies of the same indexer concurrently. 

For text-based indexing, the scheduler can start as many indexer jobs as the search service supports, which the number of [search units](search-capacity-planning.md) determines. For example, if the service has three replicas and four partitions, you can have 12 indexer jobs in active execution, whether initiated on demand or on a schedule.

For skills-based indexing, indexers run in a specific [execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). For this reason, the number of service units doesn't affect the number of skills-based indexer jobs you can run. Multiple skills-based indexers can run in parallel, but doing so depends on content processor availability within the execution environment.

**Do scheduled jobs always start at the designated time?**

Indexer processes can queue up and might not start exactly at the time posted, depending on the processing workload and other factors. For example, if an indexer happens to still be running when its next scheduled execution is set to start, the pending execution is postponed until the next scheduled occurrence, which allows the current job to finish.

To make this behavior more concrete, consider the following example. Suppose you configure an indexer schedule with an interval of hourly and a start time of January 1, 2024 at 8:00:00 AM UTC. Here's what could happen when an indexer run takes longer than an hour:

1. The first indexer execution starts at or around January 1, 2024 at 8:00 AM UTC. Assume this execution takes 20 minutes (or any amount of time that's less than 1 hour).

1. The second execution starts at or around January 1, 2024 9:00 AM UTC. Suppose that this execution takes 70 minutes - more than an hour – and it doesn't complete until 10:10 AM UTC.

1. The third execution is scheduled to start at 10:00 AM UTC, but at that time the previous execution is still running. This scheduled execution is then skipped. The next execution of the indexer doesn't start until 11:00 AM UTC.

In rare cases, such as during maintenance or when recovering from transient conditions, the system queues up multiple indexer runs. When this condition occurs, the indexer executes pending workloads sequentially within the scheduled window. For example, if an indexer is scheduled to run hourly and several runs were delayed or triggered on-demand, those queued up jobs execute back-to-back until the queue is drained. These runs aren't extra runs, but represent previously scheduled or requested executions. While this behavior is uncommon in most scenarios, the indexer is designed to eventually process all queued tasks to maintain consistency and data freshness.

> [!NOTE]
> If you have strict indexer execution requirements that are time-sensitive, consider using the [push API model](search-what-is-data-import.md#pushing-data-to-an-index) so you can control the indexing pipeline directly.

<!-- + Although multiple indexers can run simultaneously, a given indexer is single instance. You can't run two copies of the same indexer concurrently. If an indexer happens to still be running when its next scheduled execution is set to start, the pending execution is postponed until the next scheduled occurrence, allowing the current job to finish. -->

**What happens if indexing fails repeatedly on the same document?**

If you set an indexer to a certain schedule but it repeatedly fails on the same document each time, the indexer begins running on a less frequent interval (up to the maximum interval of at least once every 2 hours or 24 hours, depending on different implementation factors) until it successfully makes progress again. If you believe you fixed the underlying issue, [run the indexer manually](search-howto-run-reset-indexers.md). If indexing succeeds, the indexer returns to its regular schedule. If the indexer doesn't return to its regular schedule after a successful manual run, see the next question.

**A scheduled indexer stopped triggering. How do I reset its schedule?**

If a scheduled indexer stops running, disable and then re-enable it to reset the schedule. A sign that this recovery is needed: no new runs appear in execution history even though the schedule is configured and the data source changed.

Setting `disabled` to `true` suspends the schedule. Setting it back to `false` (or omitting the property) resumes scheduling, using the current time as the new baseline for the configured interval.

### [**Azure portal**](#tab/portal-recovery)

1. Go to your search service in the [Azure portal](https://portal.azure.com).
1. Select **Indexers**.
1. Select the indexer to open it.
1. Select **Settings**.
1. Set the indexer to **Disabled**.
1. Select **Save**.
1. Set the indexer back to **Enabled**.
1. Select **Save**.
1. Select the **Execution history** tab and verify that a new run appears within the next scheduled interval.

### [**REST**](#tab/rest-recovery)

1. Call [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update) to disable the indexer:

    ```http
    PUT /indexers/<indexer-name>?api-version=2026-04-01
    {
        "dataSourceName": "<datasource-name>",
        "targetIndexName": "<index-name>",
        "schedule": { "interval": "<interval>", "startTime": "<start-time>" },
        "disabled": true
    }
    ```

1. Call [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update) again to re-enable it:

    ```http
    PUT /indexers/<indexer-name>?api-version=2026-04-01
    {
        "dataSourceName": "<datasource-name>",
        "targetIndexName": "<index-name>",
        "schedule": { "interval": "<interval>", "startTime": "<start-time>" },
        "disabled": false
    }
    ```

1. **(Optional)** Call [Run Indexer](/rest/api/searchservice/indexers/run) to trigger an on-demand run and confirm the indexer responds.

1. Call [Get Indexer Status](/rest/api/searchservice/indexers/get-status) to review `lastResult` and confirm execution succeeded.

---

> [!NOTE]
> Re-enabling the indexer resets the schedule relative to the current time, not the original `startTime`. For example, if the interval is two hours and you re-enable at 3:15 PM, the next scheduled run is at approximately 5:15 PM.

## Next steps

For indexers that run on a schedule, you can monitor operations by retrieving status from the search service, or get detailed information by enabling resource logging.

+ [Monitor search indexer status](search-monitor-indexers.md)
+ [Collect and analyze log data](monitor-azure-cognitive-search.md)
+ [Index large data sets](search-howto-large-index.md)
