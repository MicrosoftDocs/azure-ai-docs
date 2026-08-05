---
title: "Foundry Local CLI Reference"
titleSuffix: Foundry Local
description: "Complete reference guide for the Foundry Local command-line interface."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.author: lajanuar
ms.reviewer: waynechuang
author: laujan
reviewer: wayne-ch
ms.topic: reference
ms.date: 08/05/2026
ai-usage: ai-assisted
---

# Foundry Local CLI reference
[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

This article provides a comprehensive reference for the Foundry Local command-line interface (CLI). The CLI organizes commands into logical categories to help you manage models, control the local server, and maintain your local cache.

## Prerequisites

- [Install Foundry Local](#install-foundry-local).
- A local terminal where the `foundry` CLI is available.
- Ensure you have internet access for first-time downloads (execution providers and models).
- Azure RBAC: Not applicable (runs locally).
- If you have an Intel NPU on Windows, install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) for optimal NPU acceleration.

## Install Foundry Local

Install Foundry Local by using the package manager for your operating system.

- **Windows**: Open a terminal and run:
  ```bash
  winget install Microsoft.FoundryLocal
  ```
- **macOS**: Open a terminal and run:
  ```bash
  brew tap microsoft/foundrylocal
  brew install foundrylocal
  ```
  Alternatively, download the installer from the [foundry-samples GitHub repository](https://aka.ms/foundry-local-installer).

Verify the installation:

```bash
foundry --version
```

Make sure you have admin rights to install software.

> [!TIP]
> If you see a service connection error after installation (for example, `Request to local service failed`), run `foundry server restart`.

## Quick verification

Run these commands to confirm the CLI is installed and the service is reachable.

1. Show CLI help:

	```bash
	foundry --help
	```

	This command prints usage information and the list of available command groups.

	Reference: [Overview](#overview)

1. Check the server status:

	```bash
  foundry server status
	```

  This command prints whether the Foundry Local daemon is running and includes its local endpoint.

  Reference: [Server commands](#server-commands)

## Overview

Use the built-in help to explore commands and options.

The CLI organizes commands into the following groups:

- **Model**: `model`, `cache`
- **Run**: `run`, `chat`, `complete`, `transcribe`
- **Server**: `server`
- **Setup**: `config`
- **Help**: `status`, `report`

The following table summarizes the top-level commands:

| **Command** | **Description** |
| --- | --- |
| `foundry model` | Discovers, inspects, downloads, loads, and unloads local models. |
| `foundry chat <model>` | Starts an interactive local chat session. |
| `foundry complete <model> <prompt>` | Generates one stateless text completion. |
| `foundry run <model>` | Runs a model with automatic routing to chat or transcription. |
| `foundry server` | Starts, stops, restarts, inspects, and troubleshoots the local Foundry daemon. |
| `foundry cache` | Inspects and manages downloaded model cache entries. |
| `foundry config` | Views and edits persistent Foundry CLI settings. |
| `foundry status` | Shows system, service, model, and connectivity diagnostics. |
| `foundry report` | Opens a pre-filled GitHub issue with diagnostics. |
| `foundry transcribe` | Starts an interactive local speech transcription session or transcribes a file. |

## Model commands

The following table summarizes the commands related to managing and running models:

> [!NOTE]
> You can specify the `model` argument by its **alias** or **model ID**. Using an alias:
>
> - Selects the best model for your available hardware automatically. For example, if you have an Nvidia GPU available, Foundry Local selects the best GPU model. If you have a supported NPU available, Foundry Local selects the NPU model.
> - Lets you use a shorter name without needing to remember the model ID.
>
> If you want to run a specific model, use the model ID. For example, to run the `qwen2.5-0.5b` on CPU, regardless of your available hardware, use `foundry run qwen2.5-0.5b-instruct-generic-cpu`.

| **Command** | **Description** |
| --- | --- |
| `foundry model --help` | Displays all available model-related commands and their usage. |
| `foundry model list` | Lists all available models for local use. On first run, it downloads execution providers (EPs) for your hardware. |
| `foundry model info <model>` | Displays detailed information about a specific model. |
| `foundry model download <model>` | Downloads a model to the local cache without running it. |
| `foundry model load <model>` | Loads a model into the service. |
| `foundry model unload <model>` | Unloads a model from the service. |

### Model list ordering

When multiple model ID variants are available for an alias, the model list shows the models in priority order. The first model in the list is the model that runs when you specify the model by `alias`.

### Model list filtering

Use the explicit options for `foundry model list` to narrow or expand the results.

> [!NOTE]
> When you run `foundry model list` for the first time after installation, Foundry Local automatically downloads the relevant execution providers (EPs) for your machine's hardware configuration. You see a progress bar indicating the download completion before the model list appears.

| **Option** | **Description** |
| --- | --- |
| `--device <device>` | Filters models by device. |
| `--type <type>` | Filters models by type. |
| `--search <query>` | Filters models by a search query. |
| `--cached` | Filters the list to cached models. |
| `--loaded` | Filters the list to loaded models. |
| `--variants` | Includes model variants in the list. |

### Examples

```bash
foundry model list --device gpu
foundry model list --type chat
foundry model list --search qwen
foundry model list --cached
foundry model list --loaded
foundry model list --variants
```

These examples filter or expand the model list by using the supported options.

Reference: [Model list filtering](#model-list-filtering)

### Run a model interactively

Run a model and interact with it directly in the terminal:

```bash
foundry chat qwen2.5-0.5b
```

Foundry Local downloads the model on first run, then starts an interactive session. Enter a prompt to get a response:

```text
Why is the sky blue?
```

> [!TIP]
> Replace `qwen2.5-0.5b` with any model alias from the catalog. Run `foundry model list` to view available models. Foundry Local downloads the variant that best matches your hardware — for example, a CUDA variant for NVIDIA GPUs or an NPU variant for Qualcomm NPUs.

## Server commands

The following table summarizes the commands related to managing and running the Foundry Local service:

| **Command** | **Description** |
| --- | --- |
| `foundry server --help` | Displays all available server-related commands and their usage. |
| `foundry server start` | Starts the Foundry Local daemon and OpenAI-compatible local service. |
| `foundry server start --port <port>` | Starts the local service on the specified TCP port. Use `0` for an OS-assigned port. |
| `foundry server start --idle-timeout <minutes>` | Stops the daemon after the specified number of inactive minutes. Use `0` to keep the daemon running. |
| `foundry server stop` | Stops the Foundry Local daemon. |
| `foundry server restart` | Restarts the Foundry Local daemon and local service. |
| `foundry server restart --port <port> --idle-timeout 0` | Restarts the local service on the specified TCP port and keeps the daemon running. |
| `foundry server status` | Displays the daemon state, local service URLs, process ID, uptime, and log location. |
| `foundry server logs` | Displays the Foundry Local daemon and SDK logs. |

### Fixed-port local server

To start the local service on a fixed port and keep the daemon running, use `--port` with `--idle-timeout 0`:

```bash
foundry server start --port 39839 --idle-timeout 0
```

If the daemon is already running and you need to apply a new port, restart it with the same options:

```bash
foundry server restart --port 39839 --idle-timeout 0
```

To verify the local endpoint URL, run:

```bash
foundry server status
```

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

## Use Open WebUI with the local server

Connect [Open WebUI](https://github.com/open-webui/open-webui) to Foundry Local for a browser-based chat interface that runs entirely on your device.

1. Start a model and leave the terminal open:

   ```bash
  foundry run qwen2.5-0.5b
   ```

1. Get your local endpoint URL:

   ```bash
  foundry server status
   ```

   Copy the endpoint URL. Foundry Local assigns a dynamic port each time the service starts.

1. Install and launch [Open WebUI](https://github.com/open-webui/open-webui), then open `http://localhost:8080` in your browser.

1. Connect Open WebUI to Foundry Local:

   1. Go to **Settings** > **Admin Settings** > **Connections** and enable **Direct Connections**.
   1. Go to **Settings** > **Connections** > **Manage Direct Connections** and select **+**.
   1. Set **URL** to `http://localhost:PORT/v1` (replace `PORT` with the port from step 2) and **Auth** to **None**.
   1. Select **Save**.

1. Select a model from the dropdown and start chatting.

> [!TIP]
> If no models appear, run `foundry run <model>` in a terminal and reload Open WebUI. If the connection fails, confirm the port with `foundry server status`.

## Upgrade Foundry Local

Run the command for your operating system to upgrade Foundry Local.

- **Windows**:
  ```bash
  winget upgrade --id Microsoft.FoundryLocal
  ```
- **macOS**:
  ```bash
  brew upgrade foundrylocal
  ```

## Uninstall Foundry Local

Run the command for your operating system to uninstall Foundry Local.

- **Windows**:
  ```bash
  winget uninstall Microsoft.FoundryLocal
  ```
- **macOS**:
  ```bash
  brew rm foundrylocal
  brew untap microsoft/foundrylocal
  brew cleanup --scrub
  ```

## Troubleshooting

### Service connection problems

If you see this error when you run a command like `foundry model list`:

```text
Exception: Request to local service failed.
Uri: http://127.0.0.1:0/foundry/list

The requested address is not valid in its context. (127.0.0.1:0)

Please check service status with 'foundry server status'.
```

Restart the service:

```bash
foundry server restart
```

This command fixes cases where the server runs but isn't accessible because of a port binding problem.

For more troubleshooting guidance, see [Best practices and troubleshooting](reference-best-practice.md).