---
title: DatetimeV2 Prebuilt entities - LUIS
titleSuffix: Azure AI services
description: This article has datetimeV2 prebuilt entity information in Language Understanding (LUIS).
ms.author: lajanuar
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.topic: reference
ms.date: 06/12/2025
---

# DatetimeV2 prebuilt entity for a LUIS app

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]


The **datetimeV2** prebuilt entity extracts date and time values. These values resolve in a standardized format for client programs to consume. When an utterance has a date or time that isn't complete, LUIS includes _both past and future values_ in the endpoint response. Because this entity is already trained, you do not need to add example utterances containing datetimeV2 to the application intents.

## Types of datetimeV2
DatetimeV2 is managed from the [Recognizers-text](https://github.com/Microsoft/Recognizers-Text/blob/master/Patterns/English/English-DateTime.yaml) GitHub repository.

## Example JSON

The following utterance and its partial JSON response is shown below.

`8am on may 2nd 2019`

#### [V3 response](#tab/1-1)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "datetime",
            "values": [
                {
                    "timex": "2019-05-02T08",
                    "resolution": [
                        {
                            "value": "2019-05-02 08:00:00"
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### [V3 verbose response](#tab/1-2)

```json

"entities": {
    "datetimeV2": [
        {
            "type": "datetime",
            "values": [
                {
                    "timex": "2019-05-02T08",
                    "resolution": [
                        {
                            "value": "2019-05-02 08:00:00"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.datetime",
                "text": "8am on may 2nd 2019",
                "startIndex": 0,
                "length": 19,
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

#### [V2 response](#tab/1-3)

```json
"entities": [
  {
    "entity": "8am on may 2nd 2019",
    "type": "builtin.datetimeV2.datetime",
    "startIndex": 0,
    "endIndex": 18,
    "resolution": {
      "values": [
        {
          "timex": "2019-05-02T08",
          "type": "datetime",
          "value": "2019-05-02 08:00:00"
        }
      ]
    }
  }
]
 ```

|Property name |Property type and description|
|---|---|
|Entity|**string** - Text extracted from the utterance with type of date, time, date range, or time range.|
|type|**string** - One of the [subtypes of datetimeV2](#subtypes-of-datetimev2)
|startIndex|**int** - The index in the utterance at which the entity begins.|
|endIndex|**int** - The index in the utterance at which the entity ends.|
|resolution|Has a `values` array that has one, two, or four [values of resolution](#values-of-resolution).|
|end|The end value of a time, or date range, in the same format as `value`. Only used if `type` is `daterange`, `timerange`, or `datetimerange`|

* * *

## Subtypes of datetimeV2

The **datetimeV2** prebuilt entity has the following subtypes, and examples of each are provided in the table that follows:
* `date`
* `time`
* `daterange`
* `timerange`
* `datetimerange`


## Values of resolution
* The array has one element if the date or time in the utterance is fully specified and unambiguous.
* The array has two elements if the datetimeV2 value is ambiguous. Ambiguity includes lack of specific year, time, or time range. See [Ambiguous dates](#ambiguous-dates) for examples. When the time is ambiguous for A.M. or P.M., both values are included.
* The array has four elements if the utterance has two elements with ambiguity. This ambiguity includes elements that have:
  * A date or date range that is ambiguous as to year
  * A time or time range that is ambiguous as to A.M. or P.M. For example, 3:00 April 3rd.

Each element of the `values` array may have the following fields:

|Property name|Property description|
|--|--|
|timex|time, date, or date range expressed in TIMEX format that follows the [ISO 8601 standard](https://en.wikipedia.org/wiki/ISO_8601) and the TIMEX3 attributes for annotation using the TimeML language.|
|mod|term used to describe how to use the value such as `before`, `after`.|
|type|The subtype, which can be one of the following items: `datetime`, `date`, `time`, `daterange`, `timerange`, `datetimerange`, `duration`, `set`.|
|value|**Optional.** A datetime object in the Format yyyy-MM-dd  (date), HH:mm:ss (time) yyyy-MM-dd HH:mm:ss (datetime). If `type` is `duration`, the value is the number of seconds (duration) <br/> Only used if `type` is `datetime` or `date`, `time`, or `duration.|

## Valid date values

The **datetimeV2** supports dates between the following ranges:

| Min | Max |
|----------|-------------|
| 1st January 1900   | 31st December 2099 |

## Ambiguous dates

If the date can be in the past or future, LUIS provides both values. An example is an utterance that includes the month and date without the year.

For example, given the following utterance:

`May 2nd`

* If today's date is May 3rd 2017, LUIS provides both "2017-05-02" and "2018-05-02" as values.
* When today's date is May 1st 2017, LUIS provides both "2016-05-02" and "2017-05-02" as values.

The following example shows the resolution of the entity "may 2nd". This resolution assumes that today's date is a date between May 2nd 2017 and May 1st 2018.
Fields with `X` in the `timex` field are parts of the date that aren't explicitly specified in the utterance.

## Date resolution example


The following utterance and its partial JSON response is shown below.

`May 2nd`

#### [V3 response](#tab/2-1)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "date",
            "values": [
                {
                    "timex": "XXXX-05-02",
                    "resolution": [
                        {
                            "value": "2019-05-02"
                        },
                        {
                            "value": "2020-05-02"
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### [V3 verbose response](#tab/2-2)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "date",
            "values": [
                {
                    "timex": "XXXX-05-02",
                    "resolution": [
                        {
                            "value": "2019-05-02"
                        },
                        {
                            "value": "2020-05-02"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.date",
                "text": "May 2nd",
                "startIndex": 0,
                "length": 7,
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

#### [V2 response](#tab/2-3)

```json
  "entities": [
    {
      "entity": "may 2nd",
      "type": "builtin.datetimeV2.date",
      "startIndex": 0,
      "endIndex": 6,
      "resolution": {
        "values": [
          {
            "timex": "XXXX-05-02",
            "type": "date",
            "value": "2019-05-02"
          },
          {
            "timex": "XXXX-05-02",
            "type": "date",
            "value": "2020-05-02"
          }
        ]
      }
    }
  ]
```
* * *

## Date range resolution examples for numeric date

The `datetimeV2` entity extracts date and time ranges. The `start` and `end` fields specify the beginning and end of the range. For the utterance `May 2nd to May 5th`, LUIS provides **daterange** values for both the current year and the next year. In the `timex` field, the `XXXX` values indicate the ambiguity of the year. `P3D` indicates the time period is three days long.

The following utterance and its partial JSON response is shown below.

`May 2nd to May 5th`

#### [V3 response](#tab/3-1)

```json

"entities": {
    "datetimeV2": [
        {
            "type": "daterange",
            "values": [
                {
                    "timex": "(XXXX-05-02,XXXX-05-05,P3D)",
                    "resolution": [
                        {
                            "start": "2019-05-02",
                            "end": "2019-05-05"
                        },
                        {
                            "start": "2020-05-02",
                            "end": "2020-05-05"
                        }
                    ]
                }
            ]
        }
    ]
}
```


#### [V3 verbose response](#tab/3-2)

```json

"entities": {
    "datetimeV2": [
        {
            "type": "daterange",
            "values": [
                {
                    "timex": "(XXXX-05-02,XXXX-05-05,P3D)",
                    "resolution": [
                        {
                            "start": "2019-05-02",
                            "end": "2019-05-05"
                        },
                        {
                            "start": "2020-05-02",
                            "end": "2020-05-05"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.daterange",
                "text": "May 2nd to May 5th",
                "startIndex": 0,
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

#### [V2 response](#tab/3-3)

```json
"entities": [
    {
      "entity": "may 2nd to may 5th",
      "type": "builtin.datetimeV2.daterange",
      "startIndex": 0,
      "endIndex": 17,
      "resolution": {
        "values": [
          {
            "timex": "(XXXX-05-02,XXXX-05-05,P3D)",
            "type": "daterange",
            "start": "2019-05-02",
            "end": "2019-05-05"
          }
        ]
      }
    }
  ]
```
* * *

## Date range resolution examples for day of week

The following example shows how LUIS uses **datetimeV2** to resolve the utterance `Tuesday to Thursday`. In this example, the current date is June 19th. LUIS includes **daterange** values for both of the date ranges that precede and follow the current date.

The following utterance and its partial JSON response is shown below.

`Tuesday to Thursday`

#### [V3 response](#tab/4-1)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "daterange",
            "values": [
                {
                    "timex": "(XXXX-WXX-2,XXXX-WXX-4,P2D)",
                    "resolution": [
                        {
                            "start": "2019-10-08",
                            "end": "2019-10-10"
                        },
                        {
                            "start": "2019-10-15",
                            "end": "2019-10-17"
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### [V3 verbose response](#tab/4-2)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "daterange",
            "values": [
                {
                    "timex": "(XXXX-WXX-2,XXXX-WXX-4,P2D)",
                    "resolution": [
                        {
                            "start": "2019-10-08",
                            "end": "2019-10-10"
                        },
                        {
                            "start": "2019-10-15",
                            "end": "2019-10-17"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.daterange",
                "text": "Tuesday to Thursday",
                "startIndex": 0,
                "length": 19,
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

#### [V2 response](#tab/4-3)

```json
  "entities": [
    {
      "entity": "tuesday to thursday",
      "type": "builtin.datetimeV2.daterange",
      "startIndex": 0,
      "endIndex": 19,
      "resolution": {
        "values": [
          {
            "timex": "(XXXX-WXX-2,XXXX-WXX-4,P2D)",
            "type": "daterange",
            "start": "2019-04-30",
            "end": "2019-05-02"
          }
        ]
      }
    }
  ]
```
* * *

## Ambiguous time
The values array has two time elements if the time, or time range is ambiguous. When there's an ambiguous time, values have both the A.M. and P.M. times.

## Time range resolution example

DatetimeV2 JSON response has changed in the API V3. The following example shows how LUIS uses **datetimeV2** to resolve the utterance that has a time range.

Changes from API V2:
* `datetimeV2.timex.type` property is no longer returned because it is returned at the parent level, `datetimev2.type`.
* The `datetimeV2.value` property has been renamed to `datetimeV2.timex`.

The following utterance and its partial JSON response is shown below.

`from 6pm to 7pm`

#### [V3 response](#tab/5-1)

The following JSON is with the `verbose` parameter set to `false`:

```JSON

"entities": {
    "datetimeV2": [
        {
            "type": "timerange",
            "values": [
                {
                    "timex": "(T18,T19,PT1H)",
                    "resolution": [
                        {
                            "start": "18:00:00",
                            "end": "19:00:00"
                        }
                    ]
                }
            ]
        }
    ]
}
```
#### [V3 verbose response](#tab/5-2)

The following JSON is with the `verbose` parameter set to `true`:

```json

"entities": {
    "datetimeV2": [
        {
            "type": "timerange",
            "values": [
                {
                    "timex": "(T18,T19,PT1H)",
                    "resolution": [
                        {
                            "start": "18:00:00",
                            "end": "19:00:00"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.timerange",
                "text": "from 6pm to 7pm",
                "startIndex": 0,
                "length": 15,
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
#### [V2 response](#tab/5-3)

```json
  "entities": [
    {
      "entity": "6pm to 7pm",
      "type": "builtin.datetimeV2.timerange",
      "startIndex": 0,
      "endIndex": 9,
      "resolution": {
        "values": [
          {
            "timex": "(T18,T19,PT1H)",
            "type": "timerange",
            "start": "18:00:00",
            "end": "19:00:00"
          }
        ]
      }
    }
  ]
```

* * *

## Time resolution example

The following utterance and its partial JSON response is shown below.

`8am`

#### [V3 response](#tab/6-1)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "time",
            "values": [
                {
                    "timex": "T08",
                    "resolution": [
                        {
                            "value": "08:00:00"
                        }
                    ]
                }
            ]
        }
    ]
}
```
#### [V3 verbose response](#tab/6-2)

```json
"entities": {
    "datetimeV2": [
        {
            "type": "time",
            "values": [
                {
                    "timex": "T08",
                    "resolution": [
                        {
                            "value": "08:00:00"
                        }
                    ]
                }
            ]
        }
    ],
    "$instance": {
        "datetimeV2": [
            {
                "type": "builtin.datetimeV2.time",
                "text": "8am",
                "startIndex": 0,
                "length": 3,
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
#### [V2 response](#tab/6-3)

```json
"entities": [
  {
    "entity": "8am",
    "type": "builtin.datetimeV2.time",
    "startIndex": 0,
    "endIndex": 2,
    "resolution": {
      "values": [
        {
          "timex": "T08",
          "type": "time",
          "value": "08:00:00"
        }
      ]
    }
  }
]
```

* * *

## Deprecated prebuilt datetime

The `datetime` prebuilt entity is deprecated and replaced by **datetimeV2**.

To replace `datetime` with `datetimeV2` in your LUIS app, complete the following steps:

1. Open the **Entities** pane of the LUIS web interface.
2. Delete the **datetime** prebuilt entity.
3. Select **Add prebuilt entity**
4. Select **datetimeV2** and click **Save**.

## Next steps



Learn about the [dimension](luis-reference-prebuilt-dimension.md), [email](luis-reference-prebuilt-email.md) entities, and [number](luis-reference-prebuilt-number.md).
