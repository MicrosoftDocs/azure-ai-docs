---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

<!--
Preview (2025-11-01-preview) ingestion parameters properties table.
Included in all indexed KS how-to articles under the [2025-11-01-preview] tab.
Includes preview-only properties (e.g., ingestionPermissionOptions) not in the GA version.
-->

For indexed knowledge sources only, you can pass the following `ingestionParameters` properties to control how content is ingested and processed.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `DisableImageVerbalization` | Enables or disables the use of image verbalization. The default is `False`, which *enables* image verbalization. Set to `True` to *disable* image verbalization. | Boolean | No | No |
| `ChatCompletionModel` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `DisableImageVerbalization` is set to `False`. | Object | Only `ApiKey` and `DeploymentName` are editable | No |
| `EmbeddingModel` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `ApiKey` and `DeploymentName` are editable | No |
| `ContentExtractionMode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `AiServices` parameter is specifiable. | String | No | No |
| `AiServices` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `ContentExtractionMode` is set to `standard`. | Object | Only `ApiKey` is editable | No |
| `IngestionSchedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |
| `IngestionPermissionOptions` | The document-level permissions to ingest alongside content. Specify `UserIds`, `GroupIds`, or `RbacScope` to store permission metadata in the index. You can also specify `SensitivityLabel` to ingest [Microsoft Purview sensitivity label](../../search-indexer-sensitivity-labels.md) metadata for blob, indexed OneLake, and indexed SharePoint knowledge sources. For source-specific RBAC guidance, see [Ingest RBAC permissions from blob storage](../../search-blob-indexer-role-based-access.md#configure-a-knowledge-source) and [Ingest ACLs from ADLS Gen2](../../search-indexer-access-control-lists-and-role-based-access.md#configure-a-knowledge-source). To enforce these permissions at query time, see [Enforce permissions at query time](../../agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview). | Array | No | No |
| `AssetStore` | (2026-05-01-preview only) A blob container used to persist images extracted from source documents. Required to enable [image serving](../../agentic-retrieval-how-to-image-serving.md) (preview) for the knowledge base. Setting this parameter provisions a [knowledge store](../../knowledge-store-concept-intro.md) alongside the knowledge source to store the image artifacts. You can inspect and manage this knowledge store like any other. The storage account must remain accessible to the search service for the lifetime of the knowledge base. | Object | No | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `disable_image_verbalization` | Enables or disables the use of image verbalization. The default is `False`, which *enables* image verbalization. Set to `True` to *disable* image verbalization. | Boolean | No | No |
| `chat_completion_model` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `disable_image_verbalization` is set to `False`. | Object | Only `api_key` and `deployment_name` are editable | No |
| `embedding_model` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `api_key` and `deployment_name` are editable | No |
| `content_extraction_mode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `ai_services` parameter is specifiable. | String | No | No |
| `ai_services` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `content_extraction_mode` is set to `standard`. | Object | Only `api_key` is editable | No |
| `ingestion_schedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |
| `ingestion_permission_options` | The document-level permissions to ingest alongside content. Specify `user_ids`, `group_ids`, or `rbac_scope` to store permission metadata in the index. You can also specify `sensitivity_label` to ingest [Microsoft Purview sensitivity label](../../search-indexer-sensitivity-labels.md) metadata for blob, indexed OneLake, and indexed SharePoint knowledge sources. For source-specific RBAC guidance, see [Ingest RBAC permissions from blob storage](../../search-blob-indexer-role-based-access.md#configure-a-knowledge-source) and [Ingest ACLs from ADLS Gen2](../../search-indexer-access-control-lists-and-role-based-access.md#configure-a-knowledge-source). To enforce these permissions at query time, see [Enforce permissions at query time](../../agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview). | Array | No | No |
| `asset_store` | (2026-05-01-preview only) A blob container used to persist images extracted from source documents. Required to enable [image serving](../../agentic-retrieval-how-to-image-serving.md) (preview) for the knowledge base. Setting this parameter provisions a [knowledge store](../../knowledge-store-concept-intro.md) alongside the knowledge source to store the image artifacts. You can inspect and manage this knowledge store like any other. The storage account must remain accessible to the search service for the lifetime of the knowledge base. | Object | No | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `disableImageVerbalization` | Enables or disables the use of image verbalization. The default is `false`, which *enables* image verbalization. Set to `true` to *disable* image verbalization. | Boolean | No | No |
| `chatCompletionModel` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `disableImageVerbalization` is set to `false`. | Object | Only `apiKey` and `deploymentId` are editable | No |
| `embeddingModel` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `apiKey` and `deploymentId` are editable | No |
| `contentExtractionMode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `aiServices` parameter is specifiable. | String | No | No |
| `aiServices` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `contentExtractionMode` is set to `standard`. | Object | Only `apiKey` is editable | No |
| `ingestionSchedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |
| `ingestionPermissionOptions` | The document-level permissions to ingest alongside content. Specify `userIds`, `groupIds`, or `rbacScope` to store permission metadata in the index. You can also specify `sensitivityLabel` to ingest [Microsoft Purview sensitivity label](../../search-indexer-sensitivity-labels.md) metadata for blob, indexed OneLake, and indexed SharePoint knowledge sources. For source-specific RBAC guidance, see [Ingest RBAC permissions from blob storage](../../search-blob-indexer-role-based-access.md#configure-a-knowledge-source) and [Ingest ACLs from ADLS Gen2](../../search-indexer-access-control-lists-and-role-based-access.md#configure-a-knowledge-source). To enforce these permissions at query time, see [Enforce permissions at query time](../../agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview). | Array | No | No |
| `assetStore` | (2026-05-01-preview only) A blob container used to persist images extracted from source documents. Required to enable [image serving](../../agentic-retrieval-how-to-image-serving.md) (preview) for the knowledge base. Setting this parameter provisions a [knowledge store](../../knowledge-store-concept-intro.md) alongside the knowledge source to store the image artifacts. You can inspect and manage this knowledge store like any other. The storage account must remain accessible to the search service for the lifetime of the knowledge base. | Object | No | No |

::: zone-end
