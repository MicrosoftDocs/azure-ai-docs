---
title: How to perform Named Entity Recognition (NER)
titleSuffix: Foundry Tools
description: This article shows you how to extract named entities from text.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-ner, ignite-2024
---
# How to use Named Entity Recognition (NER)

The NER feature can evaluate unstructured text, and extract named entities from text in several predefined categories, for example: person, location, event, product, and organization.  

## Development options

[!INCLUDE [development options](./includes/development-options.md)]

## Determine how to process the data (optional)

### Input languages

When you submit input text to be processed, you can specify which of [the supported languages](language-support.md) they're written in. If you don't specify a language, key phrase extraction defaults to English. The API may return offsets in the response to support different [multilingual and emoji encodings](../concepts/multilingual-emoji-support.md). 

## Submitting data

Analysis is performed upon receipt of the request. Using the NER feature synchronously is stateless. No data is stored in your account, and results are returned immediately in the response.

[!INCLUDE [asynchronous-result-availability](../includes/async-result-availability.md)]

The API attempts to detect the [defined entity categories](concepts/named-entity-categories.md) for a given input text language. 

## Getting NER results

When you get results from NER, you can stream the results to an application or save the output to a file on the local system. The API response includes [recognized entities](concepts/named-entity-categories.md), including their categories and subcategories, and confidence scores. 

## Select which entities to be returned

The API attempts to detect the [defined entity types and tags](concepts/named-entity-categories.md) for a given input text language. The entity types and tags replace the categories and subcategories structure the older models use to define entities for more flexibility. You can also specify which entities are detected and returned, use the optional `inclusionList` and `exclusionList` parameters with the appropriate entity types. The following example would detect only `Location`. You can specify one or more [entity types](concepts/named-entity-categories.md) to be returned. Given the types and tags hierarchy introduced for this version, you have the flexibility to filter on different granularity levels as so:

**Input:**

> [!NOTE]
> In this example, it returns only the **"Location"** entity type.

```bash
{
    "kind": "EntityRecognition",
    "parameters": 
    {
        "inclusionList" :
        [
            "Location"
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
    }
}

```

The above examples would return entities falling under the `Location` entity type such as the `GPE`, `Structural`, and `Geological` tagged entities as [outlined by entity types and tags](concepts/named-entity-categories.md). We could also further filter the returned entities by filtering using one of the entity tags for the `Location` entity type such as filtering over `GPE` tag only as outlined:

```bash

    "parameters": 
    {
        "inclusionList" :
        [
            "GPE"
        ]
    }
    
```

This method returns all `Location` entities only falling under the `GPE` tag and ignore any other entity falling under the `Location` type that is tagged with any other entity tag such as `Structural` or `Geological` tagged `Location` entities. We can also further analyze our results by using the `exclusionList` parameter. `GPE` tagged entities could be tagged with the following tags: `City`, `State`, `CountryRegion`, `Continent`. We could, for example, exclude `Continent` and `CountryRegion` tags for our example:

```bash

    "parameters": 
    {
        "inclusionList" :
        [
            "GPE"
        ],
        "exclusionList": :
        [
            "Continent",
            "CountryRegion"
        ]
    }
    
```

Using these parameters we can successfully filter on only `Location` entity types, since the `GPE` entity tag included in the `inclusionList` parameter, falls under the `Location` type. We then filter on only Geopolitical entities and exclude any entities tagged with `Continent` or `CountryRegion` tags.

## Supported output attributes

In order to provide users with more insight into an entity's types and provide increased usability, NER supports these attributes in the output:

|Name of the attribute|Type        |Definition                               |
|---------------------|------------|-----------------------------------------|
|`type`               |String      |The most specific type of detected entity.<br><br>For example, "Seattle" is a `City`, a `GPE` (Geo Political Entity) and a `Location`. The most granular classification for "Seattle" is `City`. The type is `City` for the text "Seattle."|
|`tags`               |List (tags) |A list of tag objects that expresses the affinity of the detected entity to a hierarchy or any other grouping.<br><br>A tag contains two fields:<br>- `name`: A unique name for the tag.<br>- `confidenceScore`: The associated confidence score for a tag ranging from 0 to 1.<br><br>This unique tagName is used to filter in the `inclusionList` and `exclusionList` parameters.
|`metadata`           |Object      |Metadata is an object containing more data about the entity type detected. It changes based on the field `metadataKind`.

## Sample output

This sample output includes an example of output attributes.

```bash
{ 
    "kind": "EntityRecognitionResults", 
    "results": { 
        "documents": [ 
            { 
                "id": "1", 
                "entities": [ 
                    { 
                        "text": "Microsoft", 
                        "category": "Organization", 
                        "type": "Organization", 
                        "offset": 0, 
                        "length": 9, 
                        "confidenceScore": 0.97, 
                        "tags": [ 
                            { 
                                "name": "Organization", 
                                "confidenceScore": 0.97 
                            } 
                        ] 
                    }, 
                    { 
                        "text": "One", 
                        "category": "Quantity", 
                        "type": "Number", 
                        "subcategory": "Number", 
                        "offset": 21, 
                        "length": 3, 
                        "confidenceScore": 0.9, 
                        "tags": [ 
                            { 
                                "name": "Number", 
                                "confidenceScore": 0.8 
                            }, 
                            { 
                                "name": "Quantity", 
                                "confidenceScore": 0.8 
                            }, 
                            { 
                                "name": "Numeric", 
                                "confidenceScore": 0.8 
                            } 
                        ], 
                        "metadata": { 
                            "metadataKind": "NumberMetadata", 
                            "numberKind": "Integer", 
                            "value": 1.0 
                        } 
                    } 
                ], 
                "warnings": [] 
            } 
        ], 
        "errors": [], 
        "modelVersion": "2023-09-01" 
    } 
} 
```

## Specify the NER model

By default, this feature uses the latest available AI model on your text. You can also configure your API requests to use a specific [model version](../concepts/model-lifecycle.md).

## Service and data limits

[!INCLUDE [service limits article](../includes/service-limits-link.md)]

## Next steps

[Named Entity Recognition overview](overview.md)
