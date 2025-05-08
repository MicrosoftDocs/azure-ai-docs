---
title: Service quotas and limits - Content Understanding
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Content Understanding service Quotas and Limits
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: conceptual
ms.date: 04/14/2025
ms.custom: ignite-2024-understanding-release
ms.author: lajanuar
---


# Content Understanding service quotas and limits

This article offers a quick reference of the quotas and limits for the Azure AI Content Understanding service.

## Resource limits
| Quota | Standard (S0) |
| --- | --- |
| Max analyzers | 100k |
| Max analysis/min | 1000 pages/images <br> Four hours of audio <br> Four hours of video  |
| Max operations/min | 3000 |

## Input file limits

### Document and text

| Supported File Types | File Size | Length |
| --- | --- | --- |
| ✓ `.pdf`<br> ✓ `.tiff`<br> ✓ `.jpg`<br> ✓ `.png`<br> ✓ `.bmp`<br> ✓ `.heif` | ≤ 200 MB | ≤ 300 pages |
| ✓ `.txt`  | ≤ 1 MB | ≤ 1M characters |

### Image

| Supported File Types | File Size | Resolution |
| --- | --- | --- |
| ✓ `.jpg`<br> ✓ `.png`<br> ✓ `.bmp`<br> ✓ `.heif`| ≤ 200 MB | Min: 50 x 50 pixels <br> Max: 10k x 10k pixels |

### Audio

| Supported File Types | File Size | Length |
| --- | --- |  --- |
| ✓ `.wav` (`PCM`, A-law, μ-law) <br> ✓ `.mp3` <br> ✓ `.opus`, `.ogg` (Opus)<br> ✓ `.flac` <br> ✓ `.wma` <br> ✓ `.aac` <br> ✓ `.amr` (AMR-NB, AMR-WB) <br> ✓ `.webm` (Opus, Vorbis) <br> ✓ `.m4a` (`AAC`, `ALAC`)<br> ✓ `.spx` | ≤ 200 MB | ≤ 2 hours |

### Video

| Supported File Types | File Size | Resolution | Length |
| ---| --- | --- | --- |
| ✓  `.mp4`, `.m4v` <br> ✓ `.flv` (H.264 and `AAC`) <br> ✓ `.wmv`, `.asf` <br> ✓ `.avi` <br> ✓ `.mkv` <br> ✓ `.mov` | ≤20 GB † | Min: 320 x 240 pixels <br>Max: 1920 x 1,080 pixels | ≤4 hours †|

   > [!NOTE]
   > The file size limit is 200 MB and the duration limit is 30 minutes if the video file is included directly in the analysis request.

## Field schema limits

Content Understanding supports both basic field value types and nested structures, including lists, groups, tables, and fixed tables.

* **Basic field value types**: *string*, *date*, *time*, *number*, *integer*, and *boolean*.
* **List field**: A sequence of values of the same type, represented as an array of basic fields in the API.
* **Group field**: A set of semantically related fields, represented as an object of basic fields in the API.
* **Table field**: A variable number of items with fixed subfields, represented as an array of objects of basic fields in the API.
* **Fixed table field**: A group of fields with shared subfields, represented as an object of objects of basic fields in the API.

The following limits apply as of version 2024-12-01-preview.

### Basic limits

| Property | Document | Image | Text | Audio | Video |
| --- | --- | --- | --- | --- | --- |
| Max fields | 50 | 50 | 50 | 50 | 50 |
| Max classify field categories | 300 | 300 | 300 | 300 | 300 |
| Supported generation methods | extract | generate<br>classify | generate<br>classify | generate<br>classify | generate<br>classify |

* The *Max fields* limit includes all named fields. For example, a list of strings counts as one field, while a group with string and number subfields counts as three fields. To extend the limit for documents fields up to 100, contact us at `cu_contact@microsoft.com`.
* The *Max classify field categories* limit is the total number of categories across all fields using the `classify` generation method.
* The generation method currently applies only to basic fields.

### Field type limits

| Field type | Document | Image | Text | Audio | Video |
| --- | --- | --- | --- | --- | --- |
| Basic | No *boolean* | No *date*, *time* | *string* | *string* | No *date*, *time* |
| List | N/A | No *date*, *time* | *string* | *string* | No *date*, *time* |
| Group | N/A | No *date*, *time* |*string* | *string* | No *date*, *time* |
| Table | No *boolean* | No *date*, *time* | *string* | *string* | No *date*, *time* |
| Fixed table | No *boolean* | N/A | N/A | N/A | N/A |

### Classification fields

   > [!NOTE]
   > This is the classification field within the extraction capability and not the separate [Content Understanding Classifier](concepts/classifier.md) itself.

Classification fields can be defined to return either a single category (single-label classification) or multiple categories (multi-label classification).

* **Single-label classification**: Defined using a string field with the `classify` method. It can be a top-level basic field or a subfield within a group or table.
* **Multi-label classification**: Represented as a list of string fields with the `classify` method. In the [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true), `method=classify` and `enum` are specified on the inner string field and can only be a top-level field.


## Training limits
| File type| Max training data |
| ---| --- |
| Document | 1 GB total<br>50k pages/images |

## Classifier limits

The following limits apply as of version 2025-05-01-preview.

### Input File Limits (Documents only)

| Supported File Types | File Size | Length |
| --- | --- | --- |
| ✓ `.pdf`<br> ✓ `.tiff`<br> ✓ `.jpg`<br> ✓ `.png`<br> ✓ `.bmp`<br> ✓ `.heif` | ≤ 200 MB | ≤ 300 pages |
| ✓ `.txt`  | ≤ 1 MB | ≤ 1M characters |

### Category Limits

* **Category Name and Description**: Limit of total 120 characters for each category name and description combined.
* **Category Name**: Category name can't start with `$`.
* **Number of categories**: Minimum 1 to maximum 50 categories per classifier.
