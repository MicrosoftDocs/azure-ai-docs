---
title: Azure Content Understanding skill
titleSuffix: Azure AI Search
description: Learn how to analyze and chunk a document in an enrichment pipeline in Azure AI Search.
author: ruix
ms.author: ruix
ms.reviewer: haileytapia
ms.service: azure-ai-search
ms.custom:
  - references_regions
  - ignite-2025
ms.topic: reference
ms.date: 02/11/2026
ms.update-cycle: 365-days
---

# Azure Content Understanding skill

The **Azure Content Understanding** skill uses [document analyzers](/azure/ai-services/content-understanding/document/overview) from [Azure Content Understanding in Foundry Tools](/azure/ai-services/content-understanding/overview) to analyze unstructured documents and other content types, generating organized, searchable outputs that can be integrated into automation workloads. This skill extracts both text and images, including location metadata that preserves each image's position within the document. Image proximity to related content is especially useful for [multimodal search](multimodal-search-overview.md), [agentic retrieval](agentic-retrieval-overview.md), and [retrieval-augmented generation](retrieval-augmented-generation-overview.md) (RAG).

You can use the Azure Content Understanding skill for both content extraction and chunking. There's no need to use the Text Split skill in your skillset. This skill implements the same interface as the Document Layout skill, which uses the [Azure Document Intelligence in Foundry Tools layout model](/azure/ai-services/document-intelligence/concept-layout) when `outputFormat` is set to `text`. However, the Azure Content Understanding skill offers several advantages over the Document Layout skill:

+ Tables and figures are output in Markdown format, making them easier for large language models (LLMs) to understand. In contrast, the Document Layout skill outputs tables and figures as plain text, which can result in information loss.

+ For tables that span multiple pages, the Document Layout skill extracts tables page by page. The Azure Content Understanding skill can recognize and extract cross-page tables as a single unit.

+ The Document Layout skill restricts chunks to a single page, but semantic units, such as cross-page tables, shouldn't be limited by page boundaries. The Azure Content Understanding skill allows chunks to span multiple pages.

+ The Azure Content Understanding skill is more cost effective than the Document Layout skill because the Content Understanding API is less expensive.

The Azure Content Understanding skill is bound to a [billable Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md). Unlike other
Azure AI resource skills, such as the [Document Layout skill](/azure/search/cognitive-search-skill-document-intelligence-layout), the Azure Content Understanding skill doesn't provide 20 free documents per indexer per day. Execution of this skill is charged at the [Azure Content Understanding price](https://azure.microsoft.com/pricing/details/content-understanding/).

> [!TIP]
> You can use the Azure Content Understanding skill in a skillset that also performs image verbalization and chunk vectorization. In the following tutorials, replace the Document Layout skill with the Azure Content Understanding skill.
>
> + [Tutorial: Verbalize images from a structured document layout](tutorial-document-layout-image-verbalization.md)
> + [Tutorial: Vectorize from a structured document layout](tutorial-document-layout-multimodal-embeddings.md)

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
| `chunkingProperties` | See the following table. | Options that encapsulate how to chunk text content. |

| `chunkingProperties` parameters | Allowed values | Description |
|--------------------|-------------|-------------|
| `unit`    | `Characters` is the only allowed value. The chunk length is measured in characters rather than words or tokens. | Controls the cardinality of the chunk unit. |
| `maximumLength` | An integer between 300 and 50000. | The maximum chunk length in characters as measured by `String.Length`. |
| `overlapLength` | Integer. The value must be less than half of the `maximumLength`. | The length of overlap provided between two text chunks. |

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
| `text_sections` | A collection of text chunk objects. Each chunk can span multiple pages (factoring in any more chunking configured). The text chunk object includes `locationMetadata` if applicable.|
| `normalized_images` | Only applies if `extractionOptions` includes `images`. A collection of images that were extracted from the document, including `locationMetadata` if applicable. |

## Example

This example demonstrates how to output text content in fixed-sized chunks and extract images along with location metadata from the document.

### Sample definition that includes image and metadata extraction

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

## Related content

+ [What is Azure Content Understanding (preview)?](/azure/ai-services/content-understanding/overview)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [Create a skillset](cognitive-search-defining-skillset.md)
+ [Indexers - Create (REST API)](/rest/api/searchservice/indexers/create)
