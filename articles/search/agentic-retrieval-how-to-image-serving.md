---
title: Image Serving in Agentic Retrieval
description: Use image serving in Azure AI Search to inject document-embedded images into agentic retrieval answer synthesis so LLMs can reason over diagrams and scans.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/18/2026
ai-usage: ai-assisted
---

# Surface document-embedded images in agentic retrieval (preview)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-08-01-preview can't modify access permissions that were set outside of the 2026-08-01-preview. If you use the 2026-08-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-08-01-preview recognizes changes to those access or permission restrictions.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

Use *image serving* (preview) to surface images embedded in your source documents (such as diagrams, charts, infographics, scanned forms, and product images) during agentic retrieval, so your large language model (LLM) can reason over visual context alongside text when it synthesizes an answer.

When you enable image serving, Azure AI Search:

+ At indexing time, extracts images from supported documents and stores them in a customer-provided Azure Blob asset store.

+ At query time, fetches those images during the [retrieve action](agentic-retrieval-how-to-retrieve.md), base64-encodes them, and injects them as multimodal content into the LLM prompt that produces the synthesized answer.

This article shows you how to enable image serving on a knowledge base, override it per request, inspect image serving statistics, and plan for the storage account lifecycle requirements.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-08-01-preview&preserve-view=true) |
| -- | -- | -- | -- | -- | -- | -- |
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that specifies an LLM. The knowledge base must use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md).

+ A file-based indexed knowledge source configured with an [`assetStore`](#configure-the-asset-store-on-a-knowledge-source) in its `ingestionParameters`. Supported kinds:

  + [Blob knowledge source](agentic-knowledge-source-how-to-blob.md) (Azure Blob Storage or Azure Data Lake Storage Gen2)
  + [Indexed OneLake knowledge source](agentic-knowledge-source-how-to-onelake.md)
  + [Indexed SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-indexed.md)

  For blob knowledge sources that use standard extraction, complete the [blob knowledge source prerequisites](agentic-knowledge-source-how-to-blob.md#prerequisites).

+ The knowledge source must not configure `ingestionPermissionOptions`.

+ Source documents that contain extractable images, such as PNG files, JPEG files, or PDFs with embedded images.

+ A Microsoft Foundry resource in a [region supported by Azure Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/language-region-support), with Azure OpenAI embedding and multimodal chat model deployments. Use the resource endpoint in the `https://<resource-name>.services.ai.azure.com` format.

+ Permission to create or update the knowledge base and managed knowledge source. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** and **Search Index Data Contributor** roles assigned to the user or automation identity that performs these management operations (recommended). Alternatively, use an [admin API key](search-security-api-keys.md).

+ Permission to call the retrieve action. Assign the **Search Index Data Reader** role to the identity that sends retrieve requests (recommended) or use a [query API key](search-security-api-keys.md).

+ For outbound calls to the LLM during answer synthesis, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource that hosts the LLM.

+ For asset store access, configure the search service managed identity as described in [Configure asset store and application access](#configure-asset-store-and-application-access).

+ The [2026-08-01-preview](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true) REST API or an equivalent Azure SDK preview package: [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md)

## Limitations and considerations

+ Image serving is available only through the `retrieve` API in agentic retrieval. Classic `/docs/search` queries don't supply document-embedded images to downstream answer synthesis without a custom solution or configuration.

+ Image serving runs only in [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) output mode. The `extractiveData` output mode skips image serving.

+ Image serving applies only to file-based indexed knowledge sources that have `assetStore` configured and indexed chunks with populated `image_path` values.

+ In mixed knowledge bases, only supported knowledge source kinds (blob, indexed OneLake, and indexed SharePoint) supply document-embedded images to downstream answer synthesis. Other kinds can still contribute text grounding.

+ Image serving isn't supported for knowledge sources that use `ingestionPermissionOptions` to ingest document-level permissions, including ACLs, RBAC scopes, or Microsoft Purview sensitivity labels. The asset store creates an underlying knowledge store, and knowledge stores don't support permission inheritance.

+ The retrieve response schema doesn't define fields for the individual asset-store image paths or image bytes sent to the model. The `imageServing` activity reports aggregate statistics for the images retrieved and sent to the model.

+ Access to images is controlled at the storage-account level, independently of access to indexed content. Any identity with read access to the asset storage account can fetch its images.

+ Don't store secrets (account keys, tokens, connection strings) in source documents because content can be returned as grounding data.

+ Image serving can increase answer synthesis latency because of image download and multimodal token processing. Run representative queries with image serving enabled and disabled and compare response latency with the reported `imageServing` activity.

+ Content Understanding can produce different image results for PDF and DOCX files. If consistent embedded-image extraction and verbalization are required, convert source documents to PDF or test each source format with representative content.

## How image serving works

Image serving has two phases:

+ **Indexing:** When you configure standard content extraction and an asset store on a knowledge source, the generated Content Understanding skill semantically chunks the document, preserves tables as Markdown, and uses the configured LLM to describe embedded figures. Figure descriptions become part of the enriched Markdown that the embedding skill vectorizes. The skill also extracts images to your blob asset store and adds `image_path` references to overlapping chunks.

    When you configure an asset store, the search service also provisions a [knowledge store](knowledge-store-concept-intro.md) alongside the knowledge source to persist the extracted image artifacts. You can inspect and manage this knowledge store like any other.

+ **Retrieval:** When the retrieve action runs with image serving enabled, the search service fetches the matching images from the asset store, base64-encodes them, and includes them as multimodal content in the answer synthesis prompt.

## Configure asset store and application access

Image serving spans three trust boundaries. At indexing time, the search service writes image artifacts to your asset store. At query time, the search service reads from the asset store to retrieve images. Your application also reads from the asset store if it needs to render images in a UI. Configure each path to follow least-privilege access.

### Search service access to the asset store

+ Use Microsoft Entra ID and a [managed identity](search-how-to-managed-identities.md) for the search service. Assign the identity the **Storage Blob Data Contributor** role at the storage-account scope because the indexer writes image artifacts and the retrieve action reads them. When the source and asset containers share that account, the role also provides source-blob read access.

+ Don't enable anonymous public access on the asset store container.

### Application access to image references

The generated index stores `image_path` references to images in the asset store. The retrieve response schema doesn't define dedicated fields for the individual asset-store image paths or image bytes sent to the model. Optional `sourceData` is structured reference data, and `image_path` isn't required in it.

To display an indexed image in your application:

1. Assign your application's identity the **Storage Blob Data Reader** role at the asset storage-account scope.

1. Assign your application's identity the **Search Index Data Reader** role so it can query the generated index.

1. Obtain an authorized `image_path` from the generated index through an application-controlled query or service endpoint.

1. Validate that the reference resolves to the expected storage account and asset container. Reject untrusted paths before the blob lookup.

1. Fetch the resulting blob name from the asset container by using your application's identity.

This separation lets you control who can view source images independently of who can call the retrieve API.

## Configure the asset store on a knowledge source

Configure `assetStore` in the `ingestionParameters` of a supported indexed knowledge source. The asset store is a blob container that you own and that the search service writes image artifacts into.

For source-specific instructions, see:

+ [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md)
+ [Create an indexed SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-indexed.md)
+ [Create a OneLake knowledge source](agentic-knowledge-source-how-to-onelake.md)

A minimal blob knowledge source with image serving enabled looks like this:

```http
PUT https://{service-name}.search.windows.net/knowledgesources/my-blob-ks?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "name": "my-blob-ks",
  "kind": "azureBlob",
  "azureBlobParameters": {
    "connectionString": "ResourceId=<storage-resource-id>",
    "containerName": "source-documents",
    "ingestionParameters": {
      "assetStore": {
        "connectionString": "ResourceId=<storage-resource-id>",
        "containerName": "image-assets"
      },
      "chatCompletionModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "https://{foundry-resource}.services.ai.azure.com",
          "deploymentId": "gpt-4o",
          "modelName": "gpt-4o"
        }
      },
      "embeddingModel": {
        "kind": "azureOpenAI",
        "azureOpenAIParameters": {
          "resourceUri": "https://{foundry-resource}.services.ai.azure.com",
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
}
```

> [!NOTE]
> + Replace `<storage-resource-id>` with the resource ID of the Azure Storage account. The `ResourceId=<storage-resource-id>` connection format tells the search service to use its managed identity for both containers.
>
> + The Azure Storage account that hosts the asset store needs to remain available and accessible to the search service for the lifetime of the knowledge base. If you change network rules, rotate keys, swap identities, or move the storage account in a way that prevents the search service from reading the asset store, image serving can't supply those images to the model. Compare `imagesRetrieved` with `imagesSentToModel` in retrieval activity and plan and test storage account changes carefully.

### Configuration outcomes

The combination of `assetStore`, `disableImageVerbalization`, and `chatCompletionModel` determines what the indexer stores and what the model sees at query time:

+ **Asset store + verbalization (default):** `assetStore` set, `disableImageVerbalization` left as `false`, `chatCompletionModel` set. The indexer persists images to the asset store and stores text descriptions in the index. Retrieval activity can report `verbalizationUsed` as `true`.

+ **Asset store only:** `assetStore` set, `disableImageVerbalization` set to `true`, `chatCompletionModel` not required. The indexer persists images to the asset store but doesn't generate text descriptions. Retrieval activity can report `verbalizationUsed` as `false`.

+ **No asset store, model set:** `assetStore` not set, `chatCompletionModel` set. Text descriptions only, no image artifacts. Image serving doesn't apply.

+ **No asset store, no model:** No image processing.

### Verify asset store configuration

Wait for ingestion to complete before continuing:

+ Check indexer status in the [Azure portal](https://portal.azure.com) or use [Get Indexer Status](/rest/api/searchservice/indexers/get-status) (REST API).

+ Check whether indexed chunks have a populated `image_path` field. If `image_path` is empty, check the indexer status, the knowledge source asset-store configuration, the source document contents, and the asset container contents.

+ Inspect the asset store container. You should see image blobs that the indexer wrote during ingestion.

## Enable image serving on a knowledge base

Set `enableImageServing` to `true` on the knowledge source reference inside the knowledge base definition. This setting becomes the default for every retrieve request that targets the knowledge source.

The knowledge base definition also specifies the LLM used for **answer synthesis at query time**. This setting is independent of any `chatCompletionModel` that you set on the knowledge source's `ingestionParameters`, which drives image verbalization during indexing.

If your knowledge base references multiple knowledge sources, set `enableImageServing` only on supported file-based indexed kinds that have `assetStore` configured. Unsupported kinds (such as search index, remote SharePoint, or web) still contribute text grounding but don't supply document-embedded images to downstream answer synthesis.

```http
PUT https://{service-name}.search.windows.net/knowledgebases/my-kb?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "name": "my-kb",
  "knowledgeSources": [
    {
      "name": "my-blob-ks",
      "enableImageServing": true
    }
  ],
  "outputMode": "answerSynthesis",
  "models": [
    {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://{foundry-resource}.services.ai.azure.com",
        "deploymentId": "gpt-4o",
        "modelName": "gpt-4o"
      }
    }
  ]
}
```

### Verify image serving enablement

Send a `GET` request to the knowledge base endpoint and verify that the knowledge source reference includes `"enableImageServing": true`.

## Retrieve with image serving

Call the [retrieve action](agentic-retrieval-how-to-retrieve.md) against the knowledge base. To override the knowledge base default on a per-request basis, set `enableImageServing` in the matching entry under `knowledgeSourceParams`.

```http
POST https://{service-name}.search.windows.net/knowledgebases/my-kb/retrieve?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "retrievalReasoningEffort": { "kind": "medium" },
  "outputMode": "answerSynthesis",
  "includeActivity": true,
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

For image references associated with matching content, the search service downloads the corresponding images from the asset store, base64-encodes them, and passes them as multimodal content to the downstream answer-synthesis model. Inspect aggregate image-serving statistics in `activity.imageServing`. For the exact response shape, see the reference documentation for [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2026-08-01-preview&preserve-view=true) (REST API).

### Verify retrieve behavior

A retrieve response can provide these image-serving signals:

+ When `includeActivity` is `true`, the `activity` array reports `imageServing` activity for a knowledge source when the service records image-serving operations.

+ An `imagesSentToModel` value greater than `0` means the service reports that it supplied images to the downstream answer-synthesis model.

### Precedence rules

When both the knowledge base definition and the retrieve request specify `enableImageServing`, the value in the retrieve request takes precedence. The full precedence is:

1. The value in `knowledgeSourceParams[].enableImageServing` on the retrieve request (if set).
1. The value on the matching knowledge source reference in the knowledge base definition (if set).
1. `false` (the default).

The following table summarizes the nine combinations.

| Knowledge base definition (`enableImageServing`) | Retrieve request (`enableImageServing`) | Image serving enabled? |
| --- | --- | --- |
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

When image serving runs, the retrieve response includes an `imageServing` section for each knowledge source inside the `activity` array. Use this section to compare the images retrieved from the asset store with the images sent to the model.

```json
"activity": [
  {
    "type": "azureBlob",
    "knowledgeSourceName": "my-blob-ks",
    "imageServing": {
      "verbalizationUsed": true,
      "imagesRetrieved": 5,
      "imagesSentToModel": 4,
      "totalImageSizeBytes": 248361
    }
  }
]
```

The fields report:

+ `verbalizationUsed`: The service-reported image verbalization statistic for the retrieval activity.

+ `imagesRetrieved`: The number of images retrieved from the asset store.

+ `imagesSentToModel`: The number of images sent to the downstream model.

+ `totalImageSizeBytes`: The total size, in bytes, of the images sent to the model.

If `imagesRetrieved` is greater than `imagesSentToModel`, not every retrieved image was sent to the model.

Inspect `verbalizationUsed` and `imagesSentToModel` independently. A response can report both `verbalizationUsed` as `true` and one or more images sent to the model.

<!--
## Portal experience

Portal support for enabling and managing image serving is planned for a future update. This section will be expanded with a step-by-step procedure and a portal screenshot after the experience is available.
-->

## Test image serving end to end

Use one of the following samples to test the full setup:

+ [C# image-serving sample](https://github.com/Azure-Samples/azure-search-dotnet-samples/tree/main/image-serving-example)
+ [Python image-serving sample](https://github.com/Azure-Samples/azure-search-python-samples/tree/main/image-serving-example)

The samples create a blob knowledge source and knowledge base, compare retrieve requests with image serving disabled and enabled, and inspect image-serving statistics. They also use an independent wildcard index query to select an `image_path` and download that asset. The samples select one semicolon-delimited reference, remove a projection prefix such as `11.7:` from a relative path, or URL-decode an absolute path and remove its leading asset-container segment. These transformations are sample behavior, not guarantees of the retrieve API. The selected asset isn't evidence that the same image contributed to a particular retrieve response.

A typical A/B comparison checklist:

+ Pick a question that can only be answered from a diagram, chart, or scanned image.

+ Run the retrieve request with `enableImageServing: false` and capture the answer.

+ Run the same retrieve request with `enableImageServing: true` and compare the answers, latency, and reported activity.

+ Treat answer differences as observational A/B signals, not proof that images caused the differences. An `imagesSentToModel` value greater than `0` means the service reports that it supplied images to the model.

## Clean up resources

Delete the knowledge base before you delete its knowledge source. Deleting these Azure AI Search resources doesn't delete source documents or projected image blobs in Azure Storage. Delete those blobs separately only when no retained ingestion or retrieval pipeline still needs them.

## Troubleshooting

Use the `imageServing` activity block from [Inspect image serving statistics](#inspect-image-serving-statistics) as your first diagnostic. The following table lists checks for common symptoms without assuming a single cause.

| Symptom | Checks |
| --- | --- |
| `imagesRetrieved` is `0` for image-rich documents | Check indexer status and warnings, populated `image_path` values in matching indexed chunks, and image blobs in the asset container. Confirm that the source documents contain extractable images and that the search service identity has **Storage Blob Data Contributor** at the storage-account scope. |
| Retrieve response has no `imageServing` block | Confirm that the request sets `includeActivity` to `true`. Check the effective `enableImageServing` value after applying request, knowledge base, and default precedence. Confirm that `outputMode` is `answerSynthesis`, and inspect source activity errors and warnings. |
| `verbalizationUsed` differs from what you expect | Check `disableImageVerbalization`, `chatCompletionModel`, and the most recent indexer status. Inspect `verbalizationUsed` independently from `imagesSentToModel`. A response can report verbalization and images sent together. |
| Answer synthesis fails or times out after you enable image serving | Compare representative requests with image serving enabled and disabled. Inspect activity errors and warnings, the answer-synthesis model deployment status, search service identity permissions for the model and storage account, and asset-store availability. |
| Your application can't render an independently queried `image_path` | Confirm that the independent index query returns a usable `image_path`, the referenced blob exists, and the application can access the blob independently of retrieve. Check that the application identity has **Search Index Data Reader** for the index query and **Storage Blob Data Reader** at the asset storage-account scope. |

## Related content

+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Knowledge store concepts](knowledge-store-concept-intro.md)
