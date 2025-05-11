---
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

## JavaScript SDK Reference

### Installation

Install the package from npm:

```bash
npm install foundry-local-sdk
```

### FoundryLocalManager Class

The `FoundryLocalManager` class lets you manage models, control the cache, and interact with the Foundry Local service in both browser and Node.js environments.

#### Initialization

```js
import { FoundryLocalManager } from "foundry-local-sdk";

const foundryLocalManager = new FoundryLocalManager()
```

Available options:
- `serviceUrl`: Base URL of the Foundry Local service
- `fetch`: (optional) Custom fetch implementation for environments like Node.js


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
| `getModelInfo()`          | `(modelAliasOrId: string, throwOnNotFound = false) => Promise<FoundryModelInfo \| null>` | Gets model info by alias or ID.                  |


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

## Example Usage

The following code demonstrates how to use the `FoundryLocalManager` class to manage models and interact with the Foundry Local service.

```js
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded 
// to your end-user's device.
// TIP: You can find a list of available models by running the 
// following command in your terminal: `foundry model list`.
const modelAlias = "deepseek-r1-1.5b";

const manager = new FoundryLocalManager()

// Initialize the SDK and optionally load a model
const modelInfo = await manager.init(modelAlias)
console.log("Model Info:", modelInfo)

// Check if the service is running
const isRunning = await manager.isServiceRunning()
console.log(`Service running: ${isRunning}`)

// List available models in the catalog
const catalog = await manager.listCatalogModels()

// Download and load a model
await manager.downloadModel(modelAlias)
await manager.loadModel(modelAlias)

// List models in cache
const localModels = await manager.listLocalModels()

// List loaded models
const loaded = await manager.listLoadedModels()

// Unload a model
await manager.unloadModel(modelAlias)
```

---

## Integration with OpenAI Client

Install the OpenAI package:

```bash
npm install openai
```

The following code demonstrates how to integrate the `FoundryLocalManager` with the OpenAI client to interact with a local model.

```js
import { OpenAI } from "openai";
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded 
// to your end-user's device.
// TIP: You can find a list of available models by running the 
// following command in your terminal: `foundry model list`.
const modelAlias = "deepseek-r1-1.5b";

// Create a FoundryLocalManager instance. This will start the Foundry 
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager()

// Initialize the manager with a model. This will download the model 
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(modelAlias)
console.log("Model Info:", modelInfo)

const openai = new OpenAI({
  baseURL: foundryLocalManager.endpoint,
  apiKey: foundryLocalManager.apiKey,
});

async function streamCompletion() {
    const stream = await openai.chat.completions.create({
      model: modelInfo.id,
      messages: [{ role: "user", content: "What is the golden ratio?" }],
      stream: true,
    });
  
    for await (const chunk of stream) {
      if (chunk.choices[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
      }
    }
}
  
streamCompletion();
```

---

## Browser Usage

The SDK includes a browser-compatible version where you must specify the service URL manually:

```js
import { FoundryLocalManager } from "foundry-local-sdk/browser"

const manager = new FoundryLocalManager({serviceUrl: "http://localhost:5272"})

// Note: The `init`, `isServiceRunning`, and `startService` methods 
// are not available in the browser version
```

#### Example Usage

```js
import { FoundryLocalManager } from "foundry-local-sdk/browser"

const manager = new FoundryLocalManager({serviceUrl: "http://localhost:5272"})

const modelAlias = 'deepseek-r1-1.5b'

// Get all available models
const catalog = await manager.listCatalogModels()
console.log("Available models in catalog:", catalog)

// Download and load a specific model
await manager.downloadModel(modelAlias)
await manager.loadModel(modelAlias)

// View models in your local cache
const localModels = await manager.listLocalModels()
console.log("Cached models:", catalog)

// Check which models are currently loaded
const loaded = await manager.listLoadedModels()
console.log("Loaded models in inference service:", loaded)

// Unload a model when finished
await manager.unloadModel(modelAlias)
```
