---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Python SDK Migration Guide

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the Python SDK. In this section, we outline the key changes to help you migrate your applications to the latest version of the SDK.

> [!NOTE]
> In the latest Python SDK version (`1.0.0`), there are breaking changes in the API from previous versions (`<=0.5.1`).

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

The latest version provides a more object-oriented and composable API. The main entry point continues to be the `FoundryLocalManager` class, but the initialization pattern, model management, and inference have all changed significantly.

| Primitive | Previous Version (`foundry-local`) | Current Version (`foundry-local-sdk`) |
| --- | --- | --- |
| **Package** | `pip install foundry-local` | `pip install foundry-local-sdk` |
| **Import** | `from foundry_local import FoundryLocalManager` | `from foundry_local_sdk import Configuration, FoundryLocalManager` |
| **Configuration** | N/A | `config = Configuration(app_name="app-name")` |
| **Get Manager** | `manager = FoundryLocalManager(alias)` | `FoundryLocalManager.initialize(config)`<br>`manager = FoundryLocalManager.instance` |
| **Get Catalog** | N/A | `catalog = manager.catalog` |
| **List Models** | `manager.list_catalog_models()` | `catalog.list_models()` |
| **Get Model** | `manager.get_model_info(alias)` | `catalog.get_model(alias)` |
| **Download a model** | `manager.download_model(alias)` | `model.download(progress_callback)` |
| **Load a model** | `manager.load_model(alias)` | `model.load()` |
| **Unload a model** | `manager.unload_model(alias)` | `model.unload()` |
| **List loaded models** | `manager.list_loaded_models()` | `catalog.get_loaded_models()` |
| **List cached models** | `manager.list_cached_models()` | `catalog.get_cached_models()` |
| **Cache location** | `manager.get_cache_location()` | `config.model_cache_dir` |
| **Start service** | `manager.start_service()` | `manager.start_web_service()` |
| **Service endpoint** | `manager.endpoint` | `manager.urls` |

The API allows Foundry Local to be more configurable over the web server, logging, cache location, and model variant selection. For example, the `Configuration` class allows you to set up the application name, logging level, web server URLs, and directories for application data, model cache, and logs:

```python
from foundry_local_sdk import Configuration

config = Configuration(
    app_name="app-name",
    log_level="info",
    web={"urls": "http://127.0.0.1:55588"},
    model_cache_dir="./foundry_local_data/model_cache",
)
```

### References

- [Use chat completions via REST server](../../how-to/how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
