---
title: Manage Enrichment Caching
description: Cache intermediate content and incremental changes from AI enrichment pipeline in Azure Storage to preserve investments in existing processed documents. This feature is currently in preview.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 07/07/2026
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-ropc-nochange
---

# Manage an enrichment cache

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT] 
> This feature is in preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). The [preview REST API](/rest/api/searchservice/search-service-api-versions#preview-versions) supports this feature.

An *enrichment cache* is an optional feature that stores enriched content created during [skillset execution](cognitive-search-working-with-skillsets.md). It preserves content between runs so that only changed skills and documents require reprocessing. It isn't a backup of skillset outputs, indexer state, or indexed documents. 

You create the enrichment cache in Azure Storage. The cache contains the output from [document cracking](search-indexer-overview.md#document-cracking), plus the outputs of each skill for every document. Although caching is billable (it uses Azure Storage), the overall cost of enrichment is reduced because the costs of storage are less than image extraction and AI processing.

If you configure an enrichment cache, this article explains how to manage skill and data source updates so that you get maximum utility from cached enrichments.

## Prerequisites

+ An [indexer](search-indexer-overview.md) and [skillset](cognitive-search-working-with-skillsets.md)

+ An [enrichment cache](enrichment-cache-how-to-configure.md)

## Limitations

> [!CAUTION]
> If you're using the [SharePoint indexer (Preview)](search-how-to-index-sharepoint-online.md), avoid incremental enrichment. Under certain circumstances, the cache becomes invalid. To reload it, perform an [indexer reset and full rebuild](search-howto-run-reset-indexers.md).

Large data sources have an additional cache limitation.

> [!CAUTION]
> For large data sources, an enrichment cache can increase total reprocessing when long-running skills, repeated interruptions, or frequent skill failures occur. The indexer prioritizes correctness over minimizing reprocessing, so a cache backlog from repeated interruptions amplifies retry behavior.
>
> To recover from a growing cache backlog, partition the data source into smaller containers or virtual folders. Then use [parallel indexers](search-how-to-large-index.md#parallel-indexing) pointing to the same index. To disassociate the cache, set the `cache` property to null on the indexer.

## Cache configuration

Physically, the cache is stored in a blob container and tables in your Azure Storage account, one per indexer. Each indexer is assigned a unique and immutable cache identifier that corresponds to the container it's using.

The cache is created when you specify the `cache` property and run the indexer. Only enriched content can be cached. If your indexer doesn't have an attached skillset, then caching doesn't apply. 

The following example illustrates an indexer with caching enabled. See [Configure enrichment caching](enrichment-cache-how-to-configure.md) for full instructions. 

```json
POST https://[YOUR-SEARCH-SERVICE-NAME].search.windows.net/indexers?api-version=2026-05-01-preview
    {
        "name": "myIndexerName",
        "targetIndexName": "myIndex",
        "dataSourceName": "myDatasource",
        "skillsetName": "mySkillset",
        "cache" : {
            "storageConnectionString" : "<Your storage account connection string>",
            "enableReprocessing": true
        },
        "fieldMappings" : [],
        "outputFieldMappings": [],
        "parameters": []
    }
```

## Cache management

The indexer manages the cache lifecycle. If you delete an indexer, you also delete its cache. If you set the indexer's `cache` property to null or change the connection string, the existing cache is deleted during the next indexer run. 

While incremental enrichment is designed to detect and respond to changes with no intervention on your part, you can set parameters to invoke specific behaviors:

+ [Prioritize new documents](#prioritize-new-documents)
+ [Bypass skillset checks](#bypass-skillset-evaluation)
+ [Bypass data source checks](#bypass-data-source-validation-checks)
+ [Force skillset evaluation](#force-skillset-evaluation)

### Prioritize new documents

The `cache` property includes an `enableReprocessing` parameter that controls whether cached content is reprocessed. When true (default), the indexer reprocesses cached documents when you rerun it if a skill update affects them.

When false, the indexer doesn't reprocess existing documents, which prioritizes new content. Set `enableReprocessing` to false only temporarily. Keeping it true most of the time ensures that both new and existing documents remain valid for the current skillset definition.

### Bypass skillset evaluation

Modifying a skill usually goes hand in hand with reprocessing that skill. However, some changes to a skill shouldn't trigger reprocessing. For example, deploying a custom skill to a new location or with a new access key. These changes are usually peripheral modifications that don't affect the substance of the skill output. 

If you know that a change to the skill is superficial, override skill evaluation by setting the `disableCacheReprocessingChangeDetection` parameter to true:

1. Call [Update Skillset](/rest/api/searchservice/skillsets/create-or-update) and modify the skillset definition.
1. Append the `disableCacheReprocessingChangeDetection=true` parameter on the request.
1. Submit the change.

When you set this parameter, only updates to the skillset definition are committed. The change isn't evaluated for effects on the existing cache. Use a preview API version, 2020-06-30-Preview or later. Use the latest preview API.

```http
PUT https://[servicename].search.windows.net/skillsets/[skillset name]?api-version=2026-05-01-preview&disableCacheReprocessingChangeDetection
  
```

### Bypass data source validation checks

Most changes to a data source definition invalidate the cache. However, for scenarios where you know that a change shouldn't invalidate the cache - such as changing a connection string or rotating the key on the storage account - append the `ignoreResetRequirement` parameter on the [data source update](/rest/api/searchservice/data-sources/create-or-update). Set this parameter to true to allow the commit to go through, without triggering a reset condition that would result in all objects being rebuilt and populated from scratch.

```http
PUT https://[search service].search.windows.net/datasources/[data source name]?api-version=2026-05-01-preview&ignoreResetRequirement
 
```

### Force skillset evaluation

The purpose of the cache is to avoid unnecessary processing. But suppose you make a change to a skill that the indexer doesn't detect (for example, changing something in external code, such as a custom skill).

In this case, use the [Reset Skills](/rest/api/searchservice/skillsets/reset-skills?view=rest-searchservice-2026-05-01-preview&preserve-view=true) API to force reprocessing of a particular skill, including any downstream skills that have a dependency on that skill's output. This API accepts a POST request with a list of skills that should be invalidated and marked for reprocessing. After Reset Skills, follow with a [Run Indexer](/rest/api/searchservice/indexers/run) request to invoke the pipeline processing.

## Re-cache specific documents

If you [reset an indexer](/rest/api/searchservice/indexers/reset), all documents in the search corpus are reprocessed. 

In scenarios where only a few documents need reprocessing, use [Reset Documents (preview)](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2026-05-01-preview&preserve-view=true) to force reprocessing of specific documents. When you reset a document, the indexer invalidates the cache for that document. The indexer then reprocesses the document by reading it from the data source. For more information, see [Run or reset indexers, skills, and documents](search-howto-run-reset-indexers.md).

To reset specific documents, include a list of document keys as read from the search index in the request. If the key maps to a field in the external data source, use the value from the search index.

Depending on how you call the API, the request either appends, overwrites, or queues up the key list:

+ Calling the API multiple times with different keys appends the new keys to the list of document keys to reset. 

+ Calling the API with the `overwrite` query string parameter set to `true` overwrites the current list of document keys to reset with the request's payload.

+ Calling the API adds the document keys to the queue of work the indexer performs. When the indexer is next invoked, either as scheduled or on demand, it prioritizes processing the reset document keys before any other changes from the data source.

The following example illustrates a reset document request:

```http
POST https://[search service name].search.windows.net/indexers/[indexer name]/resetdocs?api-version=2026-05-01-preview
    {
        "documentKeys" : [
            "key1",
            "key2",
            "key3"
        ]
    }
```

## Changes that invalidate the cache

When you enable a cache, the indexer checks for changes in your pipeline composition to decide which content it can reuse and which content needs reprocessing. This section lists changes that invalidate the cache, followed by changes that trigger incremental processing. 

An invalidating change is one where the entire cache becomes invalid. For example, updating your data source is an invalidating change. Here's the complete list of changes to any part of the indexer pipeline that invalidate your cache:

+ Changing the data source type
+ Changing data source container
+ Changing data source credentials
+ Changing data source change detection policy
+ Changing data source delete detection policy
+ Changing indexer field mappings
+ Changing indexer parameters:
  + Parsing Mode
  + Excluded File Name Extensions
  + Indexed File Name Extensions
  + Index storage metadata only for oversized documents
  + Delimited text headers
  + Delimited text delimiter
  + Document Root
  + Image Action (Changes to how images are extracted)

## Changes that trigger incremental processing

Incremental processing evaluates your skillset definition and determines which skills to rerun. It selectively updates the affected portions of the document tree. Here's the complete list of changes that result in incremental enrichment:

+ Changing the skill type (updating the OData type of the skill)
+ Updating skill-specific parameters, such as a URL, defaults, or other parameters
+ Changing skill outputs, such as when the skill returns additional or different outputs
+ Changing skill inputs that result in different ancestry or skill chaining
+ Any upstream skill invalidation, if you update a skill that provides an input to this skill
+ Updating the knowledge store projection location, which results in re-projecting documents
+ Changing the knowledge store projections, which results in re-projecting documents
+ Changing output field mappings on an indexer, which results in re-projecting documents to the index

## APIs used for caching

Preview APIs provide extra properties on indexers. Use the latest preview API.

Use the generally available version for skillsets and data sources. In addition to the reference documentation, see [Configure caching for incremental enrichment](enrichment-cache-how-to-configure.md) for details about order of operations.

+ [Create or Update Indexer (api-version=2026-05-01-preview)](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true) 

+ [Reset Skills (api-version=2026-05-01-preview)](/rest/api/searchservice/skillsets/reset-skills?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

+ [Create or Update Skillset (api-version=2026-05-01-preview)](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true) (New URI parameter on the request)

+ [Create or Update Data Source (api-version=2026-05-01-preview)](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true) When you call this API with a preview API version, it provides a new parameter named `ignoreResetRequirement`. Set this parameter to `true` when your update action shouldn't invalidate the cache. Use `ignoreResetRequirement` sparingly as it could lead to unintended inconsistency in your data that isn't easily detected.
