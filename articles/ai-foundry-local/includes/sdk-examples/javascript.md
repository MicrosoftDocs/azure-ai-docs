## JavaScript SDK Reference

### Installation

Install the npm package:

```bash
npm install foundry-management-sdk
```

### FoundryManager Class

The `FoundryManager` class provides methods to manage models, cache, and the Foundry Local service in the browser or Node.js.

#### Initialization

```js
import { FoundryManager } from 'foundry-management-sdk'

const manager = new FoundryManager({ serviceUrl: 'http://localhost:5272' })
```

- `serviceUrl`: The base URL of the Foundry Local service.
- `fetch`: (optional) Custom fetch implementation (e.g., for Node.js).

### Catalog Management

| Method                    | Signature                                                                 | Description                                      |
|---------------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| `listCatalogModels()`     | `() => Promise<FoundryModelInfo[]>`                                       | Lists all available models in the catalog.        |
| `refreshCatalog()`        | `() => Promise<void>`                                                     | Refreshes the model catalog.                     |
| `getModelInfo()`          | `(modelAliasOrId: string, throwOnNotFound = false) => Promise<FoundryModelInfo | null>` | Gets model info by alias or ID.                  |

### Cache Management

| Method                    | Signature                                         | Description                                      |
|---------------------------|---------------------------------------------------|--------------------------------------------------|
| `getCacheLocation()`      | `() => Promise<string>`                           | Returns the model cache directory path.           |
| `listLocalModels()`       | `() => Promise<FoundryModelInfo[]>`               | Lists models downloaded to the local cache.       |

### Model Management

| Method                        | Signature                                                                 | Description                                      |
|-------------------------------|---------------------------------------------------------------------------|--------------------------------------------------|
| `downloadModel()`             | `(modelAliasOrId: string, force = false, onProgress?) => Promise<FoundryModelInfo>` | Downloads a model to the local cache.            |
| `loadModel()`                 | `(modelAliasOrId: string, ttl = 600) => Promise<FoundryModelInfo>`        | Loads a model into the inference server.         |
| `unloadModel()`               | `(modelAliasOrId: string, force = false) => Promise<void>`                | Unloads a model from the inference server.       |
| `listLoadedModels()`          | `() => Promise<FoundryModelInfo[]>`                                       | Lists all models currently loaded in the service.|

### Properties

| Property      | Type     | Description                                  |
|-------------- |----------|----------------------------------------------|
| `serviceUrl`  | `string` | The base URL of the Foundry Local service.   |
| `endpoint`    | `string` | The API endpoint (serviceUrl + `/v1`).       |
| `apiKey`      | `string` | The API key (always `OPENAI_API_KEY`).       |

#### Example Usage

```js
import { FoundryManager } from 'foundry-management-sdk'

const manager = new FoundryManager({ serviceUrl: 'http://localhost:5272' })

// List available models in the catalog
const catalog = await manager.listCatalogModels()

// Download and load a model
await manager.downloadModel('DeepSeek-R1-Distill-Qwen-1.5B-generic-gpu')
await manager.loadModel('DeepSeek-R1-Distill-Qwen-1.5B-generic-gpu')

// List models in cache
const localModels = await manager.listLocalModels()

// List loaded models
const loaded = await manager.listLoadedModels()

// Unload a model
await manager.unloadModel('DeepSeek-R1-Distill-Qwen-1.5B-generic-gpu')
```
