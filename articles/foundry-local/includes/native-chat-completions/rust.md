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

## Set up project

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Creates a `FoundryLocalManager` instance with a `FoundryLocalConfig`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a streaming response.
1. Unloads the model.

Replace the contents of `src/main.rs` with the following code:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage, FoundryLocalConfig, FoundryLocalManager,
};
use std::io::Write;
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(FoundryLocalConfig::new("app-name"))?;

    // Get a model using an alias
    let model = manager.catalog().get_model("qwen2.5-0.5b").await?;

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

    // Create a chat client
    let client = model.create_chat_client().temperature(0.7).max_tokens(256);

    // Create chat messages
    let messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestSystemMessage::new("You are a helpful AI assistant.").into(),
        ChatCompletionRequestUserMessage::new("Why is the sky blue?").into(),
    ];

    // Stream the response
    let mut stream = client.complete_streaming_chat(&messages, None).await?;
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if let Some(content) = &chunk.choices[0].message.content {
            print!("{}", content);
            std::io::stdout().flush()?;
        }
    }
    println!();

    // Tidy up - unload the model
    model.unload().await?;

    Ok(())
}
```

Add `anyhow` to your dependencies:

```bash
cargo add anyhow
```

Run the code by using the following command:

```bash
cargo run
```

## Troubleshooting

- **Build errors**: Ensure you have Rust 1.70.0 or later installed. Run `rustup update` to get the latest version.
- **`Model not found`**: Verify the model alias is correct. Use `manager.catalog().get_models().await?` to list available models.
- **Slow first run**: Model downloads can take time the first time you run the app.
