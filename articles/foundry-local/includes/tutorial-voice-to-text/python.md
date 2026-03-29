---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project

[!INCLUDE [Python project setup](../python-project-setup.md)]

## Transcribe an audio file

In this step, you load a speech-to-text model and transcribe an audio file. The Foundry Local SDK uses the `whisper` model alias to select the best Whisper variant for your hardware.

1. Create a file called `app.py`.

1. Add the following code to initialize the SDK, load the speech model, and transcribe an audio file:

    ```python
    from foundry_local_sdk import Configuration, FoundryLocalManager

    # Initialize the Foundry Local SDK
    config = Configuration(app_name="note-taker")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Load the speech-to-text model
    model = manager.catalog.get_model("whisper")
    model.download(
        lambda progress: print(
            f"\rDownloading speech model: {progress:.2f}%",
            end="",
            flush=True,
        )
    )
    print()
    model.load()

    # Transcribe an audio file
    audio_client = model.get_audio_client()
    transcription = audio_client.transcribe("meeting-notes.wav")
    print(f"Transcription:\n{transcription.text}")

    # Unload the speech model to free memory
    model.unload()
    ```

    The `get_audio_client` method returns a client for audio operations. The `transcribe` method accepts a file path and returns an object with a `text` property containing the transcribed content.

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Summarize the transcription

Now use a chat model to organize the raw transcription into structured notes. Load the `phi-3.5-mini` model and send the transcription as context with a system prompt that instructs the model to produce clean, summarized notes.

Add the following code after the transcription step:

```python
# Load the chat model for summarization
chat_model = manager.catalog.get_model("phi-3.5-mini")
chat_model.download(
    lambda progress: print(
        f"\rDownloading chat model: {progress:.2f}%",
        end="",
        flush=True,
    )
)
print()
chat_model.load()

# Summarize the transcription
client = chat_model.get_chat_client()
messages = [
    {
        "role": "system",
        "content": "You are a note-taking assistant. Summarize the "
                   "following transcription into organized, concise "
                   "notes with bullet points.",
    },
    {"role": "user", "content": transcription.text},
]

response = client.complete_chat(messages)
summary = response.choices[0].message.content
print(f"\nSummary:\n{summary}")

# Unload the chat model
chat_model.unload()
```

The system prompt shapes the model's output format. By instructing it to produce "organized, concise notes with bullet points," you get structured content rather than a raw paraphrase.

## Combine into a complete app

Create a file named `app.py` and add the following complete code that transcribes an audio file and summarizes the transcription:

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="note-taker")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Load the speech-to-text model
    speech_model = manager.catalog.get_model("whisper")
    speech_model.download(
        lambda progress: print(
            f"\rDownloading speech model: {progress:.2f}%",
            end="",
            flush=True,
        )
    )
    print()
    speech_model.load()
    print("Speech model loaded.")

    # Transcribe the audio file
    audio_client = speech_model.get_audio_client()
    transcription = audio_client.transcribe("meeting-notes.wav")
    print(f"\nTranscription:\n{transcription.text}")

    # Unload the speech model to free memory
    speech_model.unload()

    # Load the chat model for summarization
    chat_model = manager.catalog.get_model("phi-3.5-mini")
    chat_model.download(
        lambda progress: print(
            f"\rDownloading chat model: {progress:.2f}%",
            end="",
            flush=True,
        )
    )
    print()
    chat_model.load()
    print("Chat model loaded.")

    # Summarize the transcription into organized notes
    client = chat_model.get_chat_client()
    messages = [
        {
            "role": "system",
            "content": "You are a note-taking assistant. "
                       "Summarize the following transcription "
                       "into organized, concise notes with "
                       "bullet points.",
        },
        {"role": "user", "content": transcription.text},
    ]

    response = client.complete_chat(messages)
    summary = response.choices[0].message.content
    print(f"\nSummary:\n{summary}")

    # Clean up
    chat_model.unload()
    print("\nDone. Models unloaded.")


if __name__ == "__main__":
    asyncio.run(main())
```

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Run the application

Run the note taker:

```bash
python app.py
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

The application first transcribes the audio content, then passes that text to a chat model that extracts key points and organizes them into structured notes.
