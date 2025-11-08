# <a id="Microsoft_AI_Foundry_Local_IModel"></a> Interface IModel

Namespace: [Microsoft.AI.Foundry.Local](Microsoft.AI.Foundry.Local.md)  
Assembly: Microsoft.AI.Foundry.Local.dll  

Common operations for a model variant or model abstraction including caching, loading
and client creation helpers.

```csharp
public interface IModel
```

## Properties

### <a id="Microsoft_AI_Foundry_Local_IModel_Alias"></a> Alias

```csharp
[SuppressMessage("Naming", "CA1716:Identifiers should not match keywords", Justification = "Alias is a suitable name in this context.")]
string Alias { get; }
```

#### Property Value

 [string](https://learn.microsoft.com/dotnet/api/system.string)

### <a id="Microsoft_AI_Foundry_Local_IModel_Id"></a> Id

Unique model identifier.

```csharp
string Id { get; }
```

#### Property Value

 [string](https://learn.microsoft.com/dotnet/api/system.string)

## Methods

### <a id="Microsoft_AI_Foundry_Local_IModel_DownloadAsync_System_Action_System_Single__System_Nullable_System_Threading_CancellationToken__"></a> DownloadAsync\(Action<float\>?, CancellationToken?\)

Download the model to local cache if not already present.

```csharp
Task DownloadAsync(Action<float>? downloadProgress = null, CancellationToken? ct = null)
```

#### Parameters

`downloadProgress` [Action](https://learn.microsoft.com/dotnet/api/system.action\-1)<[float](https://learn.microsoft.com/dotnet/api/system.single)\>?

Optional progress callback for download progress.
Percentage download (0 - 100.0) is reported.

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

### <a id="Microsoft_AI_Foundry_Local_IModel_GetAudioClientAsync_System_Nullable_System_Threading_CancellationToken__"></a> GetAudioClientAsync\(CancellationToken?\)

Get an OpenAI API based AudioClient.

```csharp
Task<OpenAIAudioClient> GetAudioClientAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task\-1)<[OpenAIAudioClient](Microsoft.AI.Foundry.Local.OpenAIAudioClient.md)\>

<xref href="Microsoft.AI.Foundry.Local.OpenAIAudioClient" data-throw-if-not-resolved="false"></xref> instance.

### <a id="Microsoft_AI_Foundry_Local_IModel_GetChatClientAsync_System_Nullable_System_Threading_CancellationToken__"></a> GetChatClientAsync\(CancellationToken?\)

Get an OpenAI API based ChatClient.

```csharp
Task<OpenAIChatClient> GetChatClientAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task\-1)<[OpenAIChatClient](Microsoft.AI.Foundry.Local.OpenAIChatClient.md)\>

<xref href="Microsoft.AI.Foundry.Local.OpenAIChatClient" data-throw-if-not-resolved="false"></xref> instance.

### <a id="Microsoft_AI_Foundry_Local_IModel_GetPathAsync_System_Nullable_System_Threading_CancellationToken__"></a> GetPathAsync\(CancellationToken?\)

Gets the model path if cached.

```csharp
Task<string> GetPathAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task\-1)<[string](https://learn.microsoft.com/dotnet/api/system.string)\>

Path of model directory.

### <a id="Microsoft_AI_Foundry_Local_IModel_IsCachedAsync_System_Nullable_System_Threading_CancellationToken__"></a> IsCachedAsync\(CancellationToken?\)

Is the model cached locally?

```csharp
Task<bool> IsCachedAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task\-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)\>

### <a id="Microsoft_AI_Foundry_Local_IModel_IsLoadedAsync_System_Nullable_System_Threading_CancellationToken__"></a> IsLoadedAsync\(CancellationToken?\)

Is the model currently loaded in memory?

```csharp
Task<bool> IsLoadedAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task\-1)<[bool](https://learn.microsoft.com/dotnet/api/system.boolean)\>

### <a id="Microsoft_AI_Foundry_Local_IModel_LoadAsync_System_Nullable_System_Threading_CancellationToken__"></a> LoadAsync\(CancellationToken?\)

Load the model into memory if not already loaded.

```csharp
Task LoadAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

### <a id="Microsoft_AI_Foundry_Local_IModel_RemoveFromCacheAsync_System_Nullable_System_Threading_CancellationToken__"></a> RemoveFromCacheAsync\(CancellationToken?\)

Remove the model from the local cache.

```csharp
Task RemoveFromCacheAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

### <a id="Microsoft_AI_Foundry_Local_IModel_UnloadAsync_System_Nullable_System_Threading_CancellationToken__"></a> UnloadAsync\(CancellationToken?\)

Unload the model if loaded.

```csharp
Task UnloadAsync(CancellationToken? ct = null)
```

#### Parameters

`ct` [CancellationToken](https://learn.microsoft.com/dotnet/api/system.threading.cancellationtoken)?

Optional cancellation token.

#### Returns

 [Task](https://learn.microsoft.com/dotnet/api/system.threading.tasks.task)

