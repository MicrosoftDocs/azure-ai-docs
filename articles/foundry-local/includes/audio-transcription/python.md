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

## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd python/audio-transcription
```

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

:::code language="python" source="~/foundry-local-main/samples/python/audio-transcription/src/app.py" id="complete_code":::

The sample includes a `Recording.mp3` file. To transcribe a different audio file, pass the file path as an argument.

## Run the application

Run the code by using the following command:

```bash
python app.py
```

To transcribe a custom audio file:

```bash
python app.py path/to/audio.mp3
```
