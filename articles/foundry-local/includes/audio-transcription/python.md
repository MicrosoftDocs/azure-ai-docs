---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.
- A local audio file to transcribe in a supported format (for example, MP3, WAV, or FLAC).

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Create project

[!INCLUDE [project-setup](../python-project-setup.md)]

## Transcribe an audio file

The following example demonstrates how to use the native audio transcription API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` object.
1. Gets a `Model` object from the model catalog using an alias. Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.
1. Downloads and loads the model variant.
1. Uses the native audio transcription API to transcribe an audio file.
1. Unloads the model.

Copy and paste the following code into a Python file named `app.py`:

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Initialize the Foundry Local SDK
    config = Configuration(app_name="app-name")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # Get a model using an alias
    model = manager.catalog.get_model("whisper-tiny")

    # Download the model (skips download if already cached)
    model.download(lambda progress: print(f"\rDownloading model: {progress:.2f}%", end="", flush=True))
    print()

    # Load the model
    model.load()

    # Get an audio client
    audio_client = model.get_audio_client()

    # Transcribe an audio file
    transcription = audio_client.transcribe("Recording.mp3")
    print(transcription.text)

    # Tidy up - unload the model
    model.unload()


if __name__ == "__main__":
    asyncio.run(main())
```

> [!NOTE]
> Replace `"Recording.mp3"` with the path to the audio file that you want to transcribe.

## Run the application

Run the code by using the following command:

```bash
python app.py
```
