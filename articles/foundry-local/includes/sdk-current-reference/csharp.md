---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/05/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## C# SDK Reference

### Project setup guide

There are two NuGet packages for the Foundry Local SDK - a WinML and a cross-platform package - that have the same API surface but are optimized for different platforms:

- **Windows**: Uses the `Microsoft.AI.Foundry.Local.WinML` package that's specific to Windows applications, which uses the Windows Machine Learning (WinML) framework.
- **Cross-platform**: Uses the `Microsoft.AI.Foundry.Local` package that can be used for cross-platform applications (Windows, Linux, macOS).

Depending on your target platform, follow these instructions to create a new C# application and add the necessary dependencies:

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

### Quickstart

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

### Samples

- For sample applications that demonstrate how to use the Foundry Local C# SDK, see the [Foundry Local C# SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

### API reference

- For more details on the Foundry Local C# SDK read [Foundry Local C# SDK API Reference](https://aka.ms/fl-csharp-api-ref).

### Native Audio Transcription API

The C# SDK includes a native audio client for transcribing audio files on-device using Whisper models. This runs inference in-process without needing the REST web server.

#### Get an audio client

After loading a Whisper model, get an audio client:

```csharp
var audioClient = await model.GetAudioClientAsync();
```

#### Audio transcription methods

| Method | Signature | Description |
| --- | --- | --- |
| `TranscribeAudioStreamingAsync()` | `(string audioFilePath, CancellationToken ct) => IAsyncEnumerable<TranscriptionChunk>` | Streams transcription results chunk by chunk. Each chunk has a `Text` property. |

#### AudioClient settings

| Property | Type | Description |
| --- | --- | --- |
| `Language` | `string` | ISO 639-1 language code (for example, `"en"`). Improves accuracy. |
| `Temperature` | `float` | Sampling temperature (0.0–1.0). Lower values are more deterministic. |

#### Example

```csharp
var audioClient = await model.GetAudioClientAsync();
audioClient.Settings.Language = "en";
audioClient.Settings.Temperature = 0.0f;

await foreach (var chunk in audioClient.TranscribeAudioStreamingAsync(
    "recording.mp3", CancellationToken.None))
{
    Console.Write(chunk.Text);
}
```

References:

- [Transcribe audio files with Foundry Local](../../how-to/how-to-transcribe-audio.md)
