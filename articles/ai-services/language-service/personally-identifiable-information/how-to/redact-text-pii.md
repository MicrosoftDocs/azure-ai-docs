---
title: Identify and extract Personally Identifying Information (PII) from text
titleSuffix: Azure AI services
description: This article shows you how to identify, extract and redact Personally Identifying Information (PII) from text.
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 03/05/2025
ms.author: lajanuar
ms.custom: language-service-pii
---

# Detect and redact Personally Identifying Information in text

Azure AI Language is a cloud-based service that applies Natural Language Processing (NLP) features to text-based data. The PII feature can evaluate unstructured text, extract, and redact sensitive information (PII) and health information (PHI) in text across several [predefined categories](../concepts/entity-categories.md).


## Development options

[!INCLUDE [development options](../includes/development-options.md)]

## Specify the PII detection model

By default, this feature uses the latest available AI model on your text. You can also configure your API requests to use a specific [model version](../../concepts/model-lifecycle.md).

## Input languages

When you submit input text to be processed, you can specify which of [the supported languages](../language-support.md) they're written in. If you don't specify a language, extraction defaults to English. The API may return offsets in the response to support different [multilingual and emoji encodings](../../concepts/multilingual-emoji-support.md). 

## Redaction Policy (version 2024-11-5-preview only)
In version `2024-11-5-preview`, you're able to define the `redactionPolicy` parameter to reflect the redaction policy to be used when redacting text. The policy field supports three policy types:

- `DoNotRedact` 
- `MaskWithCharacter` (default) 
- `MaskWithEntityType` 

The `DoNotRedact` policy allows the user to return the response without the `redactedText` field, that is, "John Doe received a call from 424-878-9192". 

The `MaskWithRedactionCharacter` policy allows the `redactedText` to be masked with a character (such as "*"), preserving the length and offset of the original text, that is, "******** received a call from ************". This is the existing behavior.

There's also an optional field called `redactionCharacter` where you can input the character to be used in redaction if you're using the `MaskWithCharacter` policy 

The `MaskWithEntityType` policy allows you to mask the detected PII entity text with the detected entity type, that is, "[PERSON_1] received a call from [PHONENUMBER_1]". 

## Select which entities to be returned

The API attempts to detect the [defined entity categories](../concepts/entity-categories.md) for a given input text language. If you want to specify which entities are detected and returned, use the optional `piiCategories` parameter with the appropriate entity categories. This parameter can also let you detect entities that aren't enabled by default for your input text language. The following example would detect only `Person`. You can specify one or more [entity types](../concepts/entity-categories.md) to be returned.

> [!TIP]
> If you don't include `default` when specifying entity categories, The API only returns the entity categories you specify.

**Input:**

> [!NOTE]
> In this example, it returns only the **person** entity type:

`https://<your-language-resource-endpoint>/language/:analyze-text?api-version=2022-05-01`

```bash
{
    "kind": "PiiEntityRecognition",
    "parameters": 
    {
        "modelVersion": "latest",
        "piiCategories" :
        [
            "Person"
        ]
    },
    "analysisInput":
    {
        "documents":
        [
            {
                "id":"1",
                "language": "en",
                "text": "We went to Contoso foodplace located at downtown Seattle last week for a dinner party, and we adore the spot! They provide marvelous food and they have a great menu. The chief cook happens to be the owner (I think his name is John Doe) and he is super nice, coming out of the kitchen and greeted us all. We enjoyed very much dining in the place! The pasta I ordered was tender and juicy, and the place was impeccably clean. You can even pre-order from their online menu at www.contosofoodplace.com, call 112-555-0176 or send email to order@contosofoodplace.com! The only complaint I have is the food didn't come fast enough. Overall I highly recommend it!"
            }
        ]
    },
    "kind": "PiiEntityRecognition", 
    "parameters": { 
        "redactionPolicy": { 
            "policyKind": "MaskWithCharacter"  
             //MaskWithCharacter|MaskWithEntityType|DoNotRedact 
            "redactionCharacter": "*"  
}

```

**Output:**

```bash

{
    "kind": "PiiEntityRecognitionResults",
    "results": {
        "documents": [
            {
                "redactedText": "We went to Contoso foodplace located at downtown Seattle last week for a dinner party, and we adore the spot! They provide marvelous food and they have a great menu. The chief cook happens to be the owner (I think his name is ********) and he is super nice, coming out of the kitchen and greeted us all. We enjoyed very much dining in the place! The pasta I ordered was tender and juicy, and the place was impeccably clean. You can even pre-order from their online menu at www.contosofoodplace.com, call 112-555-0176 or send email to order@contosofoodplace.com! The only complaint I have is the food didn't come fast enough. Overall I highly recommend it!",
                "id": "1",
                "entities": [
                    {
                        "text": "John Doe",
                        "category": "Person",
                        "offset": 226,
                        "length": 8,
                        "confidenceScore": 0.98
                    }
                ],
                "warnings": []
            }
        ],
        "errors": [],
        "modelVersion": "2021-01-15"
    }
}
```

## Adapting PII to your domain

To accommodate and adapt to a customer’s custom vocabulary used to identify entities (also known as the “context”), the `entitySynonyms` feature allows customers to define their own synonyms for specific entity types. The goal of this feature is to help detect entities in contexts that the model is not familiar with but are used in the customer’s inputs by ensuring that the customer’s unique terms are recognized and correctly associated during the detection process. 

The `valueExclusionPolicy` option allows customers to adapt the PII service for scenarios where customers prefer certain terms not to be detected and redacted even if those terms fall into a PII category they are interested in detected. For example, a police department might want personal identifiers redacted in most cases except for terms like “police officer”, “suspect”, and “witness”. 

Customers can now adapt the PII service’s detecting by specifying their own regex using a regex recognition configuration file. See our [container how-to guides](use-containers.md) for a tutorial on how to install and run Personally Identifiable Information (PII) Detection containers. 

A more detailed tutorial can be found in the “Adapting PII to your domain” how-to guide. 


## Submitting data

Analysis is performed upon receipt of the request. Using the PII detection feature synchronously is stateless. No data is stored in your account, and results are returned immediately in the response.

[!INCLUDE [asynchronous-result-availability](../../includes/async-result-availability.md)]

## Getting PII results

When you get results from PII detection, you can stream the results to an application or save the output to a file on the local system. The API response includes [recognized entities](../concepts/entity-categories.md), including their categories and subcategories, and confidence scores. The text string with the PII entities redacted is also returned.

## Service and data limits

[!INCLUDE [service limits article](../../includes/service-limits-link.md)]

## Next steps

[Personally Identifying Information (PII) overview](../overview.md)
