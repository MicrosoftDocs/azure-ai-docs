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

### Install packages

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

### Project configuration

The sample repositories include a `.csproj` file that handles platform detection automatically. If you're building a project from scratch, use this configuration as a reference:

:::code language="xml" source="~/foundry-local-main/samples/cs/native-chat-completions/NativeChatCompletions.csproj":::

The following table explains the key project settings:

| Setting | Description |
|---------|-------------|
| `TargetFramework` | On Windows, targets `net9.0-windows10.0.26100` for WinML hardware acceleration. On other platforms, targets `net9.0`. |
| `WindowsAppSDKSelfContained` | Set to `false` to use the system-installed Windows App SDK rather than bundling it. |
| `WindowsPackageType` | Set to `None` to build as an unpackaged desktop app (no MSIX packaging). |
| `EnableCoreMrtTooling` | Set to `false` to disable MRT Core resource tooling, which isn't needed for console apps. |
| `RuntimeIdentifier` | Defaults to the current SDK's runtime identifier, ensuring the correct platform binaries are selected. |
| `Microsoft.AI.Foundry.Local.WinML` | Windows-only package that uses WinML for hardware acceleration and automatic execution provider management. |
| `Microsoft.AI.Foundry.Local` | Cross-platform package for macOS, Linux, and Windows without WinML. |
| `Microsoft.ML.OnnxRuntime.Gpu` / `OnnxRuntimeGenAI.Cuda` | Linux GPU support packages for CUDA-enabled hardware. |

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
