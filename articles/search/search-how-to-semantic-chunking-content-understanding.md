---
title: Chunk and Vectorize Content with Azure Content Understanding Skill
description: Use the Azure Content Understanding skill to semantically chunk documents, generate AI-based image descriptions, and vectorize the results in an Azure AI Search index.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ms.custom:
  - references_regions
  - build-2026
ai-usage: ai-assisted
---

# Chunk and vectorize content with the Azure Content Understanding skill

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

In this article, you learn how to use the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md) to:

> [!div class="checklist"]
> + Extract text and images from a document
> + Produce semantically coherent chunks that respect paragraph and section boundaries
> + Generate AI descriptions of charts, diagrams, and other inline images
> + Embed each chunk for vector search and project it into an Azure AI Search index

The Azure Content Understanding skill returns one or more chunks per document. Each chunk contains Markdown-formatted content, location metadata (page numbers and bounding polygons), and optional references to extracted images. When you set `chunkingProperties.method` to `semantic`, chunks follow paragraph and heading boundaries instead of fixed-character spans. When you set `modelName` and `modelDeployment`, the skill calls an Azure OpenAI chat-completion deployment to generate descriptions of embedded images. The skill then merges those descriptions into the chunk content.

This article uses the [sample health plan PDFs](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) for illustration. You can run the same pipeline against any [supported data source](search-indexer-overview.md#supported-data-sources) that exposes files in a [format that Content Understanding supports](/azure/ai-services/content-understanding/service-limits#document-and-text).

## Prerequisites

+ An Azure AI Search service in any [supported region](search-region-support.md). The search service itself isn't region-constrained for this scenario.

+ A Microsoft Foundry resource in a [region supported by the Azure Content Understanding skill](cognitive-search-skill-content-understanding.md#supported-regions). Image description and chunking are processed in the Foundry resource's region.

+ A Microsoft Foundry resource [attached to the skillset](cognitive-search-attach-cognitive-services.md) for billing. The Azure Content Understanding skill is billed at [Azure Content Understanding pricing](https://azure.microsoft.com/pricing/details/content-understanding/).

+ (Optional) An Azure OpenAI deployment of a chat completion model (such as `gpt-4.1`) in the same Foundry resource, used to generate image descriptions. Required only if you want AI-based image descriptions.

+ An Azure OpenAI deployment of an embedding model (such as `text-embedding-3-small`), used by the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) to vectorize chunks.

+ An [Azure Blob Storage](search-howto-indexing-azure-blob-storage.md) container with the files you want to index. This article uses a blob data source with the `allowSkillsetToReadFileData` indexer setting (used to pass file content to the Content Understanding skill).

## Overview

The article builds a one-to-many indexing pipeline. Each source document produces multiple search documents (one per chunk):

1. The indexer reads each file from Azure Blob Storage and passes the binary content to the skillset through `/document/file_data`.

1. The **Azure Content Understanding skill** chunks the document into `text_sections`. When `modelName` and `modelDeployment` are set, it also produces AI-generated descriptions of embedded images and inlines them into each chunk's Markdown.

1. The **Azure OpenAI Embedding skill** runs once per chunk and produces a vector for the chunk content.

1. An **index projection** writes one search document per chunk into the target index, mapping content, page metadata, image references, and the vector to fields.

1. (Optional) A **knowledge store** projects `normalized_images` to Azure Blob Storage so client apps can retrieve the extracted images by URL.


## Prepare data files

The Azure Content Understanding skill processes the binary content of each document, so source files must be in a format that the skill supports. For the current list, see the [Content Understanding service limits](/azure/ai-services/content-understanding/service-limits#document-and-text). Common supported formats include PDF, DOCX, XLSX, PPTX, and many image formats.

Upload your files to the supported data source. You can use the Azure portal, REST APIs, or an Azure SDK to [create the data source](search-how-to-index-azure-blob-storage.md).

The following minimal request creates the data source used throughout this walkthrough.

```http
POST {endpoint}/datasources?api-version=2026-05-01-preview

{
  "name": "my_blob_datasource",
  "type": "azureblob",
  "credentials": {
    "connectionString": "<your-blob-connection-string>"
  },
  "container": {
    "name": "my-container"
  }
}
```

## Create an index for one-to-many indexing

Each search document corresponds to one chunk produced by the Content Understanding skill. The index needs:

+ A key field (`chunk_id`).
+ A parent field that identifies which source document the chunk came from (`parent_id`).
+ Fields that store the chunk content, page metadata, and image references.
+ A vector field for the chunk embedding.

The following index definition matches the skillset that you create in the next section.

```json
{
  "name": "my_content_understanding_index",
  "fields": [
    {
      "name": "chunk_id",
      "type": "Edm.String",
      "key": true,
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": true,
      "facetable": false,
      "analyzer": "keyword"
    },
    {
      "name": "parent_id",
      "type": "Edm.String",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "chunk",
      "type": "Edm.String",
      "searchable": true,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "page_number_from",
      "type": "Edm.Int32",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "stored": true,
      "sortable": true,
      "facetable": false
    },
    {
      "name": "page_number_to",
      "type": "Edm.Int32",
      "searchable": false,
      "filterable": true,
      "retrievable": true,
      "stored": true,
      "sortable": true,
      "facetable": false
    },
    {
      "name": "image_path",
      "type": "Edm.String",
      "searchable": false,
      "filterable": false,
      "retrievable": true,
      "stored": true,
      "sortable": false,
      "facetable": false
    },
    {
      "name": "text_vector",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "stored": false,
      "dimensions": 1536,
      "vectorSearchProfile": "profile"
    }
  ],
  "vectorSearch": {
    "profiles": [
      {
        "name": "profile",
        "algorithm": "algorithm"
      }
    ],
    "algorithms": [
      {
        "name": "algorithm",
        "kind": "hnsw"
      }
    ]
  }
}
```

## Define a skillset for semantic chunking and vectorization

With the target index in place, define the skillset that produces the chunks, vectors, and projection mappings that feed it.

The skillset has two skills:

+ The [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md) chunks each document. Setting `chunkingProperties.method` to `semantic` makes the skill respect paragraph and heading boundaries. Setting `modelName` and `modelDeployment` enables AI-generated image descriptions, which the skill inlines into the chunk content before vectorization. For the list of supported chat completion models and other parameter details, see [Skill parameters](cognitive-search-skill-content-understanding.md#skill-parameters).

+ The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) generates a vector for each chunk's content.

The skillset uses `indexProjections` to map each chunk to a separate search document. For more information, see [Define an index projection](search-how-to-define-index-projections.md).

Before you send the request, replace `<subdomain>` with your Azure OpenAI subdomain, `<Azure OpenAI api key>` with the embedding-resource key, and `<Foundry resource key>` with the key for the Foundry resource attached to the skillset.

```http
POST {endpoint}/skillsets?api-version=2026-05-01-preview

{
  "name": "my_content_understanding_skillset",
  "description": "Semantic chunking, image descriptions, and vectorization with the Azure Content Understanding skill",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Util.ContentUnderstandingSkill",
      "name": "my_content_understanding_skill",
      "context": "/document",
      "modelName": "gpt-4.1",
      "modelDeployment": "my-gpt-4-1-deployment",
      "chunkingProperties": {
        "method": "semantic",
        "unit": "tokens",
        "maximumLength": 500
      },
      "extractionOptions": ["images", "locationMetadata"],
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        {
          "name": "text_sections",
          "targetName": "text_sections"
        },
        {
          "name": "normalized_images",
          "targetName": "normalized_images"
        }
      ]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "name": "my_azure_openai_embedding_skill",
      "context": "/document/text_sections/*",
      "inputs": [
        {
          "name": "text",
          "source": "/document/text_sections/*/content"
        }
      ],
      "outputs": [
        {
          "name": "embedding",
          "targetName": "text_vector"
        }
      ],
      "resourceUri": "https://<subdomain>.openai.azure.com",
      "deploymentId": "text-embedding-3-small",
      "modelName": "text-embedding-3-small",
      "apiKey": "<Azure OpenAI api key>"
    }
  ],
  "cognitiveServices": {
    "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
    "key": "<Foundry resource key>"
  },
  "indexProjections": {
    "selectors": [
      {
        "targetIndexName": "my_content_understanding_index",
        "parentKeyFieldName": "parent_id",
        "sourceContext": "/document/text_sections/*",
        "mappings": [
          {
            "name": "chunk",
            "source": "/document/text_sections/*/content"
          },
          {
            "name": "text_vector",
            "source": "/document/text_sections/*/text_vector"
          },
          {
            "name": "page_number_from",
            "source": "/document/text_sections/*/locationMetadata/pageNumberFrom"
          },
          {
            "name": "page_number_to",
            "source": "/document/text_sections/*/locationMetadata/pageNumberTo"
          },
          {
            "name": "image_path",
            "source": "/document/text_sections/*/imagePath"
          },
          {
            "name": "title",
            "source": "/document/metadata_storage_name"
          }
        ]
      }
    ],
    "parameters": {
      "projectionMode": "skipIndexingParentDocuments"
    }
  }
}
```

For the full parameter reference, supported values, and validation rules for the Content Understanding skill, see [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md).

> [!NOTE]
> This article uses API keys to keep the examples concise. For production, we recommend using a managed identity:
>
> + **Skillset to Foundry resource:** To bind the skillset to the Foundry resource with a managed identity instead of a key, see [Connect a search service to Azure AI services](cognitive-search-attach-cognitive-services.md). When you use managed identity, omit the `key` property from the skillset's `cognitiveServices` block.
>
> + **Skillset to Azure OpenAI:** The [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md) supports managed identity in place of `apiKey`.
>
> + **Indexer to Azure Blob Storage:** Replace the connection string with a managed-identity connection. See [Set up a connection to a data source using a managed identity](search-how-to-managed-identities.md).
>
> For an end-to-end overview, see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Configure and run the indexer

Create and run an indexer that reads from your data source, calls the skillset, and projects chunks into the index. Set `allowSkillsetToReadFileData` to `true` so the Content Understanding skill receives the file content, and set `parsingMode` to `default`.

You don't need `outputFieldMappings` in this scenario. The `indexProjections` block in the skillset already maps each chunk to the target index fields.

```http
POST {endpoint}/indexers?api-version=2026-05-01-preview

{
  "name": "my_content_understanding_indexer",
  "dataSourceName": "my_blob_datasource",
  "targetIndexName": "my_content_understanding_index",
  "skillsetName": "my_content_understanding_skillset",
  "parameters": {
    "batchSize": 1,
    "configuration": {
      "dataToExtract": "contentAndMetadata",
      "parsingMode": "default",
      "allowSkillsetToReadFileData": true
    }
  },
  "fieldMappings": [],
  "outputFieldMappings": []
}
```

When the indexer runs, the Content Understanding skill chunks each document, optionally generates image descriptions, and writes one search document per chunk to the index.

### Check indexer status

Before you query, confirm the indexer run finished:

```http
GET {endpoint}/indexers/my_content_understanding_indexer/status?api-version=2026-05-01-preview
```

Verify that `lastResult.status` is `success`. If it's `transientFailure` with `itemsProcessed` higher than `0`, the run is a partial success, and you can still query the populated chunks. For more information, see [Monitor indexer status](search-monitor-indexers.md).

## Verify results

Query the index to verify that the chunks contain the expected content and that vector search works as expected. Use [Search Explorer](search-explorer.md) or any tool that sends HTTP requests.

The following request runs a hybrid query (keyword search on `chunk` and a vector query against `text_vector`) to confirm that both the chunked text and the embeddings are populated.

```http
POST /indexes/my_content_understanding_index/docs/search?api-version=2026-05-01-preview
{
  "search": "copay for in-network providers",
  "count": true,
  "searchMode": "all",
  "vectorQueries": [
    {
      "kind": "text",
      "text": "copay for in-network providers",
      "fields": "text_vector"
    }
  ],
  "select": "chunk, title, page_number_from, page_number_to, image_path"
}
```

A successful response looks similar to the following (trimmed for brevity):

```json
{
  "@odata.count": 2,
  "value": [
    {
      "@search.score": 0.0317,
      "chunk": "## Cost sharing\n\nFor in-network providers, the copay is $20 per visit...\n\n![Chart: Copay comparison across plans](figures/3)",
      "title": "Northwind_Standard_Benefits_Details.pdf",
      "page_number_from": 4,
      "page_number_to": 4,
      "image_path": "figures/3"
    },
    {
      "@search.score": 0.0289,
      "chunk": "### Out-of-network providers\n\nWhen you visit a provider that isn't in the Northwind network, the copay is $40 per visit...",
      "title": "Northwind_Standard_Benefits_Details.pdf",
      "page_number_from": 5,
      "page_number_to": 6,
      "image_path": null
    }
  ]
}
```

The response includes:

+ `chunk`: The Markdown content of each chunk. When you configure `modelName` and `modelDeployment`, AI-generated image descriptions appear inline within the Markdown.
+ `page_number_from` and `page_number_to`: The page range that produced the chunk.
+ `image_path`: The path to the image extracted with the chunk or, when a chunk spans multiple images, a semicolon-separated list of paths. The exact shape depends on whether a knowledge store file projection is configured. Without a file projection, the path is the short form shown in the example (`figures/3`). With a file projection, the path is the relative path of the image in the knowledge store. To make these images available to client apps, see [(Optional) Project images for retrieval](#optional-project-images-for-retrieval).

## (Optional) Project images for retrieval

The `image_path` values stored in the index are pointers into the skill's enrichment tree, not directly retrievable URLs. To retrieve images, project `normalized_images` to Azure Blob Storage by using a knowledge store, and then derive a blob URL alongside each chunk.

This step is optional. Add it only if your client app needs to display or download the extracted images.

Add the following property to the skillset payload from the previous section. The skillset request uses `api-version=2026-05-01-preview`.

```json
"knowledgeStore": {
  "storageConnectionString": "<your-azure-storage-connection-string>",
  "projections": [
    {
      "files": [
        {
          "storageContainer": "extracted-images",
          "source": "/document/normalized_images/*"
        }
      ],
      "tables": [],
      "objects": []
    }
  ]
}
```

After the indexer runs, each blob in the `extracted-images` container corresponds to one `normalized_images` element. The blob URL has the form `https://<storage-account>.blob.core.windows.net/<container>/<imagePath>`, where `<imagePath>` matches the value stored in the `image_path` field.

For the full schema, including additional projection types (`tables` and `objects`) and authentication options, see [Knowledge store "projections" in Azure AI Search](knowledge-store-projection-overview.md).

## Clean up resources

When you're done, delete the indexer, skillset, and index to stop incurring Content Understanding and Azure OpenAI charges. Source files in Azure Blob Storage and the Foundry resource itself remain until you delete them.

## Troubleshooting

If the indexer fails or returns unexpected results, check the following common causes.

### Skillset validation fails with 400

The skill returns a `400 Skill validation failed` error when parameter combinations conflict. Common causes:

+ `modelName` is set without `modelDeployment`, or vice versa. Both must be set together.
+ `method` is `semantic` and `overlapLength` is greater than `0`. Set `overlapLength` to `0` or omit it.
+ `method` and `unit` aren't a supported pair. Use `fixedSize` with `characters` or `semantic` with `tokens`.

### Authorization fails against the Foundry resource

If the skill returns 401 or 403 when calling the Foundry resource, verify that:

+ The `cognitiveServices` block in the skillset points to the correct Foundry resource.
+ The identity used by the search service has the required role on the Foundry resource. For managed-identity setups, see [Attach a billable resource to a skillset in Azure AI Search](cognitive-search-attach-cognitive-services.md).

### `text_sections` is empty

If indexed documents have no chunks, verify that:

+ The file format is supported. For the list, see [Supported file formats](cognitive-search-skill-content-understanding.md#supported-file-formats).
+ The Foundry resource is in a supported region.
+ Password-protected PDFs are unlocked before indexing.

### Image descriptions are missing

If chunks don't include inline image descriptions, verify that:

+ Both `modelName` and `modelDeployment` are set in the skillset.
+ The chat completion model in `modelName` is deployed in the same Foundry resource referenced by the skillset.
+ The deployment has sufficient TPM or RPM quota for your document volume.

### Indexer times out on large documents

Content Understanding enforces a per-document processing timeout. If large PDFs fail:

+ Split the source document into smaller files before indexing.
+ Reduce `batchSize` to `1` so each document is processed independently.

For the full data limits of the Azure Content Understanding skill, see [Data limits](cognitive-search-skill-content-understanding.md#data-limits).

## Related content

+ [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md)
+ [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md)
+ [Multimodal search in Azure AI Search](multimodal-search-overview.md)
+ [Define an index projection for parent-child indexing](search-how-to-define-index-projections.md)
+ [Chunk large documents for RAG and vector search](vector-search-how-to-chunk-documents.md)
