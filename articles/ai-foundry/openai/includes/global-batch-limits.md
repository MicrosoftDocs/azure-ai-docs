---
title: Azure OpenAI Global Batch Limits
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Global batch limits for Azure OpenAI models.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 02/12/2025
---

## Batch limits

| Limit name | Limit value |
|--|--|
| Maximum files per resource | 500 |
| Maximum input file size | 200 MB |
| Maximum requests per file | 100,000 |

## Batch quota

The table shows the batch quota limit. Quota values for global batch are represented in terms of enqueued tokens. When you submit a file for batch processing, the number of tokens in the file is counted. Until the batch job reaches a terminal state, those tokens count against your total enqueued token limit.

### Global batch

|Model|Enterprise and MCA-E|Default| Monthly credit card-based subscriptions | MSDN subscriptions | Azure for Students, free trials |
|---|---|---|---|---|---|
| `gpt-4.1`| 5B | 200M | 50M | 90K | N/A |
| `gpt-4.1 mini` | 15B | 1B | 50M | 90K | N/A |
| `gpt-4.1-nano` | 15B | 1B | 50M | 90K | N/A |
| `gpt-4o` | 5B | 200M | 50M | 90K | N/A|
| `gpt-4o-mini` | 15B | 1B | 50M | 90K | N/A |
| `gpt-4-turbo` | 300M | 80M | 40M | 90K | N/A |
| `gpt-4` | 150M | 30M | 5M | 100K | N/A |
| `gpt-35-turbo` | 10B | 1B | 100M | 2M | 50K |
| `o3-mini`| 15B | 1B | 50M | 90K | N/A |
| `o4-mini` | 15B | 1B | 50M | 90K | N/A |
| `gpt-5`| 5B | 200M | 50M | 90K | N/A |

B = billion | M = million | K = thousand

### Data zone batch

|Model|Enterprise and MCA-E|Default| Monthly credit card-based subscriptions | MSDN subscriptions | Azure for Students, free trials |
|---|---|---|---|---|---|
| `gpt-4.1` | 500M | 30M | 30M | 90K | N/A|
| `gpt-4.1-mini` | 1.5B | 100M | 50M | 90K | N/A |
| `gpt-4o` | 500M | 30M | 30M | 90K | N/A|
| `gpt-4o-mini` | 1.5B | 100M | 50M | 90K | N/A |
| `o3-mini` | 1.5B | 100M | 50M | 90K | N/A |
| `gpt-5`| 5B | 200M | 50M | 90K | N/A |
