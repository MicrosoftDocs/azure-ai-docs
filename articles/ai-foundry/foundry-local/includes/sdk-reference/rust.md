---
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

- Install Foundry Local and ensure the `foundry` command is available on your `PATH`.
- Use Rust 1.70.0 or later.

### Installation
To use the Foundry Local Rust SDK, add the following to your `Cargo.toml`:

```toml
[dependencies]
foundry-local = "0.1.0"
```

Alternatively, you can add the Foundry Local crate using `cargo`:

```bash
cargo add foundry-local
```

### Quickstart

Use this snippet to verify that the SDK can start the service and read the local catalog.

```rust
use anyhow::Result;
use foundry_local::FoundryLocalManager;

#[tokio::main]
async fn main() -> Result<()> {
  let mut manager = FoundryLocalManager::builder().bootstrap(true).build().await?;

  let models = manager.list_catalog_models().await?;
  println!("Catalog models available: {}", models.len());

  Ok(())
}
```

This example prints a non-zero number when the service is running and the catalog is available.

References:

- [Foundry Local documentation](/azure/ai-foundry/foundry-local/)
- [foundry-local crate docs](https://docs.rs/foundry-local/0.1.0)

### `FoundryLocalManager`

Manager for Foundry Local SDK operations.

#### Fields

- `service_uri: Option<String>` — URI of the Foundry service.
- `client: Option<HttpClient>` — HTTP client for API requests.
- `catalog_list: Option<Vec<FoundryModelInfo>>` — Cached list of catalog models.
- `catalog_dict: Option<HashMap<String, FoundryModelInfo>>` — Cached dictionary of catalog models.
- `timeout: Option<u64>` — Optional HTTP client timeout.

#### Methods

- **`pub fn builder() -> FoundryLocalManagerBuilder`**  
  Create a new builder for `FoundryLocalManager`.

- **`pub fn service_uri(&self) -> Result<&str>`**  
  Get the service URI.  
  **Returns:** URI of the Foundry service.

- **`fn client(&self) -> Result<&HttpClient>`**  
  Get the HTTP client instance.  
  **Returns:** HTTP client.

- **`pub fn endpoint(&self) -> Result<String>`**  
  Get the endpoint for the service.  
  **Returns:** Endpoint URL.

- **`pub fn api_key(&self) -> String`**  
  Get the API key for authentication.  
  **Returns:** API key.

- **`pub fn is_service_running(&mut self) -> bool`**  
  Check if the service is running and set the service URI if found.  
  **Returns:** `true` if running, `false` otherwise.

- **`pub fn start_service(&mut self) -> Result<()>`**  
  Start the Foundry Local service.

- **`pub async fn list_catalog_models(&mut self) -> Result<&Vec<FoundryModelInfo>>`**  
  Get a list of available models in the catalog.

- **`pub fn refresh_catalog(&mut self)`**  
  Refresh the catalog cache.

- **`pub async fn get_model_info(&mut self, alias_or_model_id: &str, raise_on_not_found: bool) -> Result<FoundryModelInfo>`**  
  Get model information by alias or ID.  
  **Arguments:**  
  - `alias_or_model_id`: Alias or Model ID.  
  - `raise_on_not_found`: If true, error if not found.

- **`pub async fn get_cache_location(&self) -> Result<String>`**  
  Get the cache location as a string.

- **`pub async fn list_cached_models(&mut self) -> Result<Vec<FoundryModelInfo>>`**  
  List cached models.

- **`pub async fn download_model(&mut self, alias_or_model_id: &str, token: Option<&str>, force: bool) -> Result<FoundryModelInfo>`**  
  Download a model.  
  **Arguments:**  
  - `alias_or_model_id`: Alias or Model ID.  
  - `token`: Optional authentication token.  
  - `force`: Force re-download if already cached.

- **`pub async fn load_model(&mut self, alias_or_model_id: &str, ttl: Option<i32>) -> Result<FoundryModelInfo>`**  
  Load a model for inference.  
  **Arguments:**  
  - `alias_or_model_id`: Alias or Model ID.  
  - `ttl`: Optional time-to-live in seconds.

- **`pub async fn unload_model(&mut self, alias_or_model_id: &str, force: bool) -> Result<()>`**  
  Unload a model.  
  **Arguments:**  
  - `alias_or_model_id`: Alias or Model ID.  
  - `force`: Force unload even if in use.

- **`pub async fn list_loaded_models(&mut self) -> Result<Vec<FoundryModelInfo>>`**  
  List loaded models.


### `FoundryLocalManagerBuilder`

Builder for creating a `FoundryLocalManager` instance.

#### Fields

- `alias_or_model_id: Option<String>` — Alias or model ID to download and load.
- `bootstrap: bool` — Whether to start the service if not running.
- `timeout_secs: Option<u64>` — HTTP client timeout in seconds.

#### Methods

- **`pub fn new() -> Self`**  
  Create a new builder instance.

- **`pub fn alias_or_model_id(mut self, alias_or_model_id: impl Into<String>) -> Self`**  
  Set the alias or model ID to download and load.

- **`pub fn bootstrap(mut self, bootstrap: bool) -> Self`**  
  Set whether to start the service if not running.

- **`pub fn timeout_secs(mut self, timeout_secs: u64) -> Self`**  
  Set the HTTP client timeout in seconds.

- **`pub async fn build(self) -> Result<FoundryLocalManager>`**  
  Build the `FoundryLocalManager` instance.


### `FoundryModelInfo`

Represents information about a model.

#### Fields

- `alias: String` — The model alias.
- `id: String` — The model ID.
- `version: String` — The model version.
- `runtime: ExecutionProvider` — The execution provider (CPU, CUDA, etc.).
- `uri: String` — The model URI.
- `file_size_mb: i32` — Model file size in MB.
- `prompt_template: serde_json::Value` — Prompt template for the model.
- `provider: String` — Provider name.
- `publisher: String` — Publisher name.
- `license: String` — License type.
- `task: String` — Model task (e.g., text-generation).

#### Methods

- **`from_list_response(response: &FoundryListResponseModel) -> Self`**  
  Creates a `FoundryModelInfo` from a catalog response.

- **`to_download_body(&self) -> serde_json::Value`**  
  Converts the model info to a JSON body for download requests.

#### `ExecutionProvider`

Enum for supported execution providers.

- `CPU`
- `WebGPU`
- `CUDA`
- `QNN`

##### Methods

- **`get_alias(&self) -> String`**  
  Returns a string alias for the execution provider.

#### `ModelRuntime`

Describes the runtime environment for a model.

- `device_type: DeviceType`
- `execution_provider: ExecutionProvider`


