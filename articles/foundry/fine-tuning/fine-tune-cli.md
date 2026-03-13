---
title: Fine-tune AI models in Microsoft Foundry with the Azure Developer CLI fine-tuning extension
description: Learn how to use the Azure Developer CLI (azd) AI fine-tuning extension to initialize, submit, manage, and deploy fine-tuning jobs in Microsoft Foundry.
ms.date: 03/12/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
author: williamliang
ms.author: ssalgado
---

# Fine-tune AI models in Microsoft Foundry with the Azure Developer CLI fine-tuning extension

In this article, you learn to use the Azure Developer CLI (`azd`) AI fine-tuning extension to set up and run fine-tuning jobs in Microsoft Foundry. The extension lets you initialize projects from templates, submit and manage fine-tuning jobs, and deploy fine-tuned models directly from your terminal.


## Prerequisites

- The [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) installed (version **1.22.1** or later) and authenticated (`azd auth login`).
- The `azd` AI fine-tuning extension installed (`azd ext install azure.ai.finetune`). See [Install the fine-tuning extension](#install-the-fine-tuning-extension) for details.
- An Azure subscription with permission to create and manage Microsoft Foundry resources.
- (Optional) The [GitHub CLI](https://cli.github.com/) installed, if you plan to download sample templates from GitHub repositories.

## Install the Azure Developer CLI

Install `azd` for your operating system.

### [Windows](#tab/windows)

```bash
winget install microsoft.azd
```


### [macOS](#tab/macos)

```bash
brew tap azure/azd && brew install azd
```

### [Linux](#tab/linux)

```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

---

### Verify the installation

After installing, verify that `azd` is installed and meets the minimum version requirement:

```bash
azd version
```

Confirm the output shows version **1.22.1** or later. If you need to upgrade, run:

```bash
winget upgrade Microsoft.azd
```

## Install the fine-tuning extension

Add the Azure AI fine-tuning extension to `azd`:

```bash
azd ext install azure.ai.finetune
```

Verify the extension is installed:

```bash
azd ext list
```

## Authenticate

### Sign in to Azure (required)

Authenticate with your Azure account to access your subscription and resources:

```bash
azd auth login
```


## Initialize your project

Use the `azd ai finetuning init` command to scaffold a fine-tuning project. Navigate to your desired working directory before running any of the following initialization methods.

> [!TIP]
> You can skip initialization entirely by using the [Quick Submit](#quick-submit-skip-initialization) option, which lets you submit a fine-tuning job by providing the subscription and Foundry project endpoint inline.

### Find your project ARM resource ID

To initialize with an Azure AI Foundry project, you need the project's ARM resource ID. The resource ID follows this format:

```text
/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}
```

You can find this value in the Azure portal by navigating to your AI Foundry project's **Profile** page under **Project details**.

### Option 1: Project + Template

Use an existing Azure AI Foundry project with a template:

```bash
azd ai finetuning init -p <project-resource-id> -t <template-url>
```

Example:

```bash
azd ai finetuning init \
  -t https://github.com/achauhan-scc/foundry-samples/blob/main/samples/python/finetuning/supervised \
  -p /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}
```

### Option 2: Project + Existing job

Clone configuration from an existing fine-tuning job:

```bash
azd ai finetuning init -p <project-resource-id> -j <job-id>
```

Example:

```bash
azd ai finetuning init \
  -p /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project} \
  -j ftjob-4cad7de198a34baeb4f0c95ff01ac844
```

### Option 3: Template only

Start from a template and configure the project later:

```bash
azd ai finetuning init -t <template-url>
```

Example:

```bash
azd ai finetuning init -t https://github.com/achauhan-scc/foundry-samples/blob/main/samples/python/finetuning/supervised
```


### Option 4: Clone from job

Clone configuration from an existing job ID:

```bash
azd ai finetuning init -j <job-id>
```

Example:

```bash
azd ai finetuning init -j ftjob-4cad7de198a34baeb4f0c95ff01ac844
```

### Option 5: Project endpoint only

Initialize with just your Azure AI Foundry project endpoint:

```bash
azd ai finetuning init -e <project-endpoint>
```

Example:

```bash
azd ai finetuning init -e https://account.services.ai.azure.com/api/projects/project-name
```

### Option 6: Interactive mode

Run without parameters for guided setup prompts:

```bash
azd ai finetuning init
```

### Option 7: Minimal init (with subscription lookup)

Use minimal initialization for a simplified interactive experience with subscription lookup:

```bash
azd init --minimal
```

This option provides guided prompts to select your subscription and configure your environment.

## Run fine-tuning commands

Navigate to your project folder (where `fine-tune-job.yaml` is located) and use the following commands to manage fine-tuning jobs.

> [!TIP]
> Looking for example job YAML files? Check out the [Fine-tuning CLI Samples](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/README.md) in the Foundry samples repository.

### Quick submit (skip initialization)

You can submit a job directly without running `azd init` first by providing the subscription and project endpoint inline:

```bash
azd ai finetuning jobs submit -f <path-to-yaml> -s <subscription-id> -e <project-endpoint>
```

Example:

```bash
azd ai finetuning jobs submit \
  -f /path-from-working-directory-to-config/job.yaml \
  -s a9096eb7-bfec-47e8-be27-b040b82afac9 \
  -e https://my-resource.services.ai.azure.com/api/projects/my-project
```

| Parameter | Description |
|-----------|-------------|
| `-f` | Path to the job YAML file |
| `-s` | Azure subscription ID |
| `-e` | Project endpoint URL |

### Submit a job

```bash
azd ai finetuning jobs submit -f ./fine-tune-job.yaml
```

### List jobs

```bash
azd ai finetuning jobs list
```

### Show job details

```bash
azd ai finetuning jobs show -i <job-id>
```

### Pause a job

```bash
azd ai finetuning jobs pause -i <job-id>
```

### Resume a job

```bash
azd ai finetuning jobs resume -i <job-id>
```

### Cancel a job

```bash
azd ai finetuning jobs cancel -i <job-id>
```

## Deploy your fine-tuned model

Once your fine-tuning job completes successfully, deploy the model for inference:

```bash
azd ai finetuning jobs deploy -i <job-id> -d "<deployment-name>" -c 100 -m "OpenAI" -s "GlobalStandard" -v "1"
```

| Parameter | Description |
|-----------|-------------|
| `-i` | Job ID |
| `-d` | Deployment name |
| `-c` | Capacity |
| `-m` | Model provider |
| `-s` | SKU name |
| `-v` | Version |

## Quick reference

### Init parameters

| Parameter | Description |
|-----------|-------------|
| `-p` | Project resource ID (ARM) |
| `-e` | Project endpoint URL |
| `-t` | Template URL or path |
| `-j` | Clone from job ID |
| `-w` | Working directory |
| `-n` | Environment name |
| `-s` | Subscription ID |

### Job parameters

| Parameter | Description |
|-----------|-------------|
| `-f` | YAML file path |
| `-i` | Job ID |

## Additional resources

- [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
- [Azure Developer CLI documentation](/azure/developer/azure-developer-cli/)
- [Microsoft Foundry documentation](/azure/ai-services/)
- [GitHub CLI](https://cli.github.com/)
- [Foundry samples repository - Fine-tuning CLI Samples](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/cli/finetuning/README.md)
- [Send feedback](https://forms.office.com/r/FQd419iHft)
