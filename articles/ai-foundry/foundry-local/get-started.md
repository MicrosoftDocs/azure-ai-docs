---
title: Get started with Foundry Local
titleSuffix: Foundry Local
description: Learn how to install, configure, and run your first AI model with Foundry Local
ms.date: 07/03/2025
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: quickstart
ms.reviewer: samkemp
ms.author: jburchel
author: jonburchel
reviewer: samuel100
ms.custom:
  - build-2025
  - build-aifnd
keywords:
  - Azure AI services
  - cognitive
  - AI models
  - local inference
# customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Get started with Foundry Local

[!INCLUDE [foundry-local-preview](./includes/foundry-local-preview.md)]

This guide walks you through setting up Foundry Local to run AI models on your device. 

## What makes Foundry Local different

Foundry Local is designed specifically for IT professionals who aren't LLM experts, offering a simplified approach to local AI model deployment with integrated features that go beyond basic model hosting.

### Foundry Local vs. other solutions

| Feature | Foundry Local | Hugging Face | NVIDIA | Llama |
|---------|---------------|--------------|--------|-------|
| **Target audience** | IT professionals, non-LLM experts | AI researchers, developers | GPU-focused developers | Meta ecosystem users |
| **Setup complexity** | Simple installation with automated configuration | Manual configuration required | Complex GPU setup | Variable complexity |
| **Hardware optimization** | Automatic hardware detection and optimization | Manual optimization needed | NVIDIA GPU focused | Platform dependent |
| **Integrated tooling** | Built-in CLI, API, and management tools | Separate tools required | Developer-focused tools | Limited tooling |
| **Enterprise features** | Security, compliance, and management ready | Community-focused | Enterprise through partnerships | Open source focused |
| **Model variety** | Curated catalog with automatic variants | Extensive model hub | NVIDIA-optimized models | Llama family models |

Foundry Local abstracts away the complexity of model deployment while providing enterprise-grade features for production use.

## Prerequisites

Your system must meet the following requirements to run Foundry Local:

- **Operating System**: Windows 10 (x64), Windows 11 (x64/ARM), Windows Server 2025, macOS.
- **Hardware**: Minimum 8GB RAM, 3GB free disk space. Recommended 16GB RAM, 15GB free disk space.
- **Network**: Internet connection for initial model download (optional for offline use)
- **Acceleration (optional)**: NVIDIA GPU (2,000 series or newer), AMD GPU (6,000 series or newer), Intel iGPU, Qualcomm Snapdragon X Elite (8GB or more of memory), or Apple silicon.

Also, ensure you have administrative privileges to install software on your device.

## Quickstart

Get started with Foundry Local quickly with these options:

### Option 1: Quick CLI setup

1. **Install Foundry Local** 
    - **Windows**: Open a terminal and run the following command:
        ```bash
        winget install Microsoft.FoundryLocal
        ```
    - **macOS**: Open a terminal and run the following command:
        ```bash
        brew tap microsoft/foundrylocal
        brew install foundrylocal
        ```
    Alternatively, you can download the installer from the [Foundry Local GitHub repository](https://aka.ms/foundry-local-installer).

1. **Run your first model** Open a terminal window and run the following command to run a model: 

    ```bash
    foundry model run phi-3.5-mini 
    ```
    
    The model downloads - which can take a few minutes, depending on your internet speed - and the model runs. Once the model is running, you can interact with it using the command line interface (CLI). For example, you can ask:

    ```text
    Why is the sky blue?
    ```

    You should see a response from the model in the terminal:
    :::image type="content" source="media/get-started-output.png" alt-text="Screenshot of output from foundry local run command." lightbox="media/get-started-output.png":::

### Option 2: Download starter projects

For practical, hands-on learning, download one of our starter projects that demonstrate real-world scenarios:

- **[Chat Application Starter](https://github.com/microsoft/foundry-local-samples/chat-app)**: Build a local chat interface with multiple model support
- **[API Integration Sample](https://github.com/microsoft/foundry-local-samples/api-integration)**: Integrate Foundry Local with existing applications
- **[Batch Processing Example](https://github.com/microsoft/foundry-local-samples/batch-processing)**: Process multiple inputs efficiently

Each project includes:
- Step-by-step setup instructions
- Complete source code
- Configuration examples
- Best practices implementation

> [!TIP]
> These starter projects align with scenarios covered in our [how-to guides](how-to/how-to-chat-application-with-open-web-ui.md) and provide immediate practical value.

> [!TIP]
> You can replace `phi-3.5-mini` with any model name from the catalog (see `foundry model list` for available models). Foundry Local downloads the model variant that best matches your system's hardware and software configuration. For example, if you have an NVIDIA GPU, it downloads the CUDA version of the model. If you have a Qualcomm NPU, it downloads the NPU variant. If you have no GPU or NPU, it downloads the CPU version.

## Run the latest OpenAI open-source model

To run the latest OpenAI open-source model - `GPT-OSS-20B` - use the following command:

```bash
foundry model run gpt-oss-20b
```

> [!IMPORTANT]
> Requirements for running GPT-OSS-20B:
> - Nvidia GPU with 16GB VRAM or more.
> - Foundry Local version **0.6.87** or above. Any version below this will not support the model. You can check your Foundry Local version by running:
> ```bash
> foundry --version
> ```

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

## Upgrading Foundry Local

To upgrade Foundry Local to the latest version, use the following commands based on your operating system:

- **Windows**: Open a terminal and run:
    ```bash
    winget upgrade --id Microsoft.FoundryLocal
    ```
- **macOS**: Open a terminal and run:
    ```bash
    brew upgrade foundrylocal
    ```

## Uninstalling Foundry Local

If you wish to uninstall Foundry Local, use the following commands based on your operating system:

- **Windows**: Open a terminal and run:
    ```bash
    winget uninstall Microsoft.FoundryLocal
    ```
- **macOS**: Open a terminal and run:
    ```bash
    brew rm foundrylocal
    brew untap microsoft/foundrylocal
    brew cleanup --scrub
    ```

## Related content

> [!div class="nextstepaction"]
> [Integrate inferencing SDKs with Foundry Local](how-to/how-to-integrate-with-inference-sdks.md)

> [!div class="nextstepaction"]
> [Explore the Foundry Local documentation](index.yml)

> [!div class="nextstepaction"]
> [Learn about best practices and troubleshooting](reference/reference-best-practice.md)

> [!div class="nextstepaction"]
> [Explore the Foundry Local API reference](reference/reference-catalog-api.md)

> [!div class="nextstepaction"]
> [Learn Compile Hugging Face models](how-to/how-to-compile-hugging-face-models.md)

