---
title: Azure Content Understanding Skill
description: Learn how to analyze and chunk a document in an enrichment pipeline in Azure AI Search.
ms.reviewer: ruix
ms.service: azure-ai-search
ms.custom:
  - references_regions
  - ignite-2025
  - build-2026
ms.topic: reference
ms.date: 06/02/2026
ms.update-cycle: 365-days
ai-usage: ai-assisted
---

# Azure Content Understanding skill

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

The **Azure Content Understanding** skill uses [document analyzers](/azure/ai-services/content-understanding/document/overview) from [Azure Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/overview) to analyze unstructured documents and other content types, generating organized, searchable outputs that can be integrated into automation workloads. This skill extracts both text and images, including location metadata that preserves each image's position within the document. Image proximity to related content is especially useful for [multimodal search](multimodal-search-overview.md), [agentic retrieval](agentic-retrieval-overview.md), and [retrieval-augmented generation](retrieval-augmented-generation-overview.md) (RAG).

The Azure Content Understanding skill is bound to a [billable Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md). Unlike other Azure AI resource skills, such as the [Document Layout skill](/azure/search/cognitive-search-skill-document-intelligence-layout), the Azure Content Understanding skill doesn't provide 20 free documents per indexer per day. Execution of this skill is charged at the [Azure Content Understanding price](https://azure.microsoft.com/pricing/details/content-understanding/).

You can use the Azure Content Understanding skill for both content extraction and chunking. There's no need to use the Text Split skill in your skillset. This skill implements the same interface as the Document Layout skill, which uses the [Azure Document Intelligence in Foundry Tools layout model](/azure/ai-services/document-intelligence/concept-layout) when `outputFormat` is set to `text`. However, the Azure Content Understanding skill offers several advantages over the Document Layout skill:

+ Tables and figures are output in Markdown format, making them easier for large language models (LLMs) to understand. In contrast, the Document Layout skill outputs tables and figures as plain text, which can result in information loss.

+ For tables that span multiple pages, the Azure Content Understanding skill can recognize and extract cross-page tables as a single unit.

+ The Azure Content Understanding skill allows chunks to span multiple pages via semantic units.

+ The Azure Content Understanding skill is more cost effective than the Document Layout skill because the Content Understanding API is less expensive.

The Azure Content Understanding skill is generally available in the [`2026-04-01` REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true). Starting with the [`2026-05-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true), the skill optionally generates AI-based descriptions for document-embedded images, charts, and diagrams. To enable descriptions, you must deploy an Azure OpenAI chat completion model in the Foundry resource attached to the skillset. This API version also adds *semantic* chunking, a layout-aware option that respects paragraph boundaries and measures chunk length in tokens. Both capabilities require opt-in. When the new parameters are omitted, the skill behaves the same as in the stable `2026-04-01` API version.

## Limitations

The Azure Content Understanding skill has the following limitations:

+ This skill isn't suitable for large documents requiring more than five minutes of processing in the Content Understanding document analyzer. The skill times out, but charges still apply to the Foundry resource that's attached to the skillset. Ensure documents are optimized to stay within processing limits to avoid unnecessary costs.

+ This skill calls the Azure Content Understanding document analyzer, so all documented [service behaviors for different document types](/azure/ai-services/content-understanding/service-limits#document-and-text) apply to its output. For example, Word (DOCX) and PDF files might produce different results due to differences in how images are handled. If consistent image behavior across DOCX and PDF is required, consider converting documents to PDF or reviewing the [multimodal search documentation](multimodal-search-overview.md) for alternative approaches.

## Supported regions

The Azure Content Understanding skill calls the [Content Understanding 2025-11-01 REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2025-11-01&preserve-view=true). Your Foundry resource must be in a supported region, which is described in [Azure Content Understanding region and language support](/azure/ai-services/content-understanding/language-region-support).

Your search service can be in any [supported Azure AI Search region](search-region-support.md). When your Foundry resource and Azure AI Search service aren't in the same region, cross-region network latency impacts your indexer's performance.

## Supported file formats

The Azure Content Understanding skill recognizes the following file formats:

+ .PDF
+ .JPEG
+ .JPG
+ .PNG
+ .BMP
+ .HEIF
+ .TIFF
+ .DOCX
+ .XLSX
+ .PPTX
+ .HTML
+ .TXT
+ .MD
+ .RTF
+ .EML

## Supported languages

For printed text, see [Azure Content Understanding region and language support](/azure/ai-services/content-understanding/language-region-support#language-support).

## @odata.type

Microsoft.Skills.Util.ContentUnderstandingSkill

## Data limits

+ Even when the file size for analyzing documents is within the 200 MB limit, as described in the [Azure Content Understanding service quotas and limits](/azure/ai-services/content-understanding/service-limits), indexing is still subject to the [indexer limits](search-limits-quotas-capacity.md#indexer-limits) of your search service tier.

+ Image dimensions must be between 50 pixels x 50 pixels or 10,000 pixels x 10,000 pixels.

+ If your PDFs are password locked, remove the lock before you run the indexer.
  
## Skill parameters

Parameters are case sensitive.

| Parameter name | Allowed values | Description |
|--------------------|----------------|-------------|
| `extractionOptions` |`["images"]`, `["images", "locationMetadata"]`, `["locationMetadata"]` | Identify any extra content extracted from the document. Define an array of enums that correspond to the content to be included in the output. For example, if `extractionOptions` is `["images", "locationMetadata"]`, the output includes images and location metadata that provides page location and visual information related to where the content was extracted.  |
| `modelName` | String, such as `"gpt-4.1"`. | Optional. Available starting with the `2026-05-01-preview` REST API. The name of the Azure OpenAI chat completion model used to generate descriptions of embedded images, charts, and diagrams. Image description is independent of `extractionOptions` and can be enabled without extracting images. Must be specified together with `modelDeployment`. For a list of supported models, see [Supported generative models](/azure/ai-services/content-understanding/service-limits#supported-generative-models). |
| `modelDeployment` | String. | Optional. Available starting with the `2026-05-01-preview` REST API. The deployment name of the Azure OpenAI model in the Foundry resource that's attached to the skillset. Must be specified together with `modelName`. |
| `chunkingProperties` | See the following table. | Options that encapsulate how to chunk text content. |

| `chunkingProperties` parameters | Allowed values | Description |
|--------------------|-------------|-------------|
| `method` | `fixedSize` (default) or `semantic`. Available starting with the `2026-05-01-preview` REST API. | The chunking strategy. `fixedSize` uses character-based windowed chunking. `semantic` uses layout-aware chunking that respects paragraph boundaries and intelligently handles large tables that span chunk boundaries. |
| `unit` | `characters` (with `fixedSize`) or `tokens` (with `semantic`, available starting with the `2026-05-01-preview` REST API). | Controls the cardinality of the chunk unit. Only the `fixedSize` + `characters` and `semantic` + `tokens` combinations are supported. If `unit` is omitted, it's inferred from `method`. |
| `maximumLength` | When `unit` is `characters`, an integer between 300 and 50,000. When `unit` is `tokens`, an integer between 100 and 8,000. Default is 500. | The maximum chunk length, measured in the configured `unit`. |
| `overlapLength` | Integer. The value must be less than half of `maximumLength`. | The length of overlap between two text chunks. Applies only when `method` is `fixedSize`. Must be omitted or set to `0` when `method` is `semantic`. |


## Skill inputs

| Input name | Description |
|--------------------|-------------|
| `file_data` | The file from which content should be extracted. |

The `file_data` input must be an object defined as:

```json
{
  "$type": "file",
  "data": "BASE64 encoded string of the file"
}
```

Alternatively, it can be defined as:

```json
{
  "$type": "file",
  "url": "URL to download the file",
  "sasToken": "OPTIONAL: SAS token for authentication if the provided URL is for a file in blob storage"
}
```

The file reference object can be generated in one of following ways:

+ Setting the `allowSkillsetToReadFileData` parameter on your indexer definition to `true`. This setting creates a `/document/file_data` path that's an object representing the original file data downloaded from your blob data source. This parameter only applies to files in Azure Blob Storage.

+ Having a custom skill returning a JSON object definition that provides `$type`, `data`, or `url` and `sastoken`. The `$type` parameter must be set to `file`, and  `data` must be the base 64-encoded byte array of the file content. The `url` parameter must be a valid URL with access to download the file at that location.

## Skill outputs

| Output name | Description |
|---------------|-------------------------------|
| `text_sections` | A collection of text chunk objects. Each chunk can span multiple pages (factoring in any more chunking configured). The text chunk object includes `locationMetadata` if applicable, and an `imagePath` list when the chunk overlaps with figure spans in the document. |
| `normalized_images` | Only applies if `extractionOptions` includes `images`. A collection of images that were extracted from the document, including `locationMetadata` if applicable. |

Each element in `text_sections` has the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | String | Unique identifier for the chunk. |
| `content` | String | Markdown content for the chunk. When `method` is `semantic`, the content includes AI-generated descriptions of figures and tables inlined as Markdown. |
| `locationMetadata` | Object | Page range and positional data (`pageNumberFrom`, `pageNumberTo`, `ordinalPosition`, `source`). Present when `extractionOptions` includes `locationMetadata`. |
| `imagePath` | String | Semicolon-separated list of paths to images that are contained in the chunk. Present when the chunk overlaps with figure spans in the document. |

Each element in `normalized_images` has the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | String | Unique identifier for the image. |
| `data` | String | Base64-encoded image data. |
| `imagePath` | String | Path reference to the image within the document, such as `"figures/0"`. |
| `locationMetadata` | Object | Page range and positional data. Present when `extractionOptions` includes `locationMetadata`. |

## Examples

The first example uses fixed-size chunking and demonstrates how to output text content in fixed-sized chunks and extract images along with location metadata from the document. The second example, available starting with the `2026-05-01-preview` REST API, uses semantic chunking with AI-generated image descriptions.

### Example 1: Fixed-size chunking with image and metadata extraction

```json
{
  "skills": [
    {
      "description": "Analyze a document",
      "@odata.type": "#Microsoft.Skills.Util.ContentUnderstandingSkill",
      "context": "/document",
      "extractionOptions": ["images", "locationMetadata"],
      "chunkingProperties": {     
          "unit": "characters",
          "maximumLength": 1325, 
          "overlapLength": 0
      },
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
    }
  ]
}
```

### Sample output

```json
{
  "text_sections": [
      {
        "id": "1_d4545398-8df1-409f-acbb-f605d851ae85",
        "content": "What is Azure Content Understanding (preview)?09/16/2025Important· Azure Al Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.· Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).. For more information, see Supplemental Terms of Use for Microsoft Azure PreviewsAzure Content Understanding is a Foundry Tool that uses generative AI to process/ingest content of many types (documents, images, videos, and audio) into a user-defined output format.Content Understanding offers a streamlined process to reason over large amounts of unstructured data, accelerating time-to-value by generating an output that can be integrated into automation and analytical workflows.<figure>\n\nInputs\n\nAnalyzers\n\nOutput\n\n0\nSearch\n\nContent Extraction\n\nField Extraction\n\nDocuments\n\nNew\n\nAgents\n\nPreprocessing\n\nEnrichments\n\nReasoning\n\nImage\n\nNormalization\n(resolution,\nformats)\n\nSpeaker\nrecognition\n\nGen Al\nContext\nwindows\n\nPostprocessing\nConfidence\nscores\nGrounding\nNormalization\n\nMulti-file input\nReference data\n\nDatabases\n\nVideo\n\nOrientation /\nde-skew\n\nLayout and\nstructure\n\nPrompt tuning\n\nStructured\noutput\n\nAudio\n\nFace grouping\n\nMarkdown or JSON schema\n\nCopilots\n\nApps\n\n\\+\n\nFaurIC\n\n</figure>",
        "locationMetadata": {
          "pageNumberFrom": 1,
          "pageNumberTo": 1,
          "ordinalPosition": 0,
          "source": "D(1,0.6348,0.3598,7.2258,0.3805,7.223,1.2662,0.632,1.2455);D(1,0.6334,1.3758,1.3896,1.3738,1.39,1.5401,0.6338,1.542);D(1,0.8104,2.0716,1.8137,2.0692,1.8142,2.2669,0.8109,2.2693);D(1,1.0228,2.5023,7.6222,2.5029,7.6221,3.0075,1.0228,3.0069);D(1,1.0216,3.1121,7.3414,3.1057,7.342,3.6101,1.0221,3.6165);D(1,1.0219,3.7145,7.436,3.7048,7.4362,3.9006,1.0222,3.9103);D(1,0.6303,4.3295,7.7875,4.3236,7.7879,4.812,0.6307,4.8179);D(1,0.6304,5.0295,7.8065,5.0303,7.8064,5.7858,0.6303,5.7849);D(1,0.635,5.9572,7.8544,5.9573,7.8562,8.6971,0.6363,8.6968);D(1,0.6381,9.1451,5.2731,9.1476,5.2729,9.4829,0.6379,9.4803)"
        }
      },
      ...
      {
        "id": "2_e0e57fd4-e835-4879-8532-73a415e47b0b",
        "content": "<table>\n<tr>\n<th>Application</th>\n<th>Description</th>\n</tr>\n<tr>\n<td>Post-call analytics</td>\n<td>Businesses and call centers can generate insights from call recordings to track key KPIs, improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.</td>\n</tr>\n<tr>\n<th>Application</th>\n<th>Description</th>\n</tr>\n<tr>\n<td>Media asset management</td>\n<td>Software and media vendors can use Content Understanding to extract richer, targeted information from videos for media asset management solutions.</td>\n</tr>\n<tr>\n<td>Tax automation</td>\n<td>Tax preparation companies can use Content Understanding to generate a unified view of information from various documents and create comprehensive tax returns.</td>\n</tr>\n<tr>\n<td>Chart understanding</td>\n<td>Businesses can enhance chart understanding by automating the analysis and interpretation of various types of charts and diagrams using Content Understanding.</td>\n</tr>\n<tr>\n<td>Mortgage application processing</td>\n<td>Analyze supplementary supporting documentation and mortgage applications to determine whether a prospective home buyer provided all the necessary documentation to secure a mortgage.</td>\n</tr>\n<tr>\n<td>Invoice contract verification</td>\n<td>Review invoices and contr",
        "locationMetadata": {
          "pageNumberFrom": 2,
          "pageNumberTo": 3,
          "ordinalPosition": 3,
          "source": "D(2,0.6438,9.2645,7.8576,9.2649,7.8565,10.5199,0.6434,10.5194);D(3,0.6494,0.3919,7.8649,0.3929,7.8639,4.3254,0.6485,4.3232)"
        }
        ...
      }
    ],
    "normalized_images": [
        { 
            "id": "1_335140f1-9d31-4507-8916-2cde758639cb", 
            "data": "aW1hZ2UgMSBkYXRh", 
            "imagePath": "aHR0cHM6Ly9henNyb2xsaW5nLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tdWx0aW1vZGFsaXR5L0NVLnBkZg2/normalized_images_0.jpg",  
            "locationMetadata": {
              "pageNumberFrom": 1,
              "pageNumberTo": 1,
              "ordinalPosition": 0,
              "source": "D(1,0.635,5.9572,7.8544,5.9573,7.8562,8.6971,0.6363,8.6968)"
            }
        },
        { 
            "id": "3_699d33ac-1a1b-4015-9cbd-eb8bfff2e6b4", 
            "data": "aW1hZ2UgMiBkYXRh", 
            "imagePath": "aHR0cHM6Ly9henNyb2xsaW5nLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tdWx0aW1vZGFsaXR5L0NVLnBkZg2/normalized_images_1.jpg",  
            "locationMetadata": {
              "pageNumberFrom": 3,
              "pageNumberTo": 3,
              "ordinalPosition": 1,
              "source": "D(3,0.6353,5.2142,7.8428,5.218,7.8443,8.4631,0.6363,8.4594)"
            } 
        }
    ] 
}
```

`locationMetadata` is based on the `source` property provided by Azure Content Understanding. For information about how visual position of the element in the file is encoded, see [Document analysis: Extract structured content](/azure/ai-services/content-understanding/document/elements#source).

`imagePath` represents the relative path of a stored image. If the knowledge store file projection is configured in the skillset, this path matches the relative path of the image stored in the knowledge store.

### Example 2: Semantic chunking with image description

This example, available starting with the `2026-05-01-preview` REST API, uses semantic chunking and produces AI-generated descriptions of embedded images, charts, and diagrams. The Foundry resource attached to the skillset must have the chat completion model identified by `modelName` and the deployed `modelDeployment`.

```json
{
  "skills": [
    {
      "description": "Extract and chunk document content with image descriptions",
      "@odata.type": "#Microsoft.Skills.Util.ContentUnderstandingSkill",
      "context": "/document",
      "modelName": "gpt-4.1",
      "modelDeployment": "myGpt41Deployment",
      "extractionOptions": ["images", "locationMetadata"],
      "chunkingProperties": {
        "method": "semantic",
        "unit": "tokens",
        "maximumLength": 500
      },
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
    }
  ]
}
```

With semantic chunking, each chunk in `text_sections` contains Markdown content that includes AI-generated descriptions of any figures and tables it covers. When a chunk overlaps with one or more figure spans, the chunk object also includes an `imagePath` field that lists the corresponding image paths:

```json
{
  "id": "1_d4545398-8df1-409f-acbb-f605d851ae85",
  "content": "# Architecture overview\n\nThe following diagram summarizes the ingestion pipeline...\n\n<figure>The diagram shows three stages: Inputs, Analyzers, and Output. Inputs include documents, images, video, and audio. Analyzers perform preprocessing, enrichments, and reasoning. Output is structured Markdown or JSON consumed by search, agents, copilots, and apps.</figure>",
  "locationMetadata": {
    "pageNumberFrom": 1,
    "pageNumberTo": 1,
    "ordinalPosition": 0,
    "source": "D(1,0.6348,0.3598,7.2258,0.3805,7.223,1.2662,0.632,1.2455)"
  },
  "imagePath": "aHR0cHM6Ly9henNyb2xsaW5nLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tdWx0aW1vZGFsaXR5L0NVLnBkZg2/normalized_images_0.jpg"
}
```

## Related content

+ [What is Azure Content Understanding in Foundry Tools?](/azure/ai-services/content-understanding/overview)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [Create a skillset](cognitive-search-defining-skillset.md)
+ [Indexers - Create](/rest/api/searchservice/indexers/create) (REST API)
