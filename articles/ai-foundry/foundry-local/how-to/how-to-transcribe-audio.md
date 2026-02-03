---
title: Transcribe audio files with Foundry Local
titleSuffix: Foundry Local
description: This article provides instructions on how to transcribe audio using Foundry Local.
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
    
# Transcribe recorded audio files with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Use Foundry Local's native audio transcription API to convert a local audio file into text. In this article, you create a C# console application that downloads a Whisper model, loads it, and streams transcription output.

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.
- A local audio file to transcribe.
- Internet access to download models (recommended).
- Azure role-based access control (RBAC): Not applicable.

## Quickstart

Use this snippet to verify that the SDK can initialize and access the local model catalog.

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;
using System.Linq;

var config = new Configuration
{
    AppName = "app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

await FoundryLocalManager.CreateAsync(config, logger);
var manager = FoundryLocalManager.Instance;

var catalog = await manager.GetCatalogAsync();
var models = await catalog.ListModelsAsync();

Console.WriteLine($"Models available: {models.Count()}");
```

This example prints the number of models available for your hardware.

References:

- [Foundry Local SDK reference](../reference/reference-sdk.md)
- [Catalog API reference](../reference/reference-catalog-api.md)

## Samples repository

The sample in this article can be found in the [Foundry Local C# SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](../includes/csharp-project-setup.md)]

## Transcribe an audio file

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` object.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to generate a response.
1. Unloads the model.

Copy and paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;
using System.Linq;

var config = new Configuration
{
    AppName = "app-name",
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

// Get a model using an alias and select the CPU model variant
var model = await catalog.GetModelAsync("whisper-tiny") ?? throw new System.Exception("Model not found");
var modelVariant = model.Variants.First(v => v.Info.Runtime?.DeviceType == DeviceType.CPU);
model.SelectVariant(modelVariant);

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

// Get an audio client
var audioClient = await model.GetAudioClientAsync();

var ct = CancellationToken.None;

// Get a transcription with streaming outputs
var response = audioClient.TranscribeAudioStreamingAsync("Recording.mp3", ct);
await foreach (var chunk in response)
{
    Console.Write(chunk.Text);
    Console.Out.Flush();
}
Console.WriteLine();

// Tidy up - unload the model
await model.UnloadAsync();
```

> [!NOTE]
> You need to replace `"Recording.mp3"` with the path to the audio file that you want to transcribe.

**What to expect**

- On the first run, the app downloads the model and prints the download progress.
- As the transcription streams, the app prints text to the console.

References:

- [Foundry Local SDK reference](../reference/reference-sdk.md)
- [Best practices and troubleshooting guide for Foundry Local](../reference/reference-best-practice.md)

Run the code by using the following command:

### [Windows](#tab/windows)

If your architecture is `x64`, use the following command:

```bash
dotnet run -r:win-x64
```

If your architecture is `arm64`, use the following command:

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

---

## Validate results

1. Confirm the app prints transcription text to the console.
1. If the model downloads on first run, confirm a second run starts faster and doesn't re-download the model.


## Related content

- [Use native chat completions API with Foundry Local](how-to-use-native-chat-completions.md)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)