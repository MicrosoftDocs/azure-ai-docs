---
title: Fine-tuning model guidance
titleSuffix: Azure OpenAI
description: Describes the models that support fine-tuning and the regions where fine-tuning is available.
author: mrbullwinkle 
ms.author: mbullwin 
ms.service: azure-ai-openai
ms.topic: include
ms.date: 02/06/2025
manager: nitinme
---

> [!NOTE]
> `gpt-35-turbo` - Fine-tuning of this model is limited to a subset of regions, and isn't available in every region the base model is available. 
>
> The supported regions for fine-tuning might vary if you use Azure OpenAI models in an Azure AI Foundry project versus outside a project.

|  Model ID  | Fine-tuning regions | Max request (tokens) | Training Data (up to) |
|  --- | --- | :---: | :---: |
| `gpt-35-turbo` (1106) | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | Input: 16,385<br> Output: 4,096 |  Sep 2021|
| `gpt-35-turbo` (0125)  | East US2 <br> North Central US <br> Sweden Central <br> Switzerland West | 16,385 | Sep 2021 |
| `gpt-4o-mini` (2024-07-18) | North Central US <br> Sweden Central | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 64,536 | Oct 2023 |
| `gpt-4o` (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | Input: 128,000 <br> Output: 16,384  <br> Training example context length: 64,536 | Oct 2023 | 
