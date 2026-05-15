---
author: samuel100
ms.author: samkemp
ms.reviewer: samkemp
ms.topic: include
ms.date: 07/23/2025
---

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) version 20 or later installed.
- A working microphone connected to your computer.

## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/js/live-audio-transcription-example
```

## Install packages

[!INCLUDE [project-setup](../javascript-project-setup.md)]

Install the [naudiodon2](https://www.npmjs.com/package/naudiodon2) package for microphone capture:

```bash
npm install naudiodon2
```

## Live transcribe from microphone

The following code initializes the Foundry Local SDK, loads a streaming speech model, captures audio from your microphone using naudiodon2, and streams it to the live transcription API. Partial results appear as you speak, and final results are printed on a new line.

Copy and paste the following code into `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/live-audio-transcription/app.js":::

The `createLiveTranscriptionSession` method returns a session that accepts raw PCM audio and yields transcription results as an async generator. The naudiodon2 `AudioIO` captures microphone audio at 16 kHz mono 16-bit — the format the session expects.

Run the application:

```bash
node app.js
```

Speak into your microphone. You see real-time transcription output:

```
Listening... (press Ctrl+C to stop)
Hello, this is a test of the live transcription feature.
It transcribes audio from the microphone in real time.
```

Press **Ctrl+C** to stop recording. The model finishes processing any remaining audio and the application exits.
