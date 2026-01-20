---
title: Foundry Local architecture
titleSuffix: Foundry Local
description: Learn about the architecture and components of Foundry Local
ms.service: azure-ai-foundry
ms.subservice: foundry-local
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

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local provides efficient, secure, and scalable AI model inference directly on your device. This article explains the core components of Foundry Local and how they work together to deliver AI capabilities.

## Prerequisites

- Install Foundry Local. For setup steps, see [Get started with Foundry Local](../get-started.md).
- Use a local terminal where the `foundry` CLI is available.

## Quick verification

Use the following quick checks to confirm the service is running and reachable.

1. Get the service status and local endpoint:

  ```bash
  foundry service status
  ```

  This command prints the service status and the dynamically assigned local endpoint.

  Reference: [Foundry Local CLI Reference](../reference/reference-cli.md#service-commands)

1. Call the local REST status endpoint:

  ```bash
  curl http://localhost:PORT/openai/status
  ```

  Replace `PORT` with the port shown by `foundry service status`. A successful response is JSON that includes `Endpoints`, `ModelDirPath`, and `PipeName`.

  Reference: [Foundry Local REST API Reference](../reference/reference-rest.md#get-openaistatus)

Foundry Local offers these key benefits:

> [!div class="checklist"]
>
> - **Low latency**: Run models locally to minimize processing time and deliver faster results.
> - **Data privacy**: Process sensitive data locally without sending it to the cloud for inference, helping meet data protection requirements.
> - **Flexibility**: Support for diverse hardware configurations lets you choose the optimal setup for your needs.
> - **Scalability**: Deploy across various devices, from laptops to servers, to suit different use cases.
> - **Cost-effectiveness**: Reduce cloud computing costs, especially for high-volume applications.
> - **Offline operation**: Work without an internet connection in remote or disconnected environments.
> - **Seamless integration**: Easily incorporate into existing development workflows for smooth adoption.

Foundry Local can still use the network for operations like downloading models and execution providers. If you report a problem, you might choose to share logs (for example, by using `foundry zip-logs`).

## Key components

The Foundry Local architecture consists of these main components:

:::image type="content" source="../media/architecture/foundry-local-arch.png" alt-text="Diagram showing Foundry Local service and ONNX Runtime using locally cached models and device execution providers.":::

### Foundry Local service

The Foundry Local Service includes an OpenAI-compatible REST server that provides a standard interface for working with the inference engine. You can also manage models over REST. Developers use this API to send requests, run models, and get results programmatically.

- **Endpoint**: The endpoint is _dynamically allocated_ when the service starts. Find it by running the `foundry service status` command, or by calling `GET /openai/status`. When using Foundry Local in your applications, use an integration SDK that automatically handles endpoint discovery. For more details, see [Integrate with inference SDKs](../how-to/how-to-integrate-with-inference-sdks.md) and the [Foundry Local REST API Reference](../reference/reference-rest.md).
- **Use Cases**:
  - Connect Foundry Local to your custom applications
  - Execute models through HTTP requests

### ONNX runtime

The ONNX Runtime is a core component that executes AI models. It runs optimized ONNX models efficiently on local hardware like CPUs, GPUs, or NPUs.

**Features**:

- Works with multiple hardware providers (NVIDIA, AMD, Intel, Qualcomm) and device types (NPUs, CPUs, GPUs)
- Offers a consistent interface for running models across different hardware
- Delivers high performance
- Supports quantized models for faster inference

### Model management

Foundry Local provides robust tools for managing AI models, ensuring that they're readily available for inference and easy to maintain. You handle model management through the **Model Cache** and the **Command-Line Interface (CLI)**.

#### Model cache

The model cache stores downloaded AI models locally on your device, which ensures models are ready for inference without needing to download them repeatedly. You can manage the cache by using either the Foundry CLI or REST API.

- **Purpose**: Speeds up inference by keeping models locally available
- **Key Commands**:
  - `foundry cache list`: Shows all models in your local cache
  - `foundry cache remove <model-name>`: Removes a specific model from the cache
  - `foundry cache cd <path>`: Changes the storage location for cached models

#### Model lifecycle

1. **Download**: Download models from the Foundry model catalog and save them to your local disk.
1. **Load**: Load models into the Foundry Local service memory for inference. Set a TTL (time-to-live) to control how long the model stays in memory (default: 600 seconds).
1. **Run**: Execute model inference for your requests.
1. **Unload**: Remove models from memory to free up resources when no longer needed.
1. **Delete**: Remove models from your local cache to reclaim disk space.

#### Model compilation using Olive

Before you can use models with Microsoft Foundry Local, you must compile and optimize them in the [ONNX](https://onnx.ai) format. Microsoft provides a selection of published models in the Foundry model catalog that are already optimized for Foundry Local. However, you aren't limited to those models - by using [Olive](https://microsoft.github.io/Olive/). Olive is a powerful framework for preparing AI models for efficient inference. It converts models into the ONNX format, optimizes their graph structure, and applies techniques like quantization to improve performance on local hardware.

> [!TIP]
> To learn more about compiling models for Foundry Local, see [How to compile Hugging Face models to run on Foundry Local](../how-to/how-to-compile-hugging-face-models.md).

### Hardware abstraction layer

The hardware abstraction layer ensures that Foundry Local runs on various devices by abstracting the underlying hardware. To optimize performance based on the available hardware, Foundry Local supports:

- **multiple _execution providers_**, such as NVIDIA CUDA, AMD, Qualcomm, Intel.
- **multiple _device types_**, such as CPU, GPU, NPU.

> [!NOTE]
> For Intel NPU support on Windows, install the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) to enable hardware acceleration.

> [!NOTE]
> For Qualcomm NPU support, install the [Qualcomm NPU driver](https://softwarecenter.qualcomm.com/catalog/item/QHND). If you encounter the error `Qnn error code 5005: "Failed to load from EpContext model. qnn_backend_manager."`, this error typically indicates an outdated driver or NPU resource conflicts. Try rebooting to clear NPU resource conflicts, especially after using Windows Copilot+ features.

### Developer experiences

The Foundry Local architecture is designed to provide a seamless developer experience, enabling easy integration and interaction with AI models.
Developers can choose from various interfaces to interact with the system, including:

#### Command-Line Interface (CLI)

The Foundry CLI is a powerful tool for managing models, the inference engine, and the local cache.

**Examples**:

- `foundry model list`: Lists all available models in the local cache.
- `foundry model run <model-name>`: Runs a model.
- `foundry service status`: Checks the status of the service.

> [!TIP]
> To learn more about the CLI commands, read [Foundry Local CLI Reference](../reference/reference-cli.md).

#### Inferencing SDK integration

Foundry Local supports integration with various SDKs in most languages, such as the OpenAI SDK, enabling developers to use familiar programming interfaces to interact with the local inference engine.

> [!TIP]
> To learn more about integrating with inferencing SDKs, read [Integrate inferencing SDKs with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md).

#### AI Toolkit for Visual Studio Code

The AI Toolkit for Visual Studio Code provides a user-friendly interface for developers to interact with Foundry Local. It allows users to run models, manage the local cache, and visualize results directly within the IDE.

**Features**:

- Model management: Download, load, and run models from within the IDE.
- Interactive console: Send requests and view responses in real-time.
- Visualization tools: Graphical representation of model performance and results.

**Prerequisites:**

- You have installed [Foundry Local](../get-started.md) and have a model service running.
- You have installed the [AI Toolkit for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) extension.

**Connect a Foundry Local model to AI Toolkit:**

1. **Add model in AI Toolkit**: Open AI Toolkit from the activity bar of Visual Studio Code. In the 'My Models' panel, select the 'Add model for remote interface' button and then select 'Add a custom model' from the dropdown menu.

2. **Enter the chat-compatible endpoint URL**: Enter `http://localhost:PORT/v1/chat/completions`, where `PORT` is the port number of your Foundry Local endpoint. Find the port by running `foundry service status`. Foundry Local dynamically assigns a port, so it might not always be the same.
3. **Provide the model name**: Enter the exact model name you want to use, for example `phi-3.5-mini`. List downloaded and cached models with `foundry cache list`, or use `foundry model list` to see models available for local use. You'll also be asked to enter a display name, which is only for your local use. To avoid confusion, use the same value as the model name.
4. **Authentication**: If your local setup doesn't require authentication, leave the authentication headers field blank.

After completing these steps, your Foundry Local model appears in the **My Models** list in AI Toolkit. To start using it, right-click the model and select **Load in Playground**.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Integrate inferencing SDKs with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md)
- [Foundry Local CLI Reference](../reference/reference-cli.md)
