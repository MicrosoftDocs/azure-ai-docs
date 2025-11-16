---
title: Transcribe audio files with Foundry Local
titleSuffix: Foundry Local
description: This article provides instructions on how to transcribe audio using Foundry Local.
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
    
# Transcribe recorded audio files with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

In this article, you learn how to use Foundry Local's native audio transcription API to convert recorded audio files into text. You create a C# console application that downloads a transcription model called Whisper, loads it, and transcribes an audio file using the Whisper model. By the end of this article, you understand how to integrate audio transcription capabilities into your local applications without requiring cloud connectivity.

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) or later installed.

## Samples repository

The sample in this article can be found in the [Foundry Local C# SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

## Use audio transcription API

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias. Note: Foundry Local selects the best variant for the model automatically based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to generate a response.
1. Unloads the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;

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

// Get a model using an alias
var model = await catalog.GetModelAsync("whisper-tiny") ?? throw new System.Exception("Model not found");

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
var audioClient = await model.GetAudioClientAsync();

// get a cancellation token
CancellationToken ct = new CancellationToken();

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
> You'll need to replace `"Recording.mp3"` with the path to your audio file that you want to transcribe. Foundry Local has a native audio transcription API that allows you to transcribe audio files in the following formats:
>
> - WAV
> - MP3
> - FLAC

Run the code using the following command:

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
> If you are targeting Windows, we recommend using the Windows-specific instructions under the Windows tab for optimal performance and experience.

---


## Related content

- [Use native chat completions API with Foundry Local](how-to-use-native-chat-completions.md)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)