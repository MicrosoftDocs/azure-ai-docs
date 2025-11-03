---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 06/09/2025
ms.author: samkemp
author: samuel100
---

## C# SDK Reference

### Version `>=0.4.0` Redesign

To improve your ability to ship applications using on-device AI, we've made substantial changes to the architecture of the C# SDK and with that there are breaking changes in the API from version `0.3.0` and earlier to version `0.4.0` and later.

#### Architecture changes

The following diagram shows how the previous architecture - for versions `0.3.0` and earlier - relied heavily on using a REST webserver to manage models and inference like chat completions:

![previous architecture](../../media/architecture/current-sdk-architecture.png)

The SDK would use an RPC call to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, we have redesigned the architecture in version `0.4.0` and later to use a more streamlined approach. The new architecture is as follows:

![new architecture](../../media/architecture/new-sdk-architecture.png)

In this new architecture:

- Your application is **self-contained**. It does not require the Foundry Local CLI to be installed separately on the end user's machine. This allows you to package and distribute your application more easily.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other SDKs or tools that communicate over HTTP, but for most use cases, you can interact directly with the Foundry Local service process. Read [Use chat completions via REST server with Foundry Local](../../how-to/how-to-integrate-with-inference-sdks.md) for details on how to use this feature.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies. Read [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md) for details on how to use this feature.
- On Windows devices, you can use a Windows ML build that will handle **hardware acceleration** for models on the device by pulling in the right runtime and drivers.


#### API changes

Version `0.4.0` and later provides a more object-orientated and composable API. The main entry point continues to be the `FoundryLocalManager` class, but instead of being a flat set of methods that operate via static calls to a stateless HTTP API, the SDK now exposes methods on the `FoundryLocalManager` instance that maintain state about the service and models.

| Primitive           | Versions <= 0.3.0 | Versions >= 0.4.0 |
|---------------------|-------------------|-------------------|
| **Configuration**    | N/A | `config = Configuration(...)` |
| **Get Manager**     | `mgr = FoundryLocalManager();`| `await FoundryLocalManager.CreateAsync(config, logger);`<br>`var mgr = FoundryLocalManager.Instance;`  |
| **Get Catalog**   | N/A | `catalog = mgr.GetCatalog();` |
| **List Models**            | `mgr.ListCatalogModelsAsync();`| `catalog.ListModelsAsync();`                           |
| **Get Model**  | `mgr.GetModelInfoAsync("aliasOrModelId");`| `catalog.GetModelAsync(alias: "alias");`     |
| **Get Variant**| N/A  | `model.SelectedVariant;` |
| **Set Variant**| N/A  | `model.SelectVariant();` |
| **Download a model**| `mgr.DownloadModelAsync("aliasOrModelId");` | `model.DownloadAsync()`                                                               |
| **Load a model**    | `mgr.LoadModelAsync("aliasOrModelId");`     | `model.LoadAsync()`                                                                   |
| **Unload a Model**  | `mgr.UnloadModelAsync("aliasOrModelId");`   | `model.UnloadAsync()`                                                                 |
| **List Loaded Models**   | `mgr.ListLoadedModelsAsync();`             | `catalog.GetLoadedModelsAsync();`                                                               |
| **Get Model Path**  | N/A                                        | `model.GetPathAsync()`                                                                |
| **Start service**   | `mgr.StartServiceAsync();`                 | `mgr.StartWebServerAsync();` |
| **Stop Service**    | `mgr.StopServiceAsync();`                | `mgr.StopWebServerAsync();`      |
| **Cache Location**  | `mgr.GetCacheLocationAsync();`        | `config.ModelCacheDir`                           |
| **List Cached Models** | `mgr.ListCachedModelsAsync();`     | `catalog.GetCachedModelsAsync();`                                                         |

##### Side-by-side basic usage

## [Version <= 0.3.0](#tab/previous)

```csharp
using Microsoft.AI.Foundry.Local;

// Initialize the manager
var manager = new FoundryLocalManager();
await manager.StartServiceAsync();

// List available models in the catalog
var models = await manager.ListCatalogModelsAsync();

// Download and load a model by alias
var alias = "qwen2.5-0.5b";
await manager.DownloadModelAsync(alias);
await manager.LoadModelAsync(alias);

// List loaded models
var loaded = await manager.ListLoadedModelsAsync();

// Unload the model
await manager.UnloadModelAsync(alias);
```

## [Version >= 0.4.0](#tab/vNext)

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;


var config = new Configuration
{
    AppName = "my-app-name"
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance.
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Get the model catalog
var catalog = mgr.GetCatalog();

// List available models in the catalog
var models = await catalog.ListModelsAsync();

// Get a model using an alias
var model = await catalog.GetModelAsync("qwen2.5-0.5b") ?? throw new Exception("Model not found");

// Download and load the model
await model.DownloadAsync();
await model.LoadAsync();

// List loaded models
var loaded = await catalog.GetLoadedModelsAsync();

// Unload the model
await model.UnloadAsync();
```

---

### Installation

To use the Foundry Local C# SDK, you need to install the NuGet package:

```bash
dotnet add package Microsoft.AI.Foundry.Local
```
