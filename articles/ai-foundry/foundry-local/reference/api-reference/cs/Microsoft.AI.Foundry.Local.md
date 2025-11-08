# <a id="Microsoft_AI_Foundry_Local"></a> Namespace Microsoft.AI.Foundry.Local

### Classes

 [OpenAIChatClient.ChatSettings](Microsoft.AI.Foundry.Local.OpenAIChatClient.ChatSettings.md)

Settings controlling chat completion generation. Only the subset supported by Foundry Local.

 [Configuration](Microsoft.AI.Foundry.Local.Configuration.md)

Foundry Local configuration used to initialize the <xref href="Microsoft.AI.Foundry.Local.FoundryLocalManager" data-throw-if-not-resolved="false"></xref> singleton.

 [FoundryLocalException](Microsoft.AI.Foundry.Local.FoundryLocalException.md)

Exception type thrown by the Foundry Local SDK to represent operational or initialization errors.

 [FoundryLocalManager](Microsoft.AI.Foundry.Local.FoundryLocalManager.md)

Entry point for Foundry Local SDK providing initialization, catalog access, model management
and optional web service hosting.

 [Model](Microsoft.AI.Foundry.Local.Model.md)

Represents a logical model grouping multiple downloadable / loadable variants under a shared alias.

 [ModelInfo](Microsoft.AI.Foundry.Local.ModelInfo.md)

Full descriptive metadata for a model variant within the catalog.

 [ModelSettings](Microsoft.AI.Foundry.Local.ModelSettings.md)

Optional settings applied to a model instance (e.g. default parameters).

 [ModelVariant](Microsoft.AI.Foundry.Local.ModelVariant.md)

 [OpenAIAudioClient](Microsoft.AI.Foundry.Local.OpenAIAudioClient.md)

Audio transcription client using an OpenAI compatible API surface implemented via Foundry Local Core.
Supports standard and streaming transcription of audio files.

 [OpenAIChatClient](Microsoft.AI.Foundry.Local.OpenAIChatClient.md)

Chat client using an OpenAI compatible API surface implemented via Foundry Local Core.
Provides convenience methods for standard and streaming chat completions.

 [Parameter](Microsoft.AI.Foundry.Local.Parameter.md)

A single configurable parameter that can influence model behavior.

 [PromptTemplate](Microsoft.AI.Foundry.Local.PromptTemplate.md)

Template segments used to build a prompt for a model. Individual segments are optional.

 [Runtime](Microsoft.AI.Foundry.Local.Runtime.md)

Runtime configuration details describing how the model will execute.

 [Configuration.WebService](Microsoft.AI.Foundry.Local.Configuration.WebService.md)

Configuration settings if the optional web service is used.

### Interfaces

 [ICatalog](Microsoft.AI.Foundry.Local.ICatalog.md)

 [IModel](Microsoft.AI.Foundry.Local.IModel.md)

Common operations for a model variant or model abstraction including caching, loading
and client creation helpers.

### Enums

 [DeviceType](Microsoft.AI.Foundry.Local.DeviceType.md)

Device types supported by the runtime for model execution.

 [LogLevel](Microsoft.AI.Foundry.Local.LogLevel.md)

Logging verbosity levels used by the Foundry Local SDK. Mirrors typical structured logging levels.

