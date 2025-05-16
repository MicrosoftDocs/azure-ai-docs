---
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

## Python SDK Reference

### Installation

Install the Python package:

```bash
pip install foundry-local-sdk
```

### FoundryLocalManager Class

The `FoundryLocalManager` class provides methods to manage models, cache, and the Foundry Local service.

#### Initialization

```python
from foundry_local import FoundryLocalManager

# Initialize and optionally bootstrap with a model
manager = FoundryLocalManager(alias_or_model_id=None, bootstrap=True)
```

- `alias_or_model_id`: (optional) Alias or Model ID to download and load at startup.
- `bootstrap`: (default True) If True, starts the service if not running and loads the model if provided.

### A note on aliases

Many methods outlined in this reference have an `alias_or_model_id` parameter in the signature. You can pass into the method either an **alias** or **model ID** as a value. Using an alias will:

- Select the *best model* for the available hardware. For example, if a Nvidia CUDA GPU is available, Foundry Local selects the CUDA model. If a supported NPU is available, Foundry Local selects the NPU model.
- Allow you to use a shorter name without needing to remember the model ID.

> [!TIP]
> We recommend passing into the `alias_or_model_id` parameter an **alias** because when you deploy your application, Foundry Local acquires the best model for the end user's machine at run-time.

### Service Management

| Method                | Signature                  | Description                                      |
|-----------------------|---------------------------|--------------------------------------------------|
| `is_service_running()`| `() -> bool`              | Checks if the Foundry Local service is running.   |
| `start_service()`     | `() -> None`              | Starts the Foundry Local service.                |
| `service_uri`         | `@property -> str`        | Returns the service URI.                         |
| `endpoint`            | `@property -> str`        | Returns the service endpoint.                    |
| `api_key`             | `@property -> str`        | Returns the API key (from env or default).       |

### Catalog Management

| Method                    | Signature                                         | Description                                      |
|---------------------------|---------------------------------------------------|--------------------------------------------------|
| `list_catalog_models()`   | `() -> list[FoundryModelInfo]`                    | Lists all available models in the catalog.        |
| `refresh_catalog()`       | `() -> None`                                      | Refreshes the model catalog.                     |
| `get_model_info()`        | `(alias_or_model_id: str, raise_on_not_found=False) -> FoundryModelInfo or None` | Gets model info by alias or ID.                  |

### Cache Management

| Method                    | Signature                                         | Description                                      |
|---------------------------|---------------------------------------------------|--------------------------------------------------|
| `get_cache_location()`    | `() -> str`                                       | Returns the model cache directory path.           |
| `list_local_models()`     | `() -> list[FoundryModelInfo]`                    | Lists models downloaded to the local cache.       |

### Model Management

| Method                        | Signature                                                                 | Description                                      |
|-------------------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| `download_model()`            | `(alias_or_model_id: str, token: str = None, force: bool = False) -> FoundryModelInfo` | Downloads a model to the local cache.            |
| `load_model()`                | `(alias_or_model_id: str, ttl: int = 600) -> FoundryModelInfo`            | Loads a model into the inference server.         |
| `unload_model()`              | `(alias_or_model_id: str, force: bool = False) -> None`                   | Unloads a model from the inference server.       |
| `list_loaded_models()`        | `() -> list[FoundryModelInfo]`                                            | Lists all models currently loaded in the service.|

## Example Usage

The following code demonstrates how to use the `FoundryManager` class to manage models and interact with the Foundry Local service.

```python
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be selected 
# to your end-user's device.
alias = "deepseek-r1-1.5b"

# Create a FoundryLocalManager instance. This will start the Foundry.
manager = FoundryLocalManager()

# List available models in the catalog
catalog = manager.list_catalog_models()
print(f"Available models in the catalog: {catalog}")

# Download and load a model
model_info = manager.download_model(alias)
model_info = manager.load_model(alias)
print(f"Model info: {model_info}")

# List models in cache
local_models = manager.list_local_models()
print(f"Models in cache: {local_models}")

# List loaded models
loaded = manager.list_loaded_models()
print(f"Models running in the service: {loaded}")

# Unload a model
manager.unload_model(alias)
```

### Integrate with OpenAI SDK

Install the OpenAI package:

```bash
pip install openai
```

The following code demonstrates how to integrate the `FoundryLocalManager` with the OpenAI SDK to interact with a local model.

```python
import openai
from foundry_local import FoundryLocalManager

# By using an alias, the most suitable model will be downloaded 
# to your end-user's device.
alias = "deepseek-r1-1.5b"

# Create a FoundryLocalManager instance. This will start the Foundry 
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(alias)

# The remaining code us es the OpenAI Python SDK to interact with the local model.

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=manager.endpoint,
    api_key=manager.api_key  # API key is not required for local usage
)

# Set the model to use and generate a streaming response
stream = client.chat.completions.create(
    model=manager.get_model_info(alias).id,
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True
)

# Print the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```
