---
title: Fine-tune a model with direct preference optimization in Microsoft Foundry
description: Prepare preference pairs and run direct preference optimization with the portal, Python SDK, REST, or Azure Developer CLI.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ai-usage: ai-assisted
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, references_regions
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 10/05/2026
author: ssalgadodev
ms.author: ssalgado
zone_pivot_groups: foundry-fine-tuning
---

# Fine-tune a model with direct preference optimization in Microsoft Foundry

<!-- TODO(PM): Confirm model-specific DPO release status before publication. -->

Prepare preference data and create a direct preference optimization (DPO) job in Microsoft Foundry. For method comparisons and training concepts, see the [fine-tuning overview](../../fine-tuning/overview.md).

## Prerequisites

- A Foundry resource with a [DPO-supported model and training region](../../fine-tuning/overview.md#supported-models).
- The **Foundry User** role for training, or the **Foundry Owner** role if you also deploy the fine-tuned model.

::: zone pivot="programming-language-python"

- The client packages and credentials described in the [Python procedure](#create-a-dpo-job-with-python).

::: zone-end

::: zone pivot="rest-api"

- Your resource endpoint and credentials, and a Bash-compatible shell for the REST examples.

::: zone-end

::: zone pivot="azd"

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.22.1 or later.

::: zone-end

[!INCLUDE [Role rename note](../../includes/role-rename-note.md)]

[!INCLUDE [fine-tuning-direct-preference-optimization 1](../includes/how-to-fine-tuning-direct-preference-optimization-1.md)]

## Configure hyperparameters

Start with your selected model's defaults. Compare validation results before changing the balance between learning your preferences and staying close to the starting model.

::: zone pivot="programming-language-studio"

Use the settings available in the job configuration. The available controls and accepted values depend on your selected model.

::: zone-end

::: zone pivot="programming-language-python,rest-api"

The v1 examples below omit optional hyperparameters. To override defaults, use supported settings under `method.dpo.hyperparameters` in the [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

::: zone-end

::: zone pivot="azd"

Keep the default settings in your model's YAML configuration for your first job. Use the configuration sample for your selected model rather than copying settings from another model.

::: zone-end

::: zone pivot="programming-language-studio"

## Create a DPO job in the portal

Use your prepared datasets to create the job:

1. Open **Build** > **Fine-tune** in the [Foundry portal](https://ai.azure.com), and select **Fine-tune**.
1. Select a supported model and **Direct Preference Optimization**.
1. Upload the training and validation datasets, and resolve any validation errors.
1. Select a supported [training type](../../fine-tuning/overview.md#training-types), and leave [hyperparameters](#configure-hyperparameters) at their defaults for your first job.
1. Review the configuration and create the job. Retain its ID.

::: zone-end

[!INCLUDE [DPO code job workflows](../../includes/fine-tuning-direct-preference-optimization-job.md)]

::: zone pivot="azd"

[!INCLUDE [Azure Developer CLI job workflow](../../includes/fine-tuning-cli.md)]

::: zone-end

## Review training results

Review the metrics reported for your DPO job using the [monitoring workflow below](#monitor-the-job-and-select-a-checkpoint). DPO learns from preference pairs; token-prediction accuracy isn't a measure of whether responses match your preferences.

<!-- [TO VERIFY] Confirm DPO-specific training metric names and definitions against a Foundry result file or a first-party reference. The OpenAI DPO guide and cookbook don't list exported metric columns. Don't substitute SFT token-accuracy metrics or invent preference_accuracy or dpo_loss fields. -->

Compare responses from candidate checkpoints on held-out preference examples. Use the same rubric as your dataset labels, and record how often each candidate meets your preferred behavior. This is a task evaluation, not a token-accuracy metric.

Don't choose a model based only on training loss. For evaluation risks, see [challenges and limitations](../../fine-tuning/overview.md#challenges-and-limitations).

[!INCLUDE [Managed job monitoring](../../includes/fine-tuning-job-management.md)]

## Related content

- [End-to-end DPO example and preference datasets](https://github.com/microsoft-foundry/fine-tuning/tree/main/Demos/DPO_Intel_Orca).
