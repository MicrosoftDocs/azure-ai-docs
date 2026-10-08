---
title: Include file
description: Create a supervised fine-tuning job in the Foundry portal.
ms.service: microsoft-foundry
ms.topic: include
ai-usage: ai-assisted
---

## Create an SFT job in the portal

Use your prepared datasets to create the job:

1. Sign in to the [Foundry portal](https://ai.azure.com) and select your project.
1. Go to **Build** > **Fine-tune**, and select **Fine-tune**.
1. Select a supported base model and **Supervised fine-tuning**.
1. Select a [training type](../fine-tuning/overview.md#training-types) supported by your model and resource.
1. Select **Existing dataset** or **Upload new dataset** for the training and validation files. Inspect the preview and resolve validation errors.
1. Configure the available hyperparameters, such as **Batch size**, **Learning rate multiplier**, and **Number of epochs**. Keep your model's defaults for your first job. See the [hyperparameter descriptions](#configure-hyperparameters) below.

[!INCLUDE [SFT hyperparameter settings](supervised-fine-tuning-settings.md)]

Optionally, set a suffix to identify the resulting model. Review the configuration and select **Submit**. Retain the job ID.
