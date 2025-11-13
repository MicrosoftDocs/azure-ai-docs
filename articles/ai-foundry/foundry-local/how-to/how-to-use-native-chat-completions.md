---
title: Use Native Chat Completions
titleSuffix: Foundry Local
description: This article provides instructions on how to use native chat completions API in Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 10/01/2025
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---
    
# Use Foundry Local native chat completions API

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

The native chat completions API allows you to interact directly with Foundry Local's inference capabilities without needing to start a REST web server. The native API streamlines your application architecture by reducing dependencies and complexity. The native chat completions API uses the same input (request) and output (response) as the OpenAI SDK to ensure compatibility with existing applications and familiarity for developers.

This article explains how to use the native chat completions API in the Foundry Local SDK. 

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) or later installed.

## Set up project

To use Foundry Local in your C# project, you need to set up your project with the appropriate NuGet packages. Depending on your target platform, follow the instructions below to create a new C# console application and add the necessary dependencies.

### [Windows](#tab/windows)

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
    <PackageReference Include="Microsoft.Extensions.Logging" Version="9.0.10" />  </ItemGroup>

</Project>
```

### [macOS/Linux](#tab/xplatform)

First, create a new C# project and navigate into it:

```bash
dotnet new console -n hello-foundry-local
cd hello-foundry-local
```

Next, add the required NuGet packages for Foundry Local and OpenAI SDK:

```bash
dotnet add package Microsoft.AI.Foundry.Local --version 0.8.0
```

---

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local selects the best variant for the model automatically based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
1. Unloads the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

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

Run the code using the following command:

### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r:win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r:win-arm64
```


### [macOS/Linux](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r:osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r:linux-x64
```

---

## Related content

- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)