---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/13/2025
---

For indexed knowledge sources only, you can pass the following `ingestionParameters` properties to control how content is ingested and processed.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `disable_image_verbalization` | Enables or disables the use of image verbalization. The default is `False`, which *enables* image verbalization. Set to `True` to *disable* image verbalization. | Boolean | No | No |
| `chat_completion_model` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) will be included in the generated skillset. Setting this parameter also requires that `disable_image_verbalization` is set to `False`. | Object | Only `api_key` and `deployment_name` are editable | No |
| `embedding_model` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) will be included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) will be included in the generated index. | Object | Only `api_key` and `deployment_name` are editable | No |
| `content_extraction_mode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which will be included in the generated skillset. For `standard` only, the `ai_services` and `asset_store` parameters are specifiable. | String | No | No |
| `ai_services` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `content_extraction_mode` is set to `standard`. | Object | Only `api_key` is editable | Yes |
| `asset_store` | A blob container to store extracted images. Setting this parameter requires that `content_extraction_mode` is set to `standard`. | Object | No | No |
| `ingestion_schedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |
| `ingestion_permission_options` | The document-level permissions to ingest from select knowledge sources: either [ADLS Gen2](../../agentic-knowledge-source-how-to-blob.md) or [indexed SharePoint](../../agentic-knowledge-source-how-to-sharepoint-indexed.md). If you specify `user_ids`, `group_ids`, or `rbac_scope`, the generated [ADLS Gen2 indexer](../../search-indexer-access-control-lists-and-role-based-access.md) or [SharePoint indexer](../../search-indexer-sharepoint-access-control-lists.md) will include the ingested permissions. | Array | No | No |
