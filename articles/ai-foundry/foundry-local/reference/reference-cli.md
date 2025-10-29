---
title: Foundry Local CLI Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local command-line interface.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.topic: concept-article
ms.date: 10/01/2025
ai-usage: ai-assisted
---

# Foundry Local CLI Reference

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article provides a comprehensive reference for the Foundry Local command-line interface (CLI). The CLI organizes commands into logical categories to help you manage models, control the service, and maintain your local cache.

## Overview

View all available commands with the help option:

```bash
foundry --help
```

The CLI organizes commands into three main categories:

- **Model**: Commands for managing and running AI models
- **Service**: Commands for controlling the Foundry Local service
- **Cache**: Commands for managing your local model storage

## Model commands

The following table summarizes the commands related to managing and running models:

> [!NOTE]
> You can specify the `model` argument by its **alias** or **model ID**. Using an alias:
>
> - Selects the _best model_ for your available hardware. For example, if you have an Nvidia CUDA GPU available, Foundry Local selects the CUDA model. If you have a supported NPU available, Foundry Local selects the NPU model.
> - Lets you use a shorter name without needing to remember the model ID.
>
> If you want to run a specific model, use the model ID. For example, to run the `qwen2.5-0.5b` on CPU - irrespective of your available hardware - use: `foundry model run qwen2.5-0.5b-instruct-generic-cpu`.
>
> If you have an Intel NPU on Windows, ensure you install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) for optimal NPU acceleration.

| **Command**                                 | **Description**                                                                                                |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `foundry model --help`                      | Displays all available model-related commands and their usage.                                                 |
| `foundry model run <model>`                 | Runs a specified model, downloads it if it isn't cached, and starts an interaction.                               |
| `foundry model list`                        | Lists all available models for local use. On first run, it downloads execution providers (EPs) for your hardware. |
| `foundry model list --filter <key>=<value>` | Lists models filtered by the specified criteria (device, task, alias, provider).                               |
| `foundry model info <model>`                | Displays detailed information about a specific model.                                                          |
| `foundry model info <model> --license`      | Displays the license information for a specific model.                                                         |
| `foundry model download <model>`            | Downloads a model to the local cache without running it.                                                       |
| `foundry model load <model>`                | Loads a model into the service.                                                                                |
| `foundry model unload <model>`              | Unloads a model from the service.                                                                              |

### Model list filtering

The `foundry model list` command supports filtering models using the `--filter` option. You can filter models based on a single attribute using key-value pairs.

```bash
foundry model list --filter <key>=<value>
```

> [!NOTE]
> When you run `foundry model list` for the first time after installation, Foundry Local automatically downloads the relevant execution providers (EPs) for your machine's hardware configuration. You see a progress bar indicating the download completion before the model list appears.

**Supported filter keys:**

#### device - Hardware Device Type

Filters models by the hardware device they run on.

**Possible values:**

- `CPU` - Central Processing Unit models
- `GPU` - Graphics Processing Unit models
- `NPU` - Neural Processing Unit models

#### provider - Execution Provider

Filters models by their execution provider/runtime.

**Possible values:**

- `CPUExecutionProvider` - CPU-based execution
- `CUDAExecutionProvider` - NVIDIA CUDA GPU execution
- `WebGpuExecutionProvider` - WebGPU execution
- `QNNExecutionProvider` - Qualcomm Neural Network execution (NPU)
- `OpenVINOExecutionProvider` - Intel OpenVINO execution
- `NvTensorRTRTXExecutionProvider` - NVIDIA TensorRT execution
- `VitisAIExecutionProvider` - AMD Vitis AI execution

#### task - Model Task Type

Filters models by their intended use case/task.

**Common values:**

- `chat-completion`: Conversational AI models
- `text-generation`: Text generation models

#### alias - Model Alias

Filters models by their alias identifier. Supports wildcard matching with `*` suffix.

**Sample values:**

- `phi4-cpu`
- `qwen2.5-coder-0.5b-instruct-generic-cpu`
- `deepseek-r1-distill-qwen-1.5b-generic-cpu`
- `phi-4-mini-instruct-generic-cpu`

### Special filter features

**Negation Support:** Prefix any value with `!` to exclude matching models.

```bash
foundry model list --filter device=!GPU
```

**Wildcard Matching (alias only):** Append `*` to match prefixes when filtering by alias.

```bash
foundry model list --filter alias=qwen*
```

### Examples

```bash
foundry model list --filter device=GPU
foundry model list --filter task=chat-completion
foundry model list --filter provider=CUDAExecutionProvider
```

> [!NOTE]
>
> - All comparisons are case-insensitive.
> - Only one filter can be used per command.
> - Unrecognized filter keys result in an error.

## Service commands

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command**                     | **Description**                                                  |
| ------------------------------- | ---------------------------------------------------------------- |
| `foundry service --help`        | Displays all available service-related commands and their usage. |
| `foundry service start`         | Starts the Foundry Local service.                                |
| `foundry service stop`          | Stops the Foundry Local service.                                 |
| `foundry service restart`       | Restarts the Foundry Local service.                              |
| `foundry service status`        | Displays the current status of the Foundry Local service.        |
| `foundry service ps`            | Lists all models currently loaded in the Foundry Local service.  |
| `foundry service diag`          | Displays the logs of the Foundry Local service.                  |
| `foundry service set <options>` | Sets the configuration of the Foundry Local service.                  |

## Cache commands

The following table summarizes the commands for managing the local cache where models are stored:

| **Command**                    | **Description**                                                |
| ------------------------------ | -------------------------------------------------------------- |
| `foundry cache --help`         | Shows all available cache-related commands and their usage. |
| `foundry cache location`       | Shows the current cache directory.                          |
| `foundry cache list`           | Lists all models stored in the local cache.                    |
| `foundry cache cd <path>`      | Changes the cache directory to the specified path.                                   |
| `foundry cache remove <model>` | Removes a model from the local cache.                          |
