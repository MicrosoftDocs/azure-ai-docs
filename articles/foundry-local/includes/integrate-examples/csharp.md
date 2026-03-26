---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- Install Foundry Local. For setup steps, see [Get started with Foundry Local](../../get-started.md).
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Set up project

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` that includes the web service configuration. The web service is an OpenAI compliant endpoint.
1. Gets a `Model` object from the model catalog using an alias.

   > [!NOTE]
   > Foundry Local selects the best variant for the model automatically based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Starts the web service.
1. Uses the OpenAI SDK to call the local Foundry web service.
1. Tidies up by stopping the web service and unloading the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;
using OpenAI;
using System.ClientModel;

var config = new Configuration
{
    AppName = "app-name",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
    Web = new Configuration.WebService
    {
        Urls = "http://127.0.0.1:55588"
    }
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

// Start the web service
await mgr.StartWebServiceAsync();

// <<<<<< OPEN AI SDK USAGE >>>>>>
// Use the OpenAI SDK to call the local Foundry web service

ApiKeyCredential key = new ApiKeyCredential("notneeded");
OpenAIClient client = new OpenAIClient(key, new OpenAIClientOptions
{
    Endpoint = new Uri(config.Web.Urls + "/v1"),
});

var chatClient = client.GetChatClient(model.Id);

var completionUpdates = chatClient.CompleteChatStreaming("Why is the sky blue?");

Console.Write($"[ASSISTANT]: ");
foreach (var completionUpdate in completionUpdates)
{
    if (completionUpdate.ContentUpdate.Count > 0)
    {
        Console.Write(completionUpdate.ContentUpdate[0].Text);
    }
}
Console.WriteLine();
// <<<<<< END OPEN AI SDK USAGE >>>>>>

// Tidy up
// Stop the web service and unload model
await mgr.StopWebServiceAsync();
await model.UnloadAsync();
```

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r win-arm64
```


### [Cross-Platform](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r linux-x64
```

For Windows, use the following command:

```bash
dotnet run -r win-x64
```

> [!NOTE]
> If you're targeting Windows, we recommend using the Windows-specific instructions under the Windows tab for optimal performance and experience.

You should see a streaming response printed to your console.

---

## Transcribe audio with Foundry Local (C#)

Foundry Local supports **audio transcription (speech-to-text)** via the Whisper model using the native SDK API. This runs inference in-process without requiring the REST web server.

### Native audio transcription

The following example downloads the Whisper model, loads it, and transcribes an audio file with streaming output:

```csharp
using Microsoft.AI.Foundry.Local;
using Microsoft.Extensions.Logging;

var config = new Configuration { AppName = "foundry_local_samples" };

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

// Get the Whisper model and select the CPU variant
var catalog = await mgr.GetCatalogAsync();
var model = await catalog.GetModelAsync("whisper-tiny")
    ?? throw new Exception("whisper-tiny not found");
var cpuVariant = model.Variants.First(
    v => v.Info.Runtime?.DeviceType == DeviceType.CPU);
model.SelectVariant(cpuVariant);

// Download and load
await model.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading: {progress:F1}%");
    if (progress >= 100f) Console.WriteLine();
});
await model.LoadAsync();

// Transcribe with streaming output
var audioClient = await model.GetAudioClientAsync();
var response = audioClient.TranscribeAudioStreamingAsync(
    "recording.mp3", CancellationToken.None);
await foreach (var chunk in response)
{
    Console.Write(chunk.Text);
}
Console.WriteLine();

await model.UnloadAsync();
```

> [!NOTE]
> Replace `"recording.mp3"` with the path to the audio file you want to transcribe.

### Combine chat and audio in one app

A single `FoundryLocalManager` instance can manage both chat and audio models simultaneously:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;

var config = new Configuration { AppName = "foundry_local_samples" };
await FoundryLocalManager.CreateAsync(config);
var mgr = FoundryLocalManager.Instance;
var catalog = await mgr.GetCatalogAsync();

// Load chat model
var chatModel = await catalog.GetModelAsync("qwen2.5-0.5b")
    ?? throw new Exception("Chat model not found");
await chatModel.DownloadAsync();
await chatModel.LoadAsync();

// Load whisper model (CPU variant)
var whisperModel = await catalog.GetModelAsync("whisper-tiny")
    ?? throw new Exception("Whisper model not found");
var cpuVariant = whisperModel.Variants.First(
    v => v.Info.Runtime?.DeviceType == DeviceType.CPU);
whisperModel.SelectVariant(cpuVariant);
await whisperModel.DownloadAsync();
await whisperModel.LoadAsync();

// Step 1: Transcribe
var audioClient = await whisperModel.GetAudioClientAsync();
var transcriptText = "";
await foreach (var chunk in audioClient.TranscribeAudioStreamingAsync(
    "recording.mp3", CancellationToken.None))
{
    transcriptText += chunk.Text;
}
Console.WriteLine($"You said: {transcriptText}");

// Step 2: Analyze with chat model
var chatClient = await chatModel.GetChatClientAsync();
var messages = new List<ChatMessage>
{
    new() { Role = "system", Content = "Summarize the following text in one sentence." },
    new() { Role = "user", Content = transcriptText }
};
await foreach (var chunk in chatClient.CompleteChatStreamingAsync(messages))
{
    Console.Write(chunk.Choices[0].Message.Content);
}
Console.WriteLine();
```

References:

- [Transcribe audio files with Foundry Local](../../how-to/how-to-transcribe-audio.md)
- [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
