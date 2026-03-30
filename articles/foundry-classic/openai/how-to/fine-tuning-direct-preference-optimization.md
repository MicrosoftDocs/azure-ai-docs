---
title: "Direct preference optimization (classic)"
description: "Learn how to use direct preference optimization technique to fine-tune Azure OpenAI models. (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, references_regions
  - classic-and-new
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
ROBOTS: NOINDEX, NOFOLLOW
---

# Direct preference optimization (preview) (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/fine-tuning-direct-preference-optimization.md)

[!INCLUDE [fine-tuning-direct-preference-optimization 1](../../../foundry/openai/includes/how-to-fine-tuning-direct-preference-optimization-1.md)]

## How to use direct preference optimization fine-tuning

1. Prepare `jsonl` datasets in the [preference format](#direct-preference-optimization-dataset-format).
2. Select the model and then select the method of customization **Direct Preference Optimization**.
3. Upload datasets – training and validation. Preview as needed.
4. Select hyperparameters, defaults are recommended for initial experimentation.
5. Review the selections and create a fine-tuning job.

[!INCLUDE [fine-tuning-direct-preference-optimization 2](../../../foundry/openai/includes/how-to-fine-tuning-direct-preference-optimization-2.md)]
