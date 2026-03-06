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

The following models are supported for fine-tuning:

|  Model ID  | Standard regions | Global | Developer | Methods | Status | Modality |
|  --- | --- | :---: | :---: | :---: | --- |
| `gpt-4o-mini` <br> (2024-07-18) | North Central US <br> Sweden Central | ✅ | ✅ | SFT | GA | Text to text |
| `gpt-4o` <br> (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text and vision to text |
| `gpt-4.1` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text and vision to text |
| `gpt-4.1-mini` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text to text |
| `gpt-4.1-nano` (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text to text |
| `o4-mini` <br> (2025-04-16) | East US2 <br> Sweden Central | ✅ | ❌ | RFT | GA | Text to text |
| `gpt-5` <br> (2025-08-07) | North Central US <br> Sweden Central | ✅ | ✅ | SFT | Private preview | Text to text |
| `Ministral-3B` <br> (2411) | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `Qwen-32B` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `Llama-3.3-70B-Instruct` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `gpt-oss-20b` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |

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
