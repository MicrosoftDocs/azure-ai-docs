---
title: "Direct preference optimization"
description: "Learn how to use direct preference optimization technique to fine-tune Azure OpenAI models."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ai-usage: ai-assisted
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, references_regions
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
---

# Direct preference optimization (preview)

[!INCLUDE [fine-tuning-direct-preference-optimization 1](../includes/how-to-fine-tuning-direct-preference-optimization-1.md)]

## How to use direct preference optimization fine-tuning

1. Navigate to **Build** in the top section of AI foundry.
2. Select **Fine-tune** from the side menu.
3. Prepare `jsonl` datasets in the [preference format](#direct-preference-optimization-dataset-format).
4. Select a model and then select the method of customization **Direct Preference Optimization**.
5. Upload datasets – training and validation. Preview as needed.
6. Select hyperparameters, defaults are recommended for initial experimentation.
7. Review the selections and create a fine-tuning job.

[!INCLUDE [fine-tuning-direct-preference-optimization 2](../includes/how-to-fine-tuning-direct-preference-optimization-2.md)]
