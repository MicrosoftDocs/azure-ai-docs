---
author: samuel100
ms.author: samkemp
ms.reviewer: samkemp
ms.topic: include
ms.date: 06/15/2026
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).
- A working microphone connected to your computer.

## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/rust/foundry-local/live-audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

The sample uses the [cpal](https://crates.io/crates/cpal) crate for cross-platform microphone capture. The dependency is already listed in `Cargo.toml`.

## Live transcribe from microphone

The following code initializes the Foundry Local SDK, loads a streaming speech model, captures audio from your microphone using cpal, and streams it to the live transcription API. Partial results appear as you speak, and final results are printed on a new line.

Replace the contents of `src/main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/foundry-local/live-audio-transcription/src/main.rs":::

The `create_live_transcription_session` method returns a session that accepts raw Pulse-code modulation (PCM) audio and yields transcription results as an async stream. The cpal input stream captures microphone audio at 16-kHz mono, which is the format the session expects.

Run the application:

```bash
cargo run
```

Speak into your microphone. You see real-time transcription output:

```
Listening... (press Ctrl+C to stop)
Hello, this is a test of the live transcription feature.
It transcribes audio from the microphone in real time.
```

Press **Ctrl+C** to stop recording. The model finishes processing any remaining audio and the application exits.
