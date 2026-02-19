---
title: Upgrade to Read v3.0 of Azure Vision in Foundry Tools API
titleSuffix: Foundry Tools
description: Learn how to upgrade to Azure Vision in Foundry Tools v3.0 Read API from v2.0/v2.1.
author: PatrickFarley
manager: nitinme

ms.service: azure-ai-vision
ms.topic: upgrade-and-migration-article
ms.date: 09/26/2025
ms.author: pafarley
ROBOTS: NOINDEX
ms.custom: cogserv-non-critical-vision
---

# Upgrade from Read v2.x to Read v3.x

This guide shows how to upgrade your existing container or cloud API code from Read v2.x to Read v3.x.

## Determine your API path
Use the following table to determine the **version string** in the API path based on the Read 3.x version you're migrating to.

|Product type| Version | Version string in 3.x API path |
|:-----|:----|:----|
|Service | Read 3.0, 3.1, or 3.2 | **v3.0**, **v3.1**, or **v3.2** respectively |
|Service | Read 3.2 preview | **v3.2-preview.1** |
|Container | Read 3.0 preview or Read 3.1 preview | **v3.0** or **v3.1-preview.2** respectively |


Next, use the following sections to narrow your operations and replace the **version string** in your API path with the value from the table. For example, for **Read v3.2 preview** cloud and container versions, update the API path to **https://{endpoint}/vision/v3.2-preview.1/read/analyze[?language]**.

## Service/Container

### `Batch Read File`

|Read 2.x |Read 3.x  |
|----------|-----------|
|https://{endpoint}/vision/**v2.0/read/core/asyncBatchAnalyze**     |https://{endpoint}/vision/<**version string**>/read/analyze[?language]|
    
A new optional _language_ parameter is available. If you don't know the language of your document, or it might be multilingual, don't include it. 

### `Get Read Results`

|Read 2.x |Read 3.x  |
|----------|-----------|
|https://{endpoint}/vision/**v2.0/read/operations**/{operationId}     |https://{endpoint}/vision/<**version string**>/read/analyzeResults/{operationId}|

### `Get Read Operation Result` status flag

When the call to `Get Read Operation Result` succeeds, it returns a status string in the JSON body.
 
|Read 2.x |Read 3.x  |
|----------|-----------|
|`"NotStarted"` |    `"notStarted"`|
|`"Running"` | `"running"`|
|`"Failed"` | `"failed"`|
|`"Succeeded"` | `"succeeded"`|
    
### API response (JSON) 

Note the following changes to the JSON:
* In v2.x, `Get Read Operation Result` returns the OCR recognition JSON when the status is `Succeeded"`. In v3.0, this field is `succeeded`.
* To get the root for page array,  change the JSON hierarchy from `recognitionResults` to `analyzeResult`/`readResults`. The per-page line and words JSON hierarchy remains unchanged, so no code changes are required.
* The page angle `clockwiseOrientation` is renamed to `angle` and the range changes from 0 - 360 degrees to -180 to 180 degrees. Depending on your code, you might need to make changes as most math functions can handle either range.

The v3.0 API also introduces the following improvements you can optionally use:
* `createdDateTime` and `lastUpdatedDateTime` so you can track the duration of processing. 
* `version` tells you the version of the API used to generate results.
* A per-word `confidence`. This value is calibrated so that a value 0.95 means that there is a 95% chance the recognition is correct. Use the confidence score to select which text to send to human review. 
    
    
In version 2.X, the output format is as follows: 
    
```json
{
    {
    "status": "Succeeded",
    "recognitionResults": [
        {
        "page": 1,
        "language": "en",
        "clockwiseOrientation": 349.59,
        "width": 2661,
        "height": 1901,
        "unit": "pixel",
        "lines": [
            {
            "boundingBox": [
                67,
                646,
                2582,
                713,
                2580,
                876,
                67,
                821
            ],
            "text": "The quick brown fox jumps",
            "words": [
                {
                "boundingBox": [
                    143,
                    650,
                    435,
                    661,
                    436,
                    823,
                    144,
                    824
                ],
                "text": "The",
                },
        // The rest of result is omitted for brevity 
            
}
```
    
In v3.0, it has been adjusted:
    
```json
{
    {
    "status": "succeeded",
    "createdDateTime": "2020-05-28T05:13:21Z",
    "lastUpdatedDateTime": "2020-05-28T05:13:22Z",
    "analyzeResult": {
    "version": "3.0.0",
    "readResults": [
        {
        "page": 1,
        "language": "en",
        "angle": 0.8551,
        "width": 2661,
        "height": 1901,
        "unit": "pixel",
        "lines": [
            {
            "boundingBox": [
                67,
                646,
                2582,
                713,
                2580,
                876,
                67,
                821
            ],
            "text": "The quick brown fox jumps",
            "words": [
                {
                "boundingBox": [
                    143,
                    650,
                    435,
                    661,
                    436,
                    823,
                    144,
                    824
                ],
                "text": "The",
                "confidence": 0.958
                },
// The rest of result is omitted for brevity 
    
}
```

## Cloud service only

### `Recognize Text`
`Recognize Text` is a *preview* operation that is *deprecated in all versions of Azure Vision API*. You must migrate from `Recognize Text` to `Read` (v3.0) or `Batch Read File` (v2.0, v2.1). Version 3.0 of `Read` includes newer, better models for text recognition and other features, so we recommend it. To upgrade from `Recognize Text` to `Read`:

|Recognize Text 2.x |Read 3.x  |
|----------|-----------|
|https://{endpoint}/vision/**v2.0/recognizeText[?mode]**|https://{endpoint}/vision/<**version string**>/read/analyze[?language]|
    
`Recognize Text` supports the _mode_ parameter, but `Read` doesn't support it. `Read` automatically supports both handwritten and printed text.
    
`Read` introduces a new optional _language_ parameter in v3.0. If you don't know the language of your document, or it might be multilingual, don't include it. 

### `Get Recognize Text Operation Result`

|Recognize Text 2.x |Read 3.x  |
|----------|-----------|
|https://{endpoint}/vision/**v2.0/textOperations/**{operationId}|https://{endpoint}/vision/<**version string**>/read/analyzeResults/{operationId}|

### `Get Recognize Text Operation Result` status flags
When the call to `Get Recognize Text Operation Result` succeeds, it returns a status string field in the JSON body. 
 
|Recognize Text 2.x |Read 3.x  |
|----------|-----------|
|`"NotStarted"` |    `"notStarted"`|
|`"Running"` | `"running"`|
|`"Failed"` | `"failed"`|
|`"Succeeded"` | `"succeeded"`|

### API response (JSON)

Note the following changes to the JSON:    
* In version 2.x, `Get Read Operation Result` returns the OCR recognition JSON when the status is `Succeeded`. In version 3.x, this field is `succeeded`.
* To get the root for the page array, change the JSON hierarchy from `recognitionResult` to `analyzeResult`/`readResults`. The per-page line and words JSON hierarchy remains unchanged, so no code changes are required.

The version 3.0 API also introduces the following improvements you can optionally use. See the API reference for more details:
* `createdDateTime` and `lastUpdatedDateTime` so you can track the duration of processing. 
* `version` tells you the version of the API used to generate results.
* A per-word `confidence`. This value is calibrated so that a value 0.95 means that there is a 95% chance the recognition is correct. Use the confidence score to select which text to send to human review. 
* `angle` general orientation of the text in clockwise direction, measured in degrees between (-180, 180].
* `width` and `height` give you the dimensions of your document, and `unit` provides the unit of those dimensions (pixels or inches, depending on document type.)
* `page` multipage documents are supported.
* `language` the input language of the document (from the optional _language_ parameter.)


In version 2.X, the output format is as follows: 
    
```json
{
    {
    "status": "Succeeded",
    "recognitionResult": [
        {
        "lines": [
            {
            "boundingBox": [
                67,
                646,
                2582,
                713,
                2580,
                876,
                67,
                821
            ],
            "text": "The quick brown fox jumps",
            "words": [
                {
                "boundingBox": [
                    143,
                    650,
                    435,
                    661,
                    436,
                    823,
                    144,
                    824
                ],
                "text": "The",
                },
// The rest of result is omitted for brevity 
        
}
```
    
In version 3.x, it's adjusted:
    
```json
{
    {
    "status": "succeeded",
    "createdDateTime": "2020-05-28T05:13:21Z",
    "lastUpdatedDateTime": "2020-05-28T05:13:22Z",
    "analyzeResult": {
    "version": "3.0.0",
    "readResults": [
        {
        "page": 1,
        "angle": 0.8551,
        "width": 2661,
        "height": 1901,
        "unit": "pixel",
        "lines": [
            {
            "boundingBox": [
                67,
                646,
                2582,
                713,
                2580,
                876,
                67,
                821
            ],
            "text": "The quick brown fox jumps",
            "words": [
                {
                "boundingBox": [
                    143,
                    650,
                    435,
                    661,
                    436,
                    823,
                    144,
                    824
                ],
                "text": "The",
                "confidence": 0.958
                },
// The rest of result is omitted for brevity 
    
}
```

## Container only

### `Synchronous Read`

|Read 2.0 |Read 3.x  |
|----------|-----------|
|https://{endpoint}/vision/**v2.0/read/core/Analyze**     |https://{endpoint}/vision/<**version string**>/read/syncAnalyze[?language]|
