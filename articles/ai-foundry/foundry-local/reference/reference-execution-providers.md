---
title: Foundry Local execution providers
titleSuffix: Foundry Local
description: Guidance on execution providers (hardware accelerators) used by Foundry Local
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: reference
ms.date: 11/07/2025
ms.author: nakersha
author: nakersha
reviewer: metang
ms.reviewer: metang
ai-usage: ai-assisted
---

# Foundry Local licenses

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]
This article shows licenses for Foundry Local.

## Built-in execution providers

Foundry Local includes the CPU execution provider and the WebGPU execution provider.


## Downloadable execution providers

The execution providers listed below are available (depending on device and driver compatibility) for dynamic download and registration on Windows and are subject to the license terms below.

| Name (Vendor) | Requirements | License Terms |
|---------------|--------------|---------------|
| "CUDAExecutionProvider" (Nvidia) | NVIDIA GeForce RTX 30XX and above with minimum recommended driver version 32.0.15.5585 + Cuda version 12.5 | [License Agreement for NVIDIA Software Development Kits — EULA](https://docs.nvidia.com/cuda/eula/index.html) | 
| "NvTensorRtRtxExecutionProvider" (Nvidia) | NVIDIA GeForce RTX 30XX and above with minimum recommended driver version 32.0.15.5585 + Cuda version 12.5 | [License Agreement for NVIDIA Software Development Kits — EULA](eula-12Aug2025.pdf) |
| "OpenVINOExecutionProvider" (Intel) | CPU: Intel TigerLake (11th Gen) and above with min recommended driver 32.0.100.9565<br>GPU: Intel AlderLake (12th Gen) and above with min recommended driver 32.0.101.1029<br>NPU: Intel ArrowLake (15th Gen) and above with min recommended driver 32.0.100.4239 | [Intel OBL Distribution Commercial Use License Agreement v2025.02.12](https://cdrdv2.intel.com/v1/dl/getContent/849090?explicitVersion=true) |
| "QNNExecutionProvider" (Qualcomm) | Snapdragon(R) X Elite - X1Exxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and above<br>Snapdragon(R) X Plus - X1Pxxxxx - Qualcomm(R) Hexagon(TM) NPU with minimum driver version 30.0.140.0 and above | To view the QNN License, download the Qualcomm® Neural Processing SDK, extract the ZIP, and open the LICENSE.pdf file. |
| "VitisAIExecutionProvider" (AMD) | Min: Adrenalin Edition 25.6.3 with NPU driver 32.00.0203.280<br>Max: Adrenalin Edition 25.9.1 with NPU driver 32.00.0203.297 | No additional license required |
