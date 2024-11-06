---
title: Service quotas and limits - Multimodal Intelligence
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Multimodal Intelligence service Quotas and Limits
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure
ms.topic: conceptual
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
ms.author: lajanuar
---


# Service limits and quotas

This article provides both a quick reference and detailed description of Azure AI Multimodal Intelligence service quotas and limits.

## File limits

Each modality covers a set of Multipurpose Internet Mail Extensions (MIME) file types. 

### Image

|Modality| Supported File Types | File Size | Resolution | Length |
|--- | --- | --- | --- | --- |
|**Image** | √ .jpg</br>√  .png</br>√  .bmp</br>√  .heif| ≤ 20 MB (OpenAI-enforced) | Min: 50 x 50 Max: 10k x 10k |  |

### Document and text

|Modality| Supported File Types | File Size | Resolution | Length |
|--- | --- | --- | --- | --- |
|**Document** |√ pdf</br>√  tiff</br>√  jpg</br>√  png</br>√  bmp</br>√  heif</br>√  txt  | asynchronous:</br>≤ 200 MB |  | asynchronous:</br>≤ 300 pages |
| **Text**|.txt  | ≤ 1 MB | | ≤ 1M characters |

### Audio

|Modality| Supported File Types | File Size | Resolution | Length |
|--- | --- | --- | --- | --- |
|**Audio** |   √  .wav (PCM, ALAW, MULAW) </br>√  .mp3 </br>√.opus, .ogg (Opus)</br>√.flac </br>√  .wma </br>√  .aac </br>√  .amr (AMR-NB, AMR-WB) </br>√.webm (Opus, Vorbis) </br>√  .m4a (AAC, ALAC)</br>√.spx | asynchronous:</br>≤ 200 MB |  | asynchronous:</br> ≤ 2 h |

### Video

|Modality| Supported File Types | File Size | Resolution | Length |
|--- | --- | --- | --- | --- |
|**Video** | √  .mp4, .m4v </br>√  .flv (with H.264 and AAC codecs) </br>√  .wmv, .asf </br>√  .avi (Uncompressed 8bit/10bit) </br>√  .mkv </br>√  .mov  | asynchronous:</br>≤2 GB (body) asynchronous:</br>≤20 GB (URL)| Min:</br>320 x 240</br></br>Max:</br>1920 x 1080 | asynchronous:</br>≤30 m (body)</br></br> asynchronous:</br>≤30 m (URL) |


## Field Schema Limits

A schema in Multimodal Intelligence refers to a defined structure specifying the types of data to be extracted from various types of unstructured content. Unstructured content types include documents, images, videos, and audio. This structured representation of data is crucial for enabling downstream applications to process and analyze the extracted information effectively.

This section details the limits of the field inputs for schema definition.

| Data type|Supported format|Schema limits|
| --- | --- |---|
| **String**| √ Plain Text||
|**Date** | √ Normalized to ISO 8601 (YYYY-MM-DD) format||
| **Time**| √ Normalized to ISO 8601 (hh:mm:ss) format||
| **number**| √ Float number normalized to double precision floating point||
| **Integer**| √ Integer number, normalized to 64-bit signed integer||
| **Boolean**| √ Boolean value, normalized to `true` or `false`||
| **array**| √ List of subfields of the same type||
| **Object**| √ Named list of subfields of potentially different types. | 10 (audio, image, video), 50 (document) |

## Training limits for Custom Document
| Quota | Standard (S0) |
| --- | --- |
| Max training file size | 1 GB |
| Max training length | 50k pages/images |

## Resource limits
| Quota | Standard (S0) |
| --- | --- |
| Max analyzers | 100k |
| Max analysis/min | 1000 pages/images four, (4) hours of audio, 1 hour of video  |
| Max operations/min | 3000 |