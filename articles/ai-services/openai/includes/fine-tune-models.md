---
title: Fine-tuning model guidance
titleSuffix: Azure OpenAI
description: Describes the models that support fine-tuning and the regions where fine-tuning is available.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 02/06/2025
ms.service: azure-ai-openai
ms.topic: include
ms.custom:
  - build-2025
---

> [!NOTE]
> `gpt-35-turbo` - Fine-tuning of this model is limited to a subset of regions, and isn't available in every region the base model is available. 
>
> The supported regions for fine-tuning might vary if you use Azure OpenAI models in an Azure AI Foundry project versus outside a project.
>

|  Model ID  | Standard Training Regions | Global Training (Preview) | Max request (tokens) | Training Data (up to) | Modality |
|  --- | --- | :---: | :---: | :---: | --- |
| `gpt-35-turbo` (1106) | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | - | Input: 16,385<br> Output: 4,096 |  Sep 2021 | Text to Text |
| `gpt-35-turbo` (0125)  | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | - | 16,385 | Sep 2021 | Text to Text |
| `gpt-4o-mini` (2024-07-18) | North Central US <br> Sweden Central | - | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 65,536 | Oct 2023 | Text to Text |
| `gpt-4o` (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | - | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 65,536 | Oct 2023 | Text & Vision to Text |
| `gpt-4.1` (2025-04-14) | North Central US <br> Sweden Central | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text & Vision to Text |
| `gpt-4.1-mini` (2025-04-14) | North Central US <br> Sweden Central | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text to Text |
| `gpt-4.1-nano` (2025-04-14) | North Central US <br> Sweden Central | ✅ | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 32,768 | May 2024 | Text to Text |
| `o4-mini` (2025-04-16) | East US2 <br> Sweden Central | - | Input: 128,000 <br> Output: 16,384 <br> Training example context length: 65,536 | May 2024 | Text to Text |

> [!NOTE]
> **Global** training (in Public Preview) provides [more affordable](https://aka.ms/aoai-pricing) training per-token, but does not offer [data residency](https://aka.ms/data-residency). It is currently available to Azure OpenAI resources in the following regions, with more regions coming soon:
>- Australia East
>- Brazil South
>- France Central
>- Germany West Central
>- Italy North
>- Japan East _(no vision support)_
>- Korea Central
>- Norway East
>- Poland Central
>- Southeast Asia
>- Spain Central
>- South Africa North
