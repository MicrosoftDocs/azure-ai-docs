---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 06/09/2025
ms.author: samkemp
author: samuel100
---

## C# SDK Reference

### Version `>=0.4.0` Redesign

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the C# SDK in version `0.4.0` and with that there are breaking changes in the API from version `0.3.0` and earlier to version `0.4.0` and later.

#### Architecture changes

The following diagram shows how the previous architecture - for versions `0.3.0` and earlier - relied heavily on using a REST webserver to manage models and inference like chat completions:

![previous architecture](../../media/architecture/current-sdk-architecture.png)

The SDK would use a Remote Procedural Call (RPC) to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, the redesigned architecture in version `0.4.0` and later uses a more streamlined approach. The new architecture is as follows:

![new architecture](../../media/architecture/new-sdk-architecture.png)

In this new architecture:

- Your application is **self-contained**. It doesn't require the Foundry Local CLI to be installed separately on the end user's machine making it easier for you to deploy applications.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other tools that communicate over HTTP. Read [Use chat completions via REST server with Foundry Local](../../how-to/how-to-integrate-with-inference-sdks.md) for details on how to use this feature.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies. Read [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md) for details on how to use this feature.
- On Windows devices, you can use a Windows ML build that handles **hardware acceleration** for models on the device by pulling in the right runtime and drivers.


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
| **List Cached Models** | `mgr.ListCachedModelsAsync();`     | `catalog.GetCachedModelsAsync();`               |

The API allows Foundry Local to be more configurable over the web server, logging, cache location, and model variant selection. For example, the `Configuration` class allows you to set up the application name, logging level, web server URLs, and directories for application data, model cache, and logs:

```csharp
var config = new Configuration
{
    AppName = "my-app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
    Web = new Configuration.WebService
    {
        Urls = "http://127.0.0.1:55588"
    },
    AppDataDir = "./foundry_local_data",
    ModelCacheDir = "{AppDataDir}/model_cache",
    LogsDir = "{AppDataDir}/logs"
};
```

In the previous version of the Foundry Local C# SDK, you couldn't configure these settings directly through the SDK, which limited your ability to customize the behavior of the service.

##### Side-by-side basic usage

## [Versions <= 0.3.0](#tab/previous)

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

## [Versions >= 0.4.0](#tab/vNext)

The biggest change in the new SDK version is the introduction of the `Configuration` class for setting up the Foundry Local environment and the need to define a `ILogger` instance for logging.

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;

// Create configuration
var config = new Configuration
{
    AppName = "my-app-name"
};

// Set up application logging
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

// List loaded models (in memory) from the catalog
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
