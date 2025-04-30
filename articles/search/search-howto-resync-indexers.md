---
title: Resync indexers
titleSuffix: Azure AI Search
description: Resync
author: ruix
manager: arvind
ms.author: ruix
ms.service: azure-ai-search
ms.custom:
  - build-2025
ms.topic: how-to
ms.date: 04/30/2025
---

# Resync indexers
An indexer is considered synchronized with its data source for specific fields when the data in the source is consistent with the documents in the target index regarding those fields. Typically, an indexer achieves synchronization after a successful initial run. If a document is deleted from the data source, the indexer remains synchronized according to this definition. However, during the next indexer run, the corresponding document in the target index will be removed if delete tracking is enabled.

If a document is modified in the data source, the indexer becomes unsynchronized. Generally, change tracking mechanisms will resynchronize the indexer during the next run. For example, in Azure Storage, modifying a blob updates its last modified time, allowing it to be re-indexed in the subsequent indexer run because the updated time surpasses the high-water mark set by the previous run.

In contrast, for certain data sources like Azure Data Lake Storage Gen2, altering the Access Control Lists (ACLs) of a blob does not change its last modified time, rendering change tracking ineffective. Consequently, the modified blob will not be re-indexed in the subsequent run, as only documents modified after the last high-water mark are processed.

While using either "reset" or "reset docs" can address this issue, "reset" can be time-consuming and inefficient for large datasets, and "reset docs" requires identifying the document key or data source document ID of the blob intended for update.

Resync Indexers offers an efficient and convenient alternative. Users simply place the indexer in resync mode and specify the content to resynchronize by calling the indexer resync API. In the next run, the indexer will enumerate all documents in the data source and compare them with existing documents in the target index. In resync mode, the indexer will update only the documents that show discrepancies between the data source and the target index. After the resync run, the indexer will be synchronized and revert to regular indexer run mode for subsequent runs.


# How to resync and run indexers

1. Call [Indexers - Resync](/rest/api/searchservice/indexers/resync?view=rest-searchservice-2025-05-01-preview&preserve-view=true) with a preview API version to specify what content to re-synchronize.

    ```http
    POST https://[service name].search.windows.net/indexers/[indexer name]/resync?api-version=2025-05-01-preview
    {
        "options" : [
            "permissions"
        ]
    }
    ```
    + Currently the only supported option is permissions. That is, only permission filter fields in the target index will be synchronized.

1. Call [Run Indexer](/rest/api/searchservice/indexers/run) (any API version) to re-synchronize the indexer.

1. Call [Run Indexer](/rest/api/searchservice/indexers/run) a second time to process from the last high-water mark.