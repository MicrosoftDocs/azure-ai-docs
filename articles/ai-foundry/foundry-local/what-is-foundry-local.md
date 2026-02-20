---
title: What is Foundry Local?
titleSuffix: Foundry Local
description: Foundry Local is an on-device AI inference solution that lets you run AI models locally through a CLI, SDK, or REST API.
keywords: Foundry Tools, cognitive
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: overview
ms.date: 10/06/2023
ms.reviewer: samkemp
ms.author: jburchel
author: jonburchel
reviewer: samuel100
ms.custom: build-2025, dev-focus
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand what Microsoft Foundry Local is so that I can use it to build AI applications.
---

# What is Foundry Local?

[!INCLUDE [foundry-local-preview](./includes/foundry-local-preview.md)]

Foundry Local is an on-device AI inference solution that you use to run AI models locally through a CLI, SDK, or REST API.

## Prerequisites

- Install Foundry Local. Follow [Get started with Foundry Local](get-started.md).
- Use a terminal (for example, Windows Terminal or macOS Terminal).
- Have an internet connection for first-time model downloads.
- If you use Foundry Local only on your device, you don't need an Azure subscription and there are no Azure RBAC role requirements.

## Try it (CLI)

Run these commands to verify your installation and run a model locally.

```bash
foundry --help
foundry model list
foundry model run qwen2.5-0.5b
foundry chat-completion --model gpt-4 --promptMessage "Hello, how can I assist you today?" --maxTokens 100
foundry download-model --uri https://example.com/model.onnx --outputDirectory ./models --provider azure
foundry download-model-catalog --modelName qwen2.5-0.5b --outputDirectory ./catalog --provider azure
```

- `foundry --help` prints the available CLI commands.
- `foundry model list` lists available models. The first run might download execution providers for your hardware.
- `foundry model run qwen2.5-0.5b` downloads the model (first run) and starts an interactive prompt in your terminal.
- `foundry chat-completion` generates streaming chat completions using OpenAI's Chat API. Specify the model, prompt message, optional image file path, and maximum tokens for the response.
- `foundry download-model` downloads a model from a specified URI to the output directory. Options include revision, path, token, buffer size, and provider.
- `foundry download-model-catalog` downloads a model from a catalog using the model name and output directory. Options include buffer size and provider.

Reference: [Foundry Local CLI reference](reference/reference-cli.md)

## Key features

 - **On-device inference**: Run models locally to reduce costs and help keep data on your device.

- **Model customization**: Select a preset model or use your own to meet specific needs.

- **Cost efficiency**: Use existing hardware to eliminate recurring cloud costs and make AI more accessible.

- **Seamless integration**: Integrate with your apps through the SDK, API endpoints, or CLI. For multi-user or high-throughput workloads, move to [Microsoft Foundry](../index.yml).

## Use cases

Foundry Local is ideal when you need to:

- Keep sensitive data on your device
- Operate in limited or offline environments
- Reduce cloud inference costs
- Get low latency AI responses for real-time applications
- Experiment with AI models before you deploy to the cloud

## Frequently asked questions

### Does Foundry Local send my prompts or outputs to Microsoft?

Foundry Local is designed to run inference on your device. When you send prompts to a local Foundry Local endpoint (for example, `http://localhost:PORT`), your prompts and model outputs are processed locally.

Foundry Local can still use the network for operations like:

- **Model and component downloads**: The first time you run a model, Foundry Local downloads the model files. It might also download execution providers for your hardware.
- **Optional diagnostics you choose to share**: If you report a problem, you might choose to share logs (for example, by using `foundry zip-logs`).

Your use of Foundry Local is governed by the product terms and licenses that apply to the software and the models you run. If the terms allow Microsoft to collect diagnostic information, the details are described in those terms and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).

### Do I need an Azure subscription?

No. Foundry Local runs on your hardware, letting you run supported models locally without requiring an Azure subscription.

### Do I need special drivers for NPU acceleration?

Install the driver for your NPU hardware:

- Intel NPU: Install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable NPU acceleration on Windows.

- Qualcomm NPU: Install the [Qualcomm NPU driver](https://softwarecenter.qualcomm.com/catalog/item/QHND) to enable NPU acceleration. If you see the error `Qnn error code 5005: Failed to load from EpContext model. qnn_backend_manager.`, it likely indicates an outdated driver or an NPU resource conflict. Reboot to clear the conflict, especially after using Windows Copilot+ features.

After you install the drivers, Foundry Local automatically detects and uses the NPU.

## Get started

Follow the [Get started with Foundry Local](get-started.md) guide to set up Foundry Local, discover models, and run your first local AI model.

## Related content

- [Get started with Foundry Local](get-started.md)
- [Foundry Local CLI reference](reference/reference-cli.md)
- [Foundry Local REST API reference](reference/reference-rest.md)
- [Foundry Local SDK reference](reference/reference-sdk.md)
- [Compile Hugging Face models for Foundry Local](how-to/how-to-compile-hugging-face-models.md)
- [Foundry Local best practices and troubleshooting](reference/reference-best-practice.md)