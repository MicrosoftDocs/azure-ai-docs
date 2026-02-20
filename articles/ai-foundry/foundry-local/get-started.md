---
title: Get started with Foundry Local
titleSuffix: Foundry Local
description: Learn how to install, configure, and run your first AI model with Foundry Local
ms.date: 10/13/2023
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
  - peer-review-program 
  - dev-focus
keywords:
  - Foundry Tools
  - cognitive
  - AI models
  - local inference
ai-usage: ai-assisted
# customer intent: As a developer, I want to get started with Foundry Local so that I can run AI models locally.
---

# Get started with Foundry Local

[!INCLUDE [foundry-local-preview](./includes/foundry-local-preview.md)]

This guide shows you how to set up Foundry Local to run AI models on your device.

## Prerequisites

Your system must meet the following requirements to run Foundry Local:

- **Operating System**: Windows 10 (x64), Windows 11 (x64/ARM), Windows Server 2025, macOS.
- **Hardware**: Minimum 8 GB RAM and 3 GB free disk space. Recommended 16 GB RAM and 15 GB free disk space.
- **Network**: Internet connection to download models and execution providers. After you download a model, you can run cached models offline.
- **Acceleration (optional)**: NVIDIA GPU (2000 series or newer), AMD GPU (6000 series or newer), AMD NPU, Intel iGPU, Intel NPU (32 GB or more of memory), Qualcomm Snapdragon X Elite (8 GB or more of memory), Qualcomm NPU, or Apple silicon.

To install Foundry Local by using the commands in this quickstart:

- On Windows, make sure `winget` is available.
- On macOS, install Homebrew if you use the `brew` option.

> [!NOTE]
> New NPUs are supported only on systems running Windows 24H2 or later. If you use an Intel NPU on Windows, install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable NPU acceleration in Foundry Local.

Make sure you have admin rights to install software.

> [!TIP]
> If you see a service connection error after installation (for example, 'Request to local service failed'), run `foundry service restart`.

## Quickstart

Get started quickly with Foundry Local:

### Option 1: Quick CLI setup

1. **Install Foundry Local**.

   - **Windows**: Open a terminal and run the following command.
     ```bash
     winget install Microsoft.FoundryLocal
     ```
   - **macOS**: Open a terminal and run the following command.
     ```bash
     brew tap microsoft/foundrylocal
     brew install foundrylocal
     ```
     Alternatively, you can download the installer from the [Foundry Local GitHub repository](https://aka.ms/foundry-local-installer).

    Reference: [Foundry Local documentation](https://aka.ms/foundry-local-docs)

  1. **Verify the installation**. Run:
     ```bash
     foundry --version
     ```
     You should see the installed version number.

     Reference: [Foundry Local CLI reference](reference/reference-cli.md)

1. **Run your first model**. Open a terminal and run this command:
   ```bash
   foundry model run qwen2.5-0.5b
   ```

   Foundry Local downloads the model, which can take a few minutes depending on your internet speed, then runs it. After the model starts, interact with it by using the command-line interface (CLI). For example, you can ask:

   ```text
   Why is the sky blue?
   ```

   You see a response from the model in the terminal:
   :::image type="content" source="media/get-started-output.png" alt-text="Screenshot of output from Foundry Local run command." lightbox="media/get-started-output.png":::

  Reference: [Foundry Local CLI reference](reference/reference-cli.md)

### Option 2: Download starter projects

For practical, hands-on learning, download one of the starter projects that demonstrate real-world scenarios:

- [Chat Application Starter](https://github.com/microsoft/Foundry-Local/tree/main/samples/electron/foundry-chat): Build a local chat interface with multiple model support.
- [Summarize Sample](https://github.com/microsoft/Foundry-Local/tree/main/samples/python/summarize): A command-line utility that generates summaries of text files or direct text input.
- [Function Calling Example](https://github.com/microsoft/Foundry-Local/tree/main/samples/python/functioncalling): Enable and use function calling with Phi-4 mini.

Each project includes:

- Step-by-step setup instructions
- Complete source code
- Configuration examples
- Best practices

> [!TIP]
> These starter projects align with scenarios in the [how-to guides](how-to/how-to-chat-application-with-open-web-ui.md) and provide immediate practical value.

> [!TIP]
> Replace `qwen2.5-0.5b` with any model name from the catalog (run `foundry model list` to view available models). Foundry Local downloads the variant that best matches your system's hardware and software configuration. For example, if you have an NVIDIA GPU, Foundry Local downloads the CUDA version. If you have a Qualcomm NPU, Foundry Local downloads the NPU variant. If you have no GPU or NPU, Foundry Local downloads the CPU version.
>
> When you run `foundry model list` the first time, you see a download progress bar while Foundry Local downloads the execution providers for your hardware.

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

## Explore commands

The Foundry CLI organizes commands into these main categories:

- **Model**: Commands for managing and running models.
- **Service**: Commands for managing the Foundry Local service.
- **Cache**: Commands for managing the local model cache (downloaded models on local disk).

### Chat Completion Command

The `chat-completion` command uses OpenAI's Chat API to stream chat completions. It supports the following arguments and options:

#### Arguments:
- `model`: Specifies the model to use for chat completion.
- `promptMessage`: The prompt message to send to the model.

#### Options:
- `--imageFilePath`: (Optional) Path to an image file to include in the prompt.
- `--maxTokens`: (Optional) Maximum number of tokens for the response.

#### Example:
```bash
foundry chat-completion --model gpt-oss-20b --promptMessage "What is the capital of France?" --maxTokens 100
```

This command sends the prompt message to the specified model and streams the response in real time.

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

### Download Model Command

The `download-model` command downloads models from a specified URI to a local directory. It supports the following arguments and options:

#### Arguments:
- `uri`: The URI of the model to download.
- `outputDirectory`: The directory where the model will be saved.

#### Options:
- `--revision`: (Optional) Specifies the revision of the model.
- `--path`: (Optional) Custom path for the model.
- `--token`: (Optional) Authentication token for the model provider.
- `--bufferSize`: (Optional) Buffer size for downloading.
- `--provider`: (Optional) Specifies the provider for the model.

#### Example:
```bash
foundry download-model --uri https://models.example.com/model1 --outputDirectory ./models --revision v1 --provider openai
```

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

### Download Model Catalog Command

The `download-model-catalog` command downloads models from a catalog based on the model name. It supports the following arguments and options:

#### Arguments:
- `modelName`: The name of the model to download.
- `outputDirectory`: The directory where the model will be saved.

#### Options:
- `--bufferSize`: (Optional) Buffer size for downloading.
- `--provider`: (Optional) Specifies the provider for the model.

#### Example:
```bash
foundry download-model-catalog --modelName gpt-oss-20b --outputDirectory ./models --provider openai
```

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

To view all commands, use:

```bash
foundry --help
```

```bash
foundry model --help
```

```bash
foundry service --help
```

View **cache** commands:

```bash
foundry cache --help
```

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

## Optional: Run the latest GPT OSS 20B model

Run the `gpt-oss-20b` model:

```bash
foundry model run gpt-oss-20b
```

> [!IMPORTANT]
> If the model isn't available for your device, run a smaller model (for example, `qwen2.5-0.5b`).
>
> For the CUDA variant, you typically need an NVIDIA GPU with 16 GB of VRAM or more.
>
> Foundry Local version **0.6.87** or later adds support for this model. Check your version with:
>
> ```bash
> foundry --version
> ```

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

> [!TIP]
> For details on all CLI commands, see [Foundry Local CLI reference](reference/reference-cli.md).

## Upgrade Foundry Local

Run the command for your OS to upgrade Foundry Local.

- Windows: In a terminal, run:
  ```bash
  winget upgrade --id Microsoft.FoundryLocal
  ```
- macOS: In a terminal, run:
  ```bash
  brew upgrade foundrylocal
  ```

## Uninstall Foundry Local

To uninstall Foundry Local, run the command for your operating system:

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

## Troubleshooting

### Service connection problems

If you see this error when you run `foundry model list` or a similar command:

```text
foundry model list

Exception: Request to local service failed.
Uri: http://127.0.0.1:0/foundry/list

The requested address is not valid in its context. (127.0.0.1:0)

Please check service status with 'foundry service status'.
```

Run this command to restart the service:

```bash
foundry service restart
```

This command fixes cases where the service runs but isn't accessible because of a port binding problem.

Reference: [Best practices and troubleshooting](reference/reference-best-practice.md)

## Related content

- [Integrate inference SDKs with Foundry Local](how-to/how-to-integrate-with-inference-sdks.md)
- [Foundry Local documentation](index.yml)
- [Best practices and troubleshooting](reference/reference-best-practice.md)
- [Foundry Local API reference](reference/reference-catalog-api.md)
- [Compile Hugging Face models](how-to/how-to-compile-hugging-face-models.md)
- [Foundry Local on Windows Server 2025](reference/windows-server-frequently-asked-questions.md)