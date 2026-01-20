---
title: Managed online endpoints VM SKU list
titleSuffix: Azure Machine Learning
description: Lists the VM SKUs that can be used for managed online endpoints in Azure Machine Learning.
author: s-polly
ms.author: scottpolly
ms.reviewer: sehan
ms.date: 10/18/2025
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: overview
ms.custom:
  - devplatv2
  - build-2025
---

# Managed online endpoints SKU list

The following table shows the virtual machine (VM) stock keeping units (SKUs) that are supported for Azure Machine Learning managed online endpoints. Each SKU is a unique alphanumeric code assigned to a particular VM that can be purchased.

* The full SKU names listed in the table can be used for Azure CLI or Azure Resource Manager templates (ARM templates) requests to create and update deployments.

* For more information on configuration details such as CPU and RAM, see [Azure Machine Learning Pricing](https://azure.microsoft.com/pricing/details/machine-learning/) and [VM sizes](/azure/virtual-machines/sizes).

| Family Name | VM Size Name | Supports Infiniband | Architecture |  numberOfGPUs  |  numberOfCores  | Skip 20% Reservation |
| --- | --- | --- | --- | --- | --- | --- |
|  standardDASv4Family  | STANDARD_D2AS_V4 | - | Cpu | 0 | 2 | - |
|  standardDASv4Family  | STANDARD_D4AS_V4 | - | Cpu | 0 | 4 | - |
|  standardDASv4Family  | STANDARD_D8AS_V4 | - | Cpu | 0 | 8 | - |
|  standardDASv4Family  | STANDARD_D16AS_V4 | - | Cpu | 0 | 16 | - |
|  standardDASv4Family  | STANDARD_D32AS_V4 | - | Cpu | 0 | 32 | - |
|  standardDASv4Family  | STANDARD_D48AS_V4 | - | Cpu | 0 | 48 | - |
|  standardDASv4Family  | STANDARD_D64AS_V4 | - | Cpu | 0 | 64 | - |
|  standardDASv4Family  | STANDARD_D96AS_V4 | - | Cpu | 0 | 96 | - |
|  standardDAv4Family  | STANDARD_D2A_V4 | - | Cpu | 0 | 2 | - |
|  standardDAv4Family  | STANDARD_D4A_V4 | - | Cpu | 0 | 4 | - |
|  standardDAv4Family  | STANDARD_D8A_V4 | - | Cpu | 0 | 8 | - |
|  standardDAv4Family  | STANDARD_D16A_V4 | - | Cpu | 0 | 16 | - |
|  standardDAv4Family  | STANDARD_D32A_V4 | - | Cpu | 0 | 32 | - |
|  standardDAv4Family  | STANDARD_D48A_V4 | - | Cpu | 0 | 48 | - |
|  standardDAv4Family  | STANDARD_D64A_V4 | - | Cpu | 0 | 64 | - |
|  standardDAv4Family  | STANDARD_D96A_V4 | - | Cpu | 0 | 96 | - |
|  standardDSv2Family  | STANDARD_DS1_V2 | - | Cpu | 0 | 1 | - |
|  standardDSv2Family  | STANDARD_DS2_V2 | - | Cpu | 0 | 2 | - |
|  standardDSv2Family  | STANDARD_DS3_V2 | - | Cpu | 0 | 4 | - |
|  standardDSv2Family  | STANDARD_DS4_V2 | - | Cpu | 0 | 8 | - |
|  standardDSv2Family  | STANDARD_DS5_V2 | - | Cpu | 0 | 16 | - |
|  standardESv3Family  | STANDARD_E2S_V3 | - | Cpu | 0 | 2 | - |
|  standardESv3Family  | STANDARD_E4S_V3 | - | Cpu | 0 | 4 | - |
|  standardESv3Family  | STANDARD_E8S_V3 | - | Cpu | 0 | 8 | - |
|  standardESv3Family  | STANDARD_E16S_V3 | - | Cpu | 0 | 16 | - |
|  standardESv3Family  | STANDARD_E32S_V3 | - | Cpu | 0 | 32 | - |
|  standardESv3Family  | STANDARD_E48S_V3 | - | Cpu | 0 | 48 | - |
|  standardESv3Family  | STANDARD_E64S_V3 | - | Cpu | 0 | 64 | - |
|  standardFSv2Family  | STANDARD_F2S_V2 | - | Cpu | 0 | 2 | - |
|  standardFSv2Family  | STANDARD_F4S_V2 | - | Cpu | 0 | 4 | - |
|  standardFSv2Family  | STANDARD_F8S_V2 | - | Cpu | 0 | 8 | - |
|  standardFSv2Family  | STANDARD_F16S_V2 | - | Cpu | 0 | 16 | - |
|  standardFSv2Family  | STANDARD_F32S_V2 | - | Cpu | 0 | 32 | - |
|  standardFSv2Family  | STANDARD_F48S_V2 | - | Cpu | 0 | 48 | - |
|  standardFSv2Family  | STANDARD_F64S_V2 | - | Cpu | 0 | 64 | - |
|  standardFSv2Family  | STANDARD_F72S_V2 | - | Cpu | 0 | 72 | - |
|  standardFXMDVSFamily  | STANDARD_FX4MDS | - | Cpu | 0 | 4 | - |
|  standardFXMDVSFamily  | STANDARD_FX12MDS | - | Cpu | 0 | 12 | - |
|  standardFXMDVSFamily  | STANDARD_FX24MDS | - | Cpu | 0 | 24 | - |
|  standardFXMDVSFamily  | STANDARD_FX36MDS | - | Cpu | 0 | 36 | - |
|  standardFXMDVSFamily  | STANDARD_FX48MDS | - | Cpu | 0 | 48 | - |
|  standardLASv3Family  | STANDARD_L8AS_V3 | - | Cpu | 0 | 8 | - |
|  standardLASv3Family  | STANDARD_L16AS_V3 | - | Cpu | 0 | 16 | - |
|  standardLASv3Family  | STANDARD_L32AS_V3 | - | Cpu | 0 | 32 | - |
|  standardLASv3Family  | STANDARD_L48AS_V3 | - | Cpu | 0 | 48 | - |
|  standardLASv3Family  | STANDARD_L64AS_V3 | - | Cpu | 0 | 64 | - |
|  standardLASv3Family  | STANDARD_L80AS_V3 | - | Cpu | 0 | 80 | - |
|  standardLSv2Family  | STANDARD_L8S_V2 | - | Cpu | 0 | 8 | - |
|  standardLSv2Family  | STANDARD_L16S_V2 | - | Cpu | 0 | 16 | - |
|  standardLSv2Family  | STANDARD_L32S_V2 | - | Cpu | 0 | 32 | - |
|  standardLSv2Family  | STANDARD_L48S_V2 | - | Cpu | 0 | 48 | - |
|  standardLSv2Family  | STANDARD_L64S_V2 | - | Cpu | 0 | 64 | - |
|  standardLSv2Family  | STANDARD_L80S_V2 | - | Cpu | 0 | 80 | - |
|  standardLSv3Family  | STANDARD_L8S_V3 | - | Cpu | 0 | 8 | - |
|  standardLSv3Family  | STANDARD_L16S_V3 | - | Cpu | 0 | 16 | - |
|  standardLSv3Family  | STANDARD_L32S_V3 | - | Cpu | 0 | 32 | - |
|  standardLSv3Family  | STANDARD_L48S_V3 | - | Cpu | 0 | 48 | - |
|  standardLSv3Family  | STANDARD_L64S_V3 | - | Cpu | 0 | 64 | - |
|  standardLSv3Family  | STANDARD_L80S_V3 | - | Cpu | 0 | 80 | - |
|  standardNCADSA100v4Family  | STANDARD_NC24ADS_A100_V4 | - | NvidiaGpu | 1 | 24 | Yes |
|  standardNCADSA100v4Family  | STANDARD_NC48ADS_A100_V4 | - | NvidiaGpu | 2 | 48 | Yes |
|  standardNCADSA100v4Family  | STANDARD_NC96ADS_A100_V4 | - | NvidiaGpu | 4 | 96 | Yes |
|  standard NCASv3_T4 Family  | STANDARD_NC4AS_T4_V3 | - | NvidiaGpu | 1 | 4 | - |
|  standard NCASv3_T4 Family  | STANDARD_NC8AS_T4_V3 | - | NvidiaGpu | 1 | 8 | - |
|  standard NCASv3_T4 Family  | STANDARD_NC16AS_T4_V3 | - | NvidiaGpu | 1 | 16 | - |
|  standard NCASv3_T4 Family  | STANDARD_NC64AS_T4_V3 | - | NvidiaGpu | 4 | 64 | - |
|  standardNCSv2Family  | STANDARD_NC6S_V2 | - | NvidiaGpu | 1 | 6 | - |
|  standardNCSv2Family  | STANDARD_NC12S_V2 | - | NvidiaGpu | 2 | 12 | - |
|  standardNCSv2Family  | STANDARD_NC24S_V2 | - | NvidiaGpu | 4 | 24 | - |
|  standardNCSv3Family  | STANDARD_NC6S_V3 | - | NvidiaGpu | 1 | 6 | - |
|  standardNCSv3Family  | STANDARD_NC12S_V3 | - | NvidiaGpu | 2 | 12 | - |
|  standardNCSv3Family  | STANDARD_NC24S_V3 | - | NvidiaGpu | 4 | 24 | - |
|  standardNCADSH100v5Family  | STANDARD_NC40ADS_H100_V5 | - | NvidiaGpu | 1 | 40 | Yes |
|  standardNCADSH100v5Family  | STANDARD_NC80ADIS_H100_V5 | - | NvidiaGpu | 2 | 80 | Yes |
|  standard NDAMSv4_A100Family  | STANDARD_ND96AMSR_A100_V4 | Yes | NvidiaGpu | 8 | 96 | Yes |
|  standard NDASv4_A100 Family  | STANDARD_ND96ASR_V4 | Yes | NvidiaGpu | 8 | 96 | Yes |
|  standardNDSv2Family  | STANDARD_ND40RS_V2 | Yes | NvidiaGpu | 8 | 40 | Yes |
|  standardNDv5H100Family  | STANDARD_ND96IS_H100_V5 | - | NvidiaGpu | 8 | 96 | Yes |
|  standardNDv5H100Family  | STANDARD_ND96ISR_H100_V5 | Yes | NvidiaGpu | 8 | 96 | Yes |
|  standardNVADSA10v5Family | STANDARD_NV6ADS_A10_V5     | - | NvidiaGpu | 1/6 | 6  | - |
|  standardNVADSA10v5Family | STANDARD_NV12ADS_A10_V5  | - | NvidiaGpu | 1/3 | 12 | - |
|  standardNVADSA10v5Family | STANDARD_NV18ADS_A10_V5  | - | NvidiaGpu | 1/2 | 18 | - |
|  standardNVADSA10v5Family | STANDARD_NV36ADS_A10_V5  | - | NvidiaGpu | 1   | 36 | - |
|  standardNVADSA10v5Family | STANDARD_NV36ADMS_A10_V5 | - | NvidiaGpu | 1   | 36 | - |
|  standardNVADSA10v5Family | STANDARD_NV72ADS_A10_V5  | - | NvidiaGpu | 2   | 72 | - |

> [!CAUTION]
> Small VM SKUs such as `Standard_DS1_v2` and `Standard_F2s_v2` may be too small for bigger models and may lead to container termination due to insufficient memory, not enough space on the disk, or probe failure as it takes too long to initiate the container. If you face [OutOfQuota errors](how-to-troubleshoot-online-endpoints.md?tabs=cli#error-outofquota) or [ResourceNotReady errors](how-to-troubleshoot-online-endpoints.md?tabs=cli#error-resourcenotready), try bigger VM SKUs. If you want to reduce the cost of deploying multiple models with managed online endpoint, see [Deployment for several local models](concept-online-deployment-model-specification.md#deployment-for-several-local-models).

> [!NOTE]
> We recommend having more than 3 instances for deployments in production scenarios. In addition, Azure Machine Learning reserves 20% of your compute resources for performing upgrades on some VM SKUs as described in [Virtual machine quota allocation for deployment](how-to-manage-quotas.md#virtual-machine-quota-allocation-for-deployment). VM SKUs that are exempted from this extra quota reservation are specified in the "Skip 20% Reservation" column.
