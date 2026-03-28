---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed.

## Create project

Create a new Rust project and navigate into it:

```bash
cargo new hello-foundry-local
cd hello-foundry-local
```

### Install crates

Install the following Rust crates using Cargo:

```bash
cargo add foundry-local-sdk anyhow serde_json
cargo add reqwest --features json
cargo add tokio --features full
```

## Update the `main.rs` file

The following example demonstrates how to run inference by sending a request to the Foundry Local service. The code initializes the Foundry Local service, loads a model, and generates a response using the `reqwest` library.

Copy-and-paste the following code into the Rust file named `main.rs`:

```rust
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    // Create a FoundryLocalManager instance with web service configuration
    let config = FoundryLocalConfig::new("app-name")
        .with_web_urls("http://localhost:5000");
    let manager = FoundryLocalManager::create(config)?;

    // Get and prepare the model
    let model = manager.catalog().get_model("qwen2.5-0.5b").await?;
    model.download(None).await?;
    model.load().await?;

    // Start the web service
    manager.start_web_service().await?;

    // Use the OpenAI compatible API to interact with the model
    let client = reqwest::Client::new();
    let endpoint = manager.urls()[0].trim_end_matches('/');
    let response = client.post(format!("{}/v1/chat/completions", endpoint))
        .header("Content-Type", "application/json")
        .json(&serde_json::json!({
            "model": model.id(),
            "messages": [{"role": "user", "content": "What is the golden ratio?"}],
        }))
        .send()
        .await?;

    let result = response.json::<serde_json::Value>().await?;
    println!("{}", result["choices"][0]["message"]["content"]);

    Ok(())
}
```

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
cargo run
```

You should see a text response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

