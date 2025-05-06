## Python API Reference

### Installation

Install the Python package:

```bash
pip install foundry-management-sdk
```

### Model Management

| Method                         | Signature                             | Description                                     |
| ------------------------------ | ------------------------------------- | ----------------------------------------------- |
| `list_models()`                | `() -> List[Dict]`                    | Lists all available models for download.        |
| `download_model(model_id)`     | `(model_id: str) -> None`             | Downloads a model to the local disk.            |
| `get_model_info(model_id)`     | `(model_id: str) -> Dict`             | Retrieves detailed information for a model.     |
| `load_model(model_id)`         | `(model_id: str) -> None`             | Loads a model into the inference server.        |
| `unload_model(model_id)`       | `(model_id: str) -> None`             | Unloads a model from the inference server.      |

### Cache Management

| Method                        | Signature                            | Description                                        |
| ----------------------------- | ------------------------------------ | -------------------------------------------------- |
| `list_cache()`                | `() -> List[Dict]`                   | Lists models in the local cache.                   |
| `get_cache_location()`        | `() -> str`                          | Returns the model cache directory path.            |
| `remove_from_cache(model_id)` | `(model_id: str) -> None`            | Removes a model from the cache.                    |
| `set_cache_location(path)`    | `(path: str) -> None`                | Changes the directory for the model cache.         |

### Service Management

| Method                    | Signature                       | Description                                       |
| ------------------------- | ------------------------------- | ------------------------------------------------- |
| `start_service()`         | `() -> None`                    | Starts the Foundry model service.                 |
| `stop_service()`          | `() -> None`                    | Stops the Foundry model service.                  |
| `restart_service()`       | `() -> None`                    | Restarts the Foundry model service.               |
| `get_service_status()`    | `() -> Dict`                    | Returns service status (running state, etc.).     |
| `list_loaded_models()`    | `() -> List[Dict]`              | Lists all models loaded in the service.           |
