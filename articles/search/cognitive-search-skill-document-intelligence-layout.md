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
ms.date: 04/07/2025
---

# Document Layout skill

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The **Document Layout** skill analyzes a document to extract regions of interest and their inter-relationships to produce a syntactical representation of the document in Markdown format. This skill uses the [Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout) provided in [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview). 

This article is the reference documentation for the Document Layout skill. For usage information, see [Structure-aware chunking and vectorization](search-how-to-semantic-chunking.md).

The **Document Layout** skill calls the [Document Intelligence Public preview version 2024-07-31-preview](/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)&preserve-view=true). 

Supported regions varies by modality:

+ In code, your skillset can call Document Intelligence through an Azure AI multi-service resource in any region that provides both AI enrichment and Document Intelligence. See [Product availability by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table) to find regions that provide both *AI enrichment* in Azure AI Search and *Document Intelligence* under Azure AI services.

+ In the [Import and vectorize data](search-import-data-portal.md) wizard in the Azure portal, you can enable document layout detection in the data source connection step. Document layout detection in the portal is available in the following Azure regions: **East US**, **West Europe**, **North Central US**. Create an Azure AI multi-service resource in one of these three regions to get the portal experience.

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

+ The skill can't extract images embedded within documents.
+ Page numbers are not included in the generated output.
+ The skill is not suitable for large documents requiring more than 5 minutes of processing in the AI Document Intelligence layout model. The skill will time out, but charges will still apply to the AI Services multi-services resource if it is attached to the skillset for billing purposes. Ensure documents are optimized to stay within processing limits to avoid unnecessary costs.

  
## Skill parameters

Parameters are case-sensitive.

| Parameter name     | Allowed Values | Description |
|--------------------|-------------|-------------|
| `outputMode`    | `oneToMany` | Controls the cardinality of the output produced by the skill. |
| `markdownHeaderDepth` |`h1`, `h2`, `h3`, `h4`, `h5`, `h6(default)` | This parameter describes the deepest nesting level that should be considered. For instance, if the markdownHeaderDepth is indicated as "h3" any markdown section that’s deeper than h3 (that is, #### and deeper) is considered as "content" that needs to be added to whatever level its parent is at. |

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
| `markdown_document`    | A collection of "sections" objects, which represent each individual section in the Markdown document.|

## Sample definition

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

## Sample output

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

The value of the `markdownHeaderDepth` controls the number of keys in the "sections" dictionary. In the example skill definition, since the `markdownHeaderDepth` is "h3", there are three keys in the "sections" dictionary: h1, h2, h3.

## See also

+ [What is document intelligence layout model](/azure/ai-services/document-intelligence/concept-layout)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skill set](cognitive-search-defining-skillset.md)
+ [Create Indexer (REST API)](/rest/api/searchservice/indexers/create)
