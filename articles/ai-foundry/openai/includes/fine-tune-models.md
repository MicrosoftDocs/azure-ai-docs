---
title: Fine-Tuning Model Guidance
titleSuffix: Azure OpenAI
description: Describes the models that support fine-tuning and the regions where fine-tuning is available.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 02/06/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
  - references_regions
---

> [!NOTE]
> The supported regions for fine-tuning might vary if you use Azure OpenAI models in a Microsoft Foundry project versus outside a project.

|  Model ID  | Standard regions | Global | Developer | Max request (tokens) | Training data (up to) | Modality |
|  --- | --- | :---: | :---: | :---: | --- |
| `gpt-4o-mini` <br> (2024-07-18) | North Central US <br> Sweden Central | ✅ | ✅ | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 65,536 | Oct 2023 | Text to text |
| `gpt-4o` <br> (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | ✅ | ✅ | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 65,536 | Oct 2023 | Text and vision to text |
| `gpt-4.1` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text and vision to text |
| `gpt-4.1-mini` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text to text |
| `gpt-4.1-nano` (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 32,768 | May 2024 | Text to text |
| `o4-mini` <br> (2025-04-16) | East US2 <br> Sweden Central | ✅ | ❌ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text to text |
| `Ministral-3B` (preview) <br> (2411) | Not supported | ✅ | ❌ | Input: 128,000 <br> Output: Unknown <br> Training example context length: Unknown | Unknown | Text to text |
| `Qwen-32B` (preview) | Not supported | ✅ | ❌ | Input: 8,000 <br> Output: 32,000 <br> Training example context length: 8192 | July 2024 | Text to text |

> [!NOTE]
> Global training provides [more affordable](https://aka.ms/aoai-pricing) training per token, but doesn't offer [data residency](https://aka.ms/data-residency). It's currently available to Foundry resources in the following regions:
>
>- Australia East
>- Brazil South
>- Canada Central
>- Canada East
>- East US
>- East US2
>- France Central
>- Germany West Central
>- Italy North
>- Japan East _(no vision support)_
>- Korea Central
>- North Central US
>- Norway East
>- Poland Central _(no 4.1-nano support)_
>- Southeast Asia
>- South Africa North
>- South Central US
>- South India
>- Spain Central
>- Sweden Central
>- Switzerland West
>- Switzerland North
>- UK South
>- West Europe
>- West US
>- West US3
