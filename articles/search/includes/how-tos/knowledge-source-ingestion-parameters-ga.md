---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

For indexed knowledge sources only, you can pass the following `ingestionParameters` properties to control how content is ingested and processed.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `DisableImageVerbalization` | Enables or disables the use of image verbalization. The default is `False`, which *enables* image verbalization. Set to `True` to *disable* image verbalization. | Boolean | No | No |
| `ChatCompletionModel` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `DisableImageVerbalization` is set to `False`. | Object | Only `ApiKey` and `DeploymentName` are editable | No |
| `EmbeddingModel` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `ApiKey` and `DeploymentName` are editable | No |
| `ContentExtractionMode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `AiServices` and `AssetStore` parameters are specifiable. | String | No | No |
| `AiServices` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `ContentExtractionMode` is set to `standard`. | Object | Only `ApiKey` is editable | No |
| `AssetStore` | A blob container to store extracted images. Setting this parameter requires that `ContentExtractionMode` is set to `standard`. | Object | No | No |
| `IngestionSchedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `disable_image_verbalization` | Enables or disables the use of image verbalization. The default is `False`, which *enables* image verbalization. Set to `True` to *disable* image verbalization. | Boolean | No | No |
| `chat_completion_model` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `disable_image_verbalization` is set to `False`. | Object | Only `api_key` and `deployment_name` are editable | No |
| `embedding_model` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `api_key` and `deployment_name` are editable | No |
| `content_extraction_mode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `ai_services` and `asset_store` parameters are specifiable. | String | No | No |
| `ai_services` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `content_extraction_mode` is set to `standard`. | Object | Only `api_key` is editable | No |
| `asset_store` | A blob container to store extracted images. Setting this parameter requires that `content_extraction_mode` is set to `standard`. | Object | No | No |
| `ingestion_schedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | Yes | No |
| `disableImageVerbalization` | Enables or disables the use of image verbalization. The default is `false`, which *enables* image verbalization. Set to `true` to *disable* image verbalization. | Boolean | No | No |
| `chatCompletionModel` | A chat completion model that verbalizes images or extracts content. Supported models are `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`. The [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md) is included in the generated skillset. Setting this parameter also requires that `disableImageVerbalization` is set to `false`. | Object | Only `apiKey` and `deploymentId` are editable | No |
| `embeddingModel` | A text embedding model that vectorizes text and image content during indexing and at query time. Supported models are `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large`. The [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md) is included in the generated skillset, and the [Azure OpenAI vectorizer](../../vector-search-vectorizer-azure-open-ai.md) is included in the generated index. | Object | Only `apiKey` and `deploymentId` are editable | No |
| `contentExtractionMode` | Controls how content is extracted from files. The default is `minimal`, which uses standard content extraction for text and images. Set to `standard` for advanced document cracking and chunking using the [Azure Content Understanding skill](../../cognitive-search-skill-content-understanding.md), which is included in the generated skillset. For `standard` only, the `aiServices` and `assetStore` parameters are specifiable. | String | No | No |
| `aiServices` | A Microsoft Foundry resource to access Azure Content Understanding in Foundry Tools. Setting this parameter requires that `contentExtractionMode` is set to `standard`. | Object | Only `apiKey` is editable | No |
| `assetStore` | A blob container to store extracted images. Setting this parameter requires that `contentExtractionMode` is set to `standard`. | Object | No | No |
| `ingestionSchedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | Yes | No |

::: zone-end
