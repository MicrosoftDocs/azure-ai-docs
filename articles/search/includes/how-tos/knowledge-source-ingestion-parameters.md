---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 10/17/2025
---

For indexed knowledge sources only, you can pass the following `ingestionParameters` properties to control how content is ingested and processed.

| Name | Description | Type | Required |
|--|--|--|--|
| `identity` | A [managed identity](../../search-how-to-managed-identities.md) to use in the generated indexer. | Object | No |
| `disableImageVerbalization` | Enables or disables the use of image verbalization.  The default is `false`, which *enables* image verbalization. Set to `true` to *disable* image verbalization. | Boolean | No |
| `chatCompletionModel` | A chat completion model that verbalizes images or extracts content. Use a model supported by the [GenAI Prompt skill](../../cognitive-search-skill-genai-prompt.md), which will be included in the generated skillset. Setting this model also requires that `disableImageVerbalization` is set to `false`. | Object | No |
| `embeddingModel` | A text embedding model that vectorizes text and image content during indexing and at query time. Use a model supported by the [Azure OpenAI Embedding skill](../../cognitive-search-skill-azure-openai-embedding.md), [Azure AI Vision multimodal embeddings skill](../../cognitive-search-skill-vision-vectorize.md), [AML skill](../../cognitive-search-aml-skill.md), or [Custom Web API skill](../../cognitive-search-custom-skill-web-api.md). The embedding skill will be included in the generated skillset, and its equivalent vectorizer will be included in the generated index. | Object | No |
| `contentExtractionMode` | Controls how content is extracted from files. The default is `minimal`, which uses default extraction for text and images. Set to `standard` for advanced document cracking, chunking, and image verbalization using the Content Understanding skill, which will replace the [Text Split skill](../../cognitive-search-skill-textsplit.md) in the generated skillset. `standard` requires a billable `aiServices` multi-service resource. You can also use `AssetStore` to save extracted images in a blob container. | String  | No |
| `ingestionSchedule` | Adds scheduling information to the generated indexer. You can also [add a schedule](../../search-howto-schedule-indexers.md) later to automate data refresh. | Object | No |
| `ingestionPermissionOptions` | The permission types to ingest with document content. If you specify `userIds`, `groupIds`, or `rbacScope`, the generated indexer will include the ingested permissions. | Array | No |

If you get errors, make sure the embedding and chat completion models exist at the endpoints you provided.
