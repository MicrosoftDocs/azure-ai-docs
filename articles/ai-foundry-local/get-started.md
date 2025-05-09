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

- A PC with these minimum specifications:
  - Windows 10 or later
  - At least 8GB RAM
  - At least 3GB of free disk space for model caching (quantized Phi 3.2 models require about 3GB)
- Recommended hardware for optimal performance:
  - Windows 11
  - NVIDIA GPU (2000 series or newer), AMD GPU (6000 series or newer), or Qualcomm Snapdragon X Elite, with 8GB or more of VRAM
  - At least 16GB RAM
  - At least 15GB of free disk space for model caching (larger models require up to 15GB)
- Administrator access to install software

## Quickstart in 2 steps

Get started with Foundry Local quickly:

1. **Install Foundry Local**

   1. Download Foundry Local for your platform (Windows, macOS, Linux - x64/ARM) from the repository's releases page.
   2. Install the package by following the on-screen prompts.


      > [!IMPORTANT]
      > **For macOS/Linux users:** Run both components in separate terminals:
      > - Neutron Server (`Inference.Service.Agent`) - Make it executable with `chmod +x Inference.Service.Agent`
      > - Foundry Client (`foundry`) - Make it executable with `chmod +x foundry` and add it to your PATH

   3. After installation, access the tool through the command line with `foundry`.

2. **Run your first model**
   1. Open a command prompt or terminal window.
   2. Run the DeepSeek-R1 model on the CPU with this command:
      ```bash
      foundry model run deepseek-r1-1.5b-cpu
      ```

> [!TIP]
> The `foundry model run <model>` command automatically downloads the model if it isn't already in your local cache, then starts an interactive chat session. Try different models by replacing `deepseek-r1-1.5b-cpu` with any model name from the catalog. View all available models with the `foundry model list` command.

## Explore Foundry Local CLI commands

The Foundry CLI organizes commands into these main categories:

- **Model**: Commands for managing and running models
- **Service**: Commands for managing the Foundry Local service
- **Cache**: Commands for managing the local model cache

View all available commands with:

```bash
foundry --help
```

> [!TIP]
> For a complete guide to all CLI commands and their usage, see the [Foundry Local CLI Reference](reference/reference-cli.md).

## Security and privacy considerations

Foundry Local prioritizes your privacy and security:

- **Local processing**: All data stays on your device and is never sent to Microsoft or external services.
- **No telemetry**: Foundry Local doesn't collect usage data or model inputs.
- **Air-gapped environments**: After initial model download, you can use Foundry Local in offline environments.

### Security best practices

- Use Foundry Local in environments that comply with your organization's security policies.
- When handling sensitive data, ensure your device meets your organization's security requirements.
- Use disk encryption on devices where cached models might contain sensitive fine-tuning data.

### Licensing considerations

Models in Foundry Local follow their original licenses:

- Open-source models keep their original licenses (such as Apache 2.0 or MIT).
- Commercial models may have specific usage restrictions or need separate licensing.
- Always check licensing information for each model before using in production.

## Production deployment scope

Foundry Local works best for:

- Individual developer workstations
- Single-node deployments
- Local application development and testing

> [!IMPORTANT]
> Foundry Local is not designed for distributed, containerized, or multi-machine production deployments. For production-scale needs, use Azure AI Foundry for enterprise-grade availability and scale.

## Troubleshooting

### Common issues and solutions

| Issue | Possible Cause | Solution |
| --- | --- | --- |
| Slow inference | CPU-only model with large parameter count | Use GPU-optimized model variants when available |
| Model download failures | Network connectivity issues | Check your internet connection and run `foundry cache list` to verify cache status |
| Service won't start | Port conflicts or permission issues | Try `foundry service restart` or report an issue with logs using `foundry zip-logs` |

### Improving performance

If you experience slow inference:

1. Use GPU acceleration when available
2. Monitor memory usage during inference to identify bottlenecks
3. Try more quantized model variants (like INT8 instead of FP16)
4. Adjust batch sizes for non-interactive workloads

## Next steps

- [Learn how to integrate Foundry Local with your applications](how-to/integrate-with-inference-sdks.md)
- [Explore the Foundry Local documentation](index.yml)
