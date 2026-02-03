---
title: Document Layout Skill
titleSuffix: Azure AI Search
description: Analyze a document to extract regions of interest and their inter-relationships to produce a syntactical representation (markdown format) in an enrichment pipeline in Azure AI Search.
author: rawan
ms.author: rawan
ms.service: azure-ai-search
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: reference
ms.date: 01/16/2026
ms.update-cycle: 365-days
---

# Document Layout skill

The **Document Layout** skill uses the [layout model](/azure/ai-services/document-intelligence/concept-layout) from Azure Document Intelligence in Foundry Tools to analyze a document, detect its structure and characteristics, and produce a syntactical representation in Markdown or text format. This skill supports text and image extraction, the latter of which includes location metadata that preserves image position within a document. Image proximity to related content is beneficial in retrieval-augmented generation (RAG) and [multimodal search](multimodal-search-overview.md) scenarios.

For transactions that exceed 20 documents per indexer per day, this skill requires you to [attach a billable Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) to your skillset. Execution of built-in skills is charged at the existing [Foundry Tools Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/).

This article is the reference documentation for the Document Layout skill. For usage information, see [How to chunk and vectorize by document layout](search-how-to-semantic-chunking.md).

> [!TIP]
> It's common to use this skill on content that has structure and images, such as PDFs. The following tutorials demonstrate image verbalization with two different data chunking techniques:
>
> - [Tutorial: Verbalize images from a structured document layout](tutorial-document-layout-image-verbalization.md)
> - [Tutorial: Vectorize from a structured document layout](tutorial-document-layout-multimodal-embeddings.md)

## Limitations

This skill has the following limitations:

+ The skill isn't suitable for large documents requiring more than five minutes of processing in the Azure Document Intelligence layout model. The skill times out, but charges still apply to the Foundry resource if it's attached to the skillset for billing purposes. Ensure documents are optimized to stay within processing limits to avoid unnecessary costs.

+ Because this skill calls the Azure Document Intelligence layout model, all documented [service behaviors for different document types](/azure/ai-services/document-intelligence/prebuilt/layout#pages) for different file types apply to its output. For example, Word (DOCX) and PDF files may produce different results due to differences in how images are handled. If consistent image behavior across DOCX and PDF is required, consider converting documents to PDF or reviewing the [multimodal search documentation](multimodal-search-overview.md) for alternative approaches.

## Supported regions

The Document Layout skill calls v4.0 (2024-11-30) of the [Azure Document Intelligence REST API](/rest/api/aiservices/operation-groups).

Supported regions vary by modality and how the skill connects to the Azure Document Intelligence layout model. Currently, the implemented version of the layout model doesn't support [21Vianet](/azure/china/overview-operations) regions.

| Approach | Requirement |
|----------|-------------|
| [**Import data (new)** wizard](search-import-data-portal.md) | Create an Azure AI Search service and [Azure AI multi-service account](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) in one of the following regions: East US, West Europe, or North Central US. | 
| Programmatic, using a [Microsoft Foundry resource key](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) for billing | Create an Azure AI Search service and Microsoft Foundry resource in the same region. The region must support both [Azure AI Search and Azure Document Intelligence](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table). |
| Programmatic, using [Microsoft Entra ID authentication (preview)](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) for billing | No same-region requirement. Create an Azure AI Search service and Microsoft Foundry resource in any region where [each service is available](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table). |

## Supported file formats

This skill recognizes the following file formats:

+ .PDF
+ .JPEG
+ .JPG
+ .PNG
+ .BMP
+ .TIFF
+ .DOCX
+ .XLSX
+ .PPTX
+ .HTML

## Supported languages

For printed text, see [Azure Document Intelligence layout model supported languages](/azure/ai-services/document-intelligence/language-support/ocr?view=doc-intel-3.1.0&tabs=read-print%2Clayout-print%2Cgeneral#layout&preserve-view=true).

## @odata.type

Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill

## Data limits

+ For PDF and TIFF, up to 2,000 pages can be processed (with a free tier subscription, only the first two pages are processed).
+ Even if the file size for analyzing documents is 500 MB for [Azure Document Intelligence paid (S0) tier](https://azure.microsoft.com/pricing/details/cognitive-services/) and 4 MB for [Azure Document Intelligence free (F0) tier](https://azure.microsoft.com/pricing/details/cognitive-services/), indexing is subject to the [indexer limits](search-limits-quotas-capacity.md#indexer-limits) of your search service tier.
+ Image dimensions must be between 50 pixels x 50 pixels or 10,000 pixels x 10,000 pixels.
+ If your PDFs are password-locked, remove the lock before running the indexer.
  
## Skill parameters

Parameters are case sensitive. Several parameters were introduced in specific preview versions of the REST API. We recommend using the generally available version (2025-09-01) or the latest preview (2025-11-01-preview) for full access to all parameters.

| Parameter name     | Allowed Values | Description |
|--------------------|----------------|-------------|
| `outputMode`    |`oneToMany` | Controls the cardinality of the output produced by the skill. |
| `markdownHeaderDepth` |`h1`, `h2`, `h3`, `h4`, `h5`, `h6(default)` | Only applies if `outputFormat` is set to `markdown`. This parameter describes the deepest nesting level that should be considered. For instance, if the markdownHeaderDepth is `h3`, any sections that are deeper such as `h4`, are rolled into `h3`. |
| `outputFormat`    |`markdown(default)`, `text` | **New**. Controls the format of the output generated by the skill. |
| `extractionOptions`    |`["images"]`, `["images", "locationMetadata"]`, `["locationMetadata"]` | **New**. Identify any extra content extracted from the document. Define an array of enums that correspond to the content to be included in the output. For instance, if the `extractionOptions` is `["images", "locationMetadata"]`, the output includes images and location metadata which provides page location information related to where the content was extracted, such as a page number or section. This parameter applies to both output formats.  |
| `chunkingProperties` | See below. | **New**. Only applies if `outputFormat` is set to `text`. Options that encapsulate how to chunk text content while recomputing other metadata. |

| ChunkingProperties Parameter     | Version | Allowed Values | Description |
|--------------------|-------------|-------------|-------------|
| `unit`    | `Characters`. currently the only allowed value. Chunk length is measured in characters, as opposed to words or tokens | **New**. Controls the cardinality of the chunk unit. |
| `maximumLength`    | Any integer between 300-50000 | **New**. The maximum chunk length in characters as measured by String.Length. |
| `overlapLength`    | Integer. The value needs to be less than the half of the `maximumLength` | **New**. The length of overlap provided between two text chunks. |

## Skill inputs

| Input name | Description |
|--------------------|-------------|
| `file_data` | The file that content should be extracted from. |

The "file_data" input must be an object defined as:

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
  "url": "URL to download file",
  "sasToken": "OPTIONAL: SAS token for authentication if the URL provided is for a file in blob storage"
}
```

The file reference object can be generated in one of following ways:

+ Setting the `allowSkillsetToReadFileData` parameter on your indexer definition to true. This setting creates a path `/document/file_data` that's an object representing the original file data downloaded from your blob data source. This parameter only applies to files in Azure Blob storage.

+ Having a custom skill returning a JSON object definition that provides `$type`, `data`, or `url` and `sastoken`. The `$type` parameter must be set to `file`, and  `data` must be the base 64-encoded byte array of the file content. The `url` parameter must be a valid URL with access for downloading the file at that location.

## Skill outputs

| Output name      | Description                   |
|---------------|-------------------------------|
| `markdown_document`    | Only applies if `outputFormat` is set to `markdown`. A collection of "sections" objects, which represent each individual section in the Markdown document.|
| `text_sections`    | Only applies if `outputFormat` is set to `text`. A collection of text chunk objects, which represent the text within the bounds of a page (factoring in any more chunking configured), *inclusive* of any section headers themselves. The text chunk object includes `locationMetadata` if applicable.|
| `normalized_images`    | Only applies if `outputFormat` is set to `text` and `extractionOptions` includes `images`. A collection of images that were extracted from the document, including `locationMetadata` if applicable.|

### Sample definition for markdown output mode

```json
{
  "skills": [
    {
      "description": "Analyze a document",
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "context": "/document",
      "outputMode": "oneToMany", 
      "markdownHeaderDepth": "h3", 
      "inputs": [
        {
          "name": "file_data",
          "source": "/document/file_data"
        }
      ],
      "outputs": [
        {
          "name": "markdown_document", 
          "targetName": "markdown_document" 
        }
      ]
    }
  ]
}
```

### Sample output for markdown output mode

```json
{
  "markdown_document": [
    { 
      "content": "Hi this is Jim \r\nHi this is Joe", 
      "sections": { 
        "h1": "Foo", 
        "h2": "Bar", 
        "h3": "" 
      },
      "ordinal_position": 0
    }, 
    { 
      "content": "Hi this is Lance",
      "sections": { 
         "h1": "Foo", 
         "h2": "Bar", 
         "h3": "Boo" 
      },
      "ordinal_position": 1,
    } 
  ] 
}
```

The value of the `markdownHeaderDepth` controls the number of keys in the "sections" dictionary. In the example skill definition, since the `markdownHeaderDepth` is "h3," there are three keys in the "sections" dictionary: h1, h2, h3.

## Example for text output mode and image and metadata extraction

This example demonstrates how to output text content in fixed-sized chunks and extract images along with location metadata from the document.

### Sample definition for text output mode and image and metadata extraction

```json
{
  "skills": [
    {
      "description": "Analyze a document",
      "@odata.type": "#Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill",
      "context": "/document",
      "outputMode": "oneToMany",
      "outputFormat": "text",
      "extractionOptions": ["images", "locationMetadata"],
      "chunkingProperties": {     
          "unit": "characters",
          "maximumLength": 2000, 
          "overlapLength": 200
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

### Sample output for text output mode and image and metadata extraction

```json
{
  "text_sections": [
      {
        "id": "1_7e6ef1f0-d2c0-479c-b11c-5d3c0fc88f56",
        "content": "the effects of analyzers using Analyze Text (REST). For more information about analyzers, see Analyzers for text processing.During indexing, an indexer only checks field names and types. There's no validation step that ensures incoming content is correct for the corresponding search field in the index.Create an indexerWhen you're ready to create an indexer on a remote search service, you need a search client. A search client can be the Azure portal, a REST client, or code that instantiates an indexer client. We recommend the Azure portal or REST APIs for early development and proof-of-concept testing.Azure portal1. Sign in to the Azure portal 2, then find your search service.2. On the search service Overview page, choose from two options:· Import data wizard: The wizard is unique in that it creates all of the required elements. Other approaches require a predefined data source and index.All services > Azure Al services | Al Search >demo-search-svc Search serviceSearchAdd indexImport dataImport and vectorize dataOverviewActivity logEssentialsAccess control (IAM)Get startedPropertiesUsageMonitoring· Add indexer: A visual editor for specifying an indexer definition.",
        "locationMetadata": {
          "pageNumber": 1,
          "ordinalPosition": 0,
          "boundingPolygons": "[[{\"x\":1.5548,\"y\":0.4036},{\"x\":6.9691,\"y\":0.4033},{\"x\":6.9691,\"y\":0.8577},{\"x\":1.5548,\"y\":0.8581}],[{\"x\":1.181,\"y\":1.0627},{\"x\":7.1393,\"y\":1.0626},{\"x\":7.1393,\"y\":1.7363},{\"x\":1.181,\"y\":1.7365}],[{\"x\":1.1923,\"y\":2.1466},{\"x\":3.4585,\"y\":2.1496},{\"x\":3.4582,\"y\":2.4251},{\"x\":1.1919,\"y\":2.4221}],[{\"x\":1.1813,\"y\":2.6518},{\"x\":7.2464,\"y\":2.6375},{\"x\":7.2486,\"y\":3.5913},{\"x\":1.1835,\"y\":3.6056}],[{\"x\":1.3349,\"y\":3.9489},{\"x\":2.1237,\"y\":3.9508},{\"x\":2.1233,\"y\":4.1128},{\"x\":1.3346,\"y\":4.111}],[{\"x\":1.5705,\"y\":4.5322},{\"x\":5.801,\"y\":4.5326},{\"x\":5.801,\"y\":4.7311},{\"x\":1.5704,\"y\":4.7307}]]"
        },
        "sections": []
      },
      {
        "id": "2_25134f52-04c3-415a-ab3d-80729bd58e67",
        "content": "All services > Azure Al services | Al Search >demo-search-svc | Indexers Search serviceSearch0«Add indexerRefreshDelete:selected: TagsFilter by name ...:selected: Diagnose and solve problemsSearch managementStatusNameIndexesIndexers*Data sourcesRun the indexerBy default, an indexer runs immediately when you create it on the search service. You can override this behavior by setting disabled to true in the indexer definition. Indexer execution is the moment of truth where you find out if there are problems with connections, field mappings, or skillset construction.There are several ways to run an indexer:· Run on indexer creation or update (default).. Run on demand when there are no changes to the definition, or precede with reset for full indexing. For more information, see Run or reset indexers.· Schedule indexer processing to invoke execution at regular intervals.Scheduled execution is usually implemented when you have a need for incremental indexing so that you can pick up the latest changes. As such, scheduling has a dependency on change detection.Indexers are one of the few subsystems that make overt outbound calls to other Azure resources. In terms of Azure roles, indexers don't have separate identities; a connection from the search engine to another Azure resource is made using the system or user- assigned managed identity of a search service. If the indexer connects to an Azure resource on a virtual network, you should create a shared private link for that connection. For more information about secure connections, see Security in Azure Al Search.Check results",
        "locationMetadata": {
          "pageNumber": 2,
          "ordinalPosition": 1,
          "boundingPolygons": "[[{\"x\":2.2041,\"y\":0.4109},{\"x\":4.3967,\"y\":0.4131},{\"x\":4.3966,\"y\":0.5505},{\"x\":2.204,\"y\":0.5482}],[{\"x\":2.5042,\"y\":0.6422},{\"x\":4.8539,\"y\":0.6506},{\"x\":4.8527,\"y\":0.993},{\"x\":2.5029,\"y\":0.9845}],[{\"x\":2.3705,\"y\":1.1496},{\"x\":2.6859,\"y\":1.15},{\"x\":2.6858,\"y\":1.2612},{\"x\":2.3704,\"y\":1.2608}],[{\"x\":3.7418,\"y\":1.1709},{\"x\":3.8082,\"y\":1.171},{\"x\":3.8081,\"y\":1.2508},{\"x\":3.7417,\"y\":1.2507}],[{\"x\":3.9692,\"y\":1.1445},{\"x\":4.0541,\"y\":1.1445},{\"x\":4.0542,\"y\":1.2621},{\"x\":3.9692,\"y\":1.2622}],[{\"x\":4.5326,\"y\":1.2263},{\"x\":5.1065,\"y\":1.229},{\"x\":5.106,\"y\":1.346},{\"x\":4.5321,\"y\":1.3433}],[{\"x\":5.5508,\"y\":1.2267},{\"x\":5.8992,\"y\":1.2268},{\"x\":5.8991,\"y\":1.3408},{\"x\":5.5508,\"y\":1.3408}]]"
        },
        "sections": []
       }
    ],
    "normalized_images": [ 
        { 
            "id": "1_550e8400-e29b-41d4-a716-446655440000", 
            "data": "SGVsbG8sIFdvcmxkIQ==", 
            "imagePath": "aHR0cHM6Ly9henNyb2xsaW5nLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tdWx0aW1vZGFsaXR5L0NyZWF0ZUluZGV4ZXJwNnA3LnBkZg2/normalized_images_0.jpg",  
            "locationMetadata": {
              "pageNumber": 1,
              "ordinalPosition": 0,
              "boundingPolygons": "[[{\"x\":2.0834,\"y\":6.2245},{\"x\":7.1818,\"y\":6.2244},{\"x\":7.1816,\"y\":7.9375},{\"x\":2.0831,\"y\":7.9377}]]"
            }
        },
        { 
            "id": "2_123e4567-e89b-12d3-a456-426614174000", 
            "data": "U29tZSBtb3JlIGV4YW1wbGUgdGV4dA==", 
            "imagePath": "aHR0cHM6Ly9henNyb2xsaW5nLmJsb2IuY29yZS53aW5kb3dzLm5ldC9tdWx0aW1vZGFsaXR5L0NyZWF0ZUluZGV4ZXJwNnA3LnBkZg2/normalized_images_1.jpg",  
            "locationMetadata": {
              "pageNumber": 2,
              "ordinalPosition": 1,
              "boundingPolygons": "[[{\"x\":2.0784,\"y\":0.3734},{\"x\":7.1837,\"y\":0.3729},{\"x\":7.183,\"y\":2.8611},{\"x\":2.0775,\"y\":2.8615}]]"
            } 
        }
    ] 
}
```
Note that the `“sections”` in the sample output above appear blank. To populate them, you’ll need to add an additional skill configured with `outputFormat` set to `markdown`to ensure the sections are properly filled.

The skill uses [Azure Document Intelligence](/azure/ai-services/document-intelligence/overview) to compute locationMetadata. Refer to [Azure Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout) for details on how pages and bounding polygon coordinates are defined.

The `imagePath` represents the relative path of a stored image. If the knowledge store file projection is configured in the skillset, this path matches the relative path of the image stored in the knowledge store.

## See also

+ [What is the Azure Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skill set](cognitive-search-defining-skillset.md)
+ [Create Indexer (REST API)](/rest/api/searchservice/indexers/create)
