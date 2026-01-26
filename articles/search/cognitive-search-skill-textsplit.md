---
title: Text Split skill
titleSuffix: Azure AI Search
description: Break text into chunks or pages of text based on length in an AI enrichment pipeline in Azure AI Search.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: reference
ms.date: 01/07/2026
ms.update-cycle: 365-days
---

# Text Split cognitive skill

> [!IMPORTANT] 
> Some parameters are in public preview under [Supplemental Terms of Use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). The [preview REST API](/rest/api/searchservice/index-preview) supports these parameters.

The **Text Split** skill breaks text into chunks of text. You can specify whether you want to break the text into sentences or into pages of a particular length. Positional metadata like offset and ordinal position are also available as outputs. This skill is useful if there are maximum text length requirements in other skills downstream, such as embedding skills that pass data chunks to embedding models on Azure OpenAI and other model providers. For more information about this scenario, see [Chunk documents for vector search](vector-search-how-to-chunk-documents.md).

Several parameters are version-specific. The skills parameter table notes the API version in which a parameter was introduced so that you know whether a [version upgrade](search-api-migration.md) is required. To use version-specific features such as *token chunking* in **2024-09-01-preview**, you can use the Azure portal, or target a REST API version, or check an Azure SDK change log to see if it supports the feature.

The Azure portal supports most preview features and can be used to create or update a skillset. For updates to the Text Split skill, edit the skillset JSON definition to add new preview parameters. 

> [!NOTE]
> This skill isn't bound to Foundry Tools. It's non-billable and has no Foundry Tools key requirement.

## @odata.type  
Microsoft.Skills.Text.SplitSkill 

## Skill Parameters

Parameters are case sensitive. 

| Parameter name     | Description |
|--------------------|-------------|-------------|
| `textSplitMode`    | Either `pages` or `sentences`. Pages have a configurable maximum length, but the skill attempts to avoid truncating a sentence so the actual length might be smaller. Sentences are a string that terminates at sentence-ending punctuation, such as a period, question mark, or exclamation point, assuming the language has sentence-ending punctuation. | 
| `maximumPageLength` | Only applies if `textSplitMode` is set to `pages`. For `unit` set to `characters`, this parameter refers to the maximum page length in characters as measured by `String.Length`. The minimum value is 300, the maximum is 50000, and the default value is 5000.  The algorithm does its best to break the text on sentence boundaries, so the size of each chunk might be slightly less than `maximumPageLength`. <br><br>For `unit` set to `azureOpenAITokens`, the maximum page length is the token length limit of the model. For text embedding models, a general recommendation for page length is 512 tokens. |
| `defaultLanguageCode`	| (optional) One of the following language codes: `am, bs, cs, da, de, en, es, et, fr, he, hi, hr, hu, fi, id, is, it, ja, ko, lv, no, nl, pl, pt-PT, pt-BR, ru, sk, sl, sr, sv, tr, ur, zh-Hans`. Default is English (en). A few things to consider: <ul><li>Providing a language code is useful to avoid cutting a word in half for nonwhitespace languages such as Chinese, Japanese, and Korean.</li><li>If you don't know the language  in advance (for example, if you're using the [LanguageDetectionSkill](cognitive-search-skill-language-detection.md) to detect language), we recommend the `en` default. </li></ul>  |
| `pageOverlapLength` | Only applies if `textSplitMode` is set to `pages`. Each page starts with this number of characters or tokens from the end of the previous page. If this parameter is set to 0, there's no overlapping text on successive pages. This [example](#example-for-chunking-and-vectorization) includes the parameter. |
| `maximumPagesToTake` | Only applies if `textSplitMode` is set to `pages`. Number of pages to return. The default is 0, which means to return all pages. You should set this value if only a subset of pages are needed. This [example](#example-for-chunking-and-vectorization) includes the parameter.|
| `unit` | Only applies if `textSplitMode` is set to `pages`. Specifies whether to chunk by `characters` (default) or `azureOpenAITokens`. Setting the unit affects `maximumPageLength` and `pageOverlapLength`. |
| `azureOpenAITokenizerParameters` An object providing extra parameters for the `azureOpenAITokens` unit. <br><br>`encoderModelName` is a designated tokenizer used for converting text into tokens, essential for natural language processing (NLP) tasks. Different models use different tokenizers. Valid values include cl100k_base (default) used by GPT-4. Other valid values are r50k_base, p50k_base, and p50k_edit. The skill implements the tiktoken library by way of [SharpToken](https://www.nuget.org/packages/SharpToken) and `Microsoft.ML.Tokenizers` but doesn't support every encoder. For example, there's currently no support for o200k_base encoding used by GPT-4o. <br><br>`allowedSpecialTokens` defines a collection of special tokens that are permitted within the tokenization process. Special tokens are  string that you want to treat uniquely, ensuring they aren't split during tokenization. For example ["[START"], "[END]"]. If the `tiktoken` library doesn't perform tokenization as expected, either due to language-specific limitations or other unexpected behaviors, it's recommended to use text splitting instead.|

## Skill Inputs

| Parameter name	   | Description      |
|----------------------|------------------|
| `text` | The text to split into substring. |
| `languageCode` | (Optional) Language code for the document. If you don't know the language of the text inputs (for example, if you're using [LanguageDetectionSkill](cognitive-search-skill-language-detection.md) to detect the language), you can omit this parameter. If you set `languageCode` to a language isn't in the supported list for the `defaultLanguageCode`, a warning is emitted and the text isn't split.  |

## Skill Outputs 

| Parameter name	 | Description |
|--------------------|-------------|
| `textItems` | Output is an array of substrings that were extracted. `textItems` is the default name of the output. <br><br>`targetName` is optional, but if you have multiple Text Split skills, make sure to set `targetName` so that you don't overwrite the data from the first skill with the second one. If `targetName` is set, use it in output field mappings or in downstream skills that consume the skill output, such as an embedding skill.|
| `offsets` | Output is an array of offsets that were extracted. The value at each index is an object containing the offset of the text item at that index in three encodings: UTF-8, UTF-16, and CodePoint. `offsets` is the default name of the output. <br><br>`targetName` is optional, but if you have multiple Text Split skills, make sure to set `targetName` so that you don't overwrite the data from the first skill with the second one. If `targetName` is set, use it in output field mappings or in downstream skills that consume the skill output, such as an embedding skill.|
| `lengths` | Output is an array of lengths that were extracted. The value at each index is an object containing the offset of the text item at that index in three encodings: UTF-8, UTF-16, and CodePoint. `lengths` is the default name of the output. <br><br>`targetName` is optional, but if you have multiple Text Split skills, make sure to set `targetName` so that you don't overwrite the data from the first skill with the second one. If `targetName` is set, use it in output field mappings or in downstream skills that consume the skill output, such as an embedding skill.|
| `ordinalPositions` | Output is an array of ordinal positions corresponding to the position of the text item within the source text. `ordinalPositions` is the default name of the output. <br><br>`targetName` is optional, but if you have multiple Text Split skills, make sure to set `targetName` so that you don't overwrite the data from the first skill with the second one. If `targetName` is set, use it in output field mappings or in downstream skills that consume the skill output, such as an embedding skill.|

## Sample definition

```json
{
    "name": "SplitSkill", 
    "@odata.type": "#Microsoft.Skills.Text.SplitSkill", 
    "description": "A skill that splits text into chunks", 
    "context": "/document", 
    "defaultLanguageCode": "en", 
    "textSplitMode": "pages", 
    "unit": "azureOpenAITokens", 
    "azureOpenAITokenizerParameters":{ 
        "encoderModelName":"cl100k_base", 
        "allowedSpecialTokens": [ 
            "[START]", 
            "[END]" 
        ] 
    },
    "maximumPageLength": 512,
    "inputs": [
        {
            "name": "text",
            "source": "/document/text"
        },
        {
            "name": "languageCode",
            "source": "/document/language"
        }
    ],
    "outputs": [
        {
            "name": "textItems",
            "targetName": "pages"
        }
    ]
}
```

## Sample input

```json
{
    "values": [
        {
            "recordId": "1",
            "data": {
                "text": "This is the loan application for Joe Romero, a Microsoft employee who was born in Chile and who then moved to Australia...",
                "languageCode": "en"
            }
        },
        {
            "recordId": "2",
            "data": {
                "text": "This is the second document, which will be broken into several pages...",
                "languageCode": "en"
            }
        }
    ]
}
```

## Sample output

```json
{
    "values": [
        {
            "recordId": "1",
            "data": {
                "pages": [
                    "This is the loan...",
                    "In the next section, we continue..."
                ],
                "offsets": [
                    {
                        "utf8": 0,
                        "utf16": 0,
                        "codePoint": 0
                    },
                    {
                        "utf8": 146,
                        "utf16": 146,
                        "codePoint": 146
                    }
                ],
                "lengths": [
                    {
                        "utf8": 146,
                        "utf16": 146,
                        "codePoint": 146
                    },
                    {
                        "utf8": 211,
                        "utf16": 211,
                        "codePoint": 211
                    }
                ],
                "ordinalPositions" : [
                    1,
                    2
                ]
            }
        },
        {
            "recordId": "2",
            "data": {
                "pages": [
                    "This is the second document...",
                    "In the next section of the second doc..."
                ],
                "offsets": [
                    {
                        "utf8": 0,
                        "utf16": 0,
                        "codePoint": 0
                    },
                    {
                        "utf8": 115,
                        "utf16": 115,
                        "codePoint": 115
                    }
                ],
                "lengths": [
                    {
                        "utf8": 115,
                        "utf16": 115,
                        "codePoint": 115
                    },
                    {
                        "utf8": 209,
                        "utf16": 209,
                        "codePoint": 209
                    }
                ],
                 "ordinalPositions" : [
                    1,
                    2
                ]
            }
        }
    ]
}
```


> [!NOTE]
> This example sets `textItems` to `pages` through `targetName`. Because `targetName` is set, `pages` is the value you should use to select the output from the Text Split skill. Use `/document/pages/*` in downstream skills, indexer [output field mappings](cognitive-search-concept-annotations-syntax.md), [knowledge store projections](knowledge-store-projection-overview.md), and [index projections](index-projections-concept-intro.md).
> This example doesn't set `offsets`, `lengths`, or `ordinalPosition` to any other name, so the value you should use in downstream skills would be unchanged.
> `offsets` and `lengths` are complex types rather than primitives, because they contain the values for multiple encoding types. The value you should use to obtain a specific encoding, for example UTF-8, would look like this: `/document/offsets/*/utf8`.

## Example for chunking and vectorization

This example is for integrated vectorization.

+ `pageOverlapLength`: Overlapping text is useful in [data chunking](vector-search-how-to-chunk-documents.md) scenarios because it preserves continuity between chunks generated from the same document. 

+ `maximumPagesToTake`: Limits on page intake are useful in [vectorization](vector-search-how-to-generate-embeddings.md) scenarios because it helps you stay under the maximum input limits of the embedding models providing the vectorization.

### Sample definition

This definition adds `pageOverlapLength` of 100 characters and `maximumPagesToTake` of one. 

Assuming the `maximumPageLength` is 5,000 characters (the default), then `"maximumPagesToTake": 1` processes the first 5,000 characters of each source document.

This example sets `textItems` to `myPages` through `targetName`. Because `targetName` is set, `myPages` is the value you should use to select the output from the Text Split skill. Use `/document/myPages/*` in downstream skills, indexer [output field mappings](cognitive-search-concept-annotations-syntax.md), [knowledge store projections](knowledge-store-projection-overview.md), and [index projections](index-projections-concept-intro.md).

```json
{
    "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
    "textSplitMode" : "pages", 
    "maximumPageLength": 1000,
    "pageOverlapLength": 100,
    "maximumPagesToTake": 1,
    "defaultLanguageCode": "en",
    "inputs": [
        {
            "name": "text",
            "source": "/document/content"
        },
        {
            "name": "languageCode",
            "source": "/document/language"
        }
    ],
    "outputs": [
        {
            "name": "textItems",
            "targetName": "myPages"
        }
    ]
}
```

### Sample input (same as previous example)

```json
{
    "values": [
        {
            "recordId": "1",
            "data": {
                "text": "This is the loan application for Joe Romero, a Microsoft employee who was born in Chile and who then moved to Australia...",
                "languageCode": "en"
            }
        },
        {
            "recordId": "2",
            "data": {
                "text": "This is the second document, which will be broken into several sections...",
                "languageCode": "en"
            }
        }
    ]
}
```

### Sample output (notice the overlap)

Within each "textItems" array, trailing text from the first item is copied into the beginning of the second item.

```json
{
    "values": [
        {
            "recordId": "1",
            "data": {
                "myPages": [
                    "This is the loan...Here is the overlap part",
                    "Here is the overlap part...In the next section, we continue..."
                ]
            }
        },
        {
            "recordId": "2",
            "data": {
                "myPages": [
                    "This is the second document...Here is the overlap part...",
                    "Here is the overlap part...In the next section of the second doc..."
                ]
            }
        }
    ]
}
```

## Error cases

If a language isn't supported, a warning is generated.

## See also

+ [Built-in skills](cognitive-search-predefined-skills.md)
+ [How to define a skillset](cognitive-search-defining-skillset.md)
