---
title: Foundry Local execution providers
titleSuffix: Foundry Local
description: Guidance on execution providers (hardware accelerators) used by Foundry Local
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: reference
ms.date: 11/07/2025
ms.author: nakersha
author: natke
reviewer: metang
ms.reviewer: metang
ai-usage: ai-assisted
---

# Foundry Local execution providers

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Execution providers are hardware-specific acceleration libraries that run models as efficiently as possible on device.

## Built-in execution providers

Foundry Local includes the CPU execution provider and the WebGPU execution provider. 

The CPU execution providers uses [Microsoft Linear Algebra Subroutines (MLAS)](https://github.com/microsoft/mlas) to run on any CPU and is the CPU fallback for Foundry Local.

The WebGPU execution provider uses [Dawn](https://github.com/google/dawn), the native implementation of the web-based API, for acceleration on any GPU, and is the GPU fallback for Foundry Local.


## Plugin execution providers

The execution providers listed in the table are available (depending on device and driver compatibility) for dynamic download and registration on Windows and are subject to the license terms specified.

| Name (Vendor) | Requirements | License Terms |
|---------------|--------------|---------------|
| "CUDAExecutionProvider" (Nvidia) | NVIDIA GeForce RTX 30XX and above with minimum recommended driver version 32.0.15.5585 + Cuda version 12.5 | [License Agreement for NVIDIA Software Development Kits—EULA](https://docs.nvidia.com/cuda/eula/index.html) | 
| "NvTensorRtRtxExecutionProvider" (Nvidia) | NVIDIA GeForce RTX 30XX and above with minimum recommended driver version 32.0.15.5585 + Cuda version 12.5 | [License Agreement for NVIDIA Software Development Kits—EULA](https://docs.nvidia.com/cuda/eula/index.html) |
| "OpenVINOExecutionProvider" (Intel) | CPU: Intel TigerLake (11th Gen) and later with min recommended driver 32.0.100.9565<br>GPU: Intel AlderLake (12th Gen) and later with min recommended driver 32.0.101.1029<br>NPU: Intel ArrowLake (15th Gen) and above with min recommended driver 32.0.100.4239 | [Intel OBL Distribution Commercial Use License Agreement v2025.02.12](https://cdrdv2.intel.com/v1/dl/getContent/849090?explicitVersion=true) |
| "QNNExecutionProvider" (Qualcomm) | Snapdragon(R) X Elite - X1Exxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and above<br>Snapdragon(R) X Plus - X1Pxxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and above | To view the QNN License, download the Qualcomm® Neural Processing SDK, extract the ZIP, and open the LICENSE.pdf file. |
| "VitisAIExecutionProvider" (AMD) | Min: Adrenalin Edition 25.6.3 with NPU driver 32.00.0203.280<br>Max: Adrenalin Edition 25.9.1 with NPU driver 32.00.0203.297 | No additional license required |


