---
title: Document Intelligence Layout skill
titleSuffix: Azure AI Search
description: Analyze a document to extract regions of interest and their inter-relationships to produce a syntactical representation (markdown format) in an enrichment pipeline in Azure AI Search.

author: rawan
ms.author: 

ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: reference
ms.date: 10/10/2024
---
# Document Intelligence Layout skill

The **Document Intelligence Layout** skill analyze a document to extract regions of interest and their inter-relationships to produce a syntactical representation (markdown format). This skill uses the [Document Intelligence layout model](/azure/ai-services/document-intelligence/concept-layout) provided in [Azure AI Document Intelligence](/azure/ai-services/document-intelligence/overview). This article is the reference documentation for the Document Intelligence Layout skill.

+ The **Document Intelligence Layout** skill uses [Document Intelligence Public preview version 2024-07-31-preview](https://learn.microsoft.com/en-us/rest/api/aiservices/operation-groups?view=rest-aiservices-v4.0%20(2024-07-31-preview)). It is currently only available in the following Azure regions:
    + East US
    + West US2
    + West Europe
    + North Central US

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
+ The file size for analyzing documents is 500 MB for [Azure AI Document Intelligence paid (S0) tier]((https://azure.microsoft.com/pricing/details/cognitive-services/)) and 4 MB for [Azure AI Document Intelligence free (F0) tier]((https://azure.microsoft.com/pricing/details/cognitive-services/)).
+ Image dimensions must be between 50 pixels x 50 pixels and 10,000 pixels x 10,000 pixels.
+ If your PDFs are password-locked, you must remove the lock before submission.


## Skill parameters

Parameters are case-sensitive.

| Parameter name     | Allowed Values | Description |
|--------------------|-------------|-------------|
| `outputMode`    | `oneToMany` | Controls the cardinality of the output produced by the skill. |
| `markdownHeaderDepth` |`h1`, `h2`, `h3`, `h4`, `h5`, `h6(default)` | This describes the deepest nesting level that should be considered. For instance, if the markdownHeaderDepth is indicated as “h3”, any markdown section that’s deeper than h3 (i.e., #### and deeper) will simply be considered as “content” that needs to be added to whatever level its parent is at. |

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

The file reference object can be generated one of following ways:

+ Setting the `allowSkillsetToReadFileData` parameter on your indexer definition to "true".  This creates a path `/document/file_data` that is an object representing the original file data downloaded from your blob data source. This parameter only applies to files in Blob storage.

+ Having a custom skill return a json object defined EXACTLY as above.  The `$type` parameter must be set to exactly `file` and the `data` parameter must be the base 64 encoded byte array data of the file content, or the `url` parameter must be a correctly formatted URL with access to download the file at that location.

## Skill outputs

| Output name      | Description                   |
|---------------|-------------------------------|
| `markdown_document`    | A collection of “sections” objects, which represent each individual section in the markdown document.|

## Sample definition

```json
{
  "skills": [
    {
      "description": "Extracts text (plain and structured) from image.",
      "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
      "context": "/document/normalized_images/*",
      "defaultLanguageCode": null,
      "detectOrientation": true,
      "inputs": [
        {
          "name": "image",
          "source": "/document/normalized_images/*"
        }
      ],
      "outputs": [
        {
          "name": "text",
          "targetName": "myText"
        },
        {
          "name": "layoutText",
          "targetName": "myLayoutText"
        }
      ]
    }
  ]
}
```

<a name="sample-output"></a>

## Sample output

```json
{
  "text": "Hello World. -John",
  "layoutText":
  {
    "language" : "en",
    "text" : "Hello World. -John",
    "lines" : [
      {
        "boundingBox":
        [ {"x":10, "y":10}, {"x":50, "y":10}, {"x":50, "y":30},{"x":10, "y":30}],
        "text":"Hello World."
      },
      {
        "boundingBox": [ {"x":110, "y":10}, {"x":150, "y":10}, {"x":150, "y":30},{"x":110, "y":30}],
        "text":"-John"
      }
    ],
    "words": [
      {
        "boundingBox": [ {"x":110, "y":10}, {"x":150, "y":10}, {"x":150, "y":30},{"x":110, "y":30}],
        "text":"Hello"
      },
      {
        "boundingBox": [ {"x":110, "y":10}, {"x":150, "y":10}, {"x":150, "y":30},{"x":110, "y":30}],
        "text":"World."
      },
      {
        "boundingBox": [ {"x":110, "y":10}, {"x":150, "y":10}, {"x":150, "y":30},{"x":110, "y":30}],
        "text":"-John"
      }
    ]
  }
}
```

## Sample: Merging text extracted from embedded images with the content of the document

Document cracking, the first step in skillset execution, separates text and image content. A common use case for Text Merger is merging the textual representation of images (text from an OCR skill, or the caption of an image) into the content field of a document. This is for scenarios where the source document is a PDF or Word document that combines text with embedded images.

The following example skillset creates a *merged_text* field. This field contains the textual content of your document and the OCRed text from each of the images embedded in that document.

#### Request Body Syntax

```json
{
  "description": "Extract text from images and merge with content text to produce merged_text",
  "skills":
  [
    {
      "description": "Extract text (plain and structured) from image.",
      "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
      "context": "/document/normalized_images/*",
      "defaultLanguageCode": "en",
      "detectOrientation": true,
      "inputs": [
        {
          "name": "image",
          "source": "/document/normalized_images/*"
        }
      ],
      "outputs": [
        {
          "name": "text"
        }
      ]
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.MergeSkill",
      "description": "Create merged_text, which includes all the textual representation of each image inserted at the right location in the content field.",
      "context": "/document",
      "insertPreTag": " ",
      "insertPostTag": " ",
      "inputs": [
        {
          "name":"text",
          "source": "/document/content"
        },
        {
          "name": "itemsToInsert", 
          "source": "/document/normalized_images/*/text"
        },
        {
          "name":"offsets", 
          "source": "/document/normalized_images/*/contentOffset"
        }
      ],
      "outputs": [
        {
          "name": "mergedText", 
          "targetName" : "merged_text"
        }
      ]
    }
  ]
}
```

The above skillset example assumes that a normalized-images field exists. To generate this field, set the *imageAction* configuration in your indexer definition to *generateNormalizedImages* as shown below:

```json
{
  //...rest of your indexer definition goes here ...
  "parameters": {
    "configuration": {
      "dataToExtract":"contentAndMetadata",
      "imageAction":"generateNormalizedImages"
    }
  }
}
```

## See also

+ [What is document intelligence layout model](/azure/ai-services/document-intelligence/concept-layout?view=doc-intel-4.0.0&tabs=sample-code)
+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [Create Indexer (REST)](/rest/api/searchservice/indexers/create)
