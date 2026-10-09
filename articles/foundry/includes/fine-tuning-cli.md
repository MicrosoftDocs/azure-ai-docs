---
title: Include file
description: Common Azure Developer CLI workflow for managed SFT, DPO, and RFT jobs.
author: williamliang
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/25/2026
ms.custom: include
ai-usage: ai-assisted
---

## Use the Azure Developer CLI

Install [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.22.1 or later, then install the fine-tuning extension and sign in:

```bash
azd ext install azure.ai.finetune
azd auth login
```

Reference: [Azure Developer CLI](/azure/developer/azure-developer-cli/).

Download the YAML configuration and its data or grader files for your method:

| Method | Configuration samples |
| --- | --- |
| SFT | [Supervised fine-tuning](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/supervised). |
| DPO | [Direct preference optimization](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/direct_preference_optimization). |
| RFT | [Reinforcement fine-tuning and graders](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement). |

Review the model, method, data paths, and [training type](../fine-tuning/overview.md#training-types). From the configuration directory, initialize the project, submit the job, and inspect its status:

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
