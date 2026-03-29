---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project

[!INCLUDE [C# project setup](../csharp-project-setup.md)]

## Transcribe an audio file

In this step, you load a speech-to-text model and transcribe an audio file. The Foundry Local SDK uses the `whisper` model alias to select the best Whisper variant for your hardware.

1. Open `Program.cs` and replace its contents with the following code to initialize the SDK, load the speech model, and transcribe an audio file:

    ```csharp
    using Microsoft.AI.Foundry.Local;
    using Microsoft.Extensions.Logging;
    using System.Text;

    CancellationToken ct = CancellationToken.None;

    var config = new Configuration
    {
        AppName = "note-taker",
        LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
    };

    using var loggerFactory = LoggerFactory.Create(builder =>
    {
        builder.SetMinimumLevel(
            Microsoft.Extensions.Logging.LogLevel.Information
        );
    });
    var logger = loggerFactory.CreateLogger<Program>();

    // Initialize the singleton instance
    await FoundryLocalManager.CreateAsync(config, logger);
    var mgr = FoundryLocalManager.Instance;
    var catalog = await mgr.GetCatalogAsync();

    // Load the speech-to-text model
    var speechModel = await catalog.GetModelAsync("whisper")
        ?? throw new Exception("Speech model not found");

    await speechModel.DownloadAsync(progress =>
    {
        Console.Write($"\rDownloading speech model: {progress:F2}%");
        if (progress >= 100f) Console.WriteLine();
    });

    await speechModel.LoadAsync();
    Console.WriteLine("Speech model loaded.");

    // Transcribe an audio file
    var audioClient = await speechModel.GetAudioClientAsync();
    var transcriptionText = new StringBuilder();
    var audioResponse = audioClient
        .TranscribeAudioStreamingAsync("meeting-notes.wav", ct);
    await foreach (var chunk in audioResponse)
    {
        Console.Write(chunk.Text);
        transcriptionText.Append(chunk.Text);
    }
    Console.WriteLine();
    ```

    The `GetAudioClientAsync` method returns a client for audio operations. The `TranscribeAudioStreamingAsync` method streams transcription chunks as they become available. You accumulate the text so you can pass it to the chat model in the next step.

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Summarize the transcription

Now use a chat model to organize the raw transcription into structured notes. Load the `phi-3.5-mini` model and send the transcription as context with a system prompt that instructs the model to produce clean, summarized notes.

Add the following code after the transcription step:

```csharp
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;

// Unload the speech model to free memory
await speechModel.UnloadAsync();

// Load the chat model for summarization
var chatModel = await catalog.GetModelAsync("phi-3.5-mini")
    ?? throw new Exception("Chat model not found");

await chatModel.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading chat model: {progress:F2}%");
    if (progress >= 100f) Console.WriteLine();
});

await chatModel.LoadAsync();
Console.WriteLine("Chat model loaded.");

// Summarize the transcription
var chatClient = await chatModel.GetChatClientAsync();
var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a note-taking assistant. Summarize " +
                  "the following transcription into organized, " +
                  "concise notes with bullet points."
    },
    new ChatMessage
    {
        Role = "user",
        Content = transcriptionText.ToString()
    }
};

var chatResponse = await chatClient.CompleteChatAsync(messages, ct);
var summary = chatResponse.Choices[0].Message.Content;
Console.WriteLine($"\nSummary:\n{summary}");

// Unload the chat model
await chatModel.UnloadAsync();
```

The system prompt shapes the model's output format. By instructing it to produce "organized, concise notes with bullet points," you get structured content rather than a raw paraphrase.

## Combine into a complete app

Replace the contents of `Program.cs` with the following complete code that transcribes an audio file and summarizes the transcription:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;
using System.Text;

CancellationToken ct = CancellationToken.None;

var config = new Configuration
{
    AppName = "note-taker",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(
        Microsoft.Extensions.Logging.LogLevel.Information
    );
});
var logger = loggerFactory.CreateLogger<Program>();

// Initialize the singleton instance
await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;
var catalog = await mgr.GetCatalogAsync();

// Load the speech-to-text model
var speechModel = await catalog.GetModelAsync("whisper")
    ?? throw new Exception("Speech model not found");

await speechModel.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading speech model: {progress:F2}%");
    if (progress >= 100f) Console.WriteLine();
});

await speechModel.LoadAsync();
Console.WriteLine("Speech model loaded.");

// Transcribe the audio file
var audioClient = await speechModel.GetAudioClientAsync();
var transcriptionText = new StringBuilder();

Console.WriteLine("\nTranscription:");
var audioResponse = audioClient
    .TranscribeAudioStreamingAsync("meeting-notes.wav", ct);
await foreach (var chunk in audioResponse)
{
    Console.Write(chunk.Text);
    transcriptionText.Append(chunk.Text);
}
Console.WriteLine();

// Unload the speech model to free memory
await speechModel.UnloadAsync();

// Load the chat model for summarization
var chatModel = await catalog.GetModelAsync("phi-3.5-mini")
    ?? throw new Exception("Chat model not found");

await chatModel.DownloadAsync(progress =>
{
    Console.Write($"\rDownloading chat model: {progress:F2}%");
    if (progress >= 100f) Console.WriteLine();
});

await chatModel.LoadAsync();
Console.WriteLine("Chat model loaded.");

// Summarize the transcription into organized notes
var chatClient = await chatModel.GetChatClientAsync();
var messages = new List<ChatMessage>
{
    new ChatMessage
    {
        Role = "system",
        Content = "You are a note-taking assistant. Summarize " +
                  "the following transcription into organized, " +
                  "concise notes with bullet points."
    },
    new ChatMessage
    {
        Role = "user",
        Content = transcriptionText.ToString()
    }
};

var chatResponse = await chatClient.CompleteChatAsync(messages, ct);
var summary = chatResponse.Choices[0].Message.Content;
Console.WriteLine($"\nSummary:\n{summary}");

// Clean up
await chatModel.UnloadAsync();
Console.WriteLine("\nDone. Models unloaded.");
```

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Run the application

Run the note taker:

```bash
dotnet run
```

You see output similar to:

```
Downloading speech model: 100.00%
Speech model loaded.

Transcription:
OK so let's get started with the weekly sync. First, the backend
API is nearly done. Sarah finished the authentication endpoints
yesterday. We still need to add rate limiting before we go to
staging. On the frontend, the dashboard redesign is about seventy
percent complete. Jake, can you walk us through the new layout?
Great. The charts look good. I think we should add a filter for
date range though. For testing, we have about eighty percent code
coverage on the API. We need to write integration tests for the
new auth flow before Friday. Let's plan to do a full regression
test next Tuesday before the release. Any blockers? OK, sounds
like we are in good shape. Let's wrap up.

Downloading chat model: 100.00%
Chat model loaded.

Summary:
- **Backend API**: Authentication endpoints complete. Rate limiting
  still needed before staging deployment.
- **Frontend**: Dashboard redesign 70% complete. New chart layout
  reviewed. Action item: add a date range filter.
- **Testing**: API code coverage at 80%. Integration tests for the
  auth flow due Friday. Full regression test scheduled for next
  Tuesday before release.
- **Status**: No blockers reported. Team is on track.

Done. Models unloaded.
```

The application first transcribes the audio content with streaming output, then passes the accumulated text to a chat model that extracts key points and organizes them into structured notes.
