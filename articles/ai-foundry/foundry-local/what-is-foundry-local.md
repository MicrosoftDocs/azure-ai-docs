---
title: What is Foundry Local?
titleSuffix: Foundry Local
description: Foundry Local is a trusted platform that empowers developers to drive innovation and shape the future with AI in a safe, secure, and responsible way on their devices.
keywords: Foundry Tools, cognitive
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: overview
ms.date: 10/01/2025
ms.reviewer: samkemp
ms.author: jburchel
author: jonburchel
reviewer: samuel100
ms.custom: build-2025
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand what Microsoft Foundry Local is so that I can use it to build AI applications.
---

# What is Foundry Local?

[!INCLUDE [foundry-local-preview](./includes/foundry-local-preview.md)]

Foundry Local is an on-device AI inference solution that provides performance, privacy, customization, and cost benefits. It integrates with your workflows and applications through a CLI, SDK, and REST API.

## Key features

- **On-Device inference**: Run models locally to reduce costs and keep data on your device.

- **Model customization**: Select a preset model or use your own to meet specific needs.

- **Cost efficiency**: Use existing hardware to eliminate recurring cloud costs and make AI more accessible.

- **Seamless integration**: Integrate with your apps through the SDK, API endpoints, or CLI, and scale to Microsoft Foundry as your needs grow.

## Use cases

Foundry Local is ideal when you need to:

- Keep sensitive data on your device
- Operate in limited or offline environments
- Reduce cloud inference costs
- Get low latency AI responses for real-time applications
- Experiment with AI models before you deploy to the cloud

## Do I need an Azure subscription?

No. Foundry Local runs on your hardware, letting you use your existing infrastructure without cloud services.

## Frequently asked questions

### Do I need special drivers for NPU acceleration?

Install the driver for your NPU hardware:

- Intel NPU: Install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable NPU acceleration on Windows.

- Qualcomm NPU: Install the [Qualcomm NPU driver](https://softwarecenter.qualcomm.com/catalog/item/QHND) to enable NPU acceleration. If you see the error `Qnn error code 5005: Failed to load from EpContext model. qnn_backend_manager.`, it likely indicates an outdated driver or an NPU resource conflict. Reboot to clear the conflict, especially after using Windows Copilot+ features.

After you install the drivers, Foundry Local automatically detects and uses the NPU.

## Get started

Follow the [Get started with Foundry Local](get-started.md) guide to set up Foundry Local, discover models, and run your first local AI model.

## Related content

- [Get started with Foundry Local](get-started.md)
- [Compile Hugging Face models for Foundry Local](how-to/how-to-compile-hugging-face-models.md)
