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


### Service Management

| Method                | Signature                  | Description                                      |
|-----------------------|---------------------------|--------------------------------------------------|
| `init()`              | `(modelAliasOrId?: string) => Promise<void>` | Initializes the SDK and optionally loads a model. |
| `isServiceRunning()`  | `() => Promise<boolean>`  | Checks if the Foundry Local service is running.   |
| `startService()`      | `() => Promise<void>`     | Starts the Foundry Local service.                |
| `serviceUrl`          | `string`                  | The base URL of the Foundry Local service.        |
| `endpoint`            | `string`                  | The API endpoint (serviceUrl + `/v1`).           |
| `apiKey`              | `string`                  | The API key (none).                              |


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


---

## Example Usage

```js
import { FoundryManager } from 'foundry-management-sdk'

const manager = new FoundryManager({ serviceUrl: 'http://localhost:5272' })

// Initialize the SDK and optionally load a model
await manager.init('DeepSeek-R1-Distill-Qwen-1.5B-generic-gpu')

// Check if the service is running
const isRunning = await manager.isServiceRunning()
console.log(`Service running: ${isRunning}`)

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

---

## OpenAI-Compatible Usage

You can use the Foundry Local endpoint with an OpenAI-compatible API client. For example, using the `openai` package:

```js
const { OpenAI } = require('openai')

const client = new OpenAI({
    apiKey: manager.apiKey,
    baseURL: manager.endpoint
})

const completion = await client.chat.completions.create({
    model: 'DeepSeek-R1-Distill-Qwen-1.5B-generic-gpu',
    messages: [{"role": "user", "content": "Solve x^2 + 5x + 6 = 0."}],
    max_tokens: 250,
    stream: true,
});
for await (const chunk of completion) {
    const textChunk = chunk.choices[0]?.delta?.content || "";
    if (textChunk) {
        process.stdout.write(textChunk);
    }
}
```

---

## Browser Usage

The SDK also provides a browser-compatible version. However, you must provide the service URL manually. You can use the `FoundryManager` class in the browser as follows:

```js
import { FoundryManager } from 'foundry-local/browser'

const manager = new FoundryManager({ serviceUrl: 'http://localhost:8080' })

// The rest of the code is the same as above, except that `init`, `isServiceRunning`, and `startService` are not available in the browser version.
```

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
