---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/05/2026
ms.author: jburchel
ms.reviewer: maanavd
reviewer: maanavdalal
author: jonburchel
ai-usage: ai-assisted
---

## Python SDK Reference

### Prerequisites

- Use Python 3.11 or later.

### Installation

Install the Python package:

```bash
pip install foundry-local-sdk
```

### Quickstart

Use this snippet to verify that the SDK can initialize and read the local catalog.

```python
from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="app-name")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

models = manager.catalog.list_models()
print(f"Catalog models available: {len(models)}")
```

This example prints a non-zero number when the catalog is available.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)

### FoundryLocalManager Class

The `FoundryLocalManager` class provides methods to manage models, cache, and the Foundry Local service.

#### Initialization

```python
from foundry_local_sdk import Configuration, FoundryLocalManager

# Configure and initialize the manager
config = Configuration(
    app_name="app-name",
    web={"urls": "http://localhost:5000"},
)
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance
```

- `Configuration`: Configures the SDK with app name and optional web service settings.
- `FoundryLocalManager.initialize(config)`: Initializes the singleton manager instance.
- `FoundryLocalManager.instance`: Returns the initialized manager instance.

### A note on aliases

Many methods outlined in this reference have an `alias_or_model_id` parameter in the signature. You can pass into the method either an **alias** or **model ID** as a value. Using an alias will:

- Select the _best model_ for the available hardware. For example, if a Nvidia CUDA GPU is available, Foundry Local selects the CUDA model. If a supported NPU is available, Foundry Local selects the NPU model.
- Allow you to use a shorter name without needing to remember the model ID.

> [!TIP]
> We recommend passing into the `alias_or_model_id` parameter an **alias** because when you deploy your application, Foundry Local acquires the best model for the end user's machine at run-time.

> [!NOTE]
> If you have an Intel NPU on Windows, ensure you have installed the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) for optimal NPU acceleration.

### Service Management

| Method                   | Signature          | Description                                     |
| ------------------------ | ------------------ | ----------------------------------------------- |
| `start_web_service()`    | `() -> None`       | Starts the web service for HTTP-based inference. |
| `urls`                   | `@property -> list[str]` | Returns the list of web service URLs.     |

### Catalog Management

| Method | Signature | Description |
| --- | --- | --- |
| `catalog` | `@property -> Catalog` | Returns the catalog instance for model operations. |
| `catalog.list_models()` | `() -> list[Model]` | Lists all available models in the catalog. |
| `catalog.get_model()` | `(alias_or_model_id: str) -> Model` | Gets a model by alias or ID. |

### Model Operations

| Method | Signature | Description |
| --- | --- | --- |
| `model.download()` | `(progress_callback=None) -> None` | Downloads the model to the local cache. Accepts an optional callback for progress updates. |
| `model.load()` | `() -> None` | Loads the model for inference. |
| `model.unload()` | `() -> None` | Unloads the model from the inference server. |
| `model.id` | `@property -> str` | Returns the model ID. |


### Execution Providers

One of:
- `CPUExecutionProvider` - CPU-based execution
- `CUDAExecutionProvider` - NVIDIA CUDA GPU execution
- `WebGpuExecutionProvider` - WebGPU execution
- `QNNExecutionProvider` - Qualcomm Neural Network execution (NPU)
- `OpenVINOExecutionProvider` - Intel OpenVINO execution
- `NvTensorRTRTXExecutionProvider` - NVIDIA TensorRT execution
- `VitisAIExecutionProvider` - AMD Vitis AI execution


## Example Usage

The following code demonstrates how to use the `FoundryLocalManager` class to manage models and interact with the Foundry Local service.

```python
from foundry_local_sdk import Configuration, FoundryLocalManager

# By using an alias, the most suitable model is selected
# for your end-user's device.
alias = "qwen2.5-0.5b"

# Initialize the Foundry Local SDK
config = Configuration(app_name="app-name")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# List available models in the catalog
models = manager.catalog.list_models()
print(f"Available models in the catalog: {models}")

# Get, download, and load a model
model = manager.catalog.get_model(alias)
model.download(lambda progress: print(f"\rDownloading: {progress:.2f}%", end="", flush=True))
print()
model.load()
print(f"Model ID: {model.id}")

# Unload the model
model.unload()
```

This example lists models, downloads and loads one model, and then unloads it.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)

### Integrate with OpenAI SDK

Install the OpenAI package:

```bash
pip install openai
```

The following code demonstrates how to integrate the `FoundryLocalManager` with the OpenAI SDK to interact with a local model.

```python
import openai
from foundry_local_sdk import Configuration, FoundryLocalManager

# By using an alias, the most suitable model is downloaded
# to your end-user's device.
alias = "qwen2.5-0.5b"

# Initialize the Foundry Local SDK with web service configuration
config = Configuration(
    app_name="app-name",
    web={"urls": "http://localhost:5000"},
)
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# Get and prepare the model
model = manager.catalog.get_model(alias)
model.download(lambda progress: print(f"\rDownloading: {progress:.2f}%", end="", flush=True))
print()
model.load()

# Start the web service
manager.start_web_service()

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=f"{manager.urls[0].rstrip('/')}/v1",
    api_key="local"
)

# Set the model to use and generate a streaming response
stream = client.chat.completions.create(
    model=model.id,
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True
)

# Print the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

This example streams a chat completion response from the local model.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)
