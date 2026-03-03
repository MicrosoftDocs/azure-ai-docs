---
title: Troubleshoot Storage and Metric Discrepancies
titleSuffix: Azure AI Search
description: Learn why Azure AI Search storage metrics appear inconsistent across the Azure portal, REST APIs, and SDKs, and how to resolve discrepancies.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: troubleshooting-general
ms.date: 03/03/2026
ai-usage: ai-assisted
---

# Troubleshoot storage and metric discrepancies in Azure AI Search

This article answers common questions about storage metrics that appear inconsistent across the Azure portal, REST APIs, and Azure SDKs.

Storage values in Azure AI Search are collected periodically and might not reflect the real-time state. Therefore, short-term discrepancies are expected in most scenarios.

For background on how metrics are collected and reported, see [Monitor Azure AI Search](monitor-azure-cognitive-search.md).

## Why doesn't storage change immediately when I delete or update documents?

When you delete documents, Azure AI Search acknowledges the deletion immediately, but physical storage reclamation happens asynchronously through background merge operations. The underlying document is marked as deleted and skipped during subsequent queries. As new documents are indexed and the internal index grows, the system cleans up deleted documents and reclaims the resources. This means you're likely to observe a lag between deleting documents and the underlying resources being freed.

Document updates have a similar effect on storage. Because documents are immutable, an update is internally a delete-and-insert operation: the old version is marked as deleted, and a new version is inserted. Until background merge operations clean up the old version, you might observe that storage increases temporarily rather than staying the same.

For more information, see [Delete documents in a search index](search-how-to-delete-documents.md) and [Overhead from deleting or updating documents within the index](vector-search-index-size.md#overhead-from-deleting-or-updating-documents-within-the-index).

## Why do portal and API values differ at the same point in time?

The Azure portal and REST APIs might report different values because they have different refresh cadences. Specifically:

- The **Usage** tab on the portal **Overview** page refreshes periodically, typically every few minutes.
- [GET Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) returns service-level counters, including `storageSize`, `vectorIndexSize`, and `documentCount`.
- [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics) returns per-index counters.

Service-level and index-level statistics are collected independently and at different intervals. A snapshot from one surface might not align with a snapshot from the other if they weren't captured at the same time. This behavior is normal and doesn't indicate a defect.

For more information about monitoring surfaces, see [Monitor Azure AI Search](monitor-azure-cognitive-search.md).

## Why is a rebuilt index larger than an older index with similar content?

A rebuilt index might temporarily show a different storage profile while background merge operations run. Several factors also affect final index size:

- Schema changes, such as adding fields, analyzers, or vector configurations.
- Ingestion and update patterns that affect the deleted documents ratio.
- [Vector optimization settings](vector-search-how-to-configure-compression-storage.md), such as quantization or storage reduction options.

The index size stabilizes after merge operations complete. However, overall index storage size is nondeterministic, so there might be minor differences between the old and new index storage size.

For more information about factors that affect size, see [Vector index size and limits](vector-search-index-size.md) and [Service limits in Azure AI Search](search-limits-quotas-capacity.md).

## Why doesn't total storage match vector index size?

`storageSize` and `vectorIndexSize` measure different things:

- `storageSize` is the total disk footprint of an index, including content of all data types, such as text, metadata, and vectors.
- `vectorIndexSize` is a limit on the size of a vector index loaded into memory. Vector fields that use the exhaustive KNN algorithm don't consume vector index quota and report zero for `vectorIndexSize`. For more information, see [Vector index size and limits](vector-search-index-size.md).

On disk, the total storage consumed by vectors might be larger than the in-memory vector index size because Azure AI Search stores multiple copies of vector fields for different purposes. For information about what these copies are and how to reduce disk consumption, see [Eliminate optional vector instances from storage](vector-search-how-to-storage-options.md).

## How should I compare metrics correctly?

To determine if a discrepancy is real or a timing artifact, capture values from the same surface within a consistent UTC time window:

1. Call [GET Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) and [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics) within the same five-minute window.
1. Repeat sampling on a fixed cadence, such as every 20 to 30 minutes.
1. Compare at least three consecutive windows before you conclude that values aren't converging.
1. Evaluate `storageSize` separately from `vectorIndexSize` because they track different physical structures.

## When is a discrepancy expected vs. an actual defect?

Most discrepancies are expected and resolve without intervention. If the defect criteria are met, open a support request with the evidence described in the next section.

### Expected divergence

- You recently performed heavy indexing, updates, or deletions, and values are still converging.
- Portal and API values differ, but the gap narrows across repeated samples.
- `storageSize` and `vectorIndexSize` don't match, which is by design because they measure different things.

### Possible defect

- The discrepancy persists across at least three aligned sampling windows during a period of low write or delete activity.
- No convergence trend is visible despite repeated sampling.
- Reported values lead to incorrect operational decisions, such as delayed autoscale triggering or quota enforcement failures.

## What should I include in a support request?

Include the following information in your [support request](https://portal.azure.com/#view/Microsoft_Azure_Support/HelpAndSupportBlade/~/overview/newsupportrequest/):

- UTC timestamps for each portal and API sample.
- Raw JSON responses from [GET Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) and [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics).
- Approximate ingest, update, and delete volume during the observation period.
- Description of the operational impact, such as a scaling delay, quota block, or incorrect capacity reporting.

## Related content

- [Monitor Azure AI Search](monitor-azure-cognitive-search.md)
- [Vector index size and limits](vector-search-index-size.md)
- [Service limits in Azure AI Search](search-limits-quotas-capacity.md)
- [Delete documents in a search index](search-how-to-delete-documents.md)
