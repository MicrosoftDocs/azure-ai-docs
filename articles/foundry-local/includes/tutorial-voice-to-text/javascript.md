---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Install packages


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/tutorial-voice-to-text
```

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

## Transcribe an audio file

In this step, you load a speech-to-text model and transcribe an audio file. The Foundry Local SDK uses the `whisper` model alias to select the best Whisper variant for your hardware.

1. Create a file called `app.js`.

1. Add the following code to initialize the SDK, load the speech model, and transcribe an audio file:

    :::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-voice-to-text/app.js" id="transcription":::

    The `createAudioClient` method returns a client for audio operations. The `transcribe` method accepts a file path and returns an object with a `text` property containing the transcribed content.

> [!NOTE]
> Replace `'./meeting-notes.wav'` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Summarize the transcription

Now use a chat model to organize the raw transcription into structured notes. Load the `qwen2.5-0.5b` model and send the transcription as context with a system prompt that instructs the model to produce clean, summarized notes.

Add the following code after the transcription step:

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-voice-to-text/app.js" id="summarization":::

The system prompt shapes the model's output format. By instructing it to produce "organized, concise notes with bullet points," you get structured content rather than a raw paraphrase.

## Combine into a complete app

Create a file named `app.js` and add the following complete code that transcribes an audio file and summarizes the transcription:

:::code language="javascript" source="~/foundry-local-main/samples/js/tutorial-voice-to-text/app.js" id="complete_code":::

> [!NOTE]
> Replace `'./meeting-notes.wav'` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Run the application

Run the note taker:

```bash
node app.js
```

You see output similar to:

```
Downloading speech model: 100.00%
Speech model downloaded.
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
Chat model downloaded.
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

The application first transcribes the audio content, then passes that text to a chat model that extracts key points and organizes them into structured notes.
