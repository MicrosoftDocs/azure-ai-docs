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

## Rust SDK Reference

### Project setup

[!INCLUDE [project-setup](../rust-project-setup.md)]

### Quickstart

Use this snippet to verify that the SDK can initialize and access the local model catalog.

```rust
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let manager = FoundryLocalManager::create(FoundryLocalConfig::new("app-name"))?;

    let models = manager.catalog().get_models().await?;
    println!("Models available: {}", models.len());

    Ok(())
}
```

This example prints the number of models available for your hardware.

### Samples

- For sample applications that demonstrate how to use the Foundry Local Rust SDK, see the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

### Configuration

The `FoundryLocalConfig` struct allows you to customize the SDK behavior:

```rust
use foundry_local_sdk::FoundryLocalConfig;

let config = FoundryLocalConfig::new("app-name")
    .with_log_level("info")
    .with_model_cache_dir("./foundry_local_data/model_cache")
    .with_web_urls("http://127.0.0.1:55588");
```

### Core API

| Method | Description |
| --- | --- |
| `FoundryLocalManager::create(config)` | Create a new manager with a `FoundryLocalConfig`. |
| `manager.catalog().get_models().await` | List all available models. |
| `manager.catalog().get_model(alias).await` | Get a model by alias. |
| `manager.catalog().get_cached_models().await` | List models in the local cache. |
| `manager.catalog().get_loaded_models().await` | List models currently loaded. |
| `model.download(callback).await` | Download the model (skips if cached). |
| `model.load().await` | Load the model for inference. |
| `model.unload().await` | Unload the model. |

### Native Chat Completions API

After loading a model, create a chat client with optional settings:

```rust
let client = model.create_chat_client()
    .temperature(0.7)
    .max_tokens(256);
```

| Method | Description |
| --- | --- |
| `client.complete_chat(&messages, tools).await` | Generate a complete chat response. |
| `client.complete_streaming_chat(&messages, tools).await` | Stream chat response chunks. |

Message types: `ChatCompletionRequestSystemMessage`, `ChatCompletionRequestUserMessage`, `ChatCompletionRequestMessage`.

### Native Audio Transcription API

After loading a Whisper model, create an audio client:

```rust
let audio_client = model.create_audio_client();
```

| Method | Description |
| --- | --- |
| `audio_client.transcribe(file_path).await` | Transcribe an audio file. Returns an object with a `text` field. |

References:

- [Transcribe audio files with Foundry Local](../../how-to/how-to-transcribe-audio.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
- [Use chat completions via REST server](../../how-to/how-to-integrate-with-inference-sdks.md)
