---
title: Image Serving in Agentic Retrieval
description: Use image serving in Azure AI Search to inject document-embedded images into agentic retrieval answer synthesis so LLMs can reason over diagrams and scans.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
---

# Surface document-embedded images in agentic retrieval (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

Use *image serving* (preview) to surface images embedded in your source documents (such as diagrams, charts, infographics, scanned forms, and product images) during agentic retrieval, so your large language model (LLM) can reason over visual context alongside text when it synthesizes an answer.

When you enable image serving, Azure AI Search:

+ At indexing time, extracts images from supported documents and stores them in a customer-provided Azure Blob asset store.

+ At query time, fetches those images during the [retrieve action](agentic-retrieval-how-to-retrieve.md), base64-encodes them, and injects them as multimodal content into the LLM prompt that produces the synthesized answer.

This article shows you how to enable image serving on a knowledge base, override it per request, inspect image serving statistics, and plan for the storage account lifecycle requirements.

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that specifies an LLM. The knowledge base must use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md).

+ A file-based indexed knowledge source configured with an [`assetStore`](#configure-the-asset-store-on-a-knowledge-source) in its `ingestionParameters`. Supported kinds:

  + [Blob knowledge source](agentic-knowledge-source-how-to-blob.md) (Azure Blob Storage or Azure Data Lake Storage Gen2)
  + [Indexed OneLake knowledge source](agentic-knowledge-source-how-to-onelake.md)
  + [Indexed SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-indexed.md)

+ Source documents that contain extractable images, such as PNG files, JPEG files, or PDFs with embedded images.

+ Permissions to update the knowledge base and the knowledge source. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ For outbound calls to the LLM during answer synthesis, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource that hosts the LLM.

+ For asset store access, the search service managed identity needs **Storage Blob Data Contributor** on the storage account (or container scope) that hosts the asset store. For more information, see [Configure asset store and application access](#configure-asset-store-and-application-access).

+ The [2026-05-01-preview](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true) REST API or an equivalent Azure SDK preview package: [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md)

## Limitations and considerations

+ Image serving is available only through the `retrieve` API in agentic retrieval. Classic `/docs/search` queries don't return images without a custom solution or configuration.

+ Image serving runs only in [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) output mode. The `extractiveData` output mode skips image serving.

+ Image serving applies only to file-based indexed knowledge sources that have `assetStore` configured and indexed chunks with populated `image_path` values.

+ In mixed knowledge bases, only supported knowledge source kinds (blob, indexed OneLake, and indexed SharePoint) return images. Other kinds can still contribute text grounding, but they don't return images.

+ If Microsoft Purview sensitivity labels are enabled on the knowledge source, image serving isn't supported because images can't be exported to the asset store.

+ The retrieve response returns image references in the asset store, not inline Base64 image bytes. Inline image bytes in the response payload aren't supported because they increase payload size and can degrade latency and overall performance.

+ Image serving doesn't bypass index-level security. To control who can see image references, use [document-level access control](search-document-level-access-overview.md) on the underlying knowledge source. Set `ingestionPermissionOptions` at ingestion time and pass the user's access token at query time. For more information, see [Enforce permissions at query time](agentic-retrieval-how-to-retrieve.md#enforce-permissions-at-query-time-preview).

+ Document-level permissions apply only to index content. They don't automatically propagate to the asset store. Any identity with read access to the asset store container can fetch images. If you need per-document authorization for image retrieval, place a service layer in front of blob access and validate caller permissions before returning the blob.

+ Don't store secrets (account keys, tokens, connection strings) in source documents because content can be returned as grounding data.

+ Image serving can increase answer synthesis latency because of image download and multimodal token processing. Use the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) and filtered results to control overhead.

## How image serving works

Image serving has two phases:

+ **Indexing:** When you configure an asset store on a knowledge source, the search service extracts images from each source document and writes them to your Azure Blob asset store. Optionally, it also calls an LLM to generate a text description (*verbalization*) for each image and stores that description in the index next to the chunk that references the image.

    When you configure an asset store, the search service also provisions a [knowledge store](knowledge-store-concept-intro.md) alongside the knowledge source to persist the extracted image artifacts. You can inspect and manage this knowledge store like any other.

+ **Retrieval:** When the retrieve action runs with image serving enabled, the search service fetches the matching images from the asset store, base64-encodes them, and includes them as multimodal content in the answer synthesis prompt. Image bytes aren't returned in the retrieve response; only references (the `image_path` field on each contributing chunk) are.

<!--
Authoring placeholder: Two-phase architecture diagram for image serving.

Phase 1 (top, "Indexing"): Source document -> Skillset (image extraction + optional verbalization via LLM) -> outputs: (1) Asset store (blob container) holding extracted images, (2) Search index holding chunks with image_path and optional text descriptions.

Phase 2 (bottom, "Retrieval"): Retrieve request -> Search service fetches matching chunks from index -> downloads referenced images from asset store -> base64-encodes images and sends them with text content to LLM -> Synthesized answer plus activity (imageServing block) returned to caller. Application separately reads image_path values and fetches blobs from asset store using its own identity.
-->

## Configure asset store and application access

Image serving spans three trust boundaries. At indexing time, the search service writes image artifacts to your asset store. At query time, the search service reads from the asset store to retrieve images. Your application also reads from the asset store if it needs to render images in a UI. Configure each path to follow least-privilege access.

### Search service access to the asset store

+ Use Microsoft Entra ID and a [managed identity](search-how-to-managed-identities.md) for the search service. Assign the identity the **Storage Blob Data Contributor** role on the storage account (or container scope) so the indexer can write image artifacts and the retrieve action can read them back.

+ Don't enable anonymous public access on the asset store container.

### Application access to image references

The retrieve response contains references to images (the `image_path` field on each contributing chunk), not the image bytes. To display an image in your application:

1. Assign your application's identity the **Storage Blob Data Reader** role on the asset store container.

1. Read the `image_path` value from the retrieve response and fetch the blob from Azure Storage using that identity.

This separation lets you control who can view source images independently of who can call the retrieve API.

## Configure the asset store on a knowledge source

Configure `assetStore` in the `ingestionParameters` of a supported indexed knowledge source. The asset store is a blob container that you own and that the search service writes image artifacts into.

For source-specific instructions, see:

+ [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md)
+ [Create an indexed SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-indexed.md)
+ [Create a OneLake knowledge source](agentic-knowledge-source-how-to-onelake.md)

A minimal blob knowledge source with image serving enabled looks like this:

```http
PUT https://{service-name}.search.windows.net/knowledgesources/my-blob-ks?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {admin-api-key}

{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "azureBlobParameters": {
    "connectionString": "{blob-connection-string}",
    "containerName": "source-documents"
  },
  "ingestionParameters": {
    "assetStore": {
      "connectionString": "{blob-connection-string}",
      "containerName": "image-assets"
    },
    "chatCompletionModel": {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://{aoai-resource}.openai.azure.com",
        "deploymentId": "gpt-4o",
        "modelName": "gpt-4o"
      }
    },
    "embeddingModel": {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://{aoai-resource}.openai.azure.com",
        "deploymentId": "text-embedding-3-large",
        "modelName": "text-embedding-3-large"
      }
    },
    "contentExtractionMode": "standard",
    "aiServices": {
      "uri": "https://{foundry-resource}.services.ai.azure.com"
    }
  }
}
```

> [!NOTE]
> The Azure Storage account that hosts the asset store needs to remain available and accessible to the search service for the lifetime of the knowledge base. If you change network rules, rotate keys, swap identities, or move the storage account in a way that prevents the search service from reading the asset store, image serving stops returning images. The retrieve API doesn't surface this as a hard error: it reports the drop in `imagesDropped` in activity, and answer synthesis proceeds with text only. Plan and test any storage account changes carefully.

### Configuration outcomes

The combination of `assetStore`, `disableImageVerbalization`, and `chatCompletionModel` determines what the indexer stores and what the model sees at query time:

+ **Asset store + verbalization (default):** `assetStore` set, `disableImageVerbalization` left as `false`, `chatCompletionModel` set. The indexer persists images to the asset store and stores text descriptions in the index. `verbalizationUsed` is `true` at query time.

+ **Asset store only:** `assetStore` set, `disableImageVerbalization` set to `true`, `chatCompletionModel` not required. The indexer persists images to the asset store but doesn't generate text descriptions. `verbalizationUsed` is `false`.

+ **No asset store, model set:** `assetStore` not set, `chatCompletionModel` set. Text descriptions only, no image artifacts. Image serving doesn't apply.

+ **No asset store, no model:** No image processing.

### Verify asset store configuration

Wait for ingestion to complete before continuing:

+ Check indexer status in the [Azure portal](https://portal.azure.com) or use [Get Indexer Status](/rest/api/searchservice/indexers/get-status) (REST API).

+ Verify that indexed chunks have a populated `image_path` field. Empty `image_path` values usually mean the source documents don't contain extractable images, the asset store isn't configured, or the indexer hasn't finished.

+ Inspect the asset store container. You should see image blobs that the indexer wrote during ingestion.

## Enable image serving on a knowledge base

Set `enableImageServing` to `true` on the knowledge source reference inside the knowledge base definition. This setting becomes the default for every retrieve request that targets the knowledge source.

The knowledge base definition also specifies the LLM used for **answer synthesis at query time**. This setting is independent of any `chatCompletionModel` that you set on the knowledge source's `ingestionParameters`, which drives image verbalization during indexing.

If your knowledge base references multiple knowledge sources, set `enableImageServing` only on supported file-based indexed kinds that have `assetStore` configured. Unsupported kinds (such as search index, remote SharePoint, or web) still contribute text grounding but don't return images.

```http
PUT https://{service-name}.search.windows.net/knowledgebases/my-kb?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {admin-api-key}

{
  "name": "my-kb",
  "knowledgeSources": [
    {
      "name": "my-blob-ks",
      "enableImageServing": true
    }
  ],
  "outputMode": "answerSynthesis",
  "chatCompletionModel": {
    "kind": "azureOpenAI",
    "azureOpenAIParameters": {
      "resourceUri": "https://{aoai-resource}.openai.azure.com",
      "deploymentId": "gpt-4o",
      "modelName": "gpt-4o"
    }
  }
}
```

### Verify image serving enablement

Send a `GET` request to the knowledge base endpoint and verify that the knowledge source reference includes `"enableImageServing": true`.

## Retrieve with image serving

Call the [retrieve action](agentic-retrieval-how-to-retrieve.md) against the knowledge base. To override the knowledge base default on a per-request basis, set `enableImageServing` in the matching entry under `knowledgeSourceParams`.

```http
POST https://{service-name}.search.windows.net/knowledgebases/my-kb/retrieve?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {admin-api-key}

{
  "retrievalReasoningEffort": { "kind": "medium" },
  "outputMode": "answerSynthesis",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "What's the wiring configuration shown in the installation guide?" }
      ]
    }
  ],
  "knowledgeSourceParams": [
    {
      "knowledgeSourceName": "my-blob-ks",
      "kind": "azureBlob",
      "enableImageServing": true
    }
  ]
}
```

> [!NOTE]
> Image serving runs only when `outputMode` is `answerSynthesis`. Requests that use `extractiveData` skip image serving, even when `enableImageServing` is set.

### What happens at retrieval time

For chunks that have an `image_path`, the search service downloads the corresponding image from the asset store, base64-encodes it, and passes it as multimodal content to the LLM that produces the synthesized answer. The base64 image bytes are used only for that model call; they aren't returned to your application. Image download failures are non-fatal: successful images are forwarded to the model, and failures are silently counted in `imagesDropped`. For the exact response shape, see the reference documentation for [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-05-01-preview&preserve-view=true) (REST API).

### Verify retrieve behavior

A successful retrieve response with image serving enabled has these signals:

+ The `activity` array contains an `imageServing` block for each knowledge source that returned images.

+ `imagesSentToModel` is greater than `0` for queries whose grounding includes image-bearing chunks.

+ `imagesDropped` is `0` or close to it. Persistent drops usually point to RBAC or asset store availability issues. For more information, see [Troubleshooting](#troubleshooting).

+ The synthesized answer references content that only appears in an image, such as a diagram or a scanned form.

### Precedence rules

When both the knowledge base definition and the retrieve request specify `enableImageServing`, the value in the retrieve request takes precedence. The full precedence is:

1. The value in `knowledgeSourceParams[].enableImageServing` on the retrieve request (if set).
1. The value on the matching knowledge source reference in the knowledge base definition (if set).
1. `false` (the default).

The following table summarizes the nine combinations.

| Knowledge base definition (`enableImageServing`) | Retrieve request (`enableImageServing`) | Images served? |
|---|---|---|
| `true` | `true` | Yes |
| `true` | `false` | No |
| `true` | Not set | Yes |
| `false` | `true` | Yes |
| `false` | `false` | No |
| `false` | Not set | No |
| Not set | `true` | Yes |
| Not set | `false` | No |
| Not set | Not set | No |

## Inspect image serving statistics

When image serving runs, the retrieve response includes an `imageServing` section for each knowledge source inside the `activity` array. Use this section to verify whether images were sent to the model and to diagnose dropped images.

```json
"activity": [
  {
    "type": "azureBlob",
    "knowledgeSourceName": "my-blob-ks",
    "imageServing": {
      "verbalizationUsed": true,
      "imagesRetrieved": 5,
      "imagesSentToModel": 4,
      "imagesDropped": 1
    }
  }
]
```

The fields report:

+ `verbalizationUsed`: Whether the indexing pipeline generated text descriptions for images. This value is `true` when, at indexing time, both `disableImageVerbalization` was `false` (the default) **and** `chatCompletionModel` was set on the knowledge source. It reflects the indexing-time configuration of the knowledge source, not a retrieval-time decision.

+ `imagesRetrieved`: The number of images found across the chunks that matched this knowledge source for the current request.

+ `imagesSentToModel`: The number of images that were successfully downloaded and forwarded to the LLM.

+ `imagesDropped`: The number of images that failed to download or were unavailable. Image serving treats drops as non-fatal: answer synthesis proceeds with the remaining images and text.

<!--
## Portal experience

Portal support for enabling and managing image serving is planned for a future update. This section will be expanded with a step-by-step procedure and a portal screenshot after the experience is available.
-->

## Test image serving end to end

To test the full setup against multiple agentic retrieval configurations (image serving enabled and disabled, different output modes, runtime overrides), see the [image serving testing samples](https://aka.ms/agentic-retrieval-image-serving-testing). The samples include an end-to-end walkthrough that creates the knowledge source, knowledge base, and retrieve requests so you can compare answers with and without image serving.

A typical A/B comparison checklist:

+ Pick a question that can only be answered from a diagram, chart, or scanned image.

+ Run the retrieve request with `enableImageServing: false` and capture the answer.

+ Run the same retrieve request with `enableImageServing: true` and compare answer completeness, grounding to image content, and latency.

+ Verify the `imageServing` activity reports the expected number of images sent to the model.

## Troubleshooting

Use the `imageServing` activity block from [Inspect image serving statistics](#inspect-image-serving-statistics) as your first diagnostic. The following table maps common symptoms to likely causes and fixes.

| Symptom | Likely cause | What to try |
|---|---|---|
| `imagesDropped` is high and `imagesSentToModel` is low | The search service can't read from the asset store. | Verify the search service managed identity has **Storage Blob Data Contributor** on the asset store container. Check storage account network rules and firewall settings. |
| `imagesRetrieved` is `0` for image-rich documents | `image_path` isn't populated in the index, or no matching chunks contained images. | Re-run the indexer and verify `image_path` is populated. Verify that the source documents contain extractable images (PDFs with embedded raster images, or supported image files). |
| Retrieve response has no `imageServing` block | `enableImageServing` is `false` (the default) or `outputMode` isn't `answerSynthesis`. | Set `enableImageServing` to `true` on the knowledge base or per request, and use `outputMode: "answerSynthesis"`. |
| `verbalizationUsed` is `false` but you expected `true` | At indexing time, `disableImageVerbalization` was `true` or `chatCompletionModel` wasn't set on the knowledge source. | Update the knowledge source `ingestionParameters` and re-run ingestion. |
| Answer synthesis fails or times out after you enable image serving | Multimodal token overhead exceeds the model context window, or the LLM deployment can't be reached. | Lower [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md), tighten retrieval results, or use a model deployment with higher token limits. |
| Your application can't render images from `image_path` | The application identity doesn't have **Storage Blob Data Reader** on the asset store. | Assign **Storage Blob Data Reader** to your application's identity at the storage account or container scope. |

## Related content

+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)
+ [Knowledge sources for agentic retrieval](agentic-knowledge-source-overview.md)
+ [Knowledge store concepts](knowledge-store-concept-intro.md)
