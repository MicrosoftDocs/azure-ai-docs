---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/02/2025
ms.author: samkemp
author: samuel100
---

## Create project

Create a new Rust project and navigate into it:

```bash
cargo new hello-foundry-local
cd hello-foundry-local
```

### Install crates

Install the following Rust crates using Cargo:

```bash
cargo add foundry-local anyhow env_logger serde_json
cargo add reqwest --features json
cargo add tokio --features full
```

## Update the `main.rs` file

The following example demonstrates how to inference using a request to the Foundry Local service. The code initializes the Foundry Local service, loads a model, and generates a response using the `reqwest` library.

Copy-and-paste the following code into the Rust file named `main.rs`:

```rust
use foundry_local::FoundryLocalManager;
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    // Create a FoundryLocalManager instance with default options
    let mut manager = FoundryLocalManager::builder()
        .alias_or_model_id("qwen2.5-0.5b") // Specify the model to use   
        .bootstrap(true) // Start the service if not running
        .build()
        .await?;
    
    // Use the OpenAI compatible API to interact with the model
    let client = reqwest::Client::new();
    let endpoint = manager.endpoint()?;
    let response = client.post(format!("{}/chat/completions", endpoint))
        .header("Content-Type", "application/json")
        .header("Authorization", format!("Bearer {}", manager.api_key()))
        .json(&serde_json::json!({
            "model": manager.get_model_info("qwen2.5-0.5b", true).await?.id,
            "messages": [{"role": "user", "content": "What is the golden ratio?"}],
        }))
        .send()
        .await?;

    let result = response.json::<serde_json::Value>().await?;
    println!("{}", result["choices"][0]["message"]["content"]);
    
    Ok(())
}
```

Run the code using the following command:

```bash
cargo run
```

