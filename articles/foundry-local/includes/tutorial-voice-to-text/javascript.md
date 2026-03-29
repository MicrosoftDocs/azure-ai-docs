---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

## Transcribe an audio file

In this step, you load a speech-to-text model and transcribe an audio file. The Foundry Local SDK uses the `whisper` model alias to select the best Whisper variant for your hardware.

1. Create a file called `app.js`.

1. Add the following code to initialize the SDK, load the speech model, and transcribe an audio file:

    ```javascript
    import { FoundryLocalManager } from 'foundry-local-sdk';

    // Initialize the Foundry Local SDK
    const manager = FoundryLocalManager.create({
        appName: 'note-taker',
        logLevel: 'info'
    });

    // Load the speech-to-text model
    const speechModel = await manager.catalog.getModel('whisper');
    await speechModel.download((progress) => {
        process.stdout.write(
            `\rDownloading speech model: ${progress.toFixed(2)}%`
        );
    });
    console.log('\nSpeech model downloaded.');

    await speechModel.load();
    console.log('Speech model loaded.');

    // Transcribe an audio file
    const audioClient = speechModel.createAudioClient();
    const transcription = await audioClient.transcribe(
        './meeting-notes.wav'
    );
    console.log(`\nTranscription:\n${transcription.text}`);

    // Unload the speech model to free memory
    await speechModel.unload();
    ```

    The `createAudioClient` method returns a client for audio operations. The `transcribe` method accepts a file path and returns an object with a `text` property containing the transcribed content.

> [!NOTE]
> Replace `'./meeting-notes.wav'` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Summarize the transcription

Now use a chat model to organize the raw transcription into structured notes. Load the `phi-3.5-mini` model and send the transcription as context with a system prompt that instructs the model to produce clean, summarized notes.

Add the following code after the transcription step:

```javascript
// Load the chat model for summarization
const chatModel = await manager.catalog.getModel('phi-3.5-mini');
await chatModel.download((progress) => {
    process.stdout.write(
        `\rDownloading chat model: ${progress.toFixed(2)}%`
    );
});
console.log('\nChat model downloaded.');

await chatModel.load();
console.log('Chat model loaded.');

// Summarize the transcription
const chatClient = chatModel.createChatClient();
const messages = [
    {
        role: 'system',
        content: 'You are a note-taking assistant. Summarize ' +
                 'the following transcription into organized, ' +
                 'concise notes with bullet points.'
    },
    {
        role: 'user',
        content: transcription.text
    }
];

const response = await chatClient.completeChat(messages);
const summary = response.choices[0]?.message?.content;
console.log(`\nSummary:\n${summary}`);

// Unload the chat model
await chatModel.unload();
```

The system prompt shapes the model's output format. By instructing it to produce "organized, concise notes with bullet points," you get structured content rather than a raw paraphrase.

## Combine into a complete app

Create a file named `app.js` and add the following complete code that transcribes an audio file and summarizes the transcription:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';

// Initialize the Foundry Local SDK
const manager = FoundryLocalManager.create({
    appName: 'note-taker',
    logLevel: 'info'
});

// Load the speech-to-text model
const speechModel = await manager.catalog.getModel('whisper');
await speechModel.download((progress) => {
    process.stdout.write(
        `\rDownloading speech model: ${progress.toFixed(2)}%`
    );
});
console.log('\nSpeech model downloaded.');

await speechModel.load();
console.log('Speech model loaded.');

// Transcribe the audio file
const audioClient = speechModel.createAudioClient();
const transcription = await audioClient.transcribe(
    './meeting-notes.wav'
);
console.log(`\nTranscription:\n${transcription.text}`);

// Unload the speech model to free memory
await speechModel.unload();

// Load the chat model for summarization
const chatModel = await manager.catalog.getModel('phi-3.5-mini');
await chatModel.download((progress) => {
    process.stdout.write(
        `\rDownloading chat model: ${progress.toFixed(2)}%`
    );
});
console.log('\nChat model downloaded.');

await chatModel.load();
console.log('Chat model loaded.');

// Summarize the transcription into organized notes
const chatClient = chatModel.createChatClient();
const messages = [
    {
        role: 'system',
        content: 'You are a note-taking assistant. Summarize ' +
                 'the following transcription into organized, ' +
                 'concise notes with bullet points.'
    },
    {
        role: 'user',
        content: transcription.text
    }
];

const response = await chatClient.completeChat(messages);
const summary = response.choices[0]?.message?.content;
console.log(`\nSummary:\n${summary}`);

// Clean up
await chatModel.unload();
console.log('\nDone. Models unloaded.');
```

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
