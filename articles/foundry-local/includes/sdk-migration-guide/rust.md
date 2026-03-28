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

## Rust SDK Migration Guide

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the Rust SDK. In this section, we outline the key changes to help you migrate your applications to the latest version of the SDK.

> [!NOTE]
> In the latest Rust SDK version, there are breaking changes in the API from previous versions. The crate name has changed from `foundry-local` to `foundry-local-sdk`.

The following diagram shows how the previous architecture relied heavily on using a REST webserver to manage models and inference like chat completions:

:::image type="content" source="../../media/architecture/current-sdk-architecture.png" alt-text="Diagram of the previous architecture for Foundry Local." lightbox="../../media/architecture/current-sdk-architecture.png":::

The SDK would use a Remote Procedural Call (RPC) to find the Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

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

The latest version provides a more object-oriented and composable API. The builder pattern has been replaced with a configuration-based approach, and model management now uses dedicated `Model` objects.

| Primitive | Previous Version (`foundry-local`) | Current Version (`foundry-local-sdk`) |
| --- | --- | --- |
| **Crate** | `foundry-local` | `foundry-local-sdk` |
| **Configuration** | N/A | `FoundryLocalConfig::new("app-name")` |
| **Get Manager** | `FoundryLocalManager::builder().build().await?` | `FoundryLocalManager::create(config)?` |
| **Get Catalog** | N/A | `manager.catalog()` |
| **List Models** | `manager.list_catalog_models().await?` | `manager.catalog().get_models().await?` |
| **Get Model** | `manager.get_model_info(alias).await?` | `manager.catalog().get_model(alias).await?` |
| **Download a model** | `manager.download_model(alias).await?` | `model.download(callback).await?` |
| **Load a model** | `manager.load_model(alias).await?` | `model.load().await?` |
| **Unload a model** | `manager.unload_model(alias).await?` | `model.unload().await?` |
| **List loaded models** | `manager.list_loaded_models().await?` | `manager.catalog().get_loaded_models().await?` |
| **List cached models** | `manager.list_cached_models().await?` | `manager.catalog().get_cached_models().await?` |
| **Start service** | `manager.start_service()?` | `manager.start_web_service().await?` |
| **Endpoint** | `manager.endpoint()?` | `manager.urls()` |
| **HTTP calls** | `reqwest::Client` (manual REST) | Native SDK: `model.create_chat_client()` |

The new SDK provides native chat and audio clients, eliminating the need for manual HTTP requests in most cases:

```rust
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};

let config = FoundryLocalConfig::new("app-name");
let manager = FoundryLocalManager::create(config)?;

let model = manager.catalog().get_model("qwen2.5-0.5b").await?;
model.download(None).await?;
model.load().await?;

// Native chat client - no HTTP server needed
let client = model.create_chat_client().temperature(0.7).max_tokens(256);
```

### References

- [Use chat completions via REST server](../../how-to/how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
