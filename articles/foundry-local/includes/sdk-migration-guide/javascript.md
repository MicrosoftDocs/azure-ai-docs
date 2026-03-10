---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: include
ms.date: 01/22/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## JavaScript SDK Migration Guide

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the JavaScript SDK. In this section, we outline the key changes to help you migrate your applications to the latest version of the SDK.

> [!NOTE]
> In the JavaScript SDK version `0.9.0` and later, there are breaking changes in the API from previous versions.

The following diagram shows how the previous architecture relied heavily on using a REST webserver to manage models and inference like chat completions:

:::image type="content" source="../../media/architecture/current-sdk-architecture.png" alt-text="Diagram of the previous architecture for Foundry Local." lightbox="../../media/architecture/current-sdk-architecture.png":::

The SDK would use a Remote Procedural Call (RPC) to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, the redesigned architecture uses a more streamlined approach. The new architecture is as follows:

:::image type="content" source="../../media/architecture/new-sdk-architecture.png" alt-text="Diagram of the new architecture for Foundry Local." lightbox="../../media/architecture/new-sdk-architecture.png":::

In this new architecture:

- Your application is **self-contained**. It doesn't require the Foundry Local CLI to be installed separately on the end user's machine making it easier for you to deploy applications.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other tools that communicate over HTTP.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies.

#### API changes

The latest version provides a more object-orientated and composable API. The main entry point continues to be the `FoundryLocalManager` class, but instead of being a flat set of methods that operate via static calls to a stateless HTTP API, the SDK now exposes methods on the `FoundryLocalManager` instance that maintain state about the service and models.

| Primitive | Previous Version | Current Version |
| --- | --- | --- |
| **Configuration** | N/A | `config = { appName: "app-name", ... }` |
| **Get Manager** | `mgr = new FoundryLocalManager();` | `mgr = FoundryLocalManager.create(config);` |
| **Get Catalog** | N/A | `catalog = mgr.catalog;` |
| **List Models** | `mgr.listCatalogModels();` | `catalog.getModels();` |
| **Get Model** | `mgr.getModelInfo("aliasOrModelId");` | `catalog.getModel(alias);` |
| **Get Variant** | N/A | `model.id;` |
| **Set Variant** | N/A | `model.selectVariant(modelId);` |
| **Download a model** | `mgr.downloadModel("aliasOrModelId");` | `model.download();` |
| **Load a model** | `mgr.loadModel("aliasOrModelId");` | `model.load();` |
| **Unload a model** | `mgr.unloadModel("aliasOrModelId");` | `model.unload();` |
| **List loaded models** | `mgr.listLoadedModels();` | `catalog.getLoadedModels();` |
| **Get model path** | N/A | `model.path;` |
| **Start service** | `mgr.startService();` | `mgr.startWebService();` |
| **Stop service** | N/A | `mgr.stopWebService();` |
| **Cache location** | `mgr.getCacheLocation();` | `config.modelCacheDir` |
| **List cached models** | `mgr.listCachedModels();` | `catalog.getCachedModels();` |

The API allows Foundry Local to be more configurable over the web server, logging, cache location, and model variant selection. For example, the `config` allows you to set up the application name, logging level, web server URLs, and directories for application data, model cache, and logs:

```js
const config = {
  appName: "app-name",
  logLevel: "info",
  webServiceUrls: "http://127.0.0.1:55588",
  appDataDir: "./foundry_local_data",
  modelCacheDir: "{appDataDir}/model_cache",
  logsDir: "{appDataDir}/logs",
};
```

In the previous version of the Foundry Local JavaScript SDK, you couldn't configure these settings directly through the SDK, which limited your ability to customize the behavior of the service.

### References

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
