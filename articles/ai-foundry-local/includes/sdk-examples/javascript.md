## JavaScript API Reference

### Installation

Install the npm package:

```bash
npm install foundry-management-sdk
```

### Model Management

| Method                     | Signature                                     | Description                                    |
| -------------------------- | --------------------------------------------- | ---------------------------------------------- |
| `listModels()`             | `() => Promise<Array<{ id: string }>>`        | Lists all available models for download.       |
| `downloadModel(modelId)`   | `(modelId: string) => Promise<void>`          | Downloads a model to disk.                     |
| `getModelInfo(modelId)`    | `(modelId: string) => Promise<any>`           | Retrieves information for a specific model.    |
| `loadModel(modelId)`       | `(modelId: string) => Promise<void>`          | Loads a model into the inference server.       |
| `unloadModel(modelId)`     | `(modelId: string) => Promise<void>`          | Unloads a model from the inference server.     |

### Cache Management

| Method                    | Signature                              | Description                                    |
| ------------------------- | -------------------------------------- | ---------------------------------------------- |
| `listCache()`             | `() => Promise<Array<{ id: string }>>` | Lists models in the local cache.               |
| `getCacheLocation()`      | `() => Promise<string>`                | Returns the cache directory path.              |
| `removeFromCache(id)`     | `(id: string) => Promise<void>`        | Removes a model from the cache.                |
| `setCacheLocation(path)`  | `(path: string) => Promise<void>`      | Changes the cache directory.                   |

### Service Management

| Method                   | Signature                          | Description                                   |
| ------------------------ | ---------------------------------- | --------------------------------------------- |
| `startService()`         | `() => Promise<void>`              | Starts the Foundry model service.             |
| `stopService()`          | `() => Promise<void>`              | Stops the Foundry model service.              |
| `restartService()`       | `() => Promise<void>`              | Restarts the Foundry model service.           |
| `getServiceStatus()`     | `() => Promise<{ running: boolean }>` | Gets the current service status.             |
| `listLoadedModels()`     | `() => Promise<Array<{ id: string }>>` | Lists models loaded in the service.         |
