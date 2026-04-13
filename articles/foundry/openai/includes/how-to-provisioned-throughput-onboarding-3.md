---
title: Include file
description: Include file
author: msakande
ms.reviewer: seramasu
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Latest Azure OpenAI models

> [!NOTE]
> gpt-5.4, gpt-4.1, gpt-4.1-mini and gpt-4.1-nano don't support long context (requests estimated at larger than 128k prompt tokens).

| Topic | **gpt-5.4** | **gpt-5.3-codex** | **gpt-5.2** | **gpt-5.2-codex** | **gpt-5.1** | **gpt-5.1-codex** | **gpt-5** | **gpt-5-mini** | **gpt-4.1** | **gpt-4.1-mini** | **gpt-4.1-nano** | **o3** | **o4-mini** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Global & data zone provisioned minimum deployment | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| Global & data zone provisioned scale increment | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| Regional provisioned minimum deployment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Regional provisioned scale increment | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 25 | 50 | 25 | 25 | 50 | 25 |
| Input TPM per PTU | 2,400 | 3,400 | 3,400 | 3,400 | 4,750 | 4,750 | 4,750 | 23,750 | 3,000 | 14,900 | 59,400 | 3,000 | 5,400 |
| Latency Target Value | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 50 Tokens Per Second\* | 99% > 80 Tokens Per Second\* | 99% > 80 Tokens Per Second\* | 99% > 90 Tokens Per Second\* | 99% > 100 Tokens Per Second\* | 99% > 80 Tokens Per Second\* | 99% > 90 Tokens Per Second\* |

\* Calculated as p50 request latency on a per 5 minute basis.

## Previous Azure OpenAI models

|Topic| **gpt-4o** | **gpt-4o-mini** | **o3-mini** | **o1** |
| --- | --- | --- | --- | --- |
|Global & data zone provisioned minimum deployment|15|15| 15|15|
|Global & data zone provisioned scale increment|5|5| 5|5|
|Regional provisioned minimum deployment|50|25| 25|25|
|Regional provisioned scale increment|50|25| 25|50|
|Input TPM per PTU|2,500|37,000| 2,500|230|
|Latency Target Value| 99% > 25 Tokens Per Second\* | 99% > 33 Tokens Per Second\* |  99% > 66 Tokens Per Second\* | 99% > 25 Tokens Per Second\* |

\* Calculated as the average request latency on a per-minute basis across the month.
