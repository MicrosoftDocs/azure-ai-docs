---
title: Named entity recognition skill parameters
titleSuffix: Foundry Tools
description: Learn about skill parameters for named entity recognition.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 12/05/2025
ms.author: lajanuar
---
# Using named entity recognition skill parameters

Use this article to get an overview of the different API parameters used to adjust the input to a Named Entity Recognition (NER) API call. The Generally Available NER service now supports the ability to specify a list of entity tags to be included into the response or excluded from the response. If a piece of text is classified as more than one entity type, the `overlapPolicy` parameter allows customers to specify how the service handles the overlap. The `inferenceOptions` parameter allows for users to adjust the inference, such as excluding the detected entity values from being normalized and included in the metadata.

## InclusionList parameter

The `inclusionList` parameter allows for you to specify which of the NER entity tags, you would like included in the entity list output in your inference JSON listing out all words and categorizations recognized by the NER service. By default, all recognized entities are listed.

## ExclusionList parameter

The `exclusionList` parameter allows for you to specify which of the NER entity tags, you would like excluded in the entity list output in your inference JSON listing out all words and categorizations recognized by the NER service. By default, all recognized entities are listed.

## overlapPolicy parameter

The `overlapPolicy` parameter allows for you to specify how you like the NER service to respond to recognized words/phrases that fall into more than one category. 

By default, the `overlapPolicy` parameter is set to `matchLongest`. This option categorizes the extracted word/phrase under the entity category that can encompass the longest span of the extracted word/phrase (longest defined by the most number of characters included).

The alternative option for this parameter is `allowOverlap`, where all possible entity categories are listed. 
Parameters by supported API version

## inferenceOptions parameter

Defines a selection of options available for adjusting the inference. Currently we have only one property called `excludeNormalizedValues` that excludes the detected entity values to be normalized and included in the metadata. The numeric and temporal entity types support value normalization. 

## Sample

This bit of sample code explains how to use skill parameters.

```bash
{ 
    "analysisInput": { 
        "documents": [ 
            { 
                "id": "1", 
                "text": "My name is John Doe", 
                "language": "en" 
            } 
        ] 
    }, 
    "kind": "EntityRecognition", 
    "parameters": { 
        "overlapPolicy": { 
            "policyKind": "AllowOverlap" //AllowOverlap|MatchLongest(default) 
        }, 
        "inferenceOptions": { 
            "excludeNormalizedValues": true //(Default: false) 
        }, 
        "inclusionList": [ 
            "DateAndTime" // A list of entity tags to be used to allow into the response. 
        ], 
        "exclusionList": ["Date"] // A list of entity tags to be used to filter out from the response. 
    } 
} 
```

## Next steps

* See [Configure containers](../../concepts/configure-containers.md) for configuration settings.
