---
title: Service quotas and limits - Content Understanding
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Content Understanding service Quotas and Limits
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure
ms.topic: conceptual
ms.date: 10/25/2024
ms.author: lajanuar
---


# Service limits and quotas

This article is both a quick reference and detailed description of Azure AI Content Understanding service quotas and limits.

## File limits
Each modality covers a set of MIME file types. 

|Modality| Supported File Types | File Size | Resolution | Length |
|--- | --- | --- | --- | --- |
|Image | .jpg, .png, .bmp, .heif| ≤ 20 MB (OpenAI-enforced) | Min: 50 x 50 Max: 10k x 10k |  |
|Document |  pdf, tiff, jpg, png, bmp, heif, txt  | asynchronous: ≤ 200 MB |  | asynchronous: ≤ 300 pages |
|Speech | mp3, wav, wma, aac, ogg, flac, mp4, avi, mov, wmv, mkv  | asynchronous: ≤ 200 MB |  | asynchronous: ≤ 2 h |
|Video | MP4 (.mp4, .m4a, .m4v), FLV (with H.264 and AAC codecs) (.flv), ISMV (.isma, .ismv), MXF (.mxf), GXF (.gxf), MPEG2-PS, MPEG2-TS, 3GP (.ts, .ps, .3gp, .3gpp, .mpg), Windows Media Video (WMV)/ASF (.wmv, .asf), AVI (Uncompressed 8bit/10bit) (.avi), Microsoft Digital Video Recording (DVR-MS) (.dvr-ms), Matroska/WebM (.mkv), WAVE/WAV (.wav), QuickTime (.mov)  | asynchronous: ≤2 GB (body) asynchronous: ≤20 GB (URL)| Min: 320 x 240 Max: 1920 x 1080 | asynchronous: ≤30 m (body) asynchronous: ≤30 m (URL) |
| text | | ≤ 1 MB |  | ≤ 1M characters |

### Supported Codecs
|Modality| Codecs |
| --- | ---|
| Video | AVC 8-bit/10-bit, up to 4:2:2, including AVCIntra, 8 bit 4:2:0 and 4:2:2, Sony XAVC / XAVC S (in MXF container), Avid DNxHD (in MXF container), DVCPro/DVCProHD (in MXF container), Digital video (DV) (in AVI files), JPEG 2000, MPEG-2 (up to 422 Profile and High Level; including variants such as Sony XDCAM, Sony XDCAM HD, Sony XDCAM IMX, CableLabs&reg;, and D10), up to 420 profiles, MPEG-1, VC-1/WMV9, MPEG-4 Part 2, Theora, YUV420 uncompressed, or mezzanine, Apple ProRes 422, Apple ProRes 422 LT, Apple ProRes 422 HQ, Apple ProRes 4444, Apple ProRes 4444 XQ, HEVC/H.265 Main Profile |
| Audio | AAC (AAC-LC, AAC-HE, and AAC-HEv2; up to 5.1), MPEG Layer 2, MP3 (MPEG-1 Audio Layer 3), Windows Media Audio, WAV/PCM, FLAC, Opus, Vorbis, AMR (adaptive multi-rate) |

## Field Schema Limits
A schema in Content Understanding refers to a defined structure specifying the types of data to be extracted from various types of unstructured content. Unstructured content types include documents, images, videos, and audio. This structured representation of data is crucial for enabling downstream applications to process and analyze the extracted information effectively.

This section details the limits of the field inputs for schema definition.

| Field Types Supported | Max # of Fields Supported Per Schema |
| --- | --- |
| string: Plain Text, date: Date normalized to ISO 8601 (YYYY-MM-DD) format, time: Time normalized to ISO 8601 (hh:mm:ss) format. number: Floating point number normalized to double precision floating point. integer: Integer number, normalized to 64-bit signed integer. boolean: Boolean value, normalized to true or false.array: List of subfields of the same type. object: Named list of subfields of potentially different types. | 10 (audio, image, video), 50 (document) |

## Analyzer limits per resource
Analyzers in Content Understanding are specialized components designed to process and extract structured data from various types of unstructured content, such as textual documents, audio, images, and video. These analyzers are tailored to handle specific types of data and tasks, ensuring that the extracted information is accurate and useful for downstream applications.

| Quota | Standard (S0) |
| --- | --- |
| Max models | 100k |
| Max analysis/min | 1000 pages/images four, (4) hours of audio, 1 hour of video  |
| Max operations/min | 3000 |
| Free trainings / month | 10 hours |
| Max training file size | 1 GB |
| Max training length | 50k pages/images |
| Max fields | 100 (document), 10(image, audio, video) |
| Max enum values | 300 per schema |
