---
title: Service quotas and limits - Content Understanding
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Content Understanding service Quotas and Limits
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.custom:
  - build-2025
---


# Azure AI Content Understanding service quotas and limits

This article offers a quick reference of the quotas and limits for the Azure AI Content Understanding service.

## Resource limits
| Quota | Standard (S0) |
| --- | --- |
| Max analyzers | 100k |
| Max classifiers | 100k |
| Max person directories | 100k |
| Max analysis/min | 1000 pages/images <br> Four hours of audio <br> Four hours of video  |
| Max operations/min | 3000 |

## General limits

| Property | Limit |
| --- | --- |
| Resource IDs | 1-64 characters (`[a-zA-Z0-9._-]{1,64}`) |
| URL properties | ≤ 8,192 characters |
| Description properties | ≤ 1,024 characters |
| Field names | ≤ 64 characters (`[\p{L}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}._-]{1,64}`) |
| Tags properties | ≤ 10 tags |
| Tag key | ≤ 64 characters (`[a-zA-Z0-9+-.:=_/]{1,64}`) |
| Tag value | ≤ 256 characters (`[a-zA-Z0-9+-.:=_/]{0,256}`) |
| Image reference ID | ≤ 256 characters |

## Analyzers

### Input file limits

#### Document and text

| Supported File Types | File Size | Length |
| --- | --- | --- |
| ✓ `.pdf`<br> ✓ `.tiff`<br> ✓ `.jpg`, `.png`, `.bmp`, `.heif` | ≤ 200 MB | ≤ 300 pages |
| ✓ `.docx`, `.xlsx`, `.pptx` | ≤ 200 MB | ≤ 1M characters |
| ✓ `.txt` <br/> ✓ `.html`, `.md`, `.rtf` <br/> ✓ `.eml`, `.msg` <br/> ✓ `.xml`| ≤ 1 MB | ≤ 1M characters |

> [!NOTE]
> [Pro mode](./concepts/standard-pro-modes.md) currently only supports .pdf, .tiff, and image file types as input.
> Total input may not exceed 100 MB and 150 pages.

#### Image

| Supported File Types | File Size | Resolution |
| --- | --- | --- |
| ✓ `.jpg`, `.png`, `.bmp`, `.heif` | ≤ 200 MB | Min: 50 x 50 pixels <br> Max: 10k x 10k pixels |

#### Audio

| Supported File Types | File Size | Length |
| --- | --- |  --- |
| ✓ `.wav` (`PCM`, A-law, μ-law) <br> ✓ `.mp3` <br> ✓ `.mp4` <br> ✓ `.opus`, `.ogg` (Opus)<br> ✓ `.flac` <br> ✓ `.wma` <br> ✓ `.aac` <br> ✓ `.amr` (AMR-NB, AMR-WB) <br> ✓ `.3gp` (AMR-NB, AMR-WB)<br> ✓ `.webm` (Opus, Vorbis) <br> ✓ `.m4a` (`AAC`, `ALAC`)<br> ✓ `.spx` | ≤ 1 GB<sup>†</sup> | ≤ 4 hours<sup>†</sup> |

<sup>†</sup> For files ≤ 300 MB or ≤ 2 hours, Content Understanding transcription time is substantially reduced.

#### Video

| Supported File Types | File Size | Resolution | Length |
| ---| --- | --- | --- |
| ✓  `.mp4`, `.m4v` <br> ✓ `.flv` (H.264 and `AAC`) <br> ✓ `.wmv`, `.asf` <br> ✓ `.avi` <br> ✓ `.mkv` <br> ✓ `.mov` | ≤20 GB † | Min: 320 x 240 pixels <br>Max: 1920 x 1,080 pixels | ≤4 hours †|

   > [!NOTE]
   > Video analysis has the following limitations:
   > * Direct upload: Maximum file size of 200 MB and maximum duration of 30 minutes when uploading video directly
   > * Frame sampling: Analyzes approximately one frame per second, which may miss quick movements or brief events
   > * Resolution: All frames are scaled to 512 x 512 pixels, which may affect visibility of small details or distant objects


### Field schema limits

Content Understanding supports both basic field value types and nested structures, including lists, groups, tables, and fixed tables.

* **Basic field value types**: *string*, *date*, *time*, *number*, *integer*, and *boolean*.
* **List field**: A sequence of values of the same type, represented as an array of basic fields in the API.
* **Group field**: A set of semantically related fields, represented as an object of basic fields in the API.
* **Table field**: A variable number of items with fixed subfields, represented as an array of objects of basic fields in the API.
* **Fixed table field**: A group of fields with shared subfields, represented as an object of objects of basic fields in the API.

#### Basic limits

| Property | Document | Text | Image | Audio | Video |
| --- | --- | --- | --- | --- | --- |
| Max fields | 100 | 100 | 100 | 100 | 100 |
| Max classify field categories | 300 | 300 | 300 | 300 | 300 |
| Supported generation methods | extract<br>generate<br>classify | generate<br>classify | generate<br>classify | generate<br>classify | generate<br>classify |

* The *Max fields* limit includes all named fields. For example, a list of strings counts as one field, while a group with string and number subfields counts as three fields. 
* The *Max classify field categories* limit is the total number of categories across all fields using the `classify` generation method.

## Knowledge source limits

| Type | Limits |
| -----| ------ |
| Training data | Documents only <br/> 1 GB total <br/> 50k pages/images total |
| Reference data | Documents only <br/> 100 MB total <br/> 5k pages total |

---

## Classifier

### General limits

   > [!NOTE]
   > This limit is for [Content Understanding classifier](concepts/classifier.md) itself, not classify fields within the extraction capability.

| Property | Limit |
| --- | --- |
| Category name | Can't start with a dollar sign (`$`)|
| Category name and description | Maximum 120 characters for combined name and description in each category |
| Number of categories | 1 to 50 per classifier |

### Input file limits

| Supported File Types | File Size | Length |
| --- | --- | --- |
| ✓ `.pdf`<br> ✓ `.tiff`<br> ✓ `.jpg`, `.png`, `.bmp`, `.heif` | ≤ 200 MB | ≤ 300 pages |
| ✓ `.txt`  | ≤ 1 MB | ≤ 1M characters |

---

## Face / Person Directories

### General limits
| Property | Value |
| --- | --- |
| Max faces per person directory | 1,000,000 |
| Max persons per person directory | 1,000,000 |
| Max detected faces per image | 100 |
| Max identified person candidates per search | 10 |
| Max similar faces returned per search | 1000 |

### Input file limits

| Supported File Types | File Size | Length |
| --- | --- |  --- |
| ✓ `.jpg`, `.png`, `.bmp`, `.webp`, `.gif`, `.ico` | ≤ 200 MB | Max: 15k x 15k pixels |


