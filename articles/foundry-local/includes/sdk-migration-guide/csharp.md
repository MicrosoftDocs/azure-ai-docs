---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/05/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## C# SDK Migration Guide

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the C# SDK in version `0.8.0` and later. In this section, we outline the key changes to help you migrate your applications to the latest version of the SDK.

> [!NOTE]
> In the SDK version `0.8.0` and later, there are breaking changes in the API from previous versions.

The following diagram shows how the previous architecture - for versions earlier than `0.8.0` - relied heavily on using a REST webserver to manage models and inference like chat completions:

:::image type="content" source="../../media/architecture/current-sdk-architecture.png" alt-text="Diagram of the previous architecture for Foundry Local." lightbox="../../media/architecture/current-sdk-architecture.png":::

The SDK would use a Remote Procedural Call (RPC) to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, the redesigned architecture in version `0.8.0` and later uses a more streamlined approach. The new architecture is as follows:

:::image type="content" source="../../media/architecture/new-sdk-architecture.png" alt-text="Diagram of the new architecture for Foundry Local." lightbox="../../media/architecture/new-sdk-architecture.png":::

In this new architecture:

- Your application is **self-contained**. It doesn't require the Foundry Local CLI to be installed separately on the end user's machine making it easier for you to deploy applications.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other tools that communicate over HTTP. Read [Use chat completions via REST server with Foundry Local](../../how-to/how-to-integrate-with-inference-sdks.md) for details on how to use this feature.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies. Read [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md) for details on how to use this feature.
- On Windows devices, you can use a Windows ML build that handles **hardware acceleration** for models on the device by pulling in the right runtime and drivers.


#### API changes

Version `0.8.0` and later provides a more object-orientated and composable API. The main entry point continues to be the `FoundryLocalManager` class, but instead of being a flat set of methods that operate via static calls to a stateless HTTP API, the SDK now exposes methods on the `FoundryLocalManager` instance that maintain state about the service and models.

| Primitive | Versions < 0.8.0 | Versions >= 0.8.0 |
| --- | --- | --- |
| **Configuration** | N/A | `config = Configuration(...)` |
| **Get Manager** | `mgr = FoundryLocalManager();` | `await FoundryLocalManager.CreateAsync(config, logger);`<br>`var mgr = FoundryLocalManager.Instance;` |
| **Get Catalog** | N/A | `catalog = await mgr.GetCatalogAsync();` |
| **List Models** | `mgr.ListCatalogModelsAsync();` | `catalog.ListModelsAsync();` |
| **Get Model** | `mgr.GetModelInfoAsync("aliasOrModelId");` | `catalog.GetModelAsync(alias: "alias");` |
| **Get Variant** | N/A | `model.SelectedVariant;` |
| **Set Variant** | N/A | `model.SelectVariant();` |
| **Download a model** | `mgr.DownloadModelAsync("aliasOrModelId");` | `model.DownloadAsync()` |
| **Load a model** | `mgr.LoadModelAsync("aliasOrModelId");` | `model.LoadAsync()` |
| **Unload a model** | `mgr.UnloadModelAsync("aliasOrModelId");` | `model.UnloadAsync()` |
| **List loaded models** | `mgr.ListLoadedModelsAsync();` | `catalog.GetLoadedModelsAsync();` |
| **Get model path** | N/A | `model.GetPathAsync()` |
| **Start service** | `mgr.StartServiceAsync();` | `mgr.StartWebServerAsync();` |
| **Stop service** | `mgr.StopServiceAsync();` | `mgr.StopWebServerAsync();` |
| **Cache location** | `mgr.GetCacheLocationAsync();` | `config.ModelCacheDir` |
| **List cached models** | `mgr.ListCachedModelsAsync();` | `catalog.GetCachedModelsAsync();` |

The API allows Foundry Local to be more configurable over the web server, logging, cache location, and model variant selection. For example, the `Configuration` class allows you to set up the application name, logging level, web server URLs, and directories for application data, model cache, and logs:

```csharp
var config = new Configuration
{
    AppName = "app-name",
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

### API reference

- For more details on the Foundry Local C# SDK read [Foundry Local C# SDK API Reference](https://aka.ms/fl-csharp-api-ref).