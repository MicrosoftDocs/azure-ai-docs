---
title: Utilize the content generation capabilities of language models as part of content ingestion pipeline
titleSuffix: Azure AI Search
description: Use language models to caption your images and facilitate an image search through your data.
author: amitkalay
ms.author: amitkalay
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/05/2025
ms.custom:
  - devx-track-csharp
  - build-2025
---

# Generating captions for images in another language

Images often contain useful information that's relevant in search scenarios. You can [vectorize images](search-get-started-portal-image-search.md) to represent visual content in your search index. Or, you can use [AI enrichment and skillsets](cognitive-search-concept-intro.md) to create and extract searchable *text* from images.

We are going to describe each image from your data source, and then demonstrate running a query to search for a specific thing in the image. We are going to leverage the capabilities of the Custom GenAI prompt skill to generate captions for the images in your data.

To work with image content in a skillset, you need:

> + Source files that include images
> + A search indexer, configured for image actions
> + A skillset with the new custom genAI prompt skill
> + A search index with fields to receive the verbalized text output, plus output field mappings in the indexer that establish association

Optionally, you can define projections to accept image-analyzed output into a [knowledge store](knowledge-store-concept-intro.md) for data mining scenarios.

## Set up source files

Image processing is indexer-driven, which means that the raw inputs must be in a [supported data source](search-indexer-overview.md#supported-data-sources). 

Images are either standalone binary files or embedded in documents, such as PDF, RTF, or Microsoft application files. A maximum of 1,000 images can be extracted from a given document. If there are more than 1,000 images in a document, the first 1,000 are extracted and then a warning is generated.

Azure Blob Storage is the most frequently used storage for image processing in Azure AI Search. There are three main tasks related to retrieving images from a blob container:

+ Enable access to content in the container. If you're using a full access connection string that includes a key, the key gives you permission to the content. Alternatively, you can [authenticate using Microsoft Entra ID](search-howto-managed-identities-data-sources.md) or [connect as a trusted service](search-indexer-howto-access-trusted-service-exception.md).

+ [Create a data source](search-howto-indexing-azure-blob-storage.md) of type *azureblob* that connects to the blob container storing your files.

+ Review [service tier limits](search-limits-quotas-capacity.md) to make sure that your source data is under maximum size and quantity limits for indexers and enrichment.

<a name="get-normalized-images"></a>

## Configure indexers for image processing

After the source files are set up, enable image normalization by setting the `imageAction` parameter in indexer configuration. Image normalization helps make images more uniform for downstream processing. Image normalization includes the following operations:

+ Large images are resized to a maximum height and width to make them uniform.
+ For images that have metadata that specifies orientation, image rotation is adjusted for vertical loading.

Note that enabling `imageAction` (setting this parameter to other than `none`) will incur an additional charge for image extraction according to [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/).

1. [Create or update an indexer](/rest/api/searchservice/indexers/create-or-update) to set the configuration properties:

    ```json
    {
      "parameters":
      {
        "configuration": 
        {
           "dataToExtract": "contentAndMetadata",
           "parsingMode": "default",
           "imageAction": "generateNormalizedImages"
        }
      }
    }
    ```

1. Set `dataToExtract` to `contentAndMetadata` (required).

1. Verify that the `parsingMode` is set to *default* (required).

   This parameter determines the granularity of search documents created in the index. The default mode sets up a one-to-one correspondence so that one blob results in one search document. If documents are large, or if skills require smaller chunks of text, you can add the Text Split skill that subdivides a document into paging for processing purposes. But for search scenarios, one blob per document is required if enrichment includes image processing.

1. Set `imageAction` to enable the `normalized_images` node in an enrichment tree (required):

   + `generateNormalizedImages` to generate an array of normalized images as part of document cracking.

   + `generateNormalizedImagePerPage` (applies to PDF only) to generate an array of normalized images where each page in the PDF is rendered to one output image. For non-PDF files, the behavior of this parameter is similar as if you had set `generateNormalizedImages`. However, setting `generateNormalizedImagePerPage` can make indexing operation less performant by design (especially for large documents) since several images would have to be generated.

1. Optionally, adjust the width or height of the generated normalized images:

   + `normalizedImageMaxWidth` in pixels. Default is 2,000. Maximum value is 10,000.

   + `normalizedImageMaxHeight` in pixels. Default is 2,000. Maximum value is 10,000.

   The default of 2,000 pixels for the normalized images maximum width and height is based on the maximum sizes supported by the [OCR skill](cognitive-search-skill-ocr.md) and the [image analysis skill](cognitive-search-skill-image-analysis.md). The [OCR skill](cognitive-search-skill-ocr.md) supports a maximum width and height of 4,200 for non-English languages, and 10,000 for English. If you increase the maximum limits, processing could fail on larger images depending on your skillset definition and the language of the documents. 

### About normalized images

When `imageAction` is set to a value other than *none*, the new `normalized_images` field contains an array of images. Each image is a complex type that has the following members:

| Image member       | Description                             |
|--------------------|-----------------------------------------|
| data               | BASE64 encoded string of the normalized image in JPEG format.   |
| width              | Width of the normalized image in pixels. |
| height             | Height of the normalized image in pixels. |
| originalWidth      | The original width of the image before normalization. |
| originalHeight      | The original height of the image before normalization. |
| rotationFromOriginal |  Counter-clockwise rotation in degrees that occurred to create the normalized image. A value between 0 degrees and 360 degrees. This step reads the metadata from the image that is generated by a camera or scanner. Usually a multiple of 90 degrees. |
| contentOffset | The character offset within the content field where the image was extracted from. This field is only applicable for files with embedded images. The `contentOffset` for images extracted from PDF documents is always at the end of the text on the page it was extracted from in the document. This means images appear after all text on that page, regardless of the original location of the image in the page. |
| pageNumber | If the image was extracted or rendered from a PDF, this field contains the page number in the PDF it was extracted or rendered from, starting from 1. If the image isn't from a PDF, this field is 0.  |

 Sample value of `normalized_images`:

```json
[
  {
    "data": "BASE64 ENCODED STRING OF A JPEG IMAGE",
    "width": 500,
    "height": 300,
    "originalWidth": 5000,  
    "originalHeight": 3000,
    "rotationFromOriginal": 90,
    "contentOffset": 500,
    "pageNumber": 2
  }
]
```

## Define skillsets for image processing

This section supplements the [skill reference](cognitive-search-predefined-skills.md) articles by providing context for working with skill inputs, outputs, and patterns, as they relate to image processing.

1. [Create or update a skillset](/rest/api/searchservice/skillsets/create) to add skills.

1. If necessary, [include a multi-service key](cognitive-search-attach-cognitive-services.md) in the Azure AI services property of the skillset. Azure AI services must be in the same region as your search service.

Once the basic framework of your skillset is created and Azure AI services is configured, you can focus on each individual image skill, defining inputs and source context, and mapping outputs to fields in either an index or knowledge store.

> [!NOTE]
> For an example skillset that combines image processing with downstream natural language processing, see [REST Tutorial: Use REST and AI to generate searchable content from Azure blobs](cognitive-search-tutorial-blob.md). It shows how to feed skill imaging output into entity recognition and key phrase extraction.

### Inputs for image processing

As noted, images are extracted during document cracking and then normalized as a preliminary step. The normalized images are the inputs to any image processing skill, and are always represented in an enriched document tree in either one of two ways:

+ `/document/normalized_images/*` is for documents that are processed whole.

Whether you're using OCR and image analysis in the same, inputs have virtually the same construction:

```json
    {
      "@odata.type": "#Microsoft.Skills.Custom.ChatCompletionSkill",
      "context": "/document/normalized_images/*",
      "uri": "https://azs-grok-aoai.openai.azure.com/openai/deployments/azs-grok-gpt-4o/chat/completions?api-version=2025-01-01-preview", (this is just an EXAMPLE. Please use the URI provided in AI Foundry)
      "timeout": "PT1M",
      "apiKey": "<YOUR-API-KEY here>"
      "inputs": [
        {
          "name": "image",
          "source": "/document/normalized_images/*/data"
        },
        {
          "name": "systemMessage",
          "source": "='You are a useful artificial intelligence assistant that helps people.'"
        },
        {
          "name": "userMessage",
          "source": "='Describe what you see in this image in 20 words or less in Spanish.'"
        }
      ],
      "outputs": [ 
          {
            "name": "response",
            "targetName": "captionedImage"
          } 
        ]
    },
```

<a name="output-field-mappings"></a>

## Map outputs to search fields

Output text is represented as nodes in an internal enriched document tree, and each node must be mapped to fields in a search index, or to projections in a knowledge store, to make the content available in your app. 

1. [Create or update a search index](/rest/api/searchservice/indexes/create-or-update) to add fields to accept the skill outputs. 

   In the following fields collection example, *content* is blob content. *Metadata_storage_name* contains the name of the file (set `retrievable` to *true*). *Metadata_storage_path* is the unique path of the blob and is the default document key. *Merged_content* is output from Text Merge (useful when images are embedded). 

    *captionedImage* is the skill outputs and must be a string-type in order to the capture all of the language model output in the search index.

    ```json
      "fields": [
        {
          "name": "content",
          "type": "Edm.String",
          "filterable": false,
          "retrievable": true,
          "searchable": true,
          "sortable": false
        },
        {
          "name": "metadata_storage_name",
          "type": "Edm.String",
          "filterable": true,
          "retrievable": true,
          "searchable": true,
          "sortable": false
        },
        {
          "name": "metadata_storage_path",
          "type": "Edm.String",
          "filterable": false,
          "key": true,
          "retrievable": true,
          "searchable": false,
          "sortable": false
        },
        {
          "name": "captioned_image",
          "type": "Edm.String",
          "filterable": false,
          "retrievable": true,
          "searchable": true,
          "sortable": false
        }
      ]
    ```

1. [Update the indexer](/rest/api/searchservice/indexers/create-or-update) to map skillset output (nodes in an enrichment tree) to index fields.

   Enriched documents are internal. To externalize the nodes in an enriched document tree, set up an output field mapping that specifies which index field receives node content. Enriched data is accessed by your app through an index field. The following example shows a *text* node (OCR output) in an enriched document that's mapped to a *text* field in a search index.

    ```json
      "outputFieldMappings": [
        {
          "sourceFieldName": "/document/normalized_images/*/captionedImage",
          "targetFieldName": "captioned_image"
        }
      ]
    ```

1. Run the indexer to invoke source document retrieval, image processing via language model captions, and indexing.

### Verify results

Run a query against the index to check the results of image processing. Use [Search Explorer](search-explorer.md) as a search client, or any tool that sends HTTP requests. The following query selects fields that contain the output of image processing.

```http
POST /indexes/[index name]/docs/search?api-version=[api-version]
{
    "search": "*",
    "select": "metadata_storage_name, captioned_image"
}
```

## Related content
+ [Create indexer (REST)](/rest/api/searchservice/indexers/create)
+ [Gen AI Prompt Skill](/articles/search/cognitive-search-skill-genai-prompt.md)
+ [How to create a skillset](cognitive-search-defining-skillset.md)
+ [Map enriched output to fields](cognitive-search-output-field-mapping.md)
