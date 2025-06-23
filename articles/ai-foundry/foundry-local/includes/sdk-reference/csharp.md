---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 06/09/2025
ms.author: samkemp
author: samuel100
---

## C# SDK Reference

### Installation

To use the Foundry Local C# SDK, you need to install the NuGet package:

```bash
dotnet add package Microsoft.AI.Foundry.Local
```

### A note on aliases

Many methods outlined in this reference have an `aliasOrModelId` parameter in the signature. You can pass into the method either an **alias** or **model ID** as a value. Using an alias will:

- Select the *best model* for the available hardware. For example, if a Nvidia CUDA GPU is available, Foundry Local selects the CUDA model. If a supported NPU is available, Foundry Local selects the NPU model.
- Allow you to use a shorter name without needing to remember the model ID.

> [!TIP]
> We recommend passing into the `aliasOrModelId` parameter an **alias** because when you deploy your application, Foundry Local acquires the best model for the end user's machine at run-time.

### Enumerations

#### `DeviceType`

Represents the type of device used for model execution.

| Value   | Description        |
|---------|--------------------|
| CPU     | CPU device         |
| GPU     | GPU device         |
| NPU     | NPU device         |
| Invalid | Invalid/unknown    |

#### `ExecutionProvider`

Represents the execution provider for model inference.

| Value                  | Description                  |
|------------------------|-----------------------------|
| Invalid                | Invalid provider            |
| CPUExecutionProvider   | CPU execution               |
| WebGpuExecutionProvider| WebGPU execution            |
| CUDAExecutionProvider  | CUDA GPU execution          |
| QNNExecutionProvider   | Qualcomm NPU execution      |

### `FoundryLocalManager` Class

The main entry point for managing models, cache, and the Foundry Local service.

#### Construction

```csharp
var manager = new FoundryLocalManager();
```

#### Properties

| Property         | Type      | Description                                                      |
|------------------|-----------|------------------------------------------------------------------|
| ServiceUri       | `Uri`     | The base URI of the Foundry Local service.                       |
| Endpoint         | `Uri`     | The API endpoint (`ServiceUri` + `/v1`).                         |
| ApiKey           | `string`  | The API key (default: `"OPENAI_API_KEY"`).                       |
| IsServiceRunning | `bool`    | Indicates if the service is running.                             |


#### Service Management

##### Start the service

```csharp
await manager.StartServiceAsync(CancellationToken.None);
```
Starts the Foundry Local service if not already running.

##### Stop the service

```csharp
await manager.StopServiceAsync(CancellationToken.None);
```
Stops the Foundry Local service.

##### Start and load a model (static helper)

```csharp
var manager = await FoundryLocalManager.StartModelAsync("aliasOrModelId");
```

Starts the service and loads the specified model.

#### Catalog Management

##### List all catalog models

```csharp
List<ModelInfo> models = await manager.ListCatalogModelsAsync();
```
Returns all available models in the catalog.

##### Refresh the catalog

```csharp
manager.RefreshCatalog();
```
Clears the cached catalog so it will be reloaded on next access.

##### Get model info by alias or ID

```csharp
ModelInfo? info = await manager.GetModelInfoAsync("aliasOrModelId");
```
Returns model info or `null` if not found.

#### Cache Management

##### Get cache location

```csharp
string cachePath = await manager.GetCacheLocationAsync();
```
Returns the directory path where models are cached.

##### List cached models

```csharp
List<ModelInfo> cached = await manager.ListCachedModelsAsync();
```
Returns models downloaded to the local cache.

#### Model Management

##### Download a model

```csharp
ModelInfo? model = await manager.DownloadModelAsync("aliasOrModelId");
```
Downloads a model to the local cache.

##### Download a model with progress

```csharp
await foreach (var progress in manager.DownloadModelWithProgressAsync("aliasOrModelId"))
{
    // progress.Percentage, progress.Status, etc.
}
```
Streams download progress updates.

##### Load a model

```csharp
ModelInfo loaded = await manager.LoadModelAsync("aliasOrModelId");
```
Loads a model into the inference server.

##### List loaded models

```csharp
List<ModelInfo> loaded = await manager.ListLoadedModelsAsync();
```
Lists all models currently loaded in the service.

##### Unload a model

```csharp
await manager.UnloadModelAsync("aliasOrModelId");
```
Unloads a model from the inference server.

#### Disposal

Implements both `IDisposable` and `IAsyncDisposable` for proper cleanup.

```csharp
manager.Dispose();
// or
await manager.DisposeAsync();
```

### Model Types

This page documents the key data types used by the Foundry Local C# SDK for describing models, downloads, and runtime information.


#### `PromptTemplate`

Represents the prompt template for a model.

| Property   | Type    | Description                        |
|------------|---------|------------------------------------|
| Assistant  | string  | The assistant's prompt template.   |
| Prompt     | string  | The user prompt template.          |

#### `Runtime`

Describes the runtime environment for a model.

| Property          | Type           | Description                       |
|-------------------|----------------|-----------------------------------|
| DeviceType        | `DeviceType`   | The device type (CPU, GPU, etc).  |
| ExecutionProvider | `ExecutionProvider` | The execution provider (CUDA, CPU, etc). |


#### `ModelSettings`

Represents model-specific parameters.

| Property   | Type                | Description                |
|------------|---------------------|----------------------------|
| Parameters | List\<JsonElement\> | Model parameter collection |

### `ModelInfo`

Describes a model in the Foundry Local catalog or cache.

| Property             | Type            | Description                                   |
|----------------------|-----------------|-----------------------------------------------|
| ModelId              | string          | Unique model identifier.                      |
| DisplayName          | string          | Human-readable model name.                    |
| ProviderType         | string          | Provider type (e.g., "CUDA", "CPU").          |
| Uri                  | string          | Download URI for the model.                   |
| Version              | string          | Model version.                                |
| ModelType            | string          | Model type (e.g., "llm", "embedding").        |
| PromptTemplate       | PromptTemplate  | Prompt template for the model.                |
| Publisher            | string          | Publisher of the model.                       |
| Task                 | string          | Task type (e.g., "chat", "completion").       |
| Runtime              | Runtime         | Runtime environment info.                     |
| FileSizeMb           | long            | Model file size in MB.                        |
| ModelSettings        | ModelSettings   | Model-specific settings.                      |
| Alias                | string          | Alias for the model.                          |
| SupportsToolCalling  | bool            | Whether tool-calling is supported.            |
| License              | string          | License identifier.                           |
| LicenseDescription   | string          | License description.                          |
| ParentModelUri       | string          | URI of the parent model, if any.              |


#### `ModelDownloadProgress`

Represents the progress of a model download operation.

| Property     | Type        | Description                                 |
|--------------|-------------|---------------------------------------------|
| Percentage   | double      | Download completion percentage (0-100).     |
| IsCompleted  | bool        | Whether the download is complete.           |
| ModelInfo    | ModelInfo?  | Model info if download completed.           |
| ErrorMessage | string?     | Error message if download failed.           |

**Static methods:**
- `Progress(double percentage)`: Create a progress update.
- `Completed(ModelInfo modelInfo)`: Create a completed progress result.
- `Error(string errorMessage)`: Create an error result.

### Example Usage

```csharp
using Microsoft.AI.Foundry.Local;

var manager = new FoundryLocalManager();
await manager.StartServiceAsync();

var models = await manager.ListCatalogModelsAsync();
var alias = "phi-3.5-mini";

await manager.DownloadModelAsync(alias);
await manager.LoadModelAsync(alias);

var loaded = await manager.ListLoadedModelsAsync();

await manager.UnloadModelAsync(alias);

manager.Dispose();
```
