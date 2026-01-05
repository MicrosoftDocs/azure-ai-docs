---
title: Best practices and troubleshooting guide for Foundry Local
titleSuffix: Foundry Local
description: Guidance on best practices and troubleshooting for Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: troubleshooting
ms.date: 01/05/2026
ms.author: jburchel
author: jonburchel
reviewer: maanavdalal
ms.reviewer: maanavd
ai-usage: ai-assisted
---

# Best practices and troubleshooting guide for Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]
This article lists best practices and troubleshooting tips for Foundry Local.

## Security best practices

- Run Foundry Local only in environments that comply with your organization's security policies.
- Make sure your device meets your organization's security requirements when you handle sensitive data.
- Encrypt disks on devices that cache models containing sensitive fine-tuning data.

## Licensing considerations

Review the licensing implications for the models you run in Foundry Local. View the full model license terms for each model in the catalog by running the following command. In the following command, replace the placeholder *`<model>`* with the model name:

```bash
foundry model info <model> --license
```

## Production deployment scope

Foundry Local is for on-device inference, not distributed, containerized, or multi-machine production deployments.

## Troubleshooting

### Common issues and solutions

| Issue                                                                                                                                                    | Possible Cause                                                                                                  | Solution                                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Slow inference                                                                                                                                           | CPU only model with a large parameter count.                                                                       | Use GPU optimized model variants when it's available.                                                                                                                                                                                                                                             |
| Model download failures                                                                                                                                  | Network connectivity issues.                                                                                     | Check your internet connection, and run `foundry cache list` to verify cache status.                                                                                                                                                                                                          |
| Service connection errors (`Request to local service failed. Uri:http://127.0.0.1:0/foundry/list`)                                                       | Port binding issues or the service isn't accessible.                                                          | Run `foundry service restart` to restart the service and resolve port binding problems.                                                                                                                                                                                                      |
| Service fails to start.                                                                                                                               | Port conflicts or permission issues.                                                                             | Run `foundry service restart`, or [report an issue](https://github.com/microsoft/Foundry-Local/issues) with logs using `foundry zip-logs`.                                                                                                                                                    |
| Intel NPU not detected or not working                                                                                                                    | Missing or outdated Intel NPU driver.                                                                            | Install the [Intel NPU driver for Windows](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable NPU acceleration.                                                                                                                                |
| Qualcomm NPU error (`Qnn error code 5005: "Failed to load from EpContext model. qnn_backend_manager."`)                                                  | Outdated Qualcomm NPU driver or NPU resource conflicts.                                                          | Install the [Qualcomm NPU driver](https://softwarecenter.qualcomm.com/catalog/item/QHND). If the issue persists, reboot to clear NPU resource conflicts, especially after using Windows Copilot+ features.                                                                            |
| `winget install Microsoft.FoundryLocal --scope machine` fails with “The current system configuration doesn't support the installation of this package.” | Winget blocks MSIX machine scope installs because of an OS bug when using provisioning APIs from a packaged context. | Use `Add-AppxProvisionedPackage` instead. Download the `.msix` and its dependency, then run in **elevated** PowerShell: `Add-AppxProvisionedPackage -Online -PackagePath .\FoundryLocal.msix -DependencyPackagePath .\VcLibs.appx -SkipLicense`. This command installs Foundry Local for all users. |

### Improving performance

If you experience slow inference, consider the following strategies:

- Running ONNX models from the AI Toolkit for VS Code at the same time causes resource contention. Stop the AI Toolkit inference session before you run Foundry Local.
- Use GPU acceleration when it's available.
- Identify bottlenecks by monitoring memory usage during inference.
- Try more quantized model variants (like INT8 instead of FP16).
- Adjust batch sizes for noninteractive workloads.
