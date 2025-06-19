---
title: Ordinal V2 prebuilt entity - LUIS
titleSuffix: Azure AI services
description: This article contains ordinal V2 prebuilt entity information in Language Understanding (LUIS).
ms.author: lajanuar
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.topic: reference
ms.date: 06/12/2025
---

# Ordinal V2 prebuilt entity for a LUIS app

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]

Ordinal V2 number expands [Ordinal](luis-reference-prebuilt-ordinal.md) to provide relative references such as `next`, `last`, and `previous`. These are not extracted using the ordinal prebuilt entity.

## Resolution for prebuilt ordinal V2 entity

The following entity objects are returned for the query:

`what is the second to last choice in the list`

#### [V3 response](#tab/V3)

The following JSON is with the `verbose` parameter set to `false`:

```json
"entities": {
    "ordinalV2": [
        {
            "offset": -1,
            "relativeTo": "end"
        }
    ]
}
```

#### [V3 verbose response](#tab/V3-verbose)

The following JSON is with the `verbose` parameter set to `true`:

```json
"entities": {
    "ordinalV2": [
        {
            "offset": -1,
            "relativeTo": "end"
        }
    ],
    "$instance": {
        "ordinalV2": [
            {
                "type": "builtin.ordinalV2.relative",
                "text": "the second to last",
                "startIndex": 8,
                "length": 18,
                "modelTypeId": 2,
                "modelType": "Prebuilt Entity Extractor",
                "recognitionSources": [
                    "model"
                ]
            }
        ]
    }
}
```
#### [V2 response](#tab/V2)

The following example shows the resolution of the **builtin.ordinalV2** entity.

```json
"entities": [
    {
        "entity": "the second to last",
        "type": "builtin.ordinalV2.relative",
        "startIndex": 8,
        "endIndex": 25,
        "resolution": {
            "offset": "-1",
            "relativeTo": "end"
        }
    }
]
```
* * *

## Next steps



Learn about the [percentage](luis-reference-prebuilt-percentage.md), [phone number](luis-reference-prebuilt-phonenumber.md), and [temperature](luis-reference-prebuilt-temperature.md) entities.
