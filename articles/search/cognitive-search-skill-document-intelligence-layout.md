---
title: Document Layout skill
titleSuffix: Azure AI Search
description: Analyze a document to extract regions of interest and their inter-relationships to produce a syntactical representation (markdown format) in an enrichment pipeline in Azure AI Search.

author: rawan
ms.author: rawan

ms.service: azure-ai-search
ms.custom:
  - references_regions
  - ignite-2024
ms.topic: reference
ms.date: 05/08/2025
---

# Document Layout skill

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The **Document Layout** skill analyzes a document to extract regions of interest and their inter-relationships to produce a syntactical representation of the document in Markdown or Text format. This skill uses the [Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout) provided in [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview). 

This article is the reference documentation for the Document Layout skill. For usage information, see [Structure-aware chunking and vectorization](search-how-to-semantic-chunking.md).

The **Document Layout** skill calls the [Document Intelligence Public preview version 2024-07-31-preview](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true). 

Supported regions vary by modality:

+ When you're using AI services keys [to attach your multi-service resource to your skillset](cognitive-search-attach-cognitive-services.md#bill-through-a-resource-key) via the REST API, both your Azure AI Search service and AI multi-service resource must be in the same region. This is only possible in the Azure regions of **East US**, **West Europe**, **North Central US**, **West US 2**. But if you're using a managed identity for [billing through a keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection), your Azure AI Search service must be in one of the following regions: **East US**, **West Europe**, **North Central US**, **West US 2**. On the other hand, you can use AI Document Intelligence through an Azure AI multi-service resource in any region where this service is available. See [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table).

+ In the [Quickstart wizard](search-import-data-portal.md) in the Azure portal, you can enable document layout detection in the data source connection step. Document layout detection in the portal is available in the following Azure regions: **East US**, **West Europe**, **North Central US**. Create an Azure AI multi-service resource in one of these three regions to get the portal experience.

Supported file formats include:

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

Several parameters are version-specific. The skills parameter table notes the API version in which a parameter was introduced so that you know whether a version upgrade is required. To use version-specific features such as image and location metadata extraction in **2025-05-01-preview**, you can use the Azure portal, or target a REST API version, or check an Azure SDK change log to see if it supports the feature.

The Azure portal supports most preview features and can be used to create or update a skillset. For updates to the Document Layout skill, edit the skillset JSON definition to add new preview parameters.

> [!NOTE]
> This skill is bound to Azure AI services and requires [a billable resource](cognitive-search-attach-cognitive-services.md) for transactions that exceed 20 documents per indexer per day. Execution of built-in skills is charged at the existing [Azure AI services pay-as-you go price](https://azure.microsoft.com/pricing/details/cognitive-services/).
>

## @odata.type

Microsoft.Skills.Util.DocumentIntelligenceLayoutSkill

## Data limits

+ For PDF and TIFF, up to 2,000 pages can be processed (with a free tier subscription, only the first two pages are processed).
+ Even if the file size for analyzing documents is 500 MB for [Azure AI Document Intelligence paid (S0) tier](https://azure.microsoft.com/pricing/details/cognitive-services/) and 4 MB for [Azure AI Document Intelligence free (F0) tier](https://azure.microsoft.com/pricing/details/cognitive-services/), indexing is subject to the [indexer limits](search-limits-quotas-capacity.md#indexer-limits) of your search service tier.
+ Image dimensions must be between 50 pixels x 50 pixels or 10,000 pixels x 10,000 pixels.
+ If your PDFs are password-locked, remove the lock before running the indexer.

## Supported languages

Refer to [Azure AI Document Intelligence layout model supported languages](/azure/ai-services/document-intelligence/language-support/ocr?view=doc-intel-3.1.0&tabs=read-print%2Clayout-print%2Cgeneral#layout&preserve-view=true) for printed text.

## Limitations

During the public preview, this skill has the following restrictions:

+ The skill isn't suitable for large documents requiring more than 5 minutes of processing in the AI Document Intelligence layout model. The skill times out, but charges still apply to the AI Services multi-services resource if it attaches to the skillset for billing purposes. Ensure documents are optimized to stay within processing limits to avoid unnecessary costs.

  
## Skill parameters

Parameters are case-sensitive.

| Parameter name     | Version | Allowed Values | Description |
|--------------------|-------------|-------------|-------------|
| `outputMode`    | [2024-11-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true) |`oneToMany` | Controls the cardinality of the output produced by the skill. |
| `markdownHeaderDepth` | [2024-11-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true) |`h1`, `h2`, `h3`, `h4`, `h5`, `h6(default)` | Only applies if `outputFormat` is set to `markdown`. This parameter describes the deepest nesting level that should be considered. For instance, if the markdownHeaderDepth is `h3`, any sections that are deeper such as `h4`, are rolled into `h3`. |
| `outputFormat`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) |`markdown(default)`, `text` | **New**. Controls the format of the output generated by the skill. |
| `extractionOptions`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) |`["images"]`, `["images", "locationMetadata"]`, `["locationMetadata"]` | **New**. Identify any extra content extracted from the document. Define an array of enums that correspond to the content to be included in the output. For instance, if the extractionOptions is `["images", "locationMetadata"]`, the output includes images and location metadata which provides page location information related to where the content was extracted, such as a page number or section. This parameter applies to both output formats.  |
| `chunkingProperties`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) | See below | **New**. Only applies if `outputFormat` is set to `text`. Options that encapsulate how to chunk text content while recomputing other metadata. |

| ChunkingProperties Parameter     | Version | Allowed Values | Description |
|--------------------|-------------|-------------|-------------|
| `unit`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) |`Characters`. currently the only allowed value. Chunk length is measured in characters, as opposed to words or tokens | Controls the cardinality of the chunk unit. |
| `maximumLength`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) | Any integer between 300-50000 | The maximum chunk length in characters as measured by String.Length. |
| `overlapLength`    | [2025-05-01-preview](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) | Integer. The value needs to be less than the half of the `maximumLength` | The length of overlap provided between two text chunks. |

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

+ Having a custom skill returning a JSON object defined that provides `$type`, `data`, or `url` and `sastoken`. The `$type` parameter must be set to `file`, and  `data` must be the base 64-encoded byte array of the file content. The `url` parameter must be a valid URL with access for downloading the file at that location.

## Skill outputs

| Output name      | Description                   |
|---------------|-------------------------------|
| `markdown_document`    | Only applies if `outputFormat` is set to `markdown`. A collection of "sections" objects, which represent each individual section in the Markdown document.|
| `text_sections`    | Only applies if `outputFormat` is set to `text`. A collection of text chunk objects, which represent the text within the bounds of a page (factoring in any more chunking configured), *inclusive* of any section headers themselves. The text chunk object includes locationMetadata if required.|
| `normalized_images`    | Only applies if `outputFormat` is set to `text` and `extractionOptions` includes `images`.A collection of images that were extracted from the document, including locationMetadata if required.|

## Sample definition for markdown output mode
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

## Sample output for markdown output mode

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

This example demonstrates how to use the new parameters introduced in the **2025-05-01-preview** to output text content in fixed-sized chunks and extract images along with location metadata from the document.

## Sample definition for text output mode and image and metadata extraction

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

## Sample output for text output mode and image and metadata extraction

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
        "sections": ["sectionHeading"]
      },
      {
        "id": "2_25134f52-04c3-415a-ab3d-80729bd58e67",
        "content": "All services > Azure Al services | Al Search >demo-search-svc | Indexers Search serviceSearch0«Add indexerRefreshDelete:selected: TagsFilter by name ...:selected: Diagnose and solve problemsSearch managementStatusNameIndexesIndexers*Data sourcesRun the indexerBy default, an indexer runs immediately when you create it on the search service. You can override this behavior by setting disabled to true in the indexer definition. Indexer execution is the moment of truth where you find out if there are problems with connections, field mappings, or skillset construction.There are several ways to run an indexer:· Run on indexer creation or update (default).. Run on demand when there are no changes to the definition, or precede with reset for full indexing. For more information, see Run or reset indexers.· Schedule indexer processing to invoke execution at regular intervals.Scheduled execution is usually implemented when you have a need for incremental indexing so that you can pick up the latest changes. As such, scheduling has a dependency on change detection.Indexers are one of the few subsystems that make overt outbound calls to other Azure resources. In terms of Azure roles, indexers don't have separate identities; a connection from the search engine to another Azure resource is made using the system or user- assigned managed identity of a search service. If the indexer connects to an Azure resource on a virtual network, you should create a shared private link for that connection. For more information about secure connections, see Security in Azure Al Search.Check results",
        "locationMetadata": {
          "pageNumber": 2,
          "ordinalPosition": 1,
          "boundingPolygons": "[[{\"x\":2.2041,\"y\":0.4109},{\"x\":4.3967,\"y\":0.4131},{\"x\":4.3966,\"y\":0.5505},{\"x\":2.204,\"y\":0.5482}],[{\"x\":2.5042,\"y\":0.6422},{\"x\":4.8539,\"y\":0.6506},{\"x\":4.8527,\"y\":0.993},{\"x\":2.5029,\"y\":0.9845}],[{\"x\":2.3705,\"y\":1.1496},{\"x\":2.6859,\"y\":1.15},{\"x\":2.6858,\"y\":1.2612},{\"x\":2.3704,\"y\":1.2608}],[{\"x\":3.7418,\"y\":1.1709},{\"x\":3.8082,\"y\":1.171},{\"x\":3.8081,\"y\":1.2508},{\"x\":3.7417,\"y\":1.2507}],[{\"x\":3.9692,\"y\":1.1445},{\"x\":4.0541,\"y\":1.1445},{\"x\":4.0542,\"y\":1.2621},{\"x\":3.9692,\"y\":1.2622}],[{\"x\":4.5326,\"y\":1.2263},{\"x\":5.1065,\"y\":1.229},{\"x\":5.106,\"y\":1.346},{\"x\":4.5321,\"y\":1.3433}],[{\"x\":5.5508,\"y\":1.2267},{\"x\":5.8992,\"y\":1.2268},{\"x\":5.8991,\"y\":1.3408},{\"x\":5.5508,\"y\":1.3408}]]"
        },
        "sections": ["sectionHeading", "title"]
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
The skill uses [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview) to compute locationMetadata. Refer to [Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout) for details on how pages and bounding polygon coordinates are defined.
The `imagePath` represents the relative path of a stored image. If the knowledge store file projection is configured in the skillset, this path matches the relative path of the image stored in the knowledge store.

## See also

+ [What is document intelligence layout model](/azure/ai-services/document-intelligence/concept-layout)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skill set](cognitive-search-defining-skillset.md)
+ [Create Indexer (REST API)](/rest/api/searchservice/indexers/create)
