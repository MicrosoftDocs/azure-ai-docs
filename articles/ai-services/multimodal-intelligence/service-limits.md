---
title: Service quotas and limits - Multimodal Intelligence
titleSuffix: Azure AI services
description: Quick reference, detailed description, and best practices for working within Azure AI Multimodal Intelligence service Quotas and Limits
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 10/09/2024
ms.author: lajanuar
---


# Service limits and quotas

This article contains both a quick reference and detailed description of Azure AI Multimodal Intelligence service quotas and limits.

## Document limits

| Input | File Size | Resolution | Length |
| --- | --- | --- | --- |
| image (jpg, png, bmp, heif) | ≤20MB (OpenAI-enforced) | Min: 50 x 50Max: 10k x 10k |  |
| document (pdf, tiff) | asynchronous: ≤200MBBatch: ≤500MB |  | asynchronous: ≤300 pagesBatch: ≤2000 pages |
| speech | asynchronous: ≤200MBBatch: ≤1GB |  | asynchronous: ≤2hBatch: ≤4h |
| video | asynchronous: ≤???Batch: ≤20GB | Min: 320 x 240Max: 1920 x 1080 | asynchronous: ≤???Batch: ≤4h |
| text | ≤10MB |  | ≤10M characters |


## Model limits

| Quota | Free (F0) | Standard (S0) |
| --- | --- | --- |
| Max models | 100 | 100k (up to ???) |
| Max analysis/min | 5 pages/images3 min of audio1 min of video | 1000 pages/images (up to ???)4h of audio (up to ???)1h of video (up to ???) |
| Max analysis/month | 500 pages/images5 hours of audio1 hour of video | 10M pages/images??? hours of audio??? hours of video |
| Max operations/min | 50 | 1000 |
| Free trainings / month | 10 hours | 10 hours |
| Max training file size | 1 GB | 1 GB |
| Max training length | 50k pages/images... | 50k pages/images... |
| Max fields | 1000 | 1000 |

