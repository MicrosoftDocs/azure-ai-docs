---
title: "Foundry Local architecture"
titleSuffix: Foundry Local
description: "Learn how Foundry Local embeds AI inference directly inside your application as a native library."
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.topic: concept-article
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.date: 01/05/2026
ai-usage: ai-assisted
---

# Foundry Local architecture

Foundry Local is an embedded AI runtime that ships as a single native library inside your application. Rather than connecting to a separate service or daemon, your code loads the Foundry Local Core API in-process and calls it through language-specific SDKs for C#, JavaScript, Python, and Rust. The result is a self-contained application that runs small language models on local hardware with no external dependencies.

This article explains the components that make up the Foundry Local runtime and how they work together to deliver on-device AI inference.

## Architecture overview

The following diagram shows how Foundry Local fits inside your application. Your code interacts with the Core API through direct function calls. The Core API in turn delegates to ONNX Runtime for inference, Foundry Catalog for model acquisition, and WinML (on Windows) for execution provider registration.

:::image type="content" source="../media/architecture/new-sdk-architecture.png" alt-text="Diagram showing application code calling the Foundry Local Core API, which delegates to ONNX Runtime, Foundry Catalog, and WinML.":::

Because the entire runtime is embedded, your application packages everything it needs. End users receive a single distributable with no separate installer or background service to manage.

## Foundry Local Core API

The Foundry Local Core API is the central component of the runtime. It's a platform-specific native library — `.dll` on Windows, `.so` on Linux, and `.dylib` on macOS — that your application loads in-process.

The Core API handles:

- **Model lifecycle management** — downloading, loading, running inference, and unloading models through a single interface.
- **Hardware abstraction** — detecting available hardware, selecting the best execution provider, and managing the local model cache, so your application code doesn't need to handle these details.
- **Thread-safe, session-based inference** — supporting concurrent requests from multiple threads without requiring external synchronization.

Language SDKs for C#, JavaScript, Python, and Rust wrap this native library and expose idiomatic APIs for each ecosystem. Your application code calls the SDK, which makes direct in-process function calls to the Core API.

## ONNX Runtime

ONNX Runtime is the inference engine that executes AI models. The Core API calls into ONNX Runtime for all model execution.

ONNX Runtime provides:

- **Graph partitioning and optimization** — analyzing model graphs and applying optimizations before execution.
- **Plugin execution providers** — loading hardware-specific acceleration plugins at runtime to target GPUs, NPUs, or other accelerators.
- **Cross-hardware execution** — running models across the best available hardware while managing memory and data transfer between execution providers.
- **CPU fallback** — the CPU execution provider is always available, so models run on any device even without specialized hardware.

ONNX Runtime supports quantized models, which reduce memory usage and improve inference speed on resource-constrained devices.

## Foundry Catalog

The Foundry Catalog is a cloud-hosted model registry that the Core API integrates with for model acquisition.

The catalog provides:

- **Hardware-optimized model variants** — pre-compiled ONNX models tuned for specific hardware configurations (CPU, GPU, NPU).
- **Download on first use** — models are pulled from the catalog the first time your application requests them, then cached locally for subsequent runs.
- **Local caching** — downloaded models are stored on disk, so they're available immediately without re-downloading.
- **Version-aware updates** — the catalog tracks model versions and pulls updates when newer versions are available.

> [!NOTE]
> Foundry Local uses the network to download models and execution providers from the catalog. After the initial download, models run entirely offline from the local cache.

You aren't limited to models in the Foundry Catalog. You can also compile and optimize your own models in the ONNX format. For details, see [Compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md).

## WinML (Windows only)

On Windows, Foundry Local integrates with WinML for execution provider registration. WinML is a Windows-native machine learning platform that bridges the gap between ONNX Runtime and the hardware acceleration plugins available on the system.

WinML handles:

- **EP plugin acquisition** — sourcing hardware-matched execution provider plugins from the OS and Windows Update.
- **Runtime registration** — registering acquired execution providers with ONNX Runtime so they're available during inference.
- **Driver compatibility** — negotiating driver versions and handling compatibility checks to ensure stable execution.

On Linux and macOS, execution provider registration follows a different path that doesn't involve WinML.

## Optional REST API

For scenarios that require HTTP-based communication, the Foundry Local SDK can start an optional OpenAI-compatible REST endpoint within your application process. This is useful for integrating with tools that communicate over HTTP, such as LangChain or Open WebUI.

The REST API isn't required for native SDK usage. When you call the SDK directly, your application makes in-process function calls with no HTTP overhead.

## Hardware abstraction

Foundry Local abstracts the underlying hardware so your application code doesn't need to detect devices or select execution providers. The Core API automatically identifies available hardware and chooses the best execution provider for each model.

Supported execution providers include NVIDIA CUDA, AMD, Qualcomm, and Intel. Supported device types include CPU, GPU, and NPU.

> [!NOTE]
> For Intel NPU support on Windows, install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable hardware acceleration.

> [!NOTE]
> For Qualcomm NPU support, install the [Qualcomm NPU driver](https://softwarecenter.qualcomm.com/catalog/item/QHND). If you encounter the error `Qnn error code 5005: "Failed to load from EpContext model. qnn_backend_manager."`, this error typically indicates an outdated driver or NPU resource conflicts. Try rebooting to clear NPU resource conflicts, especially after using Windows Copilot+ features.

## Model lifecycle

The Foundry Local SDK manages the complete model lifecycle through the Core API. Each phase happens in-process within your application:

- **Download** — the SDK requests a model by alias. If the model isn't in the local cache, the Core API downloads it from the Foundry Catalog and stores it on disk.
- **Load** — the SDK loads the model into memory, which initializes the ONNX Runtime session and selects the appropriate execution provider for the available hardware.
- **Inference** — your application sends prompts to the loaded model and receives responses. The Core API supports both synchronous and streaming inference modes.
- **Unload** — when inference is complete, the SDK unloads the model from memory to free up resources. Cached model files remain on disk for future use.

This lifecycle is the same across all supported languages. The SDK handles each phase through a consistent API pattern: get a model from the catalog, download and load it, create a client, and run inference.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
- [Use native chat completions API](../how-to/how-to-use-native-chat-completions.md)
