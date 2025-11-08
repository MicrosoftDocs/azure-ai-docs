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

![previous architecture](../../media/architecture/current-sdk-architecture.png)

The SDK would use a Remote Procedural Call (RPC) to find Foundry Local CLI executable on the machine, start the webserver, and then communicate with it over HTTP. This architecture had several limitations, including:

- Complexity in managing the webserver lifecycle.
- Challenging deployment: End users needed to have the Foundry Local CLI installed on their machines *and* your application.
- Version management of the CLI and SDK could lead to compatibility issues.

To address these issues, the redesigned architecture in version `0.8.0` and later uses a more streamlined approach. The new architecture is as follows:

![new architecture](../../media/architecture/new-sdk-architecture.png)

In this new architecture:

- Your application is **self-contained**. It doesn't require the Foundry Local CLI to be installed separately on the end user's machine making it easier for you to deploy applications.
- The REST **web server is *optional***. You can still use the web server if you want to integrate with other tools that communicate over HTTP. Read [Use chat completions via REST server with Foundry Local](../../how-to/how-to-integrate-with-inference-sdks.md) for details on how to use this feature.
- The SDK has **native support for chat completions and audio transcriptions**, allowing you to build conversational AI applications with fewer dependencies. Read [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md) for details on how to use this feature.
- On Windows devices, you can use a Windows ML build that handles **hardware acceleration** for models on the device by pulling in the right runtime and drivers.


#### API changes

Version `0.8.0` and later provides a more object-orientated and composable API. The main entry point continues to be the `FoundryLocalManager` class, but instead of being a flat set of methods that operate via static calls to a stateless HTTP API, the SDK now exposes methods on the `FoundryLocalManager` instance that maintain state about the service and models.

| Primitive           | Versions <= 0.7.0 | Versions >= 0.8.0 |
|---------------------|-------------------|-------------------|
| **Configuration**    | N/A | `config = Configuration(...)` |
| **Get Manager**     | `mgr = FoundryLocalManager();`| `await FoundryLocalManager.CreateAsync(config, logger);`<br>`var mgr = FoundryLocalManager.Instance;`  |
| **Get Catalog**   | N/A | `catalog = mgr.GetCatalog();` |
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

To use Foundry Local in your C# project, you need to set up your project with the appropriate NuGet packages. Depending on your target platform, follow the instructions below to create a new C# console application and add the necessary dependencies.

#### [Windows](#tab/windows)

First, create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

Next, open the `hello-foundry-local.csproj` file and modify to the following:

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

The Windows-specific package `Microsoft.AI.Foundry.Local.WinML` includes support for Windows ML hardware acceleration. On initialization, Foundry Local will automatically detect compatible hardware and use it for model inference. If the host machine is missing the correct runtimes and drivers for the available hardware, Foundry Local will automatically download and install them on initialization. You can also override the automatic runtime/driver download behavior and manage the download in your application logic. By keeping the runtimes and drivers separated from the Foundry Local SDK package, we ensure the package size remains small and only the necessary components are installed on the host machine, which will reduce your application's size.

For an up-to-date list of supported hardware accelerators, see [Supported execution providers in Windows ML](https://learn.microsoft.com/windows/ai/new-windows-ml/supported-execution-providers).

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

On macOS, Foundry Local supports hardware acceleration for Apple Silicon CPU and GPU. In the case of GPU, Foundry Local uses [Apple Metal](https://developer.apple.com/metal/) for acceleration via the WebGPU execution provider in ONNX Runtime. The WebGPU execution provider using a library called Dawn that converts from the WebGPU shader language to Metal.

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

On Linux, Foundry Local supports hardware acceleration for CPU and Nvidia CUDA-enabled GPUs. For Nvidia GPUs, you'll need to ensure you have installed the appropriate CUDA drivers and libraries.

---
