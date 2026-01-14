---
title: Use native chat completions
titleSuffix: Foundry Local
description: This article provides instructions on how to use native chat completions API in Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 01/06/2026
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---
    
# Use Foundry Local native chat completions API

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

The native chat completions API enables you to run chat completions directly in-process, without starting a REST web server.

In this article, you create a console app that downloads a local model, generates a streaming chat response, and then unloads the model.

This article explains how to use the native chat completions API in the Foundry Local SDK. 

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.
- Azure role-based access control (RBAC): Not applicable.

## Samples repository

You can find the sample in this article in the [Foundry Local C# SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Set up project

[!INCLUDE [project-setup](../includes/csharp-project-setup.md)]

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
1. Unloads the model.

Copy and paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = CancellationToken.None;

var config = new Configuration
{
    AppName = "app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance.
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Get the model catalog
var catalog = await mgr.GetCatalogAsync();

// Get a model using an alias
var model = await catalog.GetModelAsync("qwen2.5-0.5b") ?? throw new Exception("Model not found");

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

References:

- [Foundry Local SDK reference](../reference/reference-sdk.md)
- [Foundry Local C# SDK API Reference](https://aka.ms/fl-csharp-api-ref)
- [CancellationToken](/dotnet/api/system.threading.cancellationtoken)

### Optional: list model aliases available on your device

If you don't know which model alias to use, list the models available for your hardware.

```csharp
// List available models and aliases
Console.WriteLine("Available models for your hardware:");
var models = await catalog.ListModelsAsync();
foreach (var availableModel in models)
{
    foreach (var variant in availableModel.Variants)
    {
        Console.WriteLine($"  - Alias: {variant.Alias}");
    }
}
```

References:

- [Foundry Local SDK reference](../reference/reference-sdk.md)

Run the code by using the following command:

### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r:win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r:win-arm64
```


### [Cross-Platform](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r:osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r:linux-x64
```

For Windows, use the following command:

```bash
dotnet run -r:win-x64
```

> [!NOTE]
> If you're targeting Windows, use the Windows-specific instructions under the Windows tab for the best performance and experience.

**What to expect**

- On first run, the app downloads and then loads the model.
- The app prints a streaming response to the prompt.

---

## Troubleshooting

- **Build errors referencing `net9.0`**: Install the [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0), then rebuild the app.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `GetModelAsync`.
- **Slow first run**: Model downloads can take time the first time you run the app.

## Related content

- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)