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
pip install foundry-manager
```

### FoundryManager Class

The `FoundryManager` class provides methods to manage models, cache, and the Foundry Local service.

#### Initialization

```python
from foundry_manager import FoundryManager

# Initialize and optionally bootstrap with a model
manager = FoundryManager(model_id_or_alias=None, bootstrap=True)
```

- `model_id_or_alias`: (optional) Model ID or alias to download and load at startup.
- `bootstrap`: (default True) If True, starts the service if not running and loads the model if provided.

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
| `get_model_info()`        | `(model_alias_or_id: str, raise_on_not_found=False) -> FoundryModelInfo or None` | Gets model info by alias or ID.                  |

### Cache Management

| Method                    | Signature                                         | Description                                      |
|---------------------------|---------------------------------------------------|--------------------------------------------------|
| `get_cache_location()`    | `() -> str`                                       | Returns the model cache directory path.           |
| `list_local_models()`     | `() -> list[FoundryModelInfo]`                    | Lists models downloaded to the local cache.       |

### Model Management

| Method                        | Signature                                                                 | Description                                      |
|-------------------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| `download_model()`            | `(model_alias_or_id: str, token: str = None, force: bool = False) -> FoundryModelInfo` | Downloads a model to the local cache.            |
| `load_model()`                | `(model_alias_or_id: str, ttl: int = 600) -> FoundryModelInfo`            | Loads a model into the inference server.         |
| `unload_model()`              | `(model_alias_or_id: str, force: bool = False) -> None`                   | Unloads a model from the inference server.       |
| `list_loaded_models()`        | `() -> list[FoundryModelInfo]`                                            | Lists all models currently loaded in the service.|

#### Example Usage

```python
from foundry_local import FoundryManager

manager = FoundryManager()

# List available models in the catalog
catalog = manager.list_catalog_models()

# Download and load a model
manager.download_model("DeepSeek-R1-Distill-Qwen-1.5B")
manager.load_model("DeepSeek-R1-Distill-Qwen-1.5B")

# List models in cache
local_models = manager.list_local_models()

# List loaded models
loaded = manager.list_loaded_models()

# Unload a model
manager.unload_model("DeepSeek-R1-Distill-Qwen-1.5B")
```
