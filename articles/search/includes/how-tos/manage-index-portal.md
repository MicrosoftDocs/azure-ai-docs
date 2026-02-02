---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/03/2025
---

After you [create an index](../../search-how-to-create-search-index.md), you can use the [Azure portal](https://portal.azure.com) to access its statistics and definition or remove it from your search service.

This article describes how to manage an index without affecting its content. For guidance on modifying an index definition, see [Update or rebuild an index in Azure AI Search](../../search-howto-reindex.md).

## Limitations

The pricing tier of your search service determines the maximum number and size of your indexes, fields, and documents. For more information, see [Service limits in Azure AI Search](../../search-limits-quotas-capacity.md).

Otherwise, the following limitations apply to index management:

+ You can't take an index offline for maintenance. Indexes are always available for search operations.

+ You can't directly copy or duplicate an index within or across search services. However, you can use the backup and restore sample for [.NET](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) or [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) to achieve similar functionality.

## View all indexes

To view all your indexes:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. From the left pane, select **Search management** > **Indexes**.

   :::image type="content" source="../../media/search-how-to-manage-index/indexes-page.png" alt-text="Screenshot of the indexes page in the portal." border="true" lightbox="../../media/search-how-to-manage-index/indexes-page.png":::

   By default, the indexes are sorted by name in ascending order. You can sort by **Name**, **Document count**, **Vector index quota usage**, or **Total storage size** by selecting the corresponding column header.

## View an index's statistics

On the index page, the portal provides the following statistics:

+ Number of documents in the index.
+ Storage space used by the index.
+ Vector storage space used by the index.
+ Maximum storage space for each index on your search service, which [depends on your pricing tier](../../search-limits-quotas-capacity.md). This value doesn't represent the total storage currently available to the index.

:::image type="content" source="../../media/search-how-to-manage-index/index-statistics.png" alt-text="Screenshot of the index statistics in the portal." border="true" lightbox="../../media/search-how-to-manage-index/index-statistics.png":::

## View an index's definition

Each index is defined by fields and optional components that enhance search capabilities, such as analyzers, normalizers, tokenizers, and synonym maps. This definition determines the index's structure and behavior during indexing and querying.

On the index page, select **Edit JSON** to view its complete definition.

:::image type="content" source="../../media/search-how-to-manage-index/edit-json-button.png" alt-text="Screenshot of the Edit JSON button in the portal." border="true" lightbox="../../media/search-how-to-manage-index/edit-json-button.png":::

<!--
> [!NOTE]
> The portal doesn't support synonym map definitions. You can use the portal to view existing synonyms, but you can't create them or assign them to fields. For more information, see [Add synonyms in Azure AI Search](../../search-synonym.md).
-->

## Delete an index

> [!WARNING]
> You can't undo an index deletion. Before you proceed, make sure that you want to permanently remove the index and its documents from your search service.

On the index page, select **Delete** to initiate the deletion process.

:::image type="content" source="../../media/search-how-to-manage-index/delete-button.png" alt-text="Screenshot of the Delete button in the portal." border="true" lightbox="../../media/search-how-to-manage-index/delete-button.png":::

The portal prompts you to confirm the deletion. After you select **Delete**, check your notifications to confirm that the deletion was successful.

:::image type="content" source="../../media/search-how-to-manage-index/delete-confirmation.png" alt-text="Screenshot of the deletion confirmation in the portal." border="true" lightbox="../../media/search-how-to-manage-index/delete-confirmation.png":::
