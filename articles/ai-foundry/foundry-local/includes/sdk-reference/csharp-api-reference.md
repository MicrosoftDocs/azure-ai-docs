---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 06/09/2025
ms.author: samkemp
author: samuel100
---

# Microsoft.AI.Foundry.Local API Reference

## Namespace: Microsoft.AI.Foundry.Local

### Overview

The Microsoft.AI.Foundry.Local namespace provides the core SDK for running AI models locally with Foundry Local.

---

## Classes

### Class: Configuration

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Foundry Local configuration used to initialize the [`Microsoft.AI.Foundry.Local.FoundryLocalManager`](#class-foundrylocalmanager) singleton.

```csharp
public class Configuration
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Configuration](#class-configuration)

#### Properties

##### AdditionalSettings

Additional settings that Foundry Local Core can consume.
Keys and values are strings.

```csharp
public IDictionary<string, string>? AdditionalSettings { get; init; }
```

**Property Value:** [IDictionary](https://learn.microsoft.com/dotnet/api/system.collections.generic.idictionary-2)<[string](https://learn.microsoft.com/dotnet/api/system.string), [string](https://learn.microsoft.com/dotnet/api/system.string)>?

##### AppDataDir

Application data directory.
Default: {home}/.{appname}, where {home} is the user's home directory and {appname} is the AppName value.

```csharp
public string? AppDataDir { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

##### AppName

Your application name. MUST be set to a valid name.

```csharp
public required string AppName { get; set; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### LogLevel

Logging level.
Valid values are: Verbose, Debug, Information, Warning, Error, Fatal.
Default: [`Microsoft.AI.Foundry.Local.LogLevel.Warning`](#enum-loglevel).

```csharp
public LogLevel LogLevel { get; init; }
```

**Property Value:** [LogLevel](#enum-loglevel)

##### LogsDir

Log directory.
Default: {appdata}/logs

```csharp
public string? LogsDir { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

##### ModelCacheDir

Model cache directory.
Default: {appdata}/cache/models, where {appdata} is the AppDataDir value.

```csharp
public string? ModelCacheDir { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

##### Web

Optional configuration for the built-in web service.
NOTE: This is not included in all builds.

```csharp
public Configuration.WebService? Web { get; init; }
```

**Property Value:** [Configuration.WebService](#class-configurationwebservice)?

---

### Class: Configuration.WebService

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Configuration settings if the optional web service is used.

```csharp
public class Configuration.WebService
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Configuration.WebService](#class-configurationwebservice)

#### Properties

##### ExternalUrl

If the web service is running in a separate process, it will be accessed using this URI.
Both processes should be using the same version of the SDK. If a random port is assigned when creating
the web service in the external process the actual port must be provided here.

```csharp
public Uri? ExternalUrl { get; init; }
```

**Property Value:** [Uri](https://learn.microsoft.com/dotnet/api/system.uri)?

##### Urls

Url/s to bind to the web service when [`Microsoft.AI.Foundry.Local.FoundryLocalManager.StartWebServiceAsync()`](#method-startwebserviceasync) is called.
After startup, [`Microsoft.AI.Foundry.Local.FoundryLocalManager.Urls`](#property-urls) will contain the actual URL/s the service is listening on.
Default: 127.0.0.1:0, which binds to a random ephemeral port. Multiple URLs can be specified as a semi-colon separated list.

```csharp
public string? Urls { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

---

### Class: FoundryLocalException

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Exception type thrown by the Foundry Local SDK to represent operational or initialization errors.

```csharp
public class FoundryLocalException : Exception, ISerializable
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Exception](https://learn.microsoft.com/dotnet/api/system.exception) ← 
[FoundryLocalException](#class-foundrylocalexception)

#### Implements

[ISerializable](https://learn.microsoft.com/dotnet/api/system.runtime.serialization.iserializable)

#### Constructors

##### FoundryLocalException(string)

Create a new [FoundryLocalException](#class-foundrylocalexception).

```csharp
public FoundryLocalException(string message)
```

**Parameters:**

- `message` [string](https://learn.microsoft.com/dotnet/api/system.string) - Error message.

##### FoundryLocalException(string, Exception)

Create a new [FoundryLocalException](#class-foundrylocalexception) with an inner exception.

```csharp
public FoundryLocalException(string message, Exception innerException)
```

**Parameters:**

- `message` [string](https://learn.microsoft.com/dotnet/api/system.string) - Error message.
- `innerException` [Exception](https://learn.microsoft.com/dotnet/api/system.exception) - Underlying exception.

---

### Class: FoundryLocalManager

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Entry point for Foundry Local SDK providing initialization, catalog access, model management
and optional web service hosting.

```csharp
public class FoundryLocalManager : IDisposable
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[FoundryLocalManager](#class-foundrylocalmanager)

#### Implements

[IDisposable](https://learn.microsoft.com/dotnet/api/system.idisposable)

#### Properties

##### Instance

Singleton instance. Must call [`Microsoft.AI.Foundry.Local.FoundryLocalManager.CreateAsync()`](#method-createasync) before use.

```csharp
public static FoundryLocalManager Instance { get; }
```

**Property Value:** [FoundryLocalManager](#class-foundrylocalmanager)

##### IsInitialized

Has the manager been successfully initialized?

```csharp
public static bool IsInitialized { get; }
```

**Property Value:** [bool](https://learn.microsoft.com/dotnet/api/system.boolean)

##### Urls

Bound Urls if the web service has been started. Null otherwise.
See [`Microsoft.AI.Foundry.Local.FoundryLocalManager.StartWebServiceAsync()`](#method-startwebserviceasync).

```csharp
public string[]? Urls { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)[]?

#### Methods

##### CreateAsync(Configuration, ILogger, CancellationToken?)

Create the [FoundryLocalManager](#class-foundrylocalmanager) singleton instance.

```csharp
public static Task CreateAsync(Configuration configuration, ILogger logger, CancellationToken? ct = null)
```

**Parameters:**

- `configuration` [Configuration](#class-configuration) - Configuration to use.
- `logger` [ILogger](https://learn.microsoft.com/dotnet/api/microsoft.extensions.logging.ilogger) - Application logger to use.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token for the initialization.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task creating the instance.

##### Dispose(bool)

Dispose managed resources held by the manager.

```csharp
protected virtual void Dispose(bool disposing)
```

**Parameters:**

- `disposing` [bool](https://learn.microsoft.com/dotnet/api/system.boolean) - True when called from Dispose.

##### Dispose()

Dispose the manager instance.

```csharp
public void Dispose()
```

##### EnsureEpsDownloadedAsync(CancellationToken?)

Ensure execution providers are downloaded and registered (WinML builds only).
Subsequent calls are fast after initial download.

```csharp
public Task EnsureEpsDownloadedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### GetCatalogAsync(CancellationToken?)

Get the model catalog instance. Populated on first use.

```csharp
public Task<ICatalog> GetCatalogAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[ICatalog](#interface-icatalog)> - The model catalog.

**Remarks:**

If using a WinML build this may trigger execution provider download if not already done. Call
[`Microsoft.AI.Foundry.Local.FoundryLocalManager.EnsureEpsDownloadedAsync()`](#method-ensureepsdownloadedasync) first to separate these operations.

##### StartWebServiceAsync(CancellationToken?)

Start the optional web service exposing OpenAI compatible endpoints.

```csharp
public Task StartWebServiceAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task completing once service started.

##### StopWebServiceAsync(CancellationToken?)

Stops the web service if started.

```csharp
public Task StopWebServiceAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task completing once service stopped.

---

### Class: Model

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Represents a logical model grouping multiple downloadable / loadable variants under a shared alias.

```csharp
public class Model : IModel
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Model](#class-model)

#### Implements

[IModel](#interface-imodel)

#### Properties

##### Alias

Model alias grouping multiple versions / variants.

```csharp
public string Alias { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Id

Unique Id of the currently selected variant.

```csharp
public string Id { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### SelectedVariant

Currently selected variant used for IModel operations.

```csharp
public ModelVariant SelectedVariant { get; }
```

**Property Value:** [ModelVariant](#class-modelvariant)

##### Variants

All known variants for this model alias.

```csharp
public List<ModelVariant> Variants { get; }
```

**Property Value:** [List](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1)<[ModelVariant](#class-modelvariant)>

#### Methods

##### DownloadAsync(Action<float>?, CancellationToken?)

Download the model to local cache if not already present.

```csharp
public Task DownloadAsync(Action<float>? downloadProgress = null, CancellationToken? ct = null)
```

**Parameters:**

- `downloadProgress` [Action](https://learn.microsoft.com/dotnet/api/system.action-1)<[float](https://learn.microsoft.com/dotnet/api/system.single)>? - Optional progress callback for download progress. Percentage download (0 - 100.0) is reported.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### GetAudioClientAsync(CancellationToken?)

Get an OpenAI API based AudioClient.

```csharp
public Task<OpenAIAudioClient> GetAudioClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIAudioClient](#class-openaiaudioclient)> - OpenAIAudioClient instance.

##### GetChatClientAsync(CancellationToken?)

Get an OpenAI API based ChatClient.

```csharp
public Task<OpenAIChatClient> GetChatClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIChatClient](#class-openaichatclient)> - OpenAIChatClient instance.

##### GetLatestVersion(ModelVariant)

Get the latest version of the specified model variant.

```csharp
public ModelVariant GetLatestVersion(ModelVariant variant)
```

**Parameters:**

- `variant` [ModelVariant](#class-modelvariant) - Model variant.

**Returns:** [ModelVariant](#class-modelvariant) - ModelVariant for latest version. Same as `variant` if that is the latest version.

**Exceptions:**

- [FoundryLocalException](#class-foundrylocalexception) - If variant is not valid for this model.

##### GetPathAsync(CancellationToken?)

Gets the model path if cached.

```csharp
public Task<string> GetPathAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[string](https://learn.microsoft.com/dotnet/api/system.string)> - Path of model directory.

##### IsCachedAsync(CancellationToken?)

Is the currently selected variant cached locally?

```csharp
public Task<bool> IsCachedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)>

##### IsLoadedAsync(CancellationToken?)

Is the currently selected variant loaded in memory?

```csharp
public Task<bool> IsLoadedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)>

##### LoadAsync(CancellationToken?)

Load the model into memory if not already loaded.

```csharp
public Task LoadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### RemoveFromCacheAsync(CancellationToken?)

Remove the model from the local cache.

```csharp
public Task RemoveFromCacheAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### SelectVariant(ModelVariant)

Select a specific model variant by its unique model ID.
The selected variant will be used for [IModel](#interface-imodel) operations.

```csharp
public void SelectVariant(ModelVariant variant)
```

**Parameters:**

- `variant` [ModelVariant](#class-modelvariant)

**Exceptions:**

- [FoundryLocalException](#class-foundrylocalexception) - If variant is not valid for this model.

##### UnloadAsync(CancellationToken?)

Unload the model if loaded.

```csharp
public Task UnloadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

---

### Class: ModelInfo

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Full descriptive metadata for a model variant within the catalog.

```csharp
public record ModelInfo : IEquatable<ModelInfo>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[ModelInfo](#class-modelinfo)

#### Implements

[IEquatable<ModelInfo>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### Alias

Alias grouping multiple versions of the same model.

```csharp
[JsonPropertyName("alias")]
public string Alias { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Cached

True if the model is currently cached locally.

```csharp
[JsonPropertyName("cached")]
public bool Cached { get; init; }
```

**Property Value:** [bool](https://learn.microsoft.com/dotnet/api/system.boolean)

##### CreatedAtUnix

Unix timestamp (seconds) when the model was added to the catalog.

```csharp
[JsonPropertyName("createdAt")]
public long CreatedAtUnix { get; init; }
```

**Property Value:** [long](https://learn.microsoft.com/dotnet/api/system.int64)

##### DisplayName

User friendly display name.

```csharp
[JsonPropertyName("displayName")]
public string DisplayName { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### FileSizeMb

Approximate download size of the model files in megabytes.

```csharp
[JsonPropertyName("fileSizeMb")]
public int FileSizeMb { get; init; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)

##### Id

Globally unique model identifier.

```csharp
[JsonPropertyName("id")]
public string Id { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### License

License identifier string.

```csharp
[JsonPropertyName("license")]
public string License { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### LicenseDescription

Human readable license description.

```csharp
[JsonPropertyName("licenseDescription")]
public string LicenseDescription { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### MaxOutputTokens

Maximum supported output tokens for generation.

```csharp
[JsonPropertyName("maxOutputTokens")]
public long MaxOutputTokens { get; init; }
```

**Property Value:** [long](https://learn.microsoft.com/dotnet/api/system.int64)

##### MinFLVersion

Minimum required Foundry Local version for this model.

```csharp
[JsonPropertyName("minFLVersion")]
public string MinFLVersion { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### ModelSettings

Optional model specific settings.

```csharp
[JsonPropertyName("modelSettings")]
public ModelSettings? ModelSettings { get; init; }
```

**Property Value:** [ModelSettings](#class-modelsettings)?

##### ModelType

Model task / modality type (e.g. chat, audio).

```csharp
[JsonPropertyName("modelType")]
public string ModelType { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Name

Internal model name (typically includes size / architecture).

```csharp
[JsonPropertyName("name")]
public string Name { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### PromptTemplate

Optional prompt template guidance for this model.

```csharp
[JsonPropertyName("promptTemplate")]
public PromptTemplate? PromptTemplate { get; init; }
```

**Property Value:** [PromptTemplate](#class-prompttemplate)?

##### ProviderType

Provider type (e.g. onnx, openai).

```csharp
[JsonPropertyName("providerType")]
public string ProviderType { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Publisher

Publisher or organization name.

```csharp
[JsonPropertyName("publisher")]
public string Publisher { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Runtime

Runtime configuration describing target device and execution provider.

```csharp
[JsonPropertyName("runtime")]
public Runtime Runtime { get; init; }
```

**Property Value:** [Runtime](#class-runtime)

##### SupportsToolCalling

True if the model supports tool calling capabilities.

```csharp
[JsonPropertyName("supportsToolCalling")]
public bool SupportsToolCalling { get; init; }
```

**Property Value:** [bool](https://learn.microsoft.com/dotnet/api/system.boolean)

##### Task

Primary task supported by the model (e.g. completion, transcription).

```csharp
[JsonPropertyName("task")]
public string Task { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Uri

Source URI for the model artifacts.

```csharp
[JsonPropertyName("uri")]
public string Uri { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Version

Integer version of the model.

```csharp
[JsonPropertyName("version")]
public int Version { get; init; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)

---

### Class: ModelSettings

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Optional settings applied to a model instance (e.g. default parameters).

```csharp
public record ModelSettings : IEquatable<ModelSettings>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[ModelSettings](#class-modelsettings)

#### Implements

[IEquatable<ModelSettings>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### Parameters

Collection of parameters for the model or null if none are defined.

```csharp
[JsonPropertyName("parameters")]
public Parameter[]? Parameters { get; set; }
```

**Property Value:** [Parameter](#class-parameter)[]?

---

### Class: ModelVariant

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

```csharp
public class ModelVariant : IModel
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[ModelVariant](#class-modelvariant)

#### Implements

[IModel](#interface-imodel)

#### Properties

##### Alias

Alias grouping related variants.

```csharp
public string Alias { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Id

Unique model identifier.

```csharp
public string Id { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Info

Full metadata record for this variant.

```csharp
public ModelInfo Info { get; }
```

**Property Value:** [ModelInfo](#class-modelinfo)

##### Version

Parsed version number (falling back to 0 if unavailable).

```csharp
public int Version { get; init; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)

#### Methods

##### DownloadAsync(Action<float>?, CancellationToken?)

Download the model files from the server.

```csharp
public Task DownloadAsync(Action<float>? downloadProgress = null, CancellationToken? ct = null)
```

**Parameters:**

- `downloadProgress` [Action](https://learn.microsoft.com/dotnet/api/system.action-1)<[float](https://learn.microsoft.com/dotnet/api/system.single)>? - Optional progress callback.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task representing the asynchronous operation.

##### GetAudioClientAsync(CancellationToken?)

Get an OpenAI audio client for the model.

```csharp
public Task<OpenAIAudioClient> GetAudioClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIAudioClient](#class-openaiaudioclient)> - Task that resolves to an OpenAIAudioClient instance.

##### GetChatClientAsync(CancellationToken?)

Get an OpenAI chat client for the model.

```csharp
public Task<OpenAIChatClient> GetChatClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIChatClient](#class-openaichatclient)> - Task that resolves to an OpenAIChatClient instance.

##### GetPathAsync(CancellationToken?)

Get the file system path where the model is cached.

```csharp
public Task<string> GetPathAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[string](https://learn.microsoft.com/dotnet/api/system.string)> - Task that resolves to the model path string.

##### IsCachedAsync(CancellationToken?)

Check if the model is cached on the file system.

```csharp
public Task<bool> IsCachedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)> - Task that resolves to true if the model is cached, false otherwise.

##### IsLoadedAsync(CancellationToken?)

Check if the model is currently loaded in the runtime.

```csharp
public Task<bool> IsLoadedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)> - Task that resolves to true if the model is loaded, false otherwise.

##### LoadAsync(CancellationToken?)

Load the model into the runtime for inference.

```csharp
public Task LoadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task representing the asynchronous operation.

##### RemoveFromCacheAsync(CancellationToken?)

Remove the model files from the cache.

```csharp
public Task RemoveFromCacheAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task representing the asynchronous operation.

##### UnloadAsync(CancellationToken?)

Unload the model from the runtime.

```csharp
public Task UnloadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task) - Task representing the asynchronous operation.

---

### Class: OpenAIAudioClient

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Audio transcription client using an OpenAI compatible API surface implemented via Foundry Local Core.
Supports standard and streaming transcription of audio files.

```csharp
public class OpenAIAudioClient
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[OpenAIAudioClient](#class-openaiaudioclient)

#### Methods

##### TranscribeAudioAsync(string, CancellationToken?)

Transcribe audio from a file.

```csharp
public Task<AudioCreateTranscriptionResponse> TranscribeAudioAsync(string audioFilePath, CancellationToken? ct = null)
```

**Parameters:**

- `audioFilePath` [string](https://learn.microsoft.com/dotnet/api/system.string) - Path to the file containing audio recording. Supported formats depend on the underlying model/runtime.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<AudioCreateTranscriptionResponse> - Transcription response.

##### TranscribeAudioStreamingAsync(string, CancellationToken)

Transcribe audio from a file with streamed output.

```csharp
public IAsyncEnumerable<AudioCreateTranscriptionResponse> TranscribeAudioStreamingAsync(string audioFilePath, CancellationToken ct)
```

**Parameters:**

- `audioFilePath` [string](https://learn.microsoft.com/dotnet/api/system.string) - Path to the file containing audio recording. Supported formats depend on the underlying model/runtime.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken) - Cancellation token.

**Returns:** [IAsyncEnumerable](https://learn.microsoft.com/dotnet/api/system.collections.generic.iasyncenumerable-1)<AudioCreateTranscriptionResponse> - An asynchronous enumerable of transcription responses.

---

### Class: OpenAIChatClient

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Chat client using an OpenAI compatible API surface implemented via Foundry Local Core.
Provides convenience methods for standard and streaming chat completions.

```csharp
public class OpenAIChatClient
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[OpenAIChatClient](#class-openaichatclient)

#### Properties

##### Settings

Mutable settings applied on each request.

```csharp
public OpenAIChatClient.ChatSettings Settings { get; }
```

**Property Value:** [OpenAIChatClient.ChatSettings](#class-openaichatclientchatsettings)

#### Methods

##### CompleteChatAsync(IEnumerable<ChatMessage>, CancellationToken?)

Execute a chat completion request.
To continue a conversation, add prior response messages and new prompt to the messages list.

```csharp
public Task<ChatCompletionCreateResponse> CompleteChatAsync(IEnumerable<ChatMessage> messages, CancellationToken? ct = null)
```

**Parameters:**

- `messages` [IEnumerable](https://learn.microsoft.com/dotnet/api/system.collections.generic.ienumerable-1)<ChatMessage> - Chat messages including system / user / assistant roles.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<ChatCompletionCreateResponse> - Chat completion response.

##### CompleteChatStreamingAsync(IEnumerable<ChatMessage>, CancellationToken)

Execute a chat completion request with streamed output.
To continue a conversation, add prior response messages and new prompt to the messages list.

```csharp
public IAsyncEnumerable<ChatCompletionCreateResponse> CompleteChatStreamingAsync(IEnumerable<ChatMessage> messages, CancellationToken ct)
```

**Parameters:**

- `messages` [IEnumerable](https://learn.microsoft.com/dotnet/api/system.collections.generic.ienumerable-1)<ChatMessage> - Chat messages including system / user / assistant roles.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken) - Cancellation token.

**Returns:** [IAsyncEnumerable](https://learn.microsoft.com/dotnet/api/system.collections.generic.iasyncenumerable-1)<ChatCompletionCreateResponse> - Async enumerable producing incremental chat completion responses.

---

### Class: OpenAIChatClient.ChatSettings

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Settings controlling chat completion generation. Only the subset supported by Foundry Local.

```csharp
public record OpenAIChatClient.ChatSettings : IEquatable<OpenAIChatClient.ChatSettings>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[OpenAIChatClient.ChatSettings](#class-openaichatclientchatsettings)

#### Implements

[IEquatable<OpenAIChatClient.ChatSettings>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### FrequencyPenalty

Penalizes repeated tokens.

```csharp
public float? FrequencyPenalty { get; set; }
```

**Property Value:** [float](https://learn.microsoft.com/dotnet/api/system.single)?

##### MaxTokens

Maximum number of output tokens to generate.

```csharp
public int? MaxTokens { get; set; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)?

##### N

Number of parallel completions to request.

```csharp
public int? N { get; set; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)?

##### PresencePenalty

Penalizes new tokens based on whether they appear in the existing text.

```csharp
public float? PresencePenalty { get; set; }
```

**Property Value:** [float](https://learn.microsoft.com/dotnet/api/system.single)?

##### RandomSeed

Optional random seed for deterministic sampling.

```csharp
public int? RandomSeed { get; set; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)?

##### Temperature

Sampling temperature. Higher values increase randomness.

```csharp
public float? Temperature { get; set; }
```

**Property Value:** [float](https://learn.microsoft.com/dotnet/api/system.single)?

##### TopK

Top-K sampling parameter.

```csharp
public int? TopK { get; set; }
```

**Property Value:** [int](https://learn.microsoft.com/dotnet/api/system.int32)?

##### TopP

Top-P (nucleus) sampling parameter.

```csharp
public float? TopP { get; set; }
```

**Property Value:** [float](https://learn.microsoft.com/dotnet/api/system.single)?

---

### Class: Parameter

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

A single configurable parameter that can influence model behavior.

```csharp
public record Parameter : IEquatable<Parameter>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Parameter](#class-parameter)

#### Implements

[IEquatable<Parameter>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### Name

Parameter name.

```csharp
public required string Name { get; set; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Value

Optional parameter value as string.

```csharp
public string? Value { get; set; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

---

### Class: PromptTemplate

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Template segments used to build a prompt for a model. Individual segments are optional.

```csharp
public record PromptTemplate : IEquatable<PromptTemplate>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[PromptTemplate](#class-prompttemplate)

#### Implements

[IEquatable<PromptTemplate>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### Assistant

Assistant response segment used when constructing multi‑turn prompts.

```csharp
[JsonPropertyName("assistant")]
public string Assistant { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Prompt

Raw prompt text passed to the model.

```csharp
[JsonPropertyName("prompt")]
public string Prompt { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### System

Optional system instruction segment.

```csharp
[JsonPropertyName("system")]
public string? System { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

##### User

Optional user message segment.

```csharp
[JsonPropertyName("user")]
public string? User { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)?

---

### Class: Runtime

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Runtime configuration details describing how the model will execute.

```csharp
public record Runtime : IEquatable<Runtime>
```

#### Inheritance

[object](https://learn.microsoft.com/dotnet/api/system.object) ← 
[Runtime](#class-runtime)

#### Implements

[IEquatable<Runtime>](https://learn.microsoft.com/dotnet/api/system.iequatable-1)

#### Properties

##### DeviceType

Device type the model will run on.

```csharp
[JsonPropertyName("deviceType")]
public DeviceType DeviceType { get; init; }
```

**Property Value:** [DeviceType](#enum-devicetype)

##### ExecutionProvider

Execution provider name (e.g. cuda, directml, webgpu). Open‑ended string.

```csharp
[JsonPropertyName("executionProvider")]
public string ExecutionProvider { get; init; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

---

## Interfaces

### Interface: ICatalog

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

```csharp
public interface ICatalog
```

#### Properties

##### Name

The catalog name.

```csharp
string Name { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

#### Methods

##### GetCachedModelsAsync(CancellationToken?)

Get a list of currently downloaded models from the model cache.

```csharp
Task<List<ModelVariant>> GetCachedModelsAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional CancellationToken.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[List](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1)<[ModelVariant](#class-modelvariant)>> - List of ModelVariant instances.

##### GetLoadedModelsAsync(CancellationToken?)

Get a list of the currently loaded models.

```csharp
Task<List<ModelVariant>> GetLoadedModelsAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional CancellationToken.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[List](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1)<[ModelVariant](#class-modelvariant)>> - List of ModelVariant instances.

##### GetModelAsync(string, CancellationToken?)

Lookup a model by its alias.

```csharp
Task<Model?> GetModelAsync(string modelAlias, CancellationToken? ct = null)
```

**Parameters:**

- `modelAlias` [string](https://learn.microsoft.com/dotnet/api/system.string) - Model alias.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional CancellationToken.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[Model](#class-model)?> - Model if found.

##### GetModelVariantAsync(string, CancellationToken?)

Lookup a model variant by its unique model id.

```csharp
Task<ModelVariant?> GetModelVariantAsync(string modelId, CancellationToken? ct = null)
```

**Parameters:**

- `modelId` [string](https://learn.microsoft.com/dotnet/api/system.string) - Model id.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional CancellationToken.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[ModelVariant](#class-modelvariant)?> - Model variant if found.

##### ListModelsAsync(CancellationToken?)

List the available models in the catalog.

```csharp
Task<List<Model>> ListModelsAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional CancellationToken.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[List](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1)<[Model](#class-model)>> - List of Model instances.

---

### Interface: IModel

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Common operations for a model variant or model abstraction including caching, loading
and client creation helpers.

```csharp
public interface IModel
```

#### Properties

##### Alias

```csharp
[SuppressMessage("Naming", "CA1716:Identifiers should not match keywords", Justification = "Alias is a suitable name in this context.")]
string Alias { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

##### Id

Unique model identifier.

```csharp
string Id { get; }
```

**Property Value:** [string](https://learn.microsoft.com/dotnet/api/system.string)

#### Methods

##### DownloadAsync(Action<float>?, CancellationToken?)

Download the model to local cache if not already present.

```csharp
Task DownloadAsync(Action<float>? downloadProgress = null, CancellationToken? ct = null)
```

**Parameters:**

- `downloadProgress` [Action](https://learn.microsoft.com/dotnet/api/system.action-1)<[float](https://learn.microsoft.com/dotnet/api/system.single)>? - Optional progress callback for download progress. Percentage download (0 - 100.0) is reported.
- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### GetAudioClientAsync(CancellationToken?)

Get an OpenAI API based AudioClient.

```csharp
Task<OpenAIAudioClient> GetAudioClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIAudioClient](#class-openaiaudioclient)> - OpenAIAudioClient instance.

##### GetChatClientAsync(CancellationToken?)

Get an OpenAI API based ChatClient.

```csharp
Task<OpenAIChatClient> GetChatClientAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[OpenAIChatClient](#class-openaichatclient)> - OpenAIChatClient instance.

##### GetPathAsync(CancellationToken?)

Gets the model path if cached.

```csharp
Task<string> GetPathAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[string](https://learn.microsoft.com/dotnet/api/system.string)> - Path of model directory.

##### IsCachedAsync(CancellationToken?)

Is the model cached locally?

```csharp
Task<bool> IsCachedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)>

##### IsLoadedAsync(CancellationToken?)

Is the model currently loaded in memory?

```csharp
Task<bool> IsLoadedAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)>

##### LoadAsync(CancellationToken?)

Load the model into memory if not already loaded.

```csharp
Task LoadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### RemoveFromCacheAsync(CancellationToken?)

Remove the model from the local cache.

```csharp
Task RemoveFromCacheAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

##### UnloadAsync(CancellationToken?)

Unload the model if loaded.

```csharp
Task UnloadAsync(CancellationToken? ct = null)
```

**Parameters:**

- `ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)? - Optional cancellation token.

**Returns:** [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

---

## Enums

### Enum: DeviceType

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Device types supported by the runtime for model execution.

```csharp
[JsonConverter(typeof(JsonStringEnumConverter<DeviceType>))]
public enum DeviceType
```

#### Fields

- `CPU = 1` - Standard system CPU.
- `GPU = 2` - Discrete or integrated GPU device.
- `Invalid = 0` - Invalid / unspecified device type.
- `NPU = 3` - Neural Processing Unit.

---

### Enum: LogLevel

**Namespace:** [Microsoft.AI.Foundry.Local](#namespace-microsoftaifoundrylocal)  
**Assembly:** Microsoft.AI.Foundry.Local.dll  

Logging verbosity levels used by the Foundry Local SDK. Mirrors typical structured logging levels.

```csharp
public enum LogLevel
```

#### Fields

- `Debug = 1` - Debug level diagnostic messages.
- `Error = 4` - Recoverable error events.
- `Fatal = 5` - Fatal errors causing operation termination.
- `Information = 2` - Information messages describing normal operations.
- `Verbose = 0` - Highly verbose diagnostic output.
- `Warning = 3` - Warning events indicating potential issues.
