---
title: Foundry Local CLI Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local command-line interface.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.topic: concept-article
ms.date: 10/10/2023
ai-usage: ai-assisted
---

# Foundry Local CLI reference

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article provides a comprehensive reference for the Foundry Local command-line interface (CLI). The CLI organizes commands into logical categories to help you manage models, control the service, and maintain your local cache.

## Prerequisites

- Install Foundry Local. For setup steps, see [Get started with Foundry Local](../get-started.md).
- Use a local terminal where the `foundry` CLI is available.
- Ensure you have internet access for first-time downloads (execution providers and models).
- Azure RBAC: Not applicable (runs locally).
- If you have an Intel NPU on Windows, install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) for optimal NPU acceleration.

## Quick verification

Run these commands to confirm the CLI is installed and the service is reachable.

1. Show CLI help:

	```bash
	foundry --help
	```

	This command prints usage information and the list of available command groups.

	Reference: [Overview](#overview)

1. Check the service status:

	```bash
	foundry service status
	```

	This command prints whether the Foundry Local service is running and includes its local endpoint.

	Reference: [Service commands](#service-commands)

## Overview

Use the built-in help to explore commands and options.

The CLI organizes commands into three main categories:

- **Model**: Commands for managing and running AI models
- **Service**: Commands for controlling the Foundry Local service
- **Cache**: Commands for managing your local model storage

## Model commands

The following table summarizes the commands related to managing and running models:

> [!NOTE]
> You can specify the `model` argument by its **alias** or **model ID**. Using an alias:
>
> - Selects the best model for your available hardware automatically. For example, if you have an Nvidia GPU available, Foundry Local selects the best GPU model. If you have a supported NPU available, Foundry Local selects the NPU model.
> - Lets you use a shorter name without needing to remember the model ID.
>
> If you want to run a specific model, use the model ID. For example, to run the `qwen2.5-0.5b` on CPU - irrespective of your available hardware - use: `foundry model run qwen2.5-0.5b-instruct-generic-cpu`.

| **Command** | **Description** |
| --- | --- |
| `foundry model --help` | Displays all available model-related commands and their usage. |
| `foundry model run <model>` | Runs a specified model, downloads it if it isn't cached, and starts an interaction. |
| `foundry model list` | Lists all available models for local use. On first run, it downloads execution providers (EPs) for your hardware. |
| `foundry model list --filter <key>=<value>` | Lists models filtered by the specified criteria (device, task, alias, provider). |
| `foundry model info <model>` | Displays detailed information about a specific model. |
| `foundry model info <model> --license` | Displays the license information for a specific model. |
| `foundry model download <model>` | Downloads a model to the local cache without running it. |
| `foundry model load <model>` | Loads a model into the service. |
| `foundry model unload <model>` | Unloads a model from the service. |
| `foundry model chat-completion` | Streams chat completions using OpenAI's Chat API. |

### Chat Completion Command

The `foundry model chat-completion` command allows you to interact with conversational AI models using OpenAI's Chat API. You can specify the model, prompt message, and additional options for enhanced functionality.

#### Arguments

| **Argument** | **Description** |
| --- | --- |
| `model` | The model to use for generating chat completions. Specify by alias or model ID. |
| `promptMessage` | The input prompt for the chat model. |

#### Options

| **Option** | **Description** |
| --- | --- |
| `--imageFilePath <path>` | Optional. Specifies the path to an image file to provide additional context for the chat model. |
| `--maxTokens <number>` | Optional. Sets the maximum number of tokens for the response. |

#### Examples

```bash
foundry model chat-completion qwen2.5-coder-0.5b-instruct-generic-cpu "Write a poem about AI."
```

This command uses the `qwen2.5-coder-0.5b-instruct-generic-cpu` model to generate a poem about AI.

```bash
foundry model chat-completion phi4-cpu "Summarize the latest AI trends." --maxTokens 100
```

This command generates a summary of AI trends with a maximum of 100 tokens.

```bash
foundry model chat-completion phi4-cpu "Analyze this image." --imageFilePath ./images/sample.jpg
```

This command analyzes the provided image file using the specified model.

---

## Download commands

The following table summarizes the commands for downloading models and catalogs:

| **Command** | **Description** |
| --- | --- |
| `foundry model download <model>` | Downloads a model to the local cache without running it. |
| `foundry model download-model` | Downloads a model using a URI and saves it to the specified output directory. |
| `foundry model download-model-catalog` | Downloads models from a catalog using the model name and output directory. |

### Download Model Command

The `foundry model download-model` command supports downloading models using various providers. You can specify the URI, output directory, and additional options.

#### Arguments

| **Argument** | **Description** |
| --- | --- |
| `uri` | The URI of the model to download. |
| `outputDirectory` | The directory where the downloaded model will be saved. |

#### Options

| **Option** | **Description** |
| --- | --- |
| `--revision <revision>` | Optional. Specifies the model revision to download. |
| `--path <path>` | Optional. Specifies a custom path for the downloaded model. |
| `--token <token>` | Optional. Authentication token for accessing the model. |
| `--bufferSize <size>` | Optional. Sets the buffer size for downloading. |
| `--provider <provider>` | Optional. Specifies the provider for downloading the model. |

#### Examples

```bash
foundry model download-model https://example.com/model.zip ./models
```

This command downloads the model from the specified URI and saves it to the `./models` directory.

```bash
foundry model download-model https://example.com/model.zip ./models --revision v1.2 --provider OpenVINOExecutionProvider
```

This command downloads the model revision `v1.2` using the OpenVINO execution provider.

---

### Download Model Catalog Command

The `foundry model download-model-catalog` command supports downloading models from a catalog using the model name and output directory.

#### Arguments

| **Argument** | **Description** |
| --- | --- |
| `modelName` | The name of the model to download from the catalog. |
| `outputDirectory` | The directory where the downloaded model will be saved. |

#### Options

| **Option** | **Description** |
| --- | --- |
| `--bufferSize <size>` | Optional. Sets the buffer size for downloading. |
| `--provider <provider>` | Optional. Specifies the provider for downloading the model. |

#### Examples

```bash
foundry model download-model-catalog phi4-cpu ./models
```

This command downloads the `phi4-cpu` model from the catalog and saves it to the `./models` directory.

```bash
foundry model download-model-catalog qwen2.5-coder-0.5b ./models --provider CUDAExecutionProvider
```

This command downloads the `qwen2.5-coder-0.5b` model using the CUDA execution provider.

---

## Service commands

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command** | **Description** |
| --- | --- |
| `foundry service --help` | Displays all available service-related commands and their usage. |
| `foundry service start` | Starts the Foundry Local service. |
| `foundry service stop` | Stops the Foundry Local service. |
| `foundry service restart` | Restarts the Foundry Local service. |
| `foundry service status` | Displays the current status of the Foundry Local service. |
| `foundry service ps` | Lists all models currently loaded in the Foundry Local service. |
| `foundry service diag` | Displays the logs of the Foundry Local service. |
| `foundry service set <options>` | Sets the configuration of the Foundry Local service. |

## Cache commands

The following table summarizes the commands for managing the local cache where models are stored:

| **Command** | **Description** |
| --- | --- |
| `foundry cache --help` | Shows all available cache-related commands and their usage. |
| `foundry cache location` | Shows the current cache directory. |
| `foundry cache list` | Lists all models stored in the local cache. |
| `foundry cache cd <path>` | Changes the cache directory to the specified path. |
| `foundry cache remove <model>` | Removes a model from the local cache. |

## Execution providers

Execution providers are hardware-specific acceleration libraries that run models as efficiently as possible on your device.

### Built-in execution providers

Foundry Local includes the CPU execution provider, the WebGPU execution provider, and the CUDA execution provider. 

The CPU execution provider uses [Microsoft Linear Algebra Subroutines (MLAS)](https://github.com/microsoft/mlas) to run on any CPU and is the CPU fallback for Foundry Local.

The WebGPU execution provider uses [Dawn](https://github.com/google/dawn), the native implementation of the web-based API, for acceleration on any GPU, and is the GPU fallback for Foundry Local.

The CUDA execution provider uses NVIDIA CUDA for acceleration on NVIDIA GPUs. It requires an NVIDIA GeForce RTX 30 series and later with a minimum recommended driver version 32.0.15.5585 and CUDA version 12.5. It's subject to the following license terms: [License Agreement for NVIDIA Software Development Kits—EULA](https://docs.nvidia.com/cuda/eula/index.html). 


### Plugin execution providers

The execution providers listed in the following table are available for dynamic download and registration on Windows, depending on device and driver compatibility. They're subject to the license terms specified.

Foundry Local automatically downloads these execution providers on first run. The plugin execution providers automatically update when new versions are available.

| Name (Vendor) | Requirements | License terms |
| --- | --- | --- |
| `NvTensorRTRTXExecutionProvider` (NVIDIA) | NVIDIA GeForce RTX 30XX and later versions with minimum recommended driver version 32.0.15.5585 and CUDA version 12.5 | [License Agreement for NVIDIA Software Development Kits—EULA](https://docs.nvidia.com/cuda/eula/index.html) |
| `OpenVINOExecutionProvider` (Intel) | CPU: Intel TigerLake (11th Gen) and later versions with min recommended driver 32.0.100.9565<br>GPU: Intel AlderLake (12th Gen) and later versions with min recommended driver 32.0.101.1029<br>NPU: Intel ArrowLake (15th Gen) and later versions with min recommended driver 32.0.100.4239 | [Intel OBL Distribution Commercial Use License Agreement v2025.02.12](https://cdrdv2.intel.com/v1/dl/getContent/849090?explicitVersion=true) |
| `QNNExecutionProvider` (Qualcomm) | Snapdragon(R) X Elite - X1Exxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and later versions<br>Snapdragon(R) X Plus - X1Pxxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and later versions | To view the QNN License, download the Qualcomm® Neural Processing SDK, extract the ZIP, and open the LICENSE.pdf file. |
| `VitisAIExecutionProvider` (AMD) | Min: Adrenalin Edition 25.6.3 with NPU driver 32.00.0203.280<br>Max: Adrenalin Edition 25.9.1 with NPU driver 32.00.0203.297 | No additional license required |

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local overview](../overview.md)