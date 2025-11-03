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

Foundry Local has a native audio transcription API that allows you to transcribe audio files in the following formats:

- WAV
- MP3
- FLAC


## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) or later installed.

## Create project

Create a new C# project and navigate into it:

```bash
dotnet new console -n audio-transcription
cd audio-transcription
```

### Install NuGet Packages

Install the following NuGet packages into your project folder:

```bash
dotnet add package Microsoft.AI.Foundry.Local
```

## Use audio transcription API

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias. Note: Foundry Local will select the best variant for the model automatically based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to generate a response.
1. Unloads the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;

var config = new Configuration
{
    AppName = "my-audio-app",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
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
var catalog = mgr.GetCatalog();

// Get a model using an alias
var model = await catalog.GetModelAsync("whisper-tiny") ?? throw new System.Exception("Model not found");

// Download and load the variant
await model.DownloadAsync();
await model.LoadAsync();

// Get a chat client
var audioClient = await model.GetAudioClientAsync();

// Get a transcription
var response = await audioClient.TranscribeAudio("Recording.mp3");
Console.WriteLine($"Response: {response}");

// Tidy up - unload the model
await model.UnloadAsync();
```

> [!NOTE]
> You will need to replace `"Recording.mp3"` with the path to your audio file that you want to transcribe.

Run the code using the following command:

```bash
dotnet run
```


## Related content

- [Integrate Foundry Local with 3rd party SDKs](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)