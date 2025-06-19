---
title: PersonName prebuilt entity - LUIS
titleSuffix: Azure AI services
description: This article contains personName prebuilt entity information in Language Understanding (LUIS).
ms.author: lajanuar
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.topic: reference
ms.date: 06/12/2025
---

# PersonName prebuilt entity for a LUIS app

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]

The prebuilt personName entity detects people names. Because this entity is already trained, you do not need to add example utterances containing personName to the application intents. personName entity is supported in English and Chinese [cultures](luis-reference-prebuilt-entities.md).

## Resolution for personName entity

The following entity objects are returned for the query:

`Is Jill Jones in Cairo?`


#### [V3 response](#tab/V3)


The following JSON is with the `verbose` parameter set to `false`:

```json
"entities": {
    "personName": [
        "Jill Jones"
    ]
}
```
#### [V3 verbose response](#tab/V3-verbose)
The following JSON is with the `verbose` parameter set to `true`:

```json
"entities": {
    "personName": [
        "Jill Jones"
    ],
    "$instance": {
        "personName": [
            {
                "type": "builtin.personName",
                "text": "Jill Jones",
                "startIndex": 3,
                "length": 10,
                "modelTypeId": 2,
                "modelType": "Prebuilt Entity Extractor",
                "recognitionSources": [
                    "model"
                ]
            }
        ],
    }
}
```
#### [V2 response](#tab/V2)

The following example shows the resolution of the **builtin.personName** entity.

```json
"entities": [
{
    "entity": "Jill Jones",
    "type": "builtin.personName",
    "startIndex": 3,
    "endIndex": 12
}
]
```
* * *

## Next steps



Learn about the [email](luis-reference-prebuilt-email.md), [number](luis-reference-prebuilt-number.md), and [ordinal](luis-reference-prebuilt-ordinal.md) entities.
