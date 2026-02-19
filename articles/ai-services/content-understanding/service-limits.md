---
title: Service quotas and limits - Content Understanding
titleSuffix: Foundry Tools
description: Quick reference, detailed description, and best practices for working within Azure Content Understanding in Foundry Tools service Quotas and Limits
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: limits-and-quotas
ms.custom:
  - build-2025
---


# Azure Content Understanding in Foundry Tools service quotas and limits

This article lists the quotas and limits for the Azure Content Understanding in Foundry Tools service.

## General limits

| Property | Limit |
| --- | --- |
| Analyzer ID | 1-64 characters. Alphanumeric, period, and underscore. Pattern: `[a-zA-Z0-9._]{1,64}` |
| URL properties | ≤ 8,192 characters |
| Description properties | ≤ 1,024 characters |
| Field names | ≤ 64 characters. Unicode letters, numbers, combining marks, connecting punctuation, period, hyphen, and underscore. Pattern: `[\p{L}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}._-]{1,64}` |
| Tags | ≤ 10 tags |
| Tag key | ≤ 64 characters. Alphanumeric and `+ - . : = _ /` characters. Pattern: `[a-zA-Z0-9+-.:=_/]{1,64}` |
| Tag value | ≤ 256 characters. Alphanumeric and `+ - . : = _ /` characters. Can be empty. Pattern: `[a-zA-Z0-9+-.:=_/]{0,256}` |
| Image reference ID | ≤ 256 characters |

## Resource limits

| Quota | Standard (S0) |
| --- | --- |
| Max analyzers | 100,000 |
| Max analysis/min | 1,000 pages/images <br> Four hours of audio <br> Four hours of video  |
| Max operations/min | 3,000 |

## Supported generative models

Content Understanding connects to Foundry Models for generative capabilities. The service is periodically updated to add support for more models. To learn more, see [Connect your Content Understanding analyzer to Foundry model deployments](./concepts/models-deployments.md).  

The currently supported models are:

| Model Type | Model | Version |
|--|--|--|
|Chat Completion | gpt-4o | `2024-08-06` |
|Chat Completion | gpt-4o | `2024-11-20` |
|Chat Completion | gpt-4o-mini | `2024-11-20` |
|Chat Completion | gpt-4.1 | `2024-11-20` |
|Chat Completion | gpt-4.1-mini | `2024-11-20` |
|Chat Completion | gpt-4.1-nano | `2024-11-20` |
|Embeddings | text-embedding-3-small |  |
|Embeddings | text-embedding-3-large |  |
|Embeddings | text-embedding-ada-002 |  |

## Input file limits

### Document and text

| Supported file types | File size | Length |
| --- | --- | --- |
| ✓ `.pdf`<br> ✓ `.tiff`<br> ✓ `.jpg`, `.jpeg`, `.jpe`, `.png`, `.bmp`, `.heif`, `.heic` | ≤ 200 MB | ≤ 300 pages |
| ✓ `.docx`, `.xlsx`, `.pptx` | ≤ 200 MB | ≤ 1M characters |
| ✓ `.txt` <br/> ✓ `.html`, `.md`, `.rtf` <br/> ✓ `.eml`, `.msg` <br/> ✓ `.xml`| ≤ 1 MB | ≤ 1M characters |

> [!NOTE]
> [Pro mode (preview)](./concepts/standard-pro-modes.md) currently only supports .pdf, .tiff, and image file types as input.
> Total input can't exceed 100 MB and 150 pages.

### Image

| Supported file types | File size | Resolution |
| --- | --- | --- |
| ✓ `.jpg`, `.jpeg`, `.jpe`, `.png`, `.bmp`, `.heif`, `.heic` | ≤ 200 MB | Min: 50 x 50 pixels <br> Max: 10k x 10k pixels |

### Audio

| Supported file types | File size | Length |
| --- | --- |  --- |
| ✓ `.wav` (PCM, A-law, μ-law) <br> ✓ `.mp3` <br> ✓ `.mp4` <br> ✓ `.opus`, `.ogg` (Opus)<br> ✓ `.flac` <br> ✓ `.wma` <br> ✓ `.aac` <br> ✓ `.amr` (AMR-NB, AMR-WB) <br> ✓ `.3gp` (AMR-NB, AMR-WB)<br> ✓ `.webm` (Opus, Vorbis) <br> ✓ `.m4a` (AAC, ALAC)<br> ✓ `.spx` | Max: 300 MB<sup>†</sup> | Max: 2 hours<sup>†</sup> |

<sup>†</sup> Content Understanding supports audio files up to 1 GB and 4 hours in duration, but transcription time is substantially reduced for files 300 MB or less or 2 hours or less.

### Video

#### Supported file types and resolution

| Supported File Types | Resolution |
| --- | --- |
| ✓  `.mp4`, `.m4v` <br> ✓ `.flv` (H.264 and `AAC`) <br> ✓ `.wmv`, `.asf` <br> ✓ `.avi` <br> ✓ `.mkv` <br> ✓ `.mov` | Min: 320 x 240 pixels <br>Max: 1920 x 1,080 pixels |

#### File size limits

| Upload Method | File Size | Length | Description |
| --- | --- | --- | --- |
| analyzeBinary API (direct upload) | ≤ 200 MB | ≤ 30 minutes | Upload video files directly in the API request body by using the analyzeBinary API. The Microsoft Foundry UX and Content Understanding Studio UX use this method.  |
| analyze API (file reference) | Max: 4 GB | Max: 2 hours | Reference video files via URL from Azure Blob Storage or similar storage when you use the analyze API. |

> [!NOTE]
> Video analysis has the following limitations:
> * analyzeBinary API: Maximum file size of 200 MB and maximum duration of 30 minutes when uploading video directly in the request body
> * Frame sampling: Analyzes approximately one frame per second, which might miss quick movements or brief events
> * Resolution: All frames are scaled to 512 x 512 pixels, which might affect visibility of small details or distant objects


## Field schema limits

Content Understanding supports both basic field value types and nested structures, including lists, groups, tables, and fixed tables.

* **Basic field value types**: *string*, *date*, *time*, *number*, *integer*, and *boolean*.
* **List field**: A sequence of values of the same type, represented as an array of basic fields in the API.
* **Group field**: A set of semantically related fields, represented as an object of basic fields in the API.
* **Table field**: A variable number of items with fixed subfields, represented as an array of objects of basic fields in the API.
* **Fixed table field**: A group of fields with shared subfields, represented as an object of objects of basic fields in the API.

### Basic limits

| Property | Document | Text | Image | Audio | Video |
| --- | --- | --- | --- | --- | --- |
| Max fields | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 |
| Max classify field categories | 300 | 300 | 300 | 300 | 300 |
| Supported generation methods | extract<br>generate<br>classify | generate<br>classify | generate<br>classify | generate<br>classify | generate<br>classify |

* The *Max fields* limit includes all named fields. For example, a list of strings counts as one field, while a group with string and number subfields counts as three fields. 
* The *Max classify field categories* limit is the total number of categories across all fields using the `classify` generation method.

## Knowledge source limits

| Type | Limits |
| -----| ------ |
| Training data | Documents only <br/> 1 GB total <br/> 50,000 pages/images total |


## Segmentation and classification limits

> [!NOTE]
> These limits apply to [Content Understanding segmentation and classification](concepts/classifier.md) itself. They don't apply to classifying fields within the extraction capability.

| Property | Limit |
| --- | --- |
| Category name | Can't start with a dollar sign (`$`).|
| Category name and description | Maximum 120 characters for combined name and description in each category. |
| Number of categories | 200 per analyzer for documents, 1 for videos. |
| Hierarchical classification | 5 layers for documents, 2 layers for videos |





