## C# API Reference

### Installation

Install the NuGet package:

```bash
dotnet add package Microsoft.AI.Foundry.Management
```

### Model Management

| Method                               | Signature                                       | Description                                    |
| ------------------------------------ | ----------------------------------------------- | ---------------------------------------------- |
| `ListModelsAsync()`                  | `Task<List<Model>>`                             | Lists all available models for download.       |
| `DownloadModelAsync(string modelId)` | `Task`                                          | Downloads a model to local disk.               |
| `GetModelInfoAsync(string modelId)`  | `Task<Model>`                                   | Retrieves information for a specific model.    |
| `LoadModelAsync(string modelId)`     | `Task`                                          | Loads a model into the inference server.       |
| `UnloadModelAsync(string modelId)`   | `Task`                                          | Unloads a model from the inference server.     |

### Cache Management

| Method                                       | Signature                            | Description                                   |
| -------------------------------------------- | ------------------------------------ | --------------------------------------------- |
| `ListCacheAsync()`                           | `Task<List<Model>>`                  | Lists models in the local cache.              |
| `GetCacheLocationAsync()`                    | `Task<string>`                       | Returns the cache directory path.             |
| `RemoveFromCacheAsync(string modelId)`       | `Task`                               | Removes a model from the cache.               |
| `SetCacheLocationAsync(string path)`         | `Task`                               | Changes the cache directory.                  |

### Service Management

| Method                                  | Signature                             | Description                                   |
| --------------------------------------- | ------------------------------------- | --------------------------------------------- |
| `StartServiceAsync()`                   | `Task`                                | Starts the Foundry model service.             |
| `StopServiceAsync()`                    | `Task`                                | Stops the Foundry model service.              |
| `RestartServiceAsync()`                 | `Task`                                | Restarts the Foundry model service.           |
| `GetServiceStatusAsync()`               | `Task<ServiceStatus>`                 | Gets the current service status (Running).    |
| `ListLoadedModelsAsync()`               | `Task<List<Model>>`                   | Lists models loaded in the service.           |
