---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project

[!INCLUDE [Rust project setup](../rust-project-setup.md)]

## Transcribe an audio file

In this step, you load a speech-to-text model and transcribe an audio file. The Foundry Local SDK uses the `whisper` model alias to select the best Whisper variant for your hardware.

1. Open `src/main.rs` and replace its contents with the following code to initialize the SDK, load the speech model, and transcribe an audio file:

    ```rust
    use foundry_local_sdk::{
        FoundryLocalConfig, FoundryLocalManager,
    };
    use std::io::Write;

    #[tokio::main]
    async fn main() -> anyhow::Result<()> {
        // Initialize the Foundry Local SDK
        let manager = FoundryLocalManager::create(
            FoundryLocalConfig::new("note-taker"),
        )?;

        // Load the speech-to-text model
        let speech_model = manager
            .catalog()
            .get_model("whisper")
            .await?;

        speech_model
            .download(Some(|progress: f32| {
                print!(
                    "\rDownloading speech model: {:.2}%",
                    progress
                );
                std::io::stdout().flush().unwrap();
            }))
            .await?;
        println!();

        speech_model.load().await?;
        println!("Speech model loaded.");

        // Transcribe an audio file
        let audio_client = speech_model.create_audio_client();
        let transcription = audio_client
            .transcribe("meeting-notes.wav")
            .await?;
        println!("\nTranscription:\n{}", transcription.text);

        // Unload the speech model to free memory
        speech_model.unload().await?;

        Ok(())
    }
    ```

    The `create_audio_client` method returns a client for audio operations. The `transcribe` method accepts a file path and returns an object with a `text` field containing the transcribed content.

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Summarize the transcription

Now use a chat model to organize the raw transcription into structured notes. Load the `phi-3.5-mini` model and send the transcription as context with a system prompt that instructs the model to produce clean, summarized notes.

Add the following code after the transcription step, inside the `main` function:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
};

// Load the chat model for summarization
let chat_model = manager
    .catalog()
    .get_model("phi-3.5-mini")
    .await?;

chat_model
    .download(Some(|progress: f32| {
        print!(
            "\rDownloading chat model: {:.2}%",
            progress
        );
        std::io::stdout().flush().unwrap();
    }))
    .await?;
println!();

chat_model.load().await?;
println!("Chat model loaded.");

// Summarize the transcription
let client = chat_model
    .create_chat_client()
    .temperature(0.7)
    .max_tokens(512);

let messages: Vec<ChatCompletionRequestMessage> = vec![
    ChatCompletionRequestSystemMessage::new(
        "You are a note-taking assistant. Summarize the \
         following transcription into organized, concise \
         notes with bullet points.",
    )
    .into(),
    ChatCompletionRequestUserMessage::new(
        &transcription.text,
    )
    .into(),
];

let response = client
    .complete_chat(&messages, None)
    .await?;
let summary = response.choices[0]
    .message
    .content
    .as_deref()
    .unwrap_or("");
println!("\nSummary:\n{}", summary);

// Unload the chat model
chat_model.unload().await?;
```

The system prompt shapes the model's output format. By instructing it to produce "organized, concise notes with bullet points," you get structured content rather than a raw paraphrase.

## Combine into a complete app

Replace the contents of `src/main.rs` with the following complete code that transcribes an audio file and summarizes the transcription:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage,
    ChatCompletionRequestSystemMessage,
    ChatCompletionRequestUserMessage,
    FoundryLocalConfig, FoundryLocalManager,
};
use std::io::Write;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize the Foundry Local SDK
    let manager = FoundryLocalManager::create(
        FoundryLocalConfig::new("note-taker"),
    )?;

    // Load the speech-to-text model
    let speech_model = manager
        .catalog()
        .get_model("whisper")
        .await?;

    speech_model
        .download(Some(|progress: f32| {
            print!(
                "\rDownloading speech model: {:.2}%",
                progress
            );
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();

    speech_model.load().await?;
    println!("Speech model loaded.");

    // Transcribe the audio file
    let audio_client = speech_model.create_audio_client();
    let transcription = audio_client
        .transcribe("meeting-notes.wav")
        .await?;
    println!("\nTranscription:\n{}", transcription.text);

    // Unload the speech model to free memory
    speech_model.unload().await?;

    // Load the chat model for summarization
    let chat_model = manager
        .catalog()
        .get_model("phi-3.5-mini")
        .await?;

    chat_model
        .download(Some(|progress: f32| {
            print!(
                "\rDownloading chat model: {:.2}%",
                progress
            );
            std::io::stdout().flush().unwrap();
        }))
        .await?;
    println!();

    chat_model.load().await?;
    println!("Chat model loaded.");

    // Summarize the transcription into organized notes
    let client = chat_model
        .create_chat_client()
        .temperature(0.7)
        .max_tokens(512);

    let messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestSystemMessage::new(
            "You are a note-taking assistant. Summarize \
             the following transcription into organized, \
             concise notes with bullet points.",
        )
        .into(),
        ChatCompletionRequestUserMessage::new(
            &transcription.text,
        )
        .into(),
    ];

    let response = client
        .complete_chat(&messages, None)
        .await?;
    let summary = response.choices[0]
        .message
        .content
        .as_deref()
        .unwrap_or("");
    println!("\nSummary:\n{}", summary);

    // Clean up
    chat_model.unload().await?;
    println!("\nDone. Models unloaded.");

    Ok(())
}
```

> [!NOTE]
> Replace `"meeting-notes.wav"` with the path to your audio file. Supported formats include WAV, MP3, and FLAC.

## Run the application

Run the note taker:

```bash
cargo run
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
