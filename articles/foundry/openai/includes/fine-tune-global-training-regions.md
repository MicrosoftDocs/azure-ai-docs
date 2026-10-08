---
title: Fine-tuning region support
titleSuffix: Microsoft Foundry
description: Compare regional support for Global managed fine-tuning and interactive training, including model-specific restrictions.
author: alvinashcraft
ms.author: aashcraft
ms.reviewer: williamliang
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 10/06/2026
ms.custom: references_regions
ai-usage: ai-assisted
---

> [!NOTE]
> Global training provides [more affordable](https://aka.ms/oai/pricing) training per token, but doesn't offer [data residency](https://aka.ms/data-residency).

The table lists the Foundry project regions required to use Global managed fine-tuning and interactive training (preview). Choose a region supported for your model and training approach, including the restrictions below. Standard and Data zone training have separate regional support.

| Foundry project region | Managed fine-tuning | Interactive training (preview) |
| --- | --- | --- |
| Australia East | ✅ | ✅ |
| Brazil South | ✅<sup>1</sup> | ❌ |
| Canada Central | ✅<sup>1</sup> | ❌ |
| Canada East | ✅<sup>1</sup> | ✅ |
| East US | ✅ | ✅ |
| East US 2 | ✅ | ✅ |
| France Central | ✅<sup>1</sup> | ❌ |
| Germany West Central | ✅<sup>1</sup> | ❌ |
| Italy North | ✅<sup>1</sup> | ❌ |
| Japan East | ✅<sup>1,2</sup> | ❌ |
| Korea Central | ✅ | ✅ |
| North Central US | ✅ | ✅ |
| Norway East | ✅<sup>1</sup> | ❌ |
| Poland Central | ✅<sup>1,3</sup> | ❌ |
| South Africa North | ✅<sup>1</sup> | ❌ |
| South Central US | ✅<sup>1</sup> | ❌ |
| South India | ✅<sup>1</sup> | ❌ |
| Southeast Asia | ✅<sup>1</sup> | ❌ |
| Spain Central | ✅<sup>1</sup> | ❌ |
| Sweden Central | ✅ | ✅ |
| Switzerland North | ✅ | ✅ |
| Switzerland West | ✅<sup>1</sup> | ❌ |
| UAE North | ✅<sup>4</sup> | ✅ |
| UK South | ✅ | ✅ |
| West Europe | ✅<sup>1</sup> | ❌ |
| West US | ✅<sup>1</sup> | ❌ |
| West US 3 | ✅ | ✅ |

- <sup>1</sup> Managed fine-tuning for `Qwen3.6-35B-A3B`, `Qwen3.8-27B`, `Muse-Glimmer-30B`, and `gpt-oss-120b` isn't supported in this region.
- <sup>2</sup> Vision fine-tuning isn't supported in Japan East.
- <sup>3</sup> Managed fine-tuning for `gpt-4.1-nano` isn't supported in Poland Central.
- <sup>4</sup> UAE North supports Global managed fine-tuning only for `Qwen3.6-35B-A3B`, `Qwen3.8-27B`, `Muse-Glimmer-30B`, and `gpt-oss-120b`.
