---
title: Include file
description: Configure supervised fine-tuning hyperparameters and submit a job with Azure Developer CLI.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/07/2026
ms.custom: include
ai-usage: ai-assisted
---

## Create an SFT job with the Azure Developer CLI

<!-- markdownlint-disable-next-line MD044 -->
<a id="use-the-azure-developer-cli"></a>

Install [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.22.1 or later, then install the fine-tuning extension and sign in:

```bash
azd ext install azure.ai.finetune
azd auth login
```

Reference: [Azure Developer CLI](/azure/developer/azure-developer-cli/).

Download an [SFT configuration sample and its data files](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/supervised) for your model. Set the model from [supported model IDs and versions](../fine-tuning/overview.md#supported-models), and review the data paths and supported [training type](../fine-tuning/overview.md#training-types).

[!INCLUDE [SFT hyperparameter settings](supervised-fine-tuning-settings.md)]

The following excerpt shows how to include hyperparameters in the job configuration. It uses values from the official CLI sample, not defaults for every model. Keep the rest of your model's configuration and adjust these values to its supported settings.

```yaml
model: <SUPPORTED_MODEL_ID>
method:
  type: supervised
  supervised:
    hyperparameters:
      epochs: 4
      batch_size: 8
      learning_rate_multiplier: 0.1
```

Reference: [SFT CLI configuration](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/supervised/sample_finetuning_supervised.yaml).

Replace `<SUPPORTED_MODEL_ID>` with your selected model ID. From the configuration directory, initialize the project, submit the complete job configuration, and inspect its status:

```bash
azd ai finetuning init -e <project-endpoint>
azd ai finetuning jobs submit -f <path-to-job-yaml>
azd ai finetuning jobs show -i <job-id>
```

Use a project endpoint in the form `https://<account>.services.ai.azure.com/api/projects/<project>`. Replace `<job-id>` with the ID returned by submission.

Reference: [Fine-tuning CLI samples and commands](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/README.md).

### Pause, resume, or cancel

Run lifecycle commands only when your model, method, and job state support them. Pause and resume aren't available for every model or method.

```bash
azd ai finetuning jobs pause -i <job-id>
azd ai finetuning jobs resume -i <job-id>
azd ai finetuning jobs cancel -i <job-id>
```

Reference: [Fine-tuning CLI commands](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/README.md).
