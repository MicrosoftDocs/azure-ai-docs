---
title: Best practices and troubleshooting guide for Foundry Local
titleSuffix: Foundry Local
description: Guidance on best practices and troubleshooting for Foundry Local.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: reference
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

# Best practices and troubleshooting guide for Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]
This document provides best practices and troubleshooting tips for Foundry Local.

## Security best practices

- Use Foundry Local in environments that comply with your organization's security policies.
- When handling sensitive data, ensure your device meets your organization's security requirements.
- Use disk encryption on devices where cached models might contain sensitive fine-tuning data.

## Licensing considerations

When using Foundry Local, be aware of the licensing implications for the models you run. You can view full terms of model license for each model in the model catalog using:

```bash
foundry model info <model> --license
```

## Production deployment scope

Foundry Local is designed for on-device inference and *not* distributed, containerized, or multi-machine production deployments.

## Troubleshooting

### Common issues and solutions

| Issue | Possible Cause | Solution |
| --- | --- | --- |
| Slow inference | CPU-only model with large parameter count | Use GPU-optimized model variants when available |
| Model download failures | Network connectivity issues | Check your internet connection and run `foundry cache list` to verify cache status |
| The service fails to start | Port conflicts or permission issues | Try `foundry service restart` or [report an issue](https://github.com/microsoft/Foundry-Local/issues) with logs using `foundry zip-logs` |
| Qualcomm NPU error (`Qnn error code 5005: "Failed to load from EpContext model. qnn_backend_manager."`) | Qualcomm NPU error | |

### Improving performance

If you experience slow inference, consider the following strategies:

- Simultaneously running ONNX models provided in the AI Toolkit for VS Code cause resource contention. Stop the AI Toolkit inference session before running Foundry Local.
- Use GPU acceleration when available
- Identify bottlenecks by monitoring memory usage during inference.
- Try more quantized model variants (like INT8 instead of FP16)
- Adjust batch sizes for non-interactive workloads