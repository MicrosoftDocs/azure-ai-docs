---
title: "What is Foundry Local?"
titleSuffix: Foundry Local
description: "Foundry Local is an embeddable, end-to-end AI runtime that handles model acquisition, hardware acceleration, and inference — all shipped inside your app."
keywords: Foundry Local, on-device AI, local inference
ms.service: azure-ai-foundry
ms.topic: overview
ms.date: 03/27/2026
ms.reviewer: samkemp
ms.author: jburchel
author: jonburchel
reviewer: samuel100
ms.custom: build-2025, dev-focus
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand what Microsoft Foundry Local is so that I can use it to build AI applications.
---

# What is Foundry Local?

Foundry Local is an **end-to-end solution for shipping applications with embedded AI that runs entirely on the user's device**. It provides an easy-to-use SDK (C#, JavaScript, Rust, and Python), a curated catalog of optimized models, and automatic hardware acceleration — all in a lightweight package.

User data never leaves the device, responses start immediately with zero network latency, and your app works offline. There are no per-token costs and no backend infrastructure to maintain.

## Features

- **Curated model catalog** — A catalog of high-quality models optimized for on-device use across a wide range of consumer hardware. The catalog covers chat completions (for example, `phi-3.5-mini`, `qwen2.5-0.5b`) and audio transcription (for example, `whisper-tiny`). Every model goes through extensive quantization and compression to deliver the best balance of quality and performance. Models are versioned, so your application can pin to a specific version or automatically receive updates.

- **Automatic hardware acceleration** — Foundry Local detects the available hardware on the user's device and selects the best execution provider. It accelerates inference on GPUs and NPUs when available and falls back to CPU seamlessly — no hardware detection code required. Execution provider and driver updates are managed automatically to ensure optimal performance across different hardware configurations.

- **Lightweight inference runtime** — Built on [ONNX Runtime](https://onnxruntime.ai/), a high-performance inference engine written in C++ with minimal disk and memory requirements. The runtime adds approximately 20 MB to your application package, making it practical to embed AI directly into applications where size matters.

- **Smart model management** — Foundry Local handles the full lifecycle of models on end-user devices. Models download automatically on first use, are cached locally for instant subsequent launches, and the best-performing variant is selected for the user's specific hardware.

- **OpenAI-compatible API** — Supports OpenAI request and response formats for both chat completions and audio transcription. If your application already uses the OpenAI SDK, point it to a Foundry Local endpoint with minimal code changes.

- **Optional local server** — An OpenAI-compatible web server for serving models to multiple processes, integrating with tools like [LangChain](how-to/how-to-use-langchain-with-foundry-local.md), or experimenting through REST calls. For most embedded application scenarios, use the SDK directly — it runs inference in-process without the overhead of a separate server.

## Motivation for on-device AI

Foundry Local is ideal for applications that need to:

- Keep sensitive data on the user's device.
- Operate in limited-connectivity or offline environments.
- Reduce per-token cloud inference costs.
- Deliver low-latency AI responses for real-time interactions.
- Support audio transcription without sending recordings to the cloud.

## Frequently asked questions

### Is Foundry Local a web server and CLI tool?

No. Foundry Local is an **embeddable runtime** that your application ships with. It handles model acquisition, hardware acceleration, and inference end-to-end inside your app process through the SDK. The optional web server and CLI are available for development workflows, but the core product is the embedded runtime and SDK that you integrate directly into your application.

### Why doesn't Foundry Local support every available model?

Foundry Local is designed for shipping production applications, not for general-purpose model experimentation. The model catalog is intentionally curated to include models that are optimized for specific application scenarios, tested across a range of consumer hardware, and small enough to distribute to end users. This approach ensures that every model in the catalog delivers reliable performance when embedded in your application — rather than offering a broad selection of models with unpredictable on-device behavior.

### Can Foundry Local run on a server?

Foundry Local is optimized for hardware-constrained devices where a single user accesses the model at a time. While you can technically install and run it on server hardware, it isn't designed as a server inference stack.

Server-oriented runtimes like vLLM or TensorRT are built for multi-user scenarios — they handle concurrent request queuing, continuous batching, and efficient GPU sharing across many simultaneous clients. Foundry Local doesn't provide these capabilities. Instead, it focuses on lightweight, single-user inference with automatic hardware detection, KV-cache management, and model lifecycle handling that make sense for client applications.

If you need to serve models to multiple concurrent users, use a dedicated server inference framework. Use Foundry Local when the model runs on the end user's own device.

### Does Foundry Local send prompts or outputs to Microsoft?

Foundry Local runs inference entirely on the device. When your application sends prompts to a Foundry Local endpoint, prompts and model outputs are processed locally.

Foundry Local can still use the network for:

- **Model and component downloads** — The first time a model runs, Foundry Local downloads the model files and might also download execution providers for the user's hardware.
- **Optional diagnostics** — If a user reports a problem, they might choose to share logs.

Use of Foundry Local is governed by the product terms and licenses that apply to the software and the models in use. If the terms allow Microsoft to collect diagnostic information, the details are described in those terms and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).

### Is an Azure subscription required?

No. Foundry Local runs entirely on local hardware. No Azure subscription is required.

### What platforms are supported?

Foundry Local supports Windows, macOS (Apple silicon), and Linux.

## Get started

Follow the [Get started with Foundry Local](get-started.md) guide to build your first on-device AI application.

## Related content

- [Foundry Local architecture](concepts/foundry-local-architecture.md)
- [Integrate with inference SDKs](how-to/how-to-integrate-with-inference-sdks.md)
- [Foundry Local SDK reference](reference/reference-sdk-current.md)
