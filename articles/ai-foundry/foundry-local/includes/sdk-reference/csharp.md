---
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 06/09/2025
ms.author: samkemp
author: samuel100
---

## C# SDK Reference

### Redesign

To improve your ability to ship applications using on-device AI, there are substantial changes to the architecture of the C# SDK in version `0.8.0` and later. In this section, we outline the key changes to help you migrate your applications to the latest version of the SDK.

> [!NOTE]
> In the SDK version `0.8.0` and later, there are breaking changes in the API from previous versions.

#### Architecture changes

The following diagram shows how the previous architecture - for versions earlier than `0.8.0` - relied heavily on using a REST webserver to manage models and inference like chat completions:

:::image type="content" source="../../media/architecture/current-sdk-architecture.png" alt-text="Diagram of the previous architecture for Foundry Local." lightbox="../../media/architecture/current-sdk-architecture.png":::

The SDK would use a Remote Procedural Call (RPC) to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, the redesigned architecture in version `0.8.0` and later uses a more streamlined approach. The new architecture is as follows:

:::image type="content" source="../../media/architecture/new-sdk-architecture.png" alt-text="Diagram of the new architecture for Foundry Local." lightbox="../../media/architecture/new-sdk-architecture.png":::

In this new architecture:

- Your application is **self-contained**. It doesn't require the Foundry Local CLI to be installed separately on the end user's machine making it easier for you to deploy applications.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other tools that communicate over HTTP. Read [Use chat completions via REST server with Foundry Local](../../how-to/how-to-integrate-with-inference-sdks.md) for details on how to use this feature.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies. Read [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md) for details on how to use this feature.
- On Windows devices, you can use a Windows ML build that handles **hardware acceleration** for models on the device by pulling in the right runtime and drivers.


#### API changes

Version `0.8.0` and later provides a more object-orientated and composable API. The main entry point continues to be the `FoundryLocalManager` class, but instead of being a flat set of methods that operate via static calls to a stateless HTTP API, the SDK now exposes methods on the `FoundryLocalManager` instance that maintain state about the service and models.

| Primitive           | Versions < 0.8.0 | Versions >= 0.8.0 |
|---------------------|-------------------|-------------------|
| **Configuration**    | N/A | `config = Configuration(...)` |
| **Get Manager**     | `mgr = FoundryLocalManager();`| `await FoundryLocalManager.CreateAsync(config, logger);`<br>`var mgr = FoundryLocalManager.Instance;`  |
| **Get Catalog**   | N/A | `catalog = await mgr.GetCatalogAsync();` |
| **List Models**            | `mgr.ListCatalogModelsAsync();`| `catalog.ListModelsAsync();`                           |
| **Get Model**  | `mgr.GetModelInfoAsync("aliasOrModelId");`| `catalog.GetModelAsync(alias: "alias");`     |
| **Get Variant**| N/A  | `model.SelectedVariant;` |
| **Set Variant**| N/A  | `model.SelectVariant();` |
| **Download a model**| `mgr.DownloadModelAsync("aliasOrModelId");` | `model.DownloadAsync()`                                                               |
| **Load a model**    | `mgr.LoadModelAsync("aliasOrModelId");`     | `model.LoadAsync()`                                                                   |
| **Unload a Model**  | `mgr.UnloadModelAsync("aliasOrModelId");`   | `model.UnloadAsync()`                                                                 |
| **List Loaded Models**   | `mgr.ListLoadedModelsAsync();`             | `catalog.GetLoadedModelsAsync();`                                                               |
| **Get Model Path**  | N/A                                        | `model.GetPathAsync()`                                                                |
| **Start service**   | `mgr.StartServiceAsync();`                 | `mgr.StartWebServerAsync();` |
| **Stop Service**    | `mgr.StopServiceAsync();`                | `mgr.StopWebServerAsync();`      |
| **Cache Location**  | `mgr.GetCacheLocationAsync();`        | `config.ModelCacheDir`                           |
| **List Cached Models** | `mgr.ListCachedModelsAsync();`     | `catalog.GetCachedModelsAsync();`               |

The API allows Foundry Local to be more configurable over the web server, logging, cache location, and model variant selection. For example, the `Configuration` class allows you to set up the application name, logging level, web server URLs, and directories for application data, model cache, and logs:

```csharp
var config = new Configuration
{
    AppName = "my-app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
    Web = new Configuration.WebService
    {
        Urls = "http://127.0.0.1:55588"
    },
    AppDataDir = "./foundry_local_data",
    ModelCacheDir = "{AppDataDir}/model_cache",
    LogsDir = "{AppDataDir}/logs"
};
```

In the previous version of the Foundry Local C# SDK, you couldn't configure these settings directly through the SDK, which limited your ability to customize the behavior of the service.


### Project setup

To use Foundry Local in your C# project, you need to set up your project with the appropriate NuGet packages. Depending on your target platform, follow these instructions to create a new C# console application and add the necessary dependencies:

#### [Windows](#tab/windows)

First, create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

Next, open the `hello-foundry-local.csproj` file and modify it to include the required WinAppSDK parameters (such as `TargetFramework` and `WindowsAppSDKSelfContained`) and NuGet packages for Foundry Local and OpenAI SDK:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0-windows10.0.26100</TargetFramework>
    <RootNamespace>hello-foundry-local</RootNamespace>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AI.Foundry.Local.WinML" Version="0.8.0" />
    <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />
    <PackageReference Include="OpenAI" Version="2.5.0" />
  </ItemGroup>

</Project>
```

The Windows-specific package `Microsoft.AI.Foundry.Local.WinML` includes support for Windows ML hardware acceleration. On initialization, Foundry Local automatically detects compatible hardware and uses it for model inference. If the host machine is missing the correct runtimes and drivers for the available hardware, Foundry Local automatically downloads and installs them on initialization. You can also override the automatic runtime/driver download behavior and manage the download in your application logic. By keeping the runtimes and drivers separated from the Foundry Local SDK package, we ensure only the necessary components are installed on the host machine, which reduces your application's size.

For an up-to-date list of supported hardware accelerators, see [Supported execution providers in Windows ML](/windows/ai/new-windows-ml/supported-execution-providers).

#### [macOS](#tab/macos)

First, create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

Next, add the required NuGet packages for Foundry Local and OpenAI SDK:

```bash
dotnet add package Microsoft.AI.Foundry.Local --version 0.8.0
dotnet add package OpenAI --version 2.5.0
```

On macOS, Foundry Local supports hardware acceleration for Apple Silicon CPU and GPU (default). Foundry Local uses [Apple Metal](https://developer.apple.com/metal/) for acceleration via the WebGPU execution provider in ONNX Runtime. The WebGPU execution provider uses a library called Dawn that converts from the WebGPU shader language to Metal.

#### [Linux](#tab/linux)

First, create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

Next, add the required NuGet packages for Foundry Local and OpenAI SDK:

```bash
dotnet add package Microsoft.AI.Foundry.Local --version 0.8.0
dotnet add package OpenAI --version 2.5.0
```

On Linux, Foundry Local supports hardware acceleration for CPU and Nvidia CUDA-enabled GPUs. For Nvidia GPUs, you need to install the appropriate CUDA drivers and libraries.

---

### Example usage

After [Project setup](#project-setup), you can use the following example code to get started with Foundry Local:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = new CancellationToken();

var config = new Configuration
{
    AppName = "my-app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Debug
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Debug);
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance.
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Get the model catalog
var catalog = await mgr.GetCatalogAsync();

// List available models
Console.WriteLine("Available models for your hardware:");
var models = await catalog.ListModelsAsync();
foreach (var availableModel in models)
{
    foreach (var variant in availableModel.Variants)
    {
        Console.WriteLine($"  - Alias: {variant.Alias} (Id: {string.Join(", ", variant.Id)})");
    }
}

// Get a model using an alias
var model = await catalog.GetModelAsync("qwen2.5-0.5b") ?? throw new Exception("Model not found");

// is model cached
Console.WriteLine($"Is model cached: {await model.IsCachedAsync()}");

// print out cached models
var cachedModels = await catalog.GetCachedModelsAsync();
Console.WriteLine("Cached models:");
foreach (var cachedModel in cachedModels)
{
    Console.WriteLine($"- {cachedModel.Alias} ({cachedModel.Id})");
}

// Download the model (the method skips download if already cached)
await model.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading model: {progress:F2}%");
    if (progress >= 100f)
    {
        Console.WriteLine();
    }
});

// Load the model
await model.LoadAsync();

// Get a chat client
var chatClient = await model.GetChatClientAsync();

// Create a chat message
List<ChatMessage> messages = new()
{
    new ChatMessage { Role = "user", Content = "Why is the sky blue?" }
};


var streamingResponse = chatClient.CompleteChatStreamingAsync(messages, ct);
await foreach (var chunk in streamingResponse)
{
    Console.Write(chunk.Choices[0].Message.Content);
    Console.Out.Flush();
}
Console.WriteLine();

// Tidy up - unload the model
await model.UnloadAsync();
```

To run the example, execute the following command in your project directory:

### [Windows](#tab/windows)

If your architecture is `x64`, use the following command:

```bash
dotnet run -r:win-x64
```

If your architecture is `arm64`, use the following command:

```bash
dotnet run -r:win-arm64
```


### [macOS](#tab/macos)

For macOS, use the following command:

```bash
dotnet run -r:osx-arm64
```

### [Linux](#tab/linux)

For Linux, use the following command:

```bash
dotnet run -r:linux-x64
```

---

### API reference

- For more details on the Foundry Local C# SDK read [Foundry Local C# SDK API Reference](https://aka.ms/fl-csharp-api-ref).