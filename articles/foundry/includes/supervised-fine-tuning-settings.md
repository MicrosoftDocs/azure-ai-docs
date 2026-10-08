---
title: Include file
description: Explain common supervised fine-tuning settings for the selected training interface.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/07/2026
ms.custom: include
ai-usage: ai-assisted
---

### Configure hyperparameters

Hyperparameters control how the job updates the model during training. Available settings and accepted values depend on your selected model. Start with its defaults, and compare validation results before changing a setting.

::: zone pivot="programming-language-studio"

Review these common settings in the job configuration:

| Setting | Description |
| --- | --- |
| **Batch size** | The number of training examples processed together in one forward and backward pass. Larger batches produce less frequent updates with lower variance. |
| **Learning rate multiplier** | Scales the training learning rate. A smaller multiplier can help reduce overfitting. |
| **Number of epochs** | The number of complete passes through the training dataset. More passes give the model more opportunities to learn, but can increase overfitting. |

::: zone-end

::: zone pivot="programming-language-python,rest-api"

Set supported values under `method.supervised.hyperparameters` in the job body:

| Hyperparameter | Value | Description |
| --- | --- | --- |
| `batch_size` | Integer or `auto` | The number of training examples processed together in one forward and backward pass. Larger batches produce less frequent updates with lower variance. |
| `learning_rate_multiplier` | Number or `auto` | Scales the training learning rate. A smaller multiplier can help reduce overfitting. |
| `n_epochs` | Integer or `auto` | The number of complete passes through the training dataset. More passes can improve learning, but can increase overfitting. |

The v1 examples use `auto` for service-selected values. If your model doesn't accept `auto`, use values supported by that model.

For the request schema, see the [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

::: zone-end

::: zone pivot="azd"

Configure supported settings in your SFT YAML file. The [CLI SFT sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/supervised/sample_finetuning_supervised.yaml) uses these names:

| Hyperparameter | Description |
| --- | --- |
| `batch_size` | The number of training examples processed together in one forward and backward pass. Larger batches produce less frequent updates with lower variance. |
| `learning_rate_multiplier` | Scales the training learning rate. A smaller multiplier can help reduce overfitting. |
| `epochs` | The number of complete passes through the training dataset. This CLI configuration uses `epochs`, rather than the v1 API's `n_epochs`. |

Use the configuration sample for your selected model rather than copying settings from another model.

::: zone-end
