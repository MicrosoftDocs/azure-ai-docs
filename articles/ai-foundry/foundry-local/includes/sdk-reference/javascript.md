---
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: include
ms.date: 01/05/2026
ms.author: jburchel
ms.reviewer: maanavd
reviewer: maanavdalal
author: jonburchel
ai-usage: ai-assisted
---

## JavaScript SDK Reference

### Prerequisites

- Install Foundry Local and ensure the `foundry` command is available on your `PATH`.

### Installation

Install the package from npm:

```bash
npm install foundry-local-sdk
```

### Quickstart

Use this snippet to verify that the SDK can start the service and reach the local catalog.

```js
import { FoundryLocalManager } from "foundry-local-sdk";

const manager = new FoundryLocalManager();

await manager.startService();
const catalogModels = await manager.listCatalogModels();

console.log(`Catalog models available: ${catalogModels.length}`);
```

This example prints a non-zero number when the service is running and the catalog is available.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)

### FoundryLocalManager Class

The `FoundryLocalManager` class lets you manage models, control the cache, and interact with the Foundry Local service in both browser and Node.js environments.

#### Initialization

```js
import { FoundryLocalManager } from "foundry-local-sdk";

const foundryLocalManager = new FoundryLocalManager();
```

Available options:

- `host`: Base URL of the Foundry Local service
- `fetch`: (optional) Custom fetch implementation for environments like Node.js

### A note on aliases

Many methods outlined in this reference have an `aliasOrModelId` parameter in the signature. You can pass into the method either an **alias** or **model ID** as a value. Using an alias will:

- Select the _best model_ for the available hardware. For example, if a Nvidia CUDA GPU is available, Foundry Local selects the CUDA model. If a supported NPU is available, Foundry Local selects the NPU model.
- Allow you to use a shorter name without needing to remember the model ID.

> [!TIP]
> We recommend passing into the `aliasOrModelId` parameter an **alias** because when you deploy your application, Foundry Local acquires the best model for the end user's machine at run-time.

> [!NOTE]
> If you have an Intel NPU on Windows, ensure you have installed the [Intel NPU driver](https://www.intel.com/content/www/us/en/download/794734/intel-npu-driver-windows.html) for optimal NPU acceleration.

### Service Management

| Method | Signature | Description |
| --- | --- | --- |
| `init()` | `(aliasOrModelId?: string) => Promise<FoundryModelInfo \| void>` | Initializes the SDK and optionally loads a model. |
| `isServiceRunning()` | `() => Promise<boolean>` | Checks if the Foundry Local service is running. |
| `startService()` | `() => Promise<void>` | Starts the Foundry Local service. |
| `serviceUrl` | `string` | The base URL of the Foundry Local service. |
| `endpoint` | `string` | The API endpoint (`serviceUrl` + `/v1`). |
| `apiKey` | `string` | The API key (none). |

### Catalog Management

| Method                | Signature                                                                                | Description                                |
| --------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------ |
| `listCatalogModels()` | `() => Promise<FoundryModelInfo[]>`                                                      | Lists all available models in the catalog. |
| `refreshCatalog()`    | `() => Promise<void>`                                                                    | Refreshes the model catalog.               |
| `getModelInfo()`      | `(aliasOrModelId: string, throwOnNotFound = false) => Promise<FoundryModelInfo \| null>` | Gets model info by alias or ID.            |

### Cache Management

| Method               | Signature                           | Description                                 |
| -------------------- | ----------------------------------- | ------------------------------------------- |
| `getCacheLocation()` | `() => Promise<string>`             | Returns the model cache directory path.     |
| `listCachedModels()` | `() => Promise<FoundryModelInfo[]>` | Lists models downloaded to the local cache. |

### Model Management

| Method               | Signature                                                                                           | Description                                       |
| -------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `downloadModel()`    | `(aliasOrModelId: string, token?: string, force = false, onProgress?) => Promise<FoundryModelInfo>` | Downloads a model to the local cache.             |
| `loadModel()`        | `(aliasOrModelId: string, ttl = 600) => Promise<FoundryModelInfo>`                                  | Loads a model into the inference server.          |
| `unloadModel()`      | `(aliasOrModelId: string, force = false) => Promise<void>`                                          | Unloads a model from the inference server.        |
| `listLoadedModels()` | `() => Promise<FoundryModelInfo[]>`                                                                 | Lists all models currently loaded in the service. |

## Example Usage

The following code demonstrates how to use the `FoundryLocalManager` class to manage models and interact with the Foundry Local service.

```js
import { FoundryLocalManager } from "foundry-local-sdk";

// By using an alias, the most suitable model will be downloaded
// to your end-user's device.
// TIP: You can find a list of available models by running the
// following command in your terminal: `foundry model list`.
const alias = "qwen2.5-0.5b";

const manager = new FoundryLocalManager();

// Initialize the SDK and optionally load a model
const modelInfo = await manager.init(alias);
console.log("Model Info:", modelInfo);

// Check if the service is running
const isRunning = await manager.isServiceRunning();
console.log(`Service running: ${isRunning}`);

// List available models in the catalog
const catalog = await manager.listCatalogModels();

// Download and load a model
await manager.downloadModel(alias);
await manager.loadModel(alias);

// List models in cache
const localModels = await manager.listCachedModels();

// List loaded models
const loaded = await manager.listLoadedModels();

// Unload a model
await manager.unloadModel(alias);
```

This example downloads and loads a model, then lists cached and loaded models.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)

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
const alias = "qwen2.5-0.5b";

// Create a FoundryLocalManager instance. This will start the Foundry
// Local service if it is not already running.
const foundryLocalManager = new FoundryLocalManager();

// Initialize the manager with a model. This will download the model
// if it is not already present on the user's device.
const modelInfo = await foundryLocalManager.init(alias);
console.log("Model Info:", modelInfo);

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

This example streams a chat completion response from the local model.

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)

## Browser Usage

The SDK includes a browser-compatible version where you must specify the host URL manually:

```js
import { FoundryLocalManager } from "foundry-local-sdk/browser";

// Specify the service URL
// Run the Foundry Local service using the CLI: `foundry service start`
// and use the URL from the CLI output
const host = "HOST";

const manager = new FoundryLocalManager({ host });

// Note: The `init`, `isServiceRunning`, and `startService` methods
// are not available in the browser version
```

> [!NOTE]
> The browser version doesn't support the `init`, `isServiceRunning`, and `startService` methods. You must ensure that the Foundry Local service is running before using the SDK in a browser environment. You can start the service using the Foundry Local CLI: `foundry service start`. You can glean the service URL from the CLI output.

#### Example Usage

```js
import { FoundryLocalManager } from "foundry-local-sdk/browser";

// Specify the service URL
// Run the Foundry Local service using the CLI: `foundry service start`
// and use the URL from the CLI output
const host = "HOST";

const manager = new FoundryLocalManager({ host });

const alias = "qwen2.5-0.5b";

// Get all available models
const catalog = await manager.listCatalogModels();
console.log("Available models in catalog:", catalog);

// Download and load a specific model
await manager.downloadModel(alias);
await manager.loadModel(alias);

// View models in your local cache
const localModels = await manager.listCachedModels();
console.log("Cached models:", localModels);

// Check which models are currently loaded
const loaded = await manager.listLoadedModels();
console.log("Loaded models in inference service:", loaded);

// Unload a model when finished
await manager.unloadModel(alias);
```

References:

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)
