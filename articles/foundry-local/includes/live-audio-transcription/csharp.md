---
author: samuel100
ms.author: samkemp
ms.reviewer: samkemp
ms.topic: include
ms.date: 07/23/2025
---

## Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.
- A working microphone connected to your computer.

## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/csharp/foundry-local/live-audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../csharp-project-setup.md)]

Install the [NAudio](https://www.nuget.org/packages/NAudio) package for microphone capture:

```bash
dotnet add package NAudio
```

## Live transcribe from microphone

The following code initializes the Foundry Local SDK, loads a streaming speech model, captures audio from your microphone using NAudio, and streams it to the live transcription API. Partial results appear as you speak, and final results are printed on a new line.

Copy and paste the following code into `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/csharp/foundry-local/live-audio-transcription/Program.cs":::

The `CreateLiveTranscriptionSession` method returns a session that accepts raw Pulse-code modulation (PCM) audio and yields transcription results as an async stream. NAudio's `WaveInEvent` captures microphone audio at 16-kHz mono—the format the session expects.

Run the application:

```bash
dotnet run
```

Speak into your microphone. You see real-time transcription output:

```
Listening... (press Ctrl+C to stop)
Hello, this is a test of the live transcription feature.
It transcribes audio from the microphone in real time.
```

Press **Ctrl+C** to stop recording. The model finishes processing any remaining audio and the application exits.
