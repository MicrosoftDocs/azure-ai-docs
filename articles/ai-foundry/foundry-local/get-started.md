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

This guide walks you through setting up Foundry Local to run AI models on your device. 

## Prerequisites

Your system must meet the following requirements to run Foundry Local:

- **Operating System**: Windows 10 (x64), Windows 11 (x64/ARM), macOS.
- **Hardware**: Minimum 8GB RAM, 3GB free disk space. Recommended 16GB RAM, 15GB free disk space.
- **Network**: Internet connection for initial model download (optional for offline use)
- **Acceleration (optional)**: NVIDIA GPU (2,000 series or newer), AMD GPU (6,000 series or newer), or Qualcomm Snapdragon X Elite, with 8GB or more of memory (RAM).

Also, ensure you have administrative privileges to install software on your device.

## Quickstart

Get started with Foundry Local quickly:

1. [**Download Foundry Local Installer**](https://aka.ms/foundry-local-installer) and **install** by following the on-screen prompts. 
    > [!TIP]
    > If you're installing on Windows, you can also use `winget` to install Foundry Local. Open a terminal window and run the following command:
    >
    > ```powershell
    > winget install Microsoft.FoundryLocal
    > ```
1. **Run your first model** Open a terminal window and run the following command to run a model: 

    ```bash
    foundry model run deepseek-r1-1.5b 
    ```
    
    The model downloads - which can take a few minutes, depending on your internet speed - and the model runs. Once the model is running, you can interact with it using the command line interface (CLI). For example, you can ask:

    ```text
    Why is the sky blue?
    ```

    You should see a response from the model in the terminal:
    :::image type="content" source="media/get-started-output.png" alt-text="Output from foundry local run command.":::


> [!TIP]
> You can replace `deepseek-r1-1.5b` with any model name from the catalog (see `foundry model list` for available models). Foundry Local downloads the model variant that best matches your system's hardware and software configuration. For example, if you have an NVIDIA GPU, it downloads the CUDA version of the model. If you have a Qualcomm NPU, it downloads the NPU variant. If you have no GPU or NPU, it downloads the CPU version.

## Explore commands

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

- [Integrate inferencing SDKs with Foundry Local](how-to/how-to-integrate-with-inference-sdks.md)
- [Explore the Foundry Local documentation](index.yml)
- [Learn about best practices and troubleshooting](reference/reference-best-practice.md)
- [Explore the Foundry Local API reference](reference/reference-catalog-api.md)
- [Learn Compile Hugging Face models](how-to/how-to-compile-hugging-face-models.md)

