---
title: Foundry Local SDK Reference
titleSuffix: Foundry Local
description: Reference guide for the Foundry Local SDK.
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.author: jburchel
author: jonburchel
ms.topic: concept-article
ms.date: 01/05/2026
zone_pivot_groups: foundry-local-sdk
reviewer: maanavdalal
ms.reviewer: maanavd
ai-usage: ai-assisted
---

# Foundry Local SDK reference

The Foundry Local SDK enables you to ship AI features in your applications that are capable of using local AI models through a simple and intuitive API. The SDK abstracts away the complexities of managing AI models and provides a seamless experience for integrating local AI capabilities into your applications. This reference documents SDK implementations for C#, JavaScript, Python, and Rust.

The SDK doesn't require the Foundry Local CLI to be installed on the end users machine, allowing you to ship your applications without extra setup steps for your users - your applications is self-contained. The extra benefits of the Foundry Local SDK include:

- **Hardware detection and optimization**: Automatic capability assessment for GPU, NPU, and CPU.
- **Execution provider management (Windows)**: Automatic download and registration of appropriate ONNX Runtime execution providers (CUDA, Vitis, QNN, OpenVINO, TensorRT) based on device capabilities.
- **Metal support via WebGpu (macOS)**: Native support for running models on Apple Silicon with optimized performance.
- **Model acquisition**: Seamless download from Foundry Model Catalog with versioning, updates, and automatically hardware-optimized model selection with fallback support.
- **Efficient runtime**: Adds approximately 20 MB to app size, runs on devices from mobile phones to desktops.
- **OpenAI API compatibility**: Easy integration with OpenAI models and tools.
- **Optional REST server**: Run Foundry Local as a local service accessible by other applications.

<!-- markdownlint-disable MD044 -->

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/sdk-current-reference/csharp.md)]
::: zone-end
::: zone pivot="programming-language-JavaScript"
[!INCLUDE [JavaScript](../includes/sdk-current-reference/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/sdk-current-reference/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/sdk-current-reference/rust.md)]
::: zone-end

<!-- markdownlint-enable MD044 -->