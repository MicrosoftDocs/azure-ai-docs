---
title: Azure OpenAI Global Batch Limits
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI model global batch limits
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 02/12/2025
---

## Batch limits

| Limit Name | Limit Value |
|--|--|
| Max files per resource | 500 |
| Max input file size | 200 MB |
| Max requests per file | 100,000 |

## Batch quota

The table shows the batch quota limit. Quota values for global batch are represented in terms of enqueued tokens. When you submit a file for batch processing the number of tokens present in the file are counted. Until the batch job reaches a terminal state, those tokens will count against your  total enqueued token limit.

### Global batch

|Model|Enterprise agreement|Default| Monthly credit card based subscriptions | MSDN subscriptions | Azure for Students, Free Trials |
|---|---|---|---|---|---|
| `gpt-4.1`| 5 B | 200 M | 50 M | 90 K | N/A |
| `gpt-4.1 mini` | 15B | 1B | 50M | 90k | N/A |
| `gpt-4.1-nano` | 15 B | 1 B | 50 M | 90 K | N/A |
| `gpt-4o` | 5 B | 200 M | 50 M | 90 K | N/A|
| `gpt-4o-mini` | 15 B | 1 B | 50 M | 90 K | N/A |
| `gpt-4-turbo` | 300 M | 80 M | 40 M | 90 K | N/A |
| `gpt-4` | 150 M | 30 M | 5 M | 100 K | N/A |
| `gpt-35-turbo` | 10 B | 1 B | 100 M | 2 M | 50 K |
| `o3-mini`| 15 B | 1 B | 50 M | 90 K | N/A |
| `o4-mini` | 15 B | 1 B | 50 M | 90 K | N/A |

B = billion | M = million | K = thousand

### Data zone batch

|Model|Enterprise agreement|Default| Monthly credit card based subscriptions | MSDN subscriptions | Azure for Students, Free Trials |
|---|---|---|---|---|---|
| `gpt-4.1` | 500 M | 30 M | 30 M | 90 K | N/A|
| `gpt-4.1-mini` | 1.5 B | 100 M | 50 M | 90 K | N/A |
| `gpt-4o` | 500 M | 30 M | 30 M | 90 K | N/A|
| `gpt-4o-mini` | 1.5 B | 100 M | 50 M | 90 K | N/A |
| `o3-mini` | 1.5 B | 100 M | 50 M | 90 K | N/A |