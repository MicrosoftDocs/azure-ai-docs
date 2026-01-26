---
title: Azure Vision Multimodal Embeddings Skill
titleSuffix: Azure AI Search
description: Vectorize images or text using the Azure Vision multimodal embeddings API.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - build-2024
  - references_regions
ms.topic: reference
ms.date: 01/16/2026
---

# Azure Vision multimodal embeddings skill

> [!IMPORTANT]
> This skill is in public preview under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). The [2024-05-01-Preview REST API](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2024-05-01-Preview&preserve-view=true) and newer preview APIs support this feature.

The **Azure Vision multimodal embeddings** skill uses the [multimodal embeddings API](/azure/ai-services/computer-vision/concept-image-retrieval) from Azure Vision in Foundry Tools to generate embeddings for text or image input.

For transactions that exceed 20 documents per indexer per day, this skill requires you to [attach a billable Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) to your skillset. Execution of built-in skills is charged at the existing [Foundry Tools Standard price](https://azure.microsoft.com/pricing/details/cognitive-services/). Image extraction is also [billable by Azure AI Search](https://azure.microsoft.com/pricing/details/search/).

The Microsoft Foundry resource is used for billing purposes only. Content processing occurs on separate resources managed and maintained by Azure AI Search. Your data is processed in the [Geo](https://azure.microsoft.com/explore/global-infrastructure/data-residency/) where your resource is deployed.

## Supported regions

Supported regions vary by modality and how the skill connects to the Azure Vision multimodal embeddings API.

| Approach | Requirement |
|----------|-------------|
| [**Import data (new)** wizard](search-import-data-portal.md) | <ol><li>Find a [region that supports multimodal embeddings](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability) in Azure Vision.</li><li>Verify the [region supports AI enrichment](search-region-support.md) in Azure AI Search.</li><li>Create an Azure AI Search service and [Azure AI multi-service account](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne) in the same region. </li></ol> |
| Programmatic, using a [key-based connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) for billing | <ol><li>Find a [region that supports multimodal embeddings](/azure/ai-services/computer-vision/overview-image-analysis?tabs=4-0#region-availability) in Azure Vision.</li><li>Verify the [region supports AI enrichment](search-region-support.md) in Azure AI Search.</li><li>Create an Azure AI Search service and Microsoft Foundry resource in the same region. </li></ol> |
| Programmatic, using a [keyless connection](cognitive-search-attach-cognitive-services.md#bill-through-a-keyless-connection) for billing | No same-region requirement. Create an Azure AI Search service and Microsoft Foundry resource in any region where [each service is available](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table). |

## @odata.type  

Microsoft.Skills.Vision.VectorizeSkill

## Data limits

The input limits for the skill can be found in the [Azure Vision documentation](/azure/ai-services/computer-vision/concept-image-retrieval#input-requirements) for images and text. Consider using the [Text Split skill](cognitive-search-skill-textsplit.md) if you need data chunking for text inputs.

Applicable inputs include:

+ Image input file size must be less than 20 megabytes (MB). Image size must be greater than 10 x 10 pixels and less than 16,000 x 16,000 pixels.
+ Text input string must be between (inclusive) one word and 70 words.

## Skill parameters

Parameters are case sensitive.

| Inputs | Description |
|---------------------|-------------|
| `modelVersion` | (Required) The model version (`2023-04-15`) to be passed to the Azure Vision multimodal embeddings API for generating embeddings. Vector embeddings can only be compared and matched if they're from the same model type. Images vectorized by one model won't be searchable through a different model. The latest Image Analysis API offers two models:<br><ul><li>The `2023-04-15` version, which supports text search in many languages.  Azure AI Search uses this version.</li><li> The legacy `2022-04-11` model, which supports only English.</li></ul> |

## Skill inputs

Skill definition inputs include name, source, and inputs. The following table provides valid values for name of the input. You can also specify recursive inputs. For more information, see the [REST API reference](/rest/api/searchservice/skillsets/create?view=rest-searchservice-2025-03-01-preview#inputfieldmappingentry&preserve-view=true) and [Create a skillset](cognitive-search-defining-skillset.md).

| Input	 | Description |
|--------|-------------|
| `text` | The input text to be vectorized. If you're using data chunking, the source might be `/document/pages/*`. |
| `image` | Complex Type. Currently only works with "/document/normalized_images" field, produced by the Azure blob indexer when ```imageAction``` is set to a value other than ```none```. |
| `url` | The URL to download the image to be vectorized. |
| `queryString` | The query string of the URL to download the image to be vectorized. Useful if you store the URL and SAS token in separate paths. |

Only one of `text`, `image` or `url`/`queryString` can be configured for a single instance of the skill. If you want to vectorize both images and text within the same skillset, include two instances of this skill in the skillset definition, one for each input type you would like to use.

## Skill outputs

| Output	 | Description |
|--------------------|-------------|
| `vector` | Output embedding array of floats for the input text or image. |

## Sample definition

For text input, consider a blob that has the following content:

```json
{
    "content": "Forests, grasslands, deserts, and mountains are all part of the Patagonian landscape that spans more than a million square  kilometers of South America."
}
```

For text inputs, your skill definition might look like this:

```json
{ 
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill", 
    "context": "/document", 
    "modelVersion": "2023-04-15", 
    "inputs": [ 
        { 
            "name": "text", 
            "source": "/document/content" 
        } 
    ], 
    "outputs": [ 
        { 
            "name": "vector",
            "targetName": "text_vector"
        } 
    ] 
} 

```

For image input, a second skill definition in the same skillset might look like this:

```json
{
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill",
    "context": "/document/normalized_images/*",
    "modelVersion": "2023-04-15", 
    "inputs": [
        {
            "name": "image",
            "source": "/document/normalized_images/*"
        }
    ],
    "outputs": [
        {
            "name": "vector",
            "targetName": "image_vector"
        }
    ]
}
```

If you want to vectorize images directly from your blob storage data source rather than extract images during indexing, your skill definition should specify a URL, and perhaps a SAS token depending on storage security. For this scenario, your skill definition  might look like this:

```json
{
    "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill",
    "context": "/document",
    "modelVersion": "2023-04-15", 
    "inputs": [
        {
            "name": "url",
            "source": "/document/metadata_storage_path"
        },
        {
            "name": "queryString",
            "source": "/document/metadata_storage_sas_token"
        }
    ],
    "outputs": [
        {
            "name": "vector",
            "targetName": "image_vector"
        }
    ]
}
```

## Sample output

For the given input, a vectorized embedding output is produced. Output is 1,024 dimensions, which is the number of dimensions supported by the Azure Vision multimodal API.

```json
{
  "text_vector": [
        0.018990106880664825,
        -0.0073809814639389515,
        .... 
        0.021276434883475304,
      ]
}
```

The output resides in memory. To send this output to a field in the search index, you must define an [outputFieldMapping](cognitive-search-output-field-mapping.md) that maps the vectorized embedding output (which is an array) to a [vector field](vector-search-how-to-create-index.md). Assuming the skill output resides in the document's **vector** node, and **content_vector** is the field in the search index, the outputFieldMapping in the indexer should look like:

```json
  "outputFieldMappings": [
    {
      "sourceFieldName": "/document/vector/*",
      "targetFieldName": "content_vector"
    }
  ]
```

For mapping image embeddings to the index, you use [index projections](index-projections-concept-intro.md). The payload for `indexProjections` might look something like the following example. image_content_vector is a field in the index, and it's populated with the content found in the **vector** of the **normalized_images** array.

```json
"indexProjections": {
    "selectors": [
        {
            "targetIndexName": "myTargetIndex",
            "parentKeyFieldName": "ParentKey",
            "sourceContext": "/document/normalized_images/*",
            "mappings": [
                {
                    "name": "image_content_vector",
                    "source": "/document/normalized_images/*/vector"
                }
            ]
        }
    ]
}
```

## See also

+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
+ [Extract text and information from images](cognitive-search-concept-image-scenarios.md)
+ [How to define output fields mappings](cognitive-search-output-field-mapping.md)
+ [Index Projections](index-projections-concept-intro.md)
+ [Azure Vision multimodal embeddings API](/azure/ai-services/computer-vision/concept-image-retrieval)
