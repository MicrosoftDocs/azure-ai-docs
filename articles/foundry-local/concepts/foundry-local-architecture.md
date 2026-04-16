---
title: "Foundry Local architecture overview"
titleSuffix: Foundry Local
description: "Learn how Foundry Local delivers end-to-end local AI inference directly inside your application as a native library."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: concept-article
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.date: 03/28/2026
ai-usage: ai-assisted
---

# Foundry Local architecture overview

Foundry Local is an end-to-end local AI solution that ships as a single native library inside your application. Rather than connecting to a separate service or daemon, your code loads the Foundry Local Core API in-process and calls it through language-specific software development kits (SDKs) for C#, JavaScript, Python, and Rust. The result is a self-contained application that runs small language models on local hardware with no external dependencies.

This article explains the components that make up the Foundry Local runtime and how they work together to deliver on-device AI inference.

## Component overview

The following diagram shows how Foundry Local fits inside your application. Your code interacts with the Core API through direct function calls. The Core API calls into Open Neural Network Exchange (ONNX) Runtime for inference, integrates with the Foundry Catalog for model acquisition, and integrates with WinML on Windows for execution provider registration.

:::image type="content" source="../media/architecture/new-sdk-architecture.png" alt-text="Diagram showing the Foundry Local architecture. Application code in JavaScript, Python, C#, or Rust calls the Foundry Local Core API through language SDKs or an optional REST endpoint.":::

Because the entire runtime is embedded, your application packages everything it needs. End users receive a single distributable with no separate installer or background service to manage.

## Foundry Local Core API

The Foundry Local Core API is the central component of the runtime. It's a platform-specific native library — `.dll` on Windows, `.so` on Linux, and `.dylib` on macOS — that your application loads in-process.

The Core API handles:

- **Model lifecycle management** — downloading, loading, running inference, and unloading models through a single interface.
- **Hardware abstraction** — detecting available hardware, selecting the best execution provider, and managing the local model cache, so your application code doesn't need to handle these details.
- **Thread-safe, session-based inference** — supporting concurrent requests from multiple threads without requiring external synchronization.

Language SDKs for C#, JavaScript, Python, and Rust wrap this native library and expose idiomatic APIs for each ecosystem:

| Language | Package |
|---|---|
| C# | [Microsoft.AI.Foundry.Local](https://www.nuget.org/packages/Microsoft.AI.Foundry.Local) (NuGet) |
| JavaScript | [foundry-local-sdk](https://www.npmjs.com/package/foundry-local-sdk) (npm) |
| Python | [foundry-local-sdk](https://pypi.org/project/foundry-local-sdk/) (PyPI) |
| Rust | [foundry-local-sdk](https://crates.io/crates/foundry-local-sdk) (crates.io) |

Your application code calls the SDK, which makes direct in-process function calls to the Core API.

## ONNX Runtime

[ONNX Runtime](https://onnxruntime.ai/) is the inference engine that executes AI models. The Core API calls into ONNX Runtime for all model execution.

ONNX Runtime provides:

- **Graph partitioning and optimization** — analyzing model graphs and applying optimizations before execution.
- **Plugin execution providers** — loading hardware-specific acceleration plugins at runtime to target graphics processing units (GPUs), neural processing units (NPUs), or other accelerators.
- **Cross-hardware execution** — running models across the best available hardware while managing memory and data transfer between execution providers.
- **CPU fallback** — the CPU execution provider is always available, so models run on any device even without specialized hardware.

ONNX Runtime supports quantized models, which reduce memory usage and improve inference speed on resource-constrained devices.

### WebGPU and Apple Silicon

On macOS with Apple Silicon, Foundry Local uses the WebGPU execution provider to access the GPU. ONNX Runtime implements WebGPU through [Dawn](https://dawn.googlesource.com/dawn), Google's open-source WebGPU implementation. Dawn acts as a translation layer that compiles WebGPU compute shaders into Metal Shading Language (MSL), which then runs natively on the Apple Silicon GPU through Apple's [Metal](https://developer.apple.com/metal/) framework.

This approach enables GPU-accelerated inference on macOS without requiring a dedicated Metal execution provider. The translation chain is: ONNX model → ONNX Runtime (WebGPU execution provider) → Dawn → Metal → Apple Silicon GPU. Key optimizations include half-precision (FP16) arithmetic for faster throughput, GPU-side tensor management to minimize CPU-to-GPU data transfers, and graph capture for repeated inference passes.

On Windows, the same WebGPU execution provider targets Direct3D through Dawn, which means your application code doesn't need platform-specific logic to benefit from GPU acceleration.

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

On Windows, Foundry Local integrates with [WinML](/windows/ai/windows-ml/) for execution provider registration. WinML is a Windows-native machine learning platform that bridges the gap between ONNX Runtime and the hardware acceleration plugins available on the system.

WinML handles:

- **Execution provider plugin acquisition** — sourcing hardware-matched execution provider plugins from the OS and Windows Update.
- **Runtime registration** — registering acquired execution providers with ONNX Runtime so they're available during inference.
- **Driver compatibility** — negotiating driver versions and handling compatibility checks to ensure stable execution.

On Linux and macOS, the Core API registers execution providers directly with ONNX Runtime without a platform intermediary. The SDK bundles the required execution provider plugins for each target platform, so registration is handled internally during model loading.

## Optional REST API

For scenarios that require HTTP-based communication, the Foundry Local SDK can start an optional OpenAI-compatible REST endpoint within your application process. This is useful for integrating with tools that communicate over HTTP, such as LangChain or Open WebUI.

The REST API isn't required for native SDK usage. When you call the SDK directly, your application makes in-process function calls with no HTTP overhead.

## Hardware abstraction

Foundry Local abstracts the underlying hardware so your application code doesn't need to detect devices or select execution providers. The Core API automatically identifies available hardware and chooses the best execution provider for each model.

The following table summarizes the supported execution providers and device types:

| Execution provider | Device type | Platform |
|---|---|---|
| NVIDIA CUDA | GPU | Windows, Linux |
| WebGPU (via Dawn) | GPU | Windows, Linux, macOS |
| AMD Vitis | NPU | Windows |
| Qualcomm | NPU | Windows |
| Intel OpenVino | GPU | Windows |
| CPU  | CPU | Windows, Linux, macOS |

The CPU execution provider is always available as a fallback. If no GPU or NPU is detected, Foundry Local runs inference on the CPU automatically.


## Model lifecycle

The Foundry Local SDK manages the complete model lifecycle through the Core API. Each phase happens in-process within your application:

- **Download** — the SDK requests a model by alias. If the model isn't in the local cache, the Core API downloads it from the Foundry Catalog and stores it on disk.
- **Load** — the SDK loads the model into memory, which initializes the ONNX Runtime session and selects the appropriate execution provider for the available hardware. For details on how execution providers are selected, see [Hardware abstraction](#hardware-abstraction).
- **Inference** — your application sends prompts to the loaded model and receives responses. The Core API supports both synchronous and streaming inference modes.
- **Unload** — when inference is complete, the SDK unloads the model from memory to free up resources. Cached model files remain on disk for future use.

This lifecycle is the same across all supported languages. The SDK handles each phase through a consistent API pattern: get a model from the catalog, download and load it, create a client, and run inference.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
- [Use native chat completions API](../how-to/how-to-use-native-chat-completions.md)
