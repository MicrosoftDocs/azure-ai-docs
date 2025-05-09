---
title: Get started with Foundry Local
titleSuffix: Foundry Local
description: Learn how to install, configure, and run your first AI model with Foundry Local
manager: scottpolly
keywords: Azure AI services, cognitive, AI models, local inference
ms.service: azure-ai-foundry
ms.topic: quickstart
ms.date: 02/20/2025
ms.reviewer: samkemp
ms.author: samkemp
author: samuel100
ms.custom: build-2025
#customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Get started with Foundry Local

This guide walks you through setting up Foundry Local to run AI models on your device. Follow these clear steps to install the tool, discover available models, and launch your first local AI model.

## Prerequisites

Your system must meet the following requirements to run Foundry Local:

- **Operating System**: Windows 10 (x64), Windows 11 (x64/ARM), macOS, or Linux (x64/ARM)
- **Hardware**: Minimum 8GB RAM, 3GB free disk space. Recommended 16GB RAM, 15GB free disk space.
- **Network**: Internet connection for initial model download (optional for offline use)
- **Acceleration (optional)**: NVIDIA GPU (2,000 series or newer), AMD GPU (6,000 series or newer), or Qualcomm Snapdragon X Elite, with 8GB or more of memory (RAM).

Also, ensure you have administrative privileges to install software on your device.

## Quickstart

Get started with Foundry Local quickly:

1. **Download** Foundry Local for your platform:
   - [Windows](https://aka.ms/foundry-local-windows)
   - [macOS](https://aka.ms/foundry-local-macos)
   - [Linux](https://aka.ms/foundry-local-linux)
1. **Install** the package by following the on-screen prompts.
1. **Run your first model** Open a terminal window and run the following command to run a model (the model will be downloaded and an interactive prompt will appear): 

    ```bash
    foundry model run phi-3-mini-4k 
    ```

> [!TIP]
> You can replace `phi-3-mini-4k` with any model name from the catalog (see `foundry model list` for available models). Foundry Local will download the model variant that best matches your system's hardware and software configuration. For example, if you have an NVIDIA GPU, it will download the CUDA version of the model. If you have an QNN NPU, it will download the NPU variant. If you have no GPU or NPU, it will download the CPU version.

> [!IMPORTANT]
> **For macOS/Linux users:** Run both components in separate terminals:
> - Neutron Server (`Inference.Service.Agent`) - Make it executable with `chmod +x Inference.Service.Agent`
> - Foundry Client (`foundry`) - Make it executable with `chmod +x foundry` and add it to your PATH

## Explore Foundry Local CLI commands

The Foundry CLI organizes commands into these main categories:

- **Model**: Commands for managing and running models.
- **Service**: Commands for managing the Foundry Local service.
- **Cache**: Commands for managing the local model cache (downloaded models on local disk).

View all available commands with:

```bash
foundry --help
```

To view available **model** commands, run:

```bash
foundry model --help
```
To view available **service** commands, run:

```bash
foundry service --help
```

To view available **cache** commands, run:

```bash
foundry cache --help
```

> [!TIP]
> For a complete guide to all CLI commands and their usage, see the [Foundry Local CLI Reference](reference/reference-cli.md).


## Next steps

- [Learn how to integrate Foundry Local with your applications](how-to/integrate-with-inference-sdks.md)
- [Explore the Foundry Local documentation](index.yml)
- [Learn about best practices and troubleshooting](reference/reference-best-practice.md)
- [Explore the Foundry Local API reference](reference/reference-catalog-api.md)
- [Learn how to compile Hugging Face models](how-to/how-to-compile-hf-models.md)

