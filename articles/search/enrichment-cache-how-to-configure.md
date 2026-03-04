---
title: Configure enrichment caching (preview)
titleSuffix: Azure AI Search
description: Cache enriched content for potential reuse when modifying downstream skills and projections in an AI enrichment pipeline.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 02/24/2026
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-ropc-nochange
---

# Configure an enrichment cache

> [!IMPORTANT] 
> This feature is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). [Preview REST APIs](/rest/api/searchservice/index-preview) support this feature.

This article explains how to add caching to a skillset pipeline so that you can modify downstream enrichment steps without a full rebuild every time. By default, a skillset is stateless, and changing any part of its composition requires a full rerun of the indexer. With an *enrichment cache*, the indexer determines which parts of the document tree must be refreshed based on skillset or indexer definition changes. Existing processed output is preserved and reused where possible.

Cached content is placed in Azure Storage using a connection string that you provide. These objects are created when you run the indexer. It should be considered an internal component managed by your search service and must not be modified.

+ A container named `ms-az-search-indexercache-<alpha-numeric-string>`
+ Tables named `MsAzSearchIndexerCacheIndex<alpha-numeric-string>`

## Prerequisites

+ [Azure Storage](/azure/storage/common/storage-account-create) for storing cached enrichments. The storage account must be [general purpose v2](/azure/storage/common/storage-account-overview#types-of-storage-accounts).

+ [For blob indexing only](search-how-to-index-azure-blob-storage.md), if you need synchronized document removal from both the cache and index when blobs are deleted from your data source, enable a [deletion policy](search-how-to-index-azure-blob-changed-deleted.md) in the indexer. Without this policy, document deletion from the cache isn't supported.

You should be familiar with setting up indexers and skillsets. Start with [indexer overview](search-indexer-overview.md) and then continue on to [skillsets](cognitive-search-working-with-skillsets.md) to learn about enrichment pipelines. 

## Limitations

> [!CAUTION]
> If you're using the [SharePoint indexer (Preview)](search-how-to-index-sharepoint-online.md), you should avoid incremental enrichment. Under certain circumstances, the cache becomes invalid, requiring an [indexer reset and full rebuild](search-howto-run-reset-indexers.md), should you choose to reload it.

## Permissions

An Azure AI Search identity needs write-access to Azure Storage:

+ **Storage Blob Data Contributor**
+ **Storage Table Data Contributor**

The connection string syntax determines whether a system-assigned or user-assigned identity is used. For more information, see [Connect to Azure Storage using a managed identity](search-howto-managed-identities-storage.md).

## Set the cache property

Use this procedure for both new and existing indexers.

In the indexer definition, set `cache` with:

+ (Required) `storageConnectionString` set to an Azure Storage connection string.
+ (Optional) `enableReprocessing` (`true` by default). Set it to `false` to suspend incremental enrichment temporarily, and switch it back to `true` later.

### [**Azure portal**](#tab/portal)

1. On the left, select **Indexers**.
1. Select **Add indexer** to create a new indexer, or open an existing one in JSON edit mode.
1. Enable incremental enrichment, set the enrichment cache storage account, and save the indexer.

   :::image type="content" source="media/search-incremental-index/portal-option.png" alt-text="Screenshot of the Azure portal option for enrichment cache.":::

1. Reset the indexer if it already exists.

1. Run the indexer. This one-time full rebuild seeds the cache. After it's loaded, incremental reuse applies on subsequent runs.

### [**REST**](#tab/rest)

We recommend that you do a [GET Indexer](/rest/api/searchservice/indexers/get?view=rest-searchservice-2025-11-01-preview&preserve-view=true) if you're editing an existing indexer.

1. Use the latest preview API for [Create or Update Indexer](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

    ```http
    PUT https://[YOUR-SEARCH-SERVICE].search.windows.net/indexers/[YOUR-INDEXER-NAME]?api-version=2025-11-01-preview
        Content-Type: application/json
        api-key: [YOUR-ADMIN-KEY]
        {
            "name": "<YOUR-INDEXER-NAME>",
            "targetIndexName": "<YOUR-INDEX-NAME>",
            "dataSourceName": "<YOUR-DATASOURCE-NAME>",
            "skillsetName": "<YOUR-SKILLSET-NAME>",
            "cache": {
                "storageConnectionString": "<YOUR-STORAGE-ACCOUNT-CONNECTION-STRING>",
                "enableReprocessing": true
            },
            "fieldMappings": [],
            "outputFieldMappings": [],
            "parameters": []
        }
    ```

1. [Reset the indexer](/rest/api/searchservice/indexers/reset) if it already exists.

1. [Run the indexer](/rest/api/searchservice/indexers/run). This one-time full rebuild seeds the cache. After it's loaded, incremental reuse applies on subsequent runs.

    ```http
    POST https://[YOUR-SEARCH-SERVICE].search.windows.net/indexers/[YOUR-INDEXER-NAME]/run?api-version=2025-11-01-preview
        Content-Type: application/json
        api-key: [YOUR-ADMIN-KEY]
    ```

If you now issue another GET request on the indexer, the response from the service includes an `ID` property in the cache object. The string is appended to the name of the container containing all the cached results and intermediate state of each document processed by this indexer. The ID is used to uniquely name the cache in Blob storage.

```http
    "cache": {
        "ID": "<ALPHA-NUMERIC STRING>",
        "enableReprocessing": true,
        "storageConnectionString": "DefaultEndpointsProtocol=https;AccountName=<YOUR-STORAGE-ACCOUNT>;AccountKey=<YOUR-STORAGE-KEY>;EndpointSuffix=core.windows.net"
    }
```

## Check for cached output

1. Sign in to the Azure portal and find your Azure Storage account.

1. Use Storage Browser to review containers and tables.

   + The container name is  `ms-az-search-indexercache-<some-alphanumeric-string>`.

   + Table names are `MsAzSearchIndexerCacheIndex<alpha-numeric-string>`

A cache is created and used by an indexer. Its content isn't human readable.

To verify whether the cache is operational, modify a skillset and run the indexer, then compare before-and-after metrics for execution time and document count.

Skillsets that include image analysis and Optical Character Recognition (OCR) of scanned documents make good test cases. If you modify a downstream text skill or any skill that isn't image-related, the indexer can retrieve previously processed image and OCR content from cache, and process only text-related changes from your edits. You can expect fewer documents in indexer execution counts, shorter execution times, and lower costs.

The [file set](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/ai-enrichment-mixed-media) used in [cog-search-demo tutorials](tutorial-skillset.md) is a useful test case because it contains 14 files of various formats JPG, PNG, HTML, DOCX, PPTX, and other types. Change `en` to `es` or another language in the text translation skill for proof-of-concept testing of incremental enrichment.

## Common errors

The following error occurs if you forget to specify a preview API version on the request:

`"The request is invalid. Details: indexer : A resource without a type name was found, but no expected type was specified. To allow entries without type information, the expected type must also be specified when the model is specified."`

A 400 Bad Request error will also occur if you're missing an indexer requirement. The error message specifies any missing dependencies.

## Next step

Incremental enrichment is applicable on indexers that contain skillsets, providing reusable content for both indexes and knowledge stores. The following link provides more information about cache management.

> [!div class="checklist"]
> + [Manage an enrichment cache](enrichment-cache-how-to-manage.md)
