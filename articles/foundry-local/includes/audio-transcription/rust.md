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

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).
- A local audio file to transcribe in a supported format (for example, MP3, WAV, or FLAC).

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Transcribe an audio file

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Creates a `FoundryLocalManager` instance with a `FoundryLocalConfig`.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to transcribe an audio file.
1. Unloads the model.

Replace the contents of `src/main.rs` with the following code:

```rust
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};
use std::io::Write;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(FoundryLocalConfig::new("app-name"))?;

    // Get a model using an alias
    let model = manager.catalog().get_model("whisper-tiny").await?;

    // Download the model (skips download if already cached)
    model
        .download(Some(|progress: f32| {
            print!("\rDownloading model: {:.2}%", progress);
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();

    // Load the model
    model.load().await?;

    // Create an audio client
    let audio_client = model.create_audio_client();

    // Transcribe an audio file
    let transcription = audio_client.transcribe("Recording.mp3").await?;
    println!("{}", transcription.text);

    // Tidy up - unload the model
    model.unload().await?;

    Ok(())
}
```

> [!NOTE]
> Replace `"Recording.mp3"` with the path to the audio file that you want to transcribe.

## Run the application

Run the code by using the following command:

```bash
cargo run
```
