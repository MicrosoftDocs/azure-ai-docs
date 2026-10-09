---
title: Fine-tune a model with supervised fine-tuning in Microsoft Foundry
description: Prepare supervised data, create and monitor an SFT job with the portal, SDK, REST, or Azure Developer CLI, and evaluate the resulting model.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, references_regions
  - classic-and-new
  - doc-kit-assisted
  - dev-focus
ms.topic: how-to
ms.date: 10/05/2026
author: ssalgadodev
ms.author: ssalgado
zone_pivot_groups: foundry-fine-tuning
ai-usage: ai-assisted
---

# Fine-tune a model with supervised fine-tuning in Microsoft Foundry

Prepare your data and create a supervised fine-tuning (SFT) job in Microsoft Foundry. For method comparisons and training concepts, see the [fine-tuning overview](../../fine-tuning/overview.md).

## Prerequisites

- A Foundry resource or project with an [SFT-supported model and training region](../../fine-tuning/overview.md#supported-models).
- The **Foundry User** role for training, or the **Foundry Owner** role if you also deploy the fine-tuned model.

::: zone pivot="programming-language-python"

- The client packages and credentials described in the [Python procedure](#create-an-sft-job-with-python).

::: zone-end

::: zone pivot="rest-api"

- Your resource endpoint and credentials, and a Bash-compatible shell for the REST examples.

::: zone-end

::: zone pivot="azd"

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.22.1 or later.

::: zone-end

[!INCLUDE [Role rename note](../../includes/role-rename-note.md)]

## Prepare your data

Start with the [text-only GSM8K sample dataset on GitHub](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Supervised_Fine_Tuning/Text-GSM8K), or prepare your own data.

Save separate `training.jsonl` and `validation.jsonl` files with one conversation per line. Include the prompt and the desired assistant response in each example:

```json
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the biggest city in France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
```

Reference: [Chat Completions message format](chatgpt.md).

Check the data-format, file-size, and minimum-example requirements for your selected model. Keep validation and final test examples out of the training set.

For specialized data formats, see [vision fine-tuning](fine-tuning-vision.md) or [tool calling](fine-tuning-functions.md).

::: zone pivot="programming-language-studio"

[!INCLUDE [Microsoft Foundry portal fine-tuning](../../includes/fine-tuning-foundry.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/fine-tuning-oai-sdk.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

::: zone pivot="azd"

[!INCLUDE [SFT Azure Developer CLI job workflow](../../includes/supervised-fine-tuning-command-line.md)]

::: zone-end

## Review training metrics

SFT measures how well the model predicts the target responses in your examples. Compare training and validation results rather than judging the model on training performance alone.

Metric availability depends on your model. Use the metrics reported for your job:

| Metrics | What to look for |
| --- | --- |
| Training loss. | Loss on the current training batch. Look for a decreasing trend. |
| Full validation loss. | Loss across the validation set at the end of an epoch. If training loss falls but validation loss rises, inspect failing validation examples. |
| Training mean token accuracy. | The fraction of target tokens correctly predicted in the training batch. Look for an increasing trend. |
| Full validation mean token accuracy. | Token accuracy across the validation set at the end of an epoch. Confirm that improvements also help your task. |

::: zone pivot="programming-language-python,rest-api"

The corresponding metric names are `train_loss`, `full_valid_loss`, `train_mean_token_accuracy`, and `full_valid_mean_token_accuracy`. Batch validation metrics, when reported, aren't the same as full-validation metrics.

::: zone-end

Compare the available checkpoints using validation metrics and held-out task results. Checkpoint creation and retention depend on the model and training workflow.

For explanations of overfitting and evaluation risks, see [challenges and limitations](../../fine-tuning/overview.md#challenges-and-limitations).

[!INCLUDE [Managed job monitoring](../../includes/fine-tuning-job-management.md)]

## Related content

- [End-to-end SFT examples](https://github.com/microsoft-foundry/fine-tuning/tree/main/Demos).
- [Generate training data](../../fine-tuning/data-generation.md).
