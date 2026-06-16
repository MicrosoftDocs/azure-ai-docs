---
author: samuel100
ms.author: samkemp
ms.reviewer: samkemp
ms.topic: include
ms.date: 07/23/2025
---

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.
- A working microphone connected to your computer.

## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/python/foundry-local/live-audio-transcription
```

## Install packages

[!INCLUDE [project-setup](../python-project-setup.md)]

Install [PyAudio](https://pypi.org/project/PyAudio/) for microphone capture:

```bash
pip install pyaudio
```

## Live transcribe from microphone

The following code initializes the Foundry Local SDK, loads a streaming speech model, captures audio from your microphone using PyAudio, and streams it to the live transcription API. Partial results appear as you speak, and final results are printed on a new line.

Copy and paste the following code into `app.py`:

:::code language="python" source="~/foundry-local-main/samples/python/foundry-local/live-audio-transcription/src/app.py":::

The `create_live_transcription_session` method returns a session that accepts raw PCM audio and yields transcription results as you stream chunks. PyAudio captures microphone audio at 16 kHz mono 16-bit — the format the session expects.

Run the application:

```bash
python src/app.py
```

Speak into your microphone. You see real-time transcription output:

```
Listening... (press Ctrl+C to stop)
Hello, this is a test of the live transcription feature.
It transcribes audio from the microphone in real time.
```

Press **Ctrl+C** to stop recording. The model finishes processing any remaining audio and the application exits.
