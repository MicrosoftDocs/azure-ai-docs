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

## Rust SDK reference

The Rust SDK for Foundry Local provides a way to manage models, control the cache, and interact with the Foundry Local service.

### Prerequisites

- Use Rust 1.70.0 or later.

### Installation
To use the Foundry Local Rust SDK, add the following to your `Cargo.toml`:

```toml
[dependencies]
foundry-local-sdk = "0.1.0"
```

Alternatively, you can add the Foundry Local crate using `cargo`:

```bash
cargo add foundry-local-sdk
```

### Quickstart

Use this snippet to verify that the SDK can initialize and read the local catalog.

```rust
use anyhow::Result;
use foundry_local_sdk::{FoundryLocalConfig, FoundryLocalManager};

#[tokio::main]
async fn main() -> Result<()> {
    let config = FoundryLocalConfig::new("app-name");
    let manager = FoundryLocalManager::create(config)?;

    let models = manager.catalog().list_models().await?;
    println!("Catalog models available: {}", models.len());

    Ok(())
}
```

This example prints a non-zero number when the catalog is available.

References:

- [Foundry Local documentation](/azure/ai-foundry/foundry-local/)
- [foundry-local-sdk crate docs](https://docs.rs/foundry-local-sdk/0.1.0)

### `FoundryLocalManager`

Manager for Foundry Local SDK operations.

#### Methods

- **`pub fn create(config: FoundryLocalConfig) -> Result<FoundryLocalManager>`**  
  Create a new `FoundryLocalManager` instance with the given configuration.  
  **Arguments:**  
  - `config`: Configuration object created with `FoundryLocalConfig::new("app-name")`.

- **`pub fn catalog(&self) -> &Catalog`**  
  Get the catalog instance for model operations.  
  **Returns:** Reference to the catalog.

- **`pub fn urls(&self) -> &[String]`**  
  Get the list of web service URLs.  
  **Returns:** Slice of URL strings.

- **`pub async fn start_web_service(&self) -> Result<()>`**  
  Start the web service for HTTP-based inference.

### `FoundryLocalConfig`

Configuration for creating a `FoundryLocalManager` instance.

#### Methods

- **`pub fn new(app_name: impl Into<String>) -> Self`**  
  Create a new configuration with the given application name.

- **`pub fn with_web_urls(self, urls: impl Into<String>) -> Self`**  
  Set the web service URL for HTTP-based inference.

### `Catalog`

Provides methods for discovering and managing models.

#### Methods

- **`pub async fn list_models(&self) -> Result<Vec<Model>>`**  
  List all available models in the catalog.

- **`pub async fn get_model(&self, alias_or_model_id: &str) -> Result<Model>`**  
  Get a model by alias or ID.  
  **Arguments:**  
  - `alias_or_model_id`: Alias or Model ID.

### `Model`

Represents a model in the catalog.

#### Methods

- **`pub fn id(&self) -> &str`**  
  Get the model ID.

- **`pub async fn download(&self, progress_callback: Option<impl Fn(f64)>) -> Result<()>`**  
  Download the model to the local cache.  
  **Arguments:**  
  - `progress_callback`: Optional callback receiving download progress as a percentage.

- **`pub async fn load(&self) -> Result<()>`**  
  Load the model for inference.

- **`pub async fn unload(&self) -> Result<()>`**  
  Unload the model from the inference server.


